---
layout: page
title: Répertoire raisonné
permalink: /repertoire-raisonne/
description: "Une bibliothèque interactive de 127 problèmes corrigés d’algèbre, d’analyse, de topologie et de probabilités."
math: true
---

{% assign repertoire_pdf = '/assets/documents/repertoire-raisonne-algebre-analyse.pdf' | relative_url %}

<div class="repertoire-library">
  <header class="repertoire-hero">
    <p class="repertoire-kicker">Répertoire avancé · algèbre et analyse</p>
    <h1>127 problèmes, un outil décisif à chaque fois</h1>
    <p>Questions courtes, preuves denses et contre-exemples : le recueil se lit comme un répertoire de méthodes, de l’action de groupe au théorème de Baire.</p>
    <div class="repertoire-actions">
      <a class="repertoire-primary-action" href="#problemes">Explorer les problèmes <span aria-hidden="true">↓</span></a>
      <a href="{{ repertoire_pdf }}">Lire le PDF</a>
      <a href="{{ repertoire_pdf }}" download>Télécharger</a>
    </div>
  </header>

  <section class="repertoire-stats" aria-label="Contenu du répertoire">
    <div><strong>127</strong><span>problèmes corrigés</span></div>
    <div><strong>66</strong><span>pages composées</span></div>
    <div><strong>14</strong><span>chapitres de lecture</span></div>
    <div><strong>5</strong><span>grandes parties</span></div>
  </section>

  <aside class="repertoire-verification" aria-label="Statut de la relecture">
    <div>
      <span class="repertoire-status-dot" aria-hidden="true"></span>
      <strong>Corpus intégralement relu</strong>
      <span>127 problèmes · 66 pages</span>
    </div>
    <p>La relecture n’a relevé aucun énoncé faux, aucun contre-exemple incorrect et aucune démonstration circulaire. Deux corrections de formulation restent consignées ci-dessous ; elles n’affectent pas les résultats.</p>
  </aside>

  <section class="repertoire-introduction" aria-labelledby="repertoire-intro-title">
    <div>
      <p class="repertoire-kicker">Principe éditorial</p>
      <h2 id="repertoire-intro-title">Chercher une méthode, pas seulement un chapitre</h2>
    </div>
    <p>Le PDF conserve l’ordre original et la solution immédiatement après l’énoncé. Cette page ajoute une seconde architecture : cinq parties cohérentes, une recherche plein texte sur les titres et des parcours transversaux. La numérotation du recueil reste inchangée.</p>
  </section>

  <section class="repertoire-paths" aria-labelledby="repertoire-paths-title">
    <div class="repertoire-section-heading">
      <div>
        <p class="repertoire-kicker">Parcours de lecture</p>
        <h2 id="repertoire-paths-title">Entrer par un fil directeur</h2>
      </div>
    </div>
    <div class="repertoire-path-grid">
      <article>
        <span>01</span>
        <h3>Agrégation · algèbre</h3>
        <p>Polynôme minimal, cyclicité, commutant, Jordan, formes quadratiques et groupes finis.</p>
        <a href="#problemes" data-repertoire-preset="algebre-lineaire">Commencer par les opérateurs</a>
      </article>
      <article>
        <span>02</span>
        <h3>Agrégation · analyse</h3>
        <p>Compacité, convergence dans Lᵖ, analyse complexe, Fourier et théorème de Baire.</p>
        <a href="#problemes" data-repertoire-preset="analyse-reelle">Commencer par l’analyse réelle</a>
      </article>
      <article>
        <span>03</span>
        <h3>Contre-exemples</h3>
        <p>Matrices symétriques complexes, réciproque de Cesàro, métriques équivalentes et loi log-normale.</p>
        <a href="{{ repertoire_pdf }}#page=10">Lire un premier contre-exemple</a>
      </article>
      <article>
        <span>04</span>
        <h3>Outils transversaux</h3>
        <p>Dimension, dualité, compacité, zéros isolés, transformée de Fourier et argument de Baire.</p>
        <a href="#coups-de-projecteur">Voir les preuves remarquables</a>
      </article>
    </div>
  </section>

  <section class="repertoire-browser" id="problemes" aria-labelledby="repertoire-browser-title">
    <div class="repertoire-browser-heading">
      <div>
        <p class="repertoire-kicker">Index interactif</p>
        <h2 id="repertoire-browser-title">Trouver un problème</h2>
      </div>
      <p id="repertoire-result-count" aria-live="polite">127 problèmes affichés</p>
    </div>

    <label class="repertoire-search">
      <span>Rechercher un numéro, un titre, une partie ou une méthode</span>
      <input id="repertoire-search-input" type="search" inputmode="search" placeholder="Par exemple : Jordan, Fourier, 57, compacité…" autocomplete="off">
    </label>

    <div class="repertoire-filter-group" aria-label="Filtrer par grande partie">
      <button type="button" class="repertoire-filter is-active" data-repertoire-part="" aria-pressed="true">Tout <span>127</span></button>
      {% for part in site.data.repertoire_raisonne %}
        {% assign part_count = 0 %}
        {% for chapter in part.chapters %}
          {% assign chapter_size = chapter.problems | size %}
          {% assign part_count = part_count | plus: chapter_size %}
        {% endfor %}
        <button type="button" class="repertoire-filter" data-repertoire-part="{{ part.id }}" aria-pressed="false">{{ part.number }} · {{ part.title }} <span>{{ part_count }}</span></button>
      {% endfor %}
    </div>
  </section>

  <div id="repertoire-no-results" class="repertoire-no-results" hidden>
    <strong>Aucun problème trouvé.</strong>
    <span>Essayez un numéro comme « 121 » ou un outil comme « Baire ».</span>
  </div>

  <div class="repertoire-catalogue">
    {% for part in site.data.repertoire_raisonne %}
      <section class="repertoire-part" id="{{ part.id }}" data-repertoire-section data-part="{{ part.id }}">
        <header>
          <span>{{ part.number }}</span>
          <div>
            <h2>{{ part.title }}</h2>
            {% assign part_count = 0 %}
            {% for chapter in part.chapters %}
              {% assign chapter_size = chapter.problems | size %}
              {% assign part_count = part_count | plus: chapter_size %}
            {% endfor %}
            <p>{{ part.chapters.size }} chapitres · {{ part_count }} problèmes</p>
          </div>
        </header>

        {% for chapter in part.chapters %}
          <section class="repertoire-chapter" id="{{ chapter.id }}" data-repertoire-chapter>
            <header>
              <span>{{ chapter.number }}</span>
              <div>
                <h3>{{ chapter.title }}</h3>
                <p>{{ chapter.problems.size }} problèmes</p>
              </div>
            </header>
            <ol class="repertoire-problem-list">
              {% for problem in chapter.problems %}
                <li
                  id="probleme-{{ problem[0] }}"
                  data-repertoire-problem
                  data-search="{{ problem[0] }} {{ problem[1] | downcase | escape }} {{ chapter.title | downcase | escape }} {{ part.title | downcase | escape }}"
                >
                  <a href="{{ repertoire_pdf }}#page={{ problem[2] }}" aria-label="Problème {{ problem[0] }} — {{ problem[1] }} — ouvrir la page {{ problem[2] }} du PDF">
                    <span class="repertoire-problem-number">{{ problem[0] }}</span>
                    <span class="repertoire-problem-title">{{ problem[1] }}</span>
                    <span class="repertoire-problem-page">p. {{ problem[2] }} <span aria-hidden="true">↗</span></span>
                  </a>
                </li>
              {% endfor %}
            </ol>
          </section>
        {% endfor %}
      </section>
    {% endfor %}
  </div>

  <section class="repertoire-highlights" id="coups-de-projecteur" aria-labelledby="repertoire-highlights-title">
    <div class="repertoire-section-heading">
      <div>
        <p class="repertoire-kicker">Coups de projecteur</p>
        <h2 id="repertoire-highlights-title">Huit preuves particulièrement réussies</h2>
      </div>
    </div>
    <div class="repertoire-highlight-grid">
      <a href="{{ repertoire_pdf }}#page=7"><span>8</span>Extension quadratique et indépendance de \(1,\gamma,\gamma^2/2\)</a>
      <a href="{{ repertoire_pdf }}#page=11"><span>18</span>Maximalité compacte de \(O_n(\mathbb R)\)</a>
      <a href="{{ repertoire_pdf }}#page=26"><span>57</span>Fermeture d’une classe de similitude</a>
      <a href="{{ repertoire_pdf }}#page=29"><span>65</span>Dimension d’un espace de matrices nilpotentes</a>
      <a href="{{ repertoire_pdf }}#page=41"><span>82</span>Inégalité de Young et existence presque partout</a>
      <a href="{{ repertoire_pdf }}#page=51"><span>100</span>Non-surjectivité de \(L^1\) vers \(C_0\)</a>
      <a href="{{ repertoire_pdf }}#page=61"><span>121</span>Argument de Baire sur les jets</a>
      <a href="{{ repertoire_pdf }}#page=63"><span>125</span>Famille de Stieltjes log-normale</a>
    </div>
  </section>

  <section class="repertoire-errata" id="errata" aria-labelledby="repertoire-errata-title">
    <div class="repertoire-section-heading">
      <div>
        <p class="repertoire-kicker">Registre de relecture</p>
        <h2 id="repertoire-errata-title">Deux corrections de formulation</h2>
      </div>
      <p>Aucun résultat mathématique n’est remis en cause.</p>
    </div>
    <article>
      <header><a href="{{ repertoire_pdf }}#page=6">Problème 4 · page 3 du livre</a><span>Titre</span></header>
      <p><strong>À lire :</strong> « réductible dans \(\mathbb F_p[X]\) pour tout nombre premier \(p\) », ou plus brièvement « réductible modulo tout nombre premier ». L’expression « sur tout corps premier » inclurait improprement \(\mathbb Q\).</p>
    </article>
    <article>
      <header><a href="{{ repertoire_pdf }}#page=6">Problème 6 · page 3 du livre</a><span>Quantification</span></header>
      <p><strong>À lire :</strong> « Pour \(s\in\{0,\ldots,r-1\}\), l’orbite de \(\alpha^{q^s}\) sous \(x\mapsto x^{q^r}\) a longueur \(d/r\). » Le calcul et la conclusion restent inchangés.</p>
    </article>
  </section>

  <section class="repertoire-notes" aria-labelledby="repertoire-notes-title">
    <div>
      <p class="repertoire-kicker">Pour une prochaine édition</p>
      <h2 id="repertoire-notes-title">Ce que la page prépare</h2>
    </div>
    <ul>
      <li>séparer les énoncés et les solutions dans le PDF numérique ;</li>
      <li>ajouter niveau, nature et outil décisif à chaque problème ;</li>
      <li>construire un index des théorèmes et un index des méthodes ;</li>
      <li>déplacer les problèmes 126-127 auprès des suites et fonctions réelles.</li>
    </ul>
  </section>

  <footer class="repertoire-download">
    <div>
      <p class="repertoire-kicker">Édition complète</p>
      <h2>Lire le répertoire hors ligne</h2>
      <p>PDF A4 de 66 pages, 127 énoncés et solutions brèves, avec sommaire et repères bibliographiques.</p>
    </div>
    <a href="{{ repertoire_pdf }}" download>Télécharger le PDF <span aria-hidden="true">↓</span></a>
  </footer>
</div>
