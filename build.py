#!/usr/bin/env python3
"""
Build aryangorde.com.

Renders build_src/ into a single self-contained index.html plus responsive
image derivatives. No Node, no CDN, no runtime dependencies in the browser —
the CSS and JS are inlined at build time, so the deployed site is one HTML
file and a handful of images.

    python3 build.py              build
    python3 build.py --check      build into a temp dir and diff; non-zero
                                  exit if index.html is stale (for CI)
    python3 build.py --serve      build, then serve on :5500 and rebuild on
                                  change

Why a build step for a static page: the content lives in content.py as plain
Python data, so adding a project is appending a dict rather than copy-pasting
a <div>. The build also enforces three invariants that are easy to break by
hand and silent when broken:

  1. every utility class used in a template is actually defined in the CSS
  2. every internal #anchor points at an id that exists
  3. every nav entry matches a real section

Any of those failing fails the build rather than shipping a subtly broken page.
"""

from __future__ import annotations

import argparse
import importlib.util
import filecmp
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
except ImportError:
    sys.exit("jinja2 is not installed.  pip install -r requirements.txt")

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is not installed.  pip install -r requirements.txt")

ROOT = Path(__file__).parent.resolve()
SRC = ROOT / "build_src"
TEMPLATES = SRC / "templates"
STATIC = SRC / "static"
SRC_IMAGES = SRC / "images"
OUT_IMAGES = ROOT / "images"
OUT_HTML = ROOT / "index.html"

# Widths to emit for the headshot. The photo renders at most ~340 CSS px, so
# 680 covers 2x retina; anything larger is wasted bytes for this layout.
PHOTO_WIDTHS = [280, 340, 520, 680]
WEBP_QUALITY = 82
JPEG_QUALITY = 88


# ---------------------------------------------------------------------------
# images
# ---------------------------------------------------------------------------

def build_images(content, out_dir: Path, quiet=False) -> dict:
    """Emit WebP + JPEG derivatives and return the data the template needs.

    Upscaling is deliberately refused: if the source is narrower than a target
    width we skip that width rather than invent detail that isn't there.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    src_path = SRC_IMAGES / content.SITE["photo"]
    if not src_path.exists():
        sys.exit(f"source photo missing: {src_path}")

    im = Image.open(src_path)
    im = im.convert("RGB")
    sw, sh = im.size
    stem = Path(content.SITE["photo"]).stem

    widths = [w for w in PHOTO_WIDTHS if w <= sw]
    # If the source is smaller than every rung, emit its native width so we
    # don't throw away real pixels. If it's larger, the ladder already covers
    # what the layout can use and a source-sized rung would just be dead weight
    # nobody downloads.
    if sw < max(PHOTO_WIDTHS) and sw not in widths:
        widths.append(sw)
    widths = sorted(set(widths))

    if not quiet and max(PHOTO_WIDTHS) > sw:
        skipped = [w for w in PHOTO_WIDTHS if w > sw]
        print(f"  photo source is only {sw}x{sh}px — skipping {skipped} rather than "
              f"upscaling (would invent detail).")
        print(f"  → the hero renders at up to 340 CSS px, so this photo is soft on "
              f"retina. A larger original would look noticeably sharper.")

    webp, jpg, written = [], [], []
    for w in widths:
        h = round(sh * w / sw)
        resized = im.resize((w, h), Image.LANCZOS)

        wp = out_dir / f"{stem}-{w}.webp"
        resized.save(wp, "WEBP", quality=WEBP_QUALITY, method=6)
        webp.append(f"images/{wp.name} {w}w")
        written.append(wp)

        jp = out_dir / f"{stem}-{w}.jpg"
        resized.save(jp, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        jpg.append(f"images/{jp.name} {w}w")
        written.append(jp)

    largest = max(widths)
    if not quiet:
        total = sum(p.stat().st_size for p in written)
        print(f"  images: {len(written)} files, {total/1024:.0f} KB total "
              f"({', '.join(str(w) for w in widths)}px)")

    initials = "".join(part[0] for part in content.SITE["name"].split()[:2]).upper()
    return {
        "webp_srcset": ", ".join(webp),
        "jpg_srcset": ", ".join(jpg),
        "fallback": f"images/{stem}-{largest}.jpg",
        "og": f"images/{stem}-{largest}.jpg",
        "width": sw,
        "height": sh,
        "alt": content.SITE["photo_alt"],
        "initials": initials,
    }


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def defined_css_classes(css: str) -> set[str]:
    """Class names the stylesheet defines, un-escaping CSS identifier escapes
    (`.sm\\:px-6` in CSS is the class `sm:px-6` in markup)."""
    found = set()
    for m in re.finditer(r"\.((?:[A-Za-z0-9_-]|\\.)+)", css):
        found.add(re.sub(r"\\(.)", r"\1", m.group(1)))
    return found


def used_html_classes(html: str) -> set[str]:
    body = re.sub(r"<style>.*?</style>", "", html, flags=re.S)
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    used = set()
    for m in re.finditer(r'class="([^"]*)"', body):
        used.update(m.group(1).split())
    return used


def run_checks(html: str, css: str, content) -> list[str]:
    """Return a list of problems. Empty list means the page is coherent."""
    problems = []

    # 1. every class used in markup is defined somewhere in the CSS
    undefined = sorted(used_html_classes(html) - defined_css_classes(css))
    for cls in undefined:
        problems.append(f"class '{cls}' is used in markup but not defined in CSS")

    # 2. internal anchors resolve
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    for href in set(re.findall(r'href="#([^"]+)"', html)):
        if href not in ids:
            problems.append(f"anchor '#{href}' points at an id that doesn't exist")

    # 3. nav matches real sections
    section_ids = set(re.findall(r'<section[^>]*\bid="([^"]+)"', html))
    for nav_id, label in content.NAV:
        if nav_id not in section_ids:
            problems.append(f"nav entry '{label}' -> #{nav_id} has no matching section")

    # 4. one h1, no skipped heading levels
    levels = [int(m) for m in re.findall(r"<h([1-6])\b", html)]
    if levels.count(1) != 1:
        problems.append(f"expected exactly one <h1>, found {levels.count(1)}")
    for a, b in zip(levels, levels[1:]):
        if b - a > 1:
            problems.append(f"heading level jumps from h{a} to h{b}")
            break

    # 5. images carry alt text
    for tag in re.findall(r"<img\b[^>]*>", html):
        if "alt=" not in tag:
            problems.append(f"<img> without alt: {tag[:70]}")

    # 6. nothing external survived the inlining
    for m in re.finditer(r'(?:src|href)="(https?://[^"]+)"', html):
        url = m.group(1)
        if not any(k in url for k in ("aryangorde.com", "github.com", "linkedin.com")):
            problems.append(f"unexpected external reference: {url}")

    return problems


# ---------------------------------------------------------------------------
# render
# ---------------------------------------------------------------------------

def load_content():
    """Import build_src/content.py fresh, every time.

    Deliberately bypasses __pycache__. Python invalidates bytecode on
    (mtime, size), and content edits that keep the byte length identical —
    renaming a nav id, flipping a single character — can slip through that
    check and silently rebuild the site from the previous version's data.
    A build tool must never do that.
    """
    sys.dont_write_bytecode = True
    src = SRC / "content.py"
    spec = importlib.util.spec_from_file_location("site_content", src)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(out_html: Path, out_images: Path, quiet=False) -> str:
    content = load_content()

    css = "\n\n".join([
        (STATIC / "css" / "utilities.css").read_text(encoding="utf-8"),
        (STATIC / "css" / "site.css").read_text(encoding="utf-8"),
    ])
    js = (STATIC / "js" / "site.js").read_text(encoding="utf-8")

    photo = build_images(content, out_images, quiet=quiet)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        undefined=StrictUndefined,      # a typo'd variable fails the build
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,               # content.py holds intentional markup
    )

    # The floating planes/motes in the contact section. Data, not markup, so
    # the parallax depths stay readable in one place.
    depth_layers = [
        {"kind": "plane", "depth": 0.06, "style": "width:min(44vw,400px); height:min(28vw,240px); left:-6%; top:14%; transform:rotate(-8deg)"},
        {"kind": "plane", "depth": 0.12, "style": "width:min(36vw,320px); height:min(24vw,210px); right:-5%; top:54%; transform:rotate(7deg)"},
        {"kind": "dot",   "depth": 0.19, "style": "width:14px; height:14px; left:16%; top:22%"},
        {"kind": "dot",   "depth": 0.27, "style": "width:9px;  height:9px;  left:76%; top:16%"},
        {"kind": "dot",   "depth": 0.15, "style": "width:18px; height:18px; left:62%; top:76%"},
        {"kind": "dot",   "depth": 0.23, "style": "width:11px; height:11px; left:30%; top:84%"},
    ]

    html = env.get_template("index.html.j2").render(
        site=content.SITE,
        nav=content.NAV,
        hero=content.HERO,
        about=content.ABOUT,
        stack=content.STACK,
        featured=content.FEATURED,
        projects=content.PROJECTS,
        labs=content.LABS,
        experience=content.EXPERIENCE,
        education=content.EDUCATION,
        skills=content.SKILLS,
        stats=content.STATS,
        stats_feature=content.STATS_FEATURE,
        contact=content.CONTACT,
        marquees=content.MARQUEES,
        borrowed=content.BORROWED,
        depth_layers=depth_layers,
        photo=photo,
        css=css,
        js=js,
        year=datetime.now().year,
        stats_meta={"sections": len(content.NAV) + 1},
    )

    problems = run_checks(html, css, content)
    if problems:
        print("\n  BUILD FAILED — the page would be subtly broken:\n", file=sys.stderr)
        for p in problems:
            print(f"    ✗ {p}", file=sys.stderr)
        print(file=sys.stderr)
        sys.exit(1)

    out_html.write_text(html, encoding="utf-8")
    return html


def report(html: str, out_html: Path):
    raw = len(html.encode())
    gz = len(subprocess.run(["gzip", "-c", str(out_html)],
                            capture_output=True).stdout)
    print(f"  {out_html.name}: {raw/1024:.1f} KB  ({gz/1024:.1f} KB gzipped)")

    # What a 2x desktop actually fetches: the photo renders at ~340 CSS px, so
    # the browser picks the 680w WebP. Estimating with the largest file on disk
    # would overstate this by ~10x and measure a download nobody performs.
    target = max(PHOTO_WIDTHS)
    hero = OUT_IMAGES / f"aryan-{target}.webp"
    if not hero.exists():                       # source smaller than the ladder
        cands = sorted(OUT_IMAGES.glob("aryan-*.webp"),
                       key=lambda p: p.stat().st_size)
        hero = cands[-1] if cands else None
    hero_kb = hero.stat().st_size / 1024 if hero else 0
    print(f"  first load ≈ {gz/1024 + hero_kb:.0f} KB "
          f"(html + {hero.name if hero else 'no photo'} @2x)")
    print(f"  checks passed: classes, anchors, nav, headings, alt text, no external refs")


# ---------------------------------------------------------------------------
# entry
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Build aryangorde.com")
    ap.add_argument("--check", action="store_true",
                    help="verify index.html is up to date; non-zero exit if stale")
    ap.add_argument("--serve", action="store_true",
                    help="build, serve on :5500, rebuild on file change")
    args = ap.parse_args()

    if args.check:
        with tempfile.TemporaryDirectory() as td:
            tmp_html = Path(td) / "index.html"
            build(tmp_html, Path(td) / "images", quiet=True)
            if not OUT_HTML.exists():
                sys.exit("index.html has not been built yet — run: python3 build.py")
            if filecmp.cmp(tmp_html, OUT_HTML, shallow=False):
                print("index.html is up to date with build_src/")
                return
            sys.exit("index.html is STALE — rebuild with: python3 build.py")

    print("building…")
    html = build(OUT_HTML, OUT_IMAGES)
    report(html, OUT_HTML)
    print("done.")

    if args.serve:
        import http.server, socketserver, threading, time
        watched = list(SRC.rglob("*.j2")) + list(SRC.rglob("*.css")) \
                  + list(SRC.rglob("*.js")) + [SRC / "content.py"]

        def watch():
            stamps = {p: p.stat().st_mtime for p in watched if p.exists()}
            while True:
                time.sleep(0.5)
                for p in watched:
                    if not p.exists():
                        continue
                    m = p.stat().st_mtime
                    if stamps.get(p) != m:
                        stamps[p] = m
                        print(f"\n{p.relative_to(ROOT)} changed — rebuilding…")
                        try:
                            h = build(OUT_HTML, OUT_IMAGES, quiet=True)
                            report(h, OUT_HTML)
                        except SystemExit as e:
                            print(f"  build failed: {e}")

        threading.Thread(target=watch, daemon=True).start()
        handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
            *a, directory=str(ROOT), **kw)
        with socketserver.TCPServer(("", 5500), handler) as httpd:
            print("\nserving http://localhost:5500  (ctrl-c to stop)")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nstopped.")


if __name__ == "__main__":
    main()
