---
layout: mat101
title: MAT101
permalink: /mat101/seances/
description: "Les 19 séances MAT101 du groupe IMA02 : compétences, parcours dans le polycopié, exercices et questions de sortie."
math: true
---

{% assign sessions = site.data.mat101_sessions %}

<div class="mat101-library mat101-course" data-mat101-course>
  <header class="mat101-page-heading">
    <h1>Séances MAT101</h1>
  </header>

  <p class="mat101-session-notice">Partiel prévu la semaine du 20 octobre.</p>

  <section class="mat101-session-browser" id="seances" aria-labelledby="mat101-session-browser-title">
    <div class="mat101-session-browser-heading">
      <div>
        <h2 id="mat101-session-browser-title">Séances</h2>
      </div>
      <p id="mat101-session-count" aria-live="polite">19 séances affichées</p>
    </div>

    <label class="mat101-session-search">
      <span>Rechercher un thème, une compétence ou un numéro</span>
      <input id="mat101-session-search-input" type="search" inputmode="search" placeholder="Par exemple : récurrence, module, séance 14…" autocomplete="off">
    </label>

    <div class="mat101-session-filters" aria-label="Filtrer les séances par bloc">
      <button class="mat101-session-filter is-active" type="button" data-mat101-session-filter="" aria-pressed="true">Tout <span>19</span></button>
      <button class="mat101-session-filter" type="button" data-mat101-session-filter="complexes" aria-pressed="false">Nombres complexes <span>9</span></button>
      <button class="mat101-session-filter" type="button" data-mat101-session-filter="langage" aria-pressed="false">Ensembles et logique <span>9</span></button>
      <button class="mat101-session-filter" type="button" data-mat101-session-filter="synthese" aria-pressed="false">Synthèse <span>1</span></button>
    </div>
  </section>

  <p id="mat101-session-no-results" class="mat101-session-no-results" hidden>
    <strong>Aucune séance trouvée.</strong>
    <span>Essayez un thème comme « quantificateurs » ou un numéro de 1 à 19.</span>
  </p>

  <ol class="mat101-session-grid" aria-label="Les 19 séances MAT101">
    {% for session in sessions %}
      <li
        class="mat101-session-card"
        data-mat101-session-card
        data-session-number="{{ session.number }}"
        data-session-block="{{ session.block }}"
        data-session-search="séance {{ session.number }} {{ session.search | escape }}"
      >
        <a href="{{ session.url | relative_url }}">
          <header>
            <span class="mat101-session-number">{{ session.number }}</span>
            <div>
              <p>{{ session.blockLabel }}</p>
              <h3>{{ session.shortTitle }}</h3>
            </div>
            {% if session.scheduleConfirmed %}
              <span class="mat101-session-date-state">Planifiée</span>
            {% else %}
              <span class="mat101-session-date-state is-pending">À confirmer</span>
            {% endif %}
          </header>
          <p class="mat101-session-date">{{ session.dateLabel }}</p>
          <ul>
            {% for skill in session.skillsPlain limit: 3 %}
              <li>{{ skill }}</li>
            {% endfor %}
          </ul>
          <footer>
            <span>Compétences · exercices · questions</span>
            <strong>Voir la séance <span aria-hidden="true">→</span></strong>
          </footer>
        </a>
      </li>
    {% endfor %}
  </ol>
</div>
