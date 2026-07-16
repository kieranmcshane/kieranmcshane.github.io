(function () {
  'use strict';

  function initializeNotationTooltips() {
    var references = document.querySelectorAll('.notation-ref[data-definition]');

    if (!references.length) {
      return;
    }

    var tooltip = document.createElement('div');
    tooltip.className = 'notation-tooltip';
    tooltip.id = 'notation-tooltip';
    tooltip.setAttribute('role', 'tooltip');
    tooltip.hidden = true;
    document.body.appendChild(tooltip);

    var activeReference = null;

    function positionTooltip(reference) {
      var referenceBox = reference.getBoundingClientRect();
      var tooltipBox = tooltip.getBoundingClientRect();
      var margin = 12;
      var gap = 10;
      var centeredLeft = referenceBox.left + referenceBox.width / 2 - tooltipBox.width / 2;
      var maximumLeft = window.innerWidth - tooltipBox.width - margin;
      var left = Math.min(Math.max(centeredLeft, margin), maximumLeft);
      var top = referenceBox.top - tooltipBox.height - gap;

      if (top < margin) {
        top = referenceBox.bottom + gap;
      }

      tooltip.style.left = left + 'px';
      tooltip.style.top = top + 'px';
      tooltip.style.visibility = 'visible';
    }

    function showTooltip(reference) {
      activeReference = reference;
      tooltip.textContent = reference.getAttribute('data-definition');
      tooltip.hidden = false;
      tooltip.style.visibility = 'hidden';
      window.requestAnimationFrame(function () {
        if (activeReference === reference) {
          positionTooltip(reference);
        }
      });
    }

    function hideTooltip(reference) {
      if (reference && activeReference !== reference) {
        return;
      }

      activeReference = null;
      tooltip.hidden = true;
      tooltip.style.visibility = 'hidden';
    }

    references.forEach(function (reference) {
      reference.addEventListener('pointerenter', function () {
        showTooltip(reference);
      });

      reference.addEventListener('pointerleave', function () {
        if (document.activeElement !== reference) {
          hideTooltip(reference);
        }
      });

      reference.addEventListener('focus', function () {
        showTooltip(reference);
      });

      reference.addEventListener('blur', function () {
        hideTooltip(reference);
      });

      reference.addEventListener('click', function () {
        hideTooltip(reference);
      });

      reference.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
          hideTooltip(reference);
        }
      });
    });

    window.addEventListener('resize', function () {
      if (activeReference) {
        positionTooltip(activeReference);
      }
    });

    window.addEventListener(
      'scroll',
      function () {
        if (activeReference) {
          positionTooltip(activeReference);
        }
      },
      { passive: true }
    );
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeNotationTooltips);
  } else {
    initializeNotationTooltips();
  }
})();
