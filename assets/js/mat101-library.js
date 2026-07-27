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
    var tagButtons = Array.from(document.querySelectorAll('[data-mat101-tag]'));
    var activeTag = '';

    if (!input || !exercises.length) return;

    function updateTagButtons() {
      tagButtons.forEach(function (button) {
        var selected = button.dataset.mat101Tag === activeTag;
        button.classList.toggle('is-active', selected);
        button.setAttribute('aria-pressed', selected ? 'true' : 'false');
      });
    }

    function updateTagUrl() {
      var url = new URL(window.location.href);
      if (activeTag) {
        url.searchParams.set('notion', activeTag);
      } else {
        url.searchParams.delete('notion');
      }
      window.history.replaceState({}, '', url);
    }

    function filterExercises() {
      var query = normalize(input.value);
      var visibleCount = 0;

      exercises.forEach(function (exercise) {
        var matchesSearch =
          !query || normalize(exercise.dataset.search || '').includes(query);
        var tags = (exercise.dataset.tags || '').split(',');
        var matchesTag = !activeTag || tags.includes(activeTag);
        var matches = matchesSearch && matchesTag;
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
    tagButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        activeTag = button.dataset.mat101Tag || '';
        updateTagButtons();
        updateTagUrl();
        filterExercises();
      });
    });

    var requestedTag = new URL(window.location.href).searchParams.get('notion');
    if (
      requestedTag &&
      tagButtons.some(function (button) {
        return button.dataset.mat101Tag === requestedTag;
      })
    ) {
      activeTag = requestedTag;
      var tagIndex = document.querySelector('.mat101-tag-index');
      if (tagIndex) tagIndex.open = true;
    }

    updateTagButtons();
    window.addEventListener('hashchange', openHashTarget);
    filterExercises();
    openHashTarget();
  });
})();
