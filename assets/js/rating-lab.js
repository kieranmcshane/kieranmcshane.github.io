(function () {
  'use strict';

  var root = document.querySelector('.rating-lab');
  if (!root) return;
  var sports = ['tennis', 'football', 'national-football', 'chess'];

  var state = {
    sport: 'tennis',
    model: 'elo',
    competition: '',
    query: '',
    sort: 'rank',
    direction: 1,
    selected: null,
    pinned: [],
    expanded: false,
    predictorCompetition: null,
    predictorModel: 'elo',
    predictorTeam: null,
    manifest: null,
    datasets: {}
  };

  var elements = {
    freshness: document.getElementById('rating-lab-freshness'),
    generation: document.getElementById('rating-lab-generation'),
    error: document.getElementById('rating-lab-error'),
    sportTabs: document.getElementById('sport-tabs'),
    modelTabs: document.getElementById('model-tabs'),
    protocolSportTabs: document.getElementById('protocol-sport-tabs'),
    protocolModelTabs: document.getElementById('protocol-model-tabs'),
    protocol: document.getElementById('rating-protocol'),
    competition: document.getElementById('competition-filter'),
    search: document.getElementById('rating-search'),
    metrics: document.getElementById('rating-metrics'),
    movers: document.getElementById('rating-movers'),
    context: document.getElementById('leaderboard-context'),
    body: document.getElementById('ranking-body'),
    empty: document.getElementById('ranking-empty'),
    more: document.getElementById('ranking-more'),
    caption: document.getElementById('ranking-caption'),
    detail: document.getElementById('rating-detail'),
    eligibility: document.getElementById('rating-eligibility'),
    parameterBody: document.getElementById('rating-parameter-body'),
    auditRecord: document.getElementById('rating-audit-record'),
    dataDownload: document.getElementById('rating-data-download'),
    predictorCompetition: document.getElementById('predictor-competition'),
    predictorModelTabs: document.getElementById('predictor-model-tabs'),
    predictorState: document.getElementById('predictor-state'),
    predictorMetrics: document.getElementById('predictor-metrics'),
    predictorCaption: document.getElementById('predictor-caption'),
    predictorBody: document.getElementById('predictor-body'),
    predictorDetail: document.getElementById('predictor-detail'),
    predictorMethod: document.getElementById('predictor-method-copy')
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

  function percent(value) {
    if (value === null || value === undefined) return '—';
    return new Intl.NumberFormat('en', {
      style: 'percent',
      maximumFractionDigits: value < 0.1 ? 1 : 0
    }).format(value);
  }

  function isStale(status) {
    if (!status || !status.checked_at || !status.stale_after_hours) return false;
    return Date.now() - new Date(status.checked_at).getTime() > status.stale_after_hours * 3600000;
  }

  function updateFreshness() {
    var statuses = state.manifest.sports;
    var labels = { tennis: 'Tennis', football: 'Clubs', 'national-football': 'Nations', chess: 'Chess' };
    var stale = sports.filter(function (sport) {
      return statuses[sport].status !== 'current' || isStale(statuses[sport]);
    });
    elements.freshness.classList.toggle('is-stale', stale.length > 0);
    elements.freshness.innerHTML = sports.map(function (sport) {
      var delayed = statuses[sport].status !== 'current' || isStale(statuses[sport]);
      return '<span class="rating-lab-freshness-chip' + (delayed ? ' is-stale' : '') + '"><i aria-hidden="true"></i>' +
        escapeHtml(labels[sport]) + ' · ' + escapeHtml(formatDate(statuses[sport].latest_result)) + '</span>';
    }).join('');
    var total = sports.reduce(function (sum, sport) {
      return sum + state.datasets[sport].models.elo.rankings.length;
    }, 0);
    elements.generation.textContent = number(total, 0) + ' published rankings · generated ' +
      formatDate(state.manifest.generated_at) + (stale.length ? ' · delayed sources retain their last valid snapshot' : '');
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
    var models = state.datasets[state.sport].models;
    var modelKeys = ['elo', 'trueskill', 'robust'];
    var selected = models[state.model].metrics;
    var definitions = [
      ['Brier score', 'brier', 4],
      ['Log loss', 'log_loss', 4],
      ['Calibration gap', 'calibration', 4]
    ];
    elements.metrics.innerHTML = definitions.map(function (definition) {
      var values = modelKeys.map(function (key) { return models[key].metrics[definition[1]]; });
      var min = Math.min.apply(null, values), max = Math.max.apply(null, values);
      var bars = modelKeys.map(function (key, index) {
        var relative = max === min ? 100 : 26 + (values[index] - min) / (max - min) * 74;
        return '<span class="rating-lab-metric-bar' + (key === state.model ? ' is-active' : '') +
          '" style="--metric-height:' + relative.toFixed(1) + '%" title="' + escapeHtml(models[key].label) +
          ': ' + number(values[index], definition[2]) + '"></span>';
      }).join('');
      return '<div class="rating-lab-metric"><span>' + definition[0] + '</span><div class="rating-lab-metric-value"><strong>' +
        number(selected[definition[1]], definition[2]) + '</strong><span class="rating-lab-metric-bars" aria-label="' +
        escapeHtml(definition[0]) + ' comparison: Elo ' + number(values[0], definition[2]) + ', Gaussian ' +
        number(values[1], definition[2]) + ', Robust ' + number(values[2], definition[2]) + '">' + bars +
        '</span></div><small>Lower is better · Elo / Gaussian / Robust</small></div>';
    }).concat(['<div class="rating-lab-metric"><span>Held-out predictions</span><div class="rating-lab-metric-value"><strong>' +
      number(selected.predictions, 0) + '</strong></div><small>Scored before each result updates the model</small></div>']).join('');
    elements.context.textContent = models[state.model].label + ' · ' +
      (state.competition || 'all competitions') + ' · ' + currentRows().length + ' published competitors';
  }

  function renderMovers() {
    var rows = currentRows().filter(function (row) { return Number.isFinite(row.change30); });
    var risers = rows.slice().sort(function (a, b) { return b.change30 - a.change30; }).slice(0, 3);
    var fallers = rows.slice().sort(function (a, b) { return a.change30 - b.change30; }).slice(0, 3);
    function group(label, items, positive) {
      return '<div><p>' + label + '</p><div>' + items.map(function (row) {
        var value = (positive && row.change30 > 0 ? '+' : '') + number(row.change30, 1);
        return '<button type="button" data-select="' + escapeHtml(row.id) + '"><span>' + escapeHtml(row.name) +
          '</span><strong class="' + (positive ? 'is-positive' : 'is-negative') + '">' + value + '</strong></button>';
      }).join('') + '</div></div>';
    }
    elements.movers.innerHTML = group('▲ Biggest risers · 30 days', risers, true) +
      group('▼ Biggest fallers · 30 days', fallers, false);
  }

  function miniSparkline(points, label) {
    if (!points || points.length < 2) return '<span class="rating-lab-mini-empty">—</span>';
    var recent = points.slice(-14), width = 94, height = 28, pad = 2;
    var values = recent.map(function (point) { return point[1]; });
    var min = Math.min.apply(null, values), max = Math.max.apply(null, values);
    if (max === min) max += 1;
    var coordinates = recent.map(function (point, index) {
      return (pad + index / (recent.length - 1) * (width - 2 * pad)).toFixed(1) + ',' +
        (height - pad - (point[1] - min) / (max - min) * (height - 2 * pad)).toFixed(1);
    }).join(' ');
    return '<svg class="rating-lab-mini-chart" viewBox="0 0 ' + width + ' ' + height + '" role="img" aria-label="' +
      escapeHtml(label) + ' recent range ' + number(min, 1) + ' to ' + number(max, 1) + '"><polyline points="' +
      coordinates + '"></polyline><title>Last ' + recent.length + ' updates · ' + number(min, 1) + ' to ' + number(max, 1) + '</title></svg>';
  }

  function renderTable() {
    var rows = currentRows();
    var displayed = state.expanded ? rows : rows.slice(0, 50);
    var model = state.datasets[state.sport].models[state.model];
    elements.caption.textContent = model.label + ' · ' + rows.length + ' published competitors';
    elements.empty.hidden = rows.length > 0;
    elements.more.hidden = rows.length <= displayed.length;
    elements.more.textContent = 'Show all ' + number(rows.length, 0) + ' competitors';
    elements.body.innerHTML = displayed.map(function (row) {
      var deltaClass = row.change30 > 0 ? 'is-positive' : row.change30 < 0 ? 'is-negative' : '';
      var delta = row.change30 > 0 ? '+' + number(row.change30, 1) : number(row.change30, 1);
      return '<tr data-id="' + escapeHtml(row.id) + '"' + (row.id === state.selected ? ' class="is-selected"' : '') + '>' +
        '<td class="rating-lab-rank">' + row.rank + '</td>' +
        '<th scope="row"><button type="button" class="rating-lab-entity" data-select="' + escapeHtml(row.id) + '"><span>' + escapeHtml(row.name) + '</span><small>' + escapeHtml(row.competition || row.country) + '</small></button></th>' +
        '<td class="rating-lab-trend-column">' + miniSparkline(row.history, row.name) + '</td>' +
        '<td><strong>' + number(row.score, 1) + '</strong></td>' +
        '<td class="rating-lab-optional">' + (row.sigma === null ? '—' : '±' + number(row.sigma, 1)) + '</td>' +
        '<td class="' + deltaClass + '">' + delta + '</td>' +
        '<td class="rating-lab-optional">' + number(row.recent_matches, 0) + '</td>' +
        '</tr>';
    }).join('');
  }

  function historyChart(series, label) {
    var usable = series.filter(function (item) { return item.points && item.points.length > 1; });
    if (!usable.length) return '<p class="rating-lab-detail-placeholder">Not enough history to chart yet.</p>';
    var width = 380, height = 178, left = 43, right = 8, top = 10, bottom = 28;
    var all = usable.reduce(function (items, item) { return items.concat(item.points); }, []);
    var values = all.map(function (point) { return point[1]; });
    var min = Math.min.apply(null, values), max = Math.max.apply(null, values);
    var range = max - min || 1;
    min -= range * 0.06;
    max += range * 0.06;
    var firstDate = Math.min.apply(null, all.map(function (point) { return new Date(point[0]).getTime(); }));
    var lastDate = Math.max.apply(null, all.map(function (point) { return new Date(point[0]).getTime(); }));
    if (lastDate === firstDate) lastDate += 86400000;
    function x(date) { return left + (new Date(date).getTime() - firstDate) / (lastDate - firstDate) * (width - left - right); }
    function y(value) { return top + (max - value) / (max - min) * (height - top - bottom); }
    var grid = [0, 1, 2, 3].map(function (index) {
      var value = min + (max - min) * index / 3;
      var yPos = y(value);
      return '<line class="rating-lab-gridline" x1="' + left + '" y1="' + yPos.toFixed(1) + '" x2="' +
        (width - right) + '" y2="' + yPos.toFixed(1) + '"></line><text x="' + (left - 6) + '" y="' +
        (yPos + 3).toFixed(1) + '" text-anchor="end">' + number(value, 0) + '</text>';
    }).join('');
    var paths = usable.map(function (item, seriesIndex) {
      var coordinates = item.points.map(function (point) { return x(point[0]).toFixed(1) + ',' + y(point[1]).toFixed(1); });
      var points = item.points.map(function (point) {
        return '<circle class="rating-lab-chart-hit" cx="' + x(point[0]).toFixed(1) + '" cy="' + y(point[1]).toFixed(1) +
          '" r="7" data-chart-point data-series="' + escapeHtml(item.name) + '" data-date="' + escapeHtml(point[0]) +
          '" data-value="' + point[1] + '"><title>' + escapeHtml(item.name) + ' · ' + escapeHtml(formatDate(point[0])) +
          ' · ' + number(point[1], 1) + '</title></circle>';
      }).join('');
      return '<polyline class="rating-lab-series-' + (seriesIndex + 1) + '" points="' + coordinates.join(' ') +
        '"></polyline>' + points;
    }).join('');
    var middleDate = new Date((firstDate + lastDate) / 2).toISOString().slice(0, 10);
    var dateLabels = [new Date(firstDate).toISOString().slice(0, 10), middleDate, new Date(lastDate).toISOString().slice(0, 10)];
    var axis = dateLabels.map(function (date, index) {
      return '<text x="' + (left + index * (width - left - right) / 2).toFixed(1) + '" y="' + (height - 6) +
        '" text-anchor="' + (index === 0 ? 'start' : index === 2 ? 'end' : 'middle') + '">' +
        escapeHtml(new Intl.DateTimeFormat('en', { month: 'short', year: '2-digit' }).format(new Date(date + 'T12:00:00Z'))) + '</text>';
    }).join('');
    var legend = usable.length > 1 ? '<div class="rating-lab-chart-legend">' + usable.map(function (item, index) {
      return '<span><i class="rating-lab-series-' + (index + 1) + '"></i>' + escapeHtml(item.name) + '</span>';
    }).join('') + '</div>' : '';
    return '<div class="rating-lab-chart-wrap"><svg class="rating-lab-chart" viewBox="0 0 ' + width + ' ' + height +
      '" role="img" aria-label="' + escapeHtml(label) + ' with labelled date and rating axes">' + grid + paths + axis +
      '<line class="rating-lab-crosshair" x1="0" y1="' + top + '" x2="0" y2="' + (height - bottom) + '"></line></svg>' +
      '<p class="rating-lab-chart-readout" aria-live="polite">Hover a point for its exact date and rating.</p>' + legend + '</div>';
  }

  function distribution(row, rows) {
    var values = rows.map(function (item) { return item.score; });
    var min = Math.min.apply(null, values), max = Math.max.apply(null, values), bins = 12;
    var width = (max - min || 1) / bins;
    var counts = Array(bins).fill(0);
    values.forEach(function (value) { counts[Math.min(bins - 1, Math.floor((value - min) / width))] += 1; });
    var tallest = Math.max.apply(null, counts) || 1;
    var selectedBin = Math.min(bins - 1, Math.floor((row.score - min) / width));
    var bars = counts.map(function (count, index) {
      var start = min + index * width, end = start + width;
      return '<button type="button" class="rating-lab-histogram-bar' + (index === selectedBin ? ' is-selected' : '') +
        '" style="--histogram-height:' + Math.max(4, count / tallest * 100).toFixed(1) + '%" data-histogram="' +
        number(start, 0) + '–' + number(end, 0) + ' · ' + count + ' competitors" aria-label="Ratings ' +
        number(start, 0) + ' to ' + number(end, 0) + ': ' + count + ' competitors"></button>';
    }).join('');
    return '<div class="rating-lab-distribution"><p class="rating-lab-inspector-label">Rating distribution</p><div class="rating-lab-histogram">' +
      bars + '</div><div class="rating-lab-histogram-axis"><span>' + number(min, 0) + '</span><span>' + number(max, 0) +
      '</span></div><p class="rating-lab-histogram-readout">Selected: ' + number(row.score, 1) + '</p></div>';
  }

  function renderDetail() {
    var dataset = state.datasets[state.sport];
    var rows = dataset.models[state.model].rankings;
    var row = rows.find(function (candidate) { return candidate.id === state.selected; });
    if (!row) {
      elements.detail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a row to inspect history, compare models, and pin competitors.</p>';
      return;
    }
    var modelKeys = ['elo', 'trueskill', 'robust'];
    var crossModel = modelKeys.map(function (key) {
      var modelRow = dataset.models[key].rankings.find(function (candidate) { return candidate.id === row.id; });
      return '<tr><th scope="row">' + escapeHtml(dataset.models[key].label) + '</th><td>' +
        (modelRow ? '#' + modelRow.rank : '—') + '</td><td>' + (modelRow ? number(modelRow.score, 1) : '—') +
        '</td><td>' + (modelRow && modelRow.sigma !== null ? '±' + number(modelRow.sigma, 1) : '—') + '</td></tr>';
    }).join('');
    var isPinned = state.pinned.indexOf(row.id) !== -1;
    var pinnedRows = state.pinned.map(function (id) {
      return rows.find(function (candidate) { return candidate.id === id; });
    }).filter(Boolean);
    var compare = '';
    if (pinnedRows.length) {
      compare = '<div class="rating-lab-compare"><div class="rating-lab-compare-heading"><p class="rating-lab-inspector-label">Pinned comparison</p><div>' +
        pinnedRows.map(function (item) { return '<button type="button" data-unpin="' + escapeHtml(item.id) + '">' +
          escapeHtml(item.name) + ' ×</button>'; }).join('') + '</div></div>' +
        (pinnedRows.length === 2 ? historyChart(pinnedRows.map(function (item) { return { name: item.name, points: item.history }; }),
          pinnedRows[0].name + ' and ' + pinnedRows[1].name + ' rating comparison') :
          '<p class="rating-lab-detail-placeholder">Pin one more competitor to overlay both histories.</p>') + '</div>';
    }
    elements.detail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">Rank ' + row.rank +
      '</p><h3>' + escapeHtml(row.name) + '</h3></div><strong>' + number(row.score, 1) + '</strong></div>' +
      '<button type="button" class="rating-lab-pin" data-pin="' + escapeHtml(row.id) + '" aria-pressed="' +
      (isPinned ? 'true' : 'false') + '">' + (isPinned ? 'Pinned for comparison' : 'Pin for comparison') + '</button>' +
      historyChart([{ name: row.name, points: row.history }], row.name + ' rating history') +
      '<p class="rating-lab-inspector-label">Across all three models</p><table class="rating-lab-model-compare"><thead><tr><th>Model</th><th>Rank</th><th>Score</th><th>±σ</th></tr></thead><tbody>' +
      crossModel + '</tbody></table>' + distribution(row, rows) +
      '<dl><div><dt>Last played</dt><dd>' + formatDate(row.last_played) + '</dd></div><div><dt>Recent matches</dt><dd>' + row.recent_matches + '</dd></div><div><dt>All matches</dt><dd>' + row.matches + '</dd></div>' +
      (row.sigma === null ? '' : '<div><dt>Uncertainty σ</dt><dd>' + number(row.sigma, 2) + '</dd></div>') + '</dl>' + compare;
  }

  function parameterText(parameters) {
    return Object.keys(parameters).sort().map(function (key) {
      var value = parameters[key];
      return key + '=' + (typeof value === 'number' ? number(value, 4) : String(value));
    }).join(', ');
  }

  function renderAudit() {
    var data = state.datasets[state.sport];
    var status = state.manifest.sports[state.sport];
    var modelNames = ['elo', 'trueskill', 'robust'];
    elements.eligibility.textContent = data.eligibility.rule + ' “Recent” covers ' +
      number(data.eligibility.recent_window_days, 0) + ' days for this cohort.';
    elements.parameterBody.innerHTML = modelNames.map(function (model) {
      var candidates = data.candidate_parameters[model].map(parameterText).join(' · ');
      return '<tr><th scope="row">' + escapeHtml(data.models[model].label) + '</th>' +
        '<td><code>' + escapeHtml(parameterText(data.parameters[model])) + '</code></td>' +
        '<td><code>' + escapeHtml(candidates) + '</code></td></tr>';
    }).join('');
    var revision = state.manifest.code_revision || 'unknown';
    var snapshot = data.source.snapshot_sha256 || 'Published through source API/archive';
    elements.auditRecord.innerHTML = [
      ['Schema', data.schema_version],
      ['Method', state.manifest.methodology_version || '—'],
      ['Code revision', revision.substring(0, 12)],
      ['Generated', formatDate(data.generated_at)],
      ['Data window', formatDate(data.data_window.first_result) + ' – ' + formatDate(data.data_window.last_result)],
      ['Input size', number(data.data_window.matches, 0) + ' results · ' + number(data.data_window.entities, 0) + ' entities'],
      ['Source state', status.status],
      ['Snapshot SHA-256', snapshot]
    ].map(function (item) {
      return '<div><dt>' + escapeHtml(item[0]) + '</dt><dd>' + escapeHtml(item[1]) + '</dd></div>';
    }).join('');
    elements.dataDownload.href = dataUrl(state.sport + '.json');
  }

  function dateBefore(value, days) {
    var shifted = new Date(value + 'T12:00:00Z');
    shifted.setUTCDate(shifted.getUTCDate() - days);
    return shifted.toISOString().slice(0, 10);
  }

  function protocolSportRules(sport) {
    var rules = {
      tennis: {
        label: 'ATP singles',
        input: 'Completed tour-level singles results. Player identity uses the source player code; tournament start date is the available chronological date. Surface is retained as metadata but is not used by the models.',
        venue: 'No home or venue advantage. Draws are not valid tennis outcomes.',
        initialization: 'Every player starts at Elo 1500 or Bayesian μ=25, σ=8.333.',
        special: 'No seasonal regression.'
      },
      football: {
        label: 'European club football',
        input: 'Full-time results from the five covered domestic leagues and Champions League. Club identity uses the source ID, with normalized names only for the documented OpenFootball fallback.',
        venue: 'The listed home team receives the selected home advantage. A draw is y=0.5.',
        initialization: 'Every club starts at Elo 1500 or Bayesian μ=25, σ=8.333.',
        special: 'Only club Elo regresses 25% toward 1500 when the season label changes. Bayesian models do not receive seasonal mean reversion.'
      },
      'national-football': {
        label: "Men's national teams",
        input: 'Completed men’s full internationals since 2016. Country identity is a normalized team name from the CC0 source.',
        venue: 'Home advantage applies only when the source does not mark the match neutral. A draw is y=0.5.',
        initialization: 'Every national team starts at Elo 1500 or Bayesian μ=25, σ=8.333.',
        special: 'No seasonal regression; all recorded tournament and friendly results receive the same update weight.'
      },
      chess: {
        label: 'Elite over-the-board chess',
        input: 'Decisive games and draws from official Lichess broadcast PGNs. Both players must have numeric FIDE IDs; online games and engine identities are excluded.',
        venue: 'White receives the selected color advantage. A draw is y=0.5.',
        initialization: 'At first appearance, Elo is initialized from the PGN FIDE rating when it is at least 1000. Bayesian μ=25+(FIDE−2000)/80 with σ=3; otherwise the generic prior is retained.',
        special: 'All valid FIDE-identified broadcast games update ratings; the 2200 official-rating threshold applies to publication eligibility.'
      }
    };
    return rules[sport];
  }

  function protocolModelRules(model, parameters) {
    if (model === 'elo') {
      return {
        prediction: 'Compute expected score p = 1 / (1 + 10^−((Rₐ + advantage − Rᵦ) / scale)).',
        update: 'After recording p, update both sides symmetrically: R′ₐ = Rₐ + K(y−p) and R′ᵦ = Rᵦ − K(y−p).',
        publication: 'Publish and rank the raw Elo rating. Elo has no uncertainty estimate.',
        constants: 'Initial rating 1500. Selected K=' + number(parameters.k, 4) + ', scale=' + number(parameters.scale, 4) + ', advantage=' + number(parameters.home, 4) + '.'
      };
    }
    var robust = model === 'robust';
    return {
      prediction: 'Integrate win, draw, and loss likelihoods over the Gaussian belief for the skill difference using the fixed 20-node Gauss–Hermite rule. Expected score is p(win)+0.5p(draw).',
      update: 'Before prediction, add τ² × max(days inactive / 7, 1) to each variance. Condition on the observed result, numerically compute the posterior moments, then moment-match back to independent Gaussian beliefs.',
      publication: 'Publish μ and σ, but rank by the conservative score μ−3σ. More uncertainty therefore lowers the published rank.',
      constants: 'Initial μ=25 and σ=8.333; τ=0.08333; performance noise ' + (robust ? 'Student-t ν=1 (Cauchy)' : 'Gaussian') +
        '; β=' + number(parameters.beta, 4) + '; draw margin=' + number(parameters.draw_margin, 4) + '; advantage=' + number(parameters.advantage, 4) + '.'
    };
  }

  function protocolParameterMeaning(key) {
    return {
      k: 'Maximum Elo response scale for one result',
      scale: 'Rating-gap width in the Elo logistic curve',
      home: 'Elo points added only when the advantage flag is true',
      beta: 'Performance-noise scale; larger values expect more upsets',
      draw_margin: 'Skill-difference interval treated as a draw',
      advantage: 'Bayesian skill units added when home/White advantage is active',
      robust: 'Whether performance noise uses Student-t ν=1 rather than Gaussian'
    }[key] || key;
  }

  function renderProtocol() {
    var data = state.datasets[state.sport];
    var model = data.models[state.model];
    var parameters = data.parameters[state.model];
    var sportRules = protocolSportRules(state.sport);
    var modelRules = protocolModelRules(state.model, parameters);
    var latest = data.data_window.last_result;
    var validationStart = dateBefore(latest, 730);
    var evaluationStart = dateBefore(latest, 365);
    var parameterRows = Object.keys(parameters).sort().map(function (key) {
      var value = parameters[key];
      return '<div><dt><code>' + escapeHtml(key) + '</code></dt><dd><strong>' +
        escapeHtml(typeof value === 'number' ? number(value, 4) : String(value)) + '</strong><span>' +
        escapeHtml(protocolParameterMeaning(key)) + '</span></dd></div>';
    }).join('');
    var candidates = data.candidate_parameters[state.model].map(parameterText).join(' · ');
    var metric = model.metrics;
    elements.protocol.innerHTML = '<p class="rating-lab-protocol-status"><strong>' + escapeHtml(sportRules.label) +
      ' · ' + escapeHtml(model.label) + '</strong><span>Source window ' + escapeHtml(formatDate(data.data_window.first_result)) +
      '–' + escapeHtml(formatDate(latest)) + ' · ' + number(data.data_window.matches, 0) + ' deduplicated results</span></p>' +
      '<ol class="rating-lab-protocol-flow">' +
      '<li><span>1</span><div><h3>Accept and identify</h3><p>' + escapeHtml(sportRules.input) + '</p></div></li>' +
      '<li><span>2</span><div><h3>Order deterministically</h3><p>Deduplicate exact date/entity/score/competition signatures, then sort by date, entity A ID, entity B ID, competition, and score. ' + escapeHtml(sportRules.initialization) + '</p></div></li>' +
      '<li><span>3</span><div><h3>Predict before learning</h3><p>' + escapeHtml(modelRules.prediction + ' ' + sportRules.venue) + '</p></div></li>' +
      '<li><span>4</span><div><h3>Apply the result</h3><p>' + escapeHtml(modelRules.update + ' ' + sportRules.special) + '</p></div></li>' +
      '<li><span>5</span><div><h3>Evaluate and publish</h3><p>' + escapeHtml(modelRules.publication) + ' Histories are display-downsampled to at most 24 points; rating replay itself is not downsampled.</p></div></li>' +
      '</ol><div class="rating-lab-protocol-grid"><article><h3>Selected parameters</h3><dl class="rating-lab-protocol-parameters">' +
      parameterRows + '</dl><p class="rating-lab-protocol-fixed"><strong>Fixed constants:</strong> ' + escapeHtml(modelRules.constants) +
      '</p></article><article><h3>Eligibility and publication</h3><p>' + escapeHtml(data.eligibility.rule) + '</p><p>“Recent” counts the latest ' +
      number(data.eligibility.recent_window_days, 0) + ' days. After eligibility, the public file retains at most the top 500 entities for each model.</p>' +
      '<h3>Candidate grid actually tested</h3><p><code>' + escapeHtml(candidates) + '</code></p></article></div>' +
      '<div class="rating-lab-protocol-evaluation"><h3>Chronological tuning and untouched evaluation</h3><div><p><strong>Warm-up</strong><span>Before ' +
      escapeHtml(formatDate(validationStart)) + '</span></p><p><strong>Validation</strong><span>' + escapeHtml(formatDate(validationStart)) +
      '–' + escapeHtml(formatDate(evaluationStart)) + '</span></p><p><strong>Evaluation</strong><span>' + escapeHtml(formatDate(evaluationStart)) +
      '–' + escapeHtml(formatDate(latest)) + '</span></p></div><p>Choose the declared candidate with the lowest validation log loss. Then score ' +
      number(metric.predictions, 0) + ' one-step-ahead evaluation predictions: log loss ' + number(metric.log_loss, 4) +
      ', Brier ' + number(metric.brier, 4) + ', calibration gap ' + number(metric.calibration, 4) +
      '. Calibration uses 10 equal-width probability bins and a count-weighted absolute predicted-versus-observed gap.</p></div>';
    setPressed(elements.protocolSportTabs, 'protocolSport', state.sport);
    setPressed(elements.protocolModelTabs, 'protocolModel', state.model);
  }

  function predictorData() {
    var predictor = state.datasets.football.tournament_predictor;
    var competition = predictor.competitions.find(function (item) {
      return item.id === state.predictorCompetition;
    });
    return { predictor: predictor, competition: competition, model: competition.models[state.predictorModel] };
  }

  function probabilityCell(value) {
    return '<span class="rating-lab-probability" style="--probability:' +
      (value * 100).toFixed(1) + '%"><span>' + percent(value) + '</span></span>';
  }

  function renderPredictorDetail(team, competition) {
    if (!team) {
      elements.predictorDetail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a team to inspect its full finishing-position distribution.</p>';
      return;
    }
    var bars = team.positions.map(function (probability, index) {
      var relegation = index >= team.positions.length - 3 ? ' is-relegation' : '';
      return '<span class="rating-lab-position-bar' + relegation + '" style="--height:' +
        Math.max(probability * 100, 1).toFixed(1) + '%" aria-label="Position ' + (index + 1) + ': ' +
        escapeHtml(percent(probability)) + '"></span>';
    }).join('');
    elements.predictorDetail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">Expected position ' +
      number(team.expected_position, 2) + '</p><h3>' + escapeHtml(team.name) + '</h3></div><strong>' +
      number(team.expected_points, 1) + ' pts</strong></div>' +
      '<div class="rating-lab-position-chart" role="img" aria-label="Finishing-position probabilities for ' +
      escapeHtml(team.name) + '">' + bars + '</div><div class="rating-lab-position-axis"><span>Champion</span><span>Position ' +
      team.positions.length + '</span></div><dl><div><dt>Title</dt><dd>' + percent(team.champion) +
      '</dd></div><div><dt>Top four</dt><dd>' + percent(team.top_four) +
      '</dd></div><div><dt>Bottom three</dt><dd>' + percent(team.bottom_three) +
      '</dd></div><div><dt>Current points</dt><dd>' + team.current_points + '</dd></div></dl>';
  }

  function renderPredictor() {
    var view = predictorData();
    var competition = view.competition;
    var model = view.model;
    if (!state.predictorTeam || !model.teams.some(function (team) { return team.id === state.predictorTeam; })) {
      state.predictorTeam = model.teams[0].id;
    }
    elements.predictorState.textContent = competition.status.charAt(0).toUpperCase() + competition.status.slice(1) +
      ' · fixtures through ' + formatDate(competition.last_fixture);
    elements.predictorMetrics.innerHTML = [
      ['Competition state', model.completed_matches + ' of ' + competition.total_matches + ' played'],
      ['Next fixture', competition.next_fixture ? formatDate(competition.next_fixture) : 'Competition complete'],
      ['Forecast sample', number(model.simulations, 0) + ' deterministic seasons']
    ].map(function (item) {
      return '<div><span>' + escapeHtml(item[0]) + '</span><strong>' + escapeHtml(item[1]) + '</strong></div>';
    }).join('');
    elements.predictorCaption.textContent = competition.label + ' ' + competition.season + ' · projected by ' +
      state.datasets.football.models[state.predictorModel].label;
    elements.predictorBody.innerHTML = model.teams.map(function (team, index) {
      return '<tr' + (team.id === state.predictorTeam ? ' class="is-selected"' : '') + '><td class="rating-lab-rank">' +
        (index + 1) + '</td><th scope="row"><button type="button" class="rating-lab-predictor-team" data-predictor-team="' +
        escapeHtml(team.id) + '">' + escapeHtml(team.name) + '</button></th><td>' +
        (team.played ? team.current_rank : '—') + '</td><td><strong>' + number(team.expected_points, 1) +
        '</strong></td><td>' + probabilityCell(team.champion) + '</td><td class="rating-lab-optional">' +
        probabilityCell(team.top_four) + '</td><td class="rating-lab-optional">' + probabilityCell(team.bottom_three) + '</td></tr>';
    }).join('');
    renderPredictorDetail(model.teams.find(function (team) { return team.id === state.predictorTeam; }), competition);
    elements.predictorMethod.innerHTML = escapeHtml(view.predictor.simulations_per_model) +
      ' simulations per model and competition. Fixed seed: <code>' + escapeHtml(String(model.seed)) +
      '</code>. Fixture snapshot: <code>' + escapeHtml(competition.snapshot_sha256.substring(0, 12)) +
      '</code>. <a href="' + escapeHtml(competition.source_url) + '">Open fixture source</a>.';
  }

  function render() {
    updateFreshness();
    renderMetrics();
    renderMovers();
    renderTable();
    renderDetail();
    renderProtocol();
    renderAudit();
    renderPredictor();
  }

  elements.sportTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-sport]');
    if (!button || button.dataset.sport === state.sport) return;
    state.sport = button.dataset.sport;
    state.selected = null;
    state.pinned = [];
    state.expanded = false;
    setPressed(elements.sportTabs, 'sport', state.sport);
    populateCompetitions();
    render();
  });

  elements.modelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-model]');
    if (!button || button.dataset.model === state.model) return;
    state.model = button.dataset.model;
    state.expanded = false;
    setPressed(elements.modelTabs, 'model', state.model);
    render();
  });

  elements.protocolSportTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-protocol-sport]');
    if (!button || button.dataset.protocolSport === state.sport) return;
    state.sport = button.dataset.protocolSport;
    state.selected = null;
    state.pinned = [];
    state.expanded = false;
    setPressed(elements.sportTabs, 'sport', state.sport);
    populateCompetitions();
    render();
  });

  elements.protocolModelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-protocol-model]');
    if (!button || button.dataset.protocolModel === state.model) return;
    state.model = button.dataset.protocolModel;
    state.expanded = false;
    setPressed(elements.modelTabs, 'model', state.model);
    render();
  });

  elements.competition.addEventListener('change', function () {
    state.competition = elements.competition.value;
    state.expanded = false;
    renderMetrics();
    renderMovers();
    renderTable();
    renderDetail();
  });

  elements.search.addEventListener('input', function () {
    state.query = elements.search.value;
    state.expanded = false;
    renderMetrics();
    renderMovers();
    renderTable();
  });

  elements.more.addEventListener('click', function () {
    state.expanded = true;
    renderTable();
  });

  elements.body.addEventListener('click', function (event) {
    var button = event.target.closest('[data-select]');
    if (!button) return;
    state.selected = button.dataset.select;
    renderTable();
    renderDetail();
  });

  elements.movers.addEventListener('click', function (event) {
    var button = event.target.closest('[data-select]');
    if (!button) return;
    state.selected = button.dataset.select;
    renderTable();
    renderDetail();
  });

  elements.detail.addEventListener('click', function (event) {
    var pin = event.target.closest('[data-pin]');
    var unpin = event.target.closest('[data-unpin]');
    if (pin) {
      var index = state.pinned.indexOf(pin.dataset.pin);
      if (index === -1) {
        if (state.pinned.length === 2) state.pinned.shift();
        state.pinned.push(pin.dataset.pin);
      } else state.pinned.splice(index, 1);
      renderDetail();
    } else if (unpin) {
      state.pinned = state.pinned.filter(function (id) { return id !== unpin.dataset.unpin; });
      renderDetail();
    }
  });

  elements.detail.addEventListener('mouseover', function (event) {
    var point = event.target.closest('[data-chart-point]');
    var histogram = event.target.closest('[data-histogram]');
    if (point) {
      var chartWrap = point.closest('.rating-lab-chart-wrap');
      var crosshair = chartWrap.querySelector('.rating-lab-crosshair');
      var x = point.getAttribute('cx');
      crosshair.setAttribute('x1', x);
      crosshair.setAttribute('x2', x);
      crosshair.classList.add('is-visible');
      chartWrap.querySelector('.rating-lab-chart-readout').textContent = point.dataset.series + ' · ' +
        formatDate(point.dataset.date) + ' · ' + number(Number(point.dataset.value), 1);
    }
    if (histogram) histogram.closest('.rating-lab-distribution').querySelector('.rating-lab-histogram-readout').textContent = histogram.dataset.histogram;
  });

  elements.detail.addEventListener('focusin', function (event) {
    var histogram = event.target.closest('[data-histogram]');
    if (histogram) histogram.closest('.rating-lab-distribution').querySelector('.rating-lab-histogram-readout').textContent = histogram.dataset.histogram;
  });

  elements.predictorCompetition.addEventListener('change', function () {
    state.predictorCompetition = elements.predictorCompetition.value;
    state.predictorTeam = null;
    renderPredictor();
  });

  elements.predictorModelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-predictor-model]');
    if (!button || button.dataset.predictorModel === state.predictorModel) return;
    state.predictorModel = button.dataset.predictorModel;
    state.predictorTeam = null;
    setPressed(elements.predictorModelTabs, 'predictorModel', state.predictorModel);
    renderPredictor();
  });

  elements.predictorBody.addEventListener('click', function (event) {
    var button = event.target.closest('[data-predictor-team]');
    if (!button) return;
    state.predictorTeam = button.dataset.predictorTeam;
    renderPredictor();
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
      return Promise.all(sports.map(function (sport) {
        return fetch(dataUrl(sport + '.json')).then(function (response) {
          if (!response.ok) throw new Error(sport + ' ratings could not be loaded.');
          return response.json();
        }).then(function (payload) { state.datasets[sport] = payload; });
      }));
    })
    .then(function () {
      var predictor = state.datasets.football.tournament_predictor;
      elements.predictorCompetition.innerHTML = predictor.competitions.map(function (competition) {
        return '<option value="' + escapeHtml(competition.id) + '">' + escapeHtml(competition.label + ' ' + competition.season) + '</option>';
      }).join('');
      state.predictorCompetition = predictor.competitions[0].id;
      populateCompetitions();
      render();
    })
    .catch(function (error) {
      elements.freshness.hidden = true;
      elements.error.hidden = false;
      elements.error.textContent = error.message + ' Please try again later.';
    });
}());
