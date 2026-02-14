// fullstackpm.tech — Dark Mode & Mobile Menu

(function () {
  "use strict";

  // --- Dark Mode ---
  const STORAGE_KEY = "theme";

  function getPreferredTheme() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) return stored;
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function applyTheme(theme) {
    document.documentElement.classList.toggle("dark", theme === "dark");
    localStorage.setItem(STORAGE_KEY, theme);

    // Update toggle icon
    const sunIcon = document.getElementById("theme-icon-sun");
    const moonIcon = document.getElementById("theme-icon-moon");
    if (sunIcon && moonIcon) {
      sunIcon.classList.toggle("hidden", theme === "light");
      moonIcon.classList.toggle("hidden", theme === "dark");
    }
  }

  // Apply theme immediately to prevent flash
  applyTheme(getPreferredTheme());

  document.addEventListener("DOMContentLoaded", function () {
    // Re-apply to update icons after DOM is ready
    applyTheme(getPreferredTheme());

    // Dark mode toggle button
    const toggleBtn = document.getElementById("theme-toggle");
    if (toggleBtn) {
      toggleBtn.addEventListener("click", function () {
        const current = document.documentElement.classList.contains("dark")
          ? "dark"
          : "light";
        applyTheme(current === "dark" ? "light" : "dark");
      });
    }

    // --- Mobile Menu ---
    const menuBtn = document.getElementById("mobile-menu-btn");
    const mobileMenu = document.getElementById("mobile-menu");

    if (menuBtn && mobileMenu) {
      menuBtn.addEventListener("click", function () {
        const isOpen = !mobileMenu.classList.contains("hidden");
        mobileMenu.classList.toggle("hidden");
        menuBtn.setAttribute("aria-expanded", String(!isOpen));
      });

      // Close menu when clicking a link
      mobileMenu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
          mobileMenu.classList.add("hidden");
          menuBtn.setAttribute("aria-expanded", "false");
        });
      });
    }
  });
})();
