(function () {
  'use strict';

  var STORAGE_KEY = 'mat101-owner-github-token';
  var library = document.querySelector('[data-mat101-owner-access]');
  if (!library) return;

  var clientId = (library.dataset.ownerClientId || '').trim();
  var allowedLogins = (library.dataset.ownerLogins || '')
    .split(',')
    .map(function (value) {
      return value.trim().toLowerCase();
    })
    .filter(Boolean);
  var solutionsUrl = library.dataset.ownerSolutionsUrl || '';
  var panel = document.getElementById('mat101-owner-access-panel');
  var status = document.getElementById('mat101-owner-access-status');
  var loginButton = document.getElementById('mat101-owner-login');
  var logoutButton = document.getElementById('mat101-owner-logout');
  var devicePrompt = document.getElementById('mat101-owner-device-prompt');
  var ownerDownloads = document.getElementById('mat101-owner-downloads');
  var ownerCredits = document.getElementById('mat101-owner-credits');

  function setStatus(message) {
    if (!status) return;
    status.textContent = message;
  }

  function typeset(nodes) {
    if (!window.MathJax || !MathJax.typesetPromise) {
      return Promise.resolve();
    }
    return MathJax.typesetPromise(nodes || undefined);
  }

  function createSolutionBlock(html) {
    var details = document.createElement('details');
    details.className = 'mat101-native-solution mat101-owner-solution';

    var summary = document.createElement('summary');
    var title = document.createElement('span');
    title.textContent = 'Afficher le corrigé détaillé';
    var subtitle = document.createElement('small');
    subtitle.textContent = 'Solution non officielle · niveau L1 · accès éditeur';
    summary.appendChild(title);
    summary.appendChild(subtitle);

    var body = document.createElement('div');
    body.className = 'mat101-solution-body';
    body.innerHTML = html;

    details.appendChild(summary);
    details.appendChild(body);
    return details;
  }

  function revealOwnerDownloads() {
    if (ownerDownloads) ownerDownloads.hidden = false;
    if (ownerCredits) ownerCredits.hidden = false;
  }

  function injectSolutions(solutionsById) {
    var injected = [];

    document.querySelectorAll('[data-mat101-exercise]').forEach(function (card) {
      if (card.querySelector('.mat101-native-solution')) return;

      var exerciseId = card.dataset.exerciseId;
      var html = solutionsById[exerciseId];
      if (!html) return;

      var content = card.querySelector('.mat101-native-content');
      var footer = content ? content.querySelector('.mat101-exercise-footer') : null;
      if (!content || !footer) return;

      var block = createSolutionBlock(html);
      content.insertBefore(block, footer);
      injected.push(block);
    });

    document.documentElement.classList.add('mat101-owner-unlocked');
    revealOwnerDownloads();
    return typeset(injected);
  }

  function updatePanel(loggedIn, loginName) {
    if (!panel) return;
    panel.hidden = !clientId;
    if (!clientId) return;

    if (loggedIn) {
      panel.dataset.state = 'unlocked';
      setStatus(
        loginName
          ? 'Accès éditeur actif pour @' + loginName + '. Tous les corrigés sont visibles sur cette page.'
          : 'Accès éditeur actif. Tous les corrigés sont visibles sur cette page.'
      );
      if (loginButton) loginButton.hidden = true;
      if (logoutButton) logoutButton.hidden = false;
      if (devicePrompt) devicePrompt.hidden = true;
      return;
    }

    panel.dataset.state = 'locked';
    setStatus(
      'Connectez votre compte GitHub autorisé pour afficher tous les corrigés sur cette page.'
    );
    if (loginButton) loginButton.hidden = false;
    if (logoutButton) logoutButton.hidden = true;
    if (devicePrompt) devicePrompt.hidden = true;
  }

  function fetchUser(token) {
    return fetch('https://api.github.com/user', {
      headers: {
        Accept: 'application/vnd.github+json',
        Authorization: 'Bearer ' + token,
        'X-GitHub-Api-Version': '2022-11-28',
      },
    }).then(function (response) {
      if (!response.ok) {
        throw new Error('auth');
      }
      return response.json();
    });
  }

  function loadSolutions() {
    return fetch(solutionsUrl, { credentials: 'same-origin' }).then(function (response) {
      if (!response.ok) {
        throw new Error('solutions');
      }
      return response.json();
    });
  }

  function unlockWithToken(token) {
    return fetchUser(token)
      .then(function (user) {
        var login = String(user.login || '').toLowerCase();
        if (!allowedLogins.includes(login)) {
          throw new Error('forbidden');
        }
        return loadSolutions().then(function (solutions) {
          localStorage.setItem(STORAGE_KEY, token);
          return injectSolutions(solutions).then(function () {
            updatePanel(true, user.login);
          });
        });
      });
  }

  function clearAccess() {
    localStorage.removeItem(STORAGE_KEY);
    document.documentElement.classList.remove('mat101-owner-unlocked');
    document.querySelectorAll('.mat101-owner-solution').forEach(function (node) {
      node.remove();
    });
    if (ownerDownloads) ownerDownloads.hidden = true;
    if (ownerCredits) ownerCredits.hidden = true;
    updatePanel(false);
  }

  function pollForToken(deviceCode, intervalSeconds) {
    return new Promise(function (resolve, reject) {
      var stopped = false;

      function poll() {
        if (stopped) return;

        fetch('https://github.com/login/oauth/access_token', {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            client_id: clientId,
            device_code: deviceCode,
            grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
          }),
        })
          .then(function (response) {
            return response.json();
          })
          .then(function (payload) {
            if (payload.error === 'authorization_pending') {
              window.setTimeout(poll, intervalSeconds * 1000);
              return;
            }
            if (payload.error) {
              stopped = true;
              reject(new Error(payload.error));
              return;
            }
            stopped = true;
            resolve(payload.access_token);
          })
          .catch(function (error) {
            stopped = true;
            reject(error);
          });
      }

      poll();
    });
  }

  function startDeviceFlow() {
    if (!clientId) return;

    setStatus('Demande du code GitHub en cours…');
    if (loginButton) loginButton.disabled = true;

    fetch('https://github.com/login/device/code', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        client_id: clientId,
        scope: 'read:user',
      }),
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (payload) {
        if (!payload.device_code || !payload.user_code || !payload.verification_uri) {
          throw new Error('device');
        }

        if (devicePrompt) {
          devicePrompt.hidden = false;
          devicePrompt.innerHTML =
            '<p>Ouvrez <a href="' +
            payload.verification_uri +
            '" target="_blank" rel="noopener noreferrer">' +
            payload.verification_uri +
            '</a> et saisissez le code <strong>' +
            payload.user_code +
            '</strong>.</p>';
        }
        setStatus('En attente de la validation GitHub…');

        return pollForToken(payload.device_code, payload.interval || 5).then(function (token) {
          return unlockWithToken(token);
        });
      })
      .catch(function (error) {
        if (error && error.message === 'forbidden') {
          setStatus('Ce compte GitHub n’est pas autorisé pour l’accès éditeur.');
        } else {
          setStatus('La connexion GitHub a échoué. Réessayez dans un instant.');
        }
      })
      .finally(function () {
        if (loginButton) loginButton.disabled = false;
      });
  }

  if (loginButton) {
    loginButton.addEventListener('click', startDeviceFlow);
  }
  if (logoutButton) {
    logoutButton.addEventListener('click', clearAccess);
  }

  updatePanel(false);

  var savedToken = localStorage.getItem(STORAGE_KEY);
  if (savedToken) {
    unlockWithToken(savedToken).catch(function () {
      clearAccess();
    });
  }
})();
