const navToggle = document.getElementById("nav-toggle");
const navList = document.getElementById("nav-list");
const themeToggle = document.getElementById("theme-toggle");
const yearNode = document.getElementById("year");

if (yearNode) {
  yearNode.textContent = new Date().getFullYear();
}

// Toggle mobile navigation visibility.
if (navToggle && navList) {
  navToggle.addEventListener("click", () => {
    const expanded = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!expanded));
    navList.classList.toggle("open");
  });

  navList.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navToggle.setAttribute("aria-expanded", "false");
      navList.classList.remove("open");
    });
  });
}

const THEME_KEY = "portfolio-theme";
const savedTheme = localStorage.getItem(THEME_KEY);

if (savedTheme === "dark") {
  document.body.setAttribute("data-theme", "dark");
}

if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    const isDark = document.body.getAttribute("data-theme") === "dark";
    if (isDark) {
      document.body.removeAttribute("data-theme");
      localStorage.setItem(THEME_KEY, "light");
    } else {
      document.body.setAttribute("data-theme", "dark");
      localStorage.setItem(THEME_KEY, "dark");
    }
  });
}

// Animate sections when they enter the viewport.
const revealElements = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }
        entry.target.classList.add("visible");
        obs.unobserve(entry.target);
      });
    },
    {
      threshold: 0.18,
    }
  );

  revealElements.forEach((el) => observer.observe(el));
} else {
  revealElements.forEach((el) => el.classList.add("visible"));
}
