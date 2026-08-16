# aryangorde.com

Personal portfolio for Aryan Gorde — backend & full-stack developer.
Built with Python. Deployed as static files on GitHub Pages.

**Design:** maximalism as the house style, with one signature device quoted
from each of nine other UI design eras. Heavily animated, and every animation
is gated behind `prefers-reduced-motion`.

---

## Build

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 build.py
```

That renders `build_src/` into a single self-contained `index.html` plus
responsive image derivatives in `images/`.

| Command | What it does |
| --- | --- |
| `python3 build.py` | Build `index.html` + images |
| `python3 build.py --serve` | Build, serve on :5500, rebuild on file change |
| `python3 build.py --check` | Fail (non-zero exit) if `index.html` is stale — for CI |

## Why a build step for a static page

The content lives in `build_src/content.py` as plain Python data. Adding a
project is appending a dict, not copy-pasting a `<div>`. The build also
enforces four invariants that are easy to break by hand and silent when broken:

1. every CSS class used in markup is actually defined in the stylesheet
2. every internal `#anchor` points at an id that exists
3. every nav entry matches a real section
4. exactly one `<h1>`, no skipped heading levels, no `<img>` without `alt`

Any of those failing **fails the build** rather than shipping a subtly broken
page. There is also a check that no external URL survived inlining, so the
"zero dependencies" claim can't quietly stop being true.

## Layout

```
build.py                     the build
requirements.txt             jinja2, pillow
build_src/
  content.py                 ← all the words live here
  templates/
    base.html.j2             page skeleton, <head>, inlining
    index.html.j2            section order
    macros.html.j2           components + the colour contract
    sections/*.html.j2       one file per section
  static/
    css/utilities.css        hand-written utility layer
    css/site.css             the design system
    js/site.js               behaviour (progressive enhancement only)
  images/aryan.jpg           source photo (build resizes it)

index.html                   ← GENERATED, do not edit
images/aryan-*.{webp,jpg}    ← GENERATED
```

## Output

One HTML file, ~73 KB (~19 KB gzipped), with CSS and JS inlined.
**No CDN, no webfonts, no runtime dependencies** — the deployed site makes zero
external requests. First load is roughly 50 KB including one photo derivative.

## The colour contract

Maximalism gets loud, so legibility is enforced structurally rather than left
to taste. Two rules, both checked:

1. Every run of text sits on an **opaque plate**. Pattern and colour happen
   *behind* plates, never under words.
2. Accents are only ever used at these verified pairings:

   | Surface | Text | Ratio |
   | --- | --- | --- |
   | `#c4007a` pink | white | 5.7:1 |
   | `#00d5ff` cyan | black | 12.0:1 |
   | `#b6ff00` lime | black | 16.3:1 |
   | `#7b2cff` violet | white | 6.9:1 |
   | `#ffe500` yellow | black | 17.0:1 |
   | `#000` black | yellow / cyan | 17.0:1 / 12.0:1 |

   Note the asymmetry: cyan on **black** is 12:1, but cyan on **pink** is
   3.3:1 and fails. Accent inks are keyed per-surface in `macros.html.j2`
   (`HEAD_INK` / `MUTED_INK`) precisely because that doesn't generalise.

Measured on the built page: **0 contrast failures across 200 text elements,
worst case 5.17:1** against a 4.5:1 requirement. All 32 focusable elements
have a visible ring, weakest 3.08:1 against a 3:1 requirement.

## The nine borrowed devices

| Era | Device | Where |
| --- | --- | --- |
| Skeuomorphism | brass bevel that depresses on press | hero résumé button |
| Neomorphism | soft extrusion in the page's own yellow | about tile |
| Glassmorphism | frosted panel over the pattern | about bio |
| Claymorphism | puffy, oversized radii | frontend card |
| Minimalism | full-bleed strip of restraint | DebtClear |
| Brutalism | materials left exposed | experience |
| Liquid glass | refractive rim, travelling sheen | hero photo badge |
| Bento grid | unequal tiles, uniform gutters | stats |
| Spatial UI | layers at different depths | contact |

Each is labelled on the page with a `credit` chip, so the quotation reads as
deliberate rather than as an inconsistency.

## Accessibility

- `prefers-reduced-motion` is the default state, not a fallback — nothing
  animates unless motion is explicitly on.
- The "Reduce motion" button in the nav doubles as the pause control the
  looping marquees need (WCAG 2.2.2). Nothing flashes faster than 0.5 Hz.
- Skip link, semantic landmarks, one `h1`, no skipped heading levels.
- Scroll reveals disarm themselves if `IntersectionObserver` never fires, so
  content can never be stranded at `opacity: 0`.
- Everything works with JavaScript disabled; JS only adds motion and counters.

## Deployment

GitHub Pages, `main` branch, root folder. `CNAME` holds `aryangorde.com`.

Commit both the sources **and** the generated `index.html` + `images/`, since
Pages serves the files directly and does not run the build.

```bash
python3 build.py && git add -A && git commit -m "rebuild" && git push
```

To catch a forgotten rebuild, run `python3 build.py --check` in CI.
