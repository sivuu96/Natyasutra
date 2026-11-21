(function () {
  "use strict";

  var dropdownBtn = document.getElementById("guruClassDropdownBtn");
  var dropdownMenu = document.getElementById("guruClassDropdownMenu");
  var dropdownArrow = document.getElementById("guruClassDropdownArrow");
  var selectedText = document.getElementById("guruClassSelectedText");
  var options = document.querySelectorAll(".guru-class-dropdown-option");
  var cards = document.querySelectorAll("#guruCompositionGrid > div");

  if (!dropdownBtn || !dropdownMenu) return;

  function closeDropdown() {
    dropdownMenu.classList.remove("opacity-100", "scale-100");
    dropdownMenu.classList.add("opacity-0", "scale-95");
    dropdownArrow.classList.remove("rotate-180");
    setTimeout(function () {
      dropdownMenu.classList.add("hidden");
    }, 200);
  }

  dropdownBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    var isHidden = dropdownMenu.classList.contains("hidden");
    if (isHidden) {
      dropdownMenu.classList.remove("hidden");
      requestAnimationFrame(function () {
        dropdownMenu.classList.remove("opacity-0", "scale-95");
        dropdownMenu.classList.add("opacity-100", "scale-100");
      });
      dropdownArrow.classList.add("rotate-180");
    } else {
      closeDropdown();
    }
  });

  options.forEach(function (option) {
    option.addEventListener("click", function () {
      var value = option.getAttribute("data-value");
      if (selectedText) selectedText.textContent = option.textContent;
      cards.forEach(function (card) {
        var category = card.getAttribute("data-category");
        if (value === "all" || category === value || (value === "kathak" && category === "kathak")) {
          card.style.display = "";
        } else if (value === "master_class" && card.textContent.toLowerCase().indexOf("master") !== -1) {
          card.style.display = "";
        } else if (value === "composition" && card.textContent.toLowerCase().indexOf("thumri") !== -1) {
          card.style.display = "";
        } else if (value === "beginners" && card.textContent.toLowerCase().indexOf("mora") !== -1) {
          card.style.display = "";
        } else if (value !== "all") {
          card.style.display = "none";
        }
      });
      if (value === "all") {
        cards.forEach(function (card) {
          card.style.display = "";
        });
      }
      closeDropdown();
    });
  });

  document.addEventListener("click", function (e) {
    if (!dropdownBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
      closeDropdown();
    }
  });
})();
