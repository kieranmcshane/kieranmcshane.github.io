---
layout: page
title: Exercices et corrigés MAT101
permalink: /mat101/exercices/
description: "Bibliothèque de 103 exercices MAT101 de niveau L1 avec énoncés, corrigés détaillés, PDF et sources LaTeX."
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
    <h1>103 exercices, 103 corrigés détaillés</h1>
    <p>Travaillez d’abord l’énoncé, puis révélez seulement l’accès à la solution lorsque vous en avez besoin. Les pages originales du polycopié collectif MAT101 sont conservées sans retranscription.</p>
    <div class="mat101-actions">
      <a class="mat101-primary-action" href="{{ statement_pdf_url }}">Ouvrir les énoncés <span aria-hidden="true">→</span></a>
      <a class="mat101-solution-action" href="{{ solution_pdf_url }}">Ouvrir le corrigé complet</a>
      <a href="#telechargements">Télécharger les fichiers</a>
    </div>
  </header>

  <section class="mat101-stats" aria-label="Contenu de la bibliothèque">
    <div><strong>103</strong><span>exercices</span></div>
    <div><strong>103</strong><span>solutions</span></div>
    <div><strong>4</strong><span>chapitres</span></div>
    <div><strong>L1</strong><span>niveau</span></div>
  </section>

  <aside class="mat101-verification" aria-label="Statut du corrigé">
    <div>
      <span class="mat101-status-dot" aria-hidden="true"></span>
      <strong>Couverture complète</strong>
      <span>103 solutions sur 103</span>
    </div>
    <p><strong>Corrigé non officiel.</strong> La structure, la numérotation et la correspondance avec les énoncés ont été contrôlées. La rédaction initiale a été assistée par OpenAI ChatGPT ; aucune relecture mathématique humaine intégrale n’est encore attestée.</p>
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
    Ouvrez l’énoncé depuis la carte de l’exercice. Le lien vers le corrigé reste masqué derrière « Voir la solution » pour éviter les révélations involontaires. Dans le polycopié, (*) vérifie les notions essentielles, (**) correspond en général au niveau attendu à l’examen et (***) propose un approfondissement.
  </aside>

  {% for chapter in site.data.mat101_exercises %}
    <section class="mat101-chapter" id="{{ chapter.id }}">
      <header>
        <span class="mat101-chapter-number">{{ chapter.number }}</span>
        <div>
          <h2>{{ chapter.title }}</h2>
          <p>{{ chapter.count }} exercices · pages originales {{ chapter.originalPages }}</p>
        </div>
      </header>
      <div class="mat101-exercise-grid" aria-label="Exercices et solutions du chapitre {{ chapter.number }}">
        {% for source_page in chapter.pages %}
          {% for exercise in source_page.exercises %}
            {% assign solution_matches = site.data.mat101_solutions | where: "id", exercise %}
            {% assign solution = solution_matches | first %}
            <article class="mat101-exercise-card" id="exercice-{{ exercise | replace: '.', '-' }}">
              <header>
                <span>Exercice</span>
                <strong>{{ exercise }}</strong>
              </header>
              <a class="mat101-statement-link" href="{{ statement_pdf_url }}#page={{ source_page.pdfPage }}" target="_blank" rel="noopener">
                <span>Énoncé</span>
                <small>p. {{ source_page.pdfPage }}</small>
              </a>
              <details class="mat101-solution-reveal">
                <summary>Voir la solution</summary>
                <a href="{{ solution_pdf_url }}#page={{ solution.pdfPage }}" target="_blank" rel="noopener">
                  <span>Ouvrir le corrigé</span>
                  <small>p. {{ solution.pdfPage }}</small>
                </a>
              </details>
            </article>
          {% endfor %}
        {% endfor %}
      </div>
    </section>
  {% endfor %}

  <section class="mat101-downloads" id="telechargements">
    <div class="mat101-download-intro">
      <p class="mat101-kicker">Fichiers</p>
      <h2>Lire, télécharger ou recompiler</h2>
      <p>Les énoncés et le corrigé sont proposés séparément pour faciliter le travail autonome. Les deux ensembles de sources LaTeX restent disponibles et compilables.</p>
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

  <section class="mat101-credits" aria-labelledby="mat101-credits-title">
    <p class="mat101-kicker">Crédits, citation et transparence</p>
    <h2 id="mat101-credits-title">Qui a produit quoi ?</h2>

    <div class="mat101-credit-grid">
      <article>
        <h3>Énoncés originaux</h3>
        <p><strong>Collectif MAT101, Université Grenoble Alpes.</strong> Le polycopié cite notamment Bernard Ycart, Agnès Coquio, Éric Dumas, Emmanuel Peyre, Pierre Dehornoy et Raphaël Rossignol, « et d’autres ». Raphaël Rossignol est indiqué comme responsable de l’édition du 13 septembre 2022.</p>
      </article>
      <article>
        <h3>Recueil et interface</h3>
        <p><strong>Kieran McShane, avec l’assistance d’OpenAI Codex.</strong> Sélection des pages, indexation des 103 exercices, couverture du recueil, correspondance énoncé–corrigé, conception et publication de cette interface.</p>
      </article>
      <article>
        <h3>Rédaction du corrigé</h3>
        <p><strong>Rédaction initiale assistée par OpenAI ChatGPT ; édition et publication par Kieran McShane, avec OpenAI Codex.</strong> Version du 27 juillet 2026. Il ne s’agit ni d’un corrigé officiel de l’UGA ni d’une validation institutionnelle.</p>
      </article>
    </div>

    <div class="mat101-review-ledger">
      <strong>Contrôles effectués avant publication</strong>
      <ul>
        <li>57 pages lisibles et source LaTeX recompilée ;</li>
        <li>103 titres de solutions distincts, de 1.1 à 4.17 ;</li>
        <li>correspondance des quatre chapitres et des 103 liens directs ;</li>
        <li>crédits et statut non officiel intégrés au site, au PDF et aux sources.</li>
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
      <p><strong>Droits et rectifications.</strong> Aucune licence de réutilisation explicite n’a été identifiée dans le PDF du 13 septembre 2022 ; les droits sur les pages originales restent attachés à leurs titulaires. Cette sélection éducative et son corrigé non officiel ne constituent pas une publication de l’UGA. Toute demande de rectification d’attribution ou de retrait peut être adressée via la <a href="{{ '/about/' | relative_url }}">page de contact</a>.</p>
    </div>
  </section>
</div>
