(function () {
  'use strict';

  function normalize(value) {
    return value
      .toLocaleLowerCase('fr')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[’']/g, ' ')
      .trim();
  }

  document.addEventListener('DOMContentLoaded', function () {
    var library = document.querySelector('.repertoire-library');
    var input = document.getElementById('repertoire-search-input');
    var counter = document.getElementById('repertoire-result-count');
    var noResults = document.getElementById('repertoire-no-results');
    var problems = Array.from(
      document.querySelectorAll('[data-repertoire-problem]')
    );
    var parts = Array.from(
      document.querySelectorAll('[data-repertoire-section]')
    );
    var chapters = Array.from(
      document.querySelectorAll('[data-repertoire-chapter]')
    );
    var filters = Array.from(
      document.querySelectorAll('[data-repertoire-part]')
    );
    var presets = Array.from(
      document.querySelectorAll('[data-repertoire-preset]')
    );
    var activePart = '';

    if (!library || !input || !problems.length) return;

    function updateButtons() {
      filters.forEach(function (button) {
        var selected = button.dataset.repertoirePart === activePart;
        button.classList.toggle('is-active', selected);
        button.setAttribute('aria-pressed', selected ? 'true' : 'false');
      });
    }

    function filterProblems() {
      var query = normalize(input.value);
      var visibleCount = 0;

      problems.forEach(function (problem) {
        var belongsToPart =
          !activePart ||
          problem.closest('[data-repertoire-section]').dataset.part === activePart;
        var matchesSearch =
          !query || normalize(problem.dataset.search || '').includes(query);
        var visible = belongsToPart && matchesSearch;
        problem.hidden = !visible;
        if (visible) visibleCount += 1;
      });

      chapters.forEach(function (chapter) {
        chapter.hidden = !chapter.querySelector(
          '[data-repertoire-problem]:not([hidden])'
        );
      });

      parts.forEach(function (part) {
        part.hidden = !part.querySelector(
          '[data-repertoire-problem]:not([hidden])'
        );
      });

      counter.textContent =
        visibleCount +
        (visibleCount > 1 ? ' problèmes affichés' : ' problème affiché');
      noResults.hidden = visibleCount !== 0;
    }

    filters.forEach(function (button) {
      button.addEventListener('click', function () {
        activePart = button.dataset.repertoirePart || '';
        updateButtons();
        filterProblems();
      });
    });

    presets.forEach(function (link) {
      link.addEventListener('click', function () {
        activePart = link.dataset.repertoirePreset || '';
        input.value = '';
        updateButtons();
        filterProblems();
      });
    });

    input.addEventListener('input', filterProblems);
    updateButtons();
    filterProblems();
  });
})();
