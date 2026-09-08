---
layout: mat101
title: Exercices MAT101
permalink: /mat101/exercices/
description: "Bibliothèque de 103 exercices MAT101 de niveau L1 avec énoncés lisibles directement en ligne."
math: true
---

{% assign statement_pdf_url = '/assets/documents/mat101/recueil-exercices-mat101.pdf' | relative_url %}
{% assign statement_tex_url = '/assets/documents/mat101/recueil-exercices-mat101.tex' | relative_url %}
{% assign statement_archive_url = '/assets/documents/mat101/recueil-exercices-mat101-sources.zip' | relative_url %}
{% assign solution_pdf_url = '/assets/documents/mat101/corrige-exercices-mat101.pdf' | relative_url %}
{% assign solution_tex_url = '/assets/documents/mat101/corrige-exercices-mat101.tex' | relative_url %}
{% assign solution_archive_url = '/assets/documents/mat101/corrige-exercices-mat101-sources.zip' | relative_url %}

<div class="mat101-library">
  <header class="mat101-page-heading">
    <h1>Exercices MAT101</h1>
    <nav class="mat101-page-links" aria-label="Autres ressources MAT101">
      <a href="{{ '/mat101/seances/' | relative_url }}">Séances</a>
      <a href="#informations">Informations</a>
      <a href="#errata">Errata</a>
      <a href="#telechargements">Téléchargements</a>
      <a href="#credits">Crédits</a>
    </nav>
  </header>

  {% include mat101-informations.html %}

  <div class="mat101-study-area" data-mat101-study-area>
    <nav class="mat101-toc" aria-label="Sommaire des exercices">
      <div class="mat101-toc-shell" data-mat101-toc>
      <p class="mat101-toc-status" id="mat101-toc-current" aria-live="polite">
        4 chapitres · 103 exercices
      </p>

      <div class="mat101-toc-panel">
        <div class="mat101-difficulty-legend" aria-label="Légende des niveaux de difficulté">
          <span><i class="mat101-level-dot mat101-level-essential" aria-hidden="true"></i>Essentiel</span>
          <span><i class="mat101-level-dot mat101-level-exam" aria-hidden="true"></i>Niveau examen</span>
          <span><i class="mat101-level-dot mat101-level-advanced" aria-hidden="true"></i>Approfondissement</span>
          <span><i class="mat101-level-dot mat101-level-mixed" aria-hidden="true"></i>Intermédiaire</span>
        </div>
        {% for chapter in site.data.mat101_exercises %}
          {% assign toc_chapter_exercises = site.data.mat101_native | where: "chapterId", chapter.id %}
          <section
            class="mat101-toc-chapter"
            data-mat101-toc-chapter
            data-chapter-id="{{ chapter.id }}"
          >
            <header>
              <a href="#{{ chapter.id }}" data-mat101-toc-chapter-link>
                <span>{{ chapter.number }}</span>
                <strong>{{ chapter.title }}</strong>
              </a>
              <small>{{ chapter.count }} exercices</small>
            </header>
            <div class="mat101-toc-exercises">
              {% for exercise in toc_chapter_exercises %}
                {% case exercise.difficulty %}
                  {% when "*" %}
                    {% assign difficulty_label = "notions essentielles" %}
                    {% assign difficulty_class = "essential" %}
                  {% when "**" %}
                    {% assign difficulty_label = "niveau généralement attendu à l’examen" %}
                    {% assign difficulty_class = "exam" %}
                  {% when "***" %}
                    {% assign difficulty_label = "approfondissement" %}
                    {% assign difficulty_class = "advanced" %}
                  {% else %}
                    {% assign difficulty_label = "niveau intermédiaire" %}
                    {% assign difficulty_class = "mixed" %}
                {% endcase %}
                <a
                  href="#exercice-{{ exercise.id | replace: '.', '-' }}"
                  data-mat101-toc-link
                  data-exercise-id="{{ exercise.id }}"
                  data-chapter-title="{{ chapter.title | escape }}"
                  aria-label="Exercice {{ exercise.id }} — {{ chapter.title }}{% if exercise.difficulty %} — {{ difficulty_label }}{% endif %}"
                >
                  <span>{{ exercise.id }}</span>
                  {% if exercise.difficulty %}
                    <i
                      class="mat101-level-dot mat101-level-{{ difficulty_class }}"
                      aria-hidden="true"
                      title="{{ difficulty_label }}"
                    ></i>
                  {% endif %}
                </a>
              {% endfor %}
            </div>
          </section>
        {% endfor %}
        </div>
      </div>
    </nav>

    <div class="mat101-study-content">

  <section class="mat101-browser" id="bibliotheque" aria-labelledby="mat101-browser-title">
    <div class="mat101-browser-heading">
      <div>
        <h2 id="mat101-browser-title">Trouver un exercice</h2>
      </div>
      <p id="mat101-result-count" aria-live="polite">103 exercices affichés</p>
    </div>
    <label class="mat101-search">
      <span>Rechercher dans les numéros, énoncés, chapitres ou notions</span>
      <input id="mat101-search-input" type="search" inputmode="search" placeholder="Par exemple : suite périodique, 2.14, injectivité…" autocomplete="off">
    </label>

    <details class="mat101-tag-index">
      <summary>
        <span>Index des notions</span>
        <small>{{ site.data.mat101_tags.tags.size }} mots-clés</small>
      </summary>
      <div class="mat101-tag-controls" aria-label="Filtrer les exercices par notion">
        <button class="mat101-tag-filter is-active" type="button" data-mat101-tag="" aria-pressed="true">
          Toutes les notions <span>103</span>
        </button>
        {% for tag in site.data.mat101_tags.tags %}
          <button class="mat101-tag-filter" type="button" data-mat101-tag="{{ tag.slug }}" aria-pressed="false">
            {{ tag.label }} <span>{{ tag.exercises.size }}</span>
          </button>
        {% endfor %}
      </div>
    </details>
  </section>

  <div id="mat101-no-results" class="mat101-no-results" hidden>
    <strong>Aucun exercice trouvé.</strong>
    <span>Essayez un numéro comme « 3.12 » ou un mot comme « fonctions ».</span>
  </div>

  {% for chapter in site.data.mat101_exercises %}
    {% assign chapter_exercises = site.data.mat101_native | where: "chapterId", chapter.id %}
    <section
      class="mat101-chapter"
      id="{{ chapter.id }}"
      data-mat101-chapter
      tabindex="-1"
    >
      <header>
        <span class="mat101-chapter-number">{{ chapter.number }}</span>
        <div>
          <h2>{{ chapter.title }}</h2>
          <p>{{ chapter.count }} exercices</p>
        </div>
      </header>

      <div class="mat101-native-list" aria-label="{% if site.mat101_show_solutions %}Exercices et solutions du chapitre {{ chapter.number }}{% else %}Exercices du chapitre {{ chapter.number }}{% endif %}">
        {% for exercise in chapter_exercises %}
          <details
            class="mat101-native-card"
            id="exercice-{{ exercise.id | replace: '.', '-' }}"
            data-mat101-exercise
            data-exercise-id="{{ exercise.id }}"
            data-tags="{% for tag in exercise.tags %}{{ tag.slug }}{% unless forloop.last %},{% endunless %}{% endfor %}"
            data-search="{{ exercise.id }} {{ exercise.chapterTitle | downcase }} {{ exercise.statementSearchText | escape }}{% for tag in exercise.tags %} {{ tag.label | downcase }}{% endfor %}"
          >
            <summary>
              <span class="mat101-exercise-summary-main">
                <span class="mat101-exercise-number">
                  <span>Exercice <strong>{{ exercise.id }}</strong></span>
                  {% if exercise.difficulty %}
                    {% case exercise.difficulty %}
                      {% when "*" %}
                        {% assign difficulty_label = "notions essentielles" %}
                        {% assign difficulty_class = "essential" %}
                      {% when "**" %}
                        {% assign difficulty_label = "niveau généralement attendu à l’examen" %}
                        {% assign difficulty_class = "exam" %}
                      {% when "***" %}
                        {% assign difficulty_label = "approfondissement" %}
                        {% assign difficulty_class = "advanced" %}
                      {% else %}
                        {% assign difficulty_label = "niveau intermédiaire" %}
                        {% assign difficulty_class = "mixed" %}
                    {% endcase %}
                    <span
                      class="mat101-difficulty mat101-difficulty-{{ difficulty_class }}"
                      aria-label="Difficulté : {{ difficulty_label }}"
                      title="Difficulté : {{ difficulty_label }}"
                    ><i class="mat101-level-dot mat101-level-{{ difficulty_class }}" aria-hidden="true"></i></span>
                  {% endif %}
                </span>
                <span class="mat101-exercise-tags" aria-label="Notions abordées">
                  {% for tag in exercise.tags %}
                    <span>{{ tag.label }}</span>
                  {% endfor %}
                  {% assign exercise_errata = site.data.mat101_errata | where: "exercise", exercise.id %}
                  {% if exercise_errata.size > 0 %}
                    <span
                      class="mat101-erratum-badge"
                      aria-label="Un erratum du document source est signalé pour l’exercice {{ exercise.id }}"
                    >Erratum source</span>
                  {% endif %}
                </span>
              </span>
              <span class="mat101-open-label">Lire l’énoncé</span>
            </summary>

            <div class="mat101-native-content">
              <section class="mat101-statement" aria-labelledby="statement-{{ exercise.id | replace: '.', '-' }}">
                <div class="mat101-content-heading">
                  <h3 id="statement-{{ exercise.id | replace: '.', '-' }}">Énoncé</h3>
                  <a href="{{ statement_pdf_url }}#page={{ exercise.statementPdfPage }}">Consulter la page source</a>
                </div>
                {{ exercise.statementHtml }}
              </section>

              {% if site.mat101_show_solutions %}
              <details class="mat101-native-solution">
                <summary>
                  <span>Afficher le corrigé détaillé</span>
                  <small>Solution non officielle · niveau L1</small>
                </summary>
                <div class="mat101-solution-body">
                  {{ exercise.solutionHtml }}
                </div>
              </details>
              {% elsif exercise.publicSolutionHtml %}
              <details class="mat101-native-solution">
                <summary>
                  <span>Afficher le corrigé détaillé</span>
                  <small>Solution non officielle · niveau L1</small>
                </summary>
                <div class="mat101-solution-body">
                  {{ exercise.publicSolutionHtml }}
                </div>
              </details>
              {% endif %}

              {% capture issue_title %}[MAT101 {{ exercise.id }}] Correction proposée{% endcapture %}
              <footer class="mat101-exercise-footer">
                <span>
                  <strong>Transcription mathématique relue</strong>
                  · Vérification effectuée sur le document source
                </span>
                <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/issues/new?template=mat101-correction.yml&amp;title={{ issue_title | url_encode }}">Signaler une erreur ou proposer une amélioration</a>
              </footer>
            </div>
          </details>
        {% endfor %}
      </div>
    </section>
  {% endfor %}

  <section class="mat101-community-review" aria-labelledby="mat101-review-title">
    <h2 id="mat101-review-title">Corrections</h2>
    <p>Les corrections sont publiques sur GitHub. Un compte gratuit est nécessaire pour en proposer une.</p>
    <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/issues/new?template=mat101-correction.yml">Proposer une correction</a>
    <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/issues?q=is%3Aissue%20MAT101">Consulter les corrections MAT101</a>
  </section>

  <section class="mat101-errata" id="errata" aria-labelledby="mat101-errata-title">
    <h2 id="mat101-errata-title">Errata du polycopié source</h2>
    <div class="mat101-errata-list">
      {% for erratum in site.data.mat101_errata %}
        <article id="erratum-{{ erratum.exercise | replace: '.', '-' }}">
          <header>
            <a href="#exercice-{{ erratum.exercise | replace: '.', '-' }}">Exercice {{ erratum.exercise }}</a>
            <span>{{ erratum.kind }}</span>
          </header>
          <div class="mat101-errata-change">
            <p><span>Avant</span> {{ erratum.problem }}</p>
            <p><span>Après</span> {{ erratum.correction }}</p>
          </div>
        </article>
      {% endfor %}
    </div>
  </section>
    </div>
  </div>

  <section class="mat101-downloads" id="telechargements" aria-labelledby="mat101-downloads-title">
    <div class="mat101-download-intro">
      <h2 id="mat101-downloads-title">Téléchargements</h2>
    </div>

    <div class="mat101-file-group">
      <p class="mat101-file-label">Énoncés originaux</p>
      <ul>
        <li><a href="{{ statement_pdf_url }}" download><strong>Recueil PDF</strong><span>103 exercices · 34 pages</span></a></li>
        <li><a href="{{ statement_tex_url }}" download><strong>Source LaTeX</strong><span>Sélection par <code>pdfpages</code></span></a></li>
        <li><a href="{{ statement_archive_url }}" download><strong>Archive complète</strong><span>LaTeX + PDF source</span></a></li>
      </ul>
    </div>

    {% if site.mat101_show_solutions %}
    <div class="mat101-file-group mat101-file-group-solution">
      <p class="mat101-file-label">Corrigé détaillé</p>
      <ul>
        <li><a href="{{ solution_pdf_url }}" download><strong>Corrigé PDF</strong><span>103 solutions · niveau L1</span></a></li>
        <li><a href="{{ solution_tex_url }}" download><strong>Source LaTeX autonome</strong><span>Un seul fichier compilable</span></a></li>
        <li><a href="{{ solution_archive_url }}" download><strong>Archive modulaire</strong><span>Fichier principal + 4 chapitres</span></a></li>
      </ul>
    </div>
    {% endif %}
  </section>

  <section class="mat101-credits" id="credits" aria-labelledby="mat101-credits-title">
    <p class="mat101-kicker" id="mat101-credits-title">Crédits</p>

    <div class="mat101-credit-grid">
      <article>
        <h3>Énoncés originaux</h3>
        <p><strong>Collectif MAT101, Université Grenoble Alpes.</strong> Polycopié du 13 septembre 2022.</p>
      </article>
      {% if site.mat101_show_solutions %}
      <article>
        <h3>Rédaction du corrigé</h3>
        <p><strong>Rédaction initiale assistée par OpenAI ChatGPT ; édition et publication par Kieran McShane, avec OpenAI Codex.</strong> Les encadrés « Idée et plan » s’inspirent de la méthode de George Pólya. Version du 27 juillet 2026. Il ne s’agit ni d’un corrigé officiel de l’UGA ni d’une validation institutionnelle.</p>
      </article>
      {% endif %}
    </div>

    <div class="mat101-rights-note">
      <p><strong>Source faisant autorité.</strong> Le recueil utilise l’édition fournie du 13 septembre 2022. Une <a href="https://www-fourier.univ-grenoble-alpes.fr/~rossigno/Enseignement/ens_files/mat_101_20221201.pdf">version institutionnelle datée du 1er décembre 2022</a> est hébergée par l’Institut Fourier.</p>
    </div>
  </section>
</div>
