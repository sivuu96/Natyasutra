(function () {
  "use strict";

  var SHOW_AFTER_PX = 320;
  var button = null;
  var ticking = false;

  function prefersReducedMotion() {
    return window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function setVisible(visible) {
    if (!button) return;
    if (!visible && document.activeElement === button) {
      button.blur();
    }
    button.classList.toggle("is-visible", visible);
    button.inert = !visible;
    button.tabIndex = visible ? 0 : -1;
  }

  function updateVisibility() {
    ticking = false;
    setVisible(window.scrollY > SHOW_AFTER_PX);
  }

  function requestVisibilityUpdate() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateVisibility);
  }

  function createButton() {
    if (document.querySelector("[data-back-to-top]")) return;

    button = document.createElement("button");
    button.type = "button";
    button.className = "back-to-top-button";
    button.setAttribute("data-back-to-top", "");
    button.setAttribute("aria-label", "Back to top");
    button.title = "Back to top";
    button.inert = true;
    button.tabIndex = -1;
    button.innerHTML =
      '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      '<path d="M12 5l-7 7 1.4 1.4L11 8.8V20h2V8.8l4.6 4.6L19 12z"></path>' +
      "</svg>";

    button.addEventListener("click", function () {
      window.scrollTo({
        top: 0,
        behavior: prefersReducedMotion() ? "auto" : "smooth",
      });
    });

    document.body.appendChild(button);
    updateVisibility();
    window.addEventListener("scroll", requestVisibilityUpdate, { passive: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", createButton);
  } else {
    createButton();
  }
})();
