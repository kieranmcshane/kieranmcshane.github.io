---
layout: page
title: Exercices MAT101
permalink: /mat101/exercices/
description: "Index complet des 103 exercices MAT101 de niveau L1, avec recueil PDF et source LaTeX."
---

{% assign pdf_url = '/assets/documents/mat101/recueil-exercices-mat101.pdf' | relative_url %}
{% assign tex_url = '/assets/documents/mat101/recueil-exercices-mat101.tex' | relative_url %}
{% assign archive_url = '/assets/documents/mat101/recueil-exercices-mat101-sources.zip' | relative_url %}
{% assign bib_url = '/assets/documents/mat101/mat101-citations.bib' | relative_url %}

<div class="mat101-library">
  <header class="mat101-hero">
    <p class="mat101-kicker">Université Grenoble Alpes · niveau L1</p>
    <h1>103 exercices de mathématiques, réunis et indexés</h1>
    <p>Ce recueil conserve les énoncés originaux du polycopié MAT101 : nombres complexes, langage mathématique, fonctions, dénombrement et limites de suites. Aucun énoncé n’a été retranscrit automatiquement.</p>
    <div class="mat101-actions">
      <a class="mat101-primary-action" href="{{ pdf_url }}">Ouvrir le recueil PDF <span aria-hidden="true">→</span></a>
      <a href="{{ pdf_url }}" download>Télécharger le PDF</a>
      <a href="{{ archive_url }}" download>Archive LaTeX compilable</a>
    </div>
  </header>

  <section class="mat101-stats" aria-label="Contenu du recueil">
    <div><strong>103</strong><span>exercices</span></div>
    <div><strong>4</strong><span>chapitres</span></div>
    <div><strong>34</strong><span>pages</span></div>
    <div><strong>L1</strong><span>niveau</span></div>
  </section>

  <nav class="mat101-chapter-nav" aria-label="Chapitres du recueil">
    {% for chapter in site.data.mat101_exercises %}
      <a href="#{{ chapter.id }}">
        <span>{{ chapter.number }}</span>
        <strong>{{ chapter.title }}</strong>
        <small>{{ chapter.count }} exercices</small>
      </a>
    {% endfor %}
  </nav>

  <aside class="mat101-reading-note">
    <strong>Repères de difficulté.</strong>
    Dans le document, (*) vérifie les notions essentielles, (**) correspond en général au niveau attendu à l’examen et (***) propose un approfondissement. Chaque lien ci-dessous ouvre directement la page contenant l’exercice.
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
      <div class="mat101-exercise-grid" aria-label="Exercices du chapitre {{ chapter.number }}">
        {% for source_page in chapter.pages %}
          {% for exercise in source_page.exercises %}
            <a href="{{ pdf_url }}#page={{ source_page.pdfPage }}" target="_blank" rel="noopener">
              <span>Exercice</span>
              <strong>{{ exercise }}</strong>
              <small>p. {{ source_page.pdfPage }}</small>
            </a>
          {% endfor %}
        {% endfor %}
      </div>
    </section>
  {% endfor %}

  <section class="mat101-downloads">
    <div>
      <p class="mat101-kicker">Fichiers</p>
      <h2>Réutiliser ou recompiler le recueil</h2>
      <p>Le PDF de 34 pages contient une couverture, un sommaire cliquable et les 32 pages originales d’exercices. Le source utilise <code>pdfpages</code>, afin de préserver exactement les formules, la numérotation et les étoiles de difficulté.</p>
    </div>
    <ul>
      <li><a href="{{ pdf_url }}" download><strong>Recueil PDF</strong><span>103 exercices · 34 pages</span></a></li>
      <li><a href="{{ tex_url }}" download><strong>Source LaTeX</strong><span>Fichier principal</span></a></li>
      <li><a href="{{ archive_url }}" download><strong>Archive complète</strong><span>LaTeX + PDF source</span></a></li>
    </ul>
  </section>

  <section class="mat101-credits" aria-labelledby="mat101-credits-title">
    <p class="mat101-kicker">Crédits, citation et transparence</p>
    <h2 id="mat101-credits-title">Qui a produit quoi ?</h2>

    <div class="mat101-credit-grid">
      <article>
        <h3>Contenu mathématique original</h3>
        <p><strong>Collectif MAT101, Université Grenoble Alpes.</strong> Le polycopié indique qu’il a été enrichi au fil des ans et cite, parmi ses contributeurs, Bernard Ycart, Agnès Coquio, Éric Dumas, Emmanuel Peyre, Pierre Dehornoy et Raphaël Rossignol, « et d’autres ». Il désigne Raphaël Rossignol comme dernier responsable de l’édition du 13 septembre 2022.</p>
      </article>
      <article>
        <h3>Cette édition et cette interface</h3>
        <p><strong>Sélection des pages, indexation, couverture et conception web : Kieran McShane, avec l’assistance d’OpenAI Codex.</strong> Les 32 pages d’exercices sont reproduites sans retranscription ni modification ; la couverture, le sommaire cliquable et les liens directs ont été ajoutés séparément.</p>
      </article>
      <article>
        <h3>Futurs corrigés</h3>
        <p>Les solutions seront des rédactions distinctes, non officielles et non attribuées à l’UGA. Chaque corrigé indiquera son mode de rédaction, sa date, sa version, son statut de vérification et le nom du relecteur lorsqu’une relecture humaine aura eu lieu. Toute source ou tout résultat externe utilisé sera cité au niveau de la solution concernée.</p>
      </article>
    </div>

    <details class="mat101-citation">
      <summary>Citation bibliographique recommandée</summary>
      <p><cite>Collectif MAT101, <em>Langage mathématique, algèbre et géométrie élémentaires</em>, UE MAT101, Portail Informatique, Mathématiques et Applications, Université Grenoble Alpes, édition du 13 septembre 2022, exercices p. 30–35, 61–70, 93–103 et 116–120. Responsable de l’édition citée : Raphaël Rossignol.</cite></p>
      <p>Pour citer cette sélection : <cite>Kieran McShane (éd.), <em>Recueil des exercices MAT101</em>, sélection, indexation et interface web, 2026, d’après le polycopié collectif MAT101 de l’Université Grenoble Alpes.</cite></p>
      <a href="{{ bib_url }}" download>Télécharger les deux références BibTeX</a>
    </details>

    <div class="mat101-rights-note">
      <p><strong>Source faisant autorité.</strong> Le recueil utilise l’édition fournie du 13 septembre 2022. Une <a href="https://www-fourier.univ-grenoble-alpes.fr/~rossigno/Enseignement/ens_files/mat_101_20221201.pdf">version institutionnelle datée du 1er décembre 2022</a> est hébergée par l’Institut Fourier.</p>
      <p><strong>Droits et rectifications.</strong> Aucune licence de réutilisation explicite n’a été identifiée dans le PDF du 13 septembre 2022 ; les droits sur les pages originales restent attachés à leurs titulaires. Cette sélection éducative ne constitue ni une édition officielle de l’UGA ni un corrigé officiel. Toute demande de rectification d’attribution ou de retrait peut être adressée via la <a href="{{ '/about/' | relative_url }}">page de contact</a>.</p>
    </div>

    <p class="mat101-solution-status">Cette page indexe actuellement les énoncés. Un corrigé intégral ne sera publié que lorsque chacune des 103 solutions aura une rédaction individualisée, une provenance explicite et un statut de vérification visible.</p>
  </section>
</div>
