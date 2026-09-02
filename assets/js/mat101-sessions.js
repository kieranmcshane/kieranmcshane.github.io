(function () {
  "use strict";

  function normalize(value) {
    return (value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .trim();
  }

  function initializeSessionBrowser() {
    var root = document.querySelector("[data-mat101-course]");
    if (!root) return;

    var input = root.querySelector("#mat101-session-search-input");
    var cards = Array.prototype.slice.call(
      root.querySelectorAll("[data-mat101-session-card]")
    );
    var filters = Array.prototype.slice.call(
      root.querySelectorAll("[data-mat101-session-filter]")
    );
    var count = root.querySelector("#mat101-session-count");
    var noResults = root.querySelector("#mat101-session-no-results");
    var activeBlock = "";

    if (!input || !count || !noResults || cards.length !== 19) return;

    cards.forEach(function (card) {
      card.dataset.normalizedSearch = normalize(card.dataset.sessionSearch);
    });

    function writeUrl() {
      var url = new URL(window.location.href);
      var query = input.value.trim();
      if (query) url.searchParams.set("q", query);
      else url.searchParams.delete("q");
      if (activeBlock) url.searchParams.set("bloc", activeBlock);
      else url.searchParams.delete("bloc");
      window.history.replaceState(null, "", url.pathname + url.search + url.hash);
    }

    function render(writeHistory) {
      var query = normalize(input.value);
      var visible = 0;

      cards.forEach(function (card) {
        var blockMatches =
          !activeBlock || card.dataset.sessionBlock === activeBlock;
        var searchMatches =
          !query || card.dataset.normalizedSearch.indexOf(query) !== -1;
        card.hidden = !(blockMatches && searchMatches);
        if (!card.hidden) visible += 1;
      });

      filters.forEach(function (button) {
        var selected = button.dataset.mat101SessionFilter === activeBlock;
        button.classList.toggle("is-active", selected);
        button.setAttribute("aria-pressed", selected ? "true" : "false");
      });

      count.textContent =
        visible + (visible === 1 ? " séance affichée" : " séances affichées");
      noResults.hidden = visible !== 0;
      if (writeHistory) writeUrl();
    }

    filters.forEach(function (button) {
      button.addEventListener("click", function () {
        activeBlock = button.dataset.mat101SessionFilter || "";
        render(true);
      });
    });

    input.addEventListener("input", function () {
      render(true);
    });

    var params = new URLSearchParams(window.location.search);
    var requestedBlock = params.get("bloc") || "";
    if (
      filters.some(function (button) {
        return button.dataset.mat101SessionFilter === requestedBlock;
      })
    ) {
      activeBlock = requestedBlock;
    }
    input.value = params.get("q") || "";
    render(false);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeSessionBrowser);
  } else {
    initializeSessionBrowser();
  }
})();
