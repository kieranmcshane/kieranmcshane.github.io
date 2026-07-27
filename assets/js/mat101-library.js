(function () {
  'use strict';

  function normalize(value) {
    return value
      .toLocaleLowerCase('fr')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .trim();
  }

  function openHashTarget() {
    if (!window.location.hash.startsWith('#exercice-')) return;

    var exercise = document.querySelector(window.location.hash);
    if (!exercise) return;

    exercise.hidden = false;
    exercise.open = true;
    var chapter = exercise.closest('[data-mat101-chapter]');
    if (chapter) chapter.hidden = false;
  }

  document.addEventListener('DOMContentLoaded', function () {
    var input = document.getElementById('mat101-search-input');
    var counter = document.getElementById('mat101-result-count');
    var noResults = document.getElementById('mat101-no-results');
    var exercises = Array.from(document.querySelectorAll('[data-mat101-exercise]'));
    var chapters = Array.from(document.querySelectorAll('[data-mat101-chapter]'));

    if (!input || !exercises.length) return;

    function filterExercises() {
      var query = normalize(input.value);
      var visibleCount = 0;

      exercises.forEach(function (exercise) {
        var matches = !query || normalize(exercise.dataset.search || '').includes(query);
        exercise.hidden = !matches;
        if (matches) visibleCount += 1;
      });

      chapters.forEach(function (chapter) {
        chapter.hidden = !chapter.querySelector('[data-mat101-exercise]:not([hidden])');
      });

      counter.textContent =
        visibleCount + (visibleCount > 1 ? ' exercices affichés' : ' exercice affiché');
      noResults.hidden = visibleCount !== 0;
    }

    input.addEventListener('input', filterExercises);
    window.addEventListener('hashchange', openHashTarget);
    filterExercises();
    openHashTarget();
  });
})();
