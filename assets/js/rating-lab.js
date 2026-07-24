(function () {
  'use strict';

  var root = document.querySelector('.rating-lab');
  if (!root) return;
  var sports = ['tennis', 'football', 'national-football', 'chess'];
  var modelKeys = ['elo', 'glicko2', 'trueskill', 'robust'];
  var ghNodes = [
    -5.387480890011233, -4.603682449550744, -3.944764040115625, -3.347854567383216,
    -2.788806058428130, -2.254974002089276, -1.738537712116586, -1.234076215395323,
    -0.737473728545394, -0.245340708300901, 0.245340708300901, 0.737473728545394,
    1.234076215395323, 1.738537712116586, 2.254974002089276, 2.788806058428130,
    3.347854567383216, 3.944764040115625, 4.603682449550744, 5.387480890011233
  ];
  var ghWeights = [
    2.229393645534151e-13, 4.399340992273181e-10, 1.086069370769281e-7,
    7.802556478532064e-6, 2.283386360163540e-4, 0.003243773342238,
    0.024810520887464, 0.109017206020023, 0.286675505362834, 0.462243669600610,
    0.462243669600610, 0.286675505362834, 0.109017206020023, 0.024810520887464,
    0.003243773342238, 2.283386360163540e-4, 7.802556478532064e-6,
    1.086069370769281e-7, 4.399340992273181e-10, 2.229393645534151e-13
  ];

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
    visibleRows: 0,
    includeProvisional: false,
    matchupA: null,
    matchupB: null,
    matchupVenue: 'neutral',
    predictorCompetition: null,
    predictorModel: 'elo',
    predictorTeam: null,
    manifest: null,
    datasets: {}
  };

  var elements = {
    localNav: document.querySelector('.rating-lab-local-nav'),
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
    mobileFilterTrigger: document.getElementById('rating-mobile-filters'),
    mobileFilterSheet: document.getElementById('rating-mobile-filter-sheet'),
    mobileFilterClose: document.getElementById('rating-mobile-filter-close'),
    mobileFilterApply: document.getElementById('rating-mobile-filter-apply'),
    mobileModelLabel: document.getElementById('rating-mobile-model-label'),
    mobileModelTabs: document.getElementById('rating-mobile-model-tabs'),
    mobileCompetition: document.getElementById('rating-mobile-competition'),
    mobileProvisionalControl: document.getElementById('rating-mobile-provisional-control'),
    mobileIncludeProvisional: document.getElementById('rating-mobile-include-provisional'),
    mobileProvisionalCount: document.getElementById('rating-mobile-provisional-count'),
    quickModel: document.getElementById('rating-quick-model'),
    quickModelMenu: document.getElementById('rating-quick-model-menu'),
    quickModelTrigger: document.getElementById('rating-quick-model-trigger'),
    quickModelLabel: document.getElementById('rating-quick-model-label'),
    metricsDisclosure: document.querySelector('.rating-lab-metrics-disclosure'),
    metrics: document.getElementById('rating-metrics'),
    movers: document.getElementById('rating-movers'),
    moversDisclosure: document.querySelector('.rating-lab-movers-disclosure'),
    context: document.getElementById('leaderboard-context'),
    rankingTable: document.getElementById('ranking-table'),
    body: document.getElementById('ranking-body'),
    empty: document.getElementById('ranking-empty'),
    more: document.getElementById('ranking-more'),
    caption: document.getElementById('ranking-caption'),
    provisionalControl: document.getElementById('rating-provisional-control'),
    includeProvisional: document.getElementById('rating-include-provisional'),
    provisionalCount: document.getElementById('rating-provisional-count'),
    provisionalNote: document.getElementById('rating-provisional-note'),
    detail: document.getElementById('rating-detail'),
    eligibility: document.getElementById('rating-eligibility'),
    parameterBody: document.getElementById('rating-parameter-body'),
    auditRecord: document.getElementById('rating-audit-record'),
    dataDownload: document.getElementById('rating-data-download'),
    matchupA: document.getElementById('matchup-a'),
    matchupB: document.getElementById('matchup-b'),
    matchupSwap: document.getElementById('matchup-swap'),
    matchupVenue: document.getElementById('matchup-venue'),
    matchupVenueLabel: document.getElementById('matchup-venue-label'),
    matchupModelTabs: document.getElementById('matchup-model-tabs'),
    matchupResult: document.getElementById('matchup-result'),
    predictorCompetition: document.getElementById('predictor-competition'),
    predictorModelTabs: document.getElementById('predictor-model-tabs'),
    predictorState: document.getElementById('predictor-state'),
    predictorMetrics: document.getElementById('predictor-metrics'),
    predictorMarket: document.getElementById('predictor-market'),
    predictorPerformanceChart: document.getElementById('predictor-performance-chart'),
    predictorCaption: document.getElementById('predictor-caption'),
    predictorBody: document.getElementById('predictor-body'),
    predictorDetail: document.getElementById('predictor-detail'),
    predictorMethod: document.getElementById('predictor-method-copy'),
    predictorColumns: {
      rank: document.getElementById('predictor-col-rank'),
      team: document.getElementById('predictor-col-team'),
      now: document.getElementById('predictor-col-now'),
      value: document.getElementById('predictor-col-value'),
      title: document.getElementById('predictor-col-title'),
      secondary: document.getElementById('predictor-col-secondary'),
      tertiary: document.getElementById('predictor-col-tertiary')
    }
  };

  if (window.matchMedia('(max-width: 650px)').matches) {
    elements.metricsDisclosure.open = false;
    elements.moversDisclosure.open = false;
  }

  function dataUrl(file) {
    return root.dataset.dataRoot.replace(/\/$/, '') + '/' + file;
  }

  function fetchJson(file) {
    return fetch(dataUrl(file)).then(function (response) {
      if (!response.ok) throw new Error(file + ' could not be loaded.');
      return response.json();
    });
  }

  function loadSportCore(sport) {
    return fetchJson('split/' + sport + '-core.json').catch(function () {
      return fetchJson(sport + '.json');
    }).then(function (payload) { state.datasets[sport] = payload; });
  }

  function ensureRankings(sport, model) {
    var dataset = state.datasets[sport];
    if (!dataset) return Promise.reject(new Error(sport + ' ratings are not loaded.'));
    var entry = dataset.models[model];
    if (entry.rankings) return Promise.resolve();
    if (entry.rankingsRequest) return entry.rankingsRequest;
    entry.rankingsRequest = fetchJson('split/' + sport + '-rankings-' + model + '.json').catch(function () {
      return fetchJson(sport + '.json').then(function (payload) { return payload.models[model]; });
    }).then(function (payload) {
      entry.rankings = payload.rankings || [];
      delete entry.rankingsRequest;
    }, function (error) {
      delete entry.rankingsRequest;
      throw error;
    });
    return entry.rankingsRequest;
  }

  function ensureModels(sport) {
    return Promise.all(modelKeys.map(function (model) { return ensureRankings(sport, model); }));
  }

  var renderQueued = false;

  function scheduleRender() {
    if (renderQueued) return;
    renderQueued = true;
    window.requestAnimationFrame(function () {
      renderQueued = false;
      render();
    });
  }

  var syncToken = 0;

  function syncData() {
    var token = ++syncToken;
    var wanted = [ensureRankings(state.sport, 'elo')];
    if (state.model !== 'elo') wanted.push(ensureRankings(state.sport, state.model));
    var loaded = state.datasets[state.sport].models[state.model].rankings &&
      state.datasets[state.sport].models.elo.rankings;
    if (!loaded) root.setAttribute('aria-busy', 'true');
    return Promise.all(wanted).then(function () {
      if (token !== syncToken) return;
      root.removeAttribute('aria-busy');
      render();
    }).catch(function (error) {
      if (token !== syncToken) return;
      root.removeAttribute('aria-busy');
      elements.error.hidden = false;
      elements.error.textContent = error.message + ' Please try again later.';
    });
  }

  function formatDate(value) {
    if (!value) return 'Unknown';
    return new Intl.DateTimeFormat('en', { day: 'numeric', month: 'short', year: 'numeric' })
      .format(new Date(value + (value.length === 10 ? 'T12:00:00Z' : '')));
  }

  function number(value, digits, minimumDigits) {
    if (value === null || value === undefined) return '—';
    var threshold = 0.5 * Math.pow(10, -digits);
    var normalized = Math.abs(value) < threshold ? 0 : value;
    return new Intl.NumberFormat('en', {
      minimumFractionDigits: minimumDigits === undefined ? 0 : minimumDigits,
      maximumFractionDigits: digits
    }).format(normalized);
  }

  function ratingNumber(value) {
    var digits = state.model === 'elo' ? 0 : 1;
    return number(value, digits, digits);
  }

  function signedNumber(value, digits) {
    if (value === null || value === undefined) return '—';
    var rounded = Math.round(value * Math.pow(10, digits)) / Math.pow(10, digits);
    if (Object.is(rounded, -0) || rounded === 0) return '0';
    return (rounded > 0 ? '+' : '') + number(rounded, digits, digits);
  }

  function percent(value) {
    if (value === null || value === undefined) return '—';
    return new Intl.NumberFormat('en', {
      style: 'percent',
      maximumFractionDigits: value < 0.1 ? 1 : 0
    }).format(value);
  }

  function competitionTitle(competition) {
    var season = String(competition.season || '');
    var label = String(competition.label || '').replace(/\s*\|\s*/g, ' · ');
    return season && label.indexOf(season) === -1 ? label + ' ' + season : label;
  }

  function competitionState(competition) {
    var value = competition.state || competition.status || '';
    if (value === 'complete') return 'finished';
    if (value === 'scheduled') return 'upcoming';
    if (value === 'waiting for draw') {
      return competition.completed_matches > 0 ? 'live' : 'upcoming';
    }
    return ['upcoming', 'live', 'finished'].indexOf(value) >= 0 ? value : 'upcoming';
  }

  function stateLabel(value) {
    return value.charAt(0).toUpperCase() + value.slice(1);
  }

  function renderCompetitionState(competition, competitionFormat) {
    var value = competitionState(competition);
    var fallback = {
      upcoming: 'Prior-heavy forecast from the published schedule or draw.',
      live: 'Current results are locked; every probability is conditional on the current state.',
      finished: 'Forecasts are replaced by protocol performance and actual-versus-expected analysis.'
    };
    elements.predictorState.className = 'rating-lab-predictor-state is-' + value;
    elements.predictorState.innerHTML = '<strong>' + escapeHtml(stateLabel(value)) +
      '</strong><span>' + escapeHtml(competition.state_message || fallback[value]) +
      '</span><small>' + escapeHtml(competitionFormat) + ' · through ' +
      escapeHtml(formatDate(competition.last_fixture)) + '</small>';
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
      var elo = state.datasets[sport].models.elo;
      return sum + (elo.rankings ? elo.rankings.length : elo.entity_count || 0);
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
    elements.mobileCompetition.innerHTML = options.join('');
    state.competition = '';
  }

  function syncMobileFilters() {
    var model = state.datasets[state.sport] && state.datasets[state.sport].models[state.model];
    elements.mobileModelLabel.textContent = model ? model.label : state.model;
    setPressed(elements.mobileModelTabs, 'mobileModel', state.model);
    elements.mobileCompetition.value = state.competition;
    var count = provisionalCount();
    elements.mobileProvisionalControl.hidden = count === 0;
    elements.mobileIncludeProvisional.checked = state.includeProvisional;
    elements.mobileProvisionalCount.textContent = number(count, 0);
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, function (character) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character];
    });
  }

  var regionCodesByName = null;

  function normalizedRegionName(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .toLocaleLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  }

  function buildRegionCodes() {
    if (regionCodesByName) return regionCodesByName;
    regionCodesByName = {};
    if (typeof Intl.DisplayNames === 'function') {
      var names = new Intl.DisplayNames(['en'], { type: 'region' });
      for (var first = 65; first <= 90; first += 1) {
        for (var second = 65; second <= 90; second += 1) {
          var code = String.fromCharCode(first, second);
          var name = names.of(code);
          if (name && name !== code) regionCodesByName[normalizedRegionName(name)] = code;
        }
      }
    }
    Object.assign(regionCodesByName, {
      'bolivia': 'BO', 'cape verde': 'CV', 'chinese taipei': 'TW', 'congo': 'CG',
      'czech republic': 'CZ', 'democratic republic of the congo': 'CD', 'dr congo': 'CD',
      'england': 'GB', 'eswatini': 'SZ', 'france': 'FR', 'hong kong': 'HK', 'iran': 'IR',
      'ivory coast': 'CI', 'kosovo': 'XK', 'laos': 'LA', 'moldova': 'MD',
      'north korea': 'KP', 'northern ireland': 'GB', 'palestine': 'PS',
      'republic of ireland': 'IE', 'russia': 'RU', 'scotland': 'GB', 'serbia': 'RS',
      'south korea': 'KR', 'syria': 'SY', 'tanzania': 'TZ', 'turkey': 'TR',
      'united states': 'US', 'venezuela': 'VE', 'vietnam': 'VN', 'wales': 'GB'
    });
    return regionCodesByName;
  }

  // ATP citizenship and FIDE federation fields use three-letter sporting
  // codes. Convert only declared source values; an unknown code stays blank
  // instead of assigning a country from a player's name.
  var sportingCountryCodes = {
    ALG: 'DZ', ARG: 'AR', ARM: 'AM', AUS: 'AU', AUT: 'AT', AZE: 'AZ', BEL: 'BE',
    BIH: 'BA', BLR: 'BY', BOL: 'BO', BRA: 'BR', BUL: 'BG', CAN: 'CA', CHI: 'CL',
    CHN: 'CN', CIV: 'CI', COL: 'CO', CRO: 'HR', CZE: 'CZ', DEN: 'DK', DOM: 'DO',
    ECU: 'EC', EGY: 'EG', ESP: 'ES', EST: 'EE', FIN: 'FI', FRA: 'FR', GBR: 'GB',
    GEO: 'GE', GER: 'DE', GRE: 'GR', HKG: 'HK', HUN: 'HU', INA: 'ID', IND: 'IN',
    IRI: 'IR', IRN: 'IR', IRQ: 'IQ', ISL: 'IS', ISR: 'IL', ITA: 'IT', JOR: 'JO',
    JPN: 'JP', KAZ: 'KZ', KOR: 'KR', KSA: 'SA', LAT: 'LV', LBN: 'LB', LTU: 'LT',
    LUX: 'LU', MAR: 'MA', MAS: 'MY', MDA: 'MD', MEX: 'MX', MKD: 'MK', MNE: 'ME',
    MON: 'MC', NED: 'NL', NOR: 'NO', NZL: 'NZ', PAK: 'PK', PAR: 'PY', PER: 'PE',
    PHI: 'PH', POL: 'PL', POR: 'PT', QAT: 'QA', ROU: 'RO', RSA: 'ZA', RUS: 'RU',
    SGP: 'SG', SLO: 'SI', SRB: 'RS', SUI: 'CH', SVK: 'SK', SWE: 'SE', THA: 'TH',
    TPE: 'TW', TUN: 'TN', TUR: 'TR', UAE: 'AE', UKR: 'UA', URU: 'UY', USA: 'US',
    UZB: 'UZ', VEN: 'VE', VIE: 'VN'
  };

  function normalizedFlagCode(value) {
    var code = String(value || '').toLocaleLowerCase();
    return /^(?:[a-z]{2}|gb-(?:eng|nir|sct|wls))$/.test(code) ? code : '';
  }

  function flagAssetUrl(code) {
    var normalized = normalizedFlagCode(code);
    return normalized ? root.dataset.flagRoot.replace(/\/$/, '') + '/' + normalized + '.svg' : '';
  }

  function nationalTeamFlagCode(name) {
    var normalized = normalizedRegionName(name);
    var subdivisions = {
      england: 'gb-eng', 'northern ireland': 'gb-nir', scotland: 'gb-sct', wales: 'gb-wls'
    };
    return normalizedFlagCode(subdivisions[normalized] || buildRegionCodes()[normalized]);
  }

  function countryFlagCode(value) {
    var raw = String(value || '').trim();
    if (!raw) return '';
    var code = raw.toUpperCase();
    var subdivisions = { ENG: 'gb-eng', NIR: 'gb-nir', SCO: 'gb-sct', WLS: 'gb-wls' };
    if (subdivisions[code]) return subdivisions[code];
    if (/^[A-Z]{2}$/.test(code)) return normalizedFlagCode(code);
    return normalizedFlagCode(sportingCountryCodes[code] || buildRegionCodes()[normalizedRegionName(raw)]);
  }

  function inlineCountryFlag(row, sport) {
    if (!row || sport === 'national-football') return '';
    var code = countryFlagCode(row.country);
    var imageUrl = flagAssetUrl(code);
    if (!imageUrl) return '';
    var sourceLabel = 'Source country or federation: ' + String(row.country).toUpperCase();
    return '<span class="rating-lab-country-flag" role="img" aria-label="' + escapeHtml(sourceLabel) +
      '" title="' + escapeHtml(sourceLabel) + '"><img src="' + escapeHtml(imageUrl) +
      '" alt="" loading="lazy" decoding="async" data-flag-image></span>';
  }

  function entityName(row, sport) {
    return '<span class="rating-lab-entity-name"><span class="rating-lab-entity-name-text">' +
      escapeHtml(row.name) + '</span>' + inlineCountryFlag(row, sport) + '</span>';
  }

  function entityInitials(name) {
    var parts = String(name || '').replace(/,/g, ' ').trim().split(/\s+/).filter(Boolean);
    if (!parts.length) return '·';
    if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }

  function entityMedia(row, sport) {
    if (row && row.media) return row.media;
    var dataset = state.datasets[sport];
    if (!dataset || !row || !row.id) return null;
    if (!dataset.models.elo.rankings) {
      ensureRankings(sport, 'elo').then(scheduleRender, function () {});
      return null;
    }
    var match = dataset.models.elo.rankings.find(function (candidate) { return candidate.id === row.id; });
    return match ? match.media || null : null;
  }

  function trustedMediaUrl(value, purpose) {
    try {
      var parsed = new URL(String(value || ''), window.location.href);
      var allowed = purpose === 'image' ? ['crests.football-data.org', 'upload.wikimedia.org'] :
        ['www.football-data.org', 'football-data.org', 'commons.wikimedia.org'];
      return parsed.protocol === 'https:' && allowed.indexOf(parsed.hostname) !== -1 ? parsed.href : '';
    } catch (_error) {
      return '';
    }
  }

  function entityBadge(row, sport) {
    var flagCode = sport === 'national-football' ? nationalTeamFlagCode(row.name) : '';
    var flagUrl = flagAssetUrl(flagCode);
    var label = entityInitials(row.name);
    var media = entityMedia(row, sport);
    var imageUrl = media && trustedMediaUrl(media.url, 'image');
    if (imageUrl) {
      return '<span class="rating-lab-identity is-media is-' + escapeHtml(media.kind) + '" aria-hidden="true">' +
        '<span class="rating-lab-identity-fallback">' + escapeHtml(label) + '</span><img src="' +
        escapeHtml(imageUrl) + '" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" data-entity-image></span>';
    }
    if (flagUrl) {
      return '<span class="rating-lab-identity is-media is-flag" aria-hidden="true">' +
        '<span class="rating-lab-identity-fallback">' + escapeHtml(label) + '</span><img src="' +
        escapeHtml(flagUrl) + '" alt="" loading="lazy" decoding="async" data-flag-image></span>';
    }
    return '<span class="rating-lab-identity" aria-hidden="true">' + escapeHtml(label) + '</span>';
  }

  function entityTitle(row, sport) {
    return '<span class="rating-lab-entity-title">' + entityBadge(row, sport) + entityName(row, sport) + '</span>';
  }

  function mediaCredit(row, sport) {
    var media = entityMedia(row, sport);
    var sourceUrl = media && trustedMediaUrl(media.source_url, 'source');
    if (!media || !sourceUrl) return '';
    return '<details class="rating-lab-media-credit"><summary>Image credit</summary><p>' + (media.kind === 'crest' ? 'Crest' : 'Portrait') + ': <a href="' +
      escapeHtml(sourceUrl) + '" rel="noopener noreferrer">' + escapeHtml(media.attribution || media.source) +
      '</a> · ' + escapeHtml(media.license) + ' · not a model input</p></details>';
  }

  function filteredRows() {
    var rows = state.datasets[state.sport].models[state.model].rankings.slice();
    var query = state.query.trim().toLocaleLowerCase();
    return rows.filter(function (row) {
      return (!state.competition || row.competition === state.competition) &&
        (!query || row.name.toLocaleLowerCase().indexOf(query) !== -1 || row.country.toLocaleLowerCase().indexOf(query) !== -1);
    });
  }

  function provisionalCount() {
    return filteredRows().filter(function (row) { return Boolean(row.provisional); }).length;
  }

  function currentRows() {
    var rows = filteredRows();
    if (!state.includeProvisional) {
      rows = rows.filter(function (row) { return !row.provisional; });
    }
    rows.sort(function (a, b) {
      if (state.sport === 'football' && state.model === 'elo' && state.sort === 'score' &&
          Boolean(a.provisional) !== Boolean(b.provisional)) {
        return a.provisional ? 1 : -1;
      }
      var left = a[state.sort];
      var right = b[state.sort];
      if (left === null || left === undefined) return 1;
      if (right === null || right === undefined) return -1;
      if (typeof left === 'string') return left.localeCompare(right) * state.direction;
      return (left - right) * state.direction;
    });
    return rows;
  }

  function renderProvisionalControl() {
    var count = provisionalCount();
    elements.provisionalControl.hidden = count === 0;
    elements.includeProvisional.checked = state.includeProvisional;
    elements.provisionalCount.textContent = number(count, 0);
    var minimum = state.datasets[state.sport].eligibility.football_elo_established_matches || 10;
    elements.provisionalNote.textContent = count + ' entr' + (count === 1 ? 'y is' : 'ies are') +
      ' below the established football Elo gate: fewer than ' + minimum +
      ' matches against established opponents, or not yet connected to that result network.';
    syncMobileFilters();
  }

  function renderMetrics() {
    var models = state.datasets[state.sport].models;
    var selected = models[state.model].metrics;
    var definitions = [
      ['Brier score', 'brier', 4],
      ['Log loss', 'log_loss', 4],
      ['Calibration gap', 'calibration', 4]
    ];
    elements.metrics.innerHTML = definitions.map(function (definition) {
      var values = modelKeys.map(function (key) { return models[key].metrics[definition[1]]; });
      var bestIndex = values.indexOf(Math.min.apply(null, values));
      return '<div class="rating-lab-metric"><span>' + definition[0] + '</span><div class="rating-lab-metric-value"><strong>' +
        number(selected[definition[1]], definition[2], definition[2]) + '</strong></div><small>Lower is better · best: ' +
        escapeHtml(models[modelKeys[bestIndex]].label) + ' ' + number(values[bestIndex], definition[2], definition[2]) + '</small></div>';
    }).concat(['<div class="rating-lab-metric"><span>Held-out predictions</span><div class="rating-lab-metric-value"><strong>' +
      number(selected.predictions, 0) + '</strong></div><small>Scored before each result updates the model</small></div>']).join('');
    var hiddenProvisional = !state.includeProvisional ? provisionalCount() : 0;
    var provisionalNote = hiddenProvisional ? ' · ' + hiddenProvisional + ' provisional hidden' :
      (provisionalCount() ? ' · provisional included' : '');
    elements.context.textContent = models[state.model].label + ' · ' +
      (state.competition || 'all competitions') + ' · ' + currentRows().length + ' eligible competitors' + provisionalNote;
  }

  function renderMovers() {
    var rows = currentRows().filter(function (row) {
      return Number.isFinite(row.change30) && !row.provisional && Math.abs(row.change30) >= 0.05;
    });
    var risers = rows.filter(function (row) { return row.change30 >= 0.05; })
      .sort(function (a, b) { return b.change30 - a.change30; }).slice(0, 3);
    var fallers = rows.filter(function (row) { return row.change30 <= -0.05; })
      .sort(function (a, b) { return a.change30 - b.change30; }).slice(0, 3);
    function group(label, items, positive) {
      var content = items.length ? items.map(function (row) {
        var value = signedNumber(row.change30, 1);
        return '<button type="button" data-select="' + escapeHtml(row.id) + '">' + entityName(row, state.sport) +
          '<strong class="' + (positive ? 'is-positive' : 'is-negative') + '">' + value + '</strong></button>';
      }).join('') : '<span class="rating-lab-movers-empty">No material movement</span>';
      return '<div><p>' + label + '</p><div>' + content + '</div></div>';
    }
    elements.movers.innerHTML = group('▲ Biggest risers', risers, true) +
      group('▼ Biggest fallers', fallers, false);
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
    var mobile = window.matchMedia('(max-width: 650px)').matches;
    var pageSize = mobile ? 6 : 20;
    var visibleRows = Math.max(state.visibleRows, pageSize);
    var displayed = state.expanded ? rows : rows.slice(0, visibleRows);
    var model = state.datasets[state.sport].models[state.model];
    var hiddenProvisional = !state.includeProvisional ? provisionalCount() : 0;
    var provisionalCaption = hiddenProvisional ? ' · ' + hiddenProvisional + ' provisional hidden' :
      (provisionalCount() ? ' · provisional included' : '');
    elements.rankingTable.classList.toggle('has-uncertainty', state.model !== 'elo');
    elements.caption.textContent = model.label + ' · ' + rows.length + ' eligible · ' +
      (model.ranking_rule || 'Current model ranking rule') + provisionalCaption;
    elements.empty.hidden = rows.length > 0;
    elements.more.hidden = rows.length <= displayed.length;
    elements.more.textContent = mobile ? 'Show ' + number(Math.min(pageSize, rows.length - displayed.length), 0) +
      ' more · ' + number(rows.length - displayed.length, 0) + ' remaining' :
      'Show all ' + number(rows.length, 0) + ' competitors';
    elements.body.innerHTML = displayed.map(function (row) {
      var deltaClass = row.change30 > 0 ? 'is-positive' : row.change30 < 0 ? 'is-negative' : '';
      var delta = signedNumber(row.change30, 1);
      var rowClasses = [];
      if (row.id === state.selected) rowClasses.push('is-selected');
      if (row.provisional) rowClasses.push('is-provisional');
      var identityContext = row.provisional ? 'Provisional Elo · ' + row.provisional_reason :
        (row.competition || row.country);
      var movement = !Number.isFinite(row.change30) ? '• no 30d baseline' :
        Math.abs(row.change30) < 0.05 ? '• 0.0 · 30d' :
          (row.change30 > 0 ? '▲ ' : '▼ ') + delta + ' · 30d';
      var selected = row.id === state.selected;
      var quickDetail = selected ? '<tr class="rating-lab-mobile-row-expansion"><td colspan="7"><div class="rating-lab-mobile-row-insight">' +
        '<div><span>Recent trend</span>' + miniSparkline(row.history, row.name) + '</div><dl><div><dt>Uncertainty</dt><dd>' +
        (row.sigma === null ? 'Not published by Elo' : '±' + number(row.sigma, 1, 1)) + '</dd></div><div><dt>Recent matches</dt><dd>' +
        number(row.recent_matches, 0) + '</dd></div><div><dt>Last activity</dt><dd>' + escapeHtml(formatDate(row.last_played)) +
        '</dd></div></dl><button type="button" data-open-profile="' + escapeHtml(row.id) + '">Full rating history and model comparison ↓</button></div></td></tr>' : '';
      return '<tr data-id="' + escapeHtml(row.id) + '" data-row-select="' + escapeHtml(row.id) + '" aria-selected="' +
        (row.id === state.selected ? 'true' : 'false') + '"' +
        (rowClasses.length ? ' class="' + rowClasses.join(' ') + '"' : '') + '>' +
        '<td class="rating-lab-rank">' + row.rank + '</td>' +
        '<th scope="row"><button type="button" class="rating-lab-entity" data-select="' + escapeHtml(row.id) + '" aria-expanded="' + selected + '">' +
        entityBadge(row, state.sport) + '<span class="rating-lab-identity-copy">' + entityName(row, state.sport) +
        '<small' + (row.provisional ? ' class="rating-lab-provisional-label" title="' +
          escapeHtml(row.provisional_reason) + '"' : '') + '>' + escapeHtml(identityContext) + '</small>' +
        '<small class="rating-lab-mobile-change ' + deltaClass + '">' + escapeHtml(movement) + '</small></span><span class="rating-lab-mobile-row-chevron" aria-hidden="true">›</span></button></th>' +
        '<td class="rating-lab-trend-column">' + miniSparkline(row.history, row.name) + '</td>' +
        '<td class="rating-lab-rating-column"><strong>' + ratingNumber(row.score) + '</strong></td>' +
        '<td class="rating-lab-uncertainty-column' + (row.sigma === null ? ' is-empty' : '') + '">' + (row.sigma === null ? '—' : '±' + number(row.sigma, 1, 1)) + '</td>' +
        '<td class="rating-lab-change-column ' + deltaClass + '">' + delta + '</td>' +
        '<td class="rating-lab-recent-column">' + number(row.recent_matches, 0) + '</td>' +
        '</tr>' + quickDetail;
    }).join('');
    elements.rankingTable.querySelectorAll('thead th').forEach(function (header) {
      header.removeAttribute('aria-sort');
    });
    var activeSort = elements.rankingTable.querySelector('[data-sort="' + state.sort + '"]');
    if (activeSort) activeSort.closest('th').setAttribute('aria-sort', state.direction === 1 ? 'ascending' : 'descending');
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
      var area = 'M' + coordinates.join(' L') + ' L' + coordinates[coordinates.length - 1].split(',')[0] +
        ',' + (height - bottom) + ' L' + coordinates[0].split(',')[0] + ',' + (height - bottom) + ' Z';
      var points = item.points.map(function (point) {
        return '<circle class="rating-lab-chart-hit" cx="' + x(point[0]).toFixed(1) + '" cy="' + y(point[1]).toFixed(1) +
          '" r="3" data-chart-point data-series-index="' + seriesIndex + '" data-series="' + escapeHtml(item.name) + '" data-date="' + escapeHtml(point[0]) +
          '" data-value="' + point[1] + '"><title>' + escapeHtml(item.name) + ' · ' + escapeHtml(formatDate(point[0])) +
          ' · ' + number(point[1], 1) + '</title></circle>';
      }).join('');
      var last = item.points[item.points.length - 1];
      return (usable.length === 1 ? '<path class="rating-lab-chart-area" d="' + area + '"></path>' : '') +
        '<polyline class="rating-lab-series-' + (seriesIndex + 1) + '" points="' + coordinates.join(' ') +
        '"></polyline>' + points + '<circle class="rating-lab-chart-endpoint rating-lab-series-' + (seriesIndex + 1) +
        '" cx="' + x(last[0]).toFixed(1) + '" cy="' + y(last[1]).toFixed(1) + '" r="3.5"></circle>';
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
    return '<div class="rating-lab-chart-wrap"><div class="rating-lab-chart-stage"><svg class="rating-lab-chart" viewBox="0 0 ' + width + ' ' + height +
      '" role="img" aria-label="' + escapeHtml(label) + ' with labelled date and rating axes">' + grid + paths + axis +
      '<line class="rating-lab-crosshair" x1="0" y1="' + top + '" x2="0" y2="' + (height - bottom) + '"></line>' +
      '<rect class="rating-lab-chart-surface" x="' + left + '" y="' + top + '" width="' + (width - left - right) +
      '" height="' + (height - top - bottom) + '" tabindex="0" data-chart-surface aria-label="Inspect ' +
      escapeHtml(label) + '. Move across the chart, tap, or use the left and right arrow keys."></rect></svg>' +
      '<div class="rating-lab-chart-tooltip" role="presentation" hidden></div></div>' +
      '<p class="rating-lab-chart-readout" aria-live="polite"><span class="rating-lab-chart-readout-pointer">Move across the chart, tap, or use ← → to inspect each update.</span>' +
      '<span class="rating-lab-chart-readout-touch">Tap the chart to inspect each update.</span></p>' + legend + '</div>';
  }

  function chartEntries(chartWrap) {
    return Array.prototype.map.call(chartWrap.querySelectorAll('[data-chart-point]'), function (point) {
      return {
        element: point,
        x: Number(point.getAttribute('cx')),
        y: Number(point.getAttribute('cy')),
        date: point.dataset.date,
        series: point.dataset.series,
        seriesIndex: Number(point.dataset.seriesIndex),
        value: Number(point.dataset.value)
      };
    });
  }

  function selectChartX(chartWrap, requestedX, explicitDate) {
    var entries = chartEntries(chartWrap);
    if (!entries.length) return;
    var minimumX = Math.min.apply(null, entries.map(function (entry) { return entry.x; }));
    var maximumX = Math.max.apply(null, entries.map(function (entry) { return entry.x; }));
    var x = Math.max(minimumX, Math.min(maximumX, requestedX));
    var series = entries.reduce(function (groups, entry) {
      if (!groups[entry.seriesIndex]) groups[entry.seriesIndex] = [];
      groups[entry.seriesIndex].push(entry);
      return groups;
    }, {});
    var selected = Object.keys(series).map(function (key) {
      return series[key].reduce(function (best, entry) {
        return !best || Math.abs(entry.x - x) < Math.abs(best.x - x) ? entry : best;
      }, null);
    });
    entries.forEach(function (entry) {
      var active = selected.some(function (candidate) { return candidate.element === entry.element; });
      entry.element.classList.toggle('is-active', active);
      entry.element.setAttribute('r', active ? '5' : '3');
    });
    var crosshairX = selected.length > 1 ? x : selected[0].x;
    var crosshair = chartWrap.querySelector('.rating-lab-crosshair');
    crosshair.setAttribute('x1', crosshairX);
    crosshair.setAttribute('x2', crosshairX);
    crosshair.classList.add('is-visible');
    var minimumTime = Math.min.apply(null, entries.map(function (entry) { return new Date(entry.date).getTime(); }));
    var maximumTime = Math.max.apply(null, entries.map(function (entry) { return new Date(entry.date).getTime(); }));
    var date = explicitDate || new Date(minimumTime + (x - minimumX) / (maximumX - minimumX || 1) *
      (maximumTime - minimumTime)).toISOString().slice(0, 10);
    var detail = formatDate(date) + ' · ' + selected.map(function (entry) {
      return entry.series + ' ' + number(entry.value, 1);
    }).join(' · ');
    chartWrap.querySelector('.rating-lab-chart-readout').textContent = detail;
    var surface = chartWrap.querySelector('[data-chart-surface]');
    surface.dataset.activeDate = date;
    surface.setAttribute('aria-valuetext', detail);
    var tooltip = chartWrap.querySelector('.rating-lab-chart-tooltip');
    tooltip.textContent = detail;
    tooltip.hidden = false;
    tooltip.style.setProperty('--chart-x', (crosshairX / 380 * 100).toFixed(2) + '%');
  }

  function selectChartDate(chartWrap, date) {
    var entries = chartEntries(chartWrap);
    if (!entries.length) return;
    var minimumX = Math.min.apply(null, entries.map(function (entry) { return entry.x; }));
    var maximumX = Math.max.apply(null, entries.map(function (entry) { return entry.x; }));
    var minimumTime = Math.min.apply(null, entries.map(function (entry) { return new Date(entry.date).getTime(); }));
    var maximumTime = Math.max.apply(null, entries.map(function (entry) { return new Date(entry.date).getTime(); }));
    var time = new Date(date).getTime();
    selectChartX(chartWrap, minimumX + (time - minimumTime) / (maximumTime - minimumTime || 1) * (maximumX - minimumX), date);
  }

  function scrubChart(event) {
    var surface = event.target.closest('[data-chart-surface]');
    if (!surface) return;
    var chartWrap = surface.closest('.rating-lab-chart-wrap');
    var svg = surface.closest('svg');
    var bounds = svg.getBoundingClientRect();
    var viewBox = svg.viewBox.baseVal;
    var pointerX = viewBox.x + (event.clientX - bounds.left) / bounds.width * viewBox.width;
    selectChartX(chartWrap, pointerX);
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
    elements.detail.hidden = !row;
    elements.detail.closest('.rating-lab-grid').classList.toggle('has-detail', Boolean(row));
    if (!row) {
      elements.detail.innerHTML = '';
      return;
    }
    if (modelKeys.some(function (key) { return !dataset.models[key].rankings; })) {
      ensureModels(state.sport).then(scheduleRender, function () {});
    }
    var crossModel = modelKeys.map(function (key) {
      var loadedRankings = dataset.models[key].rankings;
      var modelRow = loadedRankings ? loadedRankings.find(function (candidate) { return candidate.id === row.id; }) : null;
      var placeholder = loadedRankings ? '—' : '…';
      return '<tr><th scope="row">' + escapeHtml(dataset.models[key].label) + '</th><td>' +
        (modelRow ? '#' + modelRow.rank + (modelRow.provisional ? ' · provisional' : '') : placeholder) +
        '</td><td>' + (modelRow ? number(modelRow.score, 1) : placeholder) +
        '</td><td>' + (modelRow && modelRow.sigma !== null ? '±' + number(modelRow.sigma, 1) : placeholder) + '</td></tr>';
    }).join('');
    var isPinned = state.pinned.indexOf(row.id) !== -1;
    var pinnedRows = state.pinned.map(function (id) {
      return rows.find(function (candidate) { return candidate.id === id; });
    }).filter(Boolean);
    var compare = '';
    if (pinnedRows.length) {
      compare = '<div class="rating-lab-compare"><div class="rating-lab-compare-heading"><p class="rating-lab-inspector-label">Pinned comparison</p><div>' +
        pinnedRows.map(function (item) { return '<button type="button" data-unpin="' + escapeHtml(item.id) + '">' +
          entityBadge(item, state.sport) + '<span>' + escapeHtml(item.name) + ' ×</span></button>'; }).join('') + '</div></div>' +
        (pinnedRows.length === 2 ? historyChart(pinnedRows.map(function (item) { return { name: item.name, points: item.history }; }),
          pinnedRows[0].name + ' and ' + pinnedRows[1].name + ' rating comparison') :
          '<p class="rating-lab-detail-placeholder">Pin one more competitor to overlay both histories.</p>') + '</div>';
    }
    var provisional = row.provisional ? '<p class="rating-lab-provisional-note"><strong>Provisional Elo.</strong> ' +
      escapeHtml(row.provisional_reason) + '. The raw rating remains available for A-vs-B and competition forecasts, but it is ordered after established clubs because Elo has no uncertainty estimate.</p>' : '';
    elements.detail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">Rank ' + row.rank +
      '</p><h3>' + entityTitle(row, state.sport) + '</h3></div><strong>' + ratingNumber(row.score) + '</strong></div>' +
      provisional +
      '<button type="button" class="rating-lab-pin" data-pin="' + escapeHtml(row.id) + '" aria-pressed="' +
      (isPinned ? 'true' : 'false') + '">' + (isPinned ? 'Pinned for comparison' : 'Pin for comparison') + '</button>' +
      historyChart([{ name: row.name, points: row.history }], row.name + ' rating history') +
      '<p class="rating-lab-inspector-label">Across all four models</p><table class="rating-lab-model-compare"><thead><tr><th>Model</th><th>Rank</th><th>Score</th><th>Uncertainty</th></tr></thead><tbody>' +
      crossModel + '</tbody></table>' + distribution(row, rows) +
      '<dl><div><dt>Last played</dt><dd>' + formatDate(row.last_played) + '</dd></div><div><dt>Recent matches</dt><dd>' + row.recent_matches + '</dd></div><div><dt>All matches</dt><dd>' + row.matches + '</dd></div>' +
      (row.sigma === null ? '' : '<div><dt>Uncertainty σ</dt><dd>' + number(row.sigma, 2) + '</dd></div>') + '</dl>' + compare +
      mediaCredit(row, state.sport);
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
    var modelNames = modelKeys;
    elements.eligibility.textContent = data.eligibility.rule + ' “Recent” covers ' +
      number(data.eligibility.recent_window_days, 0) + ' days for this cohort.';
    elements.parameterBody.innerHTML = modelNames.map(function (model) {
      var candidates = data.candidate_parameters[model].map(parameterText).join(' · ');
      return '<tr><th scope="row">' + escapeHtml(data.models[model].label) + '</th>' +
        '<td data-label="Selected values"><code>' + escapeHtml(parameterText(data.parameters[model])) + '</code></td>' +
        '<td data-label="Candidates tested"><code>' + escapeHtml(candidates) + '</code></td></tr>';
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
        input: 'Completed tour-level singles results. Player identity uses the source player code; tournament start date is the available chronological date. Surface is normalized to hard, clay, grass, carpet, or unknown.',
        venue: 'Each prediction blends the global belief with the selected surface belief; the surface weight grows with surface evidence. Draws are not valid tennis outcomes.',
        initialization: 'Every player starts at Elo/Glicko-2 rating 1500 (Glicko-2 RD 350, volatility 0.06) or Gaussian μ=25, σ=8.333.',
        special: 'Every result updates both the global model and its surface-specific model. No seasonal regression.'
      },
      football: {
        label: 'European club football',
        input: 'Full-time results from the five covered domestic leagues and Champions League. Club identity uses the source ID, with normalized names only for the documented OpenFootball fallback.',
        venue: 'The listed home team receives the selected home advantage. A draw is y=0.5.',
        initialization: 'Every club starts at Elo/Glicko-2 rating 1500 (Glicko-2 RD 350, volatility 0.06) or Gaussian μ=25, σ=8.333.',
        special: 'Only club Elo regresses 25% toward 1500 when the season label changes. Because Elo has no uncertainty term, clubs with fewer than 10 covered results or outside the main connected result network remain in a disclosed provisional tier after established clubs. Forecasts retain them.'
      },
      'national-football': {
        label: "Men's national teams",
        input: 'Completed men’s full internationals since 2016. Country identity is a normalized team name from the CC0 source.',
        venue: 'Home advantage applies only when the source does not mark the match neutral. A draw is y=0.5.',
        initialization: 'Every national team starts at Elo/Glicko-2 rating 1500 (Glicko-2 RD 350, volatility 0.06) or Gaussian μ=25, σ=8.333.',
        special: 'No seasonal regression; all recorded tournament and friendly results receive the same update weight.'
      },
      chess: {
        label: 'Elite over-the-board chess',
        input: 'Decisive games and draws from official Lichess broadcast PGNs. Both players must have numeric FIDE IDs; online games and engine identities are excluded.',
        venue: 'White receives the selected color advantage. A draw is y=0.5.',
        initialization: 'At first appearance, Elo and Glicko-2 use the PGN FIDE rating when it is at least 1000 (Glicko-2 RD 100). Gaussian μ=25+(FIDE−2000)/80 with σ=3; otherwise the generic prior is retained.',
        special: 'All valid FIDE-identified broadcast games update ratings; the 2200 official-rating threshold applies to publication eligibility.'
      }
    };
    return rules[sport];
  }

  function protocolModelRules(model, parameters, sport) {
    if (model === 'elo') {
      return {
        prediction: 'Compute expected score p = 1 / (1 + 10^−((Rₐ + advantage − Rᵦ) / scale)).',
        update: 'After recording p, update both sides symmetrically: R′ₐ = Rₐ + K(y−p) and R′ᵦ = Rᵦ − K(y−p).',
        publication: sport === 'football' ?
          'Publish the raw Elo rating. Rank clubs with at least 10 covered results in the main connected result network first; retain all other current entrants in a provisional tier. This prevents an isolated two-team rating component from being presented as comparable with the established network.' :
          'Publish and rank the raw Elo rating. Elo has no uncertainty estimate.',
        constants: 'Initial rating 1500. Selected K=' + number(parameters.k, 4) + ', scale=' + number(parameters.scale, 4) + ', advantage=' + number(parameters.home, 4) + '.'
      };
    }
    if (model === 'glicko2') {
      return {
        prediction: 'Compute the official Glicko-2 expected score after damping the rating gap by the opponent’s rating deviation; apply the declared home/White offset when relevant.',
        update: 'Batch every calendar date as one simultaneous rating period. Inflate RD for elapsed seven-day periods, solve the published iterative volatility equation, then update rating and RD from all results in that date.',
        publication: 'Publish rating, RD, and volatility; rank by the conservative score rating−2×RD, approximately the lower end of the documented 95% interval.',
        constants: 'Initial rating=' + number(parameters.initial_rating, 1) + ', RD=' + number(parameters.initial_rd, 1) +
          ', volatility=' + number(parameters.initial_volatility, 4) + ', selected τ=' + number(parameters.tau, 4) +
          ', period scale=' + number(parameters.period_days, 1) + ' days, advantage=' + number(parameters.home, 2) + '.'
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
      home: 'Rating points added only when the home/White advantage flag is true',
      surface_weight: 'Maximum weight assigned to the independently replayed tennis-surface belief; actual weight grows from zero over the first 20 combined surface matches',
      tau: 'Glicko-2 constraint on how quickly volatility may change',
      initial_rating: 'Glicko-2 initial rating',
      initial_rd: 'Glicko-2 initial rating deviation',
      initial_volatility: 'Glicko-2 initial volatility',
      period_days: 'Calendar days represented by one inactivity period',
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
    var modelRules = protocolModelRules(state.model, parameters, state.sport);
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

  function predictorCompetitions() {
    var rows = ['tennis', 'football', 'national-football', 'chess'].reduce(function (items, sport) {
      var predictor = state.datasets[sport].tournament_predictor;
      if (!predictor) return items;
      predictor.competitions.forEach(function (competition) {
        items.push({ sport: sport, predictor: predictor, competition: competition });
      });
      return items;
    }, []);
    var priority = { live: 0, upcoming: 1, finished: 2 };
    return rows.sort(function (a, b) {
      var stateA = competitionState(a.competition);
      var stateB = competitionState(b.competition);
      var priorityA = Object.prototype.hasOwnProperty.call(priority, stateA) ? priority[stateA] : 9;
      var priorityB = Object.prototype.hasOwnProperty.call(priority, stateB) ? priority[stateB] : 9;
      return priorityA - priorityB ||
        a.competition.label.localeCompare(b.competition.label);
    });
  }

  function predictorData() {
    var view = predictorCompetitions().find(function (item) {
      return item.competition.id === state.predictorCompetition;
    });
    if (!view) return null;
    view.model = view.competition.models[state.predictorModel] || null;
    return view;
  }

  function probabilityCell(value) {
    return '<span class="rating-lab-probability" style="--probability:' +
      (value * 100).toFixed(1) + '%"><span>' + percent(value) + '</span></span>';
  }

  function noEligibleMarketCard(provider, reason, unavailable) {
    var heading = unavailable ? 'Market check unavailable' : 'No eligible market found';
    return '<section class="rating-lab-market-provider is-empty"><div class="rating-lab-market-heading"><div>' +
      '<p class="rating-lab-kicker">External benchmark · ' + escapeHtml(provider.name) + '</p><h3>' +
      escapeHtml(heading) + '</h3></div></div><p>' + escapeHtml(reason) +
      ' Our forecast remains independent; no market is guessed or attached by title alone.</p></section>';
  }

  function resolvedMarketProviderCard(view, provider) {
    var benchmark = provider.data;
    if (!benchmark) {
      return noEligibleMarketCard(
        provider,
        'No dated snapshot is present in this older dataset.',
        false
      );
    }
    var competitionHistory = (benchmark.history || []).filter(function (entry) {
      return entry.competition_id === view.competition.id;
    });
    if (!competitionHistory.length) {
      var search = (benchmark.searches || []).find(function (item) {
        return item.competition_id === view.competition.id;
      });
      return noEligibleMarketCard(
        provider,
        search && search.status === 'source_error' ?
          'The provider could not be checked while this competition was forecastable.' :
          'No eligible winner market passed the season, identity, and participant-coverage checks while this competition was forecastable.',
        Boolean(search && search.status === 'source_error')
      );
    }
    var resolved = competitionHistory.filter(function (entry) {
      return entry.resolution && entry.resolution.scores && entry.resolution.scores.market;
    });
    if (!resolved.length) {
      return '<section class="rating-lab-market-provider"><div class="rating-lab-market-heading"><div>' +
        '<p class="rating-lab-kicker">Resolved benchmark · ' + escapeHtml(provider.name) + '</p>' +
        '<h3>Snapshot retained, score unavailable</h3></div></div><p>' +
        'A dated market quote exists, but this historical frame does not contain a simultaneous model forecast on the same participant field. It is retained for provenance and is not backfilled.</p></section>';
    }
    var order = ['market', 'elo', 'glicko2', 'trueskill', 'robust'];
    var labels = {
      market: provider.name,
      elo: 'Elo',
      glicko2: 'Glicko-2',
      trueskill: 'Gaussian',
      robust: 'Robust'
    };
    var scoreRows = order.map(function (forecaster) {
      var observations = resolved.map(function (entry) {
        return entry.resolution.scores[forecaster];
      }).filter(Boolean);
      if (!observations.length) return null;
      return {
        id: forecaster,
        label: labels[forecaster],
        predictions: observations.length,
        logLoss: observations.reduce(function (sum, score) { return sum + score.log_loss; }, 0) / observations.length,
        brier: observations.reduce(function (sum, score) { return sum + score.brier; }, 0) / observations.length
      };
    }).filter(Boolean);
    var winner = resolved[0].resolution.winner_name;
    var first = resolved[0].captured_at;
    var last = resolved[resolved.length - 1].captured_at;
    var latest = resolved[resolved.length - 1];
    return '<section class="rating-lab-market-provider is-resolved"><div class="rating-lab-market-heading"><div>' +
      '<p class="rating-lab-kicker">Resolved benchmark</p><h3>' + escapeHtml(provider.name) +
      ' vs all four protocols</h3></div>' + (latest.event_url ? '<a href="' +
      escapeHtml(latest.event_url) + '" target="_blank" rel="noopener">Open market ↗</a>' : '') +
      '</div><div class="rating-lab-market-metrics"><div><span>Official winner</span><strong>' +
      escapeHtml(winner) + '</strong></div><div><span>Dated snapshots</span><strong>' +
      number(resolved.length, 0) + '</strong></div><div><span>Scoring window</span><strong>' +
      escapeHtml(formatDate(first)) + '–' + escapeHtml(formatDate(last)) +
      '</strong></div></div><div class="rating-lab-market-table-wrap"><table class="rating-lab-market-score-table">' +
      '<caption>Resolved winner forecast scores · lower is better</caption><thead><tr><th scope="col">Forecaster</th>' +
      '<th scope="col">Snapshots</th><th scope="col">Log loss</th><th scope="col">Brier</th></tr></thead><tbody>' +
      scoreRows.map(function (row) {
        return '<tr' + (row.id === 'market' ? ' class="is-market"' : '') + '><th scope="row">' +
          escapeHtml(row.label) + '</th><td>' + number(row.predictions, 0) + '</td><td>' +
          number(row.logLoss, 4) + '</td><td>' + number(row.brier, 4) + '</td></tr>';
      }).join('') + '</tbody></table></div><details class="rating-lab-market-detail"><summary>Scoring protocol and audit trail</summary>' +
      '<p class="rating-lab-market-note">' + escapeHtml(benchmark.benchmark && benchmark.benchmark.method ?
        benchmark.benchmark.method :
        'Every dated market and model forecast is frozen before the winner is known, then scored without revision.') +
      ' The public JSON retains every captured probability, source hash, winner, and per-snapshot score. Market quotes never enter a rating or simulation.</p></details></section>';
  }

  function marketProviderCard(view, modelRows, provider, options) {
    var benchmark = provider.data;
    if (options && options.resolved) {
      return resolvedMarketProviderCard(view, provider);
    }
    if (!benchmark) {
      return noEligibleMarketCard(
        provider,
        'This dataset predates the provider integration. The next refresh will check its public markets.',
        false
      );
    }
    var snapshot = (benchmark.competitions || []).find(function (item) {
      return item.competition_id === view.competition.id;
    });
    if (!snapshot) {
      var search = (benchmark.searches || []).find(function (item) {
        return item.competition_id === view.competition.id;
      });
      var reason = search && search.status === 'source_error' ?
        'The market source could not be checked.' :
        search ? 'No active event passed the season, participant-coverage, and identity checks.' :
          'This provider has no configured winner series for the selected competition.';
      return noEligibleMarketCard(
        provider,
        reason,
        Boolean(search && search.status === 'source_error')
      );
    }
    var rowsById = {};
    (modelRows || []).forEach(function (row) { rowsById[row.id] = row; });
    var comparisons = snapshot.outcomes.reduce(function (items, outcome) {
      var modelRow = rowsById[outcome.entity_id];
      if (!modelRow || !Number.isFinite(modelRow.champion)) return items;
      items.push({
        name: outcome.name,
        model: modelRow.champion,
        market: outcome.normalized_probability,
        gap: modelRow.champion - outcome.normalized_probability,
        bid: outcome.best_bid,
        ask: outcome.best_ask,
        liquidity: outcome.liquidity_usd,
        raw: outcome.raw_yes_price
      });
      return items;
    }, []);
    comparisons.sort(function (a, b) { return Math.abs(b.gap) - Math.abs(a.gap) || a.name.localeCompare(b.name); });
    var meanGap = comparisons.length ? comparisons.reduce(function (sum, row) {
      return sum + Math.abs(row.gap);
    }, 0) / comparisons.length : null;
    var retained = benchmark.status !== 'current' || isStale(benchmark);
    var freshness = retained ? ' · retained or delayed snapshot' : '';
    var suppressComparison = Boolean(options && options.withheld);
    var datedSnapshots = (benchmark.history || []).filter(function (entry) {
      return entry.competition_id === view.competition.id;
    }).length;
    var tableHead = suppressComparison ?
      '<tr><th scope="col">Participant</th><th scope="col">Market</th><th scope="col" class="rating-lab-market-raw">Raw quote</th><th scope="col" class="rating-lab-market-spread">Bid–ask</th></tr>' :
      '<tr><th scope="col">Participant</th><th scope="col">Our model</th><th scope="col">Market</th><th scope="col">Gap</th><th scope="col" class="rating-lab-market-raw">Raw quote</th><th scope="col" class="rating-lab-market-spread">Bid–ask</th></tr>';
    var table = comparisons.length ? '<div class="rating-lab-market-table-wrap"><table><caption>' +
      (suppressComparison ? provider.name + ' normalized winner field' : 'Largest model–market differences first') +
      '</caption><thead>' + tableHead + '</thead><tbody>' +
      comparisons.map(function (row) {
        var gapClass = row.gap > 0 ? 'is-positive' : row.gap < 0 ? 'is-negative' : '';
        var gap = signedNumber(row.gap * 100, 1) + ' pp';
        var spread = row.bid >= 0 && row.ask > 0 ? number(row.bid * 100, 1) + '–' + number(row.ask * 100, 1) + '%' : '—';
        var modelCells = suppressComparison ? '' : '<td>' + percent(row.model) + '</td>';
        var gapCell = suppressComparison ? '' : '<td class="' + gapClass + '">' + escapeHtml(gap) + '</td>';
        return '<tr><th scope="row">' + escapeHtml(row.name) + '</th>' + modelCells + '<td>' +
          percent(row.market) + '</td>' + gapCell + '<td class="rating-lab-market-raw">' +
          percent(row.raw) + '</td><td class="rating-lab-market-spread">' + escapeHtml(spread) + '</td></tr>';
      }).join('') + '</tbody></table></div>' :
      '<p><strong>A market was matched, but no participant IDs overlap this model output.</strong> The comparison is withheld.</p>';
    var comparisonMetric = suppressComparison ? '<span>Model comparison</span><strong>After kickoff</strong>' :
      '<span>Mean absolute gap</span><strong>' + (meanGap === null ? '—' : number(meanGap * 100, 1) + ' pp') + '</strong>';
    return '<section class="rating-lab-market-provider' + (retained ? ' is-stale' : '') + '">' +
      '<div class="rating-lab-market-heading"><div><p class="rating-lab-kicker">External benchmark</p><h3>' +
      (suppressComparison ? escapeHtml(provider.name) + ' winner market' : 'Our protocol vs ' + escapeHtml(provider.name)) + '</h3></div><a href="' +
      escapeHtml(snapshot.event_url) + '" target="_blank" rel="noopener">Open market ↗</a></div><div class="rating-lab-market-metrics"><div><span>Field coverage</span><strong>' +
      snapshot.matched_participants + ' / ' + snapshot.model_participants + '</strong></div><div><span>Raw Yes total</span><strong>' +
      number(snapshot.raw_yes_price_sum * 100, 1) + '%</strong></div><div>' + comparisonMetric +
      '</div></div><p class="rating-lab-market-benchmark-state"><strong>Benchmark clock:</strong> ' +
      number(datedSnapshots, 0) + ' dated snapshot' + (datedSnapshots === 1 ? '' : 's') +
      ' frozen; log loss and Brier score unlock after the official winner is known.</p>' +
      '<details class="rating-lab-market-detail"><summary>Participant quotes and normalization</summary><p class="rating-lab-market-note">Snapshot ' +
      escapeHtml(benchmark.fetched_at ? formatDate(benchmark.fetched_at) : 'unavailable') + freshness + '. ' +
      number(datedSnapshots, 0) + ' dated snapshot' + (datedSnapshots === 1 ? '' : 's') + ' retained. ' +
      escapeHtml(snapshot.normalization || benchmark.probability_definition) +
      ' The raw total and quote remain visible. Positive gap means our selected protocol gives a higher title probability. Once the competition resolves, this frozen quote and the simultaneous forecasts from all four protocols receive log-loss and Brier scores. Market prices are an external benchmark only—never a rating or simulation input.</p>' + table + '</details></section>';
  }

  function renderMarketComparison(view, modelRows, options) {
    elements.predictorMarket.hidden = false;
    var providers = [
      { name: 'Polymarket', data: view.predictor.market_comparison },
      { name: 'Kalshi', data: view.predictor.kalshi_comparison }
    ];
    elements.predictorMarket.classList.toggle('is-stale', providers.some(function (provider) {
      return provider.data && (provider.data.status !== 'current' || isStale(provider.data));
    }));
    var withheldBanner = options && options.withheld ?
      '<p class="rating-lab-market-withheld"><strong>Market gap withheld before play.</strong> ' +
      escapeHtml(options.withheld) + ' Venue quotes remain visible, but model–market gaps are not presented as in-season evidence yet.</p>' : '';
    elements.predictorMarket.innerHTML = withheldBanner + providers.map(function (provider) {
      return marketProviderCard(view, modelRows, provider, options);
    }).join('');
  }

  function errorFunction(value) {
    var sign = value < 0 ? -1 : 1;
    var x = Math.abs(value);
    var t = 1 / (1 + 0.3275911 * x);
    var approximation = 1 - (((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t -
      0.284496736) * t + 0.254829592) * t * Math.exp(-x * x));
    return sign * approximation;
  }

  function normalCdf(value) {
    return 0.5 * (1 + errorFunction(value / Math.sqrt(2)));
  }

  function performanceCdf(value, robust) {
    return robust ? 0.5 + Math.atan(value) / Math.PI : normalCdf(value);
  }

  function bayesianLikelihood(difference, score, parameters, robust) {
    var cdf = function (value) { return performanceCdf(value, robust); };
    if (score === 0.5) {
      return Math.max(cdf((parameters.draw_margin - difference) / parameters.beta) -
        cdf((-parameters.draw_margin - difference) / parameters.beta), 1e-12);
    }
    var signed = score === 1 ? difference : -difference;
    return Math.max(cdf((signed - parameters.draw_margin) / parameters.beta), 1e-12);
  }

  function beliefOutcomes(rowA, rowB, dataset, advantage) {
    var parameters = dataset.parameters[state.model];
    var meanDifference = rowA.rating - rowB.rating + advantage;
    if (state.model === 'elo' || state.model === 'glicko2') {
      var expected;
      if (state.model === 'elo') {
        expected = 1 / (1 + Math.pow(10, -meanDifference / parameters.scale));
      } else {
        var opponentPhi = rowB.sigma / 173.7178;
        var glickoDamping = 1 / Math.sqrt(1 + 3 * opponentPhi * opponentPhi / (Math.PI * Math.PI));
        expected = 1 / (1 + Math.exp(-glickoDamping * meanDifference / 173.7178));
      }
      var context = dataset.outcome_context || {};
      var empiricalDrawRate = Number.isFinite(context.draw_rate) ? context.draw_rate : state.sport === 'tennis' ? 0 : 0.25;
      var draw = Math.min(empiricalDrawRate * 4 * expected * (1 - expected), 2 * Math.min(expected, 1 - expected));
      return {
        win: expected - 0.5 * draw,
        draw: draw,
        loss: 1 - expected - 0.5 * draw,
        expected: expected,
        difference: meanDifference,
        empiricalDrawRate: empiricalDrawRate,
        parameters: parameters
      };
    }
    var variance = rowA.sigma * rowA.sigma + rowB.sigma * rowB.sigma;
    var totals = [0, 0, 0];
    ghNodes.forEach(function (node, index) {
      var difference = meanDifference + Math.sqrt(2 * variance) * node;
      totals[0] += ghWeights[index] * bayesianLikelihood(difference, 1, parameters, state.model === 'robust');
      totals[1] += ghWeights[index] * bayesianLikelihood(difference, 0.5, parameters, state.model === 'robust');
      totals[2] += ghWeights[index] * bayesianLikelihood(difference, 0, parameters, state.model === 'robust');
    });
    var total = Math.max((totals[0] + totals[1] + totals[2]) / Math.sqrt(Math.PI), 1e-12);
    return {
      win: totals[0] / Math.sqrt(Math.PI) / total,
      draw: totals[1] / Math.sqrt(Math.PI) / total,
      loss: totals[2] / Math.sqrt(Math.PI) / total,
      expected: (totals[0] + 0.5 * totals[1]) / Math.sqrt(Math.PI) / total,
      difference: meanDifference,
      variance: variance,
      parameters: parameters
    };
  }

  function matchupOutcomes(rowA, rowB, dataset) {
    var parameters = dataset.parameters[state.model];
    if (state.sport === 'tennis') {
      var surface = state.matchupVenue;
      var contextA = rowA.contexts && rowA.contexts[surface];
      var contextB = rowB.contexts && rowB.contexts[surface];
      var globalOutcome = beliefOutcomes(rowA, rowB, dataset, 0);
      if (!contextA || !contextB) {
        globalOutcome.surface = surface;
        globalOutcome.surfaceWeight = 0;
        globalOutcome.globalExpected = globalOutcome.expected;
        globalOutcome.surfaceExpected = null;
        return globalOutcome;
      }
      var surfaceOutcome = beliefOutcomes(contextA, contextB, dataset, 0);
      var evidence = Math.min((contextA.matches + contextB.matches) / 20, 1);
      var weight = parameters.surface_weight * evidence;
      return {
        win: (1 - weight) * globalOutcome.win + weight * surfaceOutcome.win,
        draw: (1 - weight) * globalOutcome.draw + weight * surfaceOutcome.draw,
        loss: (1 - weight) * globalOutcome.loss + weight * surfaceOutcome.loss,
        expected: (1 - weight) * globalOutcome.expected + weight * surfaceOutcome.expected,
        difference: (1 - weight) * globalOutcome.difference + weight * surfaceOutcome.difference,
        variance: Number.isFinite(globalOutcome.variance) && Number.isFinite(surfaceOutcome.variance) ?
          (1 - weight) * globalOutcome.variance + weight * surfaceOutcome.variance : null,
        empiricalDrawRate: globalOutcome.empiricalDrawRate,
        parameters: parameters,
        surface: surface,
        surfaceWeight: weight,
        globalExpected: globalOutcome.expected,
        surfaceExpected: surfaceOutcome.expected,
        contextA: contextA,
        contextB: contextB
      };
    }
    var advantageDirection = state.matchupVenue === 'a' ? 1 : state.matchupVenue === 'b' ? -1 : 0;
    var advantage = advantageDirection * (state.model === 'elo' || state.model === 'glicko2' ? parameters.home : parameters.advantage);
    return beliefOutcomes(rowA, rowB, dataset, advantage);
  }

  function matchupVenueOptions(rowA, rowB) {
    var nameA = rowA ? rowA.name : 'Competitor A';
    var nameB = rowB ? rowB.name : 'Competitor B';
    if (state.sport === 'tennis') {
      var contexts = state.datasets.tennis.prediction_contexts;
      return contexts.values.map(function (surface) {
        return { value: surface.id, label: surface.label + ' court' };
      });
    }
    if (state.sport === 'chess') return [
      { value: 'a', label: nameA + ' plays White' },
      { value: 'b', label: nameB + ' plays White' },
      { value: 'neutral', label: 'White not assigned · neutral assumption' }
    ];
    return [
      { value: 'a', label: nameA + ' at home' },
      { value: 'neutral', label: 'Neutral venue' },
      { value: 'b', label: nameB + ' at home' }
    ];
  }

  function populateMatchupControls() {
    var rows = state.datasets[state.sport].models[state.model].rankings;
    if (!rows.some(function (row) { return row.id === state.matchupA; })) state.matchupA = rows[0] ? rows[0].id : null;
    if (!rows.some(function (row) { return row.id === state.matchupB; }) || state.matchupB === state.matchupA) {
      state.matchupB = rows.find(function (row) { return row.id !== state.matchupA; });
      state.matchupB = state.matchupB ? state.matchupB.id : null;
    }
    function optionsFor(selectedId) {
      return rows.map(function (row) {
      var sourceCode = state.sport === 'national-football' ? '' : String(row.country || '').trim().toUpperCase();
      return '<option value="' + escapeHtml(row.id) + '"' + (row.id === selectedId ? ' selected' : '') + '>#' + row.rank + ' · ' +
        (sourceCode ? escapeHtml(sourceCode) + ' · ' : '') + escapeHtml(row.name) +
        (row.provisional ? ' · provisional Elo' : '') + '</option>';
      }).join('');
    }
    elements.matchupA.innerHTML = optionsFor(state.matchupA);
    elements.matchupB.innerHTML = optionsFor(state.matchupB);
    elements.matchupA.value = state.matchupA || '';
    elements.matchupB.value = state.matchupB || '';
    var rowA = rows.find(function (row) { return row.id === state.matchupA; });
    var rowB = rows.find(function (row) { return row.id === state.matchupB; });
    var venues = matchupVenueOptions(rowA, rowB);
    if (!venues.some(function (venue) { return venue.value === state.matchupVenue; })) state.matchupVenue = venues[0].value;
    elements.matchupVenue.innerHTML = venues.map(function (venue) {
      return '<option value="' + venue.value + '"' + (venue.value === state.matchupVenue ? ' selected' : '') + '>' + escapeHtml(venue.label) + '</option>';
    }).join('');
    elements.matchupVenue.value = state.matchupVenue;
    elements.matchupVenue.disabled = venues.length === 1;
    elements.matchupVenueLabel.textContent = state.sport === 'chess' ? 'Who plays White?' : state.sport === 'tennis' ? 'Surface' : 'Venue';
    setPressed(elements.matchupModelTabs, 'matchupModel', state.model);
    return {
      dataset: state.datasets[state.sport],
      rows: rows,
      rowA: rowA,
      rowB: rowB,
      venue: venues.find(function (item) { return item.value === state.matchupVenue; })
    };
  }

  function renderMatchup() {
    var selection = populateMatchupControls();
    var dataset = selection.dataset;
    var rowA = selection.rowA;
    var rowB = selection.rowB;
    if (!rowA || !rowB) {
      elements.matchupResult.innerHTML = '<p>Two published competitors are required for a matchup forecast.</p>';
      return;
    }
    var outcome = matchupOutcomes(rowA, rowB, dataset);
    var includesDraw = state.sport !== 'tennis';
    var outcomes = [
      { label: rowA.name + ' wins', short: 'A win', value: outcome.win, className: 'is-a' }
    ];
    if (includesDraw) outcomes.push({ label: 'Draw', short: 'Draw', value: outcome.draw, className: 'is-draw' });
    outcomes.push({ label: rowB.name + ' wins', short: 'B win', value: outcome.loss, className: 'is-b' });
    var strip = outcomes.map(function (item) {
      return '<span class="' + item.className + '" style="--outcome-width:' + (item.value * 100).toFixed(4) +
        '%" aria-hidden="true"></span>';
    }).join('');
    var cards = outcomes.map(function (item) {
      return '<div class="' + item.className + '"><span><i aria-hidden="true"></i>' + escapeHtml(item.label) +
        '</span><strong>' + percent(item.value) +
        '</strong><small>' + number(item.value * 100, 2) + '%</small></div>';
    }).join('');
    var venue = selection.venue;
    var parameters = outcome.parameters;
    var context = dataset.outcome_context || {
      draw_rate: state.sport === 'tennis' ? 0 : 0.25,
      draws: 0,
      matches: dataset.data_window.matches,
      method: 'Legacy snapshot fallback; refresh to schema 1.4.0 for cohort draw context.'
    };
    var beliefLabel = function (row) {
      return state.model === 'elo' ? number(row.rating, 1) : state.model === 'glicko2' ?
        'rating ' + number(row.rating, 2) + ', RD ' + number(row.sigma, 2) + ', volatility ' + number(row.volatility, 5) :
        'μ ' + number(row.rating, 2) + ', σ ' + number(row.sigma, 2);
    };
    var ratingA = beliefLabel(rowA);
    var ratingB = beliefLabel(rowB);
    if (outcome.contextA && outcome.contextB) {
      ratingA += '; ' + venue.label + ' ' + beliefLabel(outcome.contextA) + ' from ' + outcome.contextA.matches + ' matches';
      ratingB += '; ' + venue.label + ' ' + beliefLabel(outcome.contextB) + ' from ' + outcome.contextB.matches + ' matches';
    }
    var calculation;
    if (state.model === 'elo') {
      calculation = 'Expected score uses 1 / (1 + 10^(−Δ/' + number(parameters.scale, 0) + ')), where Δ includes ' +
        number(parameters.home, 2) + ' rating points when home advantage applies. The three-way split allocates draws as d = min(q × 4p(1−p), 2min(p,1−p)), using empirical q=' +
        number(outcome.empiricalDrawRate, 4) + ' from ' + number(context.draws, 0) + ' draws in ' +
        number(context.matches, 0) + ' replay results; win probabilities are p−d/2 and 1−p−d/2.';
    } else if (state.model === 'glicko2') {
      calculation = 'Expected score uses 1 / (1 + exp(−g(RDᵦ/173.7178) × Δ/173.7178)), with g(φ)=1/√(1+3φ²/π²). Δ includes ' +
        number(parameters.home, 2) + ' rating points when the selected home/White advantage applies. The result-only three-way display uses the same declared empirical-draw allocation as Elo; the Glicko-2 rating update itself records a draw as score 0.5.';
    } else {
      calculation = 'The published Gaussian skill beliefs are combined into Δ ~ N(' + number(outcome.difference, 3) + ', ' +
        number(outcome.variance, 3) + '). Win, draw, and loss likelihoods use ' +
        (state.model === 'robust' ? 'Student-t ν=1 performance noise' : 'Gaussian performance noise') +
        ' with β=' + number(parameters.beta, 4) + ' and draw margin=' + number(parameters.draw_margin, 4) +
        ', integrated with the same fixed 20-node Gauss–Hermite rule as the rating replay. The eligible cohort’s observed draw rate is ' +
        number(context.draw_rate * 100, 2) + '% (' + number(context.draws, 0) + ' of ' + number(context.matches, 0) +
        '); the Bayesian likelihood is not forced to equal that baseline.';
    }
    if (state.sport === 'tennis') {
      var surfaceDetail = outcome.surfaceExpected === null ?
        'One or both players have no published belief for this surface, so this matchup uses the global belief only.' :
        'Global expected score ' + number(outcome.globalExpected, 4) + ' and surface expected score ' +
        number(outcome.surfaceExpected, 4) + ' are blended with actual surface weight ' +
        number(outcome.surfaceWeight, 4) + '. The maximum selected surface weight is ' +
        number(parameters.surface_weight, 4) + '; evidence scales it over the first 20 combined surface matches.';
      calculation = surfaceDetail + ' ' + calculation;
    }
    var eventContext = state.sport === 'tennis' ? 'surface' : state.sport === 'chess' ? 'color' : 'venue';
    var unusedContext = state.sport === 'tennis' ?
      'It does not use score margin, injuries, player age, or bookmaker information' :
      'It does not use score margin, line-ups, injuries, time control, player age, or bookmaker information';
    elements.matchupResult.innerHTML = '<div class="rating-lab-matchup-context"><strong>' +
      escapeHtml(dataset.models[state.model].label) + '</strong><span>' + escapeHtml(venue.label) + ' · rating snapshot ' +
      escapeHtml(formatDate(dataset.latest_result)) + '</span></div><div class="rating-lab-outcome-strip" role="img" aria-label="' +
      escapeHtml(outcomes.map(function (item) { return item.label + ' ' + number(item.value * 100, 2) + ' percent'; }).join(', ')) + '">' +
      strip + '</div><div class="rating-lab-outcome-cards">' + cards + '</div><dl class="rating-lab-matchup-inputs"><div><dt>' +
      escapeHtml(rowA.name) + '</dt><dd>' + escapeHtml(ratingA) + '</dd></div><div><dt>Expected score A</dt><dd>' +
      number(outcome.expected, 4) + '</dd></div><div><dt>' + escapeHtml(rowB.name) + '</dt><dd>' + escapeHtml(ratingB) +
      '</dd></div></dl><details class="rating-lab-matchup-method"><summary>Exact calculation and assumptions</summary><p>' +
      escapeHtml(calculation) + '</p><p><strong>Published inputs:</strong> A ' + escapeHtml(ratingA) + '; B ' +
      escapeHtml(ratingB) + '; adjusted difference ' + number(outcome.difference, 3) + '. ' + escapeHtml(context.method) +
      '</p><p>This is a result-and-context probability for one event at the selected ' + eventContext + '. The published evaluation scores expected score, not a separately calibrated three-class forecast. ' + unusedContext + ', and it contains no betting margin. <a href="#protocol">Inspect the full protocol</a> or <a href="' +
      escapeHtml(dataset.source.source_url) + '">open the source data</a>.</p></details>';
  }

  function renderLeaguePredictorDetail(team, sport) {
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
      number(team.expected_position, 2) + '</p><h3>' + entityTitle(team, sport) + '</h3></div><strong>' +
      number(team.expected_points, 1) + ' pts</strong></div>' +
      '<div class="rating-lab-position-chart" role="img" aria-label="Finishing-position probabilities for ' +
      escapeHtml(team.name) + '">' + bars + '</div><div class="rating-lab-position-axis"><span>Champion</span><span>Position ' +
      team.positions.length + '</span></div><dl><div><dt>Title</dt><dd>' + percent(team.champion) +
      '</dd></div><div><dt>Top four</dt><dd>' + percent(team.top_four) +
      '</dd></div><div><dt>Bottom three</dt><dd>' + percent(team.bottom_three) +
      '</dd></div><div><dt>Current points</dt><dd>' + team.current_points + '</dd></div></dl>' + mediaCredit(team, sport);
  }

  function renderLeaguePriorDetail(team, sport) {
    if (!team) {
      elements.predictorDetail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a team to inspect its pre-season expected-points prior.</p>';
      return;
    }
    var bars = team.positions.map(function (probability, index) {
      return '<span class="rating-lab-position-bar" style="--height:' + Math.max(probability * 100, 1).toFixed(1) +
        '%" aria-label="Prior probability of position ' + (index + 1) + ': ' + escapeHtml(percent(probability)) + '"></span>';
    }).join('');
    elements.predictorDetail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">Upcoming · prior-heavy</p><h3>' +
      entityTitle(team, sport) + '</h3></div><strong>' + number(team.expected_points, 1, 1) + ' pts</strong></div>' +
      '<div class="rating-lab-position-chart" role="img" aria-label="Prior finishing-position probabilities for ' +
      escapeHtml(team.name) + '">' + bars + '</div><div class="rating-lab-position-axis"><span>Champion</span><span>Position ' +
      team.positions.length + '</span></div><dl><div><dt>Expected points</dt><dd>' +
      number(team.expected_points, 1, 1) + '</dd></div><div><dt>Prior title probability</dt><dd>' +
      percent(team.champion) + '</dd></div><div><dt>Prior top four</dt><dd>' +
      percent(team.top_four) + '</dd></div><div><dt>Prior bottom three</dt><dd>' +
      percent(team.bottom_three) + '</dd></div><div><dt>Matches played</dt><dd>0</dd></div></dl>' +
      '<p class="rating-lab-performance-note">No result from this competition has entered the simulation. These are explicit prior-heavy expected outcomes, driven by starting ratings and the published schedule—not an in-season form claim.</p>' +
      mediaCredit(team, sport);
  }

  function renderStandingsPredictorDetail(team, sport) {
    if (!team) return renderLeaguePredictorDetail(team, sport);
    var bars = team.positions.map(function (probability, index) {
      return '<span class="rating-lab-position-bar" style="--height:' + Math.max(probability * 100, 1).toFixed(1) +
        '%" aria-label="Position ' + (index + 1) + ': ' + escapeHtml(percent(probability)) + '"></span>';
    }).join('');
    elements.predictorDetail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">Expected position ' +
      number(team.expected_position, 2) + '</p><h3>' + entityTitle(team, sport) + '</h3></div><strong>' +
      number(team.expected_points, 1) + ' pts</strong></div><div class="rating-lab-position-chart" role="img" aria-label="Final-position probabilities for ' +
      escapeHtml(team.name) + '">' + bars + '</div><div class="rating-lab-position-axis"><span>Winner</span><span>Position ' +
      team.positions.length + '</span></div><dl><div><dt>Win event</dt><dd>' + percent(team.champion) +
      '</dd></div><div><dt>Podium</dt><dd>' + percent(team.podium) + '</dd></div><div><dt>Last place</dt><dd>' +
      percent(team.last_place) + '</dd></div><div><dt>Current points</dt><dd>' + number(team.current_points, 1) + '</dd></div></dl>' + mediaCredit(team, sport);
  }

  function tieForTeam(model, teamId) {
    return (model.ties || []).find(function (tie) {
      return tie.team_a_id === teamId || tie.team_b_id === teamId;
    });
  }

  function tieSnapshot(team, model) {
    var tie = tieForTeam(model, team.id);
    if (!tie) return '';
    var isA = tie.team_a_id === team.id;
    var opponent = isA ? tie.team_b_name : tie.team_a_name;
    var ownGoals = isA ? tie.aggregate_a : tie.aggregate_b;
    var opponentGoals = isA ? tie.aggregate_b : tie.aggregate_a;
    var opponentAdvance = isA ? tie.team_b_advance : tie.team_a_advance;
    var score = tie.completed_legs ?
      number(ownGoals, 0) + '–' + number(opponentGoals, 0) + ' aggregate' :
      'Tie not started';
    return '<section class="rating-lab-tie-snapshot"><p class="rating-lab-kicker">Current published tie</p>' +
      '<div><span>' + escapeHtml(team.name) + '</span><strong>' + escapeHtml(score) +
      '</strong></div><div><span>' + escapeHtml(opponent) + '</span><strong>' +
      percent(opponentAdvance) + ' advance</strong></div><p>' +
      number(tie.completed_legs, 0) + ' played · ' + number(tie.remaining_legs, 0) +
      ' remaining</p></section>';
  }

  function tieSummary(team, model) {
    var tie = tieForTeam(model, team.id);
    if (!tie) return '';
    var isA = tie.team_a_id === team.id;
    var opponent = isA ? tie.team_b_name : tie.team_a_name;
    var ownGoals = isA ? tie.aggregate_a : tie.aggregate_b;
    var opponentGoals = isA ? tie.aggregate_b : tie.aggregate_a;
    return '<small>vs ' + escapeHtml(opponent) + ' · ' +
      (tie.completed_legs ? number(ownGoals, 0) + '–' + number(opponentGoals, 0) + ' aggregate' : 'not started') +
      '</small>';
  }

  function renderKnockoutPredictorDetail(team, model, sport) {
    if (!team) {
      elements.predictorDetail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a participant to inspect its advancement probabilities.</p>';
      return;
    }
    var nextLabel = model.current_stage === 'Complete' ? 'Recorded champion' : 'Survive published stage';
    elements.predictorDetail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">' +
      escapeHtml(model.current_stage) + '</p><h3>' + entityTitle(team, sport) + '</h3></div><strong>' +
      percent(team.champion) + '</strong></div>' + tieSnapshot(team, model) +
      '<dl><div><dt>Win competition</dt><dd>' + percent(team.champion) +
      '</dd></div><div><dt>' + escapeHtml(nextLabel) + '</dt><dd>' + percent(team.reach_next_stage) +
      '</dd></div><div><dt>Model rating</dt><dd>' + number(team.rating, 1) + '</dd></div></dl>' + mediaCredit(team, sport);
  }

  function renderTennisPredictorDetail(team, model, sport) {
    if (!team) {
      elements.predictorDetail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a player to inspect the surface-aware matchup and full progression curve.</p>';
      return;
    }
    var nextMatch = team.next_match;
    var matchup = nextMatch ?
      '<section class="rating-lab-tennis-matchup"><p class="rating-lab-kicker">Next published matchup · ' +
      escapeHtml(nextMatch.round) + '</p><div><span>' + escapeHtml(team.name) + '</span><strong>' +
      percent(nextMatch.win_probability) + '</strong></div><div><span>' + escapeHtml(nextMatch.opponent_name) +
      '</span><strong>' + percent(1 - nextMatch.win_probability) + '</strong></div><p>' +
      escapeHtml(nextMatch.surface) + ' · selected protocol · no market input</p></section>' :
      '<p class="rating-lab-performance-note">No direct opponent is currently pending for this player: the player has either already advanced, been eliminated, or is waiting for the preceding bracket match.</p>';
    var progression = (team.round_probabilities || []).map(function (stage) {
      return '<div class="rating-lab-tennis-progression-row"><span>' + escapeHtml(stage.stage) +
        '</span><span class="rating-lab-tennis-progression-track" aria-hidden="true"><i style="--progress:' +
        (stage.probability * 100).toFixed(2) + '%"></i></span><strong>' + percent(stage.probability) +
        '</strong></div>';
    }).join('');
    elements.predictorDetail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">' +
      escapeHtml(model.surface + ' · ' + model.current_stage) + '</p><h3>' + entityTitle(team, sport) +
      '</h3></div><strong>' + percent(team.champion) + '</strong></div>' + matchup +
      '<section class="rating-lab-tennis-progression"><h4>Progression probability</h4>' + progression +
      '</section><dl><div><dt>Win tournament</dt><dd>' + percent(team.champion) +
      '</dd></div><div><dt>Global rating</dt><dd>' + number(team.rating, 1) +
      '</dd></div><div><dt>' + escapeHtml(model.surface) + ' rating</dt><dd>' +
      (Number.isFinite(team.surface_rating) ? number(team.surface_rating, 1) : 'Prior') +
      '</dd></div><div><dt>Surface evidence</dt><dd>' + number(team.surface_matches, 0) +
      ' matches</dd></div></dl><p class="rating-lab-performance-note">The direct probability blends the global belief with the selected-surface belief. The surface weight grows with evidence and is exactly the parameter published in Methods & data.</p>' +
      mediaCredit(team, sport);
  }

  function tennisInlineDetail(team, model) {
    var matchup = team.next_match ?
      '<p><strong>' + percent(team.next_match.win_probability) + '</strong> vs ' +
      escapeHtml(team.next_match.opponent_name) + ' · ' + escapeHtml(team.next_match.round) +
      '</p>' : '<p>Direct opponent pending or event run complete.</p>';
    var stages = (team.round_probabilities || []).map(function (stage) {
      return '<span><small>' + escapeHtml(stage.stage) + '</small><strong>' +
        percent(stage.probability) + '</strong></span>';
    }).join('');
    return '<tr class="rating-lab-tennis-inline-detail"><td colspan="5"><div><p class="rating-lab-kicker">' +
      escapeHtml(model.surface + ' probability') + '</p>' + matchup +
      '<div class="rating-lab-tennis-inline-stages">' + stages + '</div></div></td></tr>';
  }

  function renderQualifyingPredictorDetail(team, model, sport) {
    if (!team) {
      elements.predictorDetail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a club to inspect its current-round advancement probability.</p>';
      return;
    }
    elements.predictorDetail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">' +
      escapeHtml(model.current_stage + ' · ' + team.path + ' path') + '</p><h3>' + entityTitle(team, sport) +
      '</h3></div><strong>' + percent(team.reach_next_stage) + '</strong></div>' +
      tieSnapshot(team, model) + '<dl><div><dt>' +
      escapeHtml(model.target_label) + '</dt><dd>' + percent(team.reach_next_stage) +
      '</dd></div><div><dt>Model rating</dt><dd>' + number(team.rating, 1) +
      '</dd></div></dl><p class="rating-lab-performance-note">This is a probability of surviving the current published two-leg tie. It is not a Champions League title probability.</p>' + mediaCredit(team, sport);
  }

  function setPredictorColumns(type, targetLabel) {
    var tennis = type === 'tennis';
    var knockout = type === 'knockout' || tennis;
    var qualifying = type === 'qualifying';
    var standings = type === 'standings';
    elements.predictorColumns.rank.textContent = knockout || qualifying ? 'Forecast' : 'Projected';
    elements.predictorColumns.team.textContent = tennis ? 'Player' : knockout || qualifying ? 'Participant' : standings ? 'Player' : 'Team';
    elements.predictorColumns.now.textContent = knockout || qualifying ? 'Rating' : 'Now';
    elements.predictorColumns.value.textContent = qualifying ? targetLabel : tennis ? 'Advance' : knockout ? 'Next stage' : 'Expected pts';
    elements.predictorColumns.title.textContent = tennis ? 'Champion' : standings ? 'Win event' : 'Title';
    elements.predictorColumns.secondary.textContent = standings ? 'Podium' : 'Top four';
    elements.predictorColumns.tertiary.textContent = standings ? 'Last place' : 'Bottom three';
    elements.predictorColumns.now.hidden = false;
    elements.predictorColumns.value.hidden = false;
    elements.predictorColumns.secondary.hidden = knockout;
    elements.predictorColumns.tertiary.hidden = knockout;
    elements.predictorColumns.title.hidden = qualifying;
    if (qualifying) {
      elements.predictorColumns.secondary.hidden = true;
      elements.predictorColumns.tertiary.hidden = true;
    }
  }

  function setPerformanceColumns() {
    elements.predictorColumns.rank.textContent = 'TPR rank';
    elements.predictorColumns.team.textContent = 'Participant';
    elements.predictorColumns.now.textContent = 'W–D–L';
    elements.predictorColumns.value.textContent = 'Start rating';
    elements.predictorColumns.title.textContent = 'Performance rating';
    elements.predictorColumns.secondary.textContent = 'vs start';
    elements.predictorColumns.tertiary.textContent = 'Reset rank';
    elements.predictorColumns.now.hidden = false;
    elements.predictorColumns.value.hidden = false;
    elements.predictorColumns.title.hidden = false;
    elements.predictorColumns.secondary.hidden = false;
    elements.predictorColumns.tertiary.hidden = false;
  }

  function renderPerformanceDetail(team, model, sport) {
    if (!team) {
      elements.predictorDetail.innerHTML = '<p class="rating-lab-detail-placeholder">Choose a participant to inspect its completed-event performance.</p>';
      return;
    }
    var changeClass = team.performance_delta > 0 ? 'is-positive' : team.performance_delta < 0 ? 'is-negative' : '';
    var surpriseClass = team.score_residual > 0 ? 'is-positive' : team.score_residual < 0 ? 'is-negative' : '';
    var change = signedNumber(team.performance_delta, 2);
    var performanceRating = (team.performance_rating_cap === 'upper' ? '≥' : team.performance_rating_cap === 'lower' ? '≤' : '') +
      number(team.performance_rating, 2);
    var isGlicko = model.rating_type === 'glicko2_conservative_r_minus_2rd';
    var startBelief = model.rating_type === 'elo' ? number(team.start_rating, 2) : isGlicko ?
      'rating ' + number(team.start_rating, 2) + ' · RD ' + number(team.start_sigma, 2) + ' · volatility ' + number(team.start_volatility, 5) :
      'μ ' + number(team.start_rating, 2) + ' · σ ' + number(team.start_sigma, 2);
    var endBelief = model.rating_type === 'elo' ? number(team.end_rating, 2) : isGlicko ?
      'rating ' + number(team.end_rating, 2) + ' · RD ' + number(team.end_sigma, 2) + ' · volatility ' + number(team.end_volatility, 5) :
      'μ ' + number(team.end_rating, 2) + ' · σ ' + number(team.end_sigma, 2);
    elements.predictorDetail.innerHTML = '<div class="rating-lab-detail-heading"><div><p class="rating-lab-kicker">Protocol performance #' +
      team.rank + '</p><h3>' + entityTitle(team, sport) + '</h3></div><strong>' + escapeHtml(performanceRating) +
      '</strong></div><dl><div><dt>Event record</dt><dd>' + team.wins + '–' + team.draws + '–' + team.losses +
      '</dd></div><div><dt>Result score</dt><dd>' + number(team.points, 2) + ' / ' + number(team.matches, 0) +
      '</dd></div><div><dt>Protocol expectation</dt><dd>' + number(team.expected_score, 2) + ' / ' + number(team.matches, 0) +
      '</dd></div><div><dt>Score residual</dt><dd class="' + surpriseClass + '">' +
      signedNumber(team.score_residual, 2) +
      '</dd></div><div><dt>Standardized surprise</dt><dd class="' + surpriseClass + '">' +
      signedNumber(team.surprise_index, 2) + ' σ' +
      '</dd></div><div><dt>Anchored performance rating</dt><dd>' + escapeHtml(performanceRating) +
      '</dd></div><div><dt>TPR versus start</dt><dd class="' + changeClass + '">' + change +
      '</dd></div><div><dt>Tournament-only reset</dt><dd>' +
      (Number.isFinite(team.reset_rank) ? '#' + team.reset_rank + ' · ' + number(team.reset_rating, 2) : 'Unavailable in this snapshot') +
      '</dd></div><div><dt>Starting belief</dt><dd>' + escapeHtml(startBelief) + '</dd></div><div><dt>Final belief</dt><dd>' +
      escapeHtml(endBelief) + '</dd></div><div><dt>Published start</dt><dd>' + number(team.start_score, 2) +
      '</dd></div><div><dt>Post-event replay score</dt><dd>' + number(team.replay_rating, 2) +
      '</dd></div></dl><p class="rating-lab-performance-note">The performance rating solves the exact expected-score equation against opponents held at their pre-event beliefs. The reset rank starts everyone from the selected protocol’s neutral prior and uses only this event. The chronological surprise remains actual score minus the expectation recorded before each update.</p>' + mediaCredit(team, sport);
  }

  function renderPerformanceChart(rows, model, competition, sport) {
    var rankedRows = rows.filter(function (team) {
      return Number.isFinite(team.surprise_index) && Number.isFinite(team.expected_score);
    }).slice().sort(function (a, b) {
      return b.surprise_index - a.surprise_index || a.name.localeCompare(b.name);
    });
    if (!rankedRows.length) {
      elements.predictorPerformanceChart.hidden = true;
      elements.predictorPerformanceChart.innerHTML = '';
      return;
    }
    var chartRows = rankedRows.filter(function (team) { return team.surprise_index >= 0; }).slice(0, 6)
      .concat(rankedRows.filter(function (team) { return team.surprise_index < 0; }).slice(-6))
      .sort(function (a, b) { return b.surprise_index - a.surprise_index || a.name.localeCompare(b.name); });
    var maxAbs = Math.max(1, Math.max.apply(null, chartRows.map(function (team) {
      return Math.abs(team.surprise_index);
    })));
    var modelLabel = state.datasets[sport].models[state.predictorModel].label;
    elements.predictorPerformanceChart.hidden = false;
    elements.predictorPerformanceChart.innerHTML =
      '<div class="rating-lab-performance-heading"><div><p class="rating-lab-kicker">Actual versus expected</p>' +
      '<h3 id="predictor-performance-title">Largest finished-event surprises</h3></div>' +
      '<p>Selected protocol: <strong>' + escapeHtml(modelLabel) + '</strong></p></div>' +
      '<p class="rating-lab-performance-subtitle">The six largest outperformers and underperformers by signed standardized result-score residual. Solid dark bars point right; outlined light bars point left, so color is not the only cue. The complete participant table remains below.</p>' +
      '<div class="rating-lab-performance-scroll"><div class="rating-lab-performance-plot" role="group" aria-label="' +
      escapeHtml(competitionTitle(competition) + ' actual result score versus ' + modelLabel + ' expectation') + '">' +
      '<div class="rating-lab-performance-axis" aria-hidden="true"><span>Underperformed</span><span>As expected</span><span>Outperformed</span></div>' +
      chartRows.map(function (team) {
        var positive = team.surprise_index >= 0;
        var signedSurprise = signedNumber(team.surprise_index, 2) + ' σ';
        var signedResidual = signedNumber(team.score_residual, 2);
        var size = Math.min(Math.abs(team.surprise_index) / maxAbs * 50, 50).toFixed(3) + '%';
        var label = team.name + ': actual ' + number(team.points, 2) + ', expected ' + number(team.expected_score, 2) +
          ', residual ' + signedResidual + ', standardized surprise ' + signedSurprise + ', ' + team.matches + ' matches';
        return '<button type="button" class="rating-lab-performance-row' +
          (team.id === state.predictorTeam ? ' is-selected' : '') + '" data-predictor-team="' + escapeHtml(team.id) +
          '" aria-label="' + escapeHtml(label) + '"><span class="rating-lab-performance-name"><span class="rating-lab-performance-identity-line">' +
          entityBadge(team, sport) + '<span>' + escapeHtml(team.name) + '</span></span><small>' + team.matches +
          ' match' + (team.matches === 1 ? '' : 'es') + ' · ' + number(team.points, 2) +
          ' actual / ' + number(team.expected_score, 2) + ' expected</small></span><span class="rating-lab-performance-track" aria-hidden="true">' +
          '<span class="rating-lab-performance-zero"></span><span class="rating-lab-performance-bar ' +
          (positive ? 'is-outperformer' : 'is-underperformer') + '" style="--bar-size:' + size + '"></span></span>' +
          '<strong>' + escapeHtml(signedSurprise) + '</strong></button>';
      }).join('') + '</div></div><p class="rating-lab-performance-footnote">' + escapeHtml(model.surprise_method) + '</p>';
  }

  function renderCompletedPerformance(view) {
    var competition = view.competition;
    var model = competition.performance.models[state.predictorModel];
    var rows = model.participants;
    if (!state.predictorTeam || !rows.some(function (team) { return team.id === state.predictorTeam; })) {
      state.predictorTeam = rows[0].id;
    }
    setPerformanceColumns();
    renderCompetitionState(competition, competition.format || 'competition');
    elements.predictorMetrics.innerHTML = [
      ['Recorded results', number(model.results, 0)],
      ['Participants', number(rows.length, 0)],
      ['Performance rating', model.rating_type === 'elo' ? 'Anchored Elo TPR' : model.rating_type === 'glicko2_conservative_r_minus_2rd' ? 'Anchored Glicko rating' : 'Anchored skill mean']
    ].map(function (item) {
      return '<div><span>' + escapeHtml(item[0]) + '</span><strong>' + escapeHtml(item[1]) + '</strong></div>';
    }).join('');
    elements.predictorCaption.textContent = competitionTitle(competition) + ' · finished performance by ' +
      state.datasets[view.sport].models[state.predictorModel].label;
    renderMarketComparison(view, [], { resolved: true });
    renderPerformanceChart(rows, model, competition, view.sport);
    elements.predictorBody.innerHTML = rows.map(function (team) {
      var changeClass = team.performance_delta > 0 ? 'is-positive' : team.performance_delta < 0 ? 'is-negative' : '';
      var change = signedNumber(team.performance_delta, 2);
      var performanceRating = (team.performance_rating_cap === 'upper' ? '≥' : team.performance_rating_cap === 'lower' ? '≤' : '') +
        number(team.performance_rating, 2);
      return '<tr' + (team.id === state.predictorTeam ? ' class="is-selected"' : '') + '><td class="rating-lab-rank">' +
        team.rank + '</td><th scope="row" class="rating-lab-predictor-entity"><button type="button" class="rating-lab-predictor-team" data-predictor-team="' +
        escapeHtml(team.id) + '">' + entityBadge(team, view.sport) + '<span>' + escapeHtml(team.name) +
        '</span></button></th><td class="rating-lab-predictor-now">' + team.wins + '–' + team.draws + '–' +
        team.losses + '</td><td class="rating-lab-predictor-value">' + number(team.start_rating, 2) + '</td><td class="rating-lab-predictor-title"><strong>' + escapeHtml(performanceRating) +
        '</strong></td><td class="rating-lab-optional ' + changeClass + '">' + change +
        '</td><td class="rating-lab-optional">' +
        (Number.isFinite(team.reset_rank) ? '#' + team.reset_rank : '—') + '</td></tr>';
    }).join('');
    renderPerformanceDetail(rows.find(function (team) { return team.id === state.predictorTeam; }), model, view.sport);
    elements.predictorMethod.innerHTML = escapeHtml(competition.performance.method) + ' Selected model parameters are the same ones shown in the protocol section. Snapshot: <code>' +
      escapeHtml(competition.snapshot_sha256.substring(0, 12)) + '</code>. <a href="' +
      escapeHtml(competition.source_url) + '">Open completed competition source</a>.';
  }

  function renderPredictor() {
    var view = predictorData();
    if (!view) return;
    elements.predictorPerformanceChart.hidden = true;
    elements.predictorPerformanceChart.innerHTML = '';
    var competition = view.competition;
    var model = view.model;
    var predictorTable = elements.predictorBody.closest('.rating-lab-predictor-table');
    predictorTable.classList.remove('is-league', 'is-preseason', 'is-knockout', 'is-completed');
    var competitionFormat = competition.format || (model && model.teams ? 'round-robin league' : 'knockout cup');
    var currentState = competitionState(competition);
    renderCompetitionState(competition, competitionFormat);
    if (currentState === 'finished' && competition.performance && competition.performance.models[state.predictorModel]) {
      predictorTable.classList.add('is-completed');
      renderCompletedPerformance(view);
      return;
    }
    if (competition.forecast_available === false || !model) {
      setPredictorColumns('knockout');
      elements.predictorMetrics.innerHTML = [
        ['Competition state', stateLabel(currentState)],
        ['Results locked', number(competition.completed_matches || 0, 0) + ' of ' + number(competition.total_matches, 0)],
        ['Title forecast', 'Withheld']
      ].map(function (item) {
        return '<div><span>' + escapeHtml(item[0]) + '</span><strong>' + escapeHtml(item[1]) + '</strong></div>';
      }).join('');
      elements.predictorCaption.textContent = competitionTitle(competition) + ' · published structure pending';
      elements.predictorBody.innerHTML = '<tr><td colspan="5"><strong>The next forecastable draw or field is not published yet.</strong><br>' +
        escapeHtml(competition.availability) + '</td></tr>';
      elements.predictorDetail.innerHTML = '<p>' + escapeHtml(competition.availability) + '</p>';
      elements.predictorMethod.innerHTML = escapeHtml(view.predictor.availability_rule) + ' <a href="' +
        escapeHtml(competition.source_url) + '">Open competition source</a>.';
      renderMarketComparison(view, []);
      return;
    }
    var isLeague = model.forecast_type === 'league' || Boolean(model.teams);
    var isStandings = model.forecast_type === 'standings';
    var isQualifying = model.forecast_type === 'qualifying_round';
    var isTennisDraw = model.forecast_type === 'tennis_draw';
    var rows = isLeague ? model.teams.slice().sort(function (a, b) {
      return b.expected_points - a.expected_points || a.name.localeCompare(b.name);
    }) : model.participants.slice().sort(function (a, b) {
      if (isQualifying) {
        return b.reach_next_stage - a.reach_next_stage || b.rating - a.rating || a.name.localeCompare(b.name);
      }
      return b.champion - a.champion || b.reach_next_stage - a.reach_next_stage ||
        b.rating - a.rating || a.name.localeCompare(b.name);
    });
    if (!state.predictorTeam || !rows.some(function (team) { return team.id === state.predictorTeam; })) {
      state.predictorTeam = rows[0].id;
    }
    var isPreseason = isLeague && model.completed_matches === 0;
    predictorTable.classList.add(isLeague ? 'is-league' : 'is-knockout');
    if (isPreseason) predictorTable.classList.add('is-preseason');
    setPredictorColumns(isStandings ? 'standings' : isLeague ? 'league' : isQualifying ? 'qualifying' : isTennisDraw ? 'tennis' : 'knockout', model.target_label);
    if (isPreseason) {
      elements.predictorColumns.now.hidden = true;
      elements.predictorColumns.title.textContent = 'Prior title';
      elements.predictorColumns.secondary.textContent = isStandings ? 'Prior podium' : 'Prior top four';
      elements.predictorColumns.tertiary.textContent = isStandings ? 'Prior last' : 'Prior bottom three';
    }
    if (!isLeague) {
      if (isQualifying) {
        elements.predictorMetrics.innerHTML = [
          ['Current round', model.current_stage],
          ['Official ties', number(model.published_ties_remaining, 0)],
          ['Next fixture', competition.next_fixture ? formatDate(competition.next_fixture) : 'Awaiting official update']
        ].map(function (item) {
          return '<div><span>' + escapeHtml(item[0]) + '</span><strong>' + escapeHtml(item[1]) + '</strong></div>';
        }).join('');
        elements.predictorCaption.textContent = competitionTitle(competition) + ' · current-round advancement by ' +
          state.datasets[view.sport].models[state.predictorModel].label;
        elements.predictorBody.innerHTML = rows.map(function (team, index) {
          return '<tr' + (team.id === state.predictorTeam ? ' class="is-selected"' : '') + '><td class="rating-lab-rank">' +
            (index + 1) + '</td><th scope="row" class="rating-lab-predictor-entity"><button type="button" class="rating-lab-predictor-team" data-predictor-team="' +
            escapeHtml(team.id) + '">' + entityBadge(team, view.sport) + '<span><span>' + escapeHtml(team.name) +
            '</span>' + tieSummary(team, model) + '</span></button></th><td class="rating-lab-predictor-now">' + number(team.rating, 1) +
            '</td><td class="rating-lab-predictor-value">' + probabilityCell(team.reach_next_stage) + '</td></tr>';
        }).join('');
        renderQualifyingPredictorDetail(rows.find(function (team) { return team.id === state.predictorTeam; }), model, view.sport);
        renderMarketComparison(view, rows);
        var timeline = (competition.round_timeline || []).map(function (round) {
          return round.label + ': draw ' + formatDate(round.draw_date) + '; matches ' +
            round.match_dates.map(formatDate).join(', ');
        }).join(' ');
        elements.predictorMethod.innerHTML = number(model.simulations, 0) + ' deterministic current-round simulations. ' +
          escapeHtml(model.scoreline_method) + ' ' + escapeHtml(competition.availability) + ' Official calendar: ' +
          escapeHtml(timeline) + ' Fixed seed: <code>' + escapeHtml(String(model.seed)) + '</code>. Snapshot: <code>' +
          escapeHtml(competition.snapshot_sha256.substring(0, 12)) + '</code>. <a href="' +
          escapeHtml(competition.source_url) + '">Open UEFA fixture source</a>.';
        return;
      }
      if (isTennisDraw) {
        elements.predictorMetrics.innerHTML = [
          ['Current round', model.current_stage],
          ['Surface', model.surface],
          ['Forecast sample', number(model.simulations, 0) + ' locked-draw simulations']
        ].map(function (item) {
          return '<div><span>' + escapeHtml(item[0]) + '</span><strong>' + escapeHtml(item[1]) + '</strong></div>';
        }).join('');
        elements.predictorCaption.textContent = competitionTitle(competition) + ' · surface-aware progression by ' +
          state.datasets[view.sport].models[state.predictorModel].label;
        elements.predictorBody.innerHTML = rows.map(function (team, index) {
          var opponent = team.next_match ?
            '<small>vs ' + escapeHtml(team.next_match.opponent_name) + ' · ' +
            percent(team.next_match.win_probability) + '</small>' : '';
          var row = '<tr' + (team.id === state.predictorTeam ? ' class="is-selected"' : '') + '><td class="rating-lab-rank">' +
            (index + 1) + '</td><th scope="row" class="rating-lab-predictor-entity"><button type="button" class="rating-lab-predictor-team" data-predictor-team="' +
            escapeHtml(team.id) + '">' + entityBadge(team, view.sport) + '<span><span>' + escapeHtml(team.name) +
            '</span>' + opponent + '</span></button></th><td class="rating-lab-predictor-now">' + number(team.rating, 1) +
            '</td><td class="rating-lab-predictor-value">' + probabilityCell(team.reach_next_stage) +
            '</td><td class="rating-lab-predictor-title">' + probabilityCell(team.champion) + '</td></tr>';
          return row + (team.id === state.predictorTeam ? tennisInlineDetail(team, model) : '');
        }).join('');
        renderTennisPredictorDetail(rows.find(function (team) { return team.id === state.predictorTeam; }), model, view.sport);
        elements.predictorMarket.hidden = true;
        elements.predictorMarket.innerHTML = '';
        elements.predictorMethod.innerHTML = number(model.simulations, 0) +
          ' deterministic simulations of the official bracket. Completed matches and byes are locked; every unplayed match uses the selected protocol’s ' +
          escapeHtml(model.surface) + ' probability. ' + escapeHtml(view.predictor.tennis_draw) +
          ' Fixed seed: <code>' + escapeHtml(String(model.seed)) + '</code>. Snapshot: <code>' +
          escapeHtml(competition.snapshot_sha256.substring(0, 12)) + '</code>. ' +
          escapeHtml(competition.date_method || '') + ' <a href="' + escapeHtml(competition.source_url) +
          '">Open official ATP draw</a>.';
        return;
      }
      elements.predictorMetrics.innerHTML = [
        ['Competition state', model.current_stage],
        ['Published ties left', number(model.published_ties_remaining, 0)],
        ['Forecast sample', number(model.simulations, 0) + ' deterministic brackets']
      ].map(function (item) {
        return '<div><span>' + escapeHtml(item[0]) + '</span><strong>' + escapeHtml(item[1]) + '</strong></div>';
      }).join('');
      elements.predictorCaption.textContent = competitionTitle(competition) + ' · title forecast by ' +
        state.datasets[view.sport].models[state.predictorModel].label;
      elements.predictorBody.innerHTML = rows.map(function (team, index) {
        return '<tr' + (team.id === state.predictorTeam ? ' class="is-selected"' : '') + '><td class="rating-lab-rank">' +
          (index + 1) + '</td><th scope="row" class="rating-lab-predictor-entity"><button type="button" class="rating-lab-predictor-team" data-predictor-team="' +
        escapeHtml(team.id) + '">' + entityBadge(team, view.sport) + '<span><span>' + escapeHtml(team.name) +
        '</span>' + tieSummary(team, model) + '</span></button></th><td class="rating-lab-predictor-now">' + number(team.rating, 1) +
          '</td><td class="rating-lab-predictor-value">' + probabilityCell(team.reach_next_stage) + '</td><td class="rating-lab-predictor-title">' + probabilityCell(team.champion) + '</td></tr>';
      }).join('');
      renderKnockoutPredictorDetail(rows.find(function (team) { return team.id === state.predictorTeam; }), model, view.sport);
      renderMarketComparison(view, rows);
      elements.predictorMethod.innerHTML = number(model.simulations, 0) + ' simulations. Published ties are locked. ' +
        escapeHtml(view.predictor.knockout_draw) + ' Fixed seed: <code>' + escapeHtml(String(model.seed)) +
        '</code>. Snapshot: <code>' + escapeHtml(competition.snapshot_sha256.substring(0, 12)) +
        '</code>. <a href="' + escapeHtml(competition.source_url) + '">Open competition source</a>.';
      return;
    }
    elements.predictorMetrics.innerHTML = [
      ['Competition state', stateLabel(currentState) + ' · ' + model.completed_matches + ' of ' + competition.total_matches + ' played'],
      ['Next fixture', competition.next_fixture ? formatDate(competition.next_fixture) : currentState === 'finished' ? 'Competition finished' : 'Awaiting fixture'],
      [isPreseason ? 'Forecast basis' : 'Forecast sample', isPreseason ? 'Prior-heavy · no current results' : number(model.simulations, 0) + (isStandings ? ' deterministic tournaments' : ' deterministic seasons')]
    ].map(function (item) {
      return '<div><span>' + escapeHtml(item[0]) + '</span><strong>' + escapeHtml(item[1]) + '</strong></div>';
    }).join('');
    elements.predictorCaption.textContent = competitionTitle(competition) + (isPreseason ? ' · pre-season expected points; spread reflects priors · ' : ' · projected by ') +
      state.datasets[view.sport].models[state.predictorModel].label;
    elements.predictorBody.innerHTML = rows.map(function (team, index) {
      return '<tr' + (team.id === state.predictorTeam ? ' class="is-selected"' : '') + '><td class="rating-lab-rank">' +
        (index + 1) + '</td><th scope="row" class="rating-lab-predictor-entity"><button type="button" class="rating-lab-predictor-team" data-predictor-team="' +
        escapeHtml(team.id) + '">' + entityBadge(team, view.sport) + '<span>' + escapeHtml(team.name) +
        '</span></button></th>' + (isPreseason ? '' : '<td class="rating-lab-predictor-now" data-label="Now">' +
        (team.played ? team.current_rank : '—') + '</td>') + '<td class="rating-lab-predictor-value"><strong>' + number(team.expected_points, 1, 1) +
        '</strong></td><td class="rating-lab-predictor-title" data-label="' + (isPreseason ? 'Prior title' : 'Title') + '">' +
        probabilityCell(team.champion) + '</td><td class="rating-lab-optional" data-label="' +
        (isPreseason ? 'Prior ' : '') + (isStandings ? 'Podium' : 'Top four') + '">' +
        probabilityCell(isStandings ? team.podium : team.top_four) + '</td><td class="rating-lab-optional" data-label="' +
        (isPreseason ? 'Prior ' : '') + (isStandings ? 'Last' : 'Bottom three') + '">' +
        probabilityCell(isStandings ? team.last_place : team.bottom_three) + '</td></tr>';
    }).join('');
    var selectedTeam = rows.find(function (team) { return team.id === state.predictorTeam; });
    if (isPreseason) renderLeaguePriorDetail(selectedTeam, view.sport);
    else if (isStandings) renderStandingsPredictorDetail(selectedTeam, view.sport);
    else renderLeaguePredictorDetail(selectedTeam, view.sport);
    renderMarketComparison(view, rows, isPreseason ? {
      withheld: 'This competition has 0 completed matches. The visible expected-points spread reflects starting ratings and schedule priors; title comparisons are withheld until play begins.'
    } : null);
    elements.predictorMethod.innerHTML = escapeHtml(view.predictor.simulations_per_model) +
      ' simulations per model and competition. Fixed seed: <code>' + escapeHtml(String(model.seed)) +
      '</code>. Fixture snapshot: <code>' + escapeHtml(competition.snapshot_sha256.substring(0, 12)) +
      '</code>. ' + escapeHtml(competition.availability || '') + (competition.tie_break ? ' ' + escapeHtml(competition.tie_break) : '') +
      ' <a href="' + escapeHtml(competition.source_url) + '">Open fixture source</a>.';
  }

  function render() {
    updateFreshness();
    renderProvisionalControl();
    renderMetrics();
    renderMovers();
    renderTable();
    renderDetail();
    renderMatchup();
    renderProtocol();
    renderAudit();
    renderPredictor();
    syncMobileFilters();
    updateQuickModel();
  }

  var quickModelContext = null;
  var quickModelFrame = null;

  function modelLabel(model) {
    return { elo: 'Elo', glicko2: 'Glicko-2', trueskill: 'Gaussian', robust: 'Robust' }[model] || model;
  }

  function closeQuickModel() {
    elements.quickModel.classList.remove('is-open');
    elements.quickModelTrigger.setAttribute('aria-expanded', 'false');
  }

  function quickContext() {
    var probe = window.innerHeight * 0.36;
    var contexts = [
      { id: 'leaderboard', section: document.querySelector('.rating-lab-explorer'), tabs: elements.mobileFilterTrigger },
      { id: 'matchup', section: document.getElementById('matchup'), tabs: elements.matchupModelTabs },
      { id: 'predictor', section: document.getElementById('predictor'), tabs: elements.predictorModelTabs }
    ];
    return contexts.find(function (context) {
      if (!context.section) return false;
      var rect = context.section.getBoundingClientRect();
      return rect.top <= probe && rect.bottom > probe;
    }) || null;
  }

  function updateQuickModel() {
    if (!elements.quickModel || !window.matchMedia('(max-width: 650px)').matches) {
      if (elements.quickModel) elements.quickModel.hidden = true;
      return;
    }
    var context = quickContext();
    if (!context) {
      elements.quickModel.hidden = true;
      closeQuickModel();
      return;
    }
    quickModelContext = context.id;
    var tabsRect = context.tabs.getBoundingClientRect();
    var originalControlsVisible = tabsRect.bottom > 0 && tabsRect.top < window.innerHeight;
    elements.quickModel.hidden = originalControlsVisible;
    if (originalControlsVisible) closeQuickModel();
    var activeModel = context.id === 'predictor' ? state.predictorModel : state.model;
    elements.quickModelLabel.textContent = modelLabel(activeModel);
    elements.quickModelMenu.querySelectorAll('[data-quick-model]').forEach(function (button) {
      button.setAttribute('aria-pressed', String(button.dataset.quickModel === activeModel));
    });
  }

  function queueQuickModelUpdate() {
    if (quickModelFrame !== null) return;
    quickModelFrame = window.requestAnimationFrame(function () {
      quickModelFrame = null;
      updateQuickModel();
    });
  }

  function revealDetailOnMobile() {
    if (!window.matchMedia('(max-width: 650px)').matches || elements.detail.hidden) return;
    window.setTimeout(function () {
      elements.detail.scrollIntoView({
        behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
        block: 'start'
      });
    }, 0);
  }

  function selectLeaderboardModel(model) {
    if (!model || model === state.model) return;
    state.model = model;
    state.expanded = false;
    state.visibleRows = 0;
    state.includeProvisional = false;
    setPressed(elements.modelTabs, 'model', state.model);
    syncData();
  }

  function setIncludeProvisional(value) {
    state.includeProvisional = Boolean(value);
    state.expanded = false;
    state.visibleRows = 0;
    if (!state.includeProvisional) {
      var selected = state.datasets[state.sport].models[state.model].rankings.find(function (row) {
        return row.id === state.selected;
      });
      if (selected && selected.provisional) state.selected = null;
    }
    renderProvisionalControl();
    renderMetrics();
    renderMovers();
    renderTable();
    renderDetail();
  }

  function closeMobileFilters() {
    if (typeof elements.mobileFilterSheet.close === 'function') elements.mobileFilterSheet.close();
    else elements.mobileFilterSheet.removeAttribute('open');
  }

  elements.sportTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-sport]');
    if (!button || button.dataset.sport === state.sport) return;
    state.sport = button.dataset.sport;
    state.selected = null;
    state.pinned = [];
    state.expanded = false;
    state.visibleRows = 0;
    state.includeProvisional = false;
    state.matchupA = null;
    state.matchupB = null;
    state.matchupVenue = 'neutral';
    setPressed(elements.sportTabs, 'sport', state.sport);
    populateCompetitions();
    syncData();
  });

  elements.localNav.addEventListener('click', function (event) {
    var link = event.target.closest('a[href^="#"]');
    if (!link) return;
    elements.localNav.querySelectorAll('a[aria-current]').forEach(function (item) {
      item.removeAttribute('aria-current');
    });
    link.setAttribute('aria-current', 'location');
  });

  if ('IntersectionObserver' in window) {
    var navSections = [
      ['leaderboard-heading', '#leaderboard-heading'],
      ['matchup', '#matchup'],
      ['predictor', '#predictor'],
      ['research', '#research']
    ];
    var navObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var mapping = navSections.find(function (item) { return item[0] === entry.target.id; });
        if (!mapping) return;
        elements.localNav.querySelectorAll('a[aria-current]').forEach(function (item) {
          item.removeAttribute('aria-current');
        });
        var active = elements.localNav.querySelector('a[href="' + mapping[1] + '"]');
        if (active) active.setAttribute('aria-current', 'location');
      });
    }, { rootMargin: '-20% 0px -68% 0px', threshold: 0 });
    navSections.forEach(function (mapping) {
      var section = document.getElementById(mapping[0]);
      if (section) navObserver.observe(section);
    });
  }

  elements.modelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-model]');
    if (!button) return;
    selectLeaderboardModel(button.dataset.model);
  });

  elements.mobileFilterTrigger.addEventListener('click', function () {
    syncMobileFilters();
    if (typeof elements.mobileFilterSheet.showModal === 'function') elements.mobileFilterSheet.showModal();
    else elements.mobileFilterSheet.setAttribute('open', '');
  });

  elements.mobileFilterClose.addEventListener('click', closeMobileFilters);
  elements.mobileFilterApply.addEventListener('click', closeMobileFilters);
  elements.mobileFilterSheet.addEventListener('click', function (event) {
    if (event.target === elements.mobileFilterSheet) closeMobileFilters();
  });

  elements.mobileModelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-mobile-model]');
    if (!button) return;
    selectLeaderboardModel(button.dataset.mobileModel);
  });

  elements.mobileCompetition.addEventListener('change', function () {
    state.competition = elements.mobileCompetition.value;
    elements.competition.value = state.competition;
    state.expanded = false;
    state.visibleRows = 0;
    renderMetrics();
    renderMovers();
    renderTable();
    renderDetail();
    syncMobileFilters();
  });

  elements.mobileIncludeProvisional.addEventListener('change', function () {
    setIncludeProvisional(elements.mobileIncludeProvisional.checked);
  });

  elements.quickModelTrigger.addEventListener('click', function (event) {
    event.stopPropagation();
    var opening = !elements.quickModel.classList.contains('is-open');
    elements.quickModel.classList.toggle('is-open', opening);
    elements.quickModelTrigger.setAttribute('aria-expanded', String(opening));
  });

  elements.quickModelMenu.addEventListener('click', function (event) {
    event.stopPropagation();
    var button = event.target.closest('[data-quick-model]');
    if (!button) return;
    if (quickModelContext === 'predictor') {
      state.predictorModel = button.dataset.quickModel;
      state.predictorTeam = null;
      setPressed(elements.predictorModelTabs, 'predictorModel', state.predictorModel);
      renderPredictor();
    } else {
      selectLeaderboardModel(button.dataset.quickModel);
      renderMatchup();
    }
    closeQuickModel();
    updateQuickModel();
  });

  document.addEventListener('click', function (event) {
    if (!elements.quickModel.contains(event.target)) closeQuickModel();
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') closeQuickModel();
  });
  window.addEventListener('scroll', queueQuickModelUpdate, { passive: true });
  window.addEventListener('resize', queueQuickModelUpdate);

  elements.matchupModelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-matchup-model]');
    if (!button || button.dataset.matchupModel === state.model) return;
    state.model = button.dataset.matchupModel;
    state.expanded = false;
    state.visibleRows = 0;
    setPressed(elements.modelTabs, 'model', state.model);
    syncData();
  });

  elements.matchupA.addEventListener('change', function () {
    var previous = state.matchupA;
    state.matchupA = elements.matchupA.value;
    if (state.matchupA === state.matchupB) state.matchupB = previous;
    renderMatchup();
  });

  elements.matchupB.addEventListener('change', function () {
    var previous = state.matchupB;
    state.matchupB = elements.matchupB.value;
    if (state.matchupA === state.matchupB) state.matchupA = previous;
    renderMatchup();
  });

  elements.matchupSwap.addEventListener('click', function () {
    var first = state.matchupA;
    state.matchupA = state.matchupB;
    state.matchupB = first;
    if (state.matchupVenue === 'a') state.matchupVenue = 'b';
    else if (state.matchupVenue === 'b') state.matchupVenue = 'a';
    renderMatchup();
  });

  elements.matchupVenue.addEventListener('change', function () {
    state.matchupVenue = elements.matchupVenue.value;
    renderMatchup();
  });

  window.addEventListener('pageshow', function () {
    if (state.manifest && state.datasets[state.sport]) renderMatchup();
  });

  elements.protocolSportTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-protocol-sport]');
    if (!button || button.dataset.protocolSport === state.sport) return;
    state.sport = button.dataset.protocolSport;
    state.selected = null;
    state.pinned = [];
    state.expanded = false;
    state.visibleRows = 0;
    state.includeProvisional = false;
    state.matchupA = null;
    state.matchupB = null;
    state.matchupVenue = 'neutral';
    setPressed(elements.sportTabs, 'sport', state.sport);
    populateCompetitions();
    syncData();
  });

  elements.protocolModelTabs.addEventListener('click', function (event) {
    var button = event.target.closest('[data-protocol-model]');
    if (!button || button.dataset.protocolModel === state.model) return;
    state.model = button.dataset.protocolModel;
    state.expanded = false;
    state.visibleRows = 0;
    state.includeProvisional = false;
    setPressed(elements.modelTabs, 'model', state.model);
    syncData();
  });

  elements.competition.addEventListener('change', function () {
    state.competition = elements.competition.value;
    state.expanded = false;
    state.visibleRows = 0;
    renderMetrics();
    renderMovers();
    renderTable();
    renderDetail();
  });

  elements.search.addEventListener('input', function () {
    state.query = elements.search.value;
    state.expanded = false;
    state.visibleRows = 0;
    renderMetrics();
    renderMovers();
    renderTable();
  });

  elements.includeProvisional.addEventListener('change', function () {
    setIncludeProvisional(elements.includeProvisional.checked);
  });

  elements.more.addEventListener('click', function () {
    if (window.matchMedia('(max-width: 650px)').matches) {
      state.visibleRows = Math.max(state.visibleRows, 12) + 12;
      state.expanded = state.visibleRows >= currentRows().length;
    } else {
      state.expanded = true;
    }
    renderTable();
  });

  elements.body.addEventListener('click', function (event) {
    var profile = event.target.closest('[data-open-profile]');
    if (profile) {
      state.selected = profile.dataset.openProfile;
      renderDetail();
      revealDetailOnMobile();
      return;
    }
    var target = event.target.closest('[data-select], [data-row-select]');
    if (!target) return;
    var selectedId = target.dataset.select || target.dataset.rowSelect;
    state.selected = window.matchMedia('(max-width: 650px)').matches && state.selected === selectedId ? null : selectedId;
    renderTable();
    renderDetail();
    if (!window.matchMedia('(max-width: 650px)').matches) revealDetailOnMobile();
  });

  elements.movers.addEventListener('click', function (event) {
    var button = event.target.closest('[data-select]');
    if (!button) return;
    state.selected = button.dataset.select;
    renderTable();
    renderDetail();
    revealDetailOnMobile();
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
    var histogram = event.target.closest('[data-histogram]');
    if (histogram) histogram.closest('.rating-lab-distribution').querySelector('.rating-lab-histogram-readout').textContent = histogram.dataset.histogram;
  });

  elements.detail.addEventListener('pointerdown', function (event) {
    var surface = event.target.closest('[data-chart-surface]');
    if (!surface) return;
    surface.dataset.scrubbing = 'true';
    if (surface.setPointerCapture) surface.setPointerCapture(event.pointerId);
    surface.focus();
    scrubChart(event);
  });

  elements.detail.addEventListener('pointermove', function (event) {
    var surface = event.target.closest('[data-chart-surface]');
    if (!surface) return;
    if (event.pointerType === 'mouse' || surface.dataset.scrubbing === 'true') scrubChart(event);
  });

  elements.detail.addEventListener('pointerup', function (event) {
    var surface = event.target.closest('[data-chart-surface]');
    if (surface) delete surface.dataset.scrubbing;
  });

  elements.detail.addEventListener('pointercancel', function (event) {
    var surface = event.target.closest('[data-chart-surface]');
    if (surface) delete surface.dataset.scrubbing;
  });

  elements.detail.addEventListener('keydown', function (event) {
    var surface = event.target.closest('[data-chart-surface]');
    if (!surface || ['ArrowLeft', 'ArrowRight', 'Home', 'End'].indexOf(event.key) === -1) return;
    event.preventDefault();
    var chartWrap = surface.closest('.rating-lab-chart-wrap');
    var dates = chartEntries(chartWrap).map(function (entry) { return entry.date; }).filter(function (date, index, items) {
      return items.indexOf(date) === index;
    }).sort();
    var current = dates.indexOf(surface.dataset.activeDate);
    if (current < 0 && surface.dataset.activeDate) {
      var activeTime = new Date(surface.dataset.activeDate).getTime();
      current = dates.reduce(function (nearest, date, index) {
        return Math.abs(new Date(date).getTime() - activeTime) < Math.abs(new Date(dates[nearest]).getTime() - activeTime) ? index : nearest;
      }, 0);
    }
    if (event.key === 'Home') current = 0;
    else if (event.key === 'End') current = dates.length - 1;
    else if (event.key === 'ArrowLeft') current = current < 0 ? dates.length - 1 : Math.max(0, current - 1);
    else current = current < 0 ? 0 : Math.min(dates.length - 1, current + 1);
    selectChartDate(chartWrap, dates[current]);
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

  elements.predictorPerformanceChart.addEventListener('click', function (event) {
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

  function revealLinkedMethod() {
    if (!window.location.hash) return;
    var target = document.getElementById(decodeURIComponent(window.location.hash.slice(1)));
    var disclosure = target && target.closest('.rating-lab-disclosure');
    if (disclosure) disclosure.open = true;
  }

  window.addEventListener('hashchange', revealLinkedMethod);
  revealLinkedMethod();

  root.addEventListener('error', function (event) {
    if (event.target && event.target.matches && event.target.matches('[data-entity-image], [data-flag-image]')) {
      event.target.hidden = true;
    }
  }, true);

  fetchJson('manifest.json')
    .then(function (manifest) {
      state.manifest = manifest;
      return Promise.all(sports.map(loadSportCore));
    })
    .then(function () {
      return Promise.all([
        ensureRankings(state.sport, 'elo'),
        state.model === 'elo' ? null : ensureRankings(state.sport, state.model)
      ]);
    })
    .then(function () {
      var competitions = predictorCompetitions();
      elements.predictorCompetition.innerHTML = competitions.map(function (view) {
        var competition = view.competition;
        return '<option value="' + escapeHtml(competition.id) + '"' + (competition.id === competitions[0].competition.id ? ' selected' : '') + '>' +
          escapeHtml(stateLabel(competitionState(competition)) + ' · ' + competitionTitle(competition)) + '</option>';
      }).join('');
      state.predictorCompetition = competitions[0].competition.id;
      populateCompetitions();
      render();
    })
    .catch(function (error) {
      elements.freshness.hidden = true;
      elements.error.hidden = false;
      elements.error.textContent = error.message + ' Please try again later.';
    });
}());
