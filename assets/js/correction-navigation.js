(function () {
  'use strict';

  function addQuestionPermalinks(article) {
    article.querySelectorAll('h3[id]').forEach(function (heading) {
      if (heading.querySelector('.question-anchor')) {
        return;
      }

      var link = document.createElement('a');
      link.className = 'question-anchor';
      link.href = '#' + heading.id;
      link.textContent = '¶';
      link.setAttribute('aria-label', 'Permanent link to ' + heading.textContent.trim());
      heading.appendChild(link);
    });
  }

  function populateQuestionIndex(article) {
    var container = document.querySelector('[data-question-links]');
    if (!container || container.children.length) {
      return;
    }

    article.querySelectorAll('h3[id]').forEach(function (heading) {
      var headingText = heading.textContent.trim();
      if (!/^Question\s+/i.test(headingText)) {
        return;
      }

      var label = headingText
        .replace(/^Question\s+/i, '')
        .replace(/\.$/, '');
      var link = document.createElement('a');
      link.href = '#' + heading.id;
      link.textContent = label;
      link.setAttribute('aria-label', 'Go to ' + headingText);
      container.appendChild(link);
    });
  }

  function configureResponsiveQuestionIndex() {
    var details = document.querySelector('.toc-questions');
    if (!details || !window.matchMedia) {
      return;
    }

    var compactLayout = window.matchMedia('(max-width: 1179px)');
    var synchronize = function (event) {
      details.open = !event.matches;
    };

    synchronize(compactLayout);
    if (compactLayout.addEventListener) {
      compactLayout.addEventListener('change', synchronize);
    } else {
      compactLayout.addListener(synchronize);
    }
  }

  function configureResponsiveLongformIndex() {
    var details = document.querySelector('.longform-toc-details');
    if (!details || !window.matchMedia) {
      return;
    }

    var compactLayout = window.matchMedia('(max-width: 1179px)');
    var synchronize = function (event) {
      details.open = !event.matches;
    };

    synchronize(compactLayout);
    if (compactLayout.addEventListener) {
      compactLayout.addEventListener('change', synchronize);
    } else {
      compactLayout.addListener(synchronize);
    }
  }

  function initializeSectionHighlighting(article, navigation) {
    var links = Array.prototype.slice.call(
      navigation.querySelectorAll('a[href^="#"]')
    );

    if (!links.length || !('IntersectionObserver' in window)) {
      return;
    }

    var sections = links
      .map(function (link) {
        return {
          link: link,
          section: document.getElementById(link.getAttribute('href').slice(1))
        };
      })
      .filter(function (item) {
        return item.section;
      });

    function select(link) {
      links.forEach(function (candidate) {
        if (candidate === link) {
          candidate.setAttribute('aria-current', 'location');
        } else {
          candidate.removeAttribute('aria-current');
        }
      });
    }

    links.forEach(function (link) {
      link.addEventListener('click', function () {
        select(link);
      });
    });

    var observer = new IntersectionObserver(
      function (entries) {
        entries
          .filter(function (entry) {
            return entry.isIntersecting;
          })
          .sort(function (left, right) {
            return left.boundingClientRect.top - right.boundingClientRect.top;
          })
          .slice(0, 1)
          .forEach(function (entry) {
            var match = sections.find(function (item) {
              return item.section === entry.target;
            });
            if (match) {
              select(match.link);
            }
          });
      },
      { rootMargin: '-18% 0px -70% 0px', threshold: 0 }
    );

    sections.forEach(function (item) {
      observer.observe(item.section);
    });
  }

  function initializeCorrectionNavigation() {
    var article = document.querySelector('.correction-post');
    var navigation = document.querySelector('.correction-toc');

    if (article && navigation) {
      populateQuestionIndex(article);
      addQuestionPermalinks(article);
      configureResponsiveQuestionIndex();
      initializeSectionHighlighting(article, navigation);
    }

    article = document.querySelector('.longform-post');
    navigation = document.querySelector('[data-section-navigation]');

    if (article && navigation) {
      configureResponsiveLongformIndex();
      initializeSectionHighlighting(article, navigation);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCorrectionNavigation);
  } else {
    initializeCorrectionNavigation();
  }
})();
