## **Répertoire raisonné d'algèbre et d'analyse**

Questions, exemples, contre-exemples et preuves

**127 problèmes corrigés**

Algèbre, analyse, topologie, probabilités et analyse fonctionnelle.

### **Avant-propos**

Ce recueil rassemble des problèmes courts dont l'intérêt principal réside moins dans le calcul que dans l'identification de l'outil décisif : action de groupe, polynôme minimal, compacité, principe du maximum, transformée de Fourier, argument de Baire, etc. Il est conçu à la fois comme un répertoire de méthodes, une collection de contre-exemples et un support de révision avancée.

La présente édition reprend intégralement les 127 entrées du document initial. Les énoncés ont été homogénéisés, les hypothèses implicites rendues explicites et les démonstrations resserrées lorsqu'un passage pouvait prêter à confusion. Chaque problème est isolé visuellement ; sa solution suit immédiatement, afin de permettre une lecture continue comme un usage ponctuel.

**Conventions.** Sauf mention contraire, les espaces vectoriels algébriques sont de dimension finie et <sup>N</sup> = {0, 1, 2, . . .}. Pour la transformée de Fourier sur <sup>R</sup>, on adopte

$$\widehat{f}(\xi) = \int_{\mathbb{R}} f(x) e^{-ix\xi} \, dx,$$

avec la constante correspondante dans la formule d'inversion. Sur <sup>T</sup> = <sup>R</sup>/(2��Z), la convolution est normalisée par le facteur 1/(2��).

### **Architecture du recueil**

| Chap. | Thème   |              |                                        | Problèmes         |
|-------|---------|--------------|----------------------------------------|-------------------|
| 1     | Corps   | et           | extensions                             | 1–10              |
| 2     | Formes  |              | bilinéaires, quadratiques et matrices  | symétriques 11–23 |
| 3     |         | Anneaux      |                                        | 24–25             |
| 4     | Groupes | et           | représentations                        | 26–37             |
| 5     | Algèbre |              | linéaire : méthodes générales          | 38–50             |
| 6     |         | Réduction    | des endomorphismes et calcul matriciel | 51–68             |
| 7     |         | Arithmétique | et approximation diophantienne         | 69–73             |
| 8     | Calcul  |              | différentiel et applications globales  | 74–78             |
| 9     |         | Intégration  | et espaces ��                          |                   |
|       |         |              | ��                                     | 79–85             |
| 10    | Analyse |              | complexe                               | 86–95             |
| 11    |         | Convexité,   | monotonie et variation bornée          | 96–98             |
| 12    | Analyse | de           | Fourier                                | 99–107            |
| 13    | Suites  | et           | sous-additivité                        | 108–110           |
| 14    |         | Topologie    | et analyse fonctionnelle               | 111–121           |
| 15    |         | Probabilités | et problème des moments                | 122–125           |
| 16    |         | Fonctions    | d’une variable réelle                  | 126–127           |

### **Table des matières**

| I 1 2 | Algèbre Corps Formes | Avant-propos et extensions. bilinéaires, |                   | formes         | quadratiques et matrices symétriques. | i 1 2 6 |
|-------|----------------------|------------------------------------------|-------------------|----------------|---------------------------------------|---------|
| 3     | Anneaux.             |                                          |                   |                |                                       | 11      |
| 4     | Groupes              | et                                       | représentations.  |                |                                       | 12      |
| 5     | Algèbre              | linéaire                                 | :                 | méthodes       | générales.                            | 16      |
| 6     | Réduction            | des                                      |                   | endomorphismes | et calcul matriciel                   | 21      |
| 7     |                      | Arithmétique                             | élémentaire       | et             | approximation diophantienne           | 29      |
| II    | Analyse              |                                          |                   |                |                                       | 33      |
| 8     | Calcul               | différentiel                             | et                | applications   | globales.                             | 34      |
| 9     |                      | Intégration et                           | espaces           | �� ��          |                                       |         |
| 10    | Analyse              | complexe                                 |                   |                |                                       | 41      |
| 11    | Convexité,           |                                          | monotonie         | et             | variation bornée                      | 46      |
| 12    | Analyse              | de                                       | Fourier           |                |                                       | 48      |
| 13    | Suites               | et                                       | sous-additivité.  |                |                                       | 52      |
| 14    | Topologie            | et                                       | analyse           | fonctionnelle  |                                       | 54      |
| 15    |                      | Probabilités et                          | problème          | des            | moments                               | 59      |
| 16    | Fonctions            | d’une                                    | variable          | réelle         |                                       | 61      |
|       | Repères              |                                          | bibliographiques. |                |                                       | 63      |

Première partie I

# Algèbre

---

# Corps et extensions

## Problème 1 Un corps fini peut-il être algébriquement clos ?

Un corps fini peut-il être algébriquement clos ?

**Solution.** Non. Soit  $K$  un corps fini et considérons

$$P(X) = \prod_{a \in K} (X - a) + 1 \in K[X].$$

Pour tout  $a \in K$ , on a  $P(a) = 1$ , donc  $P$  n'a aucune racine dans  $K$ . Comme  $P$  est non constant,  $K$  n'est pas algébriquement clos.  $\square$ 

## Problème 2 Pourquoi $\mathbb{C}$ n'est-elle pas la clôture algébrique de $\mathbb{Q}$ ?

Pourquoi  $\mathbb{C}$  n'est-elle pas une clôture algébrique de  $\mathbb{Q}$ ?

**Solution.** La clôture algébrique  $\overline{\mathbb{Q}}$  est l'ensemble des nombres complexes algébriques sur  $\mathbb{Q}$ . L'anneau  $\mathbb{Q}[X]$  est dénombrable, et chaque polynôme non nul n'a qu'un nombre fini de racines. Par conséquent,

$$\overline{\mathbb{Q}} = \bigcup_{0 \neq P \in \mathbb{Q}[X]} \{z \in \mathbb{C} : P(z) = 0\}$$

est dénombrable. En revanche,  $\mathbb{C}$  ne l'est pas. Ainsi  $\overline{\mathbb{Q}} \neq \mathbb{C}$ .

Il est néanmoins vrai que  $\mathbb{C}$  contient une clôture algébrique de  $\mathbb{Q}$ , à savoir le sous-corps  $\overline{\mathbb{Q}}$  de ses éléments algébriques.  $\square$ 

## Problème 3 Le polynôme d'Artin–Schreier $X^p - X - 1$

Soit  $p$  un nombre premier. Montrer que  $X^p - X - 1$  est irréductible dans  $\mathbb{F}_p[X]$ .

**Solution.** Soit  $\alpha$  une racine de  $P(X) = X^p - X - 1$  dans une clôture algébrique de  $\mathbb{F}_p$ . Pour tout  $i \in \mathbb{F}_p$ ,

$$P(\alpha + i) = \alpha^p + i^p - \alpha - i - 1 = P(\alpha) = 0.$$

Les  $p$  racines de  $P$  sont donc les  $\alpha + i$ ,  $i \in \mathbb{F}_p$ , et elles sont distinctes puisque  $P'(X) = -1$ .

Soit  $\mathbb{Q}$  un facteur irréductible de  $P$ , de degré  $d$ , ayant  $\alpha$  pour racine. Les racines de  $\mathbb{Q}$  sont l'orbite de  $\alpha$  sous le Frobenius  $x \mapsto x^p$ . Or

$$\alpha^p = \alpha + 1, \quad \alpha^{p^k} = \alpha + k \quad (k \in \mathbb{N}),$$

où  $k$  est lu dans  $\mathbb{F}_p$ . Le plus petit  $k \geq 1$  tel que  $\alpha^{p^k} = \alpha$  est donc  $p$ . Ainsi  $d = p$ , et comme deg  $P = p$ , le polynôme  $P$  est irréductible.  $\square$ 

**Remarque.** La réduction modulo  $p$  fournit aussi l'irréductibilité de  $X^p - X - 1$  dans  $\mathbb{Q}[X]$ . Plus généralement, un théorème de Selmer affirme que  $X^n - X - 1$  est irréductible sur  $\mathbb{Q}$  pour tout  $n \geq 2$ .

**Problème 4**  $X^4 + 1$  : irréductible sur  $\mathbb{Z}$ , réductible sur tout corps premierMontrer que  $X^4 + 1$  est irréductible dans  $\mathbb{Z}[X]$ , mais réductible dans  $\mathbb{F}_p[X]$  pour tout nombre premier  $p$ .

**Solution.** On a  $X^4 + 1 = \Phi_8(X)$ , donc ce polynôme est irréductible sur  $\mathbb{Q}$ , puis sur  $\mathbb{Z}$  par le lemme de Gauss.

Dans  $\mathbb{F}_2[X]$ ,

$$X^4 + 1 = (X + 1)^4.$$

Supposons  $p$  impair. Alors  $p^2 \equiv 1 \pmod{8}$ , donc  $8$  divise  $p^2 - 1 = \text{card}(\mathbb{F}_{p^2}^\times)$ . Le groupe cyclique  $\mathbb{F}_{p^2}^\times$  contient un élément  $\xi$  d'ordre  $8$ . Celui-ci est racine de  $X^4 + 1$ , et son polynôme minimal sur  $\mathbb{F}_p$  a degré au plus 2. Il fournit donc un facteur propre de  $X^4 + 1$  dans  $\mathbb{F}_p[X]$ . Le polynôme est réductible pour tout  $p$ .  $\square$ 

**Problème 5** Racines primitives de l'unité en caractéristique  $p$ Soient  $n \geq 1$  et  $p$  premier. Quand existe-t-il une racine primitive  $n$ -ième de l'unité dans  $\overline{\mathbb{F}_p}$ ? Et dans  $\mathbb{F}_p$  elle-même?

**Solution.** Dans  $\overline{\mathbb{F}_p}$ , une racine primitive  $n$ -ième existe si et seulement si  $p \nmid n$ .

Si  $p \mid n$ , écrivons  $n = pm$ . De  $x^n = 1$  on déduit  $(x^m)^p = 1$ , puis  $x^m = 1$  puisque le Frobenius est injectif. Aucun élément n'a donc ordre  $n$ .

Réciproquement, si  $p \nmid n$ , le polynôme  $X^n - 1$  est séparable car sa dérivée  $nX^{n-1}$  n'est pas nulle. Dans son corps de décomposition, son groupe de racines est cyclique d'ordre  $n$ ; il contient donc un élément d'ordre exactement  $n$ .

Dans  $\mathbb{F}_p$  elle-même, le groupe  $\mathbb{F}_p^\times$  est cyclique d'ordre  $p - 1$ . Une racine primitive  $n$ -ième y existe donc si et seulement si  $n \mid p - 1$ .  $\square$ 

**Problème 6** Factorisation après extension du corps de constantesSoit  $P \in \mathbb{F}_q[X]$  irréductible de degré  $d$ , et soit  $r \mid d$ . Décrire sa factorisation dans  $\mathbb{F}_{q^r}[X]$ .

**Solution.** Soit  $\alpha$  une racine de  $P$  dans  $\mathbb{F}_{q^d}$ . Sur  $\mathbb{F}_q$ , ses conjugués sont

$$\alpha, \alpha^q, \dots, \alpha^{q^{d-1}}.$$

Sur  $\mathbb{F}_{q^r}$ , le Frobenius pertinent est  $x \mapsto x^{q^r}$ . L'orbite de  $\alpha^{q^s}$  sous ce Frobenius a longueur

$$\frac{d}{\gcd(d, r)} = \frac{d}{r},$$

car  $r \mid d$ . Chaque facteur irréductible a donc degré  $d/r$ . Les  $d$  racines se répartissent en  $r$  orbites :  $P$  est le produit de  $r$  facteurs irréductibles distincts, tous de degré  $d/r$ .  $\square$ 

**Remarque.** Sans l'hypothèse  $r \mid d$ , le nombre de facteurs est  $\gcd(d, r)$  et leur degré commun vaut  $d/\gcd(d, r)$ .

**Problème 7 Racines de l'unité dans un corps de nombres**Montrer qu'une extension finie  $K$  de  $\mathbb{Q}$  ne contient qu'un nombre fini de racines de l'unité.

**Solution.** Posons  $N = [K : \mathbb{Q}]$ . Si  $\zeta \in K$  est une racine de l'unité d'ordre  $m$ , alors

$$\varphi(m) = [\mathbb{Q}(\zeta) : \mathbb{Q}] \leq [K : \mathbb{Q}] = N.$$

Or la minoration élémentaire

$$\varphi(m) \geq \sqrt{\frac{m}{2}},$$

établie au problème 72, montre que  $\varphi(m) \rightarrow +\infty$  lorsque  $m \rightarrow +\infty$ . Il n'existe donc qu'un nombre fini d'entiers  $m$  tels que  $\varphi(m) \leq N$ . Pour chacun d'eux, il n'y a qu'un nombre fini de racines d'ordre  $m$ . L'ensemble recherché est fini.  $\square$ 

**Problème 8 Extension dont tous les éléments non triviaux sont quadratiques**Soit  $K$  un corps de caractéristique différente de 2, et  $L/K$  une extension telle que tout élément de  $L \setminus K$  soit de degré 2 sur  $K$ . Montrer que  $[L : K] = 2$ .

**Solution.** Choisissons  $\alpha \in L \setminus K$ . Alors  $[K(\alpha) : K] = 2$ . Supposons  $L \neq K(\alpha)$  et choisissons  $\beta \in L \setminus K(\alpha)$ . Comme  $[K(\beta) : K] = 2$ , on a

$$[K(\alpha, \beta) : K] = 4,$$

et  $(1, \alpha, \beta, \alpha\beta)$  est une base de  $K(\alpha, \beta)$  sur  $K$ .

Puisque  $\alpha$  et  $\beta$  sont quadratiques, il existe  $a, b, c, d \in K$  tels que

$$\alpha^2 = a + b\alpha, \quad \beta^2 = c + d\beta.$$

Considérons  $\gamma = \alpha + \beta$ . Les trois vecteurs

$$1, \quad \gamma, \quad \frac{\gamma^2}{2} = \alpha\beta + \frac{\alpha^2 + \beta^2}{2}$$

sont linéairement indépendants sur  $K$  : dans une relation linéaire, le coefficient de  $\alpha\beta$  impose d'abord l'annulation du coefficient de  $\gamma^2/2$ , puis les coefficients de  $\alpha$  et de  $\beta$  imposent les autres. Ainsi  $[K(\gamma) : K] \geq 3$ , contradiction avec l'hypothèse. Donc  $L = K(\alpha)$  et  $[L : K] = 2$ .  $\square$ 

**Problème 9 Intersection de deux corps cyclotomiques premiers entre eux**Soient  $m, n \geq 1$  premiers entre eux et  $\zeta_k = e^{2\pi i/k}$ . Montrer que

$$\mathbb{Q}(\zeta_m) \cap \mathbb{Q}(\zeta_n) = \mathbb{Q}.$$

**Solution.** Comme  $m$  et  $n$  sont premiers entre eux, il existe  $u, v \in \mathbb{Z}$  tels que  $um + vn = 1$ . On en déduit

$$\zeta_{mn} = \zeta_n^u \zeta_m^v$$

donc

$$\mathbb{Q}(\zeta_m, \zeta_n) = \mathbb{Q}(\zeta_{mn}).$$

Les extensions cyclotomiques sont galoisiennes. Pour deux extensions finies  $E, F$  de  $\mathbb{Q}$ , dont l'une est galoisienne, on a

$$[EF : \mathbb{Q}][E \cap F : \mathbb{Q}] = [E : \mathbb{Q}][F : \mathbb{Q}].$$

Ici,

$$[\mathbb{Q}(\zeta_{mn}) : \mathbb{Q}] = \varphi(mn) = \varphi(m)\varphi(n),$$

si bien que  $[\mathbb{Q}(\zeta_m) \cap \mathbb{Q}(\zeta_n) : \mathbb{Q}] = 1$ . □

### Problème 10 Description linéaire d'un compositum

Soient  $E/K$  et  $E'/K$  deux sous-extensions d'une même extension  $M/K$ , avec  $E/K$  algébrique. Montrer que

$$EE' = \left\{ \sum_{i=1}^s x_i y_i : s \geq 1, x_i \in E, y_i \in E' \right\},$$

puis que  $[EE' : E'] \leq [E : K]$ .

**Solution.** Notons  $V$  l'ensemble des sommes finies de produits  $xy$ , avec  $x \in E$  et  $y \in E'$ . C'est un sous-espace vectoriel de  $M$  sur  $E'$ , contenant  $E$  et  $E'$ . Il suffit de vérifier qu'il est stable par inversion des éléments non nuls.

Soit  $z \in V \setminus \{0\}$ . Il appartient à  $E'(x_1, \dots, x_s)$  pour certains  $x_i \in E$ . Comme les  $x_i$  sont algébriques sur  $K$ , ils le sont sur  $E'$ , donc

$$E'(x_1, \dots, x_s) = E'[x_1, \dots, x_s].$$

Cette algèbre est un corps et est contenue dans  $V$ ; elle contient donc  $z^{-1}$ . Ainsi  $V$  est un corps contenant  $E$  et  $E'$ , donc  $V = EE'$ .

Si  $(e_i)_{i \in I}$  est une base de  $E$  sur  $K$ , la famille  $(e_i)_{i \in I}$  engendre  $EE'$  sur  $E'$ . Par conséquent,

$$[EE' : E'] \leq \text{card}(I) = [E : K].$$

On peut aussi voir cette inégalité comme une conséquence de la surjectivité de l'application naturelle  $E \otimes_K E' \rightarrow EE'$ . □

# Formes bilinéaires, formes quadratiques et matrices symétriques

## Problème 11 Norme opérateur d'une matrice symétrique

Soit  $S \in M_n(\mathbb{R})$  symétrique. Montrer que

$$\rho(S) = \|S\|_{2 \rightarrow 2} := \sup_{x \neq 0} \frac{\|Sx\|_2}{\|x\|_2}.$$

**Solution.** Par le théorème spectral, il existe une base orthonormée  $(e_i)$  telle que  $Se_i = \lambda_i e_i$ . Si  $x = \sum_i x_i e_i$ , alors

$$\|Sx\|_2^2 = \sum_i \lambda_i^2 x_i^2 \leq \rho(S)^2 \sum_i x_i^2 = \rho(S)^2 \|x\|_2^2.$$

Donc  $\|S\|_{2 \rightarrow 2} \leq \rho(S)$ . Réciproquement, pour un vecteur propre unitaire associé à une valeur propre de module maximal, l'égalité est atteinte.  $\square$ 

## Problème 12 Réduction simultanée de deux formes quadratiques

Énoncer et démontrer le théorème de réduction simultanée lorsqu'une des deux formes est définie positive.

**Solution.** Soient  $q$  et  $r$  deux formes quadratiques sur un espace vectoriel réel  $E$  de dimension  $n$ , et supposons  $q$  définie positive. Notons  $b_q$  et  $b_r$  leurs formes polaires. Il existe une base de  $E$  dans laquelle les matrices de  $q$  et  $r$  sont respectivement  $I_n$  et une matrice diagonale réelle.

En effet,  $b_q$  est un produit scalaire. Le théorème de représentation de Riesz en dimension finie fournit un unique endomorphisme  $u$  tel que

$$b_r(x, y) = b_q(ux, y) \quad (x, y \in E).$$

La symétrie de  $b_r$  montre que  $u$  est auto-adjoint pour  $b_q$ . Le théorème spectral fournit donc une base  $b_q$ -orthonormée de vecteurs propres de  $u$ . Dans cette base,  $q$  a pour matrice  $I_n$  et  $r$  une matrice diagonale.

Sous forme matricielle : pour  $A \in S_n^{++}(\mathbb{R})$  et  $B \in S_n(\mathbb{R})$ , il existe  $P \in GL_n(\mathbb{R})$  et une matrice diagonale réelle  $D$  tels que

$$P^T A P = I_n, \quad P^T B P = D.$$

 $\square$ 

## Problème 13 Non-dégénérescence et isotropie sur $\mathbb{F}_p^n$

Sur  $\mathbb{F}_p^n$ , considérons

$$B(x, y) = \sum_{i=1}^n x_i y_i, \quad q(x) = B(x, x).$$

La forme  $B$  est-elle dégénérée ? Quand  $q$  possède-t-elle un vecteur isotrope non nul ?

**Solution.** La forme  $B$  est toujours non dégénérée : si  $x_j \neq 0$ , alors  $B(x, x_j^{-1}e_j) = 1$ .

Pour l'isotropie :

- si  $n = 1$ , il n'existe aucun vecteur isotrope non nul;
- si  $p = 2$  et  $n \geq 2$ , le vecteur  $e_1 + e_2$  est isotrope;
- si  $p$  est impair et  $n = 2$ , il existe un vecteur isotrope non nul si et seulement si  $-1$  est un carré dans  $\mathbb{F}_p$ , c'est-à-dire si et seulement si  $p \equiv 1 \pmod{4}$ ;
- si  $p$  est impair et  $n \geq 3$ , il existe toujours un vecteur isotrope non nul.

Pour le dernier point, les ensembles

$$A = \{x^2 : x \in \mathbb{F}_p\}, \quad B = \{-1 - y^2 : y \in \mathbb{F}_p\}$$

ont chacun  $(p+1)/2$  éléments, donc ils se rencontrent. Il existe  $x, y$  tels que  $x^2 + y^2 = -1$ , et  $(x, y, 1, 0, \dots, 0)$  est isotrope. □

**Problème 14** Une forme quadratique positive définit une norme

Soit  $q$  une forme quadratique définie positive sur un espace vectoriel réel  $E$ . Montrer que  $x \mapsto \sqrt{q(x)}$  est une norme.

**Solution.** Soit  $b$  la forme polaire de  $q$ . Comme  $q$  est définie positive,  $b$  est un produit scalaire et satisfait Cauchy-Schwarz :

$$|b(x, y)| \leq \sqrt{q(x)q(y)}.$$

La séparation et l'homogénéité sont immédiates. Enfin,

$$\begin{aligned} q(x+y) &= q(x) + 2b(x, y) + q(y) \\ &\leq q(x) + 2\sqrt{q(x)q(y)} + q(y) = (\sqrt{q(x)} + \sqrt{q(y)})^2. \end{aligned}$$

En prenant les racines carrées, on obtient l'inégalité triangulaire. □

**Problème 15** Réalité du spectre d'une matrice symétrique réelle

Montrer que toute valeur propre complexe d'une matrice symétrique réelle est réelle.

**Solution.** Soit  $A^T = A$  et soit  $v \in \mathbb{C}^n \setminus \{0\}$  tel que  $Av = \lambda v$ . En utilisant le produit hermitien,

$$\lambda \|v\|_2^2 = v^* A v.$$

Or  $A^* = A$ , donc  $v^* A v$  est réel. Il s'ensuit que  $\lambda \in \mathbb{R}$ . □

**Problème 16** Une matrice complexe symétrique non diagonalisable

Donner une matrice complexe symétrique qui ne soit pas diagonalisable.

**Solution.** La matrice

$$A = \begin{pmatrix} 1+i & 1 \\ 1 & 1-i \end{pmatrix}$$

est symétrique et vérifie  $\chi_A(X) = (X-1)^2$ . Comme  $A \neq I_2$ , son polynôme minimal est  $(X-1)^2$ , donc elle n'est pas diagonalisable.

Cela illustre que « symétrique » sur  $\mathbb{C}$  ne signifie pas « hermitienne » : le théorème spectral complexe concerne les matrices  $A$  telles que  $A^* = A$ . □

**Problème 17 Orbites de congruence des matrices symétriques réelles**Combien l'action par congruence de  $GL_n(\mathbb{R})$  possède-t-elle d'orbites sur  $S_n(\mathbb{R})$ ?**Solution.** La loi d'inertie de Sylvester affirme que toute matrice symétrique réelle est congruente à une unique matrice de la forme

$$\text{diag}(I_p, -I_q, 0_{n-p-q}), \quad p, q \geq 0, \quad p + q \leq n.$$

Les orbites sont donc indexées par les couples  $(p, q)$  satisfaisant ces contraintes. Leur nombre est

$$\sum_{p=0}^n (n - p + 1) = \frac{(n + 1)(n + 2)}{2}.$$

□**Problème 18  $O_n(\mathbb{R})$  est maximal parmi les sous-groupes compacts**Montrer que  $O_n(\mathbb{R})$  est un sous-groupe compact maximal de  $GL_n(\mathbb{R})$ , au sens où aucun sous-groupe compact strictement plus grand ne le contient.**Solution.** Le groupe  $O_n(\mathbb{R})$  est fermé et borné dans  $M_n(\mathbb{R})$ , donc compact. Soit  $A \in GL_n(\mathbb{R}) \setminus O_n(\mathbb{R})$ . Il existe un vecteur unitaire  $x$  tel que  $\|Ax\|_2 \neq 1$ . Choisissons  $Q \in O_n(\mathbb{R})$  tel que

$$Qx = \frac{Ax}{\|Ax\|_2}.$$

Alors  $B = Q^{-1}A$  vérifie  $Bx = \lambda x$ , avec  $\lambda = \|Ax\|_2 \neq 1$ . Par conséquent,

$$B^k x = \lambda^k x \quad (k \in \mathbb{Z}).$$

La famille  $(B^k)_{k \in \mathbb{Z}}$  est non bornée : on prend  $k \rightarrow +\infty$  si  $\lambda > 1$ , et  $k \rightarrow -\infty$  si  $0 < \lambda < 1$ . Tout sous-groupe de  $GL_n(\mathbb{R})$  contenant  $O_n(\mathbb{R})$  et  $A$  contient  $B$  et toutes ses puissances; il ne peut donc être compact. □

**Problème 19 Racine carrée positive d'une matrice définie positive**Soit  $A \in S_n^{++}(\mathbb{R})$ . Montrer qu'il existe une unique matrice  $R \in S_n^{++}(\mathbb{R})$  telle que  $R^2 = A$ .**Solution.** Par le théorème spectral,

$$A = P \text{diag}(\lambda_1, \dots, \lambda_n) P^\top, \quad P \in O_n(\mathbb{R}), \quad \lambda_i > 0.$$

La matrice

$$R = P \text{diag}(\sqrt{\lambda_1}, \dots, \sqrt{\lambda_n}) P^\top$$

est symétrique définie positive et vérifie  $R^2 = A$ .

Pour l'unicité, soit  $S \in S_n^+(\mathbb{R})$  tel que  $S^2 = A$ . Comme  $SA = S^3 = AS$ , chaque espace propre  $E_\lambda(A)$  est stable par  $S$ . Sur cet espace,  $S^2 = \lambda I$ . Les valeurs propres de la restriction de  $S$  sont donc parmi  $\pm\sqrt{\lambda}$ , et la positivité de  $S$  exclut le signe négatif. Ainsi  $S = \sqrt{\lambda}I$  sur chaque  $E_\lambda(A)$ , donc  $S = R$ . □

**Problème 20 Signature du produit de deux formes linéaires**Soient  $f, g \in E^*$  deux formes linéaires indépendantes sur un espace vectoriel réel  $E$  de dimension  $n$ . Montrer que  $q(x) = f(x)g(x)$  est une forme quadratique et déterminer son inertie.

**Solution.** On écrit

$$fg = \left(\frac{f+g}{2}\right)^2 - \left(\frac{f-g}{2}\right)^2.$$

Les formes  $\ell_1 = (f+g)/2$  et  $\ell_2 = (f-g)/2$  sont indépendantes. En complétant  $(\ell_1, \ell_2)$  en une base de  $E^*$  et en prenant la base antéduale de  $E$ , la matrice de  $q$  devient

$$\text{diag}(1, -1, 0, \dots, 0).$$

L'inertie est donc  $(1, 1, n-2)$  : une direction positive, une direction négative et un noyau de dimension  $n-2$ . □

**Problème 21 Norme spectrale d'une matrice et de sa transposée**Montrer que, pour toute matrice réelle  $M$ ,

$$\|M\|_{2 \rightarrow 2} = \|M^T\|_{2 \rightarrow 2}.$$

**Solution.** Les matrices  $M^T M$  et  $MM^T$  sont symétriques positives, et

$$\|M\|_{2 \rightarrow 2}^2 = \rho(M^T M), \quad \|M^T\|_{2 \rightarrow 2}^2 = \rho(MM^T).$$

Les matrices  $M^T M$  et  $MM^T$  ont les mêmes valeurs propres non nulles, avec les mêmes multiplicités; dans le cas carré, elles ont même polynôme caractéristique. Leurs rayons spectraux sont donc égaux. □

**Problème 22 Irréductibilité de  $x^2 + y^2 + z^2$** Soit  $K$  un corps de caractéristique différente de 2. Montrer que

$$x^2 + y^2 + z^2$$

est irréductible dans  $K[x, y, z]$ .

**Solution.** Le polynôme  $P = x^2 + y^2 + z^2$  est homogène de degré 2. S'il se factorisait en deux polynômes non constants, l'examen des composantes homogènes de plus bas et de plus haut degré montrerait que ces deux facteurs sont des formes linéaires :  $P = \ell m$ .

La forme quadratique associée aurait alors rang au plus 2, car, la caractéristique étant différente de 2,

$$\ell m = \left(\frac{\ell+m}{2}\right)^2 - \left(\frac{\ell-m}{2}\right)^2.$$

Or la matrice de  $P$  dans la base canonique est  $I_3$ , de rang 3. C'est une contradiction. Ainsi  $x^2 + y^2 + z^2$  est irréductible dans  $K[x, y, z]$ . □

**Problème 23 Matrice orthogonale la plus proche**Soit  $M \in GL_n(\mathbb{R})$ . Déterminer l'unique matrice de  $O_n(\mathbb{R})$  qui minimise la distance à  $M$  pour la norme de Frobenius.

**Solution.** Écrivons la décomposition polaire

$$M = QS, \quad Q \in O_n(\mathbb{R}), \quad S = (M^T M)^{1/2} \in S_n^{++}(\mathbb{R}).$$

Pour  $U \in O_n(\mathbb{R})$ , l'invariance orthogonale de la norme de Frobenius donne

$$\|M - U\|_F = \|S - Q^T U\|_F.$$

Diagonalisons  $S = PDP^T$ , où  $D = \text{diag}(\sigma_1, \dots, \sigma_n)$  et  $\sigma_i > 0$ . En posant  $V = P^T Q^T U P \in O_n(\mathbb{R})$ ,

$$\begin{aligned} \|D - V\|_F^2 &= \|D\|_F^2 + n - 2 \text{tr}(DV) \\ &= \|D\|_F^2 + n - 2 \sum_{i=1}^n \sigma_i v_{ii}. \end{aligned}$$

Comme  $v_{ii} \leq 1$  et  $\sigma_i > 0$ , le maximum de  $\text{tr}(DV)$  est  $\sum_i \sigma_i$ , atteint uniquement lorsque  $v_{ii} = 1$  pour tout  $i$ , donc lorsque  $V = I_n$ . Ainsi l'unique minimiseur est  $U = Q$ , c'est-à-dire

$$Q = M(M^T M)^{-1/2}.$$

La distance minimale vaut  $(\sum_i (\sigma_i - 1)^2)^{1/2}$ .

# Anneaux

**Problème 24** Si  $A[X]$  est principal, alors  $A$  est un corpsSoit  $A$  un anneau commutatif unitaire. Si  $A[X]$  est un anneau principal, montrer que  $A$  est un corps.

**Solution.** Par définition, un anneau principal est un domaine intègre dont tous les idéaux sont principaux. Ainsi  $A[X]$ , puis son sous-anneau  $A$ , sont intègres.

Le polynôme  $X$  est irréductible dans  $A[X]$ . En effet, si  $X = PQ$ , l'égalité des degrés impose qu'un facteur soit constant, disons  $P = a \in A$ . Si  $b$  est le coefficient dominant de  $Q$ , la comparaison des coefficients de degré 1 donne  $ab = 1$ ; le facteur constant  $a$  est donc une unité.

Dans un anneau principal, tout élément irréductible engendre un idéal maximal. Ainsi  $(X)$  est maximal, et

$$A \simeq A[X]/(X)$$

est un corps. □

**Problème 25** L'anneau des nombres décimauxMontrer que l'anneau des nombres décimaux

$$D = \mathbb{Z} \left[ \frac{1}{10} \right]$$

est principal.

**Solution.** C'est une localisation de l'anneau principal  $\mathbb{Z}$  par la partie multiplicative

$$S = \{10^k : k \geq 0\}.$$

Or toute localisation d'un anneau principal est principale.

Explicitement, soit  $I \neq 0$  un idéal de  $D$ . Il contient un entier strictement positif : si  $x \in I \setminus \{0\}$ , alors  $10^m x \in \mathbb{Z} \setminus \{0\}$  pour  $m$  assez grand. Soit  $d$  le plus petit entier positif de  $I$ . Pour  $y \in I$ , choisissons  $m$  tel que  $10^m y \in \mathbb{Z}$  et effectuons la division euclidienne

$$10^m y = qd + r, \quad 0 \leq r < d.$$

Alors  $r = 10^m y - qd \in I \cap \mathbb{Z}$ , donc  $r = 0$  par minimalité de  $d$ . Ainsi  $y = qd/10^m \in (d)$ , et  $I = (d)$ . □

# Groupes et représentations

## Problème 26 Classification des groupes d'ordre au plus 7

Classifier, à isomorphisme près, les groupes finis d'ordre inférieur ou égal à 7.

**Solution.** On obtient :

| $G$   | groupes à isomorphisme près |
|-------|-----------------------------|
| 1     | $\{1\}$                     |
| 2     | $C_2$                       |
| 3     | $C_3$                       |
| 4     | $C_4, C_2 \times C_2$       |
| 5     | $C_5$                       |
| 6     | $C_6, S_3$                  |
| 7     | $C_7$                       |

Les ordres premiers donnent des groupes cycliques. Pour l'ordre 4, soit il existe un élément d'ordre 4, soit tous les éléments non triviaux ont ordre 2, auquel cas le groupe est  $C_2^2$ .

Pour  $|G| = 6$ , le nombre  $n_3$  de 3-Sylow divise 2 et vaut 1 modulo 3, donc  $n_3 = 1$ . Si un 2-Sylow  $H$  est également distingué, alors les deux sous-groupes distingués d'ordres premiers entre eux commutent et

$$G \simeq C_3 \times C_2 \simeq C_6.$$

Sinon,  $G$  agit sur les trois classes à gauche de  $H$ . Le noyau de cette action est le cœur

$$\bigcap_{g \in G} gHg^{-1},$$

qui est contenu dans  $H$ . S'il était d'ordre 2, il serait égal à  $H$  et rendrait  $H$  distingué; il est donc trivial. L'action fournit un plongement  $G \hookrightarrow S_3$ , nécessairement un isomorphisme puisque les deux groupes ont ordre 6. □

## Problème 27 Résolubilité de $S_4$

Montrer que  $S_4$  est résoluble.

**Solution.** Le sous-groupe de Klein

$$V_4 = \{1, (12)(34), (13)(24), (14)(23)\}$$

est distingué dans  $A_4$ . La suite

$$\{1\} \triangleleft V_4 \triangleleft A_4 \triangleleft S_4$$

a des quotients successifs abéliens :  $V_4, A_4/V_4 \simeq C_3$  et  $S_4/A_4 \simeq C_2$ . Ainsi  $S_4$  est résoluble. □

**Problème 28 Une classe de conjugaison de cardinal puissance d'un premier**Soit  $G$  un groupe d'ordre  $p^\alpha q^\beta$ , où  $p \neq q$  sont premiers et  $\alpha, \beta \in \mathbb{N}$  ne sont pas tous deux nuls. Montrer qu'il existe  $g \neq 1$  dont la classe de conjugaison a cardinal 1 ou une puissance d'un nombre premier.

**Solution.** Quitte à échanger  $p$  et  $q$ , supposons  $\alpha \geq 1$ . L'équation des classes écrit  $|G|$  comme somme des cardinaux des classes de conjugaison. La classe de l'identité a cardinal 1, non divisible par  $p$ . Si toutes les autres classes avaient un cardinal divisible par  $p$ , on aurait  $|G| \equiv 1 \pmod{p}$ , contradiction. Il existe donc une classe  $C \neq \{1\}$  dont le cardinal n'est pas divisible par  $p$ .

Comme  $|C| = [G : C_G(g)]$  divise  $|G|$ , on a  $|C| = p^a q^b$ . L'absence de facteur  $p$  impose  $a = 0$ , donc  $|C| = q^b$ , éventuellement égal à 1. □

**Problème 29 Nombre de sous-groupes de Sylow**Soit  $P$  un  $p$ -Sylow de  $G$ . Montrer que

$$n_p = [G : N_G(P)].$$

**Solution.** Le groupe  $G$  agit par conjugaison sur l'ensemble de ses  $p$ -Sylow. Le deuxième théorème de Sylow affirme que cette action est transitive. Le stabilisateur de  $P$  est précisément son normalisateur  $N_G(P)$ . La formule orbite-stabilisateur donne donc

$$n_p = \text{card}(G \cdot P) = [G : N_G(P)].$$

□**Problème 30 Valeurs des caractères d'un groupe fini**Pourquoi les valeurs d'un caractère complexe d'un groupe fini sont-elles des sommes de racines de l'unité?

**Solution.** Soit  $\rho : G \rightarrow GL(V)$  une représentation complexe d'un groupe fini. Pour  $g \in G$  d'ordre  $m$ , on a  $\rho(g)^m = I$ . Le polynôme  $X^m - 1$ , qui est scindé à racines simples sur  $\mathbb{C}$ , annule  $\rho(g)$ . L'endomorphisme  $\rho(g)$  est donc diagonalisable et ses valeurs propres sont des racines  $m$ -ièmes de l'unité. Par définition,

$$\chi_\rho(g) = \text{tr}(\rho(g))$$

est leur somme. L'abélianité de  $G$  n'est pas nécessaire. □

**Problème 31 Endomorphismes continus du cercle**Déterminer les morphismes continus de groupes  $S^1 \rightarrow S^1$ .

**Solution.** Soit  $f : S^1 \rightarrow S^1$  un morphisme continu et posons

$$g(t) = f(e^{2\pi i t}), \quad t \in \mathbb{R}.$$

Alors  $g : \mathbb{R} \rightarrow S^1$  est un morphisme continu. Par continuité en 0, on peut choisir  $a > 0$  assez petit pour que

$$A = \int_0^a g(t) dt \neq 0.$$

Pour tout  $x$ ,

$$g(x) = \frac{1}{A} \int_x^{x+a} g(t) dt,$$

car  $g(x+t) = g(x)g(t)$ . Ainsi  $g$  est dérivable et

$$g'(x) = \frac{g(a) - 1}{A} g(x) = cg(x).$$

Comme  $g(0) = 1$ , on obtient  $g(x) = e^{cx}$ . La condition  $g(1) = 1$  donne  $c = 2\pi in$  pour un entier  $n$ . Par conséquent

$$f(z) = z^n.$$

Réciproquement, ces applications sont bien des morphismes continus. □

### Problème 32 Le quotient $S_4/V_4$

Montrer que  $S_4/V_4 \simeq S_3$ .

**Solution.** Le groupe  $S_4$  agit par conjugaison sur les trois doubles transpositions non triviales

$$a = (12)(34), \quad b = (13)(24), \quad c = (14)(23)$$

de  $V_4$ . On obtient un morphisme

$$\varphi : S_4 \longrightarrow S_{\{a,b,c\}} \simeq S_3.$$

La conjugaison par (12) fixe  $a$  et échange  $b$  et  $c$ , tandis que la conjugaison par (123) permute cycliquement  $a, b, c$ . L'image contient donc une transposition et un 3-cycle; elle est égale à  $S_3$ .

Tout élément de  $V_4$  commute avec les trois doubles transpositions, donc  $V_4 \subset \ker \varphi$ . Comme  $\varphi$  est surjectif,

$$|\ker \varphi| = \frac{|S_4|}{|S_3|} = 4.$$

Ainsi  $\ker \varphi = V_4$ , et le premier théorème d'isomorphisme donne

$$S_4/V_4 \simeq S_3.$$

□

### Problème 33 Sous-groupes de Sylow de $S_4$

Décrire les 2-Sylow et les 3-Sylow de  $S_4$ .

**Solution.** On a  $|S_4| = 24 = 2^3 \cdot 3$ .

Les 3-Sylow sont les sous-groupes engendrés par les 3-cycles. Il y a huit 3-cycles, deux par sous-groupe d'ordre 3, donc quatre 3-Sylow.

Un 2-Sylow a ordre 8. Le stabilisateur de la partition

$$\{1, 2\} \sqcup \{3, 4\}$$

est

$$H = \{1, (12), (34), (12)(34), (13)(24), (14)(23), (1324), (1423)\},$$

d'ordre 8; c'est donc un 2-Sylow, isomorphe au groupe diédral d'ordre 8. Les deux autres sont les stabilisateurs des partitions

$$\{1, 3\} \sqcup \{2, 4\}, \quad \{1, 4\} \sqcup \{2, 3\}.$$

Il y en a exactement trois, conformément à  $n_2 \equiv 1 \pmod{2}$  et  $n_2 \mid 3$ .

**Problème 34 Le produit direct  $A_n \times C_2$** Pour quels  $n \geq 2$  a-t-on  $S_n \simeq A_n \times C_2$ ?**Solution.** Pour  $n = 2$ , on a  $A_2 = \{1\}$  et  $S_2 \simeq C_2$ . Pour  $n \geq 3$ , un tel produit direct contiendrait un sous-groupe central d'ordre 2, à savoir  $\{1\} \times C_2$ . Son image réciproque par un isomorphisme serait contenue dans le centre de  $S_n$ , qui est trivial pour  $n \geq 3$ . C'est impossible. Ainsi seul  $n = 2$  convient. □**Problème 35 Un sous-groupe d'ordre 72 dans  $A_6$ ?**Le groupe  $A_6$  possède-t-il un sous-groupe d'ordre 72?**Solution.** Non. Un tel sous-groupe  $H$  aurait indice 5. L'action de  $A_6$  sur  $A_6/H$  fournirait un morphisme
$$\varphi : A_6 \rightarrow S_5.$$

Comme  $|A_6| = 360 > |S_5| = 120$ , ce morphisme ne serait pas injectif. Son noyau serait donc un sous-groupe distingué non trivial de  $A_6$ . La simplicité de  $A_6$  imposerait  $\ker \varphi = A_6$ , ce qui rendrait l'action triviale, en contradiction avec sa transitivité sur un ensemble de cinq éléments. □**Problème 36 Surjections  $S_n \rightarrow S_{n-1}$** Pour quels  $n \geq 2$  existe-t-il un morphisme surjectif  $S_n \rightarrow S_{n-1}$ ?**Solution.** Il en existe pour  $n = 2, 3, 4$  : le morphisme trivial  $S_2 \rightarrow S_1$ , la signature  $S_3 \rightarrow S_2$ , et le quotient  $S_4 \rightarrow S_4/V_4 \simeq S_3$ . Pour  $n \geq 5$ , le noyau d'une telle surjection aurait ordre
$$\frac{n!}{(n-1)!} = n.$$

Or les seuls sous-groupes distingués de  $S_n$  sont  $\{1\}$ ,  $A_n$  et  $S_n$  ; aucun n'a ordre  $n$ . Il n'existe donc aucune surjection pour  $n \geq 5$ . □**Problème 37 Peut-on plonger  $S_3$  dans  $A_4$ ?**Existe-t-il un morphisme injectif  $S_3 \rightarrow A_4$ ?**Solution.** Non. Supposons qu'un sous-groupe  $H \leq A_4$  soit isomorphe à  $S_3$ . Le groupe  $S_3$  possède exactement trois éléments d'ordre 2. Or les seuls éléments d'ordre 2 de  $A_4$  sont les trois doubles transpositions
$$(12)(34), \quad (13)(24), \quad (14)(23).$$

Ils appartiendraient donc tous à  $H$ . Avec l'identité, ils forment le sous-groupe de Klein  $V_4$ , si bien que  $V_4 \subset H$ . Le théorème de Lagrange imposerait alors  $4 | |H| = 6$ , ce qui est impossible. Il n'existe donc aucun morphisme injectif  $S_3 \rightarrow A_4$ . □

# Algèbre linéaire : méthodes générales

**Problème 38 Les matrices  $AB$  et  $BA$  ont même polynôme caractéristique**Soient  $A, B \in M_n(K)$ . Montrer que  $\chi_{AB} = \chi_{BA}$ .

**Solution.** On utilise l'identité de Sylvester

$$\det(I_m + UV) = \det(I_n + VU),$$

valable pour  $U \in M_{m,n}(K)$  et  $V \in M_{n,m}(K)$ . Elle se démontre en calculant de deux façons le déterminant de la matrice par blocs

$$\begin{pmatrix} I_m & U \\ -V & I_n \end{pmatrix}.$$

Pour  $X$  indéterminée, dans le corps  $K(X)$ ,

$$\begin{aligned} \det(XI_n - AB) &= X^n \det(I_n - X^{-1}AB) \\ &= X^n \det(I_n - X^{-1}BA) = \det(XI_n - BA). \end{aligned}$$

Les deux polynômes caractéristiques sont donc égaux. □

**Remarque.** Plus généralement, si  $A \in M_{m,n}(K)$  et  $B \in M_{n,m}(K)$  avec  $n \geq m$ , alors

$$\chi_{BA}(X) = X^{n-m} \chi_{AB}(X).$$

**Problème 39 Rang de  $u$  lorsque  $\text{rg}(u^2) = 4$  en dimension 8**Soit  $u \in \mathcal{L}(\mathbb{R}^8)$  tel que  $\text{rg}(u^2) = 4$ . Quelles sont les valeurs possibles de  $\text{rg}(u)$ ?

**Solution.** On a d'abord  $\text{Im}(u^2) \subset \text{Im}(u)$ , donc  $\text{rg}(u) \geq 4$ . L'inégalité de Sylvester donne

$$\text{rg}(u^2) \geq 2\text{rg}(u) - 8,$$

d'où  $4 \geq 2\text{rg}(u) - 8$  et  $\text{rg}(u) \leq 6$ . Les seules possibilités sont donc 4, 5, 6.

Elles sont toutes réalisées :

| matrice de $u$                | $\text{rg}(u)$ | $\text{rg}(u^2)$ |
|-------------------------------|----------------|------------------|
| $\text{diag}(I_4, 0_4)$       | 4              | 4                |
| $\text{diag}(J_6(0), 0_2)$    | 5              | 4                |
| $\text{diag}(J_4(0), J_4(0))$ | 6              | 4                |

**Problème 40 Existence d'un hyperplan stable**Soit  $E$  un espace vectoriel complexe de dimension finie non nulle. Montrer que tout endomorphisme de  $E$  possède un hyperplan stable.

**Solution.** Soit  $u \in \mathcal{L}(E)$ . L'endomorphisme transposé  $u^* : E^* \rightarrow E^*$  possède un vecteur propre non nul  $\varphi$ , puisque le corps est algébriquement clos. Écrivons  $u^*\varphi = \lambda\varphi$ . Alors  $H = \text{Ker } \varphi$  est un hyperplan et, pour  $x \in H$ ,

$$\varphi(ux) = (u^*\varphi)(x) = \lambda\varphi(x) = 0.$$

Ainsi  $u(H) \subset H$ . □

**Problème 41 Puissances et fonctions d'un bloc de Jordan**Pour  $k \in \mathbb{N}$ , calculer  $J_m(\lambda)^k$ , où  $J_m(\lambda) = \lambda I_m + N_m$  et  $N_m$  est le bloc nilpotent à 1 sur la surdiagonale.

**Solution.** Comme  $N_m^m = 0$  et que  $N_m$  commute avec  $\lambda I_m$ ,

$$J_m(\lambda)^k = \sum_{r=0}^{\min(k,m-1)} \binom{k}{r} \lambda^{k-r} N_m^r.$$

Autrement dit, l'entrée située sur la  $r$ -ième surdiagonale vaut

$$\binom{k}{r} \lambda^{k-r} \quad (0 \leq r \leq \min(k, m-1)),$$

et elle est nulle pour  $r > k$ .

Plus généralement, si  $f$  est holomorphe au voisinage de  $\lambda$  — en particulier si  $f$  est un polynôme —, alors

$$f(J_m(\lambda)) = \sum_{r=0}^{m-1} \frac{f^{(r)}(\lambda)}{r!} N_m^r.$$

□

**Problème 42 Ouverture de l'ensemble des endomorphismes cycliques**Montrer que l'ensemble des matrices cycliques de  $M_n(\mathbb{C})$  est un ouvert non vide.

**Solution.** Une matrice  $A$  est cyclique s'il existe  $x \in \mathbb{C}^n$  tel que

$$(x, Ax, \dots, A^{n-1}x)$$

soit une base. Pour  $x$  fixé, posons

$$\Delta_x(B) = \det(x, Bx, \dots, B^{n-1}x).$$

C'est une fonction polynomiale, donc continue, de  $B$ . L'ensemble

$$U_x = \{B : \Delta_x(B) \neq 0\}$$

est ouvert. L'ensemble des matrices cycliques est  $\bigcup_x U_x$ , donc il est ouvert.

Il est non vide : pour le bloc nilpotent  $J_n(0)$  à 1 sur la surdiagonale, le vecteur  $e_n$  est cyclique, puisque

$$(e_n, J_n e_n, \dots, J_n^{n-1} e_n) = (e_n, e_{n-1}, \dots, e_1).$$

**Problème 43 L'algèbre engendrée par un bloc de Jordan**Calculer  $\mathbb{C}[J_n(\lambda)]$ .**Solution.** En posant  $N = J_n(\lambda) - \lambda I_n$ , on a
$$\mathbb{C}[J_n(\lambda)] = \mathbb{C}[N].$$

Comme  $N^n = 0$ , cette algèbre est l'ensemble des matrices triangulaires supérieures de Toeplitz
$$\begin{pmatrix} a_0 & a_1 & \cdots & a_{n-1} \\ 0 & a_0 & \ddots & \vdots \\ \vdots & \ddots & \ddots & a_1 \\ 0 & \cdots & 0 & a_0 \end{pmatrix}, \quad a_0, \dots, a_{n-1} \in \mathbb{C}.$$

En effet, cette matrice est  $\sum_{r=0}^{n-1} a_r N^r$ .□**Problème 44 Commutant d'un bloc de Jordan**Calculer le commutant de  $J_n(\lambda)$  sur un corps  $K$  contenant  $\lambda$ .**Solution.** Il suffit de calculer le commutant de  $N = J_n(0)$ . Soit  $A$  tel que  $AN = NA$ . Le vecteur  $e_n$  est cyclique pour  $N$ . Il existe donc un unique polynôme  $P$  de degré inférieur à  $n$  tel que
$$Ae_n = P(N)e_n.$$

Pour  $0 \leq r \leq n-1$ ,
$$AN^r e_n = N^r Ae_n = N^r P(N)e_n = P(N)N^r e_n.$$

Les vecteurs  $N^r e_n$  formant une base, on obtient  $A = P(N)$ . Réciproquement, tout polynôme en  $N$  commute avec  $N$ . Ainsi
$$\text{Comm}(J_n(\lambda)) = K[J_n(\lambda)].$$

□**Problème 45 Une réunion finie de sous-espaces vectoriels**Soit  $E$  un espace vectoriel sur  $K$ , et soient  $U_1, \dots, U_m$  des sous-espaces stricts, avec  $m \leq \text{card}(K)$ . Montrer que
$$E \neq U_1 \cup \dots \cup U_m.$$

**Solution.** On peut supposer qu'aucun  $U_i$  n'est contenu dans l'union des autres. Choisissons
$$u \in U_1 \setminus \bigcup_{i=2}^m U_i, \quad v \in E \setminus U_1.$$

Considérons la droite affine  $L = v + Ku$ . Elle ne rencontre pas  $U_1$ . Pour  $i \geq 2$ , elle rencontre  $U_i$  en au plus un point : deux points distincts de l'intersection auraient pour différence un multiple non nul de  $u$ , ce qui imposerait  $u \in U_i$ . Ainsi
$$\text{card}(L \cap (U_1 \cup \dots \cup U_m)) \leq m - 1 < \text{card}(K) = \text{card}(L).$$

Il reste donc un point de  $L$  hors de l'union.

**Problème 46 Matrice d'évaluation inversible**Soient  $f_1, \dots, f_n : X \rightarrow K$  des fonctions linéairement indépendantes. Montrer qu'il existe  $x_1, \dots, x_n \in X$  tels que la matrice  $(f_i(x_j))_{i,j}$  soit inversible.

**Solution.** Posons  $F = \text{Vect}(f_1, \dots, f_n)$ . Pour  $x \in X$ , l'évaluation

$$\delta_x : F \rightarrow K, \quad \delta_x(f) = f(x),$$

est une forme linéaire. Les  $\delta_x$  engendrent  $F^*$  : sinon il existerait  $0 \neq f \in F$  annulé par toutes les  $\delta_x$ , donc identiquement nul sur  $X$ , contradiction.

On peut donc extraire  $n$  évaluations  $\delta_{x_1}, \dots, \delta_{x_n}$  formant une base de  $F^*$ . La matrice de cette base duale sur la base  $(f_i)$  est précisément  $(f_i(x_j))_{i,j}$  ; elle est inversible. □

**Problème 47 Inclusion de noyaux et combinaison linéaire**Soient  $f, f_1, \dots, f_m \in E^*$ . Montrer que

$$\bigcap_{i=1}^m \text{Ker } f_i \subset \text{Ker } f \iff f \in \text{Vect}(f_1, \dots, f_m).$$

**Solution.** Le sens réciproque est immédiat. Pour le sens direct, définissons

$$T : E \rightarrow K^m, \quad T(x) = (f_1(x), \dots, f_m(x)).$$

L'hypothèse  $\text{Ker } T \subset \text{Ker } f$  permet de définir une forme linéaire  $\ell$  sur  $\text{Im } T$  par

$$\ell(Tx) = f(x).$$

Elle est bien définie. Prolongeons  $\ell$  en une forme linéaire sur  $K^m$ , encore notée  $\ell$ , et écrivons

$$\ell(y_1, \dots, y_m) = \sum_{i=1}^m a_i y_i.$$

Alors  $f = \sum_i a_i f_i$ . □

**Problème 48 Produit nul de deux formes linéaires**Soient  $f, g \in E^*$  tels que  $f(x)g(x) = 0$  pour tout  $x \in E$ . Montrer que  $f = 0$  ou  $g = 0$ .

**Solution.** Supposons  $f$  et  $g$  non nulles. S'ils sont proportionnels,  $g = af$  avec  $a \neq 0$ , et un  $x$  tel que  $f(x) \neq 0$  donne  $f(x)g(x) \neq 0$ .

S'ils sont indépendants, l'application  $x \mapsto (f(x), g(x))$  est surjective sur  $K^2$ . Il existe donc  $x$  tel que  $f(x) = g(x) = 1$ , encore une contradiction. Ainsi l'une des deux formes est nulle. □

**Problème 49 Déterminant sous une contrainte de somme des lignes**Soit  $A = (a_{ij}) \in M_n(\mathbb{R})$  telle que

$$\sum_{j=1}^n |a_{ij}| \leq 1 \quad (1 \leq i \leq n).$$

Montrer que  $|\det A| \leq 1$  et caractériser le cas d'égalité.

**Solution.** Notons  $r_i$  les lignes de  $A$ . On a

$$\|r_i\|_2 \leq \|r_i\|_1 \leq 1.$$

L'inégalité de Hadamard donne

$$|\det A| \leq \prod_{i=1}^n \|r_i\|_2 \leq 1.$$

Si l'égalité est atteinte, toutes les inégalités sont des égalités. Les lignes sont donc orthonormées, et pour chaque  $i$ ,

$$\|r_i\|_2 = \|r_i\|_1 = 1.$$

L'égalité entre les normes  $\ell^1$  et  $\ell^2$  impose qu'une ligne possède exactement un coefficient non nul, égal à 1 ou  $-1$ . L'orthogonalité impose que ces positions soient toutes distinctes. Ainsi  $A$  est une matrice de permutation signée.

Réciproquement, toute matrice de permutation signée satisfait l'hypothèse et a déterminant de module 1. □

### Problème 50 Traces des puissances et nilpotence

Soit  $K$  un corps de caractéristique nulle,  $E$  de dimension  $n$ , et  $u \in \mathcal{L}(E)$  tel que

$$\text{tr}(u^k) = 0 \quad (1 \leq k \leq n).$$

Montrer que  $u$  est nilpotent.

**Solution.** Écrivons

$$\chi_u(X) = X^n - e_1 X^{n-1} + e_2 X^{n-2} - \cdots + (-1)^n e_n$$

et  $s_k = \text{tr}(u^k)$ . Les identités de Newton donnent, pour  $1 \leq k \leq n$ ,

$$ke_k = \sum_{j=1}^k (-1)^{j-1} e_{k-j} s_j, \quad e_0 = 1.$$

Tous les  $s_j$  étant nuls et les entiers  $k$  étant inversibles dans  $K$ , on obtient par récurrence  $e_1 = \cdots = e_n = 0$ . Ainsi  $\chi_u(X) = X^n$ . Le théorème de Cayley-Hamilton donne  $u^n = 0$ . □

# Réduction des endomorphismes et calcul matriciel

## Problème 51 À quoi sert la forme de Jordan ?

Donner les principales utilisations de la réduction de Jordan.

**Solution.** La forme de Jordan rend visibles, dans une même représentation :

- les valeurs propres, leurs multiplicités algébriques et géométriques;
- le polynôme minimal et les indices de nilpotence sur les sous-espaces caractéristiques;
- les puissances  $A^k$  et, plus généralement, les fonctions  $f(A)$ ;
- l'exponentielle  $e^{tA}$  et donc la résolution des systèmes différentiels linéaires  $x' = Ax$ ;
- la structure des sous-espaces invariants, du commutant et de l'algèbre  $K[A]$ ;
- les comportements asymptotiques gouvernés par le rayon spectral et la taille des blocs.

Son intérêt est donc moins de « diagonaliser presque » que de séparer proprement la partie spectrale de la partie nilpotente. □

## Problème 52 Une fonction multiplicative détecte l'inversibilité

Soit  $F : M_n(\mathbb{R}) \rightarrow \mathbb{R}$  multiplicative, avec  $F(0) = 0$  et  $F(I_n) = 1$ . Montrer que

$$A \in GL_n(\mathbb{R}) \iff F(A) \neq 0.$$

**Solution.** Si  $A$  est inversible,

$$1 = F(I_n) = F(A)F(A^{-1}),$$

donc  $F(A) \neq 0$ .

Supposons  $A$  singulière, de rang  $r < n$ . Il existe  $P, Q \in GL_n(\mathbb{R})$  tels que

$$PAQ = D = \text{diag}(I_r, 0_{n-r}).$$

Soit  $R$  la matrice d'une permutation cyclique des coordonnées. Les matrices  $R^k D R^{-k}$  sont diagonales et, dans le produit

$$\prod_{k=0}^{n-1} R^k D R^{-k},$$

chaque coordonnée diagonale reçoit au moins un facteur nul. Le produit vaut donc 0. Comme  $R$  est inversible,  $F(R)F(R^{-1}) = 1$  et

$$F(R^k D R^{-k}) = F(D).$$

Par multiplicativité,

$$0 = F(0) = F(D)^n,$$

d'où  $F(D) = 0$ . Comme  $F(P)$  et  $F(Q)$  sont non nuls, l'égalité  $F(D) = F(P)F(A)F(Q)$  impose  $F(A) = 0$ . □

**Problème 53 Caractérisation de la diagonalisabilité par l'algèbre  $K[u]$** Soit  $u \in \mathcal{L}(E)$ . Donner une condition nécessaire et suffisante sur la  $K$ -algèbre  $K[u]$  pour que  $u$  soit diagonalisable sur  $K$ .

**Solution.** On a l'isomorphisme canonique

$$K[u] \simeq K[X]/(\mu_u),$$

où  $\mu_u$  est le polynôme minimal. L'endomorphisme  $u$  est diagonalisable sur  $K$  si et seulement si

$$\mu_u(X) = \prod_{j=1}^r (X - \lambda_j)$$

avec les  $\lambda_j \in K$  deux à deux distincts. Par le théorème chinois, cela équivaut à

$$K[u] \simeq \prod_{j=1}^r K[X]/(X - \lambda_j) \simeq K^r$$

comme  $K$ -algèbre.

Ainsi  $u$  est diagonalisable sur  $K$  si et seulement si  $K[u]$  est une algèbre commutative réduite et totalement déployée, c'est-à-dire isomorphe à un produit fini de copies de  $K$ .  $\square$ 

**Problème 54 Toute matrice complexe est semblable à sa transposée**Montrer que  $A \in M_n(\mathbb{C})$  est semblable à  $A^T$ .

**Solution.** Un bloc de Jordan  $J_m(\lambda)$  est semblable à sa transposée : si  $R_m$  est la matrice qui renverse l'ordre de la base canonique, alors

$$R_m^{-1} J_m(\lambda) R_m = J_m(\lambda)^T.$$

Une somme directe de blocs de Jordan est donc semblable à sa transposée. Si  $A = PJP^{-1}$  est une réduction de Jordan, alors

$$A^T = (P^{-1})^T J^T P^T,$$

et  $J^T \sim J$ . Par transitivité,  $A^T \sim A$ .  $\square$ 

**Problème 55 Diagonalisabilité de  $M$  et de  $\exp M$** Montrer que, pour  $M \in M_n(\mathbb{C})$ ,

$$M \text{ est diagonalisable} \iff e^M \text{ est diagonalisable.}$$

**Solution.** Si  $M = PDP^{-1}$  avec  $D$  diagonale, alors  $e^M = Pe^DP^{-1}$  est diagonalisable.

Réciproquement, considérons un bloc  $J_m(\lambda) = \lambda I + N$ . On a

$$e^{J_m(\lambda)} = e^\lambda e^N, \quad e^N - I = NQ(N),$$

où  $Q(0) = 1$ . La matrice  $Q(N)$  est donc inversible, et  $e^N - I$  a le même indice de nilpotence que  $N$ . Si  $m \geq 2$ , le bloc  $e^{J_m(\lambda)}$  n'est pas diagonalisable. Ainsi  $e^M$  ne peut être diagonalisable que si tous les blocs de Jordan de  $M$  sont de taille 1, c'est-à-dire si  $M$  est diagonalisable.  $\square$ 

**Problème 56 Supplémentaire stable pour un endomorphisme diagonalisable**Soit  $u \in \mathcal{L}(E)$  diagonalisable. Montrer que tout sous-espace  $F \subset E$  admet un supplémentaire stable par  $u$ .

**Solution.** Choisissons une base  $(v_1, \dots, v_n)$  de  $E$  formée de vecteurs propres de  $u$ , et une base  $(f_1, \dots, f_r)$  de  $F$ . Par le lemme d'échange, on peut compléter  $(f_1, \dots, f_r)$  en une base de  $E$  en lui ajoutant certains des  $v_i$ . Si  $G$  est l'espace engendré par ces vecteurs propres ajoutés, alors

$$E = F \oplus G$$

et  $G$  est stable par  $u$ . □

**Remarque.** Sur un corps algébriquement clos, la réciproque est vraie : si tout sous-espace admet un supplémentaire stable, alors  $u$  est diagonalisable.

**Problème 57 Fermeture d'une classe de similitude**Caractériser les matrices complexes dont la classe de similitude est fermée dans  $M_n(\mathbb{C})$ .

**Solution.** La classe de similitude de  $A$  est fermée si et seulement si  $A$  est diagonalisable.

Supposons  $A$  diagonalisable et  $B_k \sim A$  avec  $B_k \rightarrow B$ . Le polynôme minimal  $\mu_A$ , scindé à racines simples, annule tous les  $B_k$ , donc annule  $B$  par passage à la limite. Ainsi  $B$  est diagonalisable. De plus  $\chi_{B_k} = \chi_A$ , et la continuité des coefficients du polynôme caractéristique donne  $\chi_B = \chi_A$ . Deux matrices diagonalisables ayant même polynôme caractéristique sont semblables, donc  $B \sim A$ .

Réciproquement, si  $A$  possède un bloc  $J_m(\lambda)$  avec  $m \geq 2$ , posons

$$D_t = \text{diag}(1, t, t^2, \dots, t^{m-1}).$$

Alors

$$D_t^{-1} J_m(\lambda) D_t = \lambda I_m + t N_m \longrightarrow \lambda I_m \quad (t \rightarrow 0).$$

En appliquant cette conjugaison bloc par bloc, on voit que la partie diagonalisable de la forme de Jordan appartient à l'adhérence de la classe de  $A$ , sans lui être semblable. La classe n'est donc pas fermée. □

**Problème 58 Même polynôme caractéristique et même polynôme minimal**Quel est le plus petit  $n$  pour lequel deux matrices de  $M_n(\mathbb{C})$  peuvent avoir le même polynôme caractéristique et le même polynôme minimal sans être semblables ?

**Solution.** La réponse est  $n = 4$ . Les matrices nilpotentes de types de Jordan  $(2, 1, 1)$  et  $(2, 2)$  ont toutes deux

$$\chi(X) = X^4, \quad \mu(X) = X^2,$$

mais elles ne sont pas semblables, par exemple parce que leurs rangs valent respectivement 1 et 2.

Pour  $n \leq 3$ , la donnée du polynôme caractéristique fixe les valeurs propres et leurs multiplicités totales, tandis que le polynôme minimal fixe la taille du plus grand bloc pour chaque valeur propre. Dans toutes les partitions d'un entier inférieur ou égal à 3, ces informations déterminent entièrement le type de Jordan. Deux telles matrices sont donc semblables. □

**Problème 59 Une matrice triangulaire**  $3 \times 3$ À quelle condition la matrice
$$A = \begin{pmatrix} 1 & a & b \\ 0 & 2 & c \\ 0 & 0 & 2 \end{pmatrix}$$

est-elle diagonalisable?**Solution.** Elle est diagonalisable si et seulement si  $c = 0$ . En effet, l'espace propre associé à 2 est le noyau de
$$A - 2I = \begin{pmatrix} -1 & a & b \\ 0 & 0 & c \\ 0 & 0 & 0 \end{pmatrix}.$$

Il doit avoir dimension 2, puisque 2 a multiplicité algébrique 2. C'est le cas exactement lorsque la matrice ci-dessus a rang 1, donc lorsque  $c = 0$ . Si  $c = 0$ , le polynôme  $(X - 1)(X - 2)$  annule  $A$  et a des racines simples, ce qui confirme la diagonalisabilité. □

**Problème 60 Quand le commutant est-il égal à  $\mathbb{C}[u]$ ?**Soit  $u \in \mathcal{L}(E)$  sur  $\mathbb{C}$ . Lire sur sa forme de Jordan la condition
$$\text{Comm}(u) = \mathbb{C}[u].$$

**Solution.** Cette égalité a lieu si et seulement s'il existe au plus un bloc de Jordan pour chaque valeur propre. Cela équivaut à

$$\mu_u = \chi_u,$$

ou encore à la cyclicité de  $u$ .S'il existe deux blocs associés à une même valeur propre  $\lambda$ , la projection sur l'un de ces blocs, parallèlement aux autres, commute avec  $u$ . Elle ne peut être un polynôme en  $u$ , car un polynôme  $P(u)$  agit par le même scalaire  $P(\lambda)$  sur toute droite propre associée à  $\lambda$ .

Réciproquement, supposons qu'il y ait un unique bloc pour chaque valeur propre. Tout endomorphisme  $v$  commutant avec  $u$  stabilise les sous-espaces caractéristiques. Sur chacun d'eux, le commutant du bloc est l'algèbre des polynômes en ce bloc. On obtient donc des polynômes  $P_i$  sur les différents blocs. Les idéaux  $(X - \lambda_i)^{m_i}$  étant deux à deux premiers entre eux, le théorème chinois fournit un polynôme  $P$  réalisant simultanément toutes les congruences. Alors  $v = P(u)$ . □

**Problème 61 Drapeaux stables**Soit  $u$  un endomorphisme d'un espace  $E$  de dimension  $n$  sur  $K$ .

1. Combien de drapeaux complets stables possède-t-il s'il est diagonalisable à spectre simple?
2. Que peut-on dire si son polynôme minimal est sans facteur carré?

**Solution.** Si le spectre est simple, les espaces propres sont des droites  $Ke_1, \dots, Ke_n$ . Un drapeau stable est obtenu en choisissant l'ordre dans lequel ces droites sont ajoutées : il y en a exactement  $n!$ .

Supposons maintenant  $\mu_u$  sans facteur carré. Si  $\mu_u$  n'est pas scindé sur  $K$ , aucun drapeau complet stable n'existe : une base adaptée à un tel drapeau rendrait  $u$  triangulaire, donc son polynôme minimal serait scindé.

Si  $\mu_u$  est scindé,  $u$  est diagonalisable. Notons  $E_1, \dots, E_s$  ses espaces propres et  $m_i = \dim E_i$ . Un drapeau stable est déterminé par :

- un drapeau complet dans chaque  $E_i$ ;
- un entrelacement des  $s$  drapeaux, soit  $n!/(m_1! \cdots m_s!)$  choix.

Ainsi le nombre total vaut

$$\frac{n!}{m_1! \cdots m_s!} \prod_{i=1}^s \mathcal{F}_{m_i}(K),$$

où  $\mathcal{F}_m(K)$  désigne le nombre de drapeaux complets de  $K^m$ . Si  $K$  est infini, ce nombre est infini dès qu'un  $m_i \geq 2$ ; si tous les  $m_i = 1$ , on retrouve  $n!$ . Si  $K = \mathbb{F}_q$ ,

$$\mathcal{F}_m(\mathbb{F}_q) = \prod_{j=1}^m \frac{q^j - 1}{q - 1}.$$

□

### Problème 62 Sous-espaces stables d'un nilpotent d'indice $n - 1$

Soit  $u$  nilpotent sur un espace de dimension  $n \geq 2$ , d'indice de nilpotence  $n - 1$ . Décrire tous ses sous-espaces stables.

**Solution.** La forme de Jordan de  $u$  est  $J_{n-1}(0) \oplus J_1(0)$ . Posons  $m = n - 1$  et choisissons une base

$$e_1, \dots, e_m, f$$

telle que

$$ue_1 = 0, \quad ue_j = e_{j-1} \quad (2 \leq j \leq m), \quad uf = 0.$$

Écrivons  $E_k = \text{Vect}(e_1, \dots, e_k)$  et  $E_0 = \{0\}$ . Les sous-espaces stables sont exactement :

1.  $\{0\}$ ;
2.  $E_k \oplus Kf$  pour  $0 \leq k \leq m$ ;
3.  $E_{k-1} \oplus K(e_k + cf)$  pour  $1 \leq k \leq m$  et  $c \in K$ .

Pour le voir, projetons  $E_m \oplus Kf$  sur  $E_m$ . Si  $W$  est stable, son image est un sous-espace stable du bloc cyclique  $J_m(0)$ , donc un  $E_k$ . Si  $Kf \subset W$ , on soustrait les composantes suivant  $f$  et l'on obtient  $W = E_k \oplus Kf$ .

Si  $W \cap Kf = \{0\}$ , la projection identifie  $W$  au graphe d'un morphisme de  $K[X]$ -modules  $\phi : E_k \rightarrow Kf$ . Comme  $u$  agit par zéro sur  $Kf$ , on a  $\phi(uE_k) = 0$ , donc  $\phi$  s'annule sur  $E_{k-1}$  et est déterminée par  $\phi(e_k) = cf$ . Cela donne exactement la troisième famille. □

### Problème 63 Sous-multiplicativité de la norme de Frobenius

Pour  $A \in M_n(\mathbb{C})$ , posons

$$\|A\|_F = \sqrt{\text{tr}(A^*A)} = \left( \sum_{i,j} |a_{ij}|^2 \right)^{1/2}.$$

Montrer que  $\|AB\|_F \leq \|A\|_F \|B\|_F$ .

**Solution.** Par Cauchy–Schwarz, pour chaque  $i, j$ ,

$$|(AB)_{ij}|^2 = \left| \sum_k a_{ik} b_{kj} \right|^2 \leq \left( \sum_k |a_{ik}|^2 \right) \left( \sum_k |b_{kj}|^2 \right).$$

En sommant en  $i$  et  $j$ , on obtient

$$\begin{aligned} \|AB\|_F^2 &\leq \sum_{i,j} \left( \sum_k |a_{ik}|^2 \right) \left( \sum_\ell |b_{\ell j}|^2 \right) \\ &= \left( \sum_{i,k} |a_{ik}|^2 \right) \left( \sum_{\ell,j} |b_{\ell j}|^2 \right) \\ &= \|A\|_F^2 \|B\|_F^2. \end{aligned}$$

La prise de la racine carrée donne l'inégalité annoncée. □

**Problème 64 Polynômes nilpotents en un endomorphisme**

Soit  $u \in \mathcal{L}(E)$  sur  $\mathbb{C}$ . Montrer que  $u$  est diagonalisable si et seulement si le seul élément nilpotent de  $\mathbb{C}[u]$  est 0.

**Solution.** Si  $u$  est diagonalisable, tout  $P(u)$  est diagonalisable dans la même base. Un endomorphisme à la fois diagonalisable et nilpotent est nul.

Réciproquement, dans la décomposition de Dunford  $u = s + n$ , la partie nilpotente  $n$  est un polynôme en  $u$ . Si le seul élément nilpotent de  $\mathbb{C}[u]$  est 0, alors  $n = 0$ , donc  $u = s$  est diagonalisable. □

**Problème 65 Dimension maximale d'un espace de matrices nilpotentes**

Quelle est la dimension maximale d'un sous-espace vectoriel de  $M_n(\mathbb{R})$  dont tous les éléments sont nilpotents?

**Solution.** La dimension maximale est

$$\frac{n(n-1)}{2}.$$

L'espace des matrices strictement triangulaires supérieures atteint cette dimension et ne contient que des matrices nilpotentes.

Soit réciproquement  $V \subset M_n(\mathbb{R})$  un sous-espace de dimension strictement supérieure à  $n(n-1)/2$ . Comme

$$\dim S_n(\mathbb{R}) = \frac{n(n+1)}{2},$$

la formule de Grassmann donne  $V \cap S_n(\mathbb{R}) \neq \{0\}$ . Or une matrice symétrique réelle est diagonalisable; si elle est nilpotente, toutes ses valeurs propres sont nulles, donc elle est nulle. Contradiction. □

**Problème 66 Formule de Gelfand en dimension finie**Soit  $A \in M_n(\mathbb{C})$  et soit  $\|\cdot\|$  une norme quelconque sur  $M_n(\mathbb{C})$ . Montrer que

$$\|A^k\|^{1/k} \rightarrow \rho(A).$$

**Solution.** Toutes les normes sur  $M_n(\mathbb{C})$  sont équivalentes. Le facteur d'équivalence disparaît après prise de la racine  $k$ -ième; il suffit donc de travailler avec une norme opérateur subordonnée.

Pour toute norme opérateur,

$$\|A^k\| \geq \rho(A^k) = \rho(A)^k,$$

donc  $\liminf \|A^k\|^{1/k} \geq \rho(A)$ .

Pour la majoration, mettons  $A$  sous forme de Jordan. Si  $\rho(A) = 0$ , alors  $A$  est nilpotente et le résultat est immédiat. Sinon, la formule des puissances d'un bloc montre qu'il existe  $C > 0$  tel que

$$\|A^k\| \leq C k^{n-1} \rho(A)^k.$$

Ainsi

$$\limsup_{k \rightarrow \infty} \|A^k\|^{1/k} \leq \rho(A) \lim_{k \rightarrow \infty} (C k^{n-1})^{1/k} = \rho(A).$$

□**Problème 67 Diagonaliser numériquement une grande matrice symétrique**Comment diagonaliser concrètement, en base orthonormée, une matrice symétrique réelle de taille 100?

**Solution.** On n'utilise pas la méthode des puissances suivie d'une déflation naïve : elle ne calcule efficacement qu'une valeur propre extrémale et peut accumuler les erreurs d'orthogonalité.

La procédure standard est la suivante :

1. réduire  $A$  par réflexions de Householder à une matrice tridiagonale symétrique  $T = Q^T A Q$ , avec  $Q \in O_n(\mathbb{R})$ ;
2. calculer les valeurs propres et les vecteurs propres de  $T$  par un algorithme QR implicite avec décalages, par division-conquête, ou par la méthode MRRR (*multiple relatively robust representations*);
3. remonter les vecteurs propres par multiplication par  $Q$ .

La réduction tridiagonale coûte  $O(n^3)$  opérations. Le calcul des seules valeurs propres de la matrice tridiagonale coûte typiquement  $O(n^2)$ ; si l'on demande tous les vecteurs propres, leur remontée vers la base initiale porte de nouveau le coût global à  $O(n^3)$ . Pour quelques valeurs propres seulement, une méthode de Lanczos est souvent préférable. En pratique, on appelle une routine spécialisée pour matrices symétriques, qui préserve numériquement l'orthogonalité et exploite la stabilité du problème auto-adjoint. □

**Problème 68 Résoudre**  $M^5 = I_2$  sur  $\mathbb{Q}$ 

Déterminer les matrices  $M \in M_2(\mathbb{Q})$  telles que  $M^5 = I_2$ .

**Solution.** Le polynôme minimal  $\mu_M$  divise

$$X^5 - 1 = (X - 1)\Phi_5(X).$$

Or  $\Phi_5(X) = X^4 + X^3 + X^2 + X + 1$  est irréductible sur  $\mathbb{Q}$  et de degré 4, tandis que  $\deg \mu_M \leq 2$ .  
Le seul diviseur unitaire non constant possible est donc  $X - 1$ . Ainsi  $\mu_M = X - 1$  et  $M = I_2$ .  $\square$ 

# Arithmétique élémentaire et approximation diophantienne

## Problème 69 Le rationnel de dénominateur fixé le plus proche

Soient  $x \in \mathbb{R}$  et  $q \geq 1$  un entier. Montrer qu'il existe  $p \in \mathbb{Z}$  tel que

$$\left| x - \frac{p}{q} \right| \leq \frac{1}{2q}.$$

Décrire les choix possibles de  $p$ .

**Solution.** Il suffit de choisir un entier  $p$  le plus proche de  $qx$ . Comme tout réel est à distance au plus  $1/2$  d'un entier,

$$|qx - p| \leq \frac{1}{2},$$

d'où l'inégalité annoncée après division par  $q$ .

Le choix est unique sauf lorsque  $qx \in \mathbb{Z} + \frac{1}{2}$ , auquel cas les deux entiers voisins conviennent. Autrement dit, les meilleures approximations parmi les rationnels écrits sous la forme  $p/q$  s'obtiennent en arrondissant  $qx$  à l'entier le plus proche. La fraction  $p/q$  peut naturellement ne pas être irréductible. □

## Problème 70 Théorème d'approximation de Dirichlet

Montrer que, pour tout  $x \in \mathbb{R}$  et tout entier  $N \geq 1$ , il existe des entiers  $p$  et  $q$  tels que

$$1 \leq q \leq N, \quad \left| x - \frac{p}{q} \right| \leq \frac{1}{qN}.$$

En déduire que, si  $x$  est irrationnel, il existe une infinité de fractions  $p/q$  vérifiant

$$\left| x - \frac{p}{q} \right| < \frac{1}{q^2}.$$

**Solution.** Considérons les  $N + 1$  parties fractionnaires

$$\{0x\}, \{x\}, \dots, \{Nx\} \in [0, 1).$$

Découpons  $[0, 1)$  en  $N$  intervalles de longueur  $1/N$ . Deux de ces parties fractionnaires, disons celles d'indices  $j < k$ , appartiennent au même intervalle. En posant  $q = k - j$ , on obtient  $1 \leq q \leq N$  et un entier  $p$  tel que

$$|qx - p| \leq \frac{1}{N}.$$

La première assertion suit.

Supposons maintenant  $x$  irrationnel. Pour  $q \geq 1$ , notons

$$\|qx\|_{\mathbb{Z}} = \min_{p \in \mathbb{Z}} |qx - p| > 0.$$

Pour chaque  $Q$ , le nombre

$$\delta_Q = \min_{1 \leq q \leq Q} \|qx\|_{\mathbb{Z}}$$

est strictement positif. Si  $N > 1/\delta_Q$ , le couple fourni par la première partie ne peut avoir  $q \leq Q$ ; les dénominateurs obtenus sont donc non bornés.

Pour chacun de ces couples,

$$\left| x - \frac{p}{q} \right| \leq \frac{1}{qN} \leq \frac{1}{q^2}.$$

L'égalité dans la dernière majoration imposerait  $q = N$  et  $x = p/q \pm 1/q^2$ , donc rendrait  $x$  rationnel. L'inégalité est ainsi stricte. Enfin, une même fraction rationnelle  $r$  ne peut apparaître pour des dénominateurs arbitrairement grands : l'inégalité  $|x - r| < q^{-2}$  forcerait alors  $x = r$  par passage à la limite. On obtient donc une infinité de fractions distinctes. □

### Problème 71 Le nombre de Liouville

Montrer que

$$L = \sum_{k=1}^{\infty} 10^{-k!}$$

est transcendant.

**Solution.** Posons

$$L_n = \sum_{k=1}^n 10^{-k!} = \frac{p_n}{q_n}, \quad q_n = 10^{n!}.$$

Le reste vérifie, pour  $n \geq 1$ ,

$$0 < L - L_n = \sum_{k=n+1}^{\infty} 10^{-k!} < 2 10^{-(n+1)!} = \frac{2}{q_n^{n+1}}.$$

Commençons par remarquer que  $L$  est irrationnel. S'il s'écrivait  $L = a/b$  avec  $a, b \in \mathbb{Z}$  et  $b \geq 1$ , alors, puisque  $L_n \neq L$ ,

$$|L - L_n| \geq \frac{1}{bq_n}.$$

Cette minoration contredit, pour  $n$  assez grand, la majoration  $2/q_n^{n+1}$  obtenue ci-dessus.

Rappelons maintenant l'inégalité de Liouville. Si  $\alpha$  est algébrique de degré  $d \geq 2$ , il existe  $c(\alpha) > 0$  tel que, pour toute fraction  $p/q \neq \alpha$ ,

$$\left| \alpha - \frac{p}{q} \right| \geq \frac{c(\alpha)}{q^d}.$$

En effet, si  $P \in \mathbb{Z}[X]$  est le polynôme minimal de  $\alpha$ , alors  $q^d P(p/q)$  est un entier non nul, donc  $|P(p/q)| \geq q^{-d}$ . Sur un voisinage compact de  $\alpha$ , le théorème des accroissements finis donne simultanément

$$|P(p/q)| \leq C |p/q - \alpha|.$$

Les fractions éloignées de  $\alpha$  sont absorbées en diminuant la constante.

Si  $L$  était algébrique, son irrationalité imposerait un degré  $d \geq 2$ . L'inégalité précédente, appliquée à  $p_n/q_n$ , contredirait

$$0 < \left| L - \frac{p_n}{q_n} \right| < \frac{2}{q_n^{n+1}}$$

pour tout  $n > d$  assez grand. Ainsi  $L$  est transcendant.

**Problème 72 Une minoration uniforme de l'indicatrice d'Euler**Montrer que, pour tout entier  $n \geq 1$ ,
$$\varphi(n) \geq \sqrt{\frac{n}{2}}.$$

**Solution.** Écrivons  $n = \prod_{p^a \parallel n} p^a$ . Alors
$$\frac{\varphi(n)^2}{n} = \prod_{p^a \parallel n} \frac{\varphi(p^a)^2}{p^a} = \prod_{p^a \parallel n} p^{a-2}(p-1)^2.$$

Pour  $p \geq 3$ , chaque facteur est au moins
$$\frac{(p-1)^2}{p} > 1.$$

Pour  $p = 2$ , il vaut  $1/2$  lorsque  $a = 1$ , et  $2^{a-2} \geq 1$  lorsque  $a \geq 2$ . Le produit est donc toujours supérieur ou égal à  $1/2$ , ce qui donne le résultat. □**Problème 73 Valeurs extrêmes de  $\varphi(n)/n$** Calculer
$$\limsup_{n \rightarrow \infty} \frac{\varphi(n)}{n} \quad \text{et} \quad \liminf_{n \rightarrow \infty} \frac{\varphi(n)}{n}.$$

**Solution.** Comme  $\varphi(n) \leq n$ , la limite supérieure est au plus 1. Pour  $n = p$  premier,
$$\frac{\varphi(p)}{p} = 1 - \frac{1}{p} \longrightarrow 1,$$

donc
$$\limsup_{n \rightarrow \infty} \frac{\varphi(n)}{n} = 1.$$

Soit maintenant  $N_k = p_1 p_2 \cdots p_k$  le produit des  $k$  premiers nombres premiers. Alors
$$\frac{\varphi(N_k)}{N_k} = \prod_{j=1}^k \left(1 - \frac{1}{p_j}\right).$$

Rappelons brièvement pourquoi  $\sum_p 1/p$  diverge. Si cette série convergait, le produit  $\prod_p (1 - 1/p)^{-1}$  serait borné, puisque  $-\log(1-t) \leq t + 2t^2$  pour  $0 \leq t \leq 1/2$ . Mais, pour tout  $x \geq 2$ ,
$$\prod_{p \leq x} \left(1 - \frac{1}{p}\right)^{-1} = \sum_{\substack{m \geq 1 \\ p \mid m \Rightarrow p \leq x}} \frac{1}{m} \geq \sum_{m \leq x} \frac{1}{m},$$

ce qui est impossible puisque la série harmonique diverge. Enfin,  $\log(1-t) \leq -t$  pour  $0 < t < 1$ , donc
$$\log\left(\frac{\varphi(N_k)}{N_k}\right) = \sum_{j=1}^k \log\left(1 - \frac{1}{p_j}\right) \leq - \sum_{j=1}^k \frac{1}{p_j} \longrightarrow -\infty.$$

Le produit tend vers 0, et par conséquent

$$\liminf_{n \rightarrow \infty} \frac{\varphi(n)}{n} = 0.$$

# **Analyse**

# Calcul différentiel et applications globales

## Problème 74 Un critère global de difféomorphisme

Soit  $f : \mathbb{R}^n \rightarrow \mathbb{R}^n$  de classe  $C^1$ . On suppose qu'il existe  $c > 0$  tel que

$$\|f(x) - f(y)\| \geq c \|x - y\| \quad (x, y \in \mathbb{R}^n).$$

Montrer que  $f$  est un difféomorphisme  $C^1$  de  $\mathbb{R}^n$  sur  $\mathbb{R}^n$ .

**Solution.** En faisant tendre  $t$  vers 0 dans

$$\|f(x + th) - f(x)\| \geq c |t| \|h\|,$$

on obtient

$$\|df_x(h)\| \geq c \|h\|.$$

L'endomorphisme  $df_x$  est donc injectif, puis inversible. Le théorème d'inversion locale montre que  $f$  est un difféomorphisme local; son image est en particulier ouverte.

L'hypothèse implique aussi que  $f$  est injective. Montrons que son image est fermée. Si  $f(x_k)$  converge, alors

$$\|x_k - x_\ell\| \leq c^{-1} \|f(x_k) - f(x_\ell)\|,$$

donc  $(x_k)$  est de Cauchy et converge vers un certain  $x \in \mathbb{R}^n$ . Par continuité,  $f(x_k) \rightarrow f(x)$ . Ainsi  $f(\mathbb{R}^n)$  est à la fois ouvert, fermé et non vide dans l'espace connexe  $\mathbb{R}^n$ ; il est égal à  $\mathbb{R}^n$ .

Enfin, les inverses locaux se recollent, et le théorème d'inversion locale assure que  $f^{-1}$  est de classe  $C^1$ . □

## Problème 75 Une application propre est fermée

Soient  $X$  un espace métrique,  $Y$  un espace métrique localement compact, et  $f : X \rightarrow Y$  une application continue telle que l'image réciproque de tout compact soit compacte. Montrer que  $f$  est fermée.

**Solution.** Soit  $F \subset X$  fermé et soit  $y \notin f(F)$ . Choisissons un voisinage  $V$  de  $y$  dont l'adhérence  $K = \overline{V}$  est compacte. L'ensemble

$$F \cap f^{-1}(K)$$

est fermé dans le compact  $f^{-1}(K)$ ; il est donc compact. Son image par  $f$  est compacte, donc fermée dans  $Y$ , et elle ne contient pas  $y$ . Le voisinage

$$V \setminus f(F \cap f^{-1}(K))$$

de  $y$  est disjoint de  $f(F)$ . Le complémentaire de  $f(F)$  est donc ouvert, et  $f(F)$  est fermé. □

**Problème 76 Théorème fondamental de l'algèbre par inversion locale**Donner une preuve du théorème fondamental de l'algèbre fondée sur le théorème d'inversion locale et la propreté des polynômes.

**Solution.** Soit  $P \in \mathbb{C}[X]$  non constant. Puisque  $|P(z)| \rightarrow \infty$  lorsque  $|z| \rightarrow \infty$ , l'application  $P : \mathbb{C} \rightarrow \mathbb{C}$  est propre.

Notons

$$\Sigma = P(\{z : P'(z) = 0\}),$$

ensemble fini des valeurs critiques, et posons

$$X = \mathbb{C} \setminus P^{-1}(\Sigma), \quad Y = \mathbb{C} \setminus \Sigma.$$

L'ensemble  $X$  est non vide : on n'a retiré à  $\mathbb{C}$  qu'un ensemble fini. La restriction  $P : X \rightarrow Y$  est un difféomorphisme local, donc une application ouverte. Elle est aussi propre : si  $K \subset Y$  est compact, alors  $P^{-1}(K)$  est compact dans  $\mathbb{C}$  et ne rencontre pas  $P^{-1}(\Sigma)$ ; c'est donc exactement l'image réciproque de  $K$  dans  $X$ . D'après le problème précédent,  $P(X)$  est fermé dans  $Y$ .

Or  $Y$ , plan privé d'un ensemble fini, est connexe. L'ensemble  $P(X)$  est non vide, ouvert et fermé dans  $Y$ ; il est donc égal à  $Y$ . Les éléments de  $\Sigma$  appartiennent eux aussi à l'image de  $P$  par définition. Ainsi  $P(\mathbb{C}) = \mathbb{C}$ , et en particulier 0 possède un antécédent.  $\square$ 

**Problème 77 Extrema de  $x^4 + y^4 - 4xy$** Déterminer les points critiques et les extrema globaux de

$$f(x, y) = x^4 + y^4 - 4xy.$$

**Solution.** Les équations critiques sont

$$x^3 = y, \quad y^3 = x.$$

Elles donnent  $x = x^9$ , donc

$$(x, y) \in \{(0, 0), (1, 1), (-1, -1)\}.$$

La matrice hessienne est

$$H_f(x, y) = \begin{pmatrix} 12x^2 & -4 \\ -4 & 12y^2 \end{pmatrix}.$$

En  $(0, 0)$ , ses valeurs propres sont 4 et  $-4$  : l'origine est un point selle. En  $(1, 1)$  et  $(-1, -1)$ , elle est définie positive, avec valeurs propres 8 et 16 : ce sont des minima locaux.

Enfin, en posant  $r^2 = x^2 + y^2$ ,

$$x^4 + y^4 \geq \frac{r^4}{2}, \quad 4|xy| \leq 2r^2,$$

d'où  $f(x, y) \geq r^4/2 - 2r^2 \rightarrow +\infty$ . La fonction est coercive; ses minima globaux sont donc  $(1, 1)$  et  $(-1, -1)$ , de valeur  $-2$ . Elle n'a pas de maximum global.  $\square$ 

**Problème 78 Théorème fondamental de l'algèbre et nombre d'enroulement**Prouver le théorème fondamental de l'algèbre à l'aide du groupe fondamental de  $\mathbb{C}^\times$  ou, de manière équivalente, du nombre d'enroulement.

**Solution.** Soit

$$P(z) = a_n z^n + \cdots + a_0, \quad n \geq 1,$$

et supposons que  $P$  ne s'annule pas. Pour  $R > 0$ , la boucle

$$\gamma_R(t) = \frac{P(Re^{it})}{|P(Re^{it})|}, \quad 0 \leq t \leq 2\pi,$$

est bien définie dans le cercle unité. L'homotopie

$$(s, t) \mapsto \frac{P(sRe^{it})}{|P(sRe^{it})|}$$

la relie à la boucle constante obtenue pour  $s = 0$ . Son nombre d'enroulement est donc nul.

Pour  $R$  assez grand,

$$|a_{n-1}z^{n-1} + \cdots + a_0| < |a_n z^n| \quad (|z| = R).$$

L'homotopie rectiligne entre  $P(z)$  et  $a_n z^n$  ne rencontre alors jamais 0 sur le cercle  $|z| = R$ . La boucle  $\gamma_R$  a donc le même nombre d'enroulement que  $t \mapsto a_n R^n e^{int}$ , à savoir  $n$ . Contradiction. Le polynôme  $P$  possède une racine. □

# Intégration et espaces $L^p$

**Problème 79 Interpolation élémentaire entre espaces  $L^p$** Soit  $(\Omega, \mu)$  un espace mesuré. Si  $1 \leq p < r < q \leq \infty$  et  $f \in L^p(\mu) \cap L^q(\mu)$ , montrer que  $f \in L^r(\mu)$  et établir l'inégalité d'interpolation correspondante.

**Solution.** Choisissons  $\theta \in (0, 1)$  tel que

$$\frac{1}{r} = \frac{\theta}{p} + \frac{1 - \theta}{q},$$

avec la convention  $1/\infty = 0$ . Si  $q < \infty$ , écrivons

$$|f|^r = |f|^{\theta r} |f|^{(1-\theta)r}$$

et appliquons Hölder avec les exposants  $p/(\theta r)$  et  $q/((1 - \theta)r)$ . On obtient

$$\|f\|_r \leq \|f\|_p^\theta \|f\|_q^{1-\theta}.$$

Si  $q = \infty$ , on utilise directement

$$\int |f|^r \leq \|f\|_\infty^{r-p} \int |f|^p,$$

ce qui donne la même formule. □

**Problème 80 Des moments nuls déterminant une fonction continue**Soit  $f \in C([0, 1], \mathbb{C})$  telle que

$$\int_0^1 x^n f(x) dx = 0 \quad (n \in \mathbb{N}).$$

Montrer que  $f = 0$ .

**Solution.** Par linéarité, l'intégrale de  $fP$  est nulle pour tout polynôme complexe  $P$ . Le théorème de Weierstrass fournit une suite de polynômes  $P_k$  convergeant uniformément vers  $\bar{f}$  sur  $[0, 1]$ . Dès lors,

$$0 = \lim_{k \rightarrow \infty} \int_0^1 f(x) P_k(x) dx = \int_0^1 |f(x)|^2 dx.$$

La continuité de  $f$  entraîne  $f = 0$  sur tout l'intervalle. □

**Problème 81 Contrôler  $f'$  par  $f$  et  $f''$  sur la demi-droite**Soit  $f : [0, \infty) \rightarrow \mathbb{C}$  de classe  $C^1$ , et supposons  $f'$  localement absolument continue. Si
$$f \in L^2(0, \infty), \quad f'' \in L^2(0, \infty),$$

montrer que  $f' \in L^2(0, \infty)$ .**Solution.** Pour  $h > 0$ , la formule de Taylor avec reste intégral donne, pour presque tout  $x \geq 0$ ,
$$f'(x) = \frac{f(x+h) - f(x)}{h} - \frac{1}{h} \int_0^h (h-s)f''(x+s) ds.$$

La première fonction du membre de droite a une norme  $L^2(0, \infty)$  au plus égale à  $2 \|f\|_2 / h$ . Par l'inégalité de Minkowski et l'invariance décroissante de la norme par translation vers la gauche sur la demi-droite, la seconde a une norme au plus
$$\frac{1}{h} \int_0^h (h-s) \|f''(\cdot + s)\|_2 ds \leq \frac{h}{2} \|f''\|_2.$$

Le membre de droite appartient donc à  $L^2(0, \infty)$  et coïncide presque partout avec  $f'$ . Ainsi
$$\|f'\|_2 \leq \frac{2}{h} \|f\|_2 + \frac{h}{2} \|f''\|_2 < \infty.$$

L'assertion est démontrée. □**Problème 82 Inégalité de Young pour la convolution**Soient  $f \in L^1(\mathbb{R}^d)$  et  $g \in L^p(\mathbb{R}^d)$ , où  $1 \leq p \leq \infty$ . Montrer que  $f * g$  est défini presque partout, appartient à  $L^p$ , et vérifie
$$\|f * g\|_p \leq \|f\|_1 \|g\|_p.$$

**Solution.** Commençons par  $1 \leq p < \infty$ . Pour  $R > 0$ , posons
$$F_R(x) = \int_{|y| \leq R} |f(y)| |g(x-y)| dy.$$

L'inégalité de Minkowski intégrale donne
$$\|F_R\|_p \leq \int_{|y| \leq R} |f(y)| \|g(\cdot - y)\|_p dy \leq \|f\|_1 \|g\|_p.$$

Lorsque  $R \rightarrow \infty$ , les fonctions  $F_R$  croissent vers  $F(x) = \int |f(y)| |g(x-y)| dy$ . Le lemme de Fatou donne  $F \in L^p$  et  $\|F\|_p \leq \|f\|_1 \|g\|_p$ . En particulier, l'intégrale définissant  $f * g$  est absolument convergente pour presque tout  $x$ , et
$$\|f * g\|_p \leq \|F\|_p \leq \|f\|_1 \|g\|_p.$$

Pour  $p = \infty$ , redéfinissons au besoin  $g$  sur un ensemble nul et choisissons un représentant vérifiant  $|g| \leq \|g\|_\infty$  en tout point. Alors, pour tout  $x$ ,
$$|(f * g)(x)| \leq \int |f(y)| |g(x-y)| dy \leq \|f\|_1 \|g\|_\infty.$$

Cela établit à la fois l'existence presque partout et l'inégalité de Young.

**Problème 83 Une fonction et sa dérivée dans  $L^1$** Soit  $f$  localement absolument continue sur  $\mathbb{R}$ , avec  $f, f' \in L^1(\mathbb{R})$ . Montrer que

$$\lim_{x \rightarrow \pm\infty} f(x) = 0.$$

**Solution.** Puisque  $f \in L^1(0, \infty)$ , il existe une suite  $y_k \rightarrow +\infty$  telle que  $f(y_k) \rightarrow 0$ . Pour  $y_k > x$ ,

$$f(y_k) - f(x) = \int_x^{y_k} f'(t) dt.$$

En faisant tendre  $k$  vers l'infini, on obtient

$$f(x) = - \int_x^\infty f'(t) dt.$$

Par conséquent,

$$|f(x)| \leq \int_x^\infty |f'(t)| dt \rightarrow 0.$$

Le même raisonnement sur  $(-\infty, 0)$  donne la limite en  $-\infty$ . □

**Problème 84 Extraire une sous-suite convergeant presque partout**Soit  $1 \leq p < \infty$ . Montrer que toute suite convergeant dans  $L^p$  possède une sous-suite convergeant presque partout vers la même limite.

**Solution.** Supposons  $f_n \rightarrow f$  dans  $L^p$ . On peut extraire une sous-suite  $(f_{n_k})$  telle que

$$\|f_{n_k} - f\|_p^p \leq 2^{-k}.$$

Par Tonelli,

$$\int \sum_{k=1}^{\infty} |f_{n_k} - f|^p = \sum_{k=1}^{\infty} \|f_{n_k} - f\|_p^p < \infty.$$

La série sous l'intégrale est donc finie presque partout. En particulier,

$$|f_{n_k}(x) - f(x)|^p \rightarrow 0$$

pour presque tout  $x$ . □

**Problème 85 Convergence presque partout et convergence des normes**Soit  $1 \leq p < \infty$ . Supposons que  $f_n, f \in L^p(\mu)$ ,

$$f_n \rightarrow f \quad \text{presque partout,} \quad \|f_n\|_p \rightarrow \|f\|_p.$$

Montrer que  $f_n \rightarrow f$  dans  $L^p$ .

**Solution.** Posons

$$G_n = 2^{p-1}(|f_n|^p + |f|^p) - |f_n - f|^p.$$

L'inégalité triangulaire convexe  $|a - b|^p \leq 2^{p-1}(|a|^p + |b|^p)$  montre que  $G_n \geq 0$ . De plus, la convergence presque partout donne

$$G_n \rightarrow 2^p |f|^p \quad \text{presque partout.}$$

Le lemme de Fatou fournit alors

$$\begin{aligned} 2^p \|f\|_p^p &\leq \liminf_{n \rightarrow \infty} \int G_n \, d\mu \\ &= 2^p \|f\|_p^p - \limsup_{n \rightarrow \infty} \|f_n - f\|_p^p, \end{aligned}$$

où l'on a utilisé  $\|f_n\|_p^p \rightarrow \|f\|_p^p$ . Par conséquent,

$$\limsup_{n \rightarrow \infty} \|f_n - f\|_p^p \leq 0,$$

et donc  $f_n \rightarrow f$  dans  $L^p$ .

# Analyse complexe

**Problème 86 Une interpolation holomorphe impossible**Existe-t-il une fonction holomorphe dans un voisinage de 0 telle que, pour tout entier  $n$  suffisamment grand,

$$f(1/n) = \frac{(-1)^n}{n^3}?$$

**Solution.** Non. Si une telle fonction existait, la continuité donnerait d'abord  $f(0) = 0$ . Écrivons son développement de Taylor

$$f(z) = a_1z + a_2z^2 + a_3z^3 + O(z^4).$$

Comme

$$nf(1/n) = \frac{(-1)^n}{n^2} \longrightarrow 0,$$

on aurait  $a_1 = 0$ . Puis

$$n^2f(1/n) = \frac{(-1)^n}{n} \longrightarrow 0$$

donnerait  $a_2 = 0$ . Il faudrait enfin que

$$n^3f(1/n) \longrightarrow a_3,$$

alors que le membre de gauche vaut  $(-1)^n$  et ne converge pas. Contradiction. □

**Problème 87 Théorème de Hurwitz**Soit  $\Omega \subset \mathbb{C}$  un ouvert connexe. Une suite  $(f_n)$  de fonctions holomorphes sans zéro sur  $\Omega$  converge uniformément sur tout compact vers une fonction holomorphe  $f$ . Montrer que  $f$  est identiquement nulle ou ne s'annule nulle part.

**Solution.** Supposons  $f$  non identiquement nulle et  $f(z_0) = 0$ . Les zéros de  $f$  sont alors isolés. On peut choisir un disque fermé  $\overline{D}(z_0, r) \subset \Omega$  tel que  $f$  ne s'annule pas sur le cercle frontière et possède au moins un zéro dans le disque.

Sur ce cercle,  $|f|$  possède un minimum strictement positif. Pour  $n$  assez grand,

$$|f_n - f| < |f|.$$

Le théorème de Rouché affirme alors que  $f_n$  et  $f$  ont le même nombre de zéros dans le disque, comptés avec multiplicité. Cela contredit l'absence de zéro de  $f_n$ . Ainsi  $f$  ne s'annule pas. □

**Problème 88 Automorphismes holomorphes du plan**Déterminer les bijections holomorphes  $f : \mathbb{C} \rightarrow \mathbb{C}$ .**Solution.** Toute application affine  $z \mapsto az + b$ , avec  $a \neq 0$ , convient. Montrons qu'il n'y en a pas d'autres.

Après avoir remplacé  $f$  par  $f - f(0)$ , supposons  $f(0) = 0$ . L'injectivité assure que 0 est son unique zéro et que  $f'(0) \neq 0$  : un zéro d'ordre au moins 2 empêcherait l'injectivité locale. La fonction

$$g(z) = \frac{z}{f(z)}$$

se prolonge donc en une fonction entière ne s'annulant pas.

La fonction  $f$  est non constante, donc ouverte par le théorème de l'application ouverte. Étant bijective, c'est un homémorphisme de  $\mathbb{C}$  sur lui-même. On a alors  $|f(z)| \rightarrow \infty$  lorsque  $|z| \rightarrow \infty$  : sinon, une suite  $z_n$  tendant vers l'infini aurait une sous-suite telle que  $f(z_n)$  converge, et la continuité de  $f^{-1}$  rendrait cette sous-suite  $(z_n)$  convergente. Il existe donc  $R$  tel que  $|f(z)| \geq 1$  pour  $|z| \geq R$ , et alors  $|g(z)| \leq |z|$ . Sur le disque de rayon  $R$ ,  $g$  est bornée. Ainsi

$$|g(z)| \leq C(1 + |z|)$$

sur  $\mathbb{C}$ . Les estimations de Cauchy montrent qu'une fonction entière de croissance au plus linéaire est un polynôme de degré au plus 1. Or un polynôme affine non constant possède un zéro ; puisque  $g$  n'en a pas,  $g$  est constante. Par conséquent  $f(z) = az$ , puis, avant normalisation,

$$f(z) = az + b, \quad a \in \mathbb{C}^\times, \quad b \in \mathbb{C}.$$

□**Problème 89 Une fonction entière coercive est un polynôme**Soit  $f$  entière et supposons
$$|f(z)| \rightarrow \infty \quad \text{lorsque } |z| \rightarrow \infty.$$

Montrer que  $f$  est un polynôme non constant.

**Solution.** Considérons  $g(w) = f(1/w)$  sur un voisinage épointé de 0. L'hypothèse dit que  $|g(w)| \rightarrow \infty$  lorsque  $w \rightarrow 0$ . Pour  $w$  assez proche de 0, la fonction  $g$  ne s'annule pas ;  $1/g$  est donc holomorphe dans un voisinage épointé de 0 et tend vers 0. Le théorème des singularités amovibles la prolonge holomorphiquement en 0, avec une valeur nulle. Ce zéro est d'ordre fini, donc  $g$  possède un pôle en 0.

Autrement dit, la singularité de  $f$  à l'infini est un pôle. Le développement de Laurent de  $g$  n'a qu'un nombre fini de termes de degré négatif ; en revenant à la variable  $z = 1/w$ , on voit que le développement entier de  $f$  n'a qu'un nombre fini de coefficients non nuls. La fonction  $f$  est donc un polynôme. Elle n'est pas constante puisque son module tend vers l'infini. □

**Problème 90 Théorème fondamental de l'algèbre par Liouville**Donner la preuve la plus courte du théorème fondamental de l'algèbre à l'aide du théorème de Liouville.

**Solution.** Soit  $P$  un polynôme non constant et supposons qu'il ne s'annule pas. Alors  $1/P$  est entière. De plus,

$$\frac{1}{P(z)} \longrightarrow 0 \quad (|z| \rightarrow \infty),$$

donc  $1/P$  est bornée sur le complémentaire d'un disque, et elle est bornée sur ce disque par continuité. Le théorème de Liouville la rend constante, ce qui est impossible puisque  $P$  est non constant. Ainsi  $P$  possède une racine complexe. □

**Problème 91 Complétude de la famille  $(x^{1/k})$** 

Montrer que le sous-espace vectoriel engendré par

$$x \longmapsto x^{1/k}, \quad k \geq 1,$$

est dense dans  $L^2(0, 1)$ .

**Solution.** Soit  $f \in L^2(0, 1)$  orthogonale à toutes ces fonctions. Pour  $\Re z > -1/2$ , définissons la transformée de Mellin

$$F(z) = \int_0^1 f(x)x^z \, dx, \quad x^z = e^{z \log x}.$$

Cette intégrale est bien définie par Cauchy-Schwarz et dépend holomorphiquement de  $z$  dans le demi-plan considéré. L'hypothèse donne

$$F(1/k) = 0 \quad (k \geq 1).$$

Les points  $1/k$  s'accumulent en 0, qui appartient au domaine d'holomorphie. Le principe des zéros isolés impose donc  $F \equiv 0$ .

En particulier,  $F(n) = 0$  pour tout  $n \in \mathbb{N}$ . La fonction  $f$  est orthogonale à tous les polynômes. Ceux-ci sont denses dans  $C([0, 1])$  pour la norme uniforme, puis dans  $L^2(0, 1)$ . On conclut que  $f = 0$  presque partout. L'orthogonal de l'espace engendré est nul, donc cet espace est dense. □

**Problème 92 Calcul de  $\int_0^\infty (1 + x^n)^{-1} \, dx$** 

Pour quel entier  $n \geq 1$  l'intégrale

$$I_n = \int_0^\infty \frac{dx}{1 + x^n}$$

converge-t-elle, et quelle est sa valeur?

**Solution.** L'intégrale diverge pour  $n = 1$  et converge pour  $n \geq 2$ . Pour  $n \geq 2$ , le changement de variable  $t = x^n$  donne

$$I_n = \frac{1}{n} \int_0^\infty \frac{t^{1/n-1}}{1 + t} \, dt = \frac{1}{n} B\left(\frac{1}{n}, 1 - \frac{1}{n}\right).$$

La relation  $B(a, b) = \Gamma(a)\Gamma(b)/\Gamma(a + b)$  et la formule de réflexion d'Euler

$$\Gamma(s)\Gamma(1 - s) = \frac{\pi}{\sin(\pi s)}$$

fournissent

$$I_n = \frac{\pi}{n \sin(\pi/n)}.$$

La même formule se déduit d'un contour en secteur d'angle  $2\pi/n$  appliqué à la fonction  $1/(1+z^n)$ . □

### Problème 93 Décomposition en éléments simples de la cotangente

Établir, pour  $z \notin \mathbb{Z}$ ,

$$\pi \cot(\pi z) = \frac{1}{z} + \sum_{n=1}^{\infty} \left( \frac{1}{z-n} + \frac{1}{z+n} \right) = \frac{1}{z} + \sum_{n=1}^{\infty} \frac{2z}{z^2 - n^2}.$$

Préciser le sens de la convergence.

**Solution.** La seconde série converge normalement sur tout compact de  $\mathbb{C} \setminus \mathbb{Z}$ , car son terme général est  $O(n^{-2})$  uniformément sur un tel compact.

Partons du produit canonique d'Euler

$$\frac{\sin(\pi z)}{\pi z} = \prod_{n=1}^{\infty} \left( 1 - \frac{z^2}{n^2} \right).$$

Sur tout compact évitant  $\mathbb{Z}$ , le produit converge normalement et uniformément loin de zéro; on peut donc y prendre la dérivée logarithmique terme à terme. On obtient

$$\pi \cot(\pi z) - \frac{1}{z} = \sum_{n=1}^{\infty} \frac{-2z/n^2}{1-z^2/n^2} = \sum_{n=1}^{\infty} \frac{2z}{z^2 - n^2}.$$

La notation bilatérale

$$\sum_{n \in \mathbb{Z}} \frac{1}{z-n}$$

doit être comprise au sens symétrique des valeurs principales :

$$\lim_{N \rightarrow \infty} \sum_{n=-N}^N \frac{1}{z-n}.$$

Une sommation non symétrique ne converge pas. □

### Problème 94 Stabilité des racines d'un polynôme

Soit

$$P(X) = a_0 + a_1X + \dots + a_dX^d \quad (a_d \neq 0).$$

Montrer que, si  $Q(X) = b_0 + b_1X + \dots + b_dX^d$  a ses coefficients suffisamment proches de ceux de  $P$ , alors les racines de  $Q$  restent proches de celles de  $P$ , avec conservation des multiplicités totales dans de petits voisinages disjoints.

**Solution.** Notons  $\lambda_1, \dots, \lambda_r$  les racines distinctes de  $P$ , de multiplicités  $m_1, \dots, m_r$ . Choisissons des disques fermés deux à deux disjoints  $D_j$ , centrés en  $\lambda_j$ , dont les frontières ne contiennent aucune racine de  $P$ .

Sur la réunion compacte des cercles  $\partial D_j$ , la quantité  $|P|$  possède un minimum  $\eta > 0$ . La convergence des coefficients entraîne la convergence uniforme des polynômes sur tout compact. Ainsi, si les coefficients de  $Q$  sont assez proches de ceux de  $P$ ,

$$|Q(z) - P(z)| < \eta \leq |P(z)| \quad (z \in \partial D_j, 1 \leq j \leq r).$$

Le théorème de Rouché montre que  $Q$  et  $P$  ont le même nombre de zéros dans chaque  $D_j$ , comptés avec multiplicité. Ce nombre est  $m_j$ .

Comme  $b_d$  reste non nul lorsque les coefficients sont assez proches,  $Q$  a degré  $d$ . Or la somme des nombres de zéros trouvés dans les disques vaut  $m_1 + \dots + m_r = d$ . Il n'existe donc aucune autre racine de  $Q$ . C'est la forme locale, avec multiplicités, de la continuité multivaluée des racines par rapport aux coefficients.  $\square$ 

### Problème 95 Intégrale dépendant holomorphiquement d'un paramètre

Soit  $\Omega \subset \mathbb{C}$  ouvert et  $(T, \mu)$  un espace mesuré. On suppose que  $h : \Omega \times T \rightarrow \mathbb{C}$  vérifie :

1. pour tout  $z \in \Omega$ , la fonction  $t \mapsto h(z, t)$  est mesurable, et, pour presque tout  $t$ , la fonction  $z \mapsto h(z, t)$  est holomorphe;
2. pour tout compact  $K \subset \Omega$ , il existe  $g_K \in L^1(\mu)$  telle que  $|h(z, t)| \leq g_K(t)$  pour  $z \in K$  et presque tout  $t$ .

Montrer que

$$H(z) = \int_T h(z, t) d\mu(t)$$

est holomorphe. Aucune domination séparée de  $\partial h / \partial z$  n'est nécessaire.

**Solution.** La domination locale assure d'abord que  $H$  est bien définie et continue, par convergence dominée. Soit  $\Delta$  un triangle dont l'adhérence est contenue dans  $\Omega$ . Fubini et le théorème de Cauchy donnent

$$\begin{aligned} \int_{\partial \Delta} H(z) dz &= \int_T \left( \int_{\partial \Delta} h(z, t) dz \right) d\mu(t) \\ &= 0. \end{aligned}$$

Le théorème de Morera implique que  $H$  est holomorphe.

La dérivation sous le signe intégral en découle également. Fixons  $z_0 \in \Omega$  et  $r > 0$  tel que  $\overline{D}(z_0, r) \subset \Omega$ . La formule de Cauchy donne, pour presque tout  $t$ ,

$$\partial_z h(z_0, t) = \frac{1}{2\pi i} \int_{|\zeta - z_0| = r} \frac{h(\zeta, t)}{(\zeta - z_0)^2} d\zeta,$$

donc

$$|\partial_z h(z_0, t)| \leq \frac{1}{r} g_{\overline{D}(z_0, r)}(t).$$

La formule de Cauchy appliquée à  $H$ , puis Fubini, donne plus précisément

$$\begin{aligned} H'(z_0) &= \frac{1}{2\pi i} \int_{|\zeta - z_0| = r} \frac{H(\zeta)}{(\zeta - z_0)^2} d\zeta \\ &= \int_T \partial_z h(z_0, t) d\mu(t). \end{aligned}$$

La domination des dérivées et la dérivation sous le signe intégral sont ainsi des conséquences de l'hypothèse locale, non des hypothèses supplémentaires.  $\square$ 

# Convexité, monotonie et variation bornée

## Problème 96 Une application croissante possède un point fixe

Soit  $f : [0, 1] \rightarrow [0, 1]$  croissante, sans hypothèse de continuité. Montrer qu'il existe  $c \in [0, 1]$  tel que  $f(c) = c$ .

**Solution.** Posons

$$A = \{x \in [0, 1] : f(x) \leq x\}.$$

Cet ensemble est non vide puisque  $f(1) \leq 1$ . Soit  $c = \inf A$ .

Si  $c = 0$ , l'inégalité  $f(c) \geq c$  est immédiate puisque  $f$  prend ses valeurs dans  $[0, 1]$ . Si  $c > 0$ , alors, pour tout  $y < c$ , on a  $y \notin A$ , donc  $f(y) > y$ . Comme  $f$  est croissante,

$$f(c) \geq f(y) > y.$$

En faisant tendre  $y$  vers  $c$  par valeurs inférieures, on obtient encore  $f(c) \geq c$ .

D'autre part, il existe une suite  $(x_n)$  dans  $A$  telle que  $x_n \rightarrow c$ . Comme  $c \leq x_n$ ,

$$f(c) \leq f(x_n) \leq x_n.$$

Le passage à la limite donne  $f(c) \leq c$ . Ainsi  $f(c) = c$ . □

## Problème 97 Limite ponctuelle de fonctions convexes

Soit  $I \subset \mathbb{R}$  un intervalle ouvert et soit  $(f_n)$  une suite de fonctions convexes réelles sur  $I$ , convergeant ponctuellement vers une fonction finie  $f$ . Montrer que  $f$  est convexe et que la convergence est uniforme sur tout compact de  $I$ .

**Solution.** Pour  $x, y \in I$  et  $t \in [0, 1]$ , l'inégalité

$$f_n(tx + (1-t)y) \leq tf_n(x) + (1-t)f_n(y)$$

passe à la limite. La fonction  $f$  est donc convexe; étant finie sur un intervalle ouvert, elle y est continue.

Fixons  $[a, b] \subset I$  et choisissons

$$\alpha < a < b < \beta, \quad [\alpha, \beta] \subset I.$$

Les quatre suites  $f_n(\alpha), f_n(a), f_n(b)$  et  $f_n(\beta)$  sont bornées. Pour  $a \leq x < y \leq b$ , la monotonie des pentes sécantes d'une fonction convexe donne

$$\frac{f_n(a) - f_n(\alpha)}{a - \alpha} \leq \frac{f_n(y) - f_n(x)}{y - x} \leq \frac{f_n(\beta) - f_n(b)}{\beta - b}.$$

Les fonctions  $f_n$  sont donc équi-lipschitziennes sur  $[a, b]$ , avec une constante commune  $L$ ; leur limite  $f$  est elle aussi  $L$ -lipschitzienne. Fixons  $\varepsilon > 0$  et choisissons une subdivision de maille inférieure à  $\varepsilon/(3L)$  (le cas  $L = 0$  étant immédiat). La convergence aux points, en nombre fini, de cette subdivision est uniforme à partir d'un certain rang; l'inégalité triangulaire donne alors  $\|f_n - f\|_{\infty, [a, b]} < \varepsilon$ . □

**Problème 98 Les fonctions à variation bornée forment une algèbre de Banach**Pour  $f : [a, b] \rightarrow \mathbb{C}$ , notons  $\text{Var}(f)$  sa variation totale. Montrer que

$$BV([a, b]) = \{f : \text{Var}(f) < \infty\}, \quad \|f\|_{BV} = \|f\|_\infty + \text{Var}(f),$$

est une algèbre de Banach unitaire.

**Solution.** Pour toute subdivision  $a = x_0 < \dots < x_m = b$ ,

$$\begin{aligned} \sum_{j=1}^m |f(x_j)g(x_j) - f(x_{j-1})g(x_{j-1})| &\leq \|f\|_\infty \sum_{j=1}^m |g(x_j) - g(x_{j-1})| \\ &\quad + \|g\|_\infty \sum_{j=1}^m |f(x_j) - f(x_{j-1})|. \end{aligned}$$

En prenant la borne supérieure,

$$\text{Var}(fg) \leq \|f\|_\infty \text{Var}(g) + \|g\|_\infty \text{Var}(f).$$

On en déduit

$$\|fg\|_{BV} \leq \|f\|_{BV} \|g\|_{BV}.$$

La fonction constante 1 est l'unité.

Reste la complétude. Si  $(f_n)$  est de Cauchy pour  $\|\cdot\|_{BV}$ , elle l'est uniformément et converge donc uniformément vers une fonction bornée  $f$ . Pour  $n$  fixé, la semi-continuité inférieure de la variation sous convergence ponctuelle donne

$$\text{Var}(f_n - f) \leq \liminf_{m \rightarrow \infty} \text{Var}(f_n - f_m).$$

Le membre de droite tend uniformément vers 0 lorsque  $n \rightarrow \infty$ . Ainsi  $f \in BV([a, b])$  et  $f_n \rightarrow f$  pour la norme  $BV$ . □

# Analyse de Fourier

**Problème 99 Une fonction dont l'auto-convolution est nulle**Soit  $f \in L^1(\mathbb{R})$  telle que  $f * f = 0$  presque partout. Déterminer  $f$ .

**Solution.** La transformée de Fourier transforme la convolution en produit :

$$\widehat{f * f}(\xi) = \widehat{f}(\xi)^2.$$

Ainsi  $\widehat{f}(\xi)^2 = 0$  pour tout  $\xi$ , donc  $\widehat{f} = 0$ . L'injectivité de la transformée de Fourier sur  $L^1(\mathbb{R})$  donne  $f = 0$  presque partout. □

**Problème 100 La transformée de Fourier de  $L^1$  n'épuise pas  $C_0$** La transformée de Fourier est-elle surjective de  $L^1(\mathbb{R})$  sur  $C_0(\mathbb{R})$  ?

**Solution.** Non. Commençons par dégager une condition nécessaire. Si  $f \in L^1(\mathbb{R})$  est impaire, alors

$$\widehat{f}(\xi) = -2i \int_0^\infty f(x) \sin(\xi x) dx.$$

Pour  $R \geq 1$ , Fubini donne

$$\int_1^R \frac{\widehat{f}(\xi)}{\xi} d\xi = -2i \int_0^\infty f(x) \left( \int_x^{Rx} \frac{\sin u}{u} du \right) dx.$$

La primitive

$$S(t) = \int_0^t \frac{\sin u}{u} du$$

est bornée sur  $[0, \infty)$  et tend vers  $\pi/2$ . L'intégrale intérieure vaut  $S(Rx) - S(x)$ ; elle est uniformément bornée et possède une limite pour tout  $x > 0$ . Par convergence dominée, le membre de gauche admet donc une limite finie lorsque  $R \rightarrow \infty$ .

Considérons maintenant la fonction impaire

$$g(\xi) = \frac{\arctan \xi}{\log(2 + \xi^2)}.$$

Elle appartient à  $C_0(\mathbb{R})$ . Supposons  $g = \widehat{f}$  avec  $f \in L^1$ . Pour  $h(x) = f(x) + f(-x)$ , on a

$$\widehat{h}(\xi) = g(\xi) + g(-\xi) = 0.$$

L'injectivité de la transformée de Fourier sur  $L^1$  donne  $h = 0$  presque partout :  $f$  est impaire. La propriété précédente imposerait alors la convergence de

$$\int_1^R \frac{g(\xi)}{\xi} d\xi.$$

Mais, lorsque  $\xi \rightarrow +\infty$ ,

$$\frac{g(\xi)}{\xi} \sim \frac{\pi}{4\xi \log \xi},$$

et cette intégrale diverge. Ainsi  $g$  n'est la transformée de Fourier d'aucune fonction de  $L^1(\mathbb{R})$ . □

### Problème 101 Lemme de Riemann–Lebesgue

Montrer que, pour tout  $f \in L^1(\mathbb{R}^d)$ ,

$$\widehat{f}(\xi) \rightarrow 0 \quad (\|\xi\| \rightarrow \infty).$$

**Solution.** Il suffit d'abord de traiter  $d = 1$ . Soit  $\varepsilon > 0$ . Choisissons  $g \in C_c^1(\mathbb{R})$  telle que  $\|f - g\|_1 < \varepsilon$ . Une intégration par parties donne, pour  $\xi \neq 0$ ,

$$i\xi \widehat{g}(\xi) = \widehat{g}'(\xi), \quad |\widehat{g}(\xi)| \leq \frac{\|g'\|_1}{|\xi|}.$$

Ainsi  $\widehat{g}(\xi) \rightarrow 0$ . D'autre part,

$$|\widehat{f}(\xi) - \widehat{g}(\xi)| \leq \|f - g\|_1 < \varepsilon.$$

On en déduit  $\widehat{f}(\xi) \rightarrow 0$ .

En dimension  $d$ , on approche de même  $f$  dans  $L^1$  par une fonction  $g \in C_c^1(\mathbb{R}^d)$ . Pour chaque  $\xi \neq 0$ , choisissons  $j$  tel que  $|\xi_j| \geq \|\xi\| / \sqrt{d}$ . Alors

$$|\widehat{g}(\xi)| \leq \frac{\|\partial_j g\|_1}{|\xi_j|} \leq \frac{\sqrt{d}}{\|\xi\|} \max_{1 \leq k \leq d} \|\partial_k g\|_1,$$

ce qui tend vers 0 lorsque  $\|\xi\| \rightarrow \infty$ . L'approximation de  $f$  conclut comme en dimension 1. □

### Problème 102 Support compact simultané d'une fonction et de sa transformée

Soit  $f \in L^1(\mathbb{R})$  à support compact. On suppose que  $\widehat{f}$  est elle aussi à support compact. Montrer que  $f = 0$  presque partout.

**Solution.** La fonction

$$F(z) = \int_{\mathbb{R}} f(t) e^{-itz} dt$$

est entière. En effet, si le support de  $f$  est contenu dans  $[-A, A]$ , l'intégrande et toutes ses dérivées en  $z$  sont, sur chaque compact de  $\mathbb{C}$ , dominées par une constante fois  $|f(t)|$ .

Sur l'axe réel,  $F$  coïncide avec  $\widehat{f}$ , qui est continue. L'hypothèse de support compact implique donc que  $F$  s'annule identiquement sur chacune des deux demi-droites situées hors de ce support, et non seulement presque partout. Le principe des zéros isolés impose  $F \equiv 0$ . L'injectivité de la transformée de Fourier donne alors  $f = 0$  presque partout. □

**Problème 103 Densité de l'espace de Schwartz**Pour quelles valeurs de  $p$  l'espace de Schwartz  $\mathcal{S}(\mathbb{R}^d)$  est-il dense dans  $L^p(\mathbb{R}^d)$ ?**Solution.** Il est dense pour
$$1 \leq p < \infty.$$

En effet, si  $f \in L^p$ , les troncatures
$$f_R = f \mathbf{1}_{B(0,R)} \mathbf{1}_{\{|f| \leq R\}}$$

convergent vers  $f$  dans  $L^p$ . Chaque  $f_R$  est bornée et à support compact. En la convolant avec une approximation de l'identité  $\rho_\varepsilon \in C_c^\infty$ , on obtient
$$f_R * \rho_\varepsilon \in C_c^\infty(\mathbb{R}^d) \subset \mathcal{S}(\mathbb{R}^d)$$

et  $f_R * \rho_\varepsilon \rightarrow f_R$  dans  $L^p$ .L'assertion est fausse pour  $p = \infty$  sur  $\mathbb{R}^d$ . Toute fonction de Schwartz tend vers 0 à l'infini, tandis que la fonction constante 1 reste à distance au moins 1 de chacune d'elles pour la norme uniforme. □**Problème 104 Absence de diviseurs de zéro à support dans une demi-droite**Existe-t-il deux fonctions non nulles  $f, g \in L^1(\mathbb{R})$ , à support contenu dans  $[0, \infty)$ , telles que  $f * g = 0$ ?**Solution.** Non. Pour  $\Im z < 0$ , posons
$$F(z) = \int_0^\infty f(t) e^{-izt} dt, \quad G(z) = \int_0^\infty g(t) e^{-izt} dt.$$

Ces fonctions sont holomorphes dans le demi-plan inférieur : sur tout compact de ce demi-plan, les dérivées de l'intégrande sont dominées par une constante intégrable fois  $|f|$  ou  $|g|$ . Par Fubini,
$$\int_0^\infty (f * g)(t) e^{-izt} dt = F(z)G(z).$$

Si  $f * g = 0$ , alors  $FG = 0$  sur un ouvert connexe. L'anneau des fonctions holomorphes sur un ouvert connexe étant intègre, l'une des deux fonctions, disons  $F$ , est identiquement nulle. Pour tout  $y > 0$ ,
$$F(x - iy) = \int_0^\infty f(t) e^{-yt} e^{-ixt} dt$$

est la transformée de Fourier de  $t \mapsto f(t)e^{-yt} \mathbf{1}_{[0,\infty)}(t)$ . Son injectivité donne  $f(t)e^{-yt} = 0$  presque partout, donc  $f = 0$ . De même,  $G \equiv 0$  implique  $g = 0$ . Il n'existe donc pas deux tels diviseurs de zéro non nuls. □**Problème 105 Idéal de convolution dense sur le tore**Soit  $f \in C(\mathbb{T})$  et
$$E_f = \{f * g : g \in C(\mathbb{T})\},$$

la convolution étant normalisée par  $1/(2\pi)$ . Donner une condition nécessaire et suffisante pour que  $E_f$  soit dense dans  $C(\mathbb{T})$  pour la norme uniforme.**Solution.** La condition est

$$\widehat{f}(n) \neq 0 \quad \text{pour tout } n \in \mathbb{Z}.$$

Elle est nécessaire : si  $\widehat{f}(n_0) = 0$ , alors

$$\widehat{f * g}(n_0) = \widehat{f}(n_0)\widehat{g}(n_0) = 0$$

pour tout  $g$ . La forme linéaire continue  $h \mapsto \widehat{h}(n_0)$  s'annule sur l'adhérence de  $E_f$ , alors qu'elle ne s'annule pas sur  $t \mapsto e^{in_0 t}$ .

Réciproquement, si tous les coefficients de Fourier de  $f$  sont non nuls, alors, avec  $e_n(t) = e^{int}$ ,

$$f * \frac{e_n}{\widehat{f}(n)} = e_n.$$

L'espace  $E_f$  contient donc tous les polynômes trigonométriques. Ceux-ci sont denses dans  $C(\mathbb{T})$  par le théorème de Stone–Weierstrass. Ainsi  $E_f$  est dense. □

### Problème 106 Densité des translatées d'une gaussienne

Montrer que le sous-espace vectoriel engendré par les fonctions

$$g_a(x) = e^{-(x-a)^2}, \quad a \in \mathbb{R},$$

est dense dans  $L^2(\mathbb{R})$ .

**Solution.** Soit  $V$  cet espace et  $f \in V^\perp$ . Avec la convention  $\langle f, h \rangle = \int_{\mathbb{R}} f(x) \overline{h(x)} dx$ , on a, pour tout  $a \in \mathbb{R}$ ,

$$0 = \langle f, g_a \rangle = \int_{\mathbb{R}} f(x) e^{-(x-a)^2} dx = (f * g_0)(a).$$

Ainsi  $f * g_0 = 0$ . Comme  $g_0 \in L^1 \cap L^2$ , le théorème de convolution dans  $L^2$  et le théorème de Plancherel donnent

$$\widehat{f}(\xi)\widehat{g}_0(\xi) = 0 \quad \text{presque partout.}$$

Or

$$\widehat{g}_0(\xi) = \sqrt{\pi} e^{-\xi^2/4} > 0.$$

Donc  $\widehat{f} = 0$  presque partout, puis  $f = 0$ . Ainsi  $V^\perp = \{0\}$  et  $V$  est dense. □

### Problème 107 Transformée de Fourier de l'indicatrice d'un intervalle

Soit  $f = \mathbf{1}_{[a,b]}$  avec  $a < b$ . La fonction  $\widehat{f}$  appartient-elle à  $L^1(\mathbb{R})$ ?

**Solution.** Non. Si  $\widehat{f} \in L^1$ , la formule d'inversion définirait une fonction continue

$$x \mapsto \frac{1}{2\pi} \int_{\mathbb{R}} \widehat{f}(\xi) e^{ix\xi} d\xi$$

égale presque partout à  $f$ . Or aucune fonction continue ne peut être égale presque partout à l'indicatrice d'un intervalle non dégénéré : au voisinage de  $a$  ou de  $b$ , elle devrait prendre par continuité simultanément les valeurs limites 0 et 1.

On peut aussi le voir directement :

$$\widehat{f}(\xi) = e^{-i(a+b)\xi/2} \frac{2 \sin((b-a)\xi/2)}{\xi},$$

et la valeur absolue de cette fonction n'est pas intégrable à l'infini.

# Suites et sous-additivité

## Problème 108 La réciproque du théorème de Cesàro

Si les moyennes de Cesàro d'une suite convergent, la suite elle-même converge-t-elle nécessairement?

**Solution.** Non. Pour  $u_n = (-1)^n$ ,

$$\frac{1}{N} \sum_{n=1}^N u_n \rightarrow 0,$$

alors que la suite  $(u_n)$  oscille entre  $-1$  et  $1$ . □

## Problème 109 Lemme de Fekete

Soit  $(a_n)_{n \geq 1}$  une suite réelle sous-additive :

$$a_{m+n} \leq a_m + a_n \quad (m, n \geq 1).$$

Montrer que

$$\lim_{n \rightarrow \infty} \frac{a_n}{n} = \inf_{m \geq 1} \frac{a_m}{m},$$

la limite pouvant valoir  $-\infty$ .

**Solution.** Fixons  $m \geq 1$  et écrivons  $n = qm + r$ , avec  $0 \leq r < m$ . En itérant la sous-additivité,

$$a_n \leq qa_m + a_r,$$

où l'on peut poser  $a_0 = 0$ . Pour  $m$  fixé, les termes  $a_r$  avec  $0 \leq r < m$  sont bornés. Par conséquent,

$$\limsup_{n \rightarrow \infty} \frac{a_n}{n} \leq \frac{a_m}{m}.$$

Comme ceci vaut pour tout  $m$ ,

$$\limsup_{n \rightarrow \infty} \frac{a_n}{n} \leq \inf_{m \geq 1} \frac{a_m}{m}.$$

L'inégalité inverse pour la limite inférieure est immédiate, puisque chaque  $a_n/n$  est supérieur ou égal à cet infimum. Les deux limites coïncident. □

## Problème 110 La suite $1/(n \sin n)$

La suite

$$u_n = \frac{1}{n \sin n}, \quad n \geq 1,$$

converge-t-elle?

**Solution.** Elle est bien définie, puisque  $\pi$  est irrationnel et qu'aucun entier strictement positif n'est multiple de  $\pi$ .

Comme  $1/(2\pi)$  est irrationnel, le théorème des rotations irrationnelles affirme que les classes de  $n$  modulo  $2\pi$  sont denses dans  $\mathbb{R}/(2\pi\mathbb{Z})$ . Toute queue de cette suite est encore dense. Il existe donc une suite  $n_k \rightarrow \infty$  telle que  $\sin n_k \rightarrow 1$ , et par conséquent

$$u_{n_k} \rightarrow 0.$$

D'autre part, le théorème de Dirichlet fournit une infinité de couples d'entiers  $(p, q)$ , avec  $q \rightarrow \infty$ , tels que

$$\left| \pi - \frac{p}{q} \right| < \frac{1}{q^2}.$$

Alors

$$|p - q\pi| < \frac{1}{q}, \quad |\sin p| = |\sin(p - q\pi)| \leq |p - q\pi| < \frac{1}{q}.$$

Il s'ensuit

$$\frac{1}{p |\sin p|} > \frac{q}{p} \rightarrow \frac{1}{\pi}.$$

La suite  $(u_n)$  possède donc une sous-suite qui tend vers 0 et une autre dont la valeur absolue reste séparée de 0. Elle ne converge pas. □

# Topologie et analyse fonctionnelle

## Problème 111 Point fixe d'une application non expansive sur un compact convexe

Soit  $K$  un compact convexe non vide d'un espace vectoriel normé et soit  $f : K \rightarrow K$  telle que

$$\|f(x) - f(y)\| \leq \|x - y\|.$$

Montrer que  $f$  possède un point fixe.

**Solution.** Fixons  $a \in K$ . Pour  $n \geq 2$ , définissons

$$f_n(x) = \frac{1}{n}a + \left(1 - \frac{1}{n}\right)f(x).$$

La convexité de  $K$  donne  $f_n(K) \subset K$ , et  $f_n$  est une contraction de rapport  $1 - 1/n$ . Comme  $K$  est complet, le théorème du point fixe de Banach fournit un point fixe  $x_n \in K$ .

L'équation  $x_n = f_n(x_n)$  donne

$$x_n - f(x_n) = \frac{1}{n}(a - f(x_n)).$$

Le membre de droite tend uniformément vers 0, puisque  $K$  est borné. Par compacité, une sous-suite  $(x_{n_k})$  converge vers un point  $x \in K$ . La fonction  $f$  est continue, et le passage à la limite donne  $x = f(x)$ . □

## Problème 112 Projection sur le cône positif de $L^2$

Dans l'espace de Hilbert réel  $L^2(\mathbb{R})$ , considérons

$$C = \{f \in L^2(\mathbb{R}) : f \geq 0 \text{ presque partout}\}.$$

Montrer que  $C$  est fermé et convexe, puis déterminer la projection orthogonale sur  $C$ .

**Solution.** La convexité est immédiate. Si  $f_n \in C$  et  $f_n \rightarrow f$  dans  $L^2$ , alors, en notant  $f_- = \max(-f, 0)$ ,

$$0 \leq f_-(x) \leq |f(x) - f_n(x)| \quad \text{presque partout.}$$

Ainsi  $\|f_-\|_2 \leq \|f - f_n\|_2 \rightarrow 0$ , donc  $f_- = 0$  presque partout et  $f \in C$ . Le cône est fermé.

La projection est la partie positive

$$P_C(f) = f_+ = \max(f, 0).$$

En effet, pour tout  $g \in C$ ,

$$\langle f - f_+, g - f_+ \rangle = \int_{\{f < 0\}} f(x)g(x) \, dx \leq 0.$$

**Problème 113 Une isométrie d'un compact dans lui-même**Soit  $(X, d)$  un espace métrique compact et  $f : X \rightarrow X$  une isométrie. Montrer que  $f$  est surjective.

**Solution.** L'application  $f$  est injective et  $f(X)$  est compact, donc fermé. Supposons qu'il existe  $x_0 \notin f(X)$ . Alors

$$\delta = d(x_0, f(X)) > 0.$$

Posons  $x_n = f^n(x_0)$ . Pour tout  $m > n$ ,

$$d(x_n, x_m) = d(x_0, x_{m-n}) \geq \delta,$$

car  $x_{m-n} \in f(X)$ . La suite  $(x_n)$  est donc  $\delta$ -séparée et ne possède aucune sous-suite convergente, en contradiction avec la compactité de  $X$ . Ainsi  $f(X) = X$ . □

**Problème 114 Compactité de la boule unité et dimension finie**Soit  $E$  un espace vectoriel normé. Montrer que  $E$  est de dimension finie si et seulement si sa boule unité fermée est compacte.

**Solution.** En dimension finie, c'est le théorème de Heine-Borel.

Réciproquement, supposons la boule unité fermée  $B$  compacte. Elle admet un recouvrement fini par des boules de rayon  $1/2$ , centrées en  $x_1, \dots, x_N \in B$ . Posons

$$F = \text{Vect}(x_1, \dots, x_N).$$

On a

$$B \subset F + \frac{1}{2}B.$$

En itérant,

$$B \subset F + 2^{-k}B \quad (k \geq 1).$$

Pour tout  $x \in B$ , la distance de  $x$  à  $F$  est donc au plus  $2^{-k}$  pour tout  $k$ , donc elle est nulle. Le sous-espace  $F$ , de dimension finie, est fermé; ainsi  $x \in F$ . On a  $B \subset F$ , puis  $E = F$ . L'espace  $E$  est de dimension finie. □

**Problème 115 Noyau d'une forme linéaire discontinue**Soit  $\ell : E \rightarrow \mathbb{K}$  une forme linéaire sur un espace vectoriel normé. Montrer que  $\text{Ker } \ell$  est fermé ou dense dans  $E$ .

**Solution.** Si  $\ell$  est continue, son noyau est fermé. Supposons  $\ell$  discontinue. Elle est alors non bornée sur la boule unité. On peut choisir  $y_n$  avec  $\|y_n\| \leq 1$  et  $|\ell(y_n)| \geq n$ . En posant

$$x_n = \frac{y_n}{\ell(y_n)},$$

on a  $\ell(x_n) = 1$  et  $x_n \rightarrow 0$ .

Pour tout  $y \in E$ ,

$$y - \ell(y)x_n \in \text{Ker } \ell \quad \text{et} \quad y - \ell(y)x_n \rightarrow y.$$

**Problème 116 Connexité de la sphère unité**Soit  $E$  un espace vectoriel normé réel de dimension au moins 2. Montrer que sa sphère unité est connexe par arcs.

**Solution.** Soient  $x, y$  deux vecteurs unitaires. Si  $y \neq -x$ , le segment  $[x, y]$  ne contient pas 0, et

$$\gamma(t) = \frac{(1-t)x + ty}{\|(1-t)x + ty\|}, \quad 0 \leq t \leq 1,$$

est un chemin continu dans la sphère reliant  $x$  à  $y$ .

Si  $y = -x$ , choisissons un vecteur unitaire  $z$  non colinéaire à  $x$ , ce qui est possible puisque  $\dim E \geq 2$ . On relie  $x$  à  $z$ , puis  $z$  à  $-x$ , par deux chemins de la forme précédente.  $\square$ 

**Problème 117 Peut-on rendre  $\mathbb{Q}$  complet?**Existe-t-il une métrique sur l'ensemble  $\mathbb{Q}$  qui le rende complet? Peut-on en choisir une qui induise la topologie usuelle de  $\mathbb{Q}$ ?

**Solution.** Oui pour la première question. L'ensemble  $\mathbb{Q}$  est dénombrable; choisissons une bijection

$$\phi : \mathbb{Q} \longrightarrow \{0\} \cup \{1/n : n \geq 1\}$$

et posons

$$d(x, y) = |\phi(x) - \phi(y)|.$$

L'espace obtenu est isométrique à un compact de  $\mathbb{R}$ ; il est donc compact et complet.

En revanche, aucune métrique complète ne peut induire sur  $\mathbb{Q}$  sa topologie usuelle. Un espace complètement métrisable est un espace de Baire. Or  $\mathbb{Q}$ , muni de sa topologie usuelle, est la réunion dénombrable de ses singletons, qui sont fermés et d'intérieur vide. Il n'est pas de Baire.  $\square$ 

**Problème 118 Un espace vectoriel topologique complet non normable**Donner un exemple naturel d'espace vectoriel topologique métrisable et complet dont la topologie ne provient d'aucune norme.

**Solution.** L'espace

$$E = C^\infty([0, 1])$$

muni des semi-normes

$$p_k(f) = \max_{0 \leq j \leq k} \|f^{(j)}\|_\infty, \quad k \in \mathbb{N},$$

est un espace de Fréchet. Une métrique compatible est, par exemple,

$$d(f, g) = \sum_{k=0}^{\infty} 2^{-k} \frac{p_k(f - g)}{1 + p_k(f - g)}.$$

Une suite de Cauchy pour cette métrique est uniformément de Cauchy avec chacune de ses dérivées. Les limites uniformes se recollent par le théorème fondamental de l'analyse : la limite de  $f_n^{(j+1)}$  est la dérivée de la limite de  $f_n^{(j)}$ . L'espace est donc complet.

Il n'est pas normable. Supposons qu'une norme  $\|\cdot\|$  définisse cette topologie. Sa boule unité ouverte contient un voisinage de base : il existe  $m \in \mathbb{N}$  et  $\varepsilon > 0$  tels que

$$p_m(f) < \varepsilon \implies \|f\| < 1.$$

Comme  $p_{m+1}$  est continu pour la topologie supposée normique, il existe  $C > 0$  tel que

$$p_{m+1}(f) \leq C \|f\| \quad (f \in E).$$

Le semi-norme  $p_{m+1}$  serait donc borné par  $C$  sur le voisinage  $\{p_m < \varepsilon\}$ .

C'est impossible. Pour  $N \geq 1$ , posons

$$f_N(x) = \frac{\varepsilon}{2(2\pi N)^m} \sin(2\pi N x).$$

Alors  $p_m(f_N) \leq \varepsilon/2$ , tandis que

$$p_{m+1}(f_N) = \varepsilon\pi N \implies \infty.$$

Cette contradiction prouve que la topologie de  $E$  ne provient d'aucune norme. □

### Problème 119 Deux métriques équivalentes, une seule complète

Donner sur un même ensemble deux métriques induisant la même topologie, l'une complète et l'autre non.

**Solution.** Sur  $\mathbb{R}$ , la métrique usuelle

$$d_0(x, y) = |x - y|$$

est complète. La métrique

$$d_1(x, y) = |\arctan x - \arctan y|$$

induit la même topologie, puisque  $\arctan$  est un homéomorphisme de  $\mathbb{R}$  sur  $(-\pi/2, \pi/2)$ .

Cependant, la suite  $x_n = n$  est de Cauchy pour  $d_1$ , car  $\arctan n \rightarrow \pi/2$ , mais elle n'a pas de limite dans  $\mathbb{R}$  pour cette métrique. Ainsi  $d_1$  n'est pas complète. La complétude dépend de la métrique, et non de la seule topologie. □

### Problème 120 Compacité séquentielle dans les espaces métriques

Montrer qu'un espace métrique  $(X, d)$  est compact si et seulement si toute suite de  $X$  possède une valeur d'adhérence, ou, de manière équivalente, une sous-suite convergente.

**Solution.** Supposons  $X$  compact. Si une suite  $(x_n)$  ne possédait aucune valeur d'adhérence, chaque point  $x \in X$  aurait un voisinage ne contenant qu'un nombre fini de termes de la suite. Un sous-recouvrement fini de ces voisinages ne contiendrait alors qu'un nombre fini de termes, contradiction. Dans un espace métrique, une valeur d'adhérence permet d'extraire une sous-suite convergente.

Réciproquement, supposons toute suite pourvue d'une sous-suite convergente. L'espace est totalement borné : sinon, pour un certain  $\varepsilon > 0$ , on construirait par récurrence une suite dont les termes sont deux à deux à distance au moins  $\varepsilon$ , sans sous-suite convergente.

Soit  $(U_i)_{i \in I}$  un recouvrement ouvert de  $X$ . Il possède un nombre de Lebesgue : il existe  $\delta > 0$  tel que toute boule de rayon  $\delta$  soit contenue dans l'un des  $U_i$ . Sinon, on choisirait  $x_n$  tel que  $B(x_n, 1/n)$  ne soit contenu dans aucun  $U_i$ . Une sous-suite convergente vers  $x \in U_{i_0}$  pour  $n$  assez grand, la boule correspondante serait pourtant contenue dans  $U_{i_0}$ , contradiction.

Enfin, une famille finie de boules de rayon  $\delta$  recouvre  $X$  par totale bornitude. En choisissant pour chacune un  $U_i$  qui la contient, on obtient un sous-recouvrement fini. L'espace est compact. □

**Problème 121** Une fonction lisse dont un jet s'annule en chaque pointSoit  $f \in C^\infty(\mathbb{R})$  telle que
$$\forall x \in \mathbb{R}, \quad \exists n \in \mathbb{N}, \quad f^{(n)}(x) = 0.$$

Montrer que  $f$  est un polynôme.**Solution.** Pour  $n \in \mathbb{N}$ , posons
$$S_n = \{x \in \mathbb{R} : f^{(n)}(x) = 0\}$$

et soit  $X$  l'ensemble des points au voisinage desquels  $f$  n'est égale à aucun polynôme. L'ensemble  $X$  est fermé. Il n'a pas de point isolé : si  $x$  était isolé dans  $X$ , la fonction serait polynomiale sur chacun des deux côtés de  $x$  ; la régularité  $C^\infty$  forcerait les deux polynômes à avoir le même jet en  $x$ , donc à coincider, ce qui rendrait  $f$  polynomiale au voisinage de  $x$ .

Supposons  $X$  non vide. C'est alors un espace complet et
$$X = \bigcup_{n \in \mathbb{N}} (X \cap S_n).$$

Le théorème de Baire fournit un entier  $n$  et un intervalle ouvert  $I$  tels que
$$\emptyset \neq X \cap I \subset S_n.$$

Chaque point de  $X \cap I$  est un point d'accumulation de cet ensemble. En dérivant successivement le long de suites de points de  $X \cap I$ , on obtient
$$f^{(n)}(x) = 0 \quad (x \in X \cap I, \quad n \geq n).$$

Sur chaque composante connexe  $J$  de  $I \setminus X$ , la fonction  $f$  est localement polynomiale ; les polynômes locaux se recollent, donc  $f$  coincide sur  $J$  avec un unique polynôme  $P_J$ . Puisque  $X \cap I$  est non vide, toute telle composante possède au moins une extrémité appartenant à  $X \cap I$ . En cette extrémité, toutes les dérivées d'ordre au moins  $n$  s'annulent. Cela impose  $\deg P_J < n$ . Par conséquent  $f^{(n)} = 0$  sur  $J$ , et aussi sur  $X \cap I$ . Ainsi  $f^{(n)} = 0$  sur tout  $I$ , donc  $f$  y est polynomiale, contradiction avec  $X \cap I \neq \emptyset$ .

On a donc  $X = \emptyset : f$  est localement polynomiale partout. Sur l'intervalle connexe  $\mathbb{R}$ , les polynômes locaux coïncident sur leurs recouvrements et se recollent en un seul polynôme global. □

# Probabilités et problème des moments

## Problème 122 Convergence en probabilité sans convergence presque sûre

Construire une suite de variables aléatoires qui converge en probabilité vers 0, mais pas presque sûrement.

**Solution.** Soit  $(X_n)_{n \geq 1}$  une suite indépendante telle que  $X_n$  suive une loi de Bernoulli de paramètre  $1/n$ . Pour  $0 < \varepsilon < 1$ ,

$$\mathbb{P}(|X_n| > \varepsilon) = \mathbb{P}(X_n = 1) = \frac{1}{n} \longrightarrow 0.$$

Ainsi  $X_n \rightarrow 0$  en probabilité.

En revanche,

$$\sum_{n=1}^{\infty} \mathbb{P}(X_n = 1) = \sum_{n=1}^{\infty} \frac{1}{n} = \infty.$$

Par le second lemme de Borel–Cantelli, l’indépendance implique

$$\mathbb{P}(X_n = 1 \text{ une infinité de fois}) = 1.$$

Presque sûrement, la suite n’est donc pas finalement nulle et ne converge pas vers 0. □

## Problème 123 La convergence en loi n’implique pas la convergence en probabilité

Donner un contre-exemple explicite.

**Solution.** Sur un même espace probabilisé, prenons une variable  $X$  et une suite  $(X_n)$  indépendantes, toutes de loi de Bernoulli de paramètre  $1/2$ . Pour tout  $n$ ,  $X_n$  et  $X$  ont exactement la même loi. La suite  $(X_n)$  converge donc en loi vers  $X$ .

Cependant,

$$\mathbb{P}(|X_n - X| > 1/2) = \mathbb{P}(X_n \neq X) = \frac{1}{2}$$

pour tout  $n$ . Il n’y a pas convergence en probabilité. □

## Problème 124 Continuité de la fonction caractéristique

Soit  $X$  une variable aléatoire à valeurs dans  $\mathbb{R}^d$ . Montrer que sa fonction caractéristique

$$\varphi_X(t) = \mathbb{E}[e^{i\langle t, X \rangle}]$$

est continue sur  $\mathbb{R}^d$ .

**Solution.** Si  $t_n \rightarrow t$ , alors

$$e^{i\langle t_n, X \rangle} \rightarrow e^{i\langle t, X \rangle}$$

presque sûrement. Tous ces termes ont un module égal à 1. Le théorème de convergence dominée donne

$$\varphi_X(t_n) \longrightarrow \varphi_X(t).$$

Aucune hypothèse de moment sur  $X$  n'est nécessaire. □

**Problème 125 La loi log-normale n'est pas déterminée par ses moments**

Soit  $X$  telle que  $\log X$  suive la loi normale  $\mathcal{N}(\mu, \sigma^2)$ , avec  $\sigma > 0$ . Construire une famille de lois distinctes possédant tous les mêmes moments entiers positifs que  $X$ .

**Solution.** La densité log-normale est

$$p(x) = \frac{1}{x\sigma\sqrt{2\pi}} \exp\left(-\frac{(\log x - \mu)^2}{2\sigma^2}\right), \quad x > 0.$$

Pour  $|\varepsilon| \leq 1$ , posons

$$p_\varepsilon(x) = p(x) \left[ 1 + \varepsilon \sin\left(\frac{2\pi(\log x - \mu)}{\sigma^2}\right) \right].$$

Le facteur entre crochets appartient à  $[0, 2]$ ;  $p_\varepsilon$  est donc positive. Montrons que la perturbation ne modifie aucun moment. Si  $Z = \log X - \mu \sim \mathcal{N}(0, \sigma^2)$  et  $n \in \mathbb{N}$ , l'intégrale perturbatrice vaut

$$\begin{aligned} & \int_0^\infty x^n p(x) \sin\left(\frac{2\pi(\log x - \mu)}{\sigma^2}\right) dx \\ &= e^{n\mu} \operatorname{Im} \mathbb{E} \exp\left[\left(n + \frac{2\pi i}{\sigma^2}\right) Z\right]. \end{aligned}$$

Or

$$\mathbb{E}e^{wZ} = \exp\left(\frac{\sigma^2 w^2}{2}\right),$$

et la partie imaginaire ci-dessus est proportionnelle à  $\sin(2\pi n) = 0$ . Pour  $n = 0$ , cela montre aussi que  $p_\varepsilon$  est de masse totale 1. Toutes les densités  $p_\varepsilon$  ont donc les moments

$$\mathbb{E}[X^n] = \exp\left(n\mu + \frac{n^2\sigma^2}{2}\right).$$

Elles sont distinctes dès que les paramètres  $\varepsilon$  le sont, car la fonction sinus n'est pas nulle presque partout. On obtient ainsi une famille de Stieltjes de lois différentes possédant exactement les mêmes moments entiers positifs. □

# Fonctions d'une variable réelle

## Problème 126 Toutes les dérivées dominées par un polynôme de degré impair

Soit  $f \in C^\infty(\mathbb{R})$  et supposons qu'il existe un polynôme réel  $P$  de degré impair tel que

$$|f^{(m)}(x)| \leq |P(x)| \quad (m \in \mathbb{N}, x \in \mathbb{R}).$$

Déterminer  $f$ .

**Solution.** Le polynôme  $P$  possède une racine réelle  $x_0$ . L'inégalité impose

$$f^{(m)}(x_0) = 0 \quad (m \in \mathbb{N}).$$

Fixons  $x \in \mathbb{R}$  et notons

$$M_x = \max_{t \in [x_0, x]} |P(t)|,$$

l'intervalle étant pris sans orientation. La formule de Taylor avec reste intégral, tous les coefficients en  $x_0$  étant nuls, donne pour tout  $N \geq 0$ 

$$|f(x)| \leq M_x \frac{|x - x_0|^{N+1}}{(N+1)!}.$$

Le membre de droite tend vers 0 lorsque  $N \rightarrow \infty$ . Ainsi  $f(x) = 0$  pour tout  $x$ , donc

$$f \equiv 0.$$

□

## Problème 127 Bornitude des dérivées intermédiaires

Soit  $n \geq 1$  et  $f \in C^n(\mathbb{R}, \mathbb{C})$ . On suppose que  $f$  et  $f^{(n)}$  sont bornées. Montrer que toutes les dérivées  $f^{(k)}$ ,  $0 \leq k \leq n$ , sont bornées.

**Solution.** Le cas  $n = 1$  est immédiat. Supposons  $n \geq 2$  et posons

$$M_0 = \|f\|_\infty, \quad M_n = \|f^{(n)}\|_\infty.$$

Pour  $j = 1, \dots, n-1$ , la formule de Taylor avec reste intégral donne

$$f(x+j) - f(x) = \sum_{k=1}^{n-1} \frac{j^k}{k!} f^{(k)}(x) + R_j(x),$$

avec

$$|R_j(x)| \leq \frac{j^n}{n!} M_n.$$

Par conséquent, le vecteur

$$Y(x) = (f(x+1) - f(x) - R_1(x), \dots, f(x+n-1) - f(x) - R_{n-1}(x))^T$$

est uniformément borné en  $x$ .

On a  $Y(x) = AX(x)$ , où

$$X(x) = (f'(x), \dots, f^{(n-1)}(x))^T, \quad A_{jk} = \frac{j^k}{k!} \quad (1 \leq j, k \leq n-1).$$

Après multiplication de la  $k$ -ième colonne par  $k!$  puis division de la  $j$ -ième ligne par  $j$ , on obtient la matrice de Vandermonde  $(j^{k-1})_{1 \leq j, k \leq n-1}$ . Les nombres  $1, \dots, n-1$  étant distincts,  $A$  est inversible. Ainsi

$$X(x) = A^{-1}Y(x)$$

est uniformément borné. Toutes les dérivées intermédiaires sont bornées. □

## **Repères bibliographiques**

Les arguments réunis ici relèvent de résultats classiques. Pour les replacer dans un cadre systématique, on pourra notamment consulter :

- D. Perrin, *Cours d'algèbre*;
- X. Gourdon, *Les maths en tête Algèbre* et *Analyse*;
- H. Brezis, *Analyse fonctionnelle*;
- E. M. Stein et R. Shakarchi, *Fourier Analysis* et *Complex Analysis*;
- P. Barbe et M. Ledoux, *Probabilité*.
