/**
 * Skrip global PortfolioWeb.
 * Menangani: toggle tema, menu mobile, dan dismiss pesan flash.
 */
(function () {
  "use strict";

  // ------------------------------------------------------------------
  // Toggle tema (terang/gelap) — preferensi tersimpan di localStorage
  // ------------------------------------------------------------------
  var themeToggles = document.querySelectorAll("[data-theme-toggle]");

  var syncPressedState = function () {
    var isDark = document.documentElement.classList.contains("dark");
    themeToggles.forEach(function (btn) {
      btn.setAttribute("aria-pressed", String(isDark));
    });
  };

  themeToggles.forEach(function (button) {
    button.addEventListener("click", function () {
      var isDark = document.documentElement.classList.toggle("dark");
      localStorage.setItem("theme", isDark ? "dark" : "light");
      syncPressedState();
    });
  });

  syncPressedState();

  // ------------------------------------------------------------------
  // Menu mobile (hamburger)
  // ------------------------------------------------------------------
  var menuToggle = document.querySelector("[data-menu-toggle]");
  var mobileMenu = document.querySelector("[data-mobile-menu]");

  if (menuToggle && mobileMenu) {
    var iconOpen = menuToggle.querySelector("[data-icon-open]");
    var iconClose = menuToggle.querySelector("[data-icon-close]");

    var setMenuOpen = function (open) {
      mobileMenu.classList.toggle("hidden", !open);
      if (iconOpen) iconOpen.classList.toggle("hidden", open);
      if (iconClose) iconClose.classList.toggle("hidden", !open);
      menuToggle.setAttribute("aria-expanded", String(open));
    };

    menuToggle.addEventListener("click", function () {
      setMenuOpen(mobileMenu.classList.contains("hidden"));
    });

    mobileMenu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setMenuOpen(false);
      });
    });
  }

  // ------------------------------------------------------------------
  // Dismiss pesan flash
  // ------------------------------------------------------------------
  document.querySelectorAll("[data-dismiss-alert]").forEach(function (button) {
    button.addEventListener("click", function () {
      var alertBox = button.closest(".alert");
      if (alertBox) alertBox.remove();
    });
  });
})();