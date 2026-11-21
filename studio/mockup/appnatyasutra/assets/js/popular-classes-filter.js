(function () {
  "use strict";

  function shouldShowCard(filterValue, cardCategory) {
    if (!filterValue || filterValue === "all" || filterValue === "art-forms") {
      return true;
    }
    return cardCategory === filterValue;
  }

  function initPopularClassesSection(section) {
    var btn =
      section.querySelector("[data-popular-classes-trigger]") ||
      section.querySelector("#classDropdownBtn");
    var menu =
      section.querySelector("[data-popular-classes-menu]") ||
      section.querySelector("#classDropdownMenu");
    var arrow =
      section.querySelector("[data-popular-classes-arrow]") ||
      section.querySelector("#classDropdownArrow");
    var selectedText =
      section.querySelector("[data-popular-classes-selected]") ||
      section.querySelector("#classSelectedText");
    var grid =
      section.querySelector("[data-popular-classes-grid]") ||
      section.querySelector("#compositionGrid");

    if (!btn || !menu || !grid) return;

    var options = section.querySelectorAll(".class-dropdown-option");
    var cards = grid.querySelectorAll("[data-category]");

    function closeDropdown() {
      menu.classList.remove("opacity-100", "scale-100");
      menu.classList.add("opacity-0", "scale-95");
      if (arrow) arrow.classList.remove("rotate-180");
      setTimeout(function () {
        menu.classList.add("hidden");
      }, 200);
    }

    function applyFilter(filterValue) {
      cards.forEach(function (card) {
        var cardCategory = card.getAttribute("data-category");
        if (shouldShowCard(filterValue, cardCategory)) {
          card.style.display = "flex";
          card.style.opacity = "0";
          setTimeout(function () {
            card.style.opacity = "1";
            card.style.transition = "opacity 300ms ease";
          }, 50);
        } else {
          card.style.display = "none";
        }
      });
    }

    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var isHidden = menu.classList.contains("hidden");
      if (isHidden) {
        menu.classList.remove("hidden");
        setTimeout(function () {
          menu.classList.remove("opacity-0", "scale-95");
          menu.classList.add("opacity-100", "scale-100");
        }, 10);
        if (arrow) arrow.classList.add("rotate-180");
      } else {
        closeDropdown();
      }
    });

    options.forEach(function (option) {
      option.addEventListener("click", function () {
        var val = option.getAttribute("data-value");
        var text = option.textContent.trim();
        if (selectedText) selectedText.textContent = text;
        closeDropdown();
        applyFilter(val);
      });
    });

    document.addEventListener("click", function (e) {
      if (!btn.contains(e.target) && !menu.contains(e.target)) {
        closeDropdown();
      }
    });
  }

  function initPopularClassesFilter() {
    document.querySelectorAll("[data-popular-classes]").forEach(initPopularClassesSection);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPopularClassesFilter);
  } else {
    initPopularClassesFilter();
  }
})();
