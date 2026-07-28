(function () {
  'use strict';

  function normalize(value) {
    return value
      .toLocaleLowerCase('fr')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .trim();
  }

  function hashTarget() {
    if (!window.location.hash.startsWith('#exercice-')) return;

    return document.getElementById(window.location.hash.slice(1)) || undefined;
  }

  function drawRootDiagram(canvas) {
    var context = canvas.getContext('2d');
    if (!context) return;

    var count = Number(canvas.dataset.rootCount);
    var startAngle = Number(canvas.dataset.startAngle || 0);
    var labels = (canvas.dataset.labels || '').split('|');
    var mutedIndex = Number(canvas.dataset.mutedIndex);
    var angleLabel = canvas.dataset.angleLabel || '';
    var size = canvas.width;
    var center = size / 2;
    var radius = size * 0.31;
    var pointRadius = size * 0.018;
    var points = [];

    context.clearRect(0, 0, size, size);
    context.lineCap = 'round';
    context.lineJoin = 'round';

    context.strokeStyle = '#b9cdd1';
    context.lineWidth = 2;
    context.beginPath();
    context.moveTo(size * 0.1, center);
    context.lineTo(size * 0.9, center);
    context.moveTo(center, size * 0.1);
    context.lineTo(center, size * 0.9);
    context.stroke();

    context.fillStyle = '#60757a';
    context.font = '600 22px system-ui, sans-serif';
    context.textAlign = 'right';
    context.fillText('Re', size * 0.91, center - 12);
    context.textAlign = 'left';
    context.fillText('Im', center + 12, size * 0.11);

    context.strokeStyle = '#7baeb6';
    context.lineWidth = 3;
    context.beginPath();
    context.arc(center, center, radius, 0, 2 * Math.PI);
    context.stroke();

    for (var index = 0; index < count; index += 1) {
      var angle = startAngle + (2 * Math.PI * index) / count;
      points.push({
        angle: angle,
        x: center + radius * Math.cos(angle),
        y: center - radius * Math.sin(angle),
      });
    }

    context.strokeStyle = 'rgba(0, 128, 146, 0.5)';
    context.lineWidth = 4;
    context.beginPath();
    points.forEach(function (point, index) {
      if (index === 0) context.moveTo(point.x, point.y);
      else context.lineTo(point.x, point.y);
    });
    context.closePath();
    context.stroke();

    if (angleLabel) {
      context.strokeStyle = '#a65c28';
      context.lineWidth = 4;
      context.save();
      context.translate(center, center);
      context.scale(1, -1);
      context.beginPath();
      context.arc(0, 0, size * 0.085, 0, startAngle, startAngle < 0);
      context.stroke();
      context.restore();

      var labelAngle = startAngle / 2;
      context.fillStyle = '#8b4a1e';
      context.font = '700 21px system-ui, sans-serif';
      context.textAlign = 'center';
      context.fillText(
        angleLabel,
        center + size * 0.13 * Math.cos(labelAngle),
        center - size * 0.13 * Math.sin(labelAngle) - 8
      );
    }

    points.forEach(function (point, index) {
      var isMuted = index === mutedIndex;
      context.beginPath();
      context.arc(point.x, point.y, pointRadius, 0, 2 * Math.PI);
      context.fillStyle = isMuted ? '#fffdfb' : '#008092';
      context.fill();
      context.strokeStyle = isMuted ? '#8b4a1e' : '#006b78';
      context.lineWidth = isMuted ? 5 : 3;
      context.stroke();

      var labelRadius = radius + size * 0.065;
      var labelX = center + labelRadius * Math.cos(point.angle);
      var labelY = center - labelRadius * Math.sin(point.angle);
      var horizontal = Math.cos(point.angle);
      var vertical = Math.sin(point.angle);
      context.fillStyle = isMuted ? '#8b4a1e' : '#183f47';
      context.font = '700 25px Georgia, serif';
      context.textAlign =
        horizontal > 0.25 ? 'left' : horizontal < -0.25 ? 'right' : 'center';
      context.textBaseline =
        vertical > 0.25 ? 'bottom' : vertical < -0.25 ? 'top' : 'middle';
      context.fillText(labels[index] || 'z' + index, labelX, labelY);
    });
  }

  function initializeRootDiagrams() {
    document.querySelectorAll('[data-mat101-root-diagram]').forEach(function (canvas) {
      drawRootDiagram(canvas);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var input = document.getElementById('mat101-search-input');
    var counter = document.getElementById('mat101-result-count');
    var noResults = document.getElementById('mat101-no-results');
    var exercises = Array.from(document.querySelectorAll('[data-mat101-exercise]'));
    var chapters = Array.from(document.querySelectorAll('[data-mat101-chapter]'));
    var tagButtons = Array.from(document.querySelectorAll('[data-mat101-tag]'));
    var tocDetails = document.querySelector('[data-mat101-toc]');
    var tocCurrent = document.getElementById('mat101-toc-current');
    var tocLinks = Array.from(document.querySelectorAll('[data-mat101-toc-link]'));
    var tocChapters = Array.from(
      document.querySelectorAll('[data-mat101-toc-chapter]')
    );
    var tocChapterLinks = Array.from(
      document.querySelectorAll('[data-mat101-toc-chapter-link]')
    );
    var activeTag = '';
    var currentExercise;

    initializeRootDiagrams();

    if (!input || !exercises.length) return;

    if (tocDetails && window.matchMedia('(min-width: 701px)').matches) {
      tocDetails.open = true;
    }

    function updateToc(visibleCount) {
      tocLinks.forEach(function (link) {
        var exercise = exercises.find(function (candidate) {
          return candidate.dataset.exerciseId === link.dataset.exerciseId;
        });
        link.hidden = !exercise || exercise.hidden;
      });

      tocChapters.forEach(function (chapter) {
        chapter.hidden = !chapter.querySelector(
          '[data-mat101-toc-link]:not([hidden])'
        );
      });

      if (!tocCurrent) return;

      if (normalize(input.value) || activeTag) {
        tocCurrent.textContent =
          visibleCount +
          (visibleCount > 1 ? ' exercices disponibles' : ' exercice disponible');
      } else if (currentExercise) {
        var currentLink = tocLinks.find(function (link) {
          return link.dataset.exerciseId === currentExercise.dataset.exerciseId;
        });
        tocCurrent.textContent = currentLink
          ? 'Exercice ' +
            currentLink.dataset.exerciseId +
            ' · ' +
            currentLink.dataset.chapterTitle
          : '4 chapitres · 103 exercices';
      } else {
        tocCurrent.textContent = '4 chapitres · 103 exercices';
      }
    }

    function setCurrentExercise(exercise) {
      currentExercise = exercise;
      tocLinks.forEach(function (link) {
        var selected =
          exercise && link.dataset.exerciseId === exercise.dataset.exerciseId;
        if (selected) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
      updateToc(exercises.filter(function (candidate) {
        return !candidate.hidden;
      }).length);
    }

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
      updateToc(visibleCount);
    }

    function openHashTarget() {
      var exercise = hashTarget();
      if (!exercise) return;

      input.value = '';
      activeTag = '';
      updateTagButtons();
      updateTagUrl();
      filterExercises();
      exercise.open = true;
      setCurrentExercise(exercise);
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
    tocLinks.forEach(function (link) {
      link.addEventListener('click', function () {
        var exercise = exercises.find(function (candidate) {
          return candidate.dataset.exerciseId === link.dataset.exerciseId;
        });
        if (!exercise) return;

        input.value = '';
        activeTag = '';
        updateTagButtons();
        updateTagUrl();
        filterExercises();
        exercise.open = true;
        setCurrentExercise(exercise);
        if (tocDetails && window.matchMedia('(max-width: 700px)').matches) {
          tocDetails.open = false;
        }
      });
    });
    tocChapterLinks.forEach(function (link) {
      link.addEventListener('click', function () {
        if (tocDetails && window.matchMedia('(max-width: 700px)').matches) {
          tocDetails.open = false;
        }
      });
    });
    exercises.forEach(function (exercise) {
      exercise.addEventListener('toggle', function () {
        if (exercise.open) setCurrentExercise(exercise);
      });
    });

    var requestedTag = new URL(window.location.href).searchParams.get('notion');
    if (
      !hashTarget() &&
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
