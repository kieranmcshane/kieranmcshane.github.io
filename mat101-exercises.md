---
layout: page
title: Exercices et corrigés MAT101
permalink: /mat101/exercices/
description: "Bibliothèque de 103 exercices MAT101 de niveau L1 avec énoncés et corrigés détaillés lisibles directement en ligne."
math: true
---

{% assign statement_pdf_url = '/assets/documents/mat101/recueil-exercices-mat101.pdf' | relative_url %}
{% assign statement_tex_url = '/assets/documents/mat101/recueil-exercices-mat101.tex' | relative_url %}
{% assign statement_archive_url = '/assets/documents/mat101/recueil-exercices-mat101-sources.zip' | relative_url %}
{% assign solution_pdf_url = '/assets/documents/mat101/corrige-exercices-mat101.pdf' | relative_url %}
{% assign solution_tex_url = '/assets/documents/mat101/corrige-exercices-mat101.tex' | relative_url %}
{% assign solution_archive_url = '/assets/documents/mat101/corrige-exercices-mat101-sources.zip' | relative_url %}
{% assign bib_url = '/assets/documents/mat101/mat101-citations.bib' | relative_url %}

<div class="mat101-library">
  <header class="mat101-hero">
    <p class="mat101-kicker">MAT101 · bibliothèque L1</p>
    <h1>103 exercices à travailler ici</h1>
    <p>Chaque énoncé est lisible directement dans la page. Ouvrez ensuite son corrigé détaillé, sans quitter le site et sans chercher la bonne page dans un PDF.</p>
    <div class="mat101-actions">
      <a class="mat101-primary-action" href="#bibliotheque">Explorer les exercices <span aria-hidden="true">↓</span></a>
      <a href="#telechargements">Télécharger les recueils</a>
      <a href="#credits">Crédits et citations</a>
    </div>
  </header>

  <section class="mat101-stats" aria-label="Contenu de la bibliothèque">
    <div><strong>103</strong><span>énoncés en ligne</span></div>
    <div><strong>103</strong><span>corrigés rédigés</span></div>
    <div><strong>4</strong><span>chapitres</span></div>
    <div><strong>L1</strong><span>niveau</span></div>
  </section>

  <aside class="mat101-verification" aria-label="Statut du corrigé">
    <div>
      <span class="mat101-status-dot" aria-hidden="true"></span>
      <strong>Couverture complète</strong>
      <span>103 solutions sur 103</span>
    </div>
    <p><strong>Corrigé non officiel.</strong> Les énoncés sont des reproductions fidèles du polycopié MAT101 crédité ci-dessous. La rédaction initiale des solutions a été assistée par OpenAI ChatGPT ; aucune relecture mathématique humaine intégrale n’est encore attestée.</p>
  </aside>

  <nav class="mat101-chapter-nav" aria-label="Chapitres du recueil">
    {% for chapter in site.data.mat101_exercises %}
      <a href="#{{ chapter.id }}">
        <span>{{ chapter.number }}</span>
        <strong>{{ chapter.title }}</strong>
        <small>{{ chapter.count }} exercices corrigés</small>
      </a>
    {% endfor %}
  </nav>

  <aside class="mat101-reading-note">
    <strong>Mode d’emploi.</strong>
    Cherchez un numéro ou un thème, ouvrez l’exercice, puis tentez-le avant de révéler le corrigé. Dans le polycopié, (*) vérifie les notions essentielles, (**) correspond en général au niveau attendu à l’examen et (***) propose un approfondissement.
  </aside>

  <section class="mat101-browser" id="bibliotheque" aria-labelledby="mat101-browser-title">
    <div class="mat101-browser-heading">
      <div>
        <p class="mat101-kicker">Bibliothèque interactive</p>
        <h2 id="mat101-browser-title">Trouver un exercice</h2>
      </div>
      <p id="mat101-result-count" aria-live="polite">103 exercices affichés</p>
    </div>
    <label class="mat101-search">
      <span>Rechercher par numéro ou chapitre</span>
      <input id="mat101-search-input" type="search" inputmode="search" placeholder="Par exemple : 2.14, complexes, limites…" autocomplete="off">
    </label>
  </section>

  <div id="mat101-no-results" class="mat101-no-results" hidden>
    <strong>Aucun exercice trouvé.</strong>
    <span>Essayez un numéro comme « 3.12 » ou un mot comme « fonctions ».</span>
  </div>

  {% for chapter in site.data.mat101_exercises %}
    {% assign chapter_exercises = site.data.mat101_native | where: "chapterId", chapter.id %}
    <section class="mat101-chapter" id="{{ chapter.id }}" data-mat101-chapter>
      <header>
        <span class="mat101-chapter-number">{{ chapter.number }}</span>
        <div>
          <h2>{{ chapter.title }}</h2>
          <p>{{ chapter.count }} exercices</p>
        </div>
      </header>

      <div class="mat101-native-list" aria-label="Exercices et solutions du chapitre {{ chapter.number }}">
        {% for exercise in chapter_exercises %}
          <details
            class="mat101-native-card"
            id="exercice-{{ exercise.id | replace: '.', '-' }}"
            data-mat101-exercise
            data-search="{{ exercise.id }} {{ exercise.chapterTitle | downcase }}"
          >
            <summary>
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
                  >{{ exercise.difficulty }}</span>
                {% endif %}
              </span>
              <span class="mat101-open-label">Lire l’énoncé</span>
            </summary>

            <div class="mat101-native-content">
              <section class="mat101-statement" aria-labelledby="statement-{{ exercise.id | replace: '.', '-' }}">
                <div class="mat101-content-heading">
                  <h3 id="statement-{{ exercise.id | replace: '.', '-' }}">Énoncé</h3>
                  <span>Reproduction fidèle du document source</span>
                </div>
                {% for statement_image in exercise.statementImages %}
                  <img
                    src="{{ statement_image | relative_url }}"
                    alt="Énoncé de l’exercice MAT101 {{ exercise.id }}{% if exercise.statementImages.size > 1 %}, partie {{ forloop.index }} sur {{ exercise.statementImages.size }}{% endif %}"
                    loading="lazy"
                    decoding="async"
                  >
                {% endfor %}
              </section>

              <details class="mat101-native-solution">
                <summary>
                  <span>Afficher le corrigé détaillé</span>
                  <small>Solution non officielle · niveau L1</small>
                </summary>
                <div class="mat101-solution-body">
                  {{ exercise.solutionHtml }}
                </div>
              </details>

              {% capture issue_title %}[MAT101 {{ exercise.id }}] Correction proposée{% endcapture %}
              <footer class="mat101-exercise-footer">
                <span>Énoncé : Collectif MAT101, UGA (2022) · Corrigé : K. McShane, assistance ChatGPT/Codex (2026)</span>
                <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/issues/new?template=mat101-correction.yml&amp;title={{ issue_title | url_encode }}">Signaler une erreur ou proposer une amélioration</a>
              </footer>
            </div>
          </details>
        {% endfor %}
      </div>
    </section>
  {% endfor %}

  <section class="mat101-community-review" aria-labelledby="mat101-review-title">
    <p class="mat101-kicker">Relecture ouverte</p>
    <h2 id="mat101-review-title">Un ticket précis pour chaque correction</h2>
    <p>Les remarques sont traitées publiquement dans GitHub : exercice concerné, passage exact, justification et proposition. Ce registre simple est mieux adapté ici qu’un système de votes de type Community Notes : une correction mathématique doit être vérifiable, attribuée et reliée à une version précise.</p>
    <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/issues/new?template=mat101-correction.yml">Ouvrir un ticket de correction</a>
    <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/issues?q=is%3Aissue%20MAT101">Consulter les tickets MAT101</a>
  </section>

  <section class="mat101-downloads" id="telechargements">
    <div class="mat101-download-intro">
      <p class="mat101-kicker">Fichiers complémentaires</p>
      <h2>Lire hors ligne ou recompiler</h2>
      <p>La bibliothèque ci-dessus est la lecture principale. Les PDF et les sources LaTeX restent disponibles pour l’impression, l’archivage et la réutilisation personnelle.</p>
    </div>

    <div class="mat101-file-group">
      <p class="mat101-file-label">Énoncés originaux</p>
      <ul>
        <li><a href="{{ statement_pdf_url }}" download><strong>Recueil PDF</strong><span>103 exercices · 34 pages</span></a></li>
        <li><a href="{{ statement_tex_url }}" download><strong>Source LaTeX</strong><span>Sélection par <code>pdfpages</code></span></a></li>
        <li><a href="{{ statement_archive_url }}" download><strong>Archive complète</strong><span>LaTeX + PDF source</span></a></li>
      </ul>
    </div>

    <div class="mat101-file-group mat101-file-group-solution">
      <p class="mat101-file-label">Corrigé détaillé</p>
      <ul>
        <li><a href="{{ solution_pdf_url }}" download><strong>Corrigé PDF</strong><span>103 solutions · 57 pages</span></a></li>
        <li><a href="{{ solution_tex_url }}" download><strong>Source LaTeX autonome</strong><span>Un seul fichier compilable</span></a></li>
        <li><a href="{{ solution_archive_url }}" download><strong>Archive modulaire</strong><span>Fichier principal + 4 chapitres</span></a></li>
      </ul>
    </div>
  </section>

  <section class="mat101-credits" id="credits" aria-labelledby="mat101-credits-title">
    <p class="mat101-kicker">Crédits, citation et transparence</p>
    <h2 id="mat101-credits-title">Qui a produit quoi ?</h2>

    <div class="mat101-credit-grid">
      <article>
        <h3>Énoncés originaux</h3>
        <p><strong>Collectif MAT101, Université Grenoble Alpes.</strong> Le polycopié cite notamment Bernard Ycart, Agnès Coquio, Éric Dumas, Emmanuel Peyre, Pierre Dehornoy et Raphaël Rossignol, « et d’autres ». Raphaël Rossignol est indiqué comme responsable de l’édition du 13 septembre 2022.</p>
      </article>
      <article>
        <h3>Adaptation web et interface</h3>
        <p><strong>Kieran McShane, avec l’assistance d’OpenAI Codex.</strong> Découpe fidèle des énoncés depuis le document source, indexation des 103 exercices, conversion du corrigé LaTeX en contenu web, correspondance énoncé–corrigé, conception et publication de l’interface.</p>
      </article>
      <article>
        <h3>Rédaction du corrigé</h3>
        <p><strong>Rédaction initiale assistée par OpenAI ChatGPT ; édition et publication par Kieran McShane, avec OpenAI Codex.</strong> Version du 27 juillet 2026. Il ne s’agit ni d’un corrigé officiel de l’UGA ni d’une validation institutionnelle.</p>
      </article>
    </div>

    <div class="mat101-review-ledger">
      <strong>Contrôles effectués avant publication</strong>
      <ul>
        <li>103 énoncés complets, y compris les exercices répartis sur plusieurs pages ;</li>
        <li>103 blocs de solutions distincts, de 1.1 à 4.17, rendus directement dans la page ;</li>
        <li>correspondance des quatre chapitres, numéros et fichiers sources ;</li>
        <li>crédits, statut non officiel et formulaire public de rectification intégrés.</li>
      </ul>
      <p><strong>Limite actuelle :</strong> ces contrôles portent sur l’exhaustivité, la structure et la provenance ; ils ne constituent pas une vérification indépendante de chaque démonstration.</p>
    </div>

    <details class="mat101-citation">
      <summary>Citations bibliographiques recommandées</summary>
      <p><cite>Collectif MAT101, <em>Langage mathématique, algèbre et géométrie élémentaires</em>, UE MAT101, Université Grenoble Alpes, édition du 13 septembre 2022. Responsable de l’édition citée : Raphaël Rossignol.</cite></p>
      <p><cite>Kieran McShane (éd.), <em>Recueil des exercices MAT101</em>, sélection, indexation et interface web, 2026, d’après le polycopié collectif MAT101 de l’Université Grenoble Alpes, avec l’assistance d’OpenAI Codex.</cite></p>
      <p><cite>Kieran McShane (éd.), <em>Corrigé détaillé des exercices MAT101</em>, rédaction initiale assistée par OpenAI ChatGPT, édition et publication avec l’assistance d’OpenAI Codex, version du 27 juillet 2026, corrigé non officiel.</cite></p>
      <a href="{{ bib_url }}" download>Télécharger les trois références BibTeX</a>
    </details>

    <div class="mat101-rights-note">
      <p><strong>Source faisant autorité.</strong> Le recueil utilise l’édition fournie du 13 septembre 2022. Une <a href="https://www-fourier.univ-grenoble-alpes.fr/~rossigno/Enseignement/ens_files/mat_101_20221201.pdf">version institutionnelle datée du 1er décembre 2022</a> est hébergée par l’Institut Fourier.</p>
      <p><strong>Droits et rectifications.</strong> Aucune licence de réutilisation explicite n’a été identifiée dans le PDF du 13 septembre 2022 ; les droits sur les pages originales restent attachés à leurs titulaires. Cette sélection éducative et son corrigé non officiel ne constituent pas une publication de l’UGA. Toute demande d’attribution, de rectification ou de retrait peut être déposée dans le registre public ci-dessus ou adressée via la <a href="{{ '/about/#contact' | relative_url }}">page de contact</a>.</p>
    </div>
  </section>
</div>
