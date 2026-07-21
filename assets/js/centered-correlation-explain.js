(function () {
  'use strict';

  var root = document.querySelector('.explain-lab');
  if (!root) return;

  var storageKey = root.dataset.storageKey || 'centered-correlation-explain-v2';
  var conceptIds = ['coordinates', 'identity', 'triangle', 'cauchy', 'variance', 'bound', 'norms', 'compatibility'];
  var defaultState = {
    proofComplete: false,
    boundComplete: false,
    boundProgress: 0,
    boundMistakes: {},
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
  var proofStateId = state.proofComplete ? 'complete' : 'start';
  var proofHistory = [];

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
    triangle: {
      label: 'Nuclear norm and rank one',
      variants: [
        {
          question: 'From $C=\\sum_kp_ku_kv_k^{\\mathsf T}$, what is the first norm estimate that is always valid?',
          options: [
            ['$\\lVert C\\rVert_*\\leq\\sum_kp_k\\lVert u_kv_k^{\\mathsf T}\\rVert_*$.', true],
            ['$\\lVert C\\rVert_*=\\sum_kp_k\\lVert u_kv_k^{\\mathsf T}\\rVert_*$ for every ensemble.', false],
            ['$\\lVert C\\rVert_*\\leq\\max_k\\lVert u_kv_k^{\\mathsf T}\\rVert_*$.', false]
          ],
          explanation: 'The triangle inequality gives the sum. Equality would require special alignment of the summands; a maximum does not control a convex sum in this way.'
        },
        {
          question: 'Why can each summand be replaced by a product of Euclidean norms?',
          options: [
            ['$u_kv_k^{\\mathsf T}$ has rank at most one, so its only nonzero singular value is $\\lVert u_k\\rVert_2\\lVert v_k\\rVert_2$.', true],
            ['Every covariance matrix is diagonal in the Bloch basis.', false],
            ['Nuclear and operator norms agree for every matrix.', false]
          ],
          explanation: 'The rank-one outer-product identity is exact; the inequality enters one line earlier through the triangle inequality.'
        }
      ]
    },
    cauchy: {
      label: 'Weighted Cauchy–Schwarz',
      variants: [
        {
          question: 'Which substitution exposes the weighted Cauchy–Schwarz step?',
          options: [
            ['$a_k=\\sqrt{p_k}\\lVert r_k-r\\rVert_2$ and $b_k=\\sqrt{p_k}\\lVert s_k-s\\rVert_2$.', true],
            ['$a_k=p_k\\lVert r_k-r\\rVert_2$ and $b_k=p_k\\lVert s_k-s\\rVert_2$.', false],
            ['$a_k=\\lVert r\\rVert_2$ and $b_k=\\lVert s\\rVert_2$ for every $k$.', false]
          ],
          explanation: 'The square roots place exactly one factor $p_k$ in each product and produce the weighted sums of squared deviations.'
        },
        {
          question: 'What does Cauchy–Schwarz control in the centered proof?',
          options: [
            ['The sum of products of local deviations by the product of their root-mean-square sizes.', true],
            ['The rank of the full correlation matrix by the local dimensions.', false],
            ['The partial-transpose eigenvalues by the marginal purities.', false]
          ],
          explanation: 'It is a classical inequality applied to the two scalar sequences of weighted deviation norms.'
        }
      ]
    },
    variance: {
      label: 'Local variance deficit',
      variants: [
        {
          question: 'For a pure local refinement, what is $\\sum_kp_k\\lVert r_k-r\\rVert_2^2$?',
          options: [
            ['$R_M^2-\\lVert r\\rVert_2^2$.', true],
            ['$R_M^2+\\lVert r\\rVert_2^2$.', false],
            ['$\\lVert r\\rVert_2^2$ independently of the ensemble.', false]
          ],
          explanation: 'Expanding the square cancels the cross term using $r=\\sum_kp_kr_k$; purity gives $\\lVert r_k\\rVert_2=R_M$.'
        },
        {
          question: 'Why does a nearly pure marginal tighten the centered bound?',
          options: [
            ['Its mean Bloch vector is near the outer radius, leaving a small variance deficit.', true],
            ['Its correlation matrix must have small rank.', false],
            ['It makes the other marginal maximally mixed.', false]
          ],
          explanation: 'The right-hand side is the product of the two local standard-deviation budgets, not a dimension-only constant.'
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
    proofExpression: document.getElementById('proof-expression'),
    proofMoveFamily: document.getElementById('proof-move-family'),
    proofActionPrompt: document.getElementById('proof-action-prompt'),
    proofActions: document.getElementById('proof-actions'),
    proofFeedback: document.getElementById('proof-feedback'),
    proofHistory: document.getElementById('proof-history'),
    proofStepCount: document.getElementById('proof-step-count'),
    proofUndo: document.getElementById('proof-undo'),
    proofReset: document.getElementById('proof-reset'),
    boundStepLabel: document.getElementById('bound-step-label'),
    boundTrace: document.getElementById('bound-trace'),
    boundChallenge: document.getElementById('bound-challenge'),
    boundContext: document.getElementById('bound-context'),
    boundFormula: document.getElementById('bound-formula'),
    boundQuestion: document.getElementById('bound-question'),
    boundOptions: document.getElementById('bound-options'),
    boundFeedback: document.getElementById('bound-feedback'),
    boundComplete: document.getElementById('bound-complete'),
    boundReset: document.getElementById('bound-reset'),
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
        builder: saved.builder || {},
        boundMistakes: saved.boundMistakes || {}
      });
    } catch (error) {
      return Object.assign({}, defaultState);
    }
  }

  function saveState() {
    if (stageStatus().filter(Boolean).length < 5) state.ready = false;
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
      state.proofComplete,
      state.boundComplete,
      conceptIds.every(function (id) { return Boolean(state.fsrsEverPassed[id]); }),
      Array.prototype.every.call(root.querySelectorAll('[data-diagnosis]'), function (card) { return Boolean(state.diagnosis[card.dataset.diagnosis]); }),
      Array.prototype.every.call(root.querySelectorAll('[data-builder]'), function (card) { return Boolean(state.builder[card.dataset.builder]); })
    ];
  }

  function updateProgress() {
    var statuses = stageStatus();
    var complete = statuses.filter(Boolean).length;
    if (complete < 5) state.ready = false;
    var labels = ['complete the checked identity', 'recover the six-step bound', 'pass the eight scheduled concepts', 'diagnose all four claims', 'assemble the explanation'];
    var remaining = labels.filter(function (_, index) { return !statuses[index]; });
    elements.progressText.textContent = complete + ' of 5 stages complete';
    elements.progressTrack.setAttribute('aria-valuenow', complete);
    elements.progressBar.style.width = (complete / 5 * 100) + '%';
    elements.markReady.disabled = complete < 5;
    elements.readinessCopy.textContent = complete === 5
      ? 'You recovered the same argument through formal rewriting, retrieval, diagnosis and reconstruction.'
      : 'Still to do: ' + remaining.join('; ') + '.';
    if (state.ready) {
      elements.readinessStatus.textContent = 'Marked as reconstructed on this browser. Scheduled reviews remain active.';
      elements.markReady.textContent = 'Reconstructed ✓';
    } else {
      elements.readinessStatus.textContent = complete === 5 ? 'All five stages are complete.' : '';
      elements.markReady.textContent = 'Mark as reconstructed';
    }
  }

  var proofModule = {
    id: 'centered-covariance',
    domain: 'Linear algebra',
    productiveMoves: 3,
    phases: [
      { progress: 0, label: 'Rewrite' },
      { progress: 1, label: 'Center' },
      { progress: 2, label: 'Factor' }
    ],
    states: {
    start: {
      progress: 0,
      expression: '$C=$ <button type="button" data-proof-object="raw" aria-label="Select T">$T$</button> $-$ <button type="button" data-proof-object="means" aria-label="Select product of means">$rs^{\\mathsf T}$</button>',
      prompts: {
        raw: {
          label: 'You selected $T$. Which matching equality should be used, and in which direction?',
          actions: [
            { id: 'cross', family: 'Rewrite an equality', label: 'Use $h_T$ backwards: replace $T$ by $\\sum_k p_k r_k s_k^{\\mathsf T}$', next: 'cross', theorem: 'rewrite_cross_moment', productive: true },
            { id: 'circular', family: 'Rewrite an equality', label: 'Solve $C=T-rs^{\\mathsf T}$ for $T$, then substitute it back', next: 'circular', theorem: 'rewrite_through_center', productive: false }
          ]
        },
        means: {
          label: 'You selected $rs^{\\mathsf T}$. Both local-mean rewrites are legal, but do they simplify this goal?',
          actions: [
            { id: 'left-mean', family: 'Substitute a definition', label: 'Replace $r$ using $h_r$', next: 'leftMean', theorem: 'rewrite_left_mean', productive: false },
            { id: 'right-mean', family: 'Substitute a definition', label: 'Replace $s$ using $h_s$', next: 'rightMean', theorem: 'rewrite_right_mean', productive: false }
          ]
        }
      }
    },
    circular: {
      progress: 0,
      expression: '$C=(C+rs^{\\mathsf T})-rs^{\\mathsf T}$',
      detour: 'This rewrite is valid, but it only restates the definition and makes no progress. Undo and inspect a different object.'
    },
    leftMean: {
      progress: 0,
      expression: '$C=T-\\left(\\sum_k p_k r_k\\right)s^{\\mathsf T}$',
      detour: 'This use of $h_r$ is valid, but it creates a product of sums before the cross-moment has been exposed. Undo and look for a rewrite of $T$.'
    },
    rightMean: {
      progress: 0,
      expression: '$C=T-r\\left(\\sum_k p_k s_k\\right)^{\\mathsf T}$',
      detour: 'This use of $h_s$ is valid, but it creates a product of sums before the cross-moment has been exposed. Undo and look for a rewrite of $T$.'
    },
    cross: {
      progress: 1,
      expression: '$C=$ <button type="button" data-proof-object="cross-rhs" aria-label="Select rewritten right hand side">$\\displaystyle \\sum_k p_k r_k s_k^{\\mathsf T}-rs^{\\mathsf T}$</button>',
      prompts: {
        'cross-rhs': {
          label: 'The cross-moment is visible. Which equality introduces the centered factors without changing the sum?',
          actions: [
            { id: 'zero-means', family: 'Add zero strategically', label: 'Insert the two zero first moments from $h_r$, $h_s$, and $h_p$', next: 'expanded', theorem: 'insert_zero_means', productive: true },
            { id: 'cross-left', family: 'Substitute a definition', label: 'Expand only $r$ as $\\sum_kp_kr_k$', next: 'crossLeft', theorem: 'rewrite_left_mean', productive: false }
          ]
        }
      }
    },
    crossLeft: {
      progress: 1,
      expression: '$C=\\displaystyle \\sum_kp_kr_ks_k^{\\mathsf T}-\\left(\\sum_kp_kr_k\\right)s^{\\mathsf T}$',
      detour: 'Still valid, but the cancellation is now hidden inside two separate sums. Undo and use both zero-mean identities together.'
    },
    expanded: {
      progress: 2,
      expression: '$C=\\displaystyle \\sum_k p_k$ <button type="button" data-proof-object="summand" aria-label="Select four term summand">$\\left(r_ks_k^{\\mathsf T}-r_ks^{\\mathsf T}-rs_k^{\\mathsf T}+rs^{\\mathsf T}\\right)$</button>',
      prompts: {
        summand: {
          label: 'You selected one four-term summand. Which local algebraic operation completes the identity?',
          actions: [
            { id: 'factor', family: 'Factor an expression', label: 'Factor it as $(r_k-r)(s_k-s)^{\\mathsf T}$', next: 'complete', theorem: 'factor_centered_summand', productive: true },
            { id: 'distribute', family: 'Distribute a sum', label: 'Distribute the outer sum back into four sums', next: 'distributed', theorem: 'insert_zero_means', productive: false }
          ]
        }
      }
    },
    distributed: {
      progress: 2,
      expression: '$C=\\sum_kp_kr_ks_k^{\\mathsf T}-\\sum_kp_kr_ks^{\\mathsf T}-\\sum_kp_krs_k^{\\mathsf T}+\\sum_kp_krs^{\\mathsf T}$',
      detour: 'This expansion is valid, but it moves away from the compact covariance form. Undo and factor the selected summand instead.'
    },
    complete: {
      progress: 3,
      expression: '$\\boxed{C=\\displaystyle \\sum_k p_k(r_k-r)(s_k-s)^{\\mathsf T}}$',
      complete: true
    }
    }
  };
  var proofStates = proofModule.states;

  function updateProofRoute(activeProofState) {
    root.querySelectorAll('[data-proof-phase]').forEach(function (item) {
      var phase = Number(item.dataset.proofPhase);
      item.classList.toggle('is-complete', activeProofState.progress >= phase);
      item.classList.toggle('is-current', !activeProofState.complete && activeProofState.progress + 1 === phase);
    });
  }

  function renderProofState(message) {
    var activeProofState = proofStates[proofStateId];
    elements.proofExpression.innerHTML = activeProofState.expression;
    elements.proofStepCount.textContent = activeProofState.progress + ' / ' + proofModule.productiveMoves + ' productive moves';
    elements.proofMoveFamily.textContent = activeProofState.complete ? 'Identity established' : 'Choose an object first';
    elements.proofActions.innerHTML = '';
    elements.proofActionPrompt.innerHTML = activeProofState.complete
      ? '<strong>Proof complete.</strong> Every displayed transition is covered by the checked Lean file.'
      : activeProofState.detour || 'Select a highlighted part of the formula.';
    elements.proofFeedback.textContent = message || '';
    elements.proofUndo.disabled = proofHistory.length === 0;
    elements.proofHistory.innerHTML = proofHistory.map(function (entry) {
      return '<li><span><small>' + entry.family + '</small>' + entry.label + '</span><code>' + entry.theorem + '</code></li>';
    }).join('');
    updateProofRoute(activeProofState);
    if (activeProofState.complete) {
      state.proofComplete = true;
      saveState();
    }
    typeset(elements.proofExpression);
    typeset(elements.proofActionPrompt);
  }

  elements.proofExpression.addEventListener('click', function (event) {
    var object = event.target.closest('[data-proof-object]');
    if (!object) return;
    elements.proofExpression.querySelectorAll('[data-proof-object]').forEach(function (item) { item.classList.remove('is-selected'); });
    object.classList.add('is-selected');
    var prompt = proofStates[proofStateId].prompts && proofStates[proofStateId].prompts[object.dataset.proofObject];
    if (!prompt) return;
    elements.proofActionPrompt.innerHTML = prompt.label;
    elements.proofActions.innerHTML = prompt.actions.map(function (action) {
      return '<button type="button" data-proof-action="' + action.id + '" data-next="' + action.next + '" data-theorem="' + action.theorem + '" data-family="' + action.family + '" data-productive="' + action.productive + '"><small>' + action.family + '</small><span>' + action.label + '</span></button>';
    }).join('');
    elements.proofMoveFamily.textContent = prompt.actions.length === 1 ? prompt.actions[0].family : 'Operations available for this object';
    elements.proofFeedback.textContent = '';
    typeset(document.getElementById('proof-action-panel'));
  });

  elements.proofActions.addEventListener('click', function (event) {
    var action = event.target.closest('[data-proof-action]');
    if (!action) return;
    proofHistory.push({ state: proofStateId, label: action.querySelector('span').textContent.trim(), family: action.dataset.family, theorem: action.dataset.theorem });
    proofStateId = action.dataset.next;
    renderProofState(action.dataset.productive === 'true'
      ? 'Lean accepts the rewrite. The proof state has advanced.'
      : 'Lean accepts the rewrite, but it is strategically unhelpful.');
    renderBoundChallenge();
  });

  elements.proofUndo.addEventListener('click', function () {
    var previous = proofHistory.pop();
    if (!previous) return;
    proofStateId = previous.state;
    state.proofComplete = false;
    renderProofState('Move undone. Try a different object or rewrite.');
    renderBoundChallenge();
    saveState();
  });

  elements.proofReset.addEventListener('click', function () {
    proofHistory = [];
    proofStateId = 'start';
    state.proofComplete = false;
    renderProofState('Puzzle restarted.');
    renderBoundChallenge();
    saveState();
  });

  var boundSteps = [
    {
      concept: 'triangle',
      context: 'Write $u_k=r_k-r$ and $v_k=s_k-s$. The covariance identity is $C=\\sum_kp_ku_kv_k^{\\mathsf T}$.',
      formula: '$\\left\\lVert\\sum_kp_ku_kv_k^{\\mathsf T}\\right\\rVert_*\\;\\;?$',
      question: 'What is the strongest unconditional first step?',
      result: '$\\lVert C\\rVert_*\\leq\\sum_kp_k\\lVert u_kv_k^{\\mathsf T}\\rVert_*$',
      options: [
        { label: 'Use the triangle inequality: $\\lVert C\\rVert_*\\leq\\sum_kp_k\\lVert u_kv_k^{\\mathsf T}\\rVert_*$.', correct: true },
        { label: 'Replace the norm of the sum by the sum of the norms with equality.', correct: false, why: 'Equality requires special alignment of the rank-one summands; separability alone does not provide it.' },
        { label: 'Bound the sum by the largest single summand.', correct: false, why: 'The weights sum to one, but the quantity being bounded is already a weighted sum of norms; the correct general step is the triangle inequality.' }
      ]
    },
    {
      concept: 'triangle',
      context: 'Each summand is an outer product. This is where matrix structure enters.',
      formula: '$\\lVert u_kv_k^{\\mathsf T}\\rVert_*\\;\\;?$',
      question: 'Which exact identity applies to each summand?',
      result: '$\\lVert u_kv_k^{\\mathsf T}\\rVert_*=\\lVert u_k\\rVert_2\\lVert v_k\\rVert_2$',
      options: [
        { label: '$\\lVert u_kv_k^{\\mathsf T}\\rVert_*=\\lVert u_k\\rVert_2\\lVert v_k\\rVert_2$ because the matrix has rank at most one.', correct: true },
        { label: '$\\lVert u_kv_k^{\\mathsf T}\\rVert_*=\\lVert u_k\\rVert_2+\\lVert v_k\\rVert_2$.', correct: false, why: 'An outer product scales multiplicatively, not additively.' },
        { label: 'Replace the nuclear norm by the operator norm because they agree for every matrix.', correct: false, why: 'They agree here only because this particular matrix has rank at most one.' }
      ]
    },
    {
      concept: 'cauchy',
      context: 'The remaining expression is a weighted sum of products of two nonnegative deviations.',
      formula: '$\\sum_kp_k\\lVert u_k\\rVert_2\\lVert v_k\\rVert_2\\;\\;?$',
      question: 'Which inequality separates Alice’s and Bob’s fluctuations?',
      result: '$\\sum_kp_k\\lVert u_k\\rVert_2\\lVert v_k\\rVert_2\\leq\\sqrt{\\sum_kp_k\\lVert u_k\\rVert_2^2}\\sqrt{\\sum_kp_k\\lVert v_k\\rVert_2^2}$',
      options: [
        { label: 'Apply weighted Cauchy–Schwarz using $\\sqrt{p_k}\\lVert u_k\\rVert_2$ and $\\sqrt{p_k}\\lVert v_k\\rVert_2$.', correct: true },
        { label: 'Apply Jensen directly to replace every deviation by the deviation of the means.', correct: false, why: 'The mean deviations vanish; that would erase the covariance rather than bound it.' },
        { label: 'Use submultiplicativity of the operator norm.', correct: false, why: 'There is no matrix product left at this stage; the expression is a scalar weighted sum.' }
      ]
    },
    {
      concept: 'variance',
      context: 'For a pure local refinement, every local Bloch vector has norm $R_M$ or $R_N$.',
      formula: '$\\sum_kp_k\\lVert r_k-r\\rVert_2^2\\;\\;?$',
      question: 'What does expanding the square give?',
      result: '$\\sum_kp_k\\lVert r_k-r\\rVert_2^2=R_M^2-\\lVert r\\rVert_2^2$',
      options: [
        { label: '$R_M^2-\\lVert r\\rVert_2^2$: the second moment minus the square of the mean.', correct: true },
        { label: '$R_M^2+\\lVert r\\rVert_2^2$: both squared terms are positive.', correct: false, why: 'The cross term uses $r=\\sum_kp_kr_k$ and subtracts twice the squared mean.' },
        { label: '$R_M^2$ because centering does not affect a second moment.', correct: false, why: 'Centering removes the squared norm of the mean; that is precisely the variance deficit.' }
      ]
    },
    {
      concept: 'bound',
      context: 'Substitute the two variance identities into the Cauchy–Schwarz estimate.',
      formula: '$\\lVert C\\rVert_*\\;\\;?$',
      question: 'Which marginal-dependent criterion follows?',
      result: '$\\boxed{\\lVert C\\rVert_*\\leq\\sqrt{(R_M^2-\\lVert r\\rVert_2^2)(R_N^2-\\lVert s\\rVert_2^2)}}$',
      options: [
        { label: '$\\lVert C\\rVert_*\\leq\\sqrt{(R_M^2-\\lVert r\\rVert_2^2)(R_N^2-\\lVert s\\rVert_2^2)}$.', correct: true },
        { label: '$\\lVert C\\rVert_*\\leq R_MR_N+\\lVert r\\rVert_2\\lVert s\\rVert_2$.', correct: false, why: 'That discards the variance deficits and is not the centered bound.' },
        { label: '$\\lVert C\\rVert_*\\leq\\lVert r\\rVert_2\\lVert s\\rVert_2$.', correct: false, why: 'The centered covariance is controlled by fluctuations around the means, not by the product of the means.' }
      ]
    },
    {
      concept: 'bound',
      context: 'Finally use $T=C+rs^{\\mathsf T}$ and a two-dimensional Cauchy–Schwarz inequality.',
      formula: '$\\lVert T\\rVert_*\\leq\\lVert C\\rVert_*+\\lVert r\\rVert_2\\lVert s\\rVert_2\\leq R_MR_N.$',
      question: 'What is the correct logical comparison between the tests?',
      result: '$\\text{centered condition}\\Longrightarrow\\text{de Vicente condition}$',
      options: [
        { label: 'Passing the centered condition implies passing de Vicente; therefore violating de Vicente also violates the centered condition.', correct: true },
        { label: 'Passing de Vicente implies passing the centered condition.', correct: false, why: 'This reverses the implication. The centered test is the stronger necessary condition.' },
        { label: 'The two conditions are equivalent for every state.', correct: false, why: 'They coincide when the marginals are maximally mixed, but not in general.' }
      ]
    }
  ];

  function queueConceptNow(id) {
    if (state.fsrsCards[id]) state.fsrsCards[id].due = new Date(0).toISOString();
    delete sessionReviewed[id];
    if (scheduler) updateSchedule(new Date());
  }

  function renderBoundChallenge(message) {
    var progress = Math.min(Number(state.boundProgress || 0), boundSteps.length);
    state.boundProgress = progress;
    elements.boundStepLabel.textContent = progress === boundSteps.length ? '6 of 6' : (progress + 1) + ' of ' + boundSteps.length;
    elements.boundTrace.innerHTML = boundSteps.slice(0, progress).map(function (step, index) {
      return '<div><span>' + (index + 1) + '</span><p>' + step.result + '</p></div>';
    }).join('');
    if (!state.proofComplete) {
      elements.boundChallenge.hidden = false;
      elements.boundComplete.hidden = true;
      elements.boundContext.textContent = 'Complete the covariance-identity puzzle first. The bound starts from the identity proved there.';
      elements.boundFormula.innerHTML = '$C=\\sum_kp_k(r_k-r)(s_k-s)^{\\mathsf T}$';
      elements.boundQuestion.textContent = 'This stage is locked until the identity has been recovered.';
      elements.boundOptions.innerHTML = '';
      elements.boundFeedback.textContent = '';
      typeset(document.getElementById('bound-lab'));
      return;
    }
    if (progress === boundSteps.length) {
      state.boundComplete = true;
      elements.boundChallenge.hidden = true;
      elements.boundComplete.hidden = false;
      saveState();
      typeset(elements.boundTrace);
      return;
    }
    var step = boundSteps[progress];
    elements.boundChallenge.hidden = false;
    elements.boundComplete.hidden = true;
    elements.boundContext.innerHTML = step.context;
    elements.boundFormula.innerHTML = step.formula;
    elements.boundQuestion.textContent = step.question;
    elements.boundOptions.innerHTML = step.options.map(function (option, index) {
      return '<button type="button" data-bound-option="' + index + '">' + option.label + '</button>';
    }).join('');
    elements.boundFeedback.innerHTML = message || '';
    typeset(document.getElementById('bound-lab'));
  }

  elements.boundOptions.addEventListener('click', function (event) {
    var button = event.target.closest('[data-bound-option]');
    if (!button || button.disabled) return;
    var step = boundSteps[state.boundProgress];
    var option = step.options[Number(button.dataset.boundOption)];
    elements.boundOptions.querySelectorAll('button').forEach(function (item) { item.disabled = true; });
    if (!option.correct) {
      state.boundMistakes[step.concept] = (state.boundMistakes[step.concept] || 0) + 1;
      queueConceptNow(step.concept);
      button.classList.add('is-wrong');
      elements.boundFeedback.innerHTML = '<strong>Valid-looking, but wrong here.</strong> ' + option.why + ' <button type="button" class="explain-text-button" data-bound-retry>Try this bottleneck again</button>';
      saveState();
      typeset(elements.boundFeedback);
      return;
    }
    button.classList.add('is-correct');
    state.boundProgress += 1;
    if (state.boundProgress === boundSteps.length) state.boundComplete = true;
    saveState();
    elements.boundFeedback.innerHTML = '<strong>Recovered.</strong> ' + step.result + ' <button type="button" class="explain-button" data-bound-continue>' + (state.boundComplete ? 'Show the completed derivation' : 'Continue') + '</button>';
    typeset(elements.boundFeedback);
  });

  elements.boundFeedback.addEventListener('click', function (event) {
    if (event.target.closest('[data-bound-retry]')) renderBoundChallenge('Try again without using elimination from the previous layout.');
    if (event.target.closest('[data-bound-continue]')) renderBoundChallenge();
  });

  elements.boundReset.addEventListener('click', function () {
    state.boundProgress = 0;
    state.boundComplete = false;
    saveState();
    renderBoundChallenge('Derivation restarted.');
  });

  function initializeFsrs() {
    if (!window.FSRS || !window.FSRS.fsrs) {
      elements.reviewCard.innerHTML = '<p class="explain-notice">The FSRS scheduler could not be loaded. Reload the page to retry; the other four stages still work.</p>';
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
    if (stageStatus().filter(Boolean).length < 5) return;
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

  renderProofState(state.proofComplete ? 'Previously completed on this browser. Restart to explore another path.' : '');
  renderBoundChallenge();
  initializeDiagnosis();
  initializeBuilder();
  if (initializeFsrs()) renderReview();
  updateProgress();
})();
