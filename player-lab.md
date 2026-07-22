---
layout: page
title: Historical Player Lab
permalink: /rating-lab/players/
description: Outcome-only historical men's and women's football player ratings from complete StatsBomb lineups using Lineup TrueSkill and RAPM.
---

<div class="rating-lab player-lab" data-player-data="{{ '/assets/data/rating-lab/player-football.json' | relative_url }}" data-flag-root="{{ '/assets/vendor/flag-icons/4x3' | relative_url }}">
  <header class="rating-lab-hero player-lab-hero">
    <p class="rating-lab-kicker">Historical men's and women's football player contribution</p>
    <h1>What changed when they played?</h1>
    <p class="rating-lab-deck">Two outcome-only models distribute team results across the players who were actually on the pitch. No passes, shots, expected goals, or tracking data enter either rating.</p>
    <p class="player-lab-back"><a href="{{ '/rating-lab/' | relative_url }}">← Back to Rating Lab</a></p>
  </header>

  <div id="player-lab-error" class="rating-lab-notice rating-lab-notice-error" role="alert" hidden></div>
  <noscript>This player leaderboard requires JavaScript.</noscript>

  <section class="player-lab-explorer" aria-labelledby="player-ranking-heading">
    <div class="rating-lab-section-heading">
      <div>
        <p class="rating-lab-kicker">Complete competitions only</p>
        <h2 id="player-ranking-heading">Historical player ratings</h2>
      </div>
      <p id="player-lab-generated">Loading the verified cohort…</p>
    </div>

    <details class="player-lab-boundary" id="player-scope" open>
      <summary>Verified cohorts and rating scope</summary>
      <p><strong>Men’s and women’s competitions pass the same evidence gates.</strong> These ratings apply only inside the selected competition. The men’s publication covers UEFA Euro 2024 and the 2022 FIFA World Cup; the women’s publication retains Liga F and the WSL 2023/24. The live five-league feed remains excluded until its lineup coverage passes the same gates.</p>
    </details>

    <div class="player-lab-toolbar">
      <label class="rating-lab-field">
        <span>Competition</span>
        <select id="player-cohort"></select>
      </label>
      <div class="rating-lab-control-group" aria-label="Player contribution model">
        <span class="rating-lab-control-label">Model</span>
        <div class="rating-lab-segmented" id="player-model-tabs">
          <button type="button" data-player-model="lineup-trueskill" aria-pressed="true">Lineup TrueSkill</button>
          <button type="button" data-player-model="rapm" aria-pressed="false">RAPM</button>
        </div>
      </div>
      <label class="rating-lab-field">
        <span>Find a player</span>
        <input id="player-search" type="search" autocomplete="off" placeholder="Player, club or nationality">
      </label>
    </div>

    <div class="rating-lab-quick-model player-lab-quick-model" id="player-quick-model" hidden>
      <div class="rating-lab-quick-model-menu" id="player-quick-model-menu" role="group" aria-label="Choose the player model">
        <button type="button" data-player-quick-model="lineup-trueskill">Lineup TrueSkill</button>
        <button type="button" data-player-quick-model="rapm">RAPM</button>
      </div>
    </div>

    <div class="rating-lab-metrics player-lab-metrics" id="player-metrics" aria-label="Cohort and model evidence"></div>

    <section class="player-lab-comparison" aria-labelledby="player-comparison-heading">
      <div class="player-lab-comparison-heading">
        <div>
          <p class="rating-lab-kicker">Agreement and disagreement</p>
          <h3 id="player-comparison-heading">Lineup TrueSkill versus RAPM</h3>
        </div>
        <p>Each axis is standardized within this competition. Flags show the source-listed nationality; upper-right players rate highly under both protocols.</p>
      </div>
      <div id="player-comparison-chart"></div>
    </section>

    <div class="player-lab-grid">
      <div class="rating-lab-table-wrap">
        <div class="player-lab-list-head">
          <div><span>Leaderboard</span><strong id="player-list-status">Loading players…</strong></div>
          <button type="button" id="player-filters-return">Filters ↑</button>
        </div>
        <table class="rating-lab-table player-lab-table">
          <caption id="player-ranking-caption">Eligible historical players</caption>
          <thead>
            <tr>
              <th scope="col">Rank</th>
              <th scope="col">Player</th>
              <th scope="col" id="player-score-heading">Conservative score</th>
              <th scope="col">Uncertainty</th>
              <th scope="col" class="rating-lab-optional">Minutes</th>
              <th scope="col" class="rating-lab-optional">Matches</th>
            </tr>
          </thead>
          <tbody id="player-ranking-body"></tbody>
        </table>
        <p id="player-ranking-empty" class="rating-lab-empty" hidden>No eligible player matches this search.</p>
        <button type="button" id="player-ranking-more" class="rating-lab-more" hidden>Show all players</button>
      </div>
      <aside class="rating-lab-detail player-lab-detail" id="player-detail" aria-live="polite" aria-label="Selected player comparison">
        <p class="rating-lab-detail-placeholder">Choose a player to compare both protocols.</p>
      </aside>
    </div>
  </section>

  <section class="player-lab-audit" aria-labelledby="player-audit-heading">
    <p class="rating-lab-kicker">Publication gates</p>
    <h2 id="player-audit-heading">Why these seasons are included</h2>
    <div class="player-lab-gates" id="player-gates"></div>

    <details class="rating-lab-limitations" id="player-methods" open>
      <summary>Exact interpretation and limitations</summary>
      <div class="player-lab-method-copy">
        <article>
          <h3>Lineup TrueSkill</h3>
          <p>Each player has a Gaussian skill belief. Team performance is the normalized minutes-weighted sum of the players’ performances. The match result updates every player after its probability is recorded. Publication uses <span class="rating-lab-formula">mean − 3 × uncertainty</span>.</p>
        </article>
        <article>
          <h3>RAPM</h3>
          <p>Match goal difference is regressed on normalized minutes for every player, with positive weights for the home side and negative weights for the away side. Ridge shrinkage is selected on the chronological final quarter. Publication uses <span class="rating-lab-formula">impact − 1.96 × uncertainty</span>.</p>
        </article>
      </div>
      <ul>
        <li>These are within-competition associations with team outcomes, not portable estimates of intrinsic talent.</li>
        <li>Players who repeatedly share the pitch remain hard to separate; ridge shrinkage and uncertainty expose rather than eliminate that problem.</li>
        <li>Lineup timestamps that overlap slightly around stoppage-time substitutions are normalized to eleven player-equivalents per side.</li>
        <li>Ratings cannot explain how a player contributed. No event or tracking surrogate is used.</li>
        <li>A match still level after extra time counts as a draw; a penalty shootout does not rewrite the preceding on-pitch result.</li>
        <li>Players need at least 450 minutes and five appearances to be ranked.</li>
      </ul>
      <div class="rating-lab-downloads">
        <a href="{{ '/assets/data/rating-lab/player-football.json' | relative_url }}" download>Player data JSON</a>
        <a href="{{ '/assets/data/rating-lab/player-schema.json' | relative_url }}" download>Player JSON schema</a>
        <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/blob/main/rating_lab/player_pipeline.py">Pipeline source</a>
        <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/blob/main/rating_lab/player_models.py">Model source</a>
      </div>
    </details>

    <div class="player-lab-attribution">
      <img src="https://raw.githubusercontent.com/statsbomb/public-images/master/statsbomb_logo_email_new.jpg" alt="StatsBomb">
      <p><strong>Sources are declared per competition.</strong> StatsBomb Open Data supplies the existing historical cohorts. World Cup 2026 is published only after <a href="https://www.api-football.com/">API-Football</a> passes the same completeness gates for all 104 matches. Under the <a href="https://api-sports.io/terms">provider terms</a>, responses stay in the private build cache; the public payload contains derived ratings, audit coverage, retrieval metadata, and a response snapshot hash.</p>
    </div>
  </section>
</div>

<script defer src="{{ '/assets/js/player-lab.js' | relative_url }}?v={{ site.github.build_revision }}"></script>
