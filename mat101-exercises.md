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
      <strong>Corpus complet — relecture en cours</strong>
      <span>103 énoncés et 103 corrections présents</span>
    </div>
    <p><strong>Corrigé non officiel.</strong> Les énoncés sont proposés sous forme de transcriptions textuelles sélectionnables, d’après le polycopié MAT101 crédité ci-dessous. La rédaction initiale des solutions a été assistée par OpenAI ChatGPT ; la vérification indépendante exercice par exercice n’est pas achevée.</p>
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
    Cherchez un numéro, un mot de l’énoncé ou un thème, ouvrez l’exercice, puis tentez-le avant de révéler le corrigé. Dans le polycopié, (*) vérifie les notions essentielles, (**) correspond en général au niveau attendu à l’examen et (***) propose un approfondissement. Le repère (*/**) signale un exercice à la frontière entre notions essentielles et niveau examen.
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
                    >{{ exercise.difficulty }}</span>
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
                <span>
                  {% if exercise.transcriptionStatus == 'curated' %}
                    <strong>Transcription mathématique relue</strong>
                  {% else %}
                    <strong>Transcription textuelle extraite</strong>
                  {% endif %}
                  ·
                  {% if exercise.mathematicalReviewStatus == 'reviewed' %}
                    Vérification effectuée sur le document source
                  {% else %}
                    Relecture mathématique indépendante en attente
                  {% endif %}
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
    <p class="mat101-kicker">Relecture ouverte</p>
    <h2 id="mat101-review-title">Un ticket précis pour chaque correction</h2>
    <p>Les remarques sont traitées publiquement dans GitHub : exercice concerné, passage exact, justification et proposition. Ce registre simple est mieux adapté ici qu’un système de votes de type Community Notes : une correction mathématique doit être vérifiable, attribuée et reliée à une version précise. Un compte GitHub gratuit est nécessaire pour déposer un ticket ; leur lecture reste publique.</p>
    <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/issues/new?template=mat101-correction.yml">Ouvrir un ticket de correction</a>
    <a href="https://github.com/kieranmcshane/kieranmcshane.github.io/issues?q=is%3Aissue%20MAT101">Consulter les tickets MAT101</a>
  </section>

  <section class="mat101-errata" id="errata" aria-labelledby="mat101-errata-title">
    <p class="mat101-kicker">Registre versionné</p>
    <h2 id="mat101-errata-title">Errata du polycopié source</h2>
    <p>Ces difficultés appartiennent à l’édition source du 13 septembre 2022. Elles ne sont pas masquées : le corrigé explique le problème, puis traite la formulation mathématiquement cohérente lorsqu’elle est identifiable.</p>
    <div class="mat101-errata-list">
      {% for erratum in site.data.mat101_errata %}
        <article id="erratum-{{ erratum.exercise | replace: '.', '-' }}">
          <header>
            <a href="#exercice-{{ erratum.exercise | replace: '.', '-' }}">Exercice {{ erratum.exercise }}</a>
            <span>{{ erratum.kind }}</span>
          </header>
          <p><strong>Problème.</strong> {{ erratum.problem }}</p>
          <p><strong>Formulation retenue.</strong> {{ erratum.correction }}</p>
          <small>Version {{ erratum.version }}</small>
        </article>
      {% endfor %}
    </div>
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
        <li><a href="{{ solution_pdf_url }}" download><strong>Corrigé PDF</strong><span>103 solutions · niveau L1</span></a></li>
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
        <p><strong>Kieran McShane, avec l’assistance d’OpenAI Codex.</strong></p>
      </article>
      <article>
        <h3>Rédaction du corrigé</h3>
        <p><strong>Rédaction initiale assistée par OpenAI ChatGPT ; édition et publication par Kieran McShane, avec OpenAI Codex.</strong> Les encadrés « Idée et plan » s’inspirent de la méthode de George Pólya. Version du 27 juillet 2026. Il ne s’agit ni d’un corrigé officiel de l’UGA ni d’une validation institutionnelle.</p>
      </article>
    </div>

    <div class="mat101-review-ledger">
      <strong>Contrôles effectués avant publication</strong>
      <ul>
        <li>103 transcriptions textuelles sélectionnables et indexées pour la recherche ;</li>
        <li>103 blocs de solutions distincts, de 1.1 à 4.17, rendus directement dans la page ;</li>
        <li>correspondance des quatre chapitres, numéros et fichiers sources ;</li>
        <li>crédits, statut non officiel, errata et formulaire de rectification intégrés.</li>
      </ul>
      <p><strong>Limite actuelle :</strong> ces contrôles portent sur l’exhaustivité, la structure et la provenance ; ils ne constituent pas une vérification indépendante de chaque démonstration.</p>
    </div>

    <details class="mat101-citation">
      <summary>Citations bibliographiques recommandées</summary>
      <p><cite>Collectif MAT101, <em>Langage mathématique, algèbre et géométrie élémentaires</em>, UE MAT101, Université Grenoble Alpes, édition du 13 septembre 2022. Responsable de l’édition citée : Raphaël Rossignol.</cite></p>
      <p><cite>Kieran McShane (éd.), <em>Recueil des exercices MAT101</em>, sélection, indexation et interface web, 2026, d’après le polycopié collectif MAT101 de l’Université Grenoble Alpes, avec l’assistance d’OpenAI Codex.</cite></p>
      <p><cite>Kieran McShane (éd.), <em>Corrigé détaillé des exercices MAT101</em>, rédaction initiale assistée par OpenAI ChatGPT, édition et publication avec l’assistance d’OpenAI Codex, version du 27 juillet 2026, corrigé non officiel.</cite></p>
      <p><cite>George Pólya, <em>How to Solve It: A New Aspect of Mathematical Method</em>, Princeton University Press, 1945.</cite></p>
      <a href="{{ bib_url }}" download>Télécharger les quatre références BibTeX</a>
    </details>

    <div class="mat101-rights-note">
      <p><strong>Source faisant autorité.</strong> Le recueil utilise l’édition fournie du 13 septembre 2022. Une <a href="https://www-fourier.univ-grenoble-alpes.fr/~rossigno/Enseignement/ens_files/mat_101_20221201.pdf">version institutionnelle datée du 1er décembre 2022</a> est hébergée par l’Institut Fourier.</p>
      <p><strong>Droits et rectifications.</strong> Aucune licence de réutilisation explicite n’a été identifiée dans le PDF du 13 septembre 2022 ; les droits sur les pages originales restent attachés à leurs titulaires. Cette sélection éducative et son corrigé non officiel ne constituent pas une publication de l’UGA. Toute demande d’attribution, de rectification ou de retrait peut être déposée dans le registre public ci-dessus ou adressée via la <a href="{{ '/about/#contact' | relative_url }}">page de contact</a>.</p>
    </div>
  </section>
</div>
