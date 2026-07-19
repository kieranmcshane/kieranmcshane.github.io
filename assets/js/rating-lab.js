(function () {
  'use strict';

  var root = document.querySelector('.rating-lab');
  if (!root) return;

  var state = {
    sport: 'tennis',
    model: 'elo',
    competition: '',
    query: '',
    sort: 'rank',
    direction: 1,
    selected: null,
    manifest: null,
    datasets: {}
  };

  var elements = {
    freshness: document.getElementById('rating-lab-freshness'),
    error: document.getElementById('rating-lab-error'),
    sportTabs: document.getElementById('sport-tabs'),
    modelTabs: document.getElementById('model-tabs'),
    competition: document.getElementById('competition-filter'),
    search: document.getElementById('rating-search'),
    metrics: document.getElementById('rating-metrics'),
    body: document.getElementById('ranking-body'),
    empty: document.getElementById('ranking-empty'),
    caption: document.getElementById('ranking-caption'),
    detail: document.getElementById('rating-detail')
  };

  function dataUrl(file) {
    return root.dataset.dataRoot.replace(/\/$/, '') + '/' + file;
  }

  function formatDate(value) {
    if (!value) return 'Unknown';
    return new Intl.DateTimeFormat('en', { day: 'numeric', month: 'short', year: 'numeric' })
      .format(new Date(value + (value.length === 10 ? 'T12:00:00Z' : '')));
  }

  function number(value, digits) {
    if (value === null || value === undefined) return '—';
    return new Intl.NumberFormat('en', { maximumFractionDigits: digits }).format(value);
  }

  function isStale(status) {
    if (!status || !status.checked_at || !status.stale_after_hours) return false;
    return Date.now() - new Date(status.checked_at).getTime() > status.stale_after_hours * 3600000;
  }

  function updateFreshness() {
    var statuses = state.manifest.sports;
    var stale = Object.keys(statuses).filter(function (sport) {
      return statuses[sport].status !== 'current' || isStale(statuses[sport]);
    });
    elements.freshness.classList.toggle('is-stale', stale.length > 0);
    elements.freshness.textContent = stale.length
      ? 'Some sources are delayed; the last valid rankings remain available.'
      : 'Sources current · latest result ' + formatDate(statuses[state.sport].latest_result);
  }

  function setPressed(container, key, value) {
    container.querySelectorAll('button').forEach(function (button) {
      button.setAttribute('aria-pressed', button.dataset[key] === value ? 'true' : 'false');
    });
  }

  function populateCompetitions() {
    var data = state.datasets[state.sport];
    var options = ['<option value="">All competitions</option>'];
    data.competitions.forEach(function (competition) {
      options.push('<option value="' + escapeHtml(competition) + '">' + escapeHtml(competition) + '</option>');
    });
    elements.competition.innerHTML = options.join('');
    state.competition = '';
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, function (character) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character];
    });
  }

  function currentRows() {
    var rows = state.datasets[state.sport].models[state.model].rankings.slice();
    var query = state.query.trim().toLocaleLowerCase();
    rows = rows.filter(function (row) {
      return (!state.competition || row.competition === state.competition) &&
        (!query || row.name.toLocaleLowerCase().indexOf(query) !== -1 || row.country.toLocaleLowerCase().indexOf(query) !== -1);
    });
    rows.sort(function (a, b) {
      var left = a[state.sort];
      var right = b[state.sort];
      if (left === null || left === undefined) return 1;
      if (right === null || right === undefined) return -1;
      if (typeof left === 'string') return left.localeCompare(right) * state.direction;
      return (left - right) * state.direction;
    });
    return rows;
  }

  function renderMetrics() {
    var model = state.datasets[state.sport].models[state.model];
    var metric = model.metrics;
    elements.metrics.innerHTML = [
      ['Brier score', number(metric.brier, 4), 'Lower is better'],
      ['Log loss', number(metric.log_loss, 4), 'Lower is better'],
      ['Calibration gap', number(metric.calibration, 4), number(metric.predictions, 0) + ' held-out predictions']
    ].map(function (item) {
      return '<div class="rating-lab-metric"><span>' + item[0] + '</span><strong>' + item[1] + '</strong><small>' + item[2] + '</small></div>';
    }).join('');
  }

  function renderTable() {
    var rows = currentRows();
    var model = state.datasets[state.sport].models[state.model];
    elements.caption.textContent = model.label + ' · ' + rows.length + ' eligible competitors';
    elements.empty.hidden = rows.length > 0;
    elements.body.innerHTML = rows.map(function (row) {
      var deltaClass = row.change30 > 0 ? 'is-positive' : row.change30 < 0 ? 'is-negative' : '';
      var delta = row.change30 > 0 ? '+' + number(row.change30, 1) : number(row.change30, 1);
      return '<tr data-id="' + escapeHtml(row.id) + '"' + (row.id === state.selected ? ' class="is-selected"' : '') + '>' +
        '<td class="rating-lab-rank">' + row.rank + '</td>' +
        '<th scope="row"><button type="button" class="rating-lab-entity" data-select="' + escapeHtml(row.id) + '"><span>' + escapeHtml(row.name) + '</span><small>' + escapeHtml(row.competition || row.country) + '</small></button></th>' +
        '<td><strong>' + number(row.score, 1) + '</strong></td>' +
        '<td class="rating-lab-optional">' + (row.sigma === null ? '—' : '±' + number(row.sigma, 1)) + '</td>' +
        '<td class="' + deltaClass + '">' + delta + '</td>' +
        '<td class="rating-lab-optional">' + number(row.recent_matches, 0) + '</td>' +
        '</tr>';
    }).join('');
  }

  function sparkline(points, label) {
    if (!points || points.length < 2) return '<p class="rating-lab-detail-placeholder">Not enough history to chart yet.</p>';
    var width = 360, height = 132, padding = 12;
    var values = points.map(function (point) { return point[1]; });
    var min = Math.min.apply(null, values), max = Math.max.apply(null, values);
    if (max === min) max += 1;
    var coordinates = points.map(function (point, index) {
      var x = padding + index / (points.length - 1) * (width - 2 * padding);
      var y = height - padding - (point[1] - min) / (max - min) * (height - 2 * padding);
      return x.toFixed(1) + ',' + y.toFixed(1);
    }).join(' ');
    return '<svg class="rating-lab-chart" viewBox="0 0 ' + width + ' ' + height + '" role="img" aria-label="Recent ' + escapeHtml(label) + ' rating history from ' + escapeHtml(formatDate(points[0][0])) + ' to ' + escapeHtml(formatDate(points[points.length - 1][0])) + '">' +
      '<line x1="' + padding + '" y1="' + (height - padding) + '" x2="' + (width - padding) + '" y2="' + (height - padding) + '"></line>' +
      '<polyline points="' + coordinates + '"></polyline>' +
      '<circle cx="' + coordinates.split(' ').pop().split(',')[0] + '" cy="' + coordinates.split(' ').pop().split(',')[1] + '" r="4"></circle>' +
      '</svg><div class="rating-lab-chart-scale"><span>' + number(min, 1) + '</span><span>' + number(max, 1) + '</span></div>';
  }

  function renderDetail() {
    var rows = state.datasets[state.sport].models[state.model].rankings;
    var row = rows.find(function (candidate) { return candidate.id === state.selected; });
    if (!row) {
      elements.detail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a row to inspect its recent rating history.</p>';
      return;
    }
    elements.detail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">Rank ' + row.rank + '</p><h3>' + escapeHtml(row.name) + '</h3></div><strong>' + number(row.score, 1) + '</strong></div>' +
      sparkline(row.history, row.name) +
      '<dl><div><dt>Last played</dt><dd>' + formatDate(row.last_played) + '</dd></div><div><dt>Recent matches</dt><dd>' + row.recent_matches + '</dd></div><div><dt>All matches</dt><dd>' + row.matches + '</dd></div>' +
      (row.sigma === null ? '' : '<div><dt>Uncertainty σ</dt><dd>' + number(row.sigma, 2) + '</dd></div>') + '</dl>';
  }

  function render() {
    updateFreshness();
    renderMetrics();
    renderTable();
    renderDetail();
  }

  elements.sportTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-sport]');
    if (!button || button.dataset.sport === state.sport) return;
    state.sport = button.dataset.sport;
    state.selected = null;
    setPressed(elements.sportTabs, 'sport', state.sport);
    populateCompetitions();
    render();
  });

  elements.modelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-model]');
    if (!button || button.dataset.model === state.model) return;
    state.model = button.dataset.model;
    setPressed(elements.modelTabs, 'model', state.model);
    render();
  });

  elements.competition.addEventListener('change', function () {
    state.competition = elements.competition.value;
    renderTable();
    renderDetail();
  });

  elements.search.addEventListener('input', function () {
    state.query = elements.search.value;
    renderTable();
  });

  elements.body.addEventListener('click', function (event) {
    var button = event.target.closest('[data-select]');
    if (!button) return;
    state.selected = button.dataset.select;
    renderTable();
    renderDetail();
  });

  document.querySelector('.rating-lab-table thead').addEventListener('click', function (event) {
    var button = event.target.closest('[data-sort]');
    if (!button) return;
    if (state.sort === button.dataset.sort) state.direction *= -1;
    else {
      state.sort = button.dataset.sort;
      state.direction = button.dataset.sort === 'name' ? 1 : -1;
    }
    renderTable();
  });

  fetch(dataUrl('manifest.json'))
    .then(function (response) {
      if (!response.ok) throw new Error('The ratings manifest could not be loaded.');
      return response.json();
    })
    .then(function (manifest) {
      state.manifest = manifest;
      return Promise.all(['tennis', 'football', 'chess'].map(function (sport) {
        return fetch(dataUrl(sport + '.json')).then(function (response) {
          if (!response.ok) throw new Error(sport + ' ratings could not be loaded.');
          return response.json();
        }).then(function (payload) { state.datasets[sport] = payload; });
      }));
    })
    .then(function () {
      populateCompetitions();
      render();
    })
    .catch(function (error) {
      elements.freshness.hidden = true;
      elements.error.hidden = false;
      elements.error.textContent = error.message + ' Please try again later.';
    });
}());
