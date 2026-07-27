---
layout: page
title: Exercices MAT101
permalink: /mat101/exercices/
description: "Index complet des 103 exercices MAT101 de niveau L1, avec recueil PDF et source LaTeX."
---

{% assign pdf_url = '/assets/documents/mat101/recueil-exercices-mat101.pdf' | relative_url %}
{% assign tex_url = '/assets/documents/mat101/recueil-exercices-mat101.tex' | relative_url %}
{% assign archive_url = '/assets/documents/mat101/recueil-exercices-mat101-sources.zip' | relative_url %}

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

  <footer class="mat101-source">
    <p><strong>Source et attribution.</strong> Polycopié collectif MAT101, <em>Langage mathématique, algèbre et géométrie élémentaires</em>, Université Grenoble Alpes, édition du 13 septembre 2022. Le document cite notamment Bernard Ycart, Agnès Coquio, Éric Dumas, Emmanuel Peyre, Pierre Dehornoy et Raphaël Rossignol parmi ses contributeurs. Une <a href="https://www-fourier.univ-grenoble-alpes.fr/~rossigno/Enseignement/ens_files/mat_101_20221201.pdf">version institutionnelle du polycopié</a> est disponible sur le site de l’Institut Fourier.</p>
    <p>Cette page indexe les énoncés. Un corrigé intégral n’est pas publié ici tant que chacune des 103 solutions n’a pas fait l’objet d’une rédaction et d’une vérification mathématique distinctes.</p>
  </footer>
</div>
