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

  function initializeSectionHighlighting(article) {
    var links = Array.prototype.slice.call(
      document.querySelectorAll('.correction-toc a[href^="#"]')
    );

    if (!links.length || !('IntersectionObserver' in window)) {
      return;
    }

    var sections = links
      .map(function (link) {
        return {
          link: link,
          section: article.querySelector(link.getAttribute('href'))
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
    if (!article) {
      return;
    }

    addQuestionPermalinks(article);
    initializeSectionHighlighting(article);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCorrectionNavigation);
  } else {
    initializeCorrectionNavigation();
  }
})();
