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
    <p>Questions courtes, preuves denses et contre-exemples : le recueil se lit comme un répertoire de méthodes. Les 127 énoncés et solutions sont désormais consultables directement dans la page.</p>
    <div class="repertoire-actions">
      <a class="repertoire-primary-action" href="#bilan-relecture">Lire les 127 problèmes en ligne <span aria-hidden="true">↓</span></a>
      <a href="#problemes">Explorer l’index</a>
      <a href="{{ repertoire_pdf }}">Lire le PDF</a>
      <a href="{{ repertoire_pdf }}" download>Télécharger</a>
    </div>
  </header>

  <section class="repertoire-stats" aria-label="Contenu du répertoire">
    <div><strong>127</strong><span>problèmes corrigés</span></div>
    <div><strong>127</strong><span>fiches natives complètes</span></div>
    <div><strong>14</strong><span>chapitres dans l’index</span></div>
    <div><strong>5</strong><span>grandes parties</span></div>
  </section>

  <aside class="repertoire-verification" aria-label="Statut de la relecture">
    <div>
      <span class="repertoire-status-dot" aria-hidden="true"></span>
      <strong>Corpus intégralement relu</strong>
      <span>127 problèmes · 66 pages</span>
    </div>
    <p>La relecture confirme les 127 énoncés et leurs résultats. Une preuve demande une conjugaison au problème 80 ; deux formulations et deux conventions sont précisées dans le registre ci-dessous.</p>
  </aside>

  <section class="repertoire-introduction" aria-labelledby="repertoire-intro-title">
    <div>
      <p class="repertoire-kicker">Principe éditorial</p>
      <h2 id="repertoire-intro-title">Chercher une méthode, pas seulement un chapitre</h2>
    </div>
    <p>Le PDF conserve l’ordre original et la solution immédiatement après l’énoncé. Cette page ajoute cinq parties cohérentes, une recherche plein texte sur les titres et des parcours transversaux. Les 127 problèmes se lisent sans quitter le site ; le PDF reste disponible comme fac-similé de contrôle.</p>
  </section>

  <aside class="repertoire-sources" aria-labelledby="repertoire-sources-title">
    <div>
      <p class="repertoire-kicker">Sources et prolongements</p>
      <h2 id="repertoire-sources-title">Une source primaire, des repères externes</h2>
    </div>
    <p>Les énoncés et solutions sont transcrits depuis le PDF revu. Les liens ajoutés dans les fiches conduisent vers des développements et références thématiques recensés par <a href="https://agreg-maths.fr/">agreg-maths.fr</a>. La page des <a href="https://agreg-maths.fr/ressources/retours">retours d’oraux</a> permet en complément de repérer les questions effectivement posées par des jurys ; ces témoignages ne sont pas traités comme des corrigés canoniques.</p>
  </aside>

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
        <a href="#probleme-natif-16">Lire un premier contre-exemple</a>
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
                  <a href="#probleme-natif-{{ problem[0] }}" aria-label="Problème {{ problem[0] }} — {{ problem[1] }} — lire l’énoncé et la solution sur cette page">
                    <span class="repertoire-problem-number">{{ problem[0] }}</span>
                    <span class="repertoire-problem-title">{{ problem[1] }}</span>
                    <span class="repertoire-problem-page">Lire ici <span aria-hidden="true">↓</span></span>
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
      <a href="#probleme-natif-8"><span>8</span>Extension quadratique et indépendance de \(1,\gamma,\gamma^2/2\)</a>
      <a href="#probleme-natif-18"><span>18</span>Maximalité compacte de \(O_n(\mathbb R)\)</a>
      <a href="#probleme-natif-57"><span>57</span>Fermeture d’une classe de similitude</a>
      <a href="#probleme-natif-65"><span>65</span>Dimension d’un espace de matrices nilpotentes</a>
      <a href="#probleme-natif-82"><span>82</span>Inégalité de Young et existence presque partout</a>
      <a href="#probleme-natif-100"><span>100</span>Non-surjectivité de \(L^1\) vers \(C_0\)</a>
      <a href="#probleme-natif-121"><span>121</span>Argument de Baire sur les jets · lire ici</a>
      <a href="#probleme-natif-125"><span>125</span>Famille de Stieltjes log-normale · lire ici</a>
    </div>
  </section>

  <section class="repertoire-native" id="bilan-relecture" aria-labelledby="repertoire-native-title">
    <div class="repertoire-section-heading">
      <div>
        <p class="repertoire-kicker">Lecture intégrée · corpus complet</p>
        <h2 id="repertoire-native-title">127 problèmes à travailler directement ici</h2>
      </div>
      <p>Énoncés complets · solutions repliables · références · notes de relecture</p>
    </div>
    <p class="repertoire-native-intro">Cette section ne renvoie plus le lecteur au livre pour comprendre le problème. Chaque fiche contient l’énoncé, la solution et des prolongements documentaires lorsqu’ils sont pertinents. Le fac-similé PDF n’apparaît qu’en source primaire de contrôle et en version téléchargeable.</p>

    {% for part in site.data.repertoire_raisonne %}
      {% for chapter in part.chapters %}
        {% assign native_transcriptions = site.data.repertoire_native_transcriptions | where: "chapterId", chapter.id %}
        {% if native_transcriptions.size > 0 %}
          <section class="repertoire-native-chapter" aria-labelledby="native-chapter-{{ chapter.id }}">
            <header>
              <span>{{ chapter.number }}</span>
              <div>
                <h3 id="native-chapter-{{ chapter.id }}">{{ chapter.title }}</h3>
                <p>{{ native_transcriptions.size }} énoncés et solutions</p>
              </div>
            </header>
            {% include repertoire-native-references.html chapter_id=chapter.id %}
            <div class="repertoire-native-list">
              {% for item in native_transcriptions %}
                <article id="probleme-natif-{{ item.number }}" data-repertoire-native-problem="{{ item.number }}">
                  <header>
                    <div>
                      <span>Problème {{ item.number }}</span>
                      <h4>{{ item.title }}</h4>
                    </div>
                    <strong>Transcription native</strong>
                  </header>
                  <section class="repertoire-native-statement" aria-labelledby="enonce-{{ item.number }}">
                    <h5 id="enonce-{{ item.number }}">Énoncé</h5>
                    <div class="repertoire-native-transcription">
                      {% if item.statementMathjax %}
                        {{ item.statementMathjax }}
                      {% else %}
                        {{ item.statement | escape }}
                      {% endif %}
                    </div>
                  </section>
                  <details class="repertoire-native-solution">
                    <summary><span>Afficher la solution</span><small>Solution du recueil</small></summary>
                    <div class="repertoire-native-transcription">
                      {% if item.solutionMathjax %}
                        {{ item.solutionMathjax }}
                      {% else %}
                        {{ item.solution | escape }}
                      {% endif %}
                    </div>
                  </details>
                  <footer>
                    <span>{{ item.transcription }}</span>
                    <a href="{{ repertoire_pdf }}#page={{ item.pdfPage }}">Comparer au fac-similé · p. {{ item.pdfPage }}</a>
                  </footer>
                </article>
              {% endfor %}
            </div>
          </section>
        {% endif %}
      {% endfor %}
    {% endfor %}

    <section class="repertoire-native-chapter" aria-labelledby="native-chapter-14">
      <header>
        <span>14</span>
        <div>
          <h3 id="native-chapter-14">Topologie et analyse fonctionnelle</h3>
          <p>Problèmes 111–121 · onze énoncés et solutions</p>
        </div>
      </header>
      {% include repertoire-native-references.html chapter_id="topologie-baire" %}
      <div class="repertoire-native-list">
        <article id="probleme-natif-111" data-repertoire-native-problem="111" data-repertoire-audit-problem="111">
          <header><div><span>Problème 111</span><h4>Point fixe d’une application non expansive sur un compact convexe</h4></div><strong>Correct</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-111">
            <h5 id="enonce-111">Énoncé</h5>
            <p>Soit \(K\) un compact convexe non vide d’un espace vectoriel normé et soit \(f:K\to K\) telle que
            \[
              \lVert f(x)-f(y)\rVert\le \lVert x-y\rVert .
            \]
            Montrer que \(f\) possède un point fixe.</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Approximation contractante et compacité</small></summary>
            <div>
              <p>Fixons \(a\in K\). Pour \(n\ge2\), définissons
              \[
                f_n(x)=\frac1n a+\left(1-\frac1n\right)f(x).
              \]
              La convexité de \(K\) donne \(f_n(K)\subset K\), et \(f_n\) est une contraction de rapport \(1-\frac1n\). Comme \(K\) est complet, le théorème du point fixe de Banach fournit un point fixe \(x_n\in K\).</p>
              <p>L’équation \(x_n=f_n(x_n)\) donne
              \[
                x_n-f(x_n)=\frac1n\bigl(a-f(x_n)\bigr).
              \]
              Le membre de droite tend uniformément vers \(0\), puisque \(K\) est borné. Par compacité, une sous-suite \((x_{n_k})\) converge vers un point \(x\in K\). La fonction \(f\) est continue, et le passage à la limite donne \(x=f(x)\).</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> La complétude requise par Banach vient exactement de la compacité de \(K\), et l’erreur \(x_n-f(x_n)\) est uniforme.</aside>
          <footer><a href="{{ repertoire_pdf }}#page=57">Comparer au fac-similé · p. 54 du livre</a></footer>
        </article>
        <article id="probleme-natif-112" data-repertoire-native-problem="112" data-repertoire-audit-problem="112">
          <header><div><span>Problème 112</span><h4>Projection sur le cône positif de \(L^2\)</h4></div><strong>Correct</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-112">
            <h5 id="enonce-112">Énoncé</h5>
            <p>Dans l’espace de Hilbert réel \(L^2(\mathbb R)\), considérons
            \[
              C=\{f\in L^2(\mathbb R):f\ge0\ \text{presque partout}\}.
            \]
            Montrer que \(C\) est fermé et convexe, puis déterminer la projection orthogonale sur \(C\).</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Parties positive et négative</small></summary>
            <div>
              <p>La convexité est immédiate. Si \(f_n\in C\) et \(f_n\to f\) dans \(L^2\), alors, en notant \(f_-=\max(-f,0)\),
              \[
                0\le f_-(x)\le |f(x)-f_n(x)|\quad\text{presque partout}.
              \]
              Ainsi \(\lVert f_-\rVert_2\le\lVert f-f_n\rVert_2\to0\), donc \(f_-=0\) presque partout et \(f\in C\). Le cône est fermé.</p>
              <p>La projection est la partie positive \(P_C(f)=f_+=\max(f,0)\). En effet, pour tout \(g\in C\),
              \[
                \langle f-f_+,g-f_+\rangle
                =\int_{\{f<0\}}f(x)g(x)\,dx\le0.
              \]
              C’est la caractérisation variationnelle de la projection sur un convexe fermé d’un espace de Hilbert.</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> L’espace est réel ; l’inégalité sur \(f_-\) ferme la preuve sans choix de représentant ponctuel.</aside>
          <footer><a href="{{ repertoire_pdf }}#page=57">Comparer au fac-similé · p. 54 du livre</a></footer>
        </article>
        <article id="probleme-natif-113" data-repertoire-native-problem="113" data-repertoire-audit-problem="113">
          <header><div><span>Problème 113</span><h4>Une isométrie d’un compact dans lui-même</h4></div><strong>Correct</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-113">
            <h5 id="enonce-113">Énoncé</h5>
            <p>Soit \((X,d)\) un espace métrique compact et \(f:X\to X\) une isométrie. Montrer que \(f\) est surjective.</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Suite séparée</small></summary>
            <div>
              <p>L’application \(f\) est injective et \(f(X)\) est compact, donc fermé. Supposons qu’il existe \(x_0\notin f(X)\). Alors
              \[
                \delta=d(x_0,f(X))>0.
              \]
              Posons \(x_n=f^n(x_0)\). Pour tout \(m>n\),
              \[
                d(x_n,x_m)=d(x_0,x_{m-n})\ge\delta,
              \]
              car \(x_{m-n}\in f(X)\). La suite \((x_n)\) est donc \(\delta\)-séparée et ne possède aucune sous-suite convergente, en contradiction avec la compacité de \(X\). Ainsi \(f(X)=X\).</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> La distance à l’image est strictement positive parce que \(f(X)\) est compact, donc fermé.</aside>
          <footer><a href="{{ repertoire_pdf }}#page=58">Comparer au fac-similé · p. 55 du livre</a></footer>
        </article>
        <article id="probleme-natif-114" data-repertoire-native-problem="114" data-repertoire-audit-problem="114">
          <header><div><span>Problème 114</span><h4>Compacité de la boule unité et dimension finie</h4></div><strong>Élégant</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-114">
            <h5 id="enonce-114">Énoncé</h5>
            <p>Soit \(E\) un espace vectoriel normé. Montrer que \(E\) est de dimension finie si et seulement si sa boule unité fermée est compacte.</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Recouvrement fini et itération</small></summary>
            <div>
              <p>En dimension finie, c’est le théorème de Heine–Borel. Réciproquement, supposons la boule unité fermée \(B\) compacte. Elle admet un recouvrement fini par des boules de rayon \(1/2\), centrées en \(x_1,\ldots,x_N\in B\). Posons \(F=\operatorname{Vect}(x_1,\ldots,x_N)\). On a
              \[
                B\subset F+\frac12B.
              \]
              En itérant,
              \[
                B\subset F+2^{-k}B\qquad(k\ge1).
              \]
              Pour tout \(x\in B\), la distance de \(x\) à \(F\) est donc au plus \(2^{-k}\) pour tout \(k\), donc elle est nulle. Le sous-espace \(F\), de dimension finie, est fermé ; ainsi \(x\in F\). On a \(B\subset F\), puis \(E=F\).</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> L’itération utilise seulement \(F+F=F\) et \(\frac12F\subset F\).</aside>
          <footer><a href="{{ repertoire_pdf }}#page=58">Comparer au fac-similé · p. 55 du livre</a></footer>
        </article>
        <article id="probleme-natif-115" data-repertoire-native-problem="115" data-repertoire-audit-problem="115">
          <header><div><span>Problème 115</span><h4>Noyau d’une forme linéaire discontinue</h4></div><strong>Correct</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-115">
            <h5 id="enonce-115">Énoncé</h5>
            <p>Soit \(\ell:E\to\mathbb K\) une forme linéaire sur un espace vectoriel normé. Montrer que \(\ker\ell\) est fermé ou dense dans \(E\).</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Normalisation d’une suite</small></summary>
            <div>
              <p>Si \(\ell\) est continue, son noyau est fermé. Supposons \(\ell\) discontinue. Elle est alors non bornée sur la boule unité. On peut choisir \(y_n\) avec \(\lVert y_n\rVert\le1\) et \(|\ell(y_n)|\ge n\). En posant
              \[
                x_n=\frac{y_n}{\ell(y_n)},
              \]
              on a \(\ell(x_n)=1\) et \(x_n\to0\). Pour tout \(y\in E\),
              \[
                y-\ell(y)x_n\in\ker\ell
                \quad\text{et}\quad
                y-\ell(y)x_n\longrightarrow y.
              \]
              Tout élément de \(E\) appartient donc à l’adhérence du noyau. Celui-ci est dense.</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> La normalisation impose simultanément \(\ell(x_n)=1\) et \(x_n\to0\).</aside>
          <footer><a href="{{ repertoire_pdf }}#page=58">Comparer au fac-similé · p. 55 du livre</a></footer>
        </article>
        <article id="probleme-natif-116" data-repertoire-native-problem="116" data-repertoire-audit-problem="116">
          <header><div><span>Problème 116</span><h4>Connexité de la sphère unité</h4></div><strong>Correct</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-116">
            <h5 id="enonce-116">Énoncé</h5>
            <p>Soit \(E\) un espace vectoriel normé réel de dimension au moins \(2\). Montrer que sa sphère unité est connexe par arcs.</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Normalisation d’un segment</small></summary>
            <div>
              <p>Soient \(x,y\) deux vecteurs unitaires. Si \(y\ne-x\), le segment \([x,y]\) ne contient pas \(0\), et
              \[
                \gamma(t)=\frac{(1-t)x+ty}{\lVert(1-t)x+ty\rVert},
                \qquad 0\le t\le1,
              \]
              est un chemin continu dans la sphère reliant \(x\) à \(y\). En effet, \((1-t)x+ty=0\) avec \(x,y\) unitaires imposerait \(t=\frac12\) puis \(y=-x\).</p>
              <p>Si \(y=-x\), choisissons un vecteur unitaire \(z\) non colinéaire à \(x\), ce qui est possible puisque \(\dim E\ge2\). On relie \(x\) à \(z\), puis \(z\) à \(-x\), par deux chemins de la forme précédente.</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> Le seul segment passant par l’origine entre deux points de la sphère est celui joignant deux points antipodaux.</aside>
          <footer><a href="{{ repertoire_pdf }}#page=59">Comparer au fac-similé · p. 56 du livre</a></footer>
        </article>
        <article id="probleme-natif-117" data-repertoire-native-problem="117" data-repertoire-audit-problem="117">
          <header><div><span>Problème 117</span><h4>Peut-on rendre \(\mathbb Q\) complet ?</h4></div><strong>Correct</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-117">
            <h5 id="enonce-117">Énoncé</h5>
            <p>Existe-t-il une métrique sur l’ensemble \(\mathbb Q\) qui le rende complet ? Peut-on en choisir une qui induise la topologie usuelle de \(\mathbb Q\) ?</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Métrique transportée et théorème de Baire</small></summary>
            <div>
              <p>Oui pour la première question. L’ensemble \(\mathbb Q\) est dénombrable ; choisissons une bijection
              \[
                \phi:\mathbb Q\longrightarrow\{0\}\cup\{1/n:n\ge1\}
              \]
              et posons \(d(x,y)=|\phi(x)-\phi(y)|\). L’espace obtenu est isométrique à un compact de \(\mathbb R\) ; il est donc compact et complet.</p>
              <p>En revanche, aucune métrique complète ne peut induire sur \(\mathbb Q\) sa topologie usuelle. Un espace complètement métrisable est un espace de Baire. Or \(\mathbb Q\), muni de sa topologie usuelle, est la réunion dénombrable de ses singletons, qui sont fermés et d’intérieur vide. Il n’est pas de Baire.</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> La première métrique n’a aucune raison de conserver la topologie usuelle ; la seconde question est donc réellement distincte.</aside>
          <footer><a href="{{ repertoire_pdf }}#page=59">Comparer au fac-similé · p. 56 du livre</a></footer>
        </article>
        <article id="probleme-natif-118" data-repertoire-native-problem="118" data-repertoire-audit-problem="118">
          <header><div><span>Problème 118</span><h4>Un espace vectoriel topologique complet non normable</h4></div><strong>Calcul vérifié</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-118">
            <h5 id="enonce-118">Énoncé</h5>
            <p>Donner un exemple naturel d’espace vectoriel topologique métrisable et complet dont la topologie ne provient d’aucune norme.</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>L’espace de Fréchet \(\mathcal C^\infty([0,1])\)</small></summary>
            <div>
              <p>L’espace \(E=\mathcal C^\infty([0,1])\), muni des semi-normes
              \[
                p_k(f)=\max_{0\le j\le k}\lVert f^{(j)}\rVert_\infty,
                \qquad k\in\mathbb N,
              \]
              est un espace de Fréchet. Une métrique compatible est
              \[
                d(f,g)=\sum_{k=0}^{\infty}2^{-k}
                \frac{p_k(f-g)}{1+p_k(f-g)}.
              \]
              Une suite de Cauchy pour cette métrique est uniformément de Cauchy avec chacune de ses dérivées. Les limites uniformes se recollent par le théorème fondamental de l’analyse : la limite de \(f_n^{(j+1)}\) est la dérivée de la limite de \(f_n^{(j)}\). L’espace est donc complet.</p>
              <p>Il n’est pas normable. Supposons qu’une norme \(\lVert\cdot\rVert\) définisse cette topologie. Sa boule unité ouverte contient un voisinage de base : il existe \(m\in\mathbb N\) et \(\varepsilon>0\) tels que
              \[
                p_m(f)<\varepsilon\Longrightarrow\lVert f\rVert<1.
              \]
              Comme \(p_{m+1}\) est continue pour la topologie supposée normique, il existe \(C>0\) tel que \(p_{m+1}(f)\le C\lVert f\rVert\). Le semi-norme \(p_{m+1}\) serait donc borné par \(C\) sur \(\{p_m<\varepsilon\}\).</p>
              <p>C’est impossible. Pour \(N\ge1\), posons
              \[
                f_N(x)=\frac{\varepsilon}{2(2\pi N)^m}\sin(2\pi Nx).
              \]
              Alors \(p_m(f_N)\le\varepsilon/2\), tandis que
              \[
                p_{m+1}(f_N)=\varepsilon\pi N\longrightarrow\infty.
              \]
              Cette contradiction prouve que la topologie de \(E\) ne provient d’aucune norme.</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> Le facteur de normalisation donne exactement \(p_m(f_N)\le\varepsilon/2\) et \(p_{m+1}(f_N)=\varepsilon\pi N\).</aside>
          <footer><a href="{{ repertoire_pdf }}#page=59">Comparer au fac-similé · pp. 56–57 du livre</a></footer>
        </article>
        <article id="probleme-natif-119" data-repertoire-native-problem="119" data-repertoire-audit-problem="119">
          <header><div><span>Problème 119</span><h4>Deux métriques équivalentes, une seule complète</h4></div><strong>Correct</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-119">
            <h5 id="enonce-119">Énoncé</h5>
            <p>Donner sur un même ensemble deux métriques induisant la même topologie, l’une complète et l’autre non.</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Transport par \(\arctan\)</small></summary>
            <div>
              <p>Sur \(\mathbb R\), la métrique usuelle \(d_0(x,y)=|x-y|\) est complète. La métrique
              \[
                d_1(x,y)=|\arctan x-\arctan y|
              \]
              induit la même topologie, puisque \(\arctan\) est un homéomorphisme de \(\mathbb R\) sur \((-\pi/2,\pi/2)\).</p>
              <p>Cependant, la suite \(x_n=n\) est de Cauchy pour \(d_1\), car \(\arctan n\to\pi/2\), mais elle n’a pas de limite dans \(\mathbb R\) pour cette métrique. Ainsi \(d_1\) n’est pas complète. La complétude dépend de la métrique, et non de la seule topologie.</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> Les deux métriques ont exactement les mêmes ouverts, mais pas les mêmes suites de Cauchy.</aside>
          <footer><a href="{{ repertoire_pdf }}#page=60">Comparer au fac-similé · p. 57 du livre</a></footer>
        </article>
        <article id="probleme-natif-120" data-repertoire-native-problem="120" data-repertoire-audit-problem="120">
          <header><div><span>Problème 120</span><h4>Compacité séquentielle dans les espaces métriques</h4></div><strong>Preuve complète</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-120">
            <h5 id="enonce-120">Énoncé</h5>
            <p>Montrer qu’un espace métrique \((X,d)\) est compact si et seulement si toute suite de \(X\) possède une valeur d’adhérence, ou, de manière équivalente, une sous-suite convergente.</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Totale bornitude et nombre de Lebesgue</small></summary>
            <div>
              <p>Supposons \(X\) compact. Si une suite \((x_n)\) ne possédait aucune valeur d’adhérence, chaque point \(x\in X\) aurait un voisinage ne contenant qu’un nombre fini de termes de la suite. Un sous-recouvrement fini de ces voisinages ne contiendrait alors qu’un nombre fini de termes, contradiction. Dans un espace métrique, une valeur d’adhérence permet d’extraire une sous-suite convergente.</p>
              <p>Réciproquement, supposons toute suite pourvue d’une sous-suite convergente. L’espace est totalement borné : sinon, pour un certain \(\varepsilon>0\), on construirait par récurrence une suite dont les termes sont deux à deux à distance au moins \(\varepsilon\), sans sous-suite convergente.</p>
              <p>Soit \((U_i)_{i\in I}\) un recouvrement ouvert de \(X\). Il possède un nombre de Lebesgue : il existe \(\delta>0\) tel que toute boule de rayon \(\delta\) soit contenue dans l’un des \(U_i\). Sinon, on choisirait \(x_n\) tel que \(B(x_n,1/n)\) ne soit contenu dans aucun \(U_i\). Une sous-suite convergerait vers \(x\in U_{i_0}\) ; pour \(n\) assez grand, la boule correspondante serait pourtant contenue dans \(U_{i_0}\), contradiction.</p>
              <p>Enfin, une famille finie de boules de rayon \(\delta\) recouvre \(X\) par totale bornitude. En choisissant pour chacune un \(U_i\) qui la contient, on obtient un sous-recouvrement fini. L’espace est compact.</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> La réciproque contient bien les trois étapes souvent condensées : totale bornitude, nombre de Lebesgue, sous-recouvrement fini.</aside>
          <footer><a href="{{ repertoire_pdf }}#page=60">Comparer au fac-similé · pp. 57–58 du livre</a></footer>
        </article>
        <article class="repertoire-native-featured" id="probleme-natif-121" data-repertoire-native-problem="121" data-repertoire-audit-problem="121">
          <header><div><span>Problème 121</span><h4>Une fonction lisse dont un jet s’annule en chaque point</h4></div><strong>Point culminant</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-121">
            <h5 id="enonce-121">Énoncé</h5>
            <p>Soit \(f\in\mathcal C^\infty(\mathbb R)\) telle que
            \[
              \forall x\in\mathbb R,\quad \exists n\in\mathbb N,\quad f^{(n)}(x)=0.
            \]
            Montrer que \(f\) est un polynôme.</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Théorème de Baire et recollement</small></summary>
            <div>
              <p>Pour \(n\in\mathbb N\), posons
              \[
                S_n=\{x\in\mathbb R:f^{(n)}(x)=0\},
              \]
              et soit \(X\) l’ensemble des points au voisinage desquels \(f\) n’est égale à aucun polynôme. L’ensemble \(X\) est fermé. Il n’a pas de point isolé : si \(x\) était isolé dans \(X\), la fonction serait polynomiale sur chacun des deux côtés de \(x\) ; la régularité \(\mathcal C^\infty\) forcerait les deux polynômes à avoir le même jet en \(x\), donc à coïncider.</p>
              <p>Supposons \(X\) non vide. C’est alors un espace complet et
              \[
                X=\bigcup_{n\in\mathbb N}(X\cap S_n).
              \]
              Le théorème de Baire fournit un entier \(n\) et un intervalle ouvert \(I\) tels que
              \[
                \varnothing\ne X\cap I\subset S_n.
              \]
              Chaque point de \(X\cap I\) est un point d’accumulation de cet ensemble. En dérivant successivement le long de suites de points de \(X\cap I\), on obtient
              \[
                f^{(m)}(x)=0
                \qquad(x\in X\cap I,\ m\ge n).
              \]</p>
              <p>Sur chaque composante connexe \(J\) de \(I\setminus X\), la fonction \(f\) est localement polynomiale ; les polynômes locaux se recollent, donc \(f\) coïncide sur \(J\) avec un unique polynôme \(P_J\). Toute telle composante possède au moins une extrémité appartenant à \(X\cap I\). En cette extrémité, toutes les dérivées d’ordre au moins \(n\) s’annulent. Cela impose \(\deg P_J<n\). Par conséquent \(f^{(n)}=0\) sur \(J\), et aussi sur \(X\cap I\). Ainsi \(f^{(n)}=0\) sur tout \(I\), donc \(f\) y est polynomiale, contradiction avec \(X\cap I\ne\varnothing\).</p>
              <p>On a donc \(X=\varnothing\) : \(f\) est localement polynomiale partout. Sur l’intervalle connexe \(\mathbb R\), les polynômes locaux coïncident sur leurs recouvrements et se recollent en un seul polynôme global.</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> Les quatre passages délicats sont explicités : fermeture et absence de points isolés, Baire, propagation aux dérivées supérieures, puis degré uniforme sur les composantes.</aside>
          <footer><a href="{{ repertoire_pdf }}#page=61">Comparer au fac-similé · p. 58 du livre</a></footer>
        </article>
      </div>
    </section>

    <section class="repertoire-native-chapter" aria-labelledby="native-chapter-15">
      <header>
        <span>15</span>
        <div>
          <h3 id="native-chapter-15">Probabilités et problème des moments</h3>
          <p>Problèmes 122–125 · quatre énoncés et solutions</p>
        </div>
      </header>
      {% include repertoire-native-references.html chapter_id="probabilites-moments" %}
      <div class="repertoire-native-list">
        <article id="probleme-natif-122" data-repertoire-native-problem="122" data-repertoire-audit-problem="122">
          <header><div><span>Problème 122</span><h4>Convergence en probabilité sans convergence presque sûre</h4></div><strong>Correct</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-122">
            <h5 id="enonce-122">Énoncé</h5>
            <p>Construire une suite de variables aléatoires qui converge en probabilité vers \(0\), mais pas presque sûrement.</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Second lemme de Borel–Cantelli</small></summary>
            <div>
              <p>Soit \((X_n)_{n\ge1}\) une suite indépendante telle que \(X_n\) suive une loi de Bernoulli de paramètre \(1/n\). Pour \(0<\varepsilon<1\),
              \[
                \mathbb P(|X_n|>\varepsilon)=\mathbb P(X_n=1)=\frac1n\longrightarrow0.
              \]
              Ainsi \(X_n\to0\) en probabilité.</p>
              <p>En revanche,
              \[
                \sum_{n=1}^{\infty}\mathbb P(X_n=1)
                =\sum_{n=1}^{\infty}\frac1n=\infty.
              \]
              Par le second lemme de Borel–Cantelli, l’indépendance implique
              \[
                \mathbb P(X_n=1\ \text{une infinité de fois})=1.
              \]
              Presque sûrement, la suite ne converge donc pas vers \(0\).</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> L’indépendance, indispensable pour Borel–Cantelli II, est bien incluse dans la construction.</aside>
          <footer><a href="{{ repertoire_pdf }}#page=62">Comparer au fac-similé · p. 59 du livre</a></footer>
        </article>
        <article id="probleme-natif-123" data-repertoire-native-problem="123" data-repertoire-audit-problem="123">
          <header><div><span>Problème 123</span><h4>La convergence en loi n’implique pas la convergence en probabilité</h4></div><strong>Correct</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-123">
            <h5 id="enonce-123">Énoncé</h5>
            <p>Donner un contre-exemple explicite.</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Variables de Bernoulli indépendantes</small></summary>
            <div>
              <p>Sur un même espace probabilisé, prenons une variable \(X\) et une suite \((X_n)\) indépendantes, toutes de loi de Bernoulli de paramètre \(1/2\). Pour tout \(n\), \(X_n\) et \(X\) ont exactement la même loi. La suite \((X_n)\) converge donc en loi vers \(X\).</p>
              <p>Cependant,
              \[
                \mathbb P(|X_n-X|>1/2)
                =\mathbb P(X_n\ne X)=\frac12
              \]
              pour tout \(n\). Il n’y a pas convergence en probabilité.</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> Le calcul vaut \(\frac14+\frac14=\frac12\) pour chaque \(n\).</aside>
          <footer><a href="{{ repertoire_pdf }}#page=62">Comparer au fac-similé · p. 59 du livre</a></footer>
        </article>
        <article id="probleme-natif-124" data-repertoire-native-problem="124" data-repertoire-audit-problem="124">
          <header><div><span>Problème 124</span><h4>Continuité de la fonction caractéristique</h4></div><strong>Correct</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-124">
            <h5 id="enonce-124">Énoncé</h5>
            <p>Soit \(X\) une variable aléatoire à valeurs dans \(\mathbb R^d\). Montrer que sa fonction caractéristique
            \[
              \varphi_X(t)=\mathbb E\!\left[e^{i\langle t,X\rangle}\right]
            \]
            est continue sur \(\mathbb R^d\).</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Convergence dominée</small></summary>
            <div>
              <p>Si \(t_n\to t\), alors
              \[
                e^{i\langle t_n,X\rangle}\longrightarrow e^{i\langle t,X\rangle}
              \]
              presque sûrement. Tous ces termes ont un module égal à \(1\). Le théorème de convergence dominée donne
              \[
                \varphi_X(t_n)\longrightarrow\varphi_X(t).
              \]
              Aucune hypothèse de moment sur \(X\) n’est nécessaire.</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> Le dominateur constant \(1\) évite toute condition d’intégrabilité supplémentaire.</aside>
          <footer><a href="{{ repertoire_pdf }}#page=62">Comparer au fac-similé · pp. 59–60 du livre</a></footer>
        </article>
        <article class="repertoire-native-featured" id="probleme-natif-125" data-repertoire-native-problem="125" data-repertoire-audit-problem="125">
          <header><div><span>Problème 125</span><h4>La loi log-normale n’est pas déterminée par ses moments</h4></div><strong>Calcul revérifié</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-125">
            <h5 id="enonce-125">Énoncé</h5>
            <p>Soit \(X\) telle que \(\log X\) suive la loi normale \(\mathcal N(\mu,\sigma^2)\), avec \(\sigma>0\). Construire une famille de lois distinctes possédant tous les mêmes moments entiers positifs que \(X\).</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Famille de Stieltjes log-normale</small></summary>
            <div>
              <p>La densité log-normale est
              \[
                p(x)=\frac{1}{x\sigma\sqrt{2\pi}}
                \exp\!\left(-\frac{(\log x-\mu)^2}{2\sigma^2}\right),
                \qquad x>0.
              \]
              Pour \(|\varepsilon|\le1\), posons
              \[
                p_\varepsilon(x)=p(x)\left[
                  1+\varepsilon\sin\!\left(
                    \frac{2\pi(\log x-\mu)}{\sigma^2}
                  \right)\right].
              \]
              Le facteur entre crochets appartient à \([0,2]\), donc \(p_\varepsilon\) est positive.</p>
              <p>Montrons que la perturbation ne modifie aucun moment. Si \(Z=\log X-\mu\sim\mathcal N(0,\sigma^2)\) et \(n\in\mathbb N\), l’intégrale perturbatrice vaut
              \[
                e^{n\mu}\,
                \operatorname{Im}\mathbb E\!\left[
                  \exp\!\left(\left(n+\frac{2\pi i}{\sigma^2}\right)Z\right)
                \right].
              \]
              Or, pour \(w\in\mathbb C\),
              \[
                \mathbb E[e^{wZ}]=\exp\!\left(\frac{\sigma^2w^2}{2}\right).
              \]
              Avec \(w=n+2\pi i/\sigma^2\),
              \[
                \frac{\sigma^2w^2}{2}
                =\frac{\sigma^2n^2}{2}+2\pi in-\frac{2\pi^2}{\sigma^2}.
              \]
              Le facteur \(e^{2\pi in}=1\) rend cette espérance réelle, donc l’intégrale perturbatrice est nulle.</p>
              <p>Pour \(n=0\), cela montre aussi que \(p_\varepsilon\) est de masse totale \(1\). Toutes les densités \(p_\varepsilon\) ont donc les moments
              \[
                \mathbb E[X^n]
                =\exp\!\left(n\mu+\frac{n^2\sigma^2}{2}\right).
              \]
              Elles sont distinctes dès que les paramètres \(\varepsilon\) le sont, car la fonction sinus n’est pas nulle presque partout.</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> Le cas \(n=0\) vérifie la masse, \(|\varepsilon|\le1\) la positivité, et le facteur \(e^{2\pi in}\) l’égalité de tous les moments.</aside>
          <footer><a href="{{ repertoire_pdf }}#page=63">Comparer au fac-similé · p. 60 du livre</a></footer>
        </article>
      </div>
    </section>

    <section class="repertoire-native-chapter" aria-labelledby="native-chapter-16">
      <header>
        <span>16</span>
        <div>
          <h3 id="native-chapter-16">Fonctions d’une variable réelle</h3>
          <p>Problèmes 126–127 · deux énoncés et solutions</p>
        </div>
      </header>
      {% include repertoire-native-references.html chapter_id="suites-fonctions-reelles" %}
      <div class="repertoire-native-list">
        <article id="probleme-natif-126" data-repertoire-native-problem="126" data-repertoire-audit-problem="126">
          <header><div><span>Problème 126</span><h4>Toutes les dérivées dominées par un polynôme de degré impair</h4></div><strong>Correct</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-126">
            <h5 id="enonce-126">Énoncé</h5>
            <p>Soit \(f\in\mathcal C^\infty(\mathbb R)\) et supposons qu’il existe un polynôme réel \(P\) de degré impair tel que
            \[
              |f^{(m)}(x)|\le |P(x)|
              \qquad(m\in\mathbb N,\ x\in\mathbb R).
            \]
            Déterminer \(f\).</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Taylor à tout ordre</small></summary>
            <div>
              <p>Le polynôme \(P\) possède une racine réelle \(x_0\). L’inégalité impose
              \[
                f^{(m)}(x_0)=0\qquad(m\in\mathbb N).
              \]
              Fixons \(x\in\mathbb R\) et notons
              \[
                M_x=\max_{t\in[x_0,x]}|P(t)|,
              \]
              l’intervalle étant pris sans orientation. La formule de Taylor avec reste intégral, tous les coefficients en \(x_0\) étant nuls, donne pour tout \(N\ge0\)
              \[
                |f(x)|\le M_x\frac{|x-x_0|^{N+1}}{(N+1)!}.
              \]
              Le membre de droite tend vers \(0\) lorsque \(N\to\infty\). Ainsi \(f(x)=0\) pour tout \(x\), donc \(f\equiv0\).</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> Pour \(x\) fixé, \(M_x\) ne dépend pas de l’ordre \(N\), ce qui autorise le passage à la limite.</aside>
          <footer><a href="{{ repertoire_pdf }}#page=64">Comparer au fac-similé · p. 61 du livre</a></footer>
        </article>
        <article id="probleme-natif-127" data-repertoire-native-problem="127" data-repertoire-audit-problem="127">
          <header><div><span>Problème 127</span><h4>Bornitude des dérivées intermédiaires</h4></div><strong>Matrice vérifiée</strong></header>
          <section class="repertoire-native-statement" aria-labelledby="enonce-127">
            <h5 id="enonce-127">Énoncé</h5>
            <p>Soit \(n\ge1\) et \(f\in\mathcal C^n(\mathbb R,\mathbb C)\). On suppose que \(f\) et \(f^{(n)}\) sont bornées. Montrer que toutes les dérivées \(f^{(k)}\), \(0\le k\le n\), sont bornées.</p>
          </section>
          <details class="repertoire-native-solution">
            <summary><span>Afficher la solution</span><small>Système de Taylor et Vandermonde</small></summary>
            <div>
              <p>Le cas \(n=1\) est immédiat. Supposons \(n\ge2\) et posons \(M_0=\lVert f\rVert_\infty\), \(M_n=\lVert f^{(n)}\rVert_\infty\). Pour \(j=1,\ldots,n-1\), la formule de Taylor avec reste intégral donne
              \[
                f(x+j)-f(x)
                =\sum_{k=1}^{n-1}\frac{j^k}{k!}f^{(k)}(x)+R_j(x),
                \qquad
                |R_j(x)|\le\frac{j^n}{n!}M_n.
              \]
              Le vecteur
              \[
                Y(x)=\bigl(f(x+j)-f(x)-R_j(x)\bigr)_{1\le j\le n-1}
              \]
              est donc uniformément borné.</p>
              <p>On a \(Y(x)=AX(x)\), où
              \[
                X(x)=\bigl(f'(x),\ldots,f^{(n-1)}(x)\bigr)^{\mathsf T},
                \qquad
                A_{jk}=\frac{j^k}{k!}.
              \]
              Après multiplication de la \(k\)-ième colonne par \(k!\), puis division de la \(j\)-ième ligne par \(j\), on obtient la matrice de Vandermonde
              \[
                (j^{k-1})_{1\le j,k\le n-1}.
              \]
              Les nombres \(1,\ldots,n-1\) étant distincts, \(A\) est inversible. Ainsi \(X(x)=A^{-1}Y(x)\) est uniformément borné. Toutes les dérivées intermédiaires sont bornées.</p>
            </div>
          </details>
          <aside><strong>Point de relecture.</strong> Les restes sont uniformes en \(x\), et la réduction à Vandermonde vérifie explicitement l’inversibilité de \(A\).</aside>
          <footer><a href="{{ repertoire_pdf }}#page=64">Comparer au fac-similé · pp. 61–62 du livre</a></footer>
        </article>
      </div>
    </section>
  </section>

  <section class="repertoire-errata" id="errata" aria-labelledby="repertoire-errata-title">
    <div class="repertoire-section-heading">
      <div>
        <p class="repertoire-kicker">Registre de relecture</p>
        <h2 id="repertoire-errata-title">Une correction, quatre précisions</h2>
      </div>
      <p>Les 127 résultats restent valides.</p>
    </div>
    <article class="repertoire-erratum-major">
      <header><a href="{{ repertoire_pdf }}#page=40">Problème 80 · page 37 du livre</a><span>Correction mathématique</span></header>
      <p>Pour une fonction complexe, la limite de \(\int fP_k\) avec \(P_k\to f\) est \(\int f^2\), et non \(\int |f|^2\). Il faut conjuguer l’hypothèse et, pour \(P_k\to f\) uniformément, écrire
      \[
        0=\lim_{k\to\infty}\int_0^1 \overline f\,P_k
        =\int_0^1 |f|^2.
      \]
      Cette retouche d’une ligne rétablit la preuve sans modifier l’énoncé.</p>
    </article>
    <article>
      <header><a href="{{ repertoire_pdf }}#page=6">Problème 4 · page 3 du livre</a><span>Titre</span></header>
      <p><strong>À lire :</strong> « réductible dans \(\mathbb F_p[X]\) pour tout nombre premier \(p\) », ou plus brièvement « réductible modulo tout nombre premier ». L’expression « sur tout corps premier » inclurait improprement \(\mathbb Q\).</p>
    </article>
    <article>
      <header><a href="{{ repertoire_pdf }}#page=6">Problème 6 · page 3 du livre</a><span>Quantification</span></header>
      <p><strong>À lire :</strong> « Pour \(s\in\{0,\ldots,r-1\}\), l’orbite de \(\alpha^{q^s}\) sous \(x\mapsto x^{q^r}\) a longueur \(d/r\). » Le calcul et la conclusion restent inchangés.</p>
    </article>
    <article>
      <header><a href="{{ repertoire_pdf }}#page=46">Problème 91 · page 43 du livre</a><span>Convention complexe</span></header>
      <p>Le crochet bilinéaire employé est licite parce que les fonctions test \(x^{1/k}\) sont réelles : les conditions bilinéaire et hermitienne se déduisent l’une de l’autre par conjugaison. Une demi-phrase suffit à lever l’ambiguïté.</p>
    </article>
    <article>
      <header><a href="{{ repertoire_pdf }}#page=54">Problème 106 · page 51 du livre</a><span>Convention complexe</span></header>
      <p>La même précision vaut pour les translatées de la gaussienne, qui sont réelles. On peut aussi déclarer explicitement que l’espace \(L^2\) considéré est réel.</p>
    </article>
  </section>

  <section class="repertoire-notes" aria-labelledby="repertoire-notes-title">
    <div>
      <p class="repertoire-kicker">Pour une prochaine édition</p>
      <h2 id="repertoire-notes-title">Ce que la page prépare</h2>
    </div>
    <ul>
      <li>reprendre progressivement les formules extraites en MathJax éditorial ;</li>
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
