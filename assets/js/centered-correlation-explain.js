(function () {
  'use strict';

  var root = document.querySelector('.explain-lab');
  if (!root) return;

  var storageKey = root.dataset.storageKey || 'centered-correlation-explain-v2';
  var conceptIds = ['coordinates', 'identity', 'bound', 'norms', 'compatibility'];
  var defaultState = {
    orderComplete: false,
    fsrsCards: {},
    fsrsReviewed: {},
    fsrsEverPassed: {},
    diagnosis: {},
    builder: {},
    ready: false
  };
  var state = loadState();
  var scheduler = null;
  var sessionReviewed = {};
  var practiseAll = false;
  var currentConcept = null;
  var currentOptions = [];
  var currentAttempts = 0;

  var concepts = {
    coordinates: {
      label: 'The four objects',
      variants: [
        {
          question: 'Which sentence best describes the centered matrix $C$?',
          options: [
            ['It is $T-rs^{\\mathsf T}$: the raw cross-moment with the product of the local means removed.', true],
            ['It is the correlation matrix $T$ after deleting its diagonal entries.', false],
            ['It is the part of $T$ produced by the reduced states alone.', false]
          ],
          explanation: '$r$ and $s$ encode the two reduced states, while $T$ contains the bipartite traceless-observable coefficients. The subtraction $C=T-rs^{\\mathsf T}$ removes the cross-moment predicted by the two local means.'
        },
        {
          question: 'What does the entry $C_{ij}$ represent, up to the fixed basis normalization?',
          options: [
            ['The covariance of the local observables $\\lambda_i$ and $\\mu_j$.', true],
            ['The probability that both observables have positive eigenvalues.', false],
            ['The commutator of the two observables.', false]
          ],
          explanation: 'Its observable form is $\\langle\\lambda_i\\otimes\\mu_j\\rangle-\\langle\\lambda_i\\rangle\\langle\\mu_j\\rangle$, up to the coefficient normalization.'
        }
      ]
    },
    identity: {
      label: 'The covariance identity',
      variants: [
        {
          question: 'Which fact makes $C=\\sum_kp_k(r_k-r)(s_k-s)^{\\mathsf T}$ valid?',
          options: [
            ['The same separable ensemble generates $r$, $s$, and $T$.', true],
            ['Every $r_k$ is orthogonal to every $s_k$.', false],
            ['The optimal decomposition of $T$ is unique.', false]
          ],
          explanation: 'Separability supplies common weights $p_k$ with $r=\\sum p_kr_k$, $s=\\sum p_ks_k$, and $T=\\sum p_kr_ks_k^{\\mathsf T}$. Expanding the centered product then gives the identity.'
        },
        {
          question: 'Why is the index $k$ described as classical in the covariance argument?',
          options: [
            ['It labels the alternatives in a convex decomposition into product states.', true],
            ['It labels eigenvalues of a quantum observable measured on both systems.', false],
            ['It is the Schmidt index of the mixed state.', false]
          ],
          explanation: 'The quantum state is represented as a classical mixture of product states. The probabilities $p_k$ turn the local Bloch vectors into ordinary jointly distributed random vectors.'
        }
      ]
    },
    bound: {
      label: 'The separability bound',
      variants: [
        {
          question: 'After using the rank-one norm identity and the triangle inequality, which step produces the product of local standard deviations?',
          options: [
            ['Weighted Cauchy–Schwarz.', true],
            ['The spectral theorem.', false],
            ['Partial transposition.', false]
          ],
          explanation: 'Cauchy–Schwarz bounds $\\sum_kp_k\\lVert r_k-r\\rVert_2\\lVert s_k-s\\rVert_2$ by the square root of the product of the two weighted variance sums.'
        },
        {
          question: 'Why does a nearly pure marginal reduce the separable centered-correlation budget?',
          options: [
            ['Its variance deficit $R_d^2-\\lVert r\\rVert_2^2$ is small.', true],
            ['Its correlation matrix must be diagonal.', false],
            ['It forces the other marginal to be maximally mixed.', false]
          ],
          explanation: 'For a pure-state refinement, the local fluctuation sum is exactly $R_d^2-\\lVert r\\rVert_2^2$. Strong local polarization leaves little room for variation inside a separable ensemble.'
        }
      ]
    },
    norms: {
      label: 'Bipartite versus multipartite norms',
      variants: [
        {
          question: 'What is genuinely equivalent to the de Vicente formulation?',
          options: [
            ['For two Euclidean factors, the projective tensor norm equals the matrix nuclear norm.', true],
            ['For every tensor order, the projective norm equals the largest unfolding norm.', false],
            ['The centered criterion is identical to PPT in all dimensions.', false]
          ],
          explanation: 'A bipartite tensor is a matrix, and its Hilbertian projective norm is its nuclear norm. Thus the uncentered projective-norm inequality is de Vicente in different language.'
        },
        {
          question: 'Why can a multipartite unfolding norm be smaller than the full projective norm?',
          options: [
            ['A rank-one matrix term across a cut need not factor across every individual party.', true],
            ['Unfolding removes all singular values smaller than one.', false],
            ['The full projective norm ignores bipartite correlations.', false]
          ],
          explanation: 'A fully factorized tensor decomposition is valid after any grouping, but an optimal grouped matrix decomposition may use terms that do not split into all local factors.'
        }
      ]
    },
    compatibility: {
      label: 'The common-decomposition problem',
      variants: [
        {
          question: 'Why are separate norm bounds for each subset tensor not yet a complete multipartite formulation?',
          options: [
            ['They do not ensure that one common separable ensemble generates every tensor order.', true],
            ['Subset tensors cannot be computed from a density matrix.', false],
            ['All lower-order tensors vanish for separable states.', false]
          ],
          explanation: 'Each order may separately admit a plausible decomposition without those decompositions being compatible. Separability requires one measure on the product Bloch bodies that produces all the moments together.'
        },
        {
          question: 'Why is the top-order centered tensor alone insufficient?',
          options: [
            ['Entanglement can live in a lower-order subsystem while the top-order tensor vanishes.', true],
            ['Top-order tensors are defined only for pure states.', false],
            ['Centering always makes the top-order tensor zero.', false]
          ],
          explanation: 'For example, an entangled $AB$ state tensored with a maximally mixed $C$ system can have a vanishing three-body tensor while retaining entanglement in the $AB$ tensor.'
        }
      ]
    }
  };

  var elements = {
    orderList: document.getElementById('explain-order-list'),
    orderFeedback: document.getElementById('order-feedback'),
    checkOrder: document.getElementById('check-order'),
    resetOrder: document.getElementById('reset-order'),
    progressText: document.getElementById('explain-progress-text'),
    progressBar: document.getElementById('explain-progress-bar'),
    progressTrack: root.querySelector('.explain-progress-track'),
    dueCount: document.getElementById('fsrs-due-count'),
    reviewedCount: document.getElementById('fsrs-reviewed-count'),
    nextDate: document.getElementById('fsrs-next-date'),
    reviewCard: document.getElementById('fsrs-review-card'),
    conceptLabel: document.getElementById('fsrs-concept-label'),
    cardStatus: document.getElementById('fsrs-card-status'),
    question: document.getElementById('fsrs-question'),
    options: document.getElementById('fsrs-options'),
    reveal: document.getElementById('fsrs-reveal'),
    answer: document.getElementById('fsrs-answer'),
    next: document.getElementById('fsrs-next'),
    empty: document.getElementById('fsrs-empty'),
    emptyCopy: document.getElementById('fsrs-empty-copy'),
    practiseAll: document.getElementById('fsrs-practise-all'),
    scheduleList: document.getElementById('fsrs-schedule-list'),
    diagnosisFeedback: document.getElementById('diagnosis-feedback'),
    assembled: document.getElementById('assembled-explanation'),
    markReady: document.getElementById('mark-ready'),
    exportProgress: document.getElementById('export-progress'),
    importProgress: document.getElementById('import-progress'),
    resetProgress: document.getElementById('reset-progress'),
    readinessCopy: document.getElementById('readiness-copy'),
    readinessStatus: document.getElementById('readiness-status')
  };

  function loadState() {
    try {
      var saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
      return Object.assign({}, defaultState, saved, {
        fsrsCards: saved.fsrsCards || {},
        fsrsReviewed: saved.fsrsReviewed || {},
        fsrsEverPassed: saved.fsrsEverPassed || {},
        diagnosis: saved.diagnosis || {},
        builder: saved.builder || {}
      });
    } catch (error) {
      return Object.assign({}, defaultState);
    }
  }

  function saveState() {
    if (stageStatus().filter(Boolean).length < 4) state.ready = false;
    try {
      localStorage.setItem(storageKey, JSON.stringify(state));
    } catch (error) {
      elements.readinessStatus.textContent = 'This browser is not allowing local progress storage.';
    }
    updateProgress();
  }

  function typeset(container) {
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise(container ? [container] : undefined).catch(function () {});
    }
  }

  function stageStatus() {
    return [
      state.orderComplete,
      conceptIds.every(function (id) { return Boolean(state.fsrsEverPassed[id]); }),
      Array.prototype.every.call(root.querySelectorAll('[data-diagnosis]'), function (card) { return Boolean(state.diagnosis[card.dataset.diagnosis]); }),
      Array.prototype.every.call(root.querySelectorAll('[data-builder]'), function (card) { return Boolean(state.builder[card.dataset.builder]); })
    ];
  }

  function updateProgress() {
    var statuses = stageStatus();
    var complete = statuses.filter(Boolean).length;
    var labels = ['order the proof', 'pass the five scheduled concepts', 'diagnose all four claims', 'assemble the explanation'];
    var remaining = labels.filter(function (_, index) { return !statuses[index]; });
    elements.progressText.textContent = complete + ' of 4 stages complete';
    elements.progressTrack.setAttribute('aria-valuenow', complete);
    elements.progressBar.style.width = (complete / 4 * 100) + '%';
    elements.markReady.disabled = complete < 4;
    elements.readinessCopy.textContent = complete === 4
      ? 'You recovered the same argument through ordering, retrieval, diagnosis and reconstruction.'
      : 'Still to do: ' + remaining.join('; ') + '.';
    if (state.ready) {
      elements.readinessStatus.textContent = 'Marked as reconstructed on this browser. Scheduled reviews remain active.';
      elements.markReady.textContent = 'Reconstructed ✓';
    } else {
      elements.readinessStatus.textContent = complete === 4 ? 'All four stages are complete.' : '';
      elements.markReady.textContent = 'Mark as reconstructed';
    }
  }

  function numberOrderItems() {
    Array.prototype.forEach.call(elements.orderList.children, function (item, index) {
      item.querySelector('.explain-order-number').textContent = index + 1;
      item.querySelector('[data-move="up"]').disabled = index === 0;
      item.querySelector('[data-move="down"]').disabled = index === elements.orderList.children.length - 1;
    });
  }

  function initializeOrder() {
    if (state.orderComplete) {
      [1, 2, 3, 4, 5].forEach(function (step) {
        elements.orderList.appendChild(elements.orderList.querySelector('[data-step="' + step + '"]'));
      });
      elements.orderList.classList.add('is-correct');
      elements.orderFeedback.textContent = 'Correct. You reconstructed the complete chain.';
    }
    numberOrderItems();
  }

  elements.orderList.addEventListener('click', function (event) {
    var button = event.target.closest('button[data-move]');
    if (!button) return;
    var item = button.closest('li');
    if (button.dataset.move === 'up' && item.previousElementSibling) {
      elements.orderList.insertBefore(item, item.previousElementSibling);
    } else if (button.dataset.move === 'down' && item.nextElementSibling) {
      elements.orderList.insertBefore(item.nextElementSibling, item);
    }
    state.orderComplete = false;
    elements.orderList.classList.remove('is-correct');
    elements.orderFeedback.textContent = '';
    numberOrderItems();
    saveState();
  });

  elements.checkOrder.addEventListener('click', function () {
    var order = Array.prototype.map.call(elements.orderList.children, function (item) { return Number(item.dataset.step); });
    var firstWrong = order.findIndex(function (step, index) { return step !== index + 1; });
    state.orderComplete = firstWrong === -1;
    elements.orderList.classList.toggle('is-correct', state.orderComplete);
    elements.orderFeedback.textContent = state.orderComplete
      ? 'Correct. Product → common mixture → centering → Cauchy–Schwarz → variance bound.'
      : 'Not yet. The first mismatch is at position ' + (firstWrong + 1) + '. Ask what information that line needs.';
    saveState();
  });

  elements.resetOrder.addEventListener('click', function () {
    [4, 1, 5, 2, 3].forEach(function (step) {
      elements.orderList.appendChild(elements.orderList.querySelector('[data-step="' + step + '"]'));
    });
    state.orderComplete = false;
    elements.orderList.classList.remove('is-correct');
    elements.orderFeedback.textContent = '';
    numberOrderItems();
    saveState();
  });

  function initializeFsrs() {
    if (!window.FSRS || !window.FSRS.fsrs) {
      elements.reviewCard.innerHTML = '<p class="explain-notice">The FSRS scheduler could not be loaded. Reload the page to retry; the other three stages still work.</p>';
      return false;
    }
    scheduler = window.FSRS.fsrs({
      request_retention: 0.9,
      maximum_interval: 36500,
      enable_fuzz: true,
      enable_short_term: false
    });
    return true;
  }

  function hydrateCard(raw, now) {
    if (!raw) return window.FSRS.createEmptyCard(now);
    var card = Object.assign({}, raw);
    card.due = new Date(raw.due);
    card.last_review = raw.last_review ? new Date(raw.last_review) : undefined;
    return card;
  }

  function serializeCard(card) {
    return Object.assign({}, card, {
      due: card.due.toISOString(),
      last_review: card.last_review ? card.last_review.toISOString() : null
    });
  }

  function dueConcepts(now) {
    return conceptIds.filter(function (id) {
      var raw = state.fsrsCards[id];
      return !raw || new Date(raw.due) <= now;
    });
  }

  function relativeDue(date, now) {
    var difference = date.getTime() - now.getTime();
    if (difference <= 60000) return 'now';
    var days = Math.round(difference / 86400000);
    if (days <= 0) return 'later today';
    if (days === 1) return 'tomorrow';
    if (days < 14) return 'in ' + days + ' days';
    return new Intl.DateTimeFormat('en', { day: 'numeric', month: 'short' }).format(date);
  }

  function shuffled(items) {
    var copy = items.slice();
    for (var index = copy.length - 1; index > 0; index -= 1) {
      var swap = Math.floor(Math.random() * (index + 1));
      var value = copy[index]; copy[index] = copy[swap]; copy[swap] = value;
    }
    return copy;
  }

  function reviewQueue(now) {
    var source = practiseAll ? conceptIds : dueConcepts(now);
    return source.filter(function (id) { return !sessionReviewed[id]; });
  }

  function updateSchedule(now) {
    var due = dueConcepts(now);
    var reviewed = conceptIds.filter(function (id) { return state.fsrsReviewed[id]; }).length;
    var futureDates = conceptIds.map(function (id) {
      return state.fsrsCards[id] ? new Date(state.fsrsCards[id].due) : now;
    }).sort(function (a, b) { return a - b; });
    elements.dueCount.textContent = due.length;
    elements.reviewedCount.textContent = reviewed + ' / ' + conceptIds.length;
    elements.nextDate.textContent = due.length ? 'now' : relativeDue(futureDates[0], now);
    elements.scheduleList.innerHTML = conceptIds.map(function (id) {
      var raw = state.fsrsCards[id];
      var dueText = raw ? relativeDue(new Date(raw.due), now) : 'new · due now';
      var passed = state.fsrsEverPassed[id] ? ' · recovered correctly' : '';
      return '<li><span>' + concepts[id].label + '</span><strong>' + dueText + passed + '</strong></li>';
    }).join('');
  }

  function chooseVariant(id) {
    var raw = state.fsrsCards[id];
    var repetitions = raw ? Number(raw.reps || 0) : 0;
    return concepts[id].variants[repetitions % concepts[id].variants.length];
  }

  function renderReview() {
    if (!scheduler) return;
    var now = new Date();
    updateSchedule(now);
    var queue = reviewQueue(now);
    if (!queue.length) {
      currentConcept = null;
      elements.reviewCard.hidden = true;
      elements.empty.hidden = false;
      var future = conceptIds.map(function (id) { return state.fsrsCards[id] ? new Date(state.fsrsCards[id].due) : now; }).sort(function (a, b) { return a - b; })[0];
      elements.emptyCopy.textContent = 'The next scheduled concept is due ' + relativeDue(future, now) + '.';
      practiseAll = false;
      return;
    }
    currentConcept = queue[0];
    currentAttempts = 0;
    var variant = chooseVariant(currentConcept);
    currentOptions = shuffled(variant.options.map(function (option) { return { text: option[0], correct: option[1] }; }));
    elements.reviewCard.hidden = false;
    elements.empty.hidden = true;
    elements.conceptLabel.textContent = concepts[currentConcept].label;
    elements.cardStatus.textContent = state.fsrsCards[currentConcept] ? 'Due review' : 'New concept';
    elements.question.textContent = variant.question;
    elements.options.innerHTML = currentOptions.map(function (option, index) {
      return '<button type="button" data-option="' + index + '">' + option.text + '</button>';
    }).join('');
    elements.answer.hidden = true;
    elements.answer.innerHTML = '<strong>Why:</strong> ' + variant.explanation;
    elements.reveal.hidden = false;
    elements.next.hidden = true;
    typeset(elements.reviewCard);
  }

  function scheduleCurrent(rating) {
    var now = new Date();
    var card = hydrateCard(state.fsrsCards[currentConcept], now);
    var result = scheduler.next(card, now, rating);
    state.fsrsCards[currentConcept] = serializeCard(result.card);
    state.fsrsReviewed[currentConcept] = (state.fsrsReviewed[currentConcept] || 0) + 1;
    if (rating >= window.FSRS.Rating.Good) state.fsrsEverPassed[currentConcept] = true;
    sessionReviewed[currentConcept] = true;
    elements.cardStatus.textContent = 'Next: ' + relativeDue(result.card.due, now);
    elements.options.querySelectorAll('button').forEach(function (button) { button.disabled = true; });
    elements.reveal.hidden = true;
    elements.answer.hidden = false;
    elements.next.hidden = false;
    saveState();
    updateSchedule(now);
  }

  elements.options.addEventListener('click', function (event) {
    var button = event.target.closest('[data-option]');
    if (!button || button.disabled || !currentConcept) return;
    var option = currentOptions[Number(button.dataset.option)];
    if (!option.correct) {
      currentAttempts += 1;
      button.classList.add('is-wrong');
      button.disabled = true;
      elements.answer.hidden = false;
      elements.answer.innerHTML = '<strong>Not this one.</strong> Use the remaining choices, or reveal the answer.';
      return;
    }
    button.classList.add('is-correct');
    var rating = currentAttempts === 0 ? window.FSRS.Rating.Good : window.FSRS.Rating.Hard;
    elements.answer.innerHTML = '<strong>' + (rating === window.FSRS.Rating.Good ? 'Recovered on the first attempt.' : 'Recovered after a correction.') + '</strong> ' + chooseVariant(currentConcept).explanation;
    scheduleCurrent(rating);
    typeset(elements.answer);
  });

  elements.reveal.addEventListener('click', function () {
    if (!currentConcept) return;
    elements.options.querySelectorAll('button').forEach(function (button, index) {
      button.classList.toggle('is-correct', currentOptions[index].correct);
    });
    elements.answer.innerHTML = '<strong>Answer revealed.</strong> ' + chooseVariant(currentConcept).explanation;
    scheduleCurrent(window.FSRS.Rating.Again);
    typeset(elements.answer);
  });

  elements.next.addEventListener('click', renderReview);
  elements.practiseAll.addEventListener('click', function () {
    practiseAll = true;
    sessionReviewed = {};
    renderReview();
  });

  function initializeDiagnosis() {
    var cards = root.querySelectorAll('[data-diagnosis]');
    cards.forEach(function (card) {
      var id = card.dataset.diagnosis;
      var correct = card.dataset.correct === 'true';
      var explanation = card.querySelector('aside');
      if (state.diagnosis[id]) {
        card.classList.add('is-correct');
        explanation.hidden = false;
      }
      card.addEventListener('click', function (event) {
        var button = event.target.closest('[data-answer]');
        if (!button) return;
        var answer = button.dataset.answer === 'true';
        explanation.hidden = false;
        if (answer === correct) {
          state.diagnosis[id] = true;
          card.classList.add('is-correct');
          card.classList.remove('is-wrong');
          card.querySelectorAll('button').forEach(function (item) { item.disabled = true; });
        } else {
          card.classList.add('is-wrong');
          elements.diagnosisFeedback.textContent = 'That diagnosis does not hold. Read the reason, then choose again.';
        }
        saveState();
        typeset(explanation);
      });
    });
  }

  function initializeBuilder() {
    var cards = root.querySelectorAll('[data-builder]');
    cards.forEach(function (card) {
      var id = card.dataset.builder;
      var feedback = card.querySelector('p');
      if (state.builder[id]) {
        card.classList.add('is-correct');
        card.querySelector('[data-choice="' + card.dataset.correct + '"]').classList.add('is-correct');
        card.querySelectorAll('button').forEach(function (item) { item.disabled = true; });
      }
      card.addEventListener('click', function (event) {
        var button = event.target.closest('[data-choice]');
        if (!button || button.disabled) return;
        if (button.dataset.choice === card.dataset.correct) {
          state.builder[id] = true;
          card.classList.add('is-correct');
          card.classList.remove('is-wrong');
          button.classList.add('is-correct');
          card.querySelectorAll('button').forEach(function (item) { item.disabled = true; });
          feedback.hidden = false;
          feedback.textContent = 'This sentence supplies the information needed by the next paragraph.';
        } else {
          card.classList.add('is-wrong');
          button.classList.add('is-wrong');
          button.disabled = true;
          feedback.hidden = false;
          feedback.textContent = 'This claim either overstates the result or does not advance the derivation.';
        }
        var complete = Array.prototype.every.call(cards, function (item) { return Boolean(state.builder[item.dataset.builder]); });
        elements.assembled.hidden = !complete;
        saveState();
        if (complete) typeset(elements.assembled);
      });
    });
    elements.assembled.hidden = !Array.prototype.every.call(cards, function (item) { return Boolean(state.builder[item.dataset.builder]); });
  }

  elements.markReady.addEventListener('click', function () {
    if (stageStatus().filter(Boolean).length < 4) return;
    state.ready = true;
    saveState();
  });

  elements.exportProgress.addEventListener('click', function () {
    var exported = Object.assign({}, state, {
      exportedAt: new Date().toISOString(),
      article: 'Centered Correlation Tensors and Quantum Separability',
      scheduler: 'FSRS-6 via ts-fsrs 5.4.1'
    });
    var blob = new Blob([JSON.stringify(exported, null, 2)], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = url;
    link.download = 'centered-correlation-fsrs-progress.json';
    link.click();
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 0);
  });

  elements.importProgress.addEventListener('change', function () {
    var file = elements.importProgress.files && elements.importProgress.files[0];
    if (!file) return;
    file.text().then(function (content) {
      var imported = JSON.parse(content);
      if (!imported || imported.article !== 'Centered Correlation Tensors and Quantum Separability') throw new Error('Unexpected progress file');
      localStorage.setItem(storageKey, JSON.stringify(Object.assign({}, defaultState, imported)));
      window.location.reload();
    }).catch(function () {
      elements.readinessStatus.textContent = 'That file is not a valid progress export for this article.';
      elements.importProgress.value = '';
    });
  });

  elements.resetProgress.addEventListener('click', function () {
    if (!window.confirm('Erase the reconstruction and FSRS history stored in this browser?')) return;
    localStorage.removeItem(storageKey);
    window.location.reload();
  });

  initializeOrder();
  initializeDiagnosis();
  initializeBuilder();
  if (initializeFsrs()) renderReview();
  updateProgress();
})();
