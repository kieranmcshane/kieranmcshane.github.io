(function () {
  'use strict';

  var root = document.querySelector('.explain-lab');
  if (!root) return;

  var storageKey = root.dataset.storageKey || 'centered-correlation-explain-v1';
  var defaultState = {
    orderComplete: false,
    cardText: {},
    cardChecks: {},
    cardConfidence: {},
    vivaCorrect: 0,
    vivaAsked: 0,
    rehearsalComplete: false,
    ready: false,
    learnerName: ''
  };
  var state = loadState();
  var currentViva = 0;
  var rehearsalInterval = null;
  var rehearsalStartedAt = null;
  var rehearsalRemaining = 90;
  var mediaRecorder = null;
  var mediaStream = null;
  var audioChunks = [];
  var audioUrl = null;

  var vivaQuestions = [
    {
      question: 'Why does a product state give a rank-one correlation matrix?',
      answer: 'For a product state, every bipartite expectation factorizes into the product of the two local expectations. In Bloch coordinates this says <strong>$T=rs^{\\mathsf T}$</strong>, an outer product, so its rank is at most one.'
    },
    {
      question: 'Where is separability used in the centered identity?',
      answer: 'Separability supplies <strong>one common classical ensemble</strong>: the same weights $p_k$ generate $r$, $s$, and $T$. Without that common decomposition, the covariance expansion of $C$ does not follow.'
    },
    {
      question: 'Which two inequalities produce the centered bound?',
      answer: 'First use the triangle inequality together with $\\lVert uv^{\\mathsf T}\\rVert_*=\\lVert u\\rVert_2\\lVert v\\rVert_2$. Then apply weighted Cauchy–Schwarz to the products $\\lVert r_k-r\\rVert_2\\lVert s_k-s\\rVert_2$.'
    },
    {
      question: 'Why is the right-hand side marginal-dependent?',
      answer: 'The two factors are local variance deficits: $R_M^2-\\lVert r\\rVert_2^2$ and $R_N^2-\\lVert s\\rVert_2^2$. A nearly pure marginal has little remaining Bloch-vector variance, so a separable ensemble has a smaller centered-correlation budget.'
    },
    {
      question: 'Is the centered criterion a complete separability test?',
      answer: 'No. Violating it certifies entanglement, but satisfying it does not prove separability for general mixed states. The article gives an NPT family that the centered criterion misses for part of its parameter range.'
    },
    {
      question: 'What is genuinely equivalent to de Vicente?',
      answer: 'In the bipartite Euclidean setting, identifying $r\\otimes s$ with $rs^{\\mathsf T}$ makes the projective tensor norm exactly the matrix nuclear norm. The uncentered projective-norm bound is therefore de Vicente’s criterion in tensor language.'
    },
    {
      question: 'Why can the full projective norm be stronger than unfoldings for three parties?',
      answer: 'Every fully factorized tensor decomposition gives a rank-one decomposition of each unfolding, but an optimal unfolding decomposition need not factor across all parties. Hence $\\lVert T_{P\\mid P^c}\\rVert_*\\leq\\lVert T\\rVert_{\\pi,2}$, and the inequality can be strict.'
    },
    {
      question: 'Why is the top-order centered tensor not enough multipartitely?',
      answer: 'Entanglement can live in a lower-order subset tensor while the full tensor vanishes. One therefore needs the family of subset tensors and must require that all of them arise from the same separable ensemble.'
    },
    {
      question: 'What does partial transposition do to a two-qubit correlation matrix?',
      answer: 'In the Pauli basis, transposition fixes $\\sigma_x$ and $\\sigma_z$ and sends $\\sigma_y$ to $-\\sigma_y$. Partial transposition therefore flips the corresponding row or column of $T$. In the zero-marginal Bell-diagonal sector, PPT becomes $|t_1|+|t_2|+|t_3|\\leq1$.'
    }
  ];

  var elements = {
    orderList: document.getElementById('explain-order-list'),
    orderFeedback: document.getElementById('order-feedback'),
    checkOrder: document.getElementById('check-order'),
    resetOrder: document.getElementById('reset-order'),
    progressText: document.getElementById('explain-progress-text'),
    progressBar: document.getElementById('explain-progress-bar'),
    progressTrack: root.querySelector('.explain-progress-track'),
    vivaQuestion: document.getElementById('viva-question'),
    vivaAnswer: document.getElementById('viva-answer'),
    vivaCount: document.getElementById('viva-count'),
    vivaScore: document.getElementById('viva-score'),
    revealViva: document.getElementById('reveal-viva'),
    vivaRating: document.getElementById('viva-rating'),
    clock: document.getElementById('rehearsal-clock'),
    startRehearsal: document.getElementById('start-rehearsal'),
    recordRehearsal: document.getElementById('record-rehearsal'),
    finishRehearsal: document.getElementById('finish-rehearsal'),
    recordingStatus: document.getElementById('recording-status'),
    audio: document.getElementById('rehearsal-audio'),
    outline: document.getElementById('rehearsal-outline'),
    learnerName: document.getElementById('learner-name'),
    markReady: document.getElementById('mark-ready'),
    exportProgress: document.getElementById('export-progress'),
    importProgress: document.getElementById('import-progress'),
    resetProgress: document.getElementById('reset-progress'),
    readinessCopy: document.getElementById('readiness-copy'),
    readinessStatus: document.getElementById('readiness-status')
  };

  function loadState() {
    try {
      return Object.assign({}, defaultState, JSON.parse(localStorage.getItem(storageKey) || '{}'));
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

  function completedCards() {
    return root.querySelectorAll('.teach-back-card').length &&
      Array.prototype.every.call(root.querySelectorAll('.teach-back-card'), function (card) {
        return state.cardConfidence[card.dataset.card] === 'mastered';
      });
  }

  function stageStatus() {
    return [
      state.orderComplete,
      completedCards(),
      state.vivaCorrect >= 3,
      state.rehearsalComplete
    ];
  }

  function updateProgress() {
    var statuses = stageStatus();
    var complete = statuses.filter(Boolean).length;
    var stageNames = ['rebuild the proof', 'explain all five hinges', 'answer three viva questions', 'complete an oral rehearsal'];
    var remaining = stageNames.filter(function (_, index) { return !statuses[index]; });
    elements.progressText.textContent = complete + ' of 4 stages complete';
    elements.progressTrack.setAttribute('aria-valuenow', complete);
    elements.progressBar.style.width = (complete / 4 * 100) + '%';
    elements.markReady.disabled = complete < 4;
    elements.vivaScore.textContent = state.vivaCorrect;
    if (state.ready) {
      var name = state.learnerName.trim();
      elements.readinessStatus.textContent = (name ? name + ': ' : '') + 'ready to explain · completed on this browser.';
      elements.markReady.textContent = 'Ready to explain ✓';
    } else {
      elements.readinessStatus.textContent = complete === 4 ? 'All four stages are complete.' : '';
      elements.markReady.textContent = 'Mark as ready to explain';
    }
    elements.readinessCopy.textContent = complete === 4
      ? 'You have reconstructed the argument in four different ways. Mark it ready when that judgment feels honest.'
      : 'Still to do: ' + remaining.join('; ') + '.';
  }

  function numberOrderItems() {
    Array.prototype.forEach.call(elements.orderList.children, function (item, index) {
      item.querySelector('.explain-order-number').textContent = index + 1;
      item.querySelector('[data-move="up"]').disabled = index === 0;
      item.querySelector('[data-move="down"]').disabled = index === elements.orderList.children.length - 1;
    });
  }

  function initialOrder() {
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
    var order = Array.prototype.map.call(elements.orderList.children, function (item) {
      return Number(item.dataset.step);
    });
    var firstWrong = order.findIndex(function (step, index) { return step !== index + 1; });
    state.orderComplete = firstWrong === -1;
    elements.orderList.classList.toggle('is-correct', state.orderComplete);
    elements.orderFeedback.textContent = state.orderComplete
      ? 'Correct. Product → common mixture → centering → Cauchy–Schwarz → variance bound.'
      : 'Not yet. The first mismatch is at position ' + (firstWrong + 1) + '. Ask what information the next step needs.';
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

  function initializeCards() {
    root.querySelectorAll('.teach-back-card').forEach(function (card) {
      var id = card.dataset.card;
      var textarea = card.querySelector('textarea');
      var reveal = card.querySelector('.reveal-rubric');
      var rubric = card.querySelector('.teach-back-rubric');
      var checks = card.querySelectorAll('input[type="checkbox"]');
      var status = card.querySelector('[data-card-state]');
      textarea.value = state.cardText[id] || '';
      reveal.disabled = textarea.value.trim().length < 30;
      (state.cardChecks[id] || []).forEach(function (checked, index) {
        if (checks[index]) checks[index].checked = checked;
      });
      if (state.cardConfidence[id]) {
        rubric.hidden = false;
        reveal.hidden = true;
      }

      function updateCardStatus() {
        var confidence = state.cardConfidence[id];
        status.textContent = confidence === 'mastered' ? 'Ready' : confidence === 'review' ? 'Review' : textarea.value ? 'Drafted' : 'Not attempted';
        card.classList.toggle('is-mastered', confidence === 'mastered');
      }

      textarea.addEventListener('input', function () {
        state.cardText[id] = textarea.value;
        reveal.disabled = textarea.value.trim().length < 30;
        updateCardStatus();
        saveState();
      });

      reveal.addEventListener('click', function () {
        rubric.hidden = false;
        reveal.hidden = true;
        typeset(rubric);
      });

      checks.forEach(function (check) {
        check.addEventListener('change', function () {
          state.cardChecks[id] = Array.prototype.map.call(checks, function (item) { return item.checked; });
          if (!Array.prototype.every.call(checks, function (item) { return item.checked; })) {
            state.cardConfidence[id] = 'review';
          }
          updateCardStatus();
          saveState();
        });
      });

      card.querySelectorAll('[data-confidence]').forEach(function (button) {
        button.addEventListener('click', function () {
          var requested = button.dataset.confidence;
          var allChecked = Array.prototype.every.call(checks, function (item) { return item.checked; });
          state.cardConfidence[id] = requested === 'mastered' && allChecked ? 'mastered' : 'review';
          if (requested === 'mastered' && !allChecked) {
            status.textContent = 'Check every essential point first';
          } else {
            updateCardStatus();
          }
          saveState();
        });
      });
      updateCardStatus();
    });
  }

  function renderViva() {
    var item = vivaQuestions[currentViva];
    elements.vivaCount.textContent = 'Question ' + (state.vivaAsked + 1);
    elements.vivaQuestion.textContent = item.question;
    elements.vivaAnswer.innerHTML = item.answer;
    elements.vivaAnswer.hidden = true;
    elements.vivaRating.hidden = true;
    elements.revealViva.hidden = false;
    typeset(elements.vivaAnswer);
  }

  elements.revealViva.addEventListener('click', function () {
    elements.vivaAnswer.hidden = false;
    elements.vivaRating.hidden = false;
    elements.revealViva.hidden = true;
  });

  elements.vivaRating.addEventListener('click', function (event) {
    var button = event.target.closest('[data-viva-rating]');
    if (!button) return;
    if (button.dataset.vivaRating === 'correct') state.vivaCorrect += 1;
    state.vivaAsked += 1;
    currentViva = (currentViva + 1 + Math.floor(Math.random() * (vivaQuestions.length - 1))) % vivaQuestions.length;
    saveState();
    renderViva();
  });

  function selectedLength() {
    return Number(root.querySelector('input[name="rehearsal-length"]:checked').value);
  }

  function formatTime(seconds) {
    var minutes = Math.floor(seconds / 60);
    var remainder = seconds % 60;
    return String(minutes).padStart(2, '0') + ':' + String(remainder).padStart(2, '0');
  }

  function updateClock() {
    elements.clock.textContent = formatTime(Math.max(0, rehearsalRemaining));
  }

  root.querySelectorAll('input[name="rehearsal-length"]').forEach(function (radio) {
    radio.addEventListener('change', function () {
      if (!rehearsalInterval) {
        rehearsalRemaining = selectedLength();
        updateClock();
      }
    });
  });

  elements.startRehearsal.addEventListener('click', function () {
    if (rehearsalInterval) return;
    rehearsalRemaining = selectedLength();
    rehearsalStartedAt = Date.now();
    elements.finishRehearsal.disabled = false;
    elements.startRehearsal.disabled = true;
    elements.outline.open = false;
    updateClock();
    rehearsalInterval = window.setInterval(function () {
      rehearsalRemaining -= 1;
      updateClock();
      if (rehearsalRemaining <= 0) finishRehearsal(true);
    }, 1000);
  });

  function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') mediaRecorder.stop();
  }

  function finishRehearsal(timerEnded) {
    if (rehearsalInterval) window.clearInterval(rehearsalInterval);
    rehearsalInterval = null;
    stopRecording();
    var elapsed = rehearsalStartedAt ? Math.floor((Date.now() - rehearsalStartedAt) / 1000) : 0;
    state.rehearsalComplete = timerEnded || elapsed >= 30;
    elements.startRehearsal.disabled = false;
    elements.finishRehearsal.disabled = true;
    elements.outline.open = true;
    elements.recordingStatus.textContent = state.rehearsalComplete
      ? 'Rehearsal saved as complete. Compare your explanation with the outline.'
      : 'Speak for at least 30 seconds before marking the rehearsal complete.';
    saveState();
  }

  elements.finishRehearsal.addEventListener('click', function () { finishRehearsal(false); });

  elements.recordRehearsal.addEventListener('click', function () {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      stopRecording();
      return;
    }
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || !window.MediaRecorder) {
      elements.recordingStatus.textContent = 'Audio recording is not supported in this browser. The timer still works.';
      return;
    }
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
      mediaStream = stream;
      audioChunks = [];
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.addEventListener('dataavailable', function (event) {
        if (event.data.size) audioChunks.push(event.data);
      });
      mediaRecorder.addEventListener('stop', function () {
        var blob = new Blob(audioChunks, { type: mediaRecorder.mimeType || 'audio/webm' });
        if (audioUrl) URL.revokeObjectURL(audioUrl);
        audioUrl = URL.createObjectURL(blob);
        elements.audio.src = audioUrl;
        elements.audio.hidden = false;
        elements.recordRehearsal.textContent = 'Record again';
        elements.recordingStatus.textContent = 'Recording stopped. Playback is available below and remains local.';
        mediaStream.getTracks().forEach(function (track) { track.stop(); });
      });
      mediaRecorder.start();
      elements.recordRehearsal.textContent = 'Stop recording';
      elements.recordingStatus.textContent = 'Recording locally…';
      if (!rehearsalInterval) elements.startRehearsal.click();
    }).catch(function () {
      elements.recordingStatus.textContent = 'Microphone access was not granted. You can still rehearse with the timer.';
    });
  });

  elements.learnerName.value = state.learnerName || '';
  elements.learnerName.addEventListener('input', function () {
    state.learnerName = elements.learnerName.value;
    saveState();
  });

  elements.markReady.addEventListener('click', function () {
    if (stageStatus().filter(Boolean).length < 4) return;
    state.ready = true;
    saveState();
  });

  elements.exportProgress.addEventListener('click', function () {
    var exportState = Object.assign({}, state, {
      exportedAt: new Date().toISOString(),
      article: 'Centered Correlation Tensors and Quantum Separability'
    });
    var blob = new Blob([JSON.stringify(exportState, null, 2)], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = url;
    link.download = 'centered-correlation-explain-progress.json';
    link.click();
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 0);
  });

  elements.importProgress.addEventListener('change', function () {
    var file = elements.importProgress.files && elements.importProgress.files[0];
    if (!file) return;
    file.text().then(function (content) {
      var imported = JSON.parse(content);
      if (!imported || imported.article !== 'Centered Correlation Tensors and Quantum Separability') {
        throw new Error('Unexpected progress file');
      }
      state = Object.assign({}, defaultState, imported);
      localStorage.setItem(storageKey, JSON.stringify(state));
      window.location.reload();
    }).catch(function () {
      elements.readinessStatus.textContent = 'That file is not a valid progress export for this article.';
      elements.importProgress.value = '';
    });
  });

  elements.resetProgress.addEventListener('click', function () {
    if (!window.confirm('Erase the explanations and progress stored in this browser?')) return;
    localStorage.removeItem(storageKey);
    window.location.reload();
  });

  window.addEventListener('beforeunload', function () {
    if (audioUrl) URL.revokeObjectURL(audioUrl);
    if (mediaStream) mediaStream.getTracks().forEach(function (track) { track.stop(); });
  });

  initialOrder();
  initializeCards();
  currentViva = state.vivaAsked % vivaQuestions.length;
  renderViva();
  rehearsalRemaining = selectedLength();
  updateClock();
  updateProgress();
})();
