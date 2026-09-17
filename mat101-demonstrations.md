---
layout: mat101
title: Démonstrations essentielles MAT101
permalink: /mat101/demonstrations/
description: "Les démonstrations essentielles du polycopié MAT101, organisées par chapitre."
math: true
image: "/assets/images/og-mat101.png"
image_alt: "MAT101 — IMA02"
---

{% assign source_pdf_url = '/assets/documents/mat101/mat_101_20251001.pdf' | relative_url %}
{% assign demonstrations = site.data.mat101_demonstrations.chapters %}
{% assign total_demonstrations = 0 %}
{% for chapter in demonstrations %}
  {% assign total_demonstrations = total_demonstrations | plus: chapter.demonstrations.size %}
{% endfor %}

<div class="mat101-library mat101-demonstrations" data-mat101-demonstrations>
  <header class="mat101-page-heading">
    <h1>Démonstrations essentielles</h1>
    <nav class="mat101-page-links" aria-label="Sections de la page démonstrations">
      <a href="#informations">Infos cours</a>
      {% for chapter in demonstrations %}
        {% if chapter.demonstrations.size > 0 %}
          <a href="#{{ chapter.id }}">Chapitre {{ chapter.number }}</a>
        {% endif %}
      {% endfor %}
    </nav>
  </header>

  {% include mat101-informations.html %}

  <section class="mat101-demonstrations-intro" aria-labelledby="mat101-demonstrations-intro-title">
    <p class="mat101-kicker">Polycopié MAT101</p>
    <h2 id="mat101-demonstrations-intro-title">Preuves à maîtriser</h2>
    <p>
      Cette page rassemble les démonstrations essentielles signalées dans le polycopié officiel.
      Les énoncés et preuves sont retranscrits pour une lecture directe en ligne.
    </p>
    <p class="mat101-demonstrations-count">{{ total_demonstrations }} démonstrations sur 4 chapitres</p>
  </section>

  <nav class="mat101-demonstrations-toc" aria-label="Sommaire des démonstrations">
    {% for chapter in demonstrations %}
      {% if chapter.demonstrations.size > 0 %}
        <section class="mat101-demonstrations-toc-chapter">
          <h3>
            <a href="#{{ chapter.id }}">Chapitre {{ chapter.number }} — {{ chapter.title }}</a>
          </h3>
          <ul>
            {% for demo in chapter.demonstrations %}
              <li>
                <a href="#demo-{{ demo.id | replace: '.', '-' }}">{{ demo.label }}</a>
                {% if demo.subtitle %}
                  <span>{{ demo.subtitle }}</span>
                {% endif %}
              </li>
            {% endfor %}
          </ul>
        </section>
      {% endif %}
    {% endfor %}
  </nav>

  {% for chapter in demonstrations %}
    <section
      class="mat101-demonstrations-chapter"
      id="{{ chapter.id }}"
      tabindex="-1"
      aria-labelledby="chapter-{{ chapter.id }}-title"
    >
      <header class="mat101-demonstrations-chapter-heading">
        <span class="mat101-chapter-number">{{ chapter.number }}</span>
        <div>
          <h2 id="chapter-{{ chapter.id }}-title">{{ chapter.title }}</h2>
          {% if chapter.demonstrations.size > 0 %}
            <p>{{ chapter.demonstrations.size }} démonstration{% if chapter.demonstrations.size > 1 %}s{% endif %}</p>
          {% endif %}
        </div>
      </header>

      {% if chapter.demonstrations.size == 0 %}
        <p class="mat101-demonstrations-empty">{{ chapter.emptyMessage }}</p>
      {% else %}
        <div class="mat101-demonstrations-list">
          {% for demo in chapter.demonstrations %}
            <article
              class="mat101-demonstration-card"
              id="demo-{{ demo.id | replace: '.', '-' }}"
              data-demonstration-id="{{ demo.id }}"
            >
              <header class="mat101-demonstration-header">
                <p class="mat101-kicker">{{ demo.label }}</p>
                <h3>{{ demo.subtitle }}</h3>
              </header>

              <section class="mat101-statement" aria-labelledby="statement-{{ demo.id | replace: '.', '-' }}">
                <div class="mat101-content-heading">
                  <h4 id="statement-{{ demo.id | replace: '.', '-' }}">Énoncé</h4>
                  <a href="{{ source_pdf_url }}">Consulter le polycopié</a>
                </div>
                <div class="mat101-statement-transcription mat101-statement-curated" lang="fr">
                  {{ demo.statementHtml }}
                </div>
              </section>

              <section class="mat101-demonstration-proof" aria-labelledby="proof-{{ demo.id | replace: '.', '-' }}">
                <div class="mat101-content-heading">
                  <h4 id="proof-{{ demo.id | replace: '.', '-' }}">Démonstration</h4>
                </div>
                <div class="mat101-solution-body">
                  {{ demo.proofHtml }}
                </div>
              </section>
            </article>
          {% endfor %}
        </div>
      {% endif %}
    </section>
  {% endfor %}
</div>
