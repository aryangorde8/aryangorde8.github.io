/* ==========================================================================
   Progressive enhancement only. Delete this whole block and you still have a
   complete, readable, navigable page — you just lose motion and the counters.
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var supportsIO = "IntersectionObserver" in window;

  /* ---- 1. Motion gate ---------------------------------------------------
     prefers-reduced-motion is the source of truth; the button overrides it in
     either direction and the choice persists. It also serves as the pause
     control for the looping marquees (WCAG 2.2.2). */
  var mq = window.matchMedia("(prefers-reduced-motion: reduce)");
  var stored = null;
  try { stored = localStorage.getItem("motion"); } catch (e) {}

  function applyMotion(mode) {
    root.setAttribute("data-motion", mode);
    root.classList.toggle("reveal-armed", mode === "full" && supportsIO);
    document.querySelectorAll("[data-motion-toggle]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", mode === "reduced" ? "true" : "false");
    });
  }

  var motionMode = stored || (mq.matches ? "reduced" : "full");
  applyMotion(motionMode);

  if (mq.addEventListener) {
    mq.addEventListener("change", function (e) {
      if (stored) return;                        // an explicit choice wins
      motionMode = e.matches ? "reduced" : "full";
      applyMotion(motionMode);
    });
  }

  document.querySelectorAll("[data-motion-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      motionMode = motionMode === "full" ? "reduced" : "full";
      stored = motionMode;
      try { localStorage.setItem("motion", motionMode); } catch (e) {}
      applyMotion(motionMode);
    });
  });

  /* ---- 2. Photo fallback ------------------------------------------------
     If images/aryan.jpg isn't there yet, show an initials tile instead of a
     broken-image icon. Self-disables once the file exists. */
  document.querySelectorAll("[data-photo-frame] img").forEach(function (img) {
    function fail() { img.closest("[data-photo-frame]").classList.add("is-missing"); }
    img.addEventListener("error", fail);
    if (img.complete && img.naturalWidth === 0) fail();
  });

  /* ---- 3. Scroll reveal -------------------------------------------------- */
  if (supportsIO) {
    var revealObserver = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("rv-in");
        obs.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.04 });
    document.querySelectorAll(".rv").forEach(function (el) { revealObserver.observe(el); });

    // Failsafe: on a healthy page the above-the-fold items reveal instantly.
    // If nothing has after 3s the observer isn't delivering, so disarm rather
    // than leave the page stranded at opacity 0.
    setTimeout(function () {
      if (!document.querySelector(".rv.rv-in")) root.classList.remove("reveal-armed");
    }, 3000);
  }

  /* ---- 4. Nav scroll spy -------------------------------------------------- */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".nav-link"));
  var sections = navLinks
    .map(function (l) { return document.getElementById(l.getAttribute("data-nav")); })
    .filter(Boolean);

  if (supportsIO && sections.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (l) {
          l.setAttribute("aria-current", l.getAttribute("data-nav") === entry.target.id ? "true" : "false");
        });
      });
    }, { rootMargin: "-45% 0px -45% 0px" });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---- 5. Stat counters --------------------------------------------------
     Count up once, on reveal, and only when motion is on. The final value is
     already in the HTML, so this never invents or hides a number. */
  if (supportsIO) {
    var countObserver = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        obs.unobserve(entry.target);
        if (root.getAttribute("data-motion") !== "full") return;

        var el = entry.target;
        var target = parseInt(el.getAttribute("data-count"), 10);
        var suffix = el.getAttribute("data-suffix") || "";
        if (isNaN(target)) return;

        var started = null, dur = 900;
        function step(ts) {
          if (started === null) started = ts;
          var p = Math.min((ts - started) / dur, 1);
          el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix;
          if (p < 1) requestAnimationFrame(step);
        }
        el.textContent = "0" + suffix;
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    document.querySelectorAll("[data-count]").forEach(function (el) { countObserver.observe(el); });
  }

  /* ---- 5b. Frost activation ----------------------------------------------
     backdrop-filter is the most expensive thing on this page. Switch it on
     only for the borrowed glass/liquid-glass panels while they're near the
     viewport, so offscreen blur never costs a frame. */
  if (supportsIO) {
    var frostObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        entry.target.classList.toggle("is-live", entry.isIntersecting);
      });
    }, { rootMargin: "250px 0px 250px 0px" });
    document.querySelectorAll("[data-frost]").forEach(function (el) { frostObserver.observe(el); });
  } else {
    document.querySelectorAll("[data-frost]").forEach(function (el) { el.classList.add("is-live"); });
  }

  /* ---- 5c. Spatial parallax ----------------------------------------------
     Borrowed from spatial UI, for the contact section only. Motion-gated and
     fine-pointer-gated: a phone has no hover and doesn't need the cost.
     Transform-only, batched into one rAF per scroll event. */
  var finePointer = window.matchMedia("(pointer: fine)").matches;
  var spatial = document.getElementById("contact");
  var depthLayers = spatial
    ? Array.prototype.slice.call(spatial.querySelectorAll("[data-depth]"))
    : [];
  var pointerX = 0, pointerY = 0, ticking = false;

  function parallaxOn() {
    return root.getAttribute("data-motion") === "full" && finePointer && depthLayers.length > 0;
  }

  function updateParallax() {
    if (!parallaxOn()) return;
    var rect = spatial.getBoundingClientRect();
    if (rect.bottom < 0 || rect.top > window.innerHeight) return;

    // -1 entering from below, +1 leaving above
    var progress = 1 - (rect.top + rect.height / 2) / (window.innerHeight / 2 + rect.height / 2);

    depthLayers.forEach(function (layer) {
      var d = parseFloat(layer.getAttribute("data-depth")) || 0;
      var y = progress * d * -170;
      var x = pointerX * d * 36;
      var ry = pointerX * d * 10;
      var rx = pointerY * d * -7;
      layer.style.transform =
        "translate3d(" + x.toFixed(1) + "px," + y.toFixed(1) + "px,0)" +
        " rotateY(" + ry.toFixed(2) + "deg) rotateX(" + rx.toFixed(2) + "deg)";
    });
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { updateParallax(); ticking = false; });
  }
  window.addEventListener("scroll", onScroll, { passive: true });

  if (spatial) {
    spatial.addEventListener("pointermove", function (e) {
      if (!parallaxOn()) return;
      var r = spatial.getBoundingClientRect();
      pointerX = (e.clientX - r.left) / r.width * 2 - 1;
      pointerY = (e.clientY - r.top) / r.height * 2 - 1;
      onScroll();
    }, { passive: true });

    spatial.addEventListener("pointerleave", function () {
      pointerX = 0; pointerY = 0; onScroll();
    }, { passive: true });
  }

  /* ---- 6. Copy email ------------------------------------------------------ */
  var copyBtn = document.getElementById("copy-email");
  var copyStatus = document.getElementById("copy-status");
  if (copyBtn && navigator.clipboard) {
    /* The address comes from the button's data-email, which the build fills
       from content.py. Hardcoding it here once meant two copies to keep in
       sync, and they drifted. */
    var addr = copyBtn.getAttribute("data-email") || "";
    copyBtn.addEventListener("click", function () {
      navigator.clipboard.writeText(addr).then(function () {
        if (copyStatus) copyStatus.textContent = "Copied to clipboard.";
      }).catch(function () {
        if (copyStatus) copyStatus.textContent = "Couldn't copy — it's " + addr;
      });
    });
  } else if (copyBtn) {
    copyBtn.hidden = true;
  }

  /* ---- 7. Housekeeping ----------------------------------------------------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---- 8. Retire the old service worker ------------------------------------
     The previous build was a React bundle and sw.js cached /assets/*, which no
     longer exists. Left registered, returning visitors can be served the old
     app from cache. Delete this block if you reintroduce a service worker. */
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.getRegistrations().then(function (regs) {
      regs.forEach(function (r) { r.unregister(); });
    }).catch(function () {});
    if (window.caches && caches.keys) {
      caches.keys().then(function (keys) {
        keys.forEach(function (k) { caches.delete(k); });
      }).catch(function () {});
    }
  }
})();
