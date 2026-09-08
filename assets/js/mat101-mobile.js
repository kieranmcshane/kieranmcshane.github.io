(function () {
  "use strict";

  var mobileQuery = window.matchMedia("(max-width: 768px)");
  var compactQuery = window.matchMedia("(max-width: 1239px)");

  function isMobileViewport() {
    return mobileQuery.matches;
  }

  function isCompactViewport() {
    return compactQuery.matches;
  }

  function prefersReducedMotion() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function shouldIgnoreSwipe(target) {
    return Boolean(
      target.closest(
        [
          "a",
          "button",
          "input",
          "textarea",
          "select",
          "label",
          "summary",
          ".mat101-session-search",
          ".mat101-session-filters",
          ".mat101-session-local-nav",
          ".mat101-shell-links",
          ".mat101-table-scroll",
          ".mat101-toc-panel",
          ".mat101-tag-index",
          "#mat101-search-input",
          ".mat101-page-links",
        ].join(", ")
      )
    );
  }

  function bindSwipe(element, handlers) {
    if (!element || element.dataset.mat101SwipeBound) return;
    element.dataset.mat101SwipeBound = "true";

    var startX = 0;
    var startY = 0;
    var tracking = false;
    var minDistance = 56;
    var ratio = 1.35;

    element.addEventListener(
      "touchstart",
      function (event) {
        if (event.touches.length !== 1) return;
        if (shouldIgnoreSwipe(event.target)) return;
        startX = event.touches[0].clientX;
        startY = event.touches[0].clientY;
        tracking = true;
      },
      { passive: true }
    );

    element.addEventListener(
      "touchend",
      function (event) {
        if (!tracking) return;
        tracking = false;

        var touch = event.changedTouches[0];
        if (!touch) return;

        var dx = touch.clientX - startX;
        var dy = touch.clientY - startY;
        if (Math.abs(dx) < minDistance) return;
        if (Math.abs(dy) * ratio > Math.abs(dx)) return;

        if (dx < 0) {
          if (handlers.onSwipeLeft) handlers.onSwipeLeft();
        } else if (handlers.onSwipeRight) {
          handlers.onSwipeRight();
        }
      },
      { passive: true }
    );
  }

  function flashSwipe(direction) {
    if (prefersReducedMotion()) return;

    var root = document.documentElement;
    root.classList.remove("mat101-swipe-left", "mat101-swipe-right");
    void root.offsetWidth;
    root.classList.add(
      direction === "left" ? "mat101-swipe-left" : "mat101-swipe-right"
    );
    window.setTimeout(function () {
      root.classList.remove("mat101-swipe-left", "mat101-swipe-right");
    }, 220);
  }

  function ensureSwipeHint(container, message) {
    if (!container || container.querySelector(".mat101-swipe-hint")) return;

    var hint = document.createElement("p");
    hint.className = "mat101-swipe-hint";
    hint.setAttribute("aria-hidden", "true");
    hint.textContent = message;
    container.appendChild(hint);
  }

  function initializeSessionDetailSwipe() {
    if (!isMobileViewport()) return;

    var page = document.querySelector(".mat101-session-page[data-mat101-session-number]");
    if (!page) return;

    page.setAttribute("data-mat101-swipe", "session-detail");

    var prev = page.querySelector('.mat101-session-pager a[rel="prev"]');
    var next = page.querySelector('.mat101-session-pager a[rel="next"]');
    if (!prev && !next) return;

    bindSwipe(page, {
      onSwipeLeft: function () {
        if (!next) return;
        flashSwipe("left");
        window.location.assign(next.href);
      },
      onSwipeRight: function () {
        if (!prev) return;
        flashSwipe("right");
        window.location.assign(prev.href);
      },
    });

    ensureSwipeHint(
      page,
      prev && next
        ? "Glisser à gauche ou à droite pour changer de séance"
        : next
          ? "Glisser à gauche pour la séance suivante"
          : "Glisser à droite pour la séance précédente"
    );
  }

  function initializeSessionHubSwipe() {
    if (!isMobileViewport()) return;

    var root = document.querySelector("[data-mat101-course]");
    if (!root) return;

    root.setAttribute("data-mat101-swipe", "session-hub");

    var filters = Array.prototype.slice.call(
      root.querySelectorAll("[data-mat101-session-filter]")
    );
    if (filters.length < 2) return;

    function activeIndex() {
      return filters.findIndex(function (button) {
        return button.classList.contains("is-active");
      });
    }

    var browser = root.querySelector(".mat101-session-browser") || root;
    bindSwipe(browser, {
      onSwipeLeft: function () {
        var index = activeIndex();
        if (index === -1) return;
        flashSwipe("left");
        filters[(index + 1) % filters.length].click();
      },
      onSwipeRight: function () {
        var index = activeIndex();
        if (index === -1) return;
        flashSwipe("right");
        filters[(index - 1 + filters.length) % filters.length].click();
      },
    });

    ensureSwipeHint(
      browser,
      "Glisser sur les filtres pour parcourir les blocs du parcours"
    );
  }

  function initializeExerciseSwipe() {
    if (!isCompactViewport()) return;

    var library = document.querySelector(".mat101-library");
    var searchInput = document.getElementById("mat101-search-input");
    if (!library || !searchInput) return;

    library.setAttribute("data-mat101-swipe", "exercises");

    function visibleExercises() {
      return Array.prototype.slice.call(
        document.querySelectorAll("[data-mat101-exercise]:not([hidden])")
      );
    }

    function openExercise(exercise) {
      if (!exercise) return;

      var current = document.querySelector("[data-mat101-exercise][open]");
      if (current && current !== exercise) current.open = false;

      exercise.open = true;
      exercise.scrollIntoView({
        behavior: prefersReducedMotion() ? "auto" : "smooth",
        block: "start",
      });

      if (exercise.id) {
        history.replaceState(null, "", "#" + exercise.id);
      }
    }

    bindSwipe(library, {
      onSwipeLeft: function () {
        var open = document.querySelector(
          "[data-mat101-exercise][open]:not([hidden])"
        );
        if (!open) return;

        var list = visibleExercises();
        var index = list.indexOf(open);
        if (index === -1 || index >= list.length - 1) return;

        flashSwipe("left");
        openExercise(list[index + 1]);
      },
      onSwipeRight: function () {
        var open = document.querySelector(
          "[data-mat101-exercise][open]:not([hidden])"
        );
        if (!open) return;

        var list = visibleExercises();
        var index = list.indexOf(open);
        if (index <= 0) return;

        flashSwipe("right");
        openExercise(list[index - 1]);
      },
    });

    if (isMobileViewport()) {
      ensureSwipeHint(
        library.querySelector(".mat101-page-heading") || library,
        "Avec un énoncé ouvert, glisser pour passer à l’exercice suivant ou précédent"
      );
    }
  }

  function initialize() {
    initializeSessionDetailSwipe();
    initializeSessionHubSwipe();
    initializeExerciseSwipe();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }

  function handleViewportChange() {
    initialize();
  }

  if (typeof mobileQuery.addEventListener === "function") {
    mobileQuery.addEventListener("change", handleViewportChange);
    compactQuery.addEventListener("change", handleViewportChange);
  } else {
    mobileQuery.addListener(handleViewportChange);
    compactQuery.addListener(handleViewportChange);
  }
})();
