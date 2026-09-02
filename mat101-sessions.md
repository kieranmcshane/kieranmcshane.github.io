---
layout: page
title: MAT101
permalink: /mat101/seances/
description: "Les 19 séances MAT101 du groupe IMA02 : compétences, parcours dans le polycopié, exercices et tickets de sortie."
math: true
---

{% assign sessions = site.data.mat101_sessions %}
{% assign student_workbook_url = '/assets/documents/mat101/parcours-19-seances-mat101-ima02.pdf' | relative_url %}

<div class="mat101-library mat101-course" data-mat101-course>
  <header class="mat101-hero mat101-course-hero">
    <p class="mat101-kicker">MAT101 · IMA02 · automne 2026</p>
    <h1>19 séances pour progresser en MAT101</h1>
    <p>Retrouvez pour chaque cours-TD les compétences à acquérir, les pages du polycopié, les exercices à travailler et le ticket de sortie.</p>
    <div class="mat101-actions">
      <a class="mat101-primary-action" href="#seances">Choisir une séance <span aria-hidden="true">↓</span></a>
      <a href="{{ '/mat101/exercices/' | relative_url }}">Les 103 exercices</a>
      <a href="{{ student_workbook_url }}">Feuille de route · PDF</a>
    </div>
  </header>

  <section class="mat101-session-browser" id="seances" aria-labelledby="mat101-session-browser-title">
    <div class="mat101-session-browser-heading">
      <div>
        <p class="mat101-kicker">Parcours chronologique</p>
        <h2 id="mat101-session-browser-title">Retrouver une séance</h2>
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
            <span>Compétences · exercices · ticket</span>
            <strong>Voir la séance <span aria-hidden="true">→</span></strong>
          </footer>
        </a>
      </li>
    {% endfor %}
  </ol>

  <section class="mat101-stats" aria-label="Structure du parcours MAT101">
    <div><strong>19</strong><span>séances complètes</span></div>
    <div><strong>90 min</strong><span>par cours-TD</span></div>
    <div><strong>2</strong><span>chapitres préparés</span></div>
    <div><strong>17 + 2</strong><span>créneaux fixés + à confirmer</span></div>
  </section>

  <aside class="mat101-course-status" aria-label="Statut du parcours">
    <div>
      <span class="mat101-status-dot" aria-hidden="true"></span>
      <strong>Les 19 parcours étudiants sont disponibles</strong>
      <span>La date et la salle des séances 18 et 19 restent à confirmer.</span>
    </div>
    <p><strong>Version étudiante.</strong> Chaque page va directement aux compétences, au travail proposé et au ticket de sortie.</p>
  </aside>

  <section class="mat101-course-download" aria-labelledby="mat101-course-download-title">
    <div>
      <p class="mat101-kicker">À garder sous la main</p>
      <h2 id="mat101-course-download-title">La feuille de route des 19 séances</h2>
      <p>Le PDF rassemble les compétences, le parcours d’exercices et le ticket de sortie de chaque séance. Les dates 18 et 19 y restent explicitement à confirmer.</p>
    </div>
    <a href="{{ student_workbook_url }}">Télécharger le PDF étudiant <span aria-hidden="true">↓</span></a>
  </section>
</div>
