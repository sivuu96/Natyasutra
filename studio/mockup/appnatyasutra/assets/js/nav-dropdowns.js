(function () {
  "use strict";

  var COMPACT_MQ = window.matchMedia("(max-width: 1023px)");
  var backdropEl = null;

  function syncNavHeight() {
    var nav = document.querySelector("nav");
    if (!nav) return;
    document.documentElement.style.setProperty(
      "--site-nav-height",
      nav.getBoundingClientRect().height + "px"
    );
  }

  function ensureBackdrop() {
    if (backdropEl) return backdropEl;
    backdropEl = document.createElement("div");
    backdropEl.id = "navDropdownBackdrop";
    backdropEl.className = "nav-dropdown-backdrop";
    backdropEl.setAttribute("aria-hidden", "true");
    backdropEl.addEventListener("click", closeAllNavDropdowns);
    document.body.appendChild(backdropEl);
    return backdropEl;
  }

  function setBackdropVisible(visible) {
    if (!COMPACT_MQ.matches) visible = false;
    var backdrop = ensureBackdrop();
    backdrop.classList.toggle("is-visible", visible);
    backdrop.setAttribute("aria-hidden", visible ? "false" : "true");
    document.body.classList.toggle("nav-dropdown-open", visible);
  }

  function resetNavDropdownPosition(menu) {
    menu.style.position = "";
    menu.style.top = "";
    menu.style.right = "";
    menu.style.left = "";
    menu.style.width = "";
    menu.style.maxHeight = "";
    menu.style.transformOrigin = "";
  }

  function positionNavDropdown(menu, btn) {
    if (!COMPACT_MQ.matches) {
      resetNavDropdownPosition(menu);
      return;
    }

    syncNavHeight();
    var nav = document.querySelector("nav");
    if (!nav) return;

    var navRect = nav.getBoundingClientRect();
    var btnRect = btn.getBoundingClientRect();
    var gutter = Math.max(12, Math.min(16, window.innerWidth * 0.04));
    var isAccount = menu.classList.contains("nav-dropdown-panel--account");
    var maxWidth = isAccount ? 224 : 352;
    var width = Math.min(maxWidth, window.innerWidth - gutter * 2);
    var right = window.innerWidth - btnRect.right;
    right = Math.max(gutter, Math.min(right, window.innerWidth - width - gutter));
    var maxHeight = window.innerHeight - navRect.bottom - gutter - 8;

    menu.style.position = "fixed";
    menu.style.top = Math.round(navRect.bottom + 8) + "px";
    menu.style.right = Math.round(right) + "px";
    menu.style.left = "auto";
    menu.style.width = Math.round(width) + "px";
    menu.style.maxHeight = Math.max(180, Math.round(maxHeight)) + "px";
    menu.style.transformOrigin = "top right";
  }

  function closeAllNavDropdowns() {
    document.querySelectorAll(".nav-dropdown-panel.is-open").forEach(function (panel) {
      panel.classList.remove("is-open");
      resetNavDropdownPosition(panel);
      var btn = panel.parentElement && panel.parentElement.querySelector("button[aria-haspopup]");
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
    setBackdropVisible(false);
  }

  function initNavDropdown(btnId, menuId, wrapId) {
    var btn = document.getElementById(btnId);
    var menu = document.getElementById(menuId);
    var wrap = document.getElementById(wrapId);
    if (!btn || !menu || !wrap) return;

    function close() {
      menu.classList.remove("is-open");
      btn.setAttribute("aria-expanded", "false");
      resetNavDropdownPosition(menu);
      if (!document.querySelector(".nav-dropdown-panel.is-open")) {
        setBackdropVisible(false);
      }
    }

    function open() {
      positionNavDropdown(menu, btn);
      menu.classList.add("is-open");
      btn.setAttribute("aria-expanded", "true");
      setBackdropVisible(true);
    }

    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      document.querySelectorAll(".nav-dropdown-panel.is-open").forEach(function (panel) {
        if (panel !== menu) {
          panel.classList.remove("is-open");
          resetNavDropdownPosition(panel);
          var otherBtn = panel.parentElement && panel.parentElement.querySelector("button[aria-haspopup]");
          if (otherBtn) otherBtn.setAttribute("aria-expanded", "false");
        }
      });

      if (menu.classList.contains("is-open")) {
        close();
      } else {
        open();
      }
    });

    document.addEventListener("click", function (e) {
      if (!wrap.contains(e.target)) close();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  function initNavDropdowns() {
    initNavDropdown("cartDropdownBtn", "cartDropdownMenu", "cartDropdownWrap");
    initNavDropdown("avatarDropdownBtn", "avatarDropdownMenu", "avatarDropdownWrap");

    var mobileBtn = document.getElementById("mobileMenuBtn");
    if (mobileBtn) {
      mobileBtn.addEventListener("click", closeAllNavDropdowns);
    }

    window.addEventListener(
      "resize",
      function () {
        syncNavHeight();
        document.querySelectorAll(".nav-dropdown-panel.is-open").forEach(function (panel) {
          var btn = panel.parentElement && panel.parentElement.querySelector("button[aria-haspopup]");
          if (!btn) return;
          if (COMPACT_MQ.matches) {
            positionNavDropdown(panel, btn);
          } else {
            resetNavDropdownPosition(panel);
            setBackdropVisible(false);
          }
        });
      },
      { passive: true }
    );

    window.addEventListener(
      "scroll",
      function () {
        if (!COMPACT_MQ.matches) return;
        document.querySelectorAll(".nav-dropdown-panel.is-open").forEach(function (panel) {
          var btn = panel.parentElement && panel.parentElement.querySelector("button[aria-haspopup]");
          if (btn) positionNavDropdown(panel, btn);
        });
      },
      { passive: true }
    );
  }

  function init() {
    syncNavHeight();
    initNavDropdowns();
  }

  window.NatyaNavDropdowns = {
    closeAll: closeAllNavDropdowns,
    syncHeight: syncNavHeight,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
