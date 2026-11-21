(function () {
  "use strict";

  function measurePanelHeight(panel) {
    panel.classList.remove("is-collapsed");
    panel.style.maxHeight = "none";
    panel.style.opacity = "0";
    panel.style.pointerEvents = "none";
    var height = panel.scrollHeight;
    panel.classList.add("is-collapsed");
    panel.style.maxHeight = "0px";
    panel.style.pointerEvents = "";
    return height;
  }

  function ensureExtraPanel(root) {
    var existing = root.querySelector("[data-curriculum-extra]");
    if (existing && existing.tagName === "DIV") {
      return existing;
    }

    var mainTable = root.querySelector("table.page-lesson-table");
    if (!mainTable) return null;

    var legacyBody = root.querySelector("tbody[data-curriculum-extra]");
    var panel = document.createElement("div");
    panel.setAttribute("data-curriculum-extra", "");
    panel.className = "is-collapsed";
    panel.setAttribute("aria-hidden", "true");

    var extraTable = document.createElement("table");
    extraTable.className = "page-lesson-table page-lesson-table--continuation";

    var colgroup = mainTable.querySelector("colgroup");
    if (colgroup) {
      extraTable.appendChild(colgroup.cloneNode(true));
    }

    var tbody = document.createElement("tbody");
    if (legacyBody) {
      while (legacyBody.firstElementChild) {
        tbody.appendChild(legacyBody.firstElementChild);
      }
      legacyBody.remove();
    }

    extraTable.appendChild(tbody);
    panel.appendChild(extraTable);

    var foot = root.querySelector(".page-lesson-table-foot");
    if (foot) {
      root.insertBefore(panel, foot);
    } else {
      root.appendChild(panel);
    }

    return panel;
  }

  function normalizeRows(root, visibleCount, primaryBody, extraTbody) {
    if (!primaryBody || !extraTbody) return;

    var primaryRows = Array.prototype.slice.call(primaryBody.querySelectorAll("tr"));
    if (primaryRows.length <= visibleCount) return;

    primaryRows.slice(visibleCount).reverse().forEach(function (row) {
      extraTbody.insertBefore(row, extraTbody.firstChild);
    });
  }

  function initCurriculumTable(root) {
    var visibleCount = parseInt(
      root.getAttribute("data-curriculum-visible-count") || "5",
      10
    );
    var primaryBody = root.querySelector("[data-curriculum-primary]");
    var panel = ensureExtraPanel(root);
    var toggle = root.querySelector("[data-curriculum-toggle]");
    if (!panel || !toggle) return;

    var extraTbody = panel.querySelector("tbody");
    normalizeRows(root, visibleCount, primaryBody, extraTbody);

    if (!extraTbody || extraTbody.querySelectorAll("tr").length === 0) {
      toggle.hidden = true;
      panel.hidden = true;
      return;
    }

    var expanded = false;

    function setCollapsedState() {
      panel.classList.add("is-collapsed");
      panel.setAttribute("aria-hidden", "true");
      panel.style.maxHeight = "0px";
      panel.style.opacity = "0";
    }

    function expand() {
      expanded = true;
      toggle.setAttribute("aria-expanded", "true");
      toggle.textContent = "Show Less";
      panel.setAttribute("aria-hidden", "false");

      var targetHeight = measurePanelHeight(panel);
      panel.classList.remove("is-collapsed");
      panel.style.maxHeight = "0px";
      panel.style.opacity = "0";
      panel.offsetHeight;
      panel.style.maxHeight = targetHeight + "px";
      panel.style.opacity = "1";

      function onExpandEnd(event) {
        if (event.propertyName !== "max-height" || !expanded) return;
        panel.removeEventListener("transitionend", onExpandEnd);
        panel.style.maxHeight = "none";
      }

      panel.addEventListener("transitionend", onExpandEnd);
    }

    function collapse() {
      expanded = false;
      toggle.setAttribute("aria-expanded", "false");
      toggle.textContent = "View All";
      panel.setAttribute("aria-hidden", "true");

      panel.style.maxHeight = panel.scrollHeight + "px";
      panel.offsetHeight;
      panel.classList.add("is-collapsed");
      panel.style.maxHeight = "0px";
      panel.style.opacity = "0";
    }

    toggle.addEventListener("click", function () {
      if (expanded) {
        collapse();
      } else {
        expand();
      }
    });

    setCollapsedState();
  }

  function init() {
    document.querySelectorAll("[data-curriculum-table]").forEach(initCurriculumTable);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
