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

  <section class="repertoire-audit" id="bilan-relecture" aria-labelledby="repertoire-audit-title">
    <div class="repertoire-section-heading">
      <div>
        <p class="repertoire-kicker">Clôture de la relecture</p>
        <h2 id="repertoire-audit-title">Relecture détaillée des 17 derniers problèmes</h2>
      </div>
      <p>Chapitres 14 à 16 du PDF</p>
    </div>
    <p class="repertoire-audit-intro">Chaque notice expose ici le point décisif qui ferme la preuve ; le lien sur son titre permet seulement de retrouver l’énoncé et la solution complète dans le livre. La numérotation des chapitres est celle du PDF.</p>

    <section class="repertoire-audit-chapter" aria-labelledby="audit-chapter-14">
      <header>
        <span>14</span>
        <div>
          <h3 id="audit-chapter-14">Topologie et analyse fonctionnelle</h3>
          <p>Problèmes 111–121 · onze preuves vérifiées</p>
        </div>
      </header>
      <div class="repertoire-audit-list">
        <article data-repertoire-audit-problem="111">
          <header><h4><a href="{{ repertoire_pdf }}#page=57">111 · Point fixe d’une application non expansive</a></h4><span>Correct</span></header>
          <p>L’approximation \(f_n=\frac1n a+(1-\frac1n)f\) reste dans \(K\) par convexité et contracte de rapport \(1-\frac1n\). Banach s’applique puisque le compact \(K\) est complet ; puis \(x_n-f(x_n)=\frac1n(a-f(x_n))\to0\), et la compacité fournit un point fixe de \(f\).</p>
        </article>
        <article data-repertoire-audit-problem="112">
          <header><h4><a href="{{ repertoire_pdf }}#page=57">112 · Projection sur le cône positif de \(L^2\)</a></h4><span>Correct</span></header>
          <p>L’espace est bien réel. Si \(f_n\ge0\) et \(f_n\to f\), alors \(\lVert f_-\rVert_2\le\lVert f-f_n\rVert_2\), donc le cône est fermé. La partie positive \(f_+\) vérifie ensuite la caractérisation variationnelle de la projection : \(\langle f-f_+,g-f_+\rangle\le0\) pour tout \(g\ge0\).</p>
        </article>
        <article data-repertoire-audit-problem="113">
          <header><h4><a href="{{ repertoire_pdf }}#page=58">113 · Une isométrie d’un compact dans lui-même</a></h4><span>Correct</span></header>
          <p>Si \(x_0\notin f(X)\), la distance \(\delta=d(x_0,f(X))\) est positive. Les itérés \(x_n=f^n(x_0)\) sont alors \(\delta\)-séparés, car \(d(x_n,x_m)=d(x_0,x_{m-n})\ge\delta\), ce qui contredit la compacité.</p>
        </article>
        <article data-repertoire-audit-problem="114">
          <header><h4><a href="{{ repertoire_pdf }}#page=58">114 · Compacité de la boule unité et dimension finie</a></h4><span>Correct · élégant</span></header>
          <p>Un recouvrement fini de la boule unité \(B\) par des boules de rayon \(1/2\) donne \(B\subset F+\frac12B\), où \(F\) est de dimension finie. L’itération \(B\subset F+2^{-k}B\) force \(\operatorname{dist}(x,F)=0\) ; comme \(F\) est fermé, \(B\subset F\), puis \(E=F\).</p>
        </article>
        <article data-repertoire-audit-problem="115">
          <header><h4><a href="{{ repertoire_pdf }}#page=58">115 · Noyau d’une forme linéaire discontinue</a></h4><span>Correct</span></header>
          <p>La discontinuité fournit \(x_n\to0\) avec \(\ell(x_n)=1\). Pour tout \(y\), les vecteurs \(y-\ell(y)x_n\) appartiennent à \(\ker\ell\) et convergent vers \(y\), ce qui prouve la densité du noyau dans le seul cas où il n’est pas fermé.</p>
        </article>
        <article data-repertoire-audit-problem="116">
          <header><h4><a href="{{ repertoire_pdf }}#page=59">116 · Connexité de la sphère unité</a></h4><span>Correct</span></header>
          <p>Le segment \([x,y]\) évite \(0\) lorsque \(y\ne-x\) : une combinaison convexe nulle de deux vecteurs unitaires imposerait \(t=\frac12\) et \(y=-x\). Sa normalisation donne donc un chemin ; dans le cas antipodal, un troisième vecteur non colinéaire permet de concaténer deux tels chemins.</p>
        </article>
        <article data-repertoire-audit-problem="117">
          <header><h4><a href="{{ repertoire_pdf }}#page=59">117 · Peut-on rendre \(\mathbb Q\) complet ?</a></h4><span>Correct</span></header>
          <p>Une bijection de \(\mathbb Q\) sur \(\{0\}\cup\{1/n:n\ge1\}\) transporte une métrique compacte, donc complète. En revanche, la topologie usuelle de \(\mathbb Q\) est une réunion dénombrable de singletons fermés d’intérieur vide : l’obstruction de Baire interdit toute métrique complète compatible.</p>
        </article>
        <article data-repertoire-audit-problem="118">
          <header><h4><a href="{{ repertoire_pdf }}#page=59">118 · Un espace de Fréchet non normable</a></h4><span>Correct · calcul vérifié</span></header>
          <p>Dans \(\mathcal C^\infty([0,1])\), une norme compatible rendrait \(p_{m+1}\) bornée sur un voisinage défini par \(p_m\). Or \(f_N(x)=\frac{\varepsilon}{2(2\pi N)^m}\sin(2\pi Nx)\) vérifie \(p_m(f_N)\le\varepsilon/2\) tandis que \(p_{m+1}(f_N)=\varepsilon\pi N\to\infty\).</p>
        </article>
        <article data-repertoire-audit-problem="119">
          <header><h4><a href="{{ repertoire_pdf }}#page=60">119 · Deux métriques équivalentes, une seule complète</a></h4><span>Correct</span></header>
          <p>Sur \(\mathbb R\), \(d_1(x,y)=|\arctan x-\arctan y|\) induit la topologie usuelle puisque \(\arctan\) est un homéomorphisme sur \((-\pi/2,\pi/2)\). Pourtant \(n\) est de Cauchy pour \(d_1\) et n’a pas de limite dans \(\mathbb R\) : la complétude dépend bien de la métrique, pas seulement de la topologie.</p>
        </article>
        <article data-repertoire-audit-problem="120">
          <header><h4><a href="{{ repertoire_pdf }}#page=60">120 · Compacité séquentielle dans les espaces métriques</a></h4><span>Correct · complet</span></header>
          <p>La réciproque contient les trois étapes nécessaires : une suite \(\varepsilon\)-séparée exclut le défaut de totale bornitude ; l’argument par sous-suite convergente établit un nombre de Lebesgue ; un recouvrement fini par des boules assez petites fournit alors un sous-recouvrement fini.</p>
        </article>
        <article class="repertoire-audit-featured" data-repertoire-audit-problem="121">
          <header><h4><a href="{{ repertoire_pdf }}#page=61">121 · Un jet nul en chaque point impose un polynôme</a></h4><span>Point culminant</span></header>
          <p>La preuve traite les quatre passages délicats. L’ensemble \(X\) où \(f\) n’est localement aucun polynôme est fermé et sans point isolé. Baire, appliqué à \(X=\bigcup_n(X\cap S_n)\), fournit un intervalle où \(f^{(n)}\) s’annule sur \(X\). Les points de \(X\) y étant d’accumulation, toutes les dérivées d’ordre \(m\ge n\) s’y annulent. Enfin, chaque composante de l’intervalle privé de \(X\) porte un polynôme dont une extrémité appartient à \(X\), donc de degré \(<n\). Ainsi \(f^{(n)}\) s’annule sur tout l’intervalle, contradiction ; les polynômes locaux se recollent alors globalement sur \(\mathbb R\).</p>
        </article>
      </div>
    </section>

    <section class="repertoire-audit-chapter" aria-labelledby="audit-chapter-15">
      <header>
        <span>15</span>
        <div>
          <h3 id="audit-chapter-15">Probabilités et problème des moments</h3>
          <p>Problèmes 122–125 · quatre preuves vérifiées</p>
        </div>
      </header>
      <div class="repertoire-audit-list">
        <article data-repertoire-audit-problem="122">
          <header><h4><a href="{{ repertoire_pdf }}#page=62">122 · Convergence en probabilité sans convergence presque sûre</a></h4><span>Correct</span></header>
          <p>Pour des Bernoulli indépendantes de paramètre \(1/n\), on a \(\mathbb P(|X_n|>\varepsilon)=1/n\to0\). Mais la série des probabilités diverge ; le second lemme de Borel–Cantelli, avec l’indépendance indispensable, donne \(X_n=1\) une infinité de fois presque sûrement.</p>
        </article>
        <article data-repertoire-audit-problem="123">
          <header><h4><a href="{{ repertoire_pdf }}#page=62">123 · La convergence en loi n’implique pas la convergence en probabilité</a></h4><span>Correct</span></header>
          <p>Des variables de Bernoulli indépendantes \(X_n\) et \(X\), toutes de paramètre \(1/2\), ont exactement la même loi : \(X_n\) converge donc en loi vers \(X\). En revanche, \(\mathbb P(X_n\ne X)=1/4+1/4=1/2\) pour tout \(n\).</p>
        </article>
        <article data-repertoire-audit-problem="124">
          <header><h4><a href="{{ repertoire_pdf }}#page=62">124 · Continuité de la fonction caractéristique</a></h4><span>Correct</span></header>
          <p>Si \(t_n\to t\), alors \(e^{i\langle t_n,X\rangle}\to e^{i\langle t,X\rangle}\) presque sûrement et tous les termes ont module \(1\). La convergence dominée suffit : aucune hypothèse de moment sur \(X\) n’est requise.</p>
        </article>
        <article class="repertoire-audit-featured" data-repertoire-audit-problem="125">
          <header><h4><a href="{{ repertoire_pdf }}#page=63">125 · La loi log-normale n’est pas déterminée par ses moments</a></h4><span>Calcul revérifié</span></header>
          <p>Pour \(w=n+2\pi i/\sigma^2\), le terme \(\sigma^2w^2/2\) vaut \(\sigma^2n^2/2+2\pi in-2\pi^2/\sigma^2\). Le facteur \(e^{2\pi in}=1\) rend l’espérance réelle : la perturbation sinusoïdale ne modifie aucun moment entier. Le cas \(n=0\) donne la masse totale \(1\), la positivité vient de \(|\varepsilon|\le1\), et des paramètres distincts produisent bien des lois distinctes.</p>
        </article>
      </div>
    </section>

    <section class="repertoire-audit-chapter" aria-labelledby="audit-chapter-16">
      <header>
        <span>16</span>
        <div>
          <h3 id="audit-chapter-16">Fonctions d’une variable réelle</h3>
          <p>Problèmes 126–127 · deux preuves vérifiées</p>
        </div>
      </header>
      <div class="repertoire-audit-list">
        <article data-repertoire-audit-problem="126">
          <header><h4><a href="{{ repertoire_pdf }}#page=64">126 · Toutes les dérivées dominées par un polynôme impair</a></h4><span>Correct</span></header>
          <p>Une racine réelle \(x_0\) du polynôme annule toutes les dérivées de \(f\) en \(x_0\). Pour \(x\) fixé, \(M_x=\max_{[x_0,x]}|P|\) ne dépend pas de l’ordre \(N\), et Taylor donne \(|f(x)|\le M_x|x-x_0|^{N+1}/(N+1)!\to0\). Ainsi \(f\equiv0\).</p>
        </article>
        <article data-repertoire-audit-problem="127">
          <header><h4><a href="{{ repertoire_pdf }}#page=64">127 · Bornitude des dérivées intermédiaires</a></h4><span>Correct · matrice vérifiée</span></header>
          <p>Les formules de Taylor aux points \(x+j\) donnent un système \(Y(x)=AX(x)\), où \(A_{jk}=j^k/k!\) et \(Y\) est uniformément borné. Après multiplication de la colonne \(k\) par \(k!\), puis division de la ligne \(j\) par \(j\), \(A\) devient la matrice de Vandermonde \((j^{k-1})\) aux nœuds distincts \(1,\ldots,n-1\). Elle est inversible, donc toutes les dérivées intermédiaires sont bornées.</p>
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
