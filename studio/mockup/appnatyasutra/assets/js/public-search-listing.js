(function () {
  "use strict";

  function normalize(value) {
    return (value || "").toLowerCase().trim();
  }

  function initPublicSearchPage(page) {
    var searchInput = page.querySelector("[data-public-search-input]");
    var sortSelect = page.querySelector("[data-public-search-sort]");
    var grid = page.querySelector("[data-public-search-results]");
    var cards = Array.prototype.slice.call(page.querySelectorAll("[data-public-search-card]"));
    var emptyState = page.querySelector("[data-public-search-empty]");
    var skeleton = page.querySelector("[data-public-search-skeleton]");
    var loadMoreBtn = page.querySelector("[data-public-search-load-more]");
    var resultCount = page.querySelector("[data-public-search-count]");
    var viewButtons = Array.prototype.slice.call(page.querySelectorAll("[data-public-search-view]"));
    var filterToggle = page.querySelector("[data-public-search-filter-toggle]");
    var filterClose = page.querySelector("[data-public-search-filter-close]");
    var filterPanel = page.querySelector("[data-public-search-filter-panel]");
    var filterBackdrop = page.querySelector("[data-public-search-filter-backdrop]");
    var filters = Array.prototype.slice.call(page.querySelectorAll("[data-public-search-filter]"));
    var clearButton = page.querySelector("[data-public-search-clear]");
    var visibleLimit = 6;
    var activeCards = cards.slice();
    var loadingTimer = null;

    if (!grid || !cards.length) return;

    function getFilterValue(name) {
      var input = filters.find(function (item) {
        return item.getAttribute("data-public-search-filter") === name;
      });
      return input ? input.value : "";
    }

    function matchesFilters(card) {
      var query = normalize(searchInput && searchInput.value);
      var haystack = normalize(
        [
          card.getAttribute("data-title"),
          card.getAttribute("data-description"),
          card.getAttribute("data-category"),
          card.getAttribute("data-level"),
          card.getAttribute("data-instructor"),
        ].join(" ")
      );

      if (query && haystack.indexOf(query) === -1) return false;

      return ["category", "level", "language", "duration", "price"].every(function (name) {
        var value = getFilterValue(name);
        return !value || value === "all" || card.getAttribute("data-" + name) === value;
      });
    }

    function sortCards(list) {
      var sortValue = sortSelect ? sortSelect.value : "newest";
      return list.slice().sort(function (a, b) {
        if (sortValue === "az") {
          return normalize(a.getAttribute("data-title")).localeCompare(normalize(b.getAttribute("data-title")));
        }
        if (sortValue === "price") {
          return Number(a.getAttribute("data-price-value") || 0) - Number(b.getAttribute("data-price-value") || 0);
        }
        if (sortValue === "popular") {
          return Number(b.getAttribute("data-rating") || 0) - Number(a.getAttribute("data-rating") || 0);
        }
        return Number(b.getAttribute("data-newness") || 0) - Number(a.getAttribute("data-newness") || 0);
      });
    }

    function setLoading(isLoading) {
      if (skeleton) skeleton.hidden = !isLoading;
      grid.setAttribute("aria-busy", isLoading ? "true" : "false");
    }

    function render() {
      activeCards = sortCards(cards.filter(matchesFilters));
      cards.forEach(function (card) {
        card.hidden = true;
      });
      activeCards.slice(0, visibleLimit).forEach(function (card) {
        card.hidden = false;
        grid.appendChild(card);
      });

      if (emptyState) emptyState.hidden = activeCards.length > 0;
      if (loadMoreBtn) loadMoreBtn.hidden = activeCards.length <= visibleLimit;
      if (resultCount) {
        resultCount.textContent = activeCards.length + (activeCards.length === 1 ? " result" : " results");
      }
    }

    function scheduleRender(resetLimit) {
      if (resetLimit) visibleLimit = 6;
      window.clearTimeout(loadingTimer);
      setLoading(true);
      loadingTimer = window.setTimeout(function () {
        render();
        setLoading(false);
      }, 180);
    }

    function openFilters() {
      if (!filterPanel) return;
      filterPanel.classList.add("is-open");
      if (filterBackdrop) filterBackdrop.hidden = false;
      filterToggle && filterToggle.setAttribute("aria-expanded", "true");
      document.body.classList.add("public-search-filter-open");
    }

    function closeFilters() {
      if (!filterPanel) return;
      filterPanel.classList.remove("is-open");
      if (filterBackdrop) filterBackdrop.hidden = true;
      filterToggle && filterToggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("public-search-filter-open");
    }

    if (searchInput) searchInput.addEventListener("input", function () { scheduleRender(true); });
    if (sortSelect) sortSelect.addEventListener("change", function () { scheduleRender(true); });
    filters.forEach(function (filter) {
      filter.addEventListener("change", function () { scheduleRender(true); });
    });

    viewButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        var view = button.getAttribute("data-public-search-view");
        grid.setAttribute("data-view", view);
        viewButtons.forEach(function (item) {
          var active = item === button;
          item.classList.toggle("is-active", active);
          item.setAttribute("aria-pressed", active ? "true" : "false");
        });
      });
    });

    if (loadMoreBtn) {
      loadMoreBtn.addEventListener("click", function () {
        visibleLimit += 3;
        render();
      });
    }

    if (clearButton) {
      clearButton.addEventListener("click", function () {
        if (searchInput) searchInput.value = "";
        filters.forEach(function (filter) { filter.value = "all"; });
        scheduleRender(true);
      });
    }

    if (filterToggle) filterToggle.addEventListener("click", openFilters);
    if (filterClose) filterClose.addEventListener("click", closeFilters);
    if (filterBackdrop) filterBackdrop.addEventListener("click", closeFilters);
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeFilters();
    });

    render();
  }

  function init() {
    document.querySelectorAll("[data-public-search-page]").forEach(initPublicSearchPage);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
