r"""Reviewed semantic transcriptions of the MAT101 exercise statements.

The source of truth is the credited MAT101 booklet.  Prose stays as HTML text;
only mathematical content is passed to MathJax with ``\( ... \)`` or
``\[ ... \]`` delimiters.
"""


def curated(body: str) -> dict[str, str]:
    return {
        "html": (
            '<div class="mat101-statement-transcription '
            'mat101-statement-curated" lang="fr">\n'
            f"{body.strip()}\n"
            "</div>"
        ),
        "transcriptionStatus": "curated",
        "mathematicalReviewStatus": "reviewed",
    }


CURATED_STATEMENTS = {
    "1.1": curated(r"""
<p>Mettre sous forme algébrique (c’est-à-dire \(x+iy\), avec \(x\) et \(y\) réels) les nombres complexes suivants (\(a\) et \(b\) sont des réels).</p>
<ol class="mat101-statement-list">
<li>\(1-2i-(-4+7i)\).</li>
<li>\(\overline{1+2i}+\overline{-4+6i}\).</li>
<li>\((1+2i)(-4+6i)\).</li>
<li>\((2-3i)(-3+2i)\).</li>
<li>\((a+ib)^2\).</li>
<li>\((a-ib)^2\).</li>
<li>\(i^{50}\).</li>
<li>\(\overline{\left(\dfrac{1+2i}{-4+6i}\right)}\).</li>
<li>\(\dfrac{3+6i}{3-4i}\).</li>
<li>\(\dfrac{5+2i}{1-2i}\).</li>
<li>\(\dfrac{(5+2i)(1-i)}{(1-2i)-(i-1)}\).</li>
<li>\(\dfrac{-2}{1-i\sqrt3}\).</li>
<li>\(\left(\dfrac{1+i}{2-i}\right)^2+\dfrac{3+6i}{3-4i}\).</li>
<li>\(\dfrac{2+5i}{1-i}+\dfrac{2-5i}{1+i}\).</li>
<li>\(\left(\dfrac{1+i-\sqrt3(1-i)}{1+i}\right)^2\).</li>
</ol>
"""),
    "1.2": curated(r"""
<p>Résoudre les équations suivantes, d’inconnue \(z\in\mathbb C\)&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(z(i-3)=2\).</li>
<li>\(3i+1-iz=4-i\).</li>
<li>\((1-i)z+\overline z=4-3i\).</li>
<li>\(3iz+2\overline z=6i\).</li>
<li>\(\dfrac{2z+i}{1-3iz}=2+3i\).</li>
<li>\(\dfrac{\overline{2z+i}}{1-\overline z}=2+i\).</li>
</ol>
"""),
    "1.3": curated(r"""
<p>Calculer le module et l’argument des nombres complexes suivants.</p>
<ol class="mat101-statement-list">
<li>\(1+i\).</li>
<li>\(3+3i\).</li>
<li>\(1+i\sqrt3\).</li>
<li>\(-1+i\sqrt3\).</li>
<li>\(\sqrt3+i\).</li>
<li>\(-\dfrac43i\).</li>
<li>\(\dfrac{1+i}{1-i}\).</li>
<li>\(\left(\dfrac{1+i}{1-i}\right)^3\).</li>
<li>\((1+i\sqrt3)^4\).</li>
<li>\((1+i\sqrt3)^5+(1-i\sqrt3)^5\).</li>
<li>\(\dfrac{1+i\sqrt3}{\sqrt3-i}\).</li>
<li>\(\dfrac{\sqrt6-i\sqrt2}{2-2i}\).</li>
<li>\(e^{e^{i\theta}}\).</li>
</ol>
"""),
    "1.4": curated(r"""
<p>Parmi les affirmations suivantes, lesquelles sont vraies, lesquelles sont fausses et pourquoi&nbsp;?</p>
<ol class="mat101-statement-list">
<li>Tout nombre réel a pour argument \(0\).</li>
<li>Tout nombre réel strictement négatif a pour argument \(\pi\).</li>
<li>Tout nombre imaginaire pur non nul a pour argument \(\pi/2\) ou \(3\pi/2\).</li>
<li>Le conjugué d’un nombre imaginaire pur est égal à son opposé.</li>
<li>Si deux nombres complexes ont le même argument, alors leur produit est réel.</li>
<li>Le produit de deux nombres imaginaires purs est réel.</li>
<li>Si deux nombres complexes non nuls ont le même argument, alors leur quotient est réel.</li>
<li>Si deux nombres complexes non nuls ont le même module, alors leur quotient a pour module \(1\).</li>
</ol>
"""),
    "1.5": curated(r"""
<p>Soit \(z\) un nombre complexe non nul. Parmi les affirmations suivantes, lesquelles sont vraies, lesquelles sont fausses et pourquoi&nbsp;?</p>
<ol class="mat101-statement-list">
<li>Le module de \(z\) est égal au module de son conjugué.</li>
<li>L’argument de \(z\) est l’opposé de l’argument de son conjugué.</li>
<li>Le produit de \(z\) par une racine \(n\)-ième de l’unité a le même module que \(z\).</li>
<li>L’argument de \(-z\) est l’opposé de l’argument de \(z\).</li>
<li>Si la partie imaginaire de \(z\) est positive, alors son argument est compris entre \(0\) et \(\pi\).</li>
<li>L’argument de \(z^2\) est le double de l’argument de \(z\).</li>
<li>L’argument de \(z/\overline z\) est égal à l’argument de \(z^2\).</li>
</ol>
"""),
    "1.6": curated(r"""
<p>Soient \(a=\rho e^{i\theta}\) et \(b=\rho e^{i\theta'}\) deux nombres complexes de même module.</p>
<ol class="mat101-statement-list">
<li>Montrer que
\[
a+b=2\rho\cos\left(\frac{\theta-\theta'}2\right)e^{i(\theta+\theta')/2}.
\]</li>
<li>Calculer le module et l’argument des nombres complexes suivants (\(\theta\) est un paramètre réel)&nbsp;:
<ol class="mat101-statement-sublist" type="a">
<li>\(1+i(1+\sqrt2)\)&nbsp;;</li>
<li>\((1+\sqrt2)-i\)&nbsp;;</li>
<li>\(e^{i\theta}+e^{2i\theta}\)&nbsp;;</li>
<li>\(1+\cos(\theta)+i\sin(\theta)\).</li>
</ol></li>
</ol>
"""),
    "1.7": curated(r"""
<p>Soit \(a\) un paramètre complexe. Résoudre en l’inconnue complexe \(z\) les équations suivantes&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(az+3=2z+i\).</li>
<li>\(az^2+bz=0\).</li>
</ol>
"""),
    "1.8": curated(r"""
<p>Calculer les racines carrées complexes, sous forme algébrique, des nombres suivants&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(-1\).</li><li>\(i\).</li><li>\(1+i\).</li><li>\(-1-i\).</li>
<li>\(1+i\sqrt3\).</li><li>\(3+4i\).</li><li>\(8-6i\).</li>
<li>\(7+24i\).</li><li>\(3-4i\).</li><li>\(24-10i\).</li>
</ol>
"""),
    "1.9": curated(r"""
<ol class="mat101-statement-list">
<li>Calculer les racines carrées de \((1+i)/\sqrt2\) sous forme algébrique. En déduire les valeurs de \(\cos(\pi/8)\) et \(\sin(\pi/8)\), exprimées à l’aide des quatre opérations standards et du signe \(\sqrt{\phantom{x}}\).</li>
<li>Calculer les racines carrées de \((\sqrt3+i)/2\) sous forme algébrique. En déduire les valeurs de \(\cos(\pi/12)\) et \(\sin(\pi/12)\).</li>
</ol>
"""),
    "1.10": curated(r"""
<p>Résoudre dans \(\mathbb C\) les équations suivantes, en donnant les solutions sous forme algébrique&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(z^2+z+1=0\).</li><li>\(z^2-z+1=0\).</li>
<li>\(z^2+2z+4=0\).</li><li>\(z^2+4z+5=0\).</li>
<li>\(4z^2-2z+1=0\).</li><li>\(z^2+(1+2i)z+i-1=0\).</li>
<li>\(z^2-(3+4i)z-1+5i=0\).</li><li>\(z^2-(1-i)z-i=0\).</li>
<li>\(z^2-(11-5i)z+24-27i=0\).</li>
</ol>
"""),
    "1.11": curated(r"""
<ol class="mat101-statement-list">
<li>Montrer que si \(P\) est un polynôme à coefficients réels et que \(z\) est une racine de \(P\), alors \(\overline z\) est également une racine de \(P\).</li>
<li>Soit \(z\) un nombre complexe non réel. Trouver deux nombres réels \(p,q\) tels que \(z^2+pz+q=0\).</li>
</ol>
"""),
    "1.12": curated(r"""
<p>Résoudre dans \(\mathbb C\) les équations suivantes, en donnant les solutions sous la forme que vous voulez&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(z^3=i\).</li>
<li>\(z^3=\dfrac{-1+i}{4}\).</li>
<li>\(z^3=2-2i\).</li>
<li>\(z^4=1\).</li>
<li>\(z^4=\dfrac{-1+i\sqrt3}{2}\).</li>
<li>\(\left(\dfrac{2z+1}{z-1}\right)^4=1\).</li>
</ol>
"""),
    "1.13": curated(r"""
<p>Montrer les égalités suivantes, en utilisant la formule de Moivre&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(\cos(4x)=8\cos^4(x)-8\cos^2(x)+1\).</li>
<li>\(\sin(4x)=8\cos^3(x)\sin(x)-4\cos(x)\sin(x)\).</li>
</ol>
"""),
    "1.14": curated(r"""
<p>Linéariser les expressions suivantes, c’est-à-dire les écrire comme sommes d’expressions de type \(a\cos(kx)\) et \(b\sin(kx)\), avec \(a,b\in\mathbb R\) et \(k\in\mathbb N\)&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(\cos^3(x)\).</li><li>\(\sin^3(x)\).</li><li>\(\cos^4(x)\).</li>
<li>\(\sin^4(x)\).</li><li>\(\cos^2(x)\sin^2(x)\).</li>
<li>\(\cos(x)\sin^3(x)\).</li><li>\(\cos^3(x)\sin(x)\).</li>
<li>\(\cos^3(x)\sin^2(x)\).</li><li>\(\cos^2(x)\sin^3(x)\).</li>
<li>\(\cos(x)\sin^4(x)\).</li>
</ol>
"""),
    "1.15": curated(r"""
<p>Soient \(A\) et \(B\) deux points du plan d’affixes respectives \(z_A=3+i\) et \(z_B=1+2i\). On note \(O\) l’origine.</p>
<ol class="mat101-statement-list">
<li>Les points \(O\), \(A\) et \(B\) sont-ils alignés&nbsp;?</li>
<li>On note \(C\) le point d’affixe \(-1-i\). Déterminer l’affixe du point \(D\) tel que \(ABCD\) soit un parallélogramme.</li>
<li>Quelle est l’affixe du centre de ce parallélogramme&nbsp;?</li>
</ol>
"""),
    "1.16": curated(r"""
<p>Soient \(A,B,C,D\) quatre points du plan. Soient \(I,J,K,L,M,N\) les milieux respectifs des segments \([A,B]\), \([B,C]\), \([C,D]\), \([D,A]\), \([A,C]\), \([B,D]\).</p>
<ol class="mat101-statement-list">
<li>En utilisant les nombres complexes, montrer que les segments \([I,K]\), \([J,L]\) et \([M,N]\) ont le même milieu.</li>
<li>Montrer que le quadrilatère de sommets \(I,J,K,L\) est un parallélogramme.</li>
</ol>
"""),
    "1.17": curated(r"""
<p>On note \(j\) le nombre complexe \(e^{2i\pi/3}\). Soient \(A,B,C\) trois points du plan d’affixes respectives \(z_A,z_B,z_C\). Montrer que le triangle \(ABC\) est équilatéral si et seulement si</p>
\[
z_A+jz_B+j^2z_C=0
\qquad\text{ou}\qquad
z_A+j^2z_B+jz_C=0.
\]
"""),
    "1.18": curated(r"""
<p>Le but de l’exercice est d’exprimer \(\cos(2\pi/5)\) à l’aide des opérations usuelles. On en déduira une façon de construire un pentagone régulier à l’aide d’une règle non graduée et d’un compas.</p>
<ol class="mat101-statement-list">
<li>Soit \(P\) le polynôme défini par \(P(z)=z^5-1\). Quelles sont les racines complexes de \(P\), exprimées sous forme polaire&nbsp;?</li>
<li>Soit \(Q\) le polynôme défini par \(Q(z)=z^4+z^3+z^2+z+1\). Montrer que \(Q(z)(z-1)=P(z)\). En déduire que les racines complexes de \(Q\) sont
\[
\cos\frac{2\pi}{5}\pm i\sin\frac{2\pi}{5}
\quad\text{et}\quad
\cos\frac{4\pi}{5}\pm i\sin\frac{4\pi}{5}.
\]</li>
<li>Pourquoi l’inverse de \(\cos(2\pi/5)+i\sin(2\pi/5)\) est-il \(\cos(2\pi/5)-i\sin(2\pi/5)\)&nbsp;? Même question avec \(4\pi/5\).</li>
<li>En utilisant l’égalité
\[
Q(z)=z^2\left(z^2+z+1+z^{-1}+z^{-2}\right),
\]
montrer que, si \(z\) est racine de \(Q\), alors \(z+z^{-1}\) est racine du polynôme \(R\) défini par \(R(y)=y^2+y-1\).</li>
<li>Déterminer les racines de \(R\) et montrer qu’elles sont réelles. On les note \(y_1,y_2\), avec \(y_1&gt;0\).</li>
<li>En utilisant les questions précédentes, montrer que
\[
\cos\frac{2\pi}{5}=\frac{-1+\sqrt5}{4}
\quad\text{et}\quad
\cos\frac{4\pi}{5}=\frac{-1-\sqrt5}{4}.
\]</li>
<li>Étant donné un segment de longueur \(1\), comment construire un segment de longueur \(\sqrt5\) à l’aide d’une règle non graduée, d’une équerre et d’un compas&nbsp;? (Penser à Pythagore.)</li>
<li>En déduire comment construire un segment de longueur \(\cos(2\pi/5)\).</li>
<li>En déduire comment construire, à partir d’un repère orthonormé, le point de coordonnées \((\cos(2\pi/5),\sin(2\pi/5))\) à la règle et au compas.</li>
<li>Comment construire un pentagone régulier à la règle et au compas&nbsp;?</li>
</ol>
"""),
    "1.20": curated(r"""
<p>On note \(\mathcal G\) l’ensemble des nombres qui s’écrivent \(m^2+n^2\), avec \(m\) et \(n\) deux entiers relatifs.</p>
<ol class="mat101-statement-list">
<li>Donner un exemple d’entier naturel qui est dans \(\mathcal G\) et un exemple d’entier naturel qui n’est pas dans \(\mathcal G\).</li>
<li>En utilisant la formule \(\lvert zz'\rvert^2=\lvert z\rvert^2\lvert z'\rvert^2\), pour \(z,z'\in\mathbb C\), montrer que \(\mathcal G\) est stable par produit, c’est-à-dire que si \(p,q\in\mathcal G\), alors \(pq\in\mathcal G\).</li>
<li>En déduire que \(221\) est dans \(\mathcal G\).</li>
</ol>
"""),
    "2.1": curated(r"""
<p>Écrire en extension, c’est-à-dire en donnant tous leurs éléments, les ensembles suivants&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(\{1,2,3\}\cup\{4,5,6\}\).</li>
<li>\(\{1,2,3\}\cup\{3,4,5\}\).</li>
<li>\(\{1,2,3\}\cup\{1,3,4\}\).</li>
<li>\(\{1,2,3\}\cap\{4,5,6\}\).</li>
<li>\(\{1,2,3\}\cap\{2,3,4\}\).</li>
<li>\((\{1,2\}\cup\{1,3\})\cap\{3,4\}\).</li>
<li>\((\{1,2,3\}\cap\{2,3,4\})\cup\{5,6\}\).</li>
<li>\((\{1,2\}\cup\{3,4\})\cap\{2,4\}\).</li>
<li>\((\{1,\{2\}\}\cup\{2,3\})\cap\{\{2\},\{3\}\}\).</li>
<li>\((\{1,\{2\}\}\cap\{\{2\},\{3\}\})\cap\{\{2\},3\}\).</li>
<li>L’ensemble des nombres entiers compris entre \(\sqrt2\) et \(2\pi\).</li>
</ol>
"""),
    "2.2": curated(r"""
<p>On note \(A=\{1,2,3\}\) et \(B=\{-1,0,1\}\). Écrire en extension les ensembles suivants&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(A\cap B\).</li><li>\(A\cup B\).</li><li>\(A\setminus B\).</li><li>\(B\setminus A\).</li>
<li>\(\{x+2\mid x\in A\}\).</li><li>\(\{2x\mid x\in B\}\).</li>
<li>\(\{1/x\mid x\in A\}\).</li><li>\(\{x+y\mid(x,y)\in A\times B\}\).</li>
<li>\(\{x+y\mid(x,y)\in A\times A\}\).</li><li>\(\{x+x\mid x\in A\}\).</li>
<li>\(\{xy\mid(x,y)\in A\times B\}\).</li><li>\(\{x\in A\mid x\ge2\}\).</li>
<li>\(\{x\in B\mid x\ge2\}\).</li><li>\(\{y\in A\mid y\le5\}\).</li>
<li>\(\{z\in A\cup B\mid z\ge0\}\).</li>
</ol>
"""),
    "2.3": curated(r"""
<p>Écrire le plus simplement possible les ensembles suivants (aucune justification n’est attendue).</p>
<ol class="mat101-statement-list">
<li>\([0,1]\cup[1,2]\).</li>
<li>\([0,1]\cap[1,2]\).</li>
<li>\([0,1]\cap\mathbb Z\).</li>
</ol>
"""),
    "2.4": curated(r"""
<p>Écrire les ensembles suivants comme intervalles ou réunions d’intervalles de \(\mathbb R\)&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(\{x\in\mathbb R\mid2\le x&lt;6\}\).</li>
<li>\(\{x\in\mathbb R\mid|x|&lt;0{,}5\}\).</li>
<li>\(\{x\in\mathbb R\mid|x-2|&lt;0{,}1\}\).</li>
<li>\(\{x\in\mathbb R\mid|x-5|\le0{,}01\}\).</li>
<li>\(\{x\in\mathbb R\mid|x-0{,}1|&lt;0{,}2\}\).</li>
<li>\(\{x\in\mathbb R\mid x^2&lt;3\}\).</li>
<li>\(\{x\in\mathbb R\mid x^4\ge1\}\).</li>
<li>\(\{x\in\mathbb R\mid x^2-x\ge0\}\).</li>
</ol>
"""),
    "2.5": curated(r"""
<p>Écrire le plus simplement possible les ensembles suivants (justifier).</p>
<ol class="mat101-statement-list">
<li>\(\{x\in\mathbb R\mid |x|=3\}\).</li>
<li>\(\{x\in\mathbb R\mid2\le |x|\le6\}\).</li>
<li>\(\{x\in\mathbb Q\mid |x|\le3\}\).</li>
<li>\(\{x\in\mathbb R\mid |x|=\lfloor x\rfloor\}\).</li>
<li>\(\displaystyle\bigcup_{i\in[\![1,3]\!]}\ \bigcap_{j\in\{2,3\}}[i+j,i+2j]\).</li>
</ol>
"""),
    "2.6": curated(r"""
<p>Parmi les ensembles suivants, lesquels sont inclus dans lesquels&nbsp;?</p>
<ol class="mat101-statement-list">
<li>\([0,1]\).</li><li>\(]-1,1[\).</li><li>\([0,\tfrac12]\).</li>
<li>\(\{x\in\mathbb R\mid x^2-x=0\}\).</li>
<li>\(\{x\in\mathbb R\mid |x|&lt;\tfrac15\}\).</li>
<li>\(\{x\in\mathbb R\mid |x-0{,}2|&lt;0{,}1\}\).</li>
<li>\(\{x\in\mathbb R\mid x^3-2x^2-x+2&gt;0\}\).</li>
</ol>
"""),
    "2.7": curated(r"""
<p>Les ensembles suivants coïncident-ils&nbsp;?</p>
<ol class="mat101-statement-list">
<li>\(\{1,1,2\}\) et \(\{2,1\}\)&nbsp;;</li>
<li>\(\{1,(1,2)\}\) et \(\{(1,1)\}\)&nbsp;;</li>
<li>\(\{(1,1),(1,2)\}\) et \(\{(1,1),(2,1)\}\)&nbsp;;</li>
<li>\(\{\{1\},\{1,2\}\}\) et \(\{\{1\},\{2,1\}\}\)&nbsp;;</li>
<li>\(\{0,1,2,3\}\) et \(\{x\in\mathbb Z\mid x\le3\}\)&nbsp;;</li>
<li>\(\{0,1,2,3\}\) et \(\{x\in\mathbb N\mid x\le3\}\)&nbsp;;</li>
<li>\([\![1,3]\!]\times[\![0,3]\!]\) et \(\{(x,y)\in\mathbb N^2\mid1\le x\le3,\ 0\le y\le3\}\)&nbsp;;</li>
<li>\(\{(x,y)\in\mathbb N^2\mid0\le x&lt;y\le3\}\) et \(\{(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)\}\).</li>
</ol>
"""),
    "2.8": curated(r"""
<p>Soient \(A\), \(B\) et \(C\) trois sous-ensembles d’un ensemble \(E\).</p>
<ol class="mat101-statement-list">
<li>Simplifier \((A\cap B\cap C)\cup(A^c\cap B\cap C)\cup B^c\cup C^c\).</li>
<li>Démontrer que
\[
(A\cap B^c)\cap C^c=A\cap(B\cup C)^c=(A\cap C^c)\cap B^c.
\]</li>
<li>A-t-on toujours
\[
(A\cup B)\cap(A^c\cup C^c)\cap B^c\cap(A^c\cup B\cup C)=\varnothing\ ?
\]</li>
</ol>
"""),
    "2.9": curated(r"""
<p>Lorsque \(T\) est un tableau de nombres, on note \(T(i,j)\) le contenu de la case située à l’intersection de la ligne \(i\) et de la colonne \(j\). On considère les quatre assertions suivantes, portant sur des tableaux ayant au moins quatre lignes et quatre colonnes&nbsp;:</p>
\[
\begin{aligned}
A&:\ \forall i\in\{1,\ldots,4\},\ \forall j\in\{1,\ldots,4\},\ T(i,j)=1,\\
B&:\ \forall i\in\{1,\ldots,4\},\ \exists j\in\{1,\ldots,4\},\ T(i,j)=1,\\
C&:\ \exists i\in\{1,\ldots,4\},\ \forall j\in\{1,\ldots,4\},\ T(i,j)=1,\\
D&:\ \exists i\in\{1,\ldots,4\},\ \exists j\in\{1,\ldots,4\},\ T(i,j)=1.
\end{aligned}
\]
<p>Pour chacun des tableaux ci-dessous, dire quelles assertions sont vérifiées parmi \(A,B,C,D\).</p>
\[
\begin{aligned}
\text{(a)}\quad T&=\begin{pmatrix}0&1&0&1\\1&1&0&0\\0&0&0&1\\0&0&1&0\end{pmatrix},
&\text{(b)}\quad T&=\begin{pmatrix}1&1&1&1\\1&1&1&1\\1&1&1&1\\1&1&1&1\end{pmatrix},\\
\text{(c)}\quad T&=\begin{pmatrix}0&1&0&1\\0&0&0&0\\1&1&1&1\\1&0&0&0\end{pmatrix},
&\text{(d)}\quad T&=\begin{pmatrix}1&0&0&1\\0&1&0&0\\0&1&0&0\\1&1&1&1\end{pmatrix}.
\end{aligned}
\]
"""),
    "2.10": curated(r"""
<p>Écrire des assertions à l’aide de quantificateurs traduisant les énoncés suivants.</p>
<ol class="mat101-statement-list">
<li>Tout nombre réel positif est le carré d’un nombre réel.</li>
<li>Tout élément de \(\mathcal P\) est le double d’un entier.</li>
<li>Pour tout entier relatif, il existe un entier relatif plus grand.</li>
<li>Pour tout nombre réel, il existe un nombre rationnel tel que la différence des deux est plus petite que \(0{,}1\) en valeur absolue.</li>
<li>Tout nombre complexe non nul est le carré de deux nombres complexes distincts.</li>
<li>Il existe deux nombres réels irrationnels dont le produit est rationnel.</li>
</ol>
"""),
    "2.11": curated(r"""
<p>Soient \(P,Q,R\) trois assertions, et \(a,b,c\) trois nombres réels. Écrire la négation des assertions suivantes.</p>
<ol class="mat101-statement-list">
<li>\(P\land(\neg Q)\).</li>
<li>\((P\Longrightarrow Q)\land R\).</li>
<li>\(\exists x\in[1,+\infty[,\ a\ge b+x\).</li>
<li>\(\exists x\in\mathbb R_+,\ a=b+x\).</li>
<li>\(a=b=c\).</li>
</ol>
"""),
    "2.12": curated(r"""
<p>Pour chacune des assertions ci-dessous, dire quelles variables sont liées. Dire ensuite si l’assertion dépend d’un paramètre. Écrire chaque assertion en français. On rappelle qu’une assertion est <em>close</em> si elle ne dépend pas d’un paramètre. Dire pour chaque assertion close si elle est vraie ou fausse.</p>
<ol class="mat101-statement-list">
<li>\(x\ge y\).</li>
<li>\(\forall x\in\mathbb R,\ x\ge y\).</li>
<li>\(\forall x\in\mathbb R,\ x\ge0\).</li>
<li>\(\forall x\in\mathbb R,\ \exists y\in\mathbb R,\ x\ge y\).</li>
<li>\(\exists x\in\mathbb R,\ \forall y\in\mathbb R,\ x\ge y\).</li>
<li>\(\forall x\in\mathbb R,\ \exists y\in\mathbb N,\ x\ge y\).</li>
<li>\(\forall x\in\mathbb R,\ \exists y\in\mathbb Z,\ x\ge y\).</li>
<li>\(\forall x\in\mathbb R,\ \exists y\in\mathbb Z,\ \bigl(x\ge y\ \text{et}\ (\forall z\in\mathbb Z,\ x\ge z\Rightarrow y\ge z)\bigr)\).</li>
</ol>
"""),
    "2.13": curated(r"""
<p>Dire si les assertions suivantes sont vraies ou fausses, et le démontrer.</p>
<ol class="mat101-statement-list">
<li>\(1+1=2\Longrightarrow1+1=3\).</li>
<li>\(1+1=3\Longrightarrow1+1=2\).</li>
<li>\(1=0\Longrightarrow(\exists a,b\in\mathbb N^*,\ a^2+b^2=0)\).</li>
<li>\(\forall x\in\mathbb R,\ x&gt;2\Longrightarrow x\ge3\).</li>
<li>\(\forall x\in\mathbb R,\ x&gt;3\Longrightarrow x\ge3\).</li>
<li>\(\forall x\in\mathbb R,\ x\in[2,3]\Longrightarrow x\in[0,4]\).</li>
<li>\(\forall x\in\mathbb R,\ x\in[2,3]\Longrightarrow x\le3\).</li>
<li>\(\forall x\in\mathbb R,\ x\notin[2,3]\Longrightarrow x\ge3\).</li>
<li>\(\forall x\in\mathbb R,\ x\notin[2,+\infty[\Longrightarrow x\le3\).</li>
<li>\(\forall x,y\in\mathbb R_+^*,\ x&gt;y\Longrightarrow\dfrac1x&lt;\dfrac1y\).</li>
<li>\(\exists x\in\mathbb R_+^*,\ x&lt;\sqrt x\).</li>
<li>\(\exists x\in\mathbb R,\ \exists y\in\mathbb R,\ x+y&gt;0\).</li>
<li>\(\exists x\in\mathbb R,\ \forall y\in\mathbb R,\ x+y&gt;0\).</li>
<li>\(\forall x\in\mathbb R,\ \exists y\in\mathbb R,\ x+y&gt;0\).</li>
<li>\(\forall x\in\mathbb R,\ \forall y\in\mathbb R,\ x+y&gt;0\).</li>
<li>\(\forall\varepsilon\in\mathbb R,\ \exists x\in\mathbb R,\ |x|&lt;\varepsilon\).</li>
<li>\(\forall\varepsilon\in\mathbb R,\ \exists x\in\mathbb R,\ x&lt;|\varepsilon|\).</li>
<li>\(\forall\varepsilon\in\mathbb R^*,\ \exists x\in\mathbb R,\ x&lt;|\varepsilon|\).</li>
<li>\(\exists t\in\mathbb R_+^*,\ \forall x\in\mathbb R,\ |x|&lt;t\Longrightarrow x^2&lt;3\).</li>
</ol>
"""),
    "2.14": curated(r"""
<p>Soient \(A,B,C\) trois sous-ensembles d’un ensemble \(E\). Écrire en fonction de \(A,B,C\) les ensembles correspondant aux assertions suivantes.</p>
<ol class="mat101-statement-list">
<li>\(x\) appartient aux trois.</li>
<li>\(x\) appartient au moins à l’un d’entre eux.</li>
<li>\(x\) appartient à deux d’entre eux au plus.</li>
<li>\(x\) appartient à l’un d’entre eux exactement.</li>
<li>\(x\) appartient à deux d’entre eux au moins.</li>
<li>\(x\) appartient à l’un d’entre eux au plus.</li>
</ol>
"""),
    "2.15": curated(r"""
<p>Soient \(P,Q,R\) des assertions. À l’aide d’une table de vérité, vérifiez que l’implication</p>
\[
\bigl((P\Rightarrow Q)\land(Q\Rightarrow R)\bigr)\Rightarrow(P\Rightarrow R)
\]
<p>est toujours vraie.</p>
"""),
    "2.16": curated(r"""
<p>Soient \(P\) et \(Q\) deux assertions. L’assertion \(P\oplus Q\), qui se lit «&nbsp;\(P\) ou exclusif \(Q\)&nbsp;», est vraie si exactement l’une des deux assertions \(P\) et \(Q\) est vraie.</p>
<ol class="mat101-statement-list">
<li>Donner la table de vérité de \(P\oplus Q\) selon les valeurs de vérité de \(P\) et \(Q\).</li>
<li>Démontrer \(P\oplus Q\Longleftrightarrow(P\land\neg Q)\lor(\neg P\land Q)\).</li>
<li>Démontrer \(P\oplus Q\Longleftrightarrow(P\lor Q)\land\neg(P\land Q)\).</li>
</ol>
"""),
    "2.17": curated(r"""
<p>Soit \(a\) un paramètre réel. Résoudre en l’inconnue réelle \(x\) les inéquations suivantes&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(ax+3\le2x+1\).</li>
<li>\(|3x-1|\le|x+4|\).</li>
</ol>
"""),
    "2.18": curated(r"""
<p>Soit \(a\) un nombre réel. On note \(\mathcal D_a\) la droite d’équation \(y=x+2a\) et \(\mathcal C_a\) le cercle de centre \((a,1)\) et de rayon \(1\).</p>
<ol class="mat101-statement-list">
<li>Pour quelles valeurs de \(a\) existe-t-il des points communs à \(\mathcal D_a\) et \(\mathcal C_a\)&nbsp;?</li>
<li>Existe-t-il des valeurs de \(a\) pour lesquelles \(\mathcal D_a\) est tangente à \(\mathcal C_a\)&nbsp;?</li>
</ol>
"""),
    "2.19": curated(r"""
<p>Les affirmations suivantes sont-elles vraies ou fausses&nbsp;? Pourquoi&nbsp;?</p>
<ol class="mat101-statement-list">
<li>Le produit de trois nombres réels est négatif si et seulement si l’un d’entre eux est négatif, les deux autres étant positifs.</li>
<li>Le produit de \(n\) nombres réels est positif si et seulement si un nombre pair d’entre eux sont négatifs, les autres étant positifs.</li>
</ol>
"""),
    "2.20": curated(r"""
<ol class="mat101-statement-list">
<li>Écrire la contraposée de
\[
\forall x,y\in\mathbb R,\quad (x+y)&gt;2\Rightarrow(x&gt;1\lor y&gt;1).
\]</li>
<li>Démontrer l’assertion ou sa contraposée.</li>
<li>Énoncer précisément la réciproque de cette assertion, et déterminer si elle est vraie ou fausse.</li>
</ol>
"""),
    "2.21": curated(r"""
<p><em>Conjectures de Goldbach.</em> La conjecture de Goldbach forte affirme que tout nombre pair supérieur ou égal à \(4\) est la somme de deux nombres premiers. La conjecture de Goldbach faible affirme que tout nombre impair supérieur ou égal à \(7\) est la somme de trois nombres premiers.</p>
<ol class="mat101-statement-list">
<li>Traduire les deux énoncés par des assertions mathématiques à l’aide de symboles.</li>
<li>Montrer que la conjecture forte implique la conjecture faible. La conjecture faible implique-t-elle la conjecture forte&nbsp;?</li>
</ol>
<p><strong>Remarque.</strong> En 2013, Harald Helfgott a démontré la conjecture de Goldbach faible.</p>
"""),
    "2.22": curated(r"""
<p>Démontrer que, pour tout entier naturel \(n\), le nombre</p>
\[
\frac{10^n-1}{9}
\]
<p>est entier. On pourra faire une récurrence.</p>
"""),
    "2.24": curated(r"""
<p>Soient \(a\) et \(b\) deux nombres réels. Montrer que si la somme \(a+b\) est irrationnelle, c’est-à-dire \(a+b\notin\mathbb Q\), alors \(a\) ou \(b\) est irrationnel. On pourra considérer la contraposée.</p>
"""),
    "2.25": curated(r"""
<p>Résoudre l’équation \(\sqrt{x+2}=x\) pour \(x\ge-2\).</p>
"""),
    "2.26": curated(r"""
<p>On considère les propriétés suivantes de l’ordre total sur \(\mathbb R\), valables pour tous réels \(a,b,c\)&nbsp;:</p>
\[
\begin{aligned}
(a\le b\ \text{et}\ b\le c)&\Rightarrow a\le c, &&\text{(16)}\\
a\le b&\Rightarrow a+c\le b+c, &&\text{(17)}\\
(a\le b\ \text{et}\ c\ge0)&\Rightarrow ac\le bc. &&\text{(18)}
\end{aligned}
\]
<ol class="mat101-statement-list">
<li>Résoudre dans \(\mathbb R\) l’inéquation \(3x+2\le-2x+1\), d’inconnue \(x\), en utilisant uniquement les règles ci-dessus pour les propriétés de l’ordre total. À chaque étape, indiquer la règle utilisée.</li>
<li>Montrer, en utilisant uniquement les règles (16) et (17), que
\[
(a\le b\ \text{et}\ c\le d)\Rightarrow a+c\le b+d.
\]</li>
<li>Montrer, en utilisant uniquement les règles (16), (17) et (18), que
\[
(a\le b\ \text{et}\ c\le0)\Rightarrow ac\ge bc.
\]</li>
<li>Montrer, en utilisant uniquement la règle (18), que
\[
(a&lt;b\ \text{et}\ c&gt;0)\Rightarrow ac&lt;bc.
\]</li>
</ol>
"""),
    "2.27": curated(r"""
<p>En utilisant un raisonnement direct, montrer que&nbsp;:</p>
<ol class="mat101-statement-list">
<li>si \(f:\mathbb R\to\mathbb R\) est dérivable et paire, alors sa dérivée \(f'\) est impaire&nbsp;;</li>
<li>pour tout \(x&gt;0\) dans \(\mathbb Q\), il existe un entier \(n&gt;0\) tel que \(n&gt;x\).</li>
</ol>
"""),
    "2.28": curated(r"""
<p>En utilisant un raisonnement par disjonction des cas, ou cas par cas&nbsp;:</p>
<ol class="mat101-statement-list">
<li>montrer
\[
\forall x\in\mathbb R,\quad (x\notin\mathbb Q)\lor(\exists n\in\mathbb N^*,\ nx\in\mathbb Z);
\]</li>
<li>soient \(a,b\) deux réels, montrer que
\[
\max(a,b)=\frac12(a+b+|a-b|),\qquad
\min(a,b)=\frac12(a+b-|a-b|);
\]</li>
<li>montrer que, quel que soit \(n\in\mathbb N\), \(3\) divise \(n(n+1)(2n+1)\)&nbsp;;</li>
<li>soit \(n\in\mathbb N\). Montrer qu’il existe \(m\in\mathbb N\) tel que \(n+m\) soit impair et \(nm\) soit pair&nbsp;;</li>
<li>trouver tous les réels \(x\) tels que \(|x+1|=3-|3x-2|\).</li>
</ol>
"""),
    "2.29": curated(r"""
<p>En utilisant un raisonnement par l’absurde, montrer que&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(\dfrac{\ln(2)}{\ln(3)}\) n’est pas rationnel&nbsp;;</li>
<li>si \(n\) est un entier naturel non nul et \(a_1,\ldots,a_n\) sont \(n\) nombres réels de somme \(1\), alors l’un de ces réels est inférieur ou égal à \(1/n\).</li>
</ol>
"""),
    "2.30": curated(r"""
<p>En utilisant un raisonnement par analyse et synthèse&nbsp;:</p>
<ol class="mat101-statement-list">
<li>soient \(a,b\) deux nombres réels. Démontrer que
\[
\forall x\in[0,1],\ ax+b\ge0
\quad\Longleftrightarrow\quad
(b\ge0\land a+b\ge0);
\]</li>
<li>soient \(D_1\) et \(D_2\) deux droites parallèles et distinctes du plan orienté. Soit \(A\) un point du plan n’appartenant ni à \(D_1\), ni à \(D_2\). Construire un triangle équilatéral \(ABC\) tel que \(B\in D_1\) et \(C\in D_2\). Combien y a-t-il de triangles possibles&nbsp;? On supposera qu’un tel triangle existe et on cherchera comment construire \(B\) ou \(C\) en utilisant la rotation de centre \(A\) et d’angle \(\pi/3\)&nbsp;;</li>
<li>montrer que toute fonction de \(\mathbb R\) dans \(\mathbb R\) est somme d’une fonction paire et d’une fonction impaire.</li>
</ol>
"""),
    "2.31": curated(r"""
<ol class="mat101-statement-list">
<li>Montrer par récurrence que tout entier supérieur ou égal à \(12\) peut s’écrire sous la forme \(4a+5b\), pour des entiers naturels \(a,b\).</li>
<li>On définit une suite \((u_n)_{n\in\mathbb N}\) par
\[
u_0=0,\qquad u_1=1,\qquad
\forall n\ge2,\quad u_{n+2}=5u_{n+1}-6u_n.
\]
Montrer par récurrence que, pour tout \(n\in\mathbb N\), \(u_n=3^n-2^n\).</li>
</ol>
"""),
    "2.32": curated(r"""
<p><em>Nombres de Fibonacci.</em> On définit les nombres de Fibonacci \((F_n)_{n\ge1}\) par</p>
\[
F_1=F_2=1,\qquad \forall n\ge1,\quad F_{n+2}=F_{n+1}+F_n.
\]
<ol class="mat101-statement-list">
<li>Calculer \(F_n\) pour \(1\le n\le10\).</li>
<li>Montrer que, pour tout \(n\ge1\), il y a exactement \(F_{n+1}\) façons de paver un échiquier de taille \(2\times n\) avec des dominos.</li>
<li>Démontrer
\[
\forall n\ge2,\ \forall m\ge1,\qquad
F_{n+m}=F_{n-1}F_m+F_nF_{m+1}.
\]
On pourra fixer \(n\ge2\) et raisonner par récurrence sur \(m\).</li>
<li>Démontrer
\[
\forall n\ge2,\qquad F_n^2=F_{n-1}F_{n+1}+(-1)^{n+1}.
\]</li>
</ol>
"""),
    "2.33": curated(r"""
<p>Déterminer l’ensemble des points du plan d’affixe \(z\) tels que</p>
\[
\frac{z^2}{z+i}
\]
<p>soit imaginaire pur.</p>
"""),
    "2.34": curated(r"""
<p><em>Une récurrence boiteuse.</em> La «&nbsp;preuve&nbsp;» suivante prétend montrer par récurrence sur \(n\ge1\) qu’étant donnés \(n\) nombres réels \(u_1,u_2,\ldots,u_n\), ils sont tous égaux.</p>
<p>Pour \(n\in\mathbb N^*\), on note \(P(n)\) l’assertion&nbsp;:</p>
<blockquote>Quels que soient \(u_1,\ldots,u_n\in\mathbb R\), on a \(u_1=u_2=\cdots=u_n\).</blockquote>
<p>Montrons \(\forall n\in\mathbb N^*,\ P(n)\) par récurrence.</p>
<p><strong>Initialisation.</strong> S’il n’y a qu’un nombre \(u_1\), il n’y a rien à montrer, ce qui prouve \(P(1)\).</p>
<p><strong>Hérédité.</strong> Soit \(n\ge1\) tel que \(P(n)\). Montrons \(P(n+1)\). Soient \(u_1,u_2,\ldots,u_n,u_{n+1}\in\mathbb R\). D’après \(P(n)\), on a déjà \(u_1=u_2=\cdots=u_n\). Par ailleurs, si l’on pose
\[
u'_1=u_2,\quad u'_2=u_3,\quad\ldots,\quad u'_n=u_{n+1}
\]
et que l’on applique \(P(n)\) à la famille \((u'_1,\ldots,u'_n)\), on obtient \(u'_1=\cdots=u'_n\), c’est-à-dire \(u_2=\cdots=u_n=u_{n+1}\). Cela entraîne \(u_1=u_2=\cdots=u_n=u_{n+1}\), et montre la propriété voulue.</p>
<p>Le résultat est évidemment faux. Où est le problème&nbsp;?</p>
"""),
    "2.35": curated(r"""
<p><em>Théorème de Helly en dimension \(1\).</em> Soit \(n\ge2\) un entier, et soient \(I_1,I_2,\ldots,I_n\) des intervalles de \(\mathbb R\). On considère l’assertion suivante&nbsp;:</p>
\[
\left(\forall i,j\in[\![1,n]\!],\ I_i\cap I_j\ne\varnothing\right)
\Longrightarrow
\left(\bigcap_{i\in[\![1,n]\!]}I_i\ \text{est un intervalle non vide de }\mathbb R\right).
\]
<p>Pour simplifier, on ne considère que des intervalles fermés.</p>
<ol class="mat101-statement-list">
<li>Faire un dessin pour \(n=3\) afin de se convaincre que l’assertion est vraie dans ce cas.</li>
<li>Montrer que l’assertion est fausse si l’on suppose seulement que \(I_1,\ldots,I_n\) sont des sous-ensembles de \(\mathbb R\), et pas nécessairement des intervalles.</li>
<li>En utilisant les notions de minimum et de maximum, donner une preuve directe de l’assertion.</li>
<li>Le théorème est-il encore vrai s’il y a une infinité d’intervalles&nbsp;?</li>
</ol>
"""),
    "3.1": curated(r"""
<p>On note \(\mathbb R\) l’ensemble des nombres réels. Parmi les ensembles suivants, dire lesquels sont les graphes d’une application d’un sous-ensemble de \(\mathbb R\) dans \(\mathbb R\). Lorsque l’ensemble est le graphe d’une application, donner son ensemble de départ.</p>
<ol class="mat101-statement-list">
<li>\(\{(x,y)\in\mathbb R^2\mid y-x+1=0\}\).</li>
<li>\(\{(x,y)\in\mathbb R^2\mid y=x^2\}\).</li>
<li>\(\{(x,y)\in\mathbb R^2\mid x=y^2\}\).</li>
<li>\(\{(x,y)\in\mathbb R^2\mid x=y^2\ \text{et}\ y\ge0\}\).</li>
</ol>
"""),
    "3.2": curated(r"""
<p>On note \(A=\{1,2,3\}\) et \(B=\{-1,0,1\}\). Écrire en extension les ensembles suivants&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(\{x+2\mid x\in A\}\).</li>
<li>\(\{2x\mid x\in B\}\).</li>
<li>\(\{1/x\mid x\in A\}\).</li>
<li>\(\{x+y\mid(x,y)\in A\times B\}\).</li>
<li>\(\{x+y\mid(x,y)\in A\times A\}\).</li>
<li>\(\{x+x\mid x\in A\}\).</li>
<li>\(\{xy\mid(x,y)\in A\times B\}\).</li>
</ol>
"""),
    "3.4": curated(r"""
<p>Soient \(I\) un intervalle non vide de \(\mathbb R\) et \(f:I\to\mathbb R\) une fonction à valeurs réelles. Exprimer à l’aide de quantificateurs les assertions suivantes.</p>
<ol class="mat101-statement-list">
<li>La fonction \(f\) s’annule.</li>
<li>La fonction \(f\) est la fonction nulle.</li>
<li>La fonction \(f\) n’est pas constante.</li>
<li>La fonction \(f\) ne prend jamais deux fois la même valeur.</li>
<li>La fonction \(f\) présente un minimum.</li>
<li>La fonction \(f\) prend des valeurs arbitrairement grandes.</li>
<li>La fonction \(f\) ne peut s’annuler qu’une seule fois.</li>
</ol>
"""),
    "3.5": curated(r"""
<p>Pour chacune des affirmations suivantes, décrire en termes simples les applications \(f:\mathbb R\to\mathbb R\) qui la vérifient.</p>
<ol class="mat101-statement-list">
<li>\(\exists x\in\mathbb R,\ \forall y\in\mathbb R,\ f(y)=f(x)\).</li>
<li>\(\forall x\in\mathbb R,\ \exists y\in\mathbb R,\ f(y)=f(x)\).</li>
<li>\(\exists x\in\mathbb R,\ \forall y\in\mathbb R,\ f(x)&lt;f(y)\).</li>
<li>\(\forall x\in\mathbb R,\ \exists y\in\mathbb R,\ f(x)&lt;f(y)\).</li>
<li>\(\forall x\in\mathbb R,\ x\le0\Rightarrow f(x)\le0\).</li>
<li>\(\forall x\in\mathbb R,\ f(x)\le0\Rightarrow x\le0\).</li>
<li>\(\forall x\in\mathbb R,\ x&gt;0\Rightarrow f(x)&gt;0\).</li>
<li>\(\forall x\in\mathbb R,\ x=0\Rightarrow f(x)=0\).</li>
<li>\(\forall x\in\mathbb R,\ f(x)=0\Rightarrow x=0\).</li>
<li>\(\forall x\in\mathbb R,\ f(x)\le0\ \text{ou}\ f(x)\ge0\).</li>
</ol>
"""),
    "3.6": curated(r"""
<p>Soient \(f\) et \(g\) les applications de \(\mathbb N\) dans \(\mathbb N\) définies par</p>
\[
\forall n\in\mathbb N,\qquad
f(n)=2n,\qquad
g(n)=
\begin{cases}
n/2,&\text{si }n\text{ est pair},\\
0,&\text{si }n\text{ est impair}.
\end{cases}
\]
<p>Déterminer \(g\circ f\), \(f\circ g\), \(g\circ g\) et \(g\circ g\circ g\).</p>
"""),
    "3.7": curated(r"""
<p>Soient \(E\) un ensemble et \(A\subset E\). On appelle <em>fonction indicatrice de \(A\)</em>, et on note \(\mathbf1_A\), l’application de \(E\) vers \(\{0,1\}\) qui, à \(x\in E\), associe \(1\) si \(x\in A\), et \(0\) si \(x\notin A\). Soient \(A,B\subset E\). Démontrer&nbsp;:</p>
<ol class="mat101-statement-list">
<li>\(\forall x\in E,\ \mathbf1_{A^c}(x)=1-\mathbf1_A(x)\).</li>
<li>\(\forall x\in E,\ \mathbf1_{A\cap B}(x)=\min\{\mathbf1_A(x),\mathbf1_B(x)\}=\mathbf1_A(x)\mathbf1_B(x)\).</li>
<li>\(\forall x\in E,\ \mathbf1_{A\cup B}(x)=\max\{\mathbf1_A(x),\mathbf1_B(x)\}=\mathbf1_A(x)+\mathbf1_B(x)-\mathbf1_A(x)\mathbf1_B(x)\).</li>
</ol>
"""),
    "3.8": curated(r"""
<p>Soient \(E,F\) deux ensembles, \(f:E\to F\), \(A,A'\subset E\) et \(B,B'\subset F\). Parmi les assertions suivantes, lesquelles sont toujours vraies&nbsp;?</p>
<ol class="mat101-statement-list">
<li>\(A\subset A'\Rightarrow f(A)\subset f(A')\).</li>
<li>\(B\subset B'\Rightarrow f^{-1}(B)\subset f^{-1}(B')\).</li>
<li>\(f(A\cup A')=f(A)\cup f(A')\).</li>
<li>\(f^{-1}(B\cup B')=f^{-1}(B)\cup f^{-1}(B')\).</li>
<li>\(f(A\cap A')=f(A)\cap f(A')\).</li>
<li>\(f^{-1}(B\cap B')=f^{-1}(B)\cap f^{-1}(B')\).</li>
<li>\(f^{-1}(f(A))=A\).</li>
<li>\(f(f^{-1}(B))=B\).</li>
<li>\(f(A\cap f^{-1}(B))=f(A)\cap B\).</li>
<li>\(f(A\cup f^{-1}(B))=f(A)\cup B\).</li>
</ol>
"""),
    "3.9": curated(r"""
<p>Soient \(A\subset\mathbb R\) et \(f:A\to\mathbb R\).</p>
<ol class="mat101-statement-list">
<li>Montrer que si \(f\) est strictement monotone, alors \(f\) est injective. La réciproque est-elle vraie&nbsp;?</li>
<li>On suppose que \(A=]-1,1[\cup]2,3[\), que \(f\) est dérivable sur \(A\) et que \(f'(x)&gt;0\) pour tout \(x\in A\). Peut-on en déduire que \(f\) est injective&nbsp;?</li>
</ol>
"""),
    "3.10": curated(r"""
<p>Soient \(E,F,G\) trois ensembles, \(f:E\to F\) et \(g:F\to G\).</p>
<ol class="mat101-statement-list">
<li>Montrer que \(g\circ f\) injective \(\Rightarrow f\) injective.</li>
<li>Montrer que \(g\circ f\) surjective \(\Rightarrow g\) surjective.</li>
<li>Que pensez-vous de \(g\circ f\) injective \(\Rightarrow g\) injective&nbsp;?</li>
</ol>
"""),
    "3.11": curated(r"""
<p>Soit \(f:E\to F\). Montrer que les assertions suivantes sont équivalentes&nbsp;:</p>
<ol class="mat101-statement-list" type="i">
<li>\(f\) est injective&nbsp;;</li>
<li>\(\forall A\subset E,\ f^{-1}(f(A))=A\).</li>
</ol>
"""),
    "3.12": curated(r"""
<p>Soient \(I\) un intervalle de \(\mathbb R\) et \(f:I\to\mathbb R\), continue sur \(I\).</p>
<ol class="mat101-statement-list">
<li>En utilisant le théorème des valeurs intermédiaires, montrer que \(f(I)\) est un intervalle.</li>
<li>On considère \(f:]-\infty,2]\to\mathbb R\), définie par \(f(x)=x^2-4x+3\). Montrer que \(f\) réalise une bijection de \(]-\infty,2]\) sur \([-1,+\infty[\).</li>
</ol>
"""),
    "3.13": curated(r"""
<p>Soit \(f:[0,1[\to]0,2]\) définie par</p>
\[
f(x)=
\begin{cases}
2x+1,&x\in[0,\tfrac12],\\
2x-1,&x\in]\tfrac12,1[.
\end{cases}
\]
<ol class="mat101-statement-list">
<li>L’application \(f\) est-elle injective&nbsp;?</li>
<li>L’application \(f\) est-elle surjective&nbsp;?</li>
<li>L’application \(f\) est-elle bijective&nbsp;?</li>
<li>Montrer que, pour tout \(x\in[0,1[\),
\[
f(x)\ge\frac32\quad\Longleftrightarrow\quad x\in\left[\frac14,\frac12\right].
\]</li>
</ol>
"""),
    "3.14": curated(r"""
<p>Soient \(a,b\in\mathbb C\). On définit \(f:\mathbb C\to\mathbb C\) par \(f(z)=az+b\).</p>
<ol class="mat101-statement-list">
<li>Montrer que \(f\) est bijective si et seulement si \(a\ne0\).</li>
<li>On suppose \(a\ne0\). Montrer que si \(ABC\) est un triangle équilatéral, alors \(f(A)f(B)f(C)\) est encore un triangle équilatéral.</li>
</ol>
"""),
    "3.15": curated(r"""
<p>Soit \(f:\mathbb C\to\mathbb C\) définie par \(f(z)=e^{i\pi/3}z+2\).</p>
<ol class="mat101-statement-list">
<li>On dit que \(z\) est un point fixe de \(f\) si \(f(z)=z\). Montrer que \(f\) admet un unique point fixe, noté \(a\).</li>
<li>Montrer que \(f(z)\) est l’image de \(z\) par la rotation de centre \(a\) et d’angle \(\pi/3\).</li>
</ol>
"""),
    "3.16": curated(r"""
<p>Soit \(f:\mathbb C\to\mathbb C\) définie par \(f(z)=e^{i\pi/3}\overline z+1\).</p>
<ol class="mat101-statement-list">
<li>Montrer que l’ensemble des points fixes de \(f\) est une droite, notée \(\Delta\).</li>
<li>Montrer que \(f(z)\) est l’image de \(z\) par la symétrie orthogonale d’axe \(\Delta\).</li>
</ol>
"""),
    "3.17": curated(r"""
<p>Soient \(a,b\in\mathbb C\). On pose \(f:\mathbb C\to\mathbb C\), \(f(z)=a\overline z+b\). Soient \(M,N,P,Q\) quatre points du plan tels que \(M\ne N\) et \(P\ne Q\). On note \(M'=f(M)\), \(N'=f(N)\), \(P'=f(P)\), \(Q'=f(Q)\). Montrer que \(f\) «&nbsp;renverse les angles&nbsp;», au sens suivant&nbsp;:</p>
\[
(\overrightarrow{M'N'},\overrightarrow{P'Q'})
=-(\overrightarrow{MN},\overrightarrow{PQ}).
\]
"""),
    "3.18": curated(r"""
<p>Calculer les nombres suivants.</p>
\[
\begin{gathered}
\sum_{k=1}^{3}\sum_{h=1}^{k}1,\qquad
\sum_{k=1}^{3}\sum_{h=1}^{k}h,\qquad
\sum_{k=1}^{3}\sum_{h=1}^{k}k,\\
\sum_{k=1}^{3}\prod_{h=1}^{k}h,\qquad
\sum_{k=1}^{3}\prod_{h=1}^{k}k,\qquad
\prod_{k=1}^{3}\sum_{h=1}^{k}h,\\
\prod_{k=1}^{3}\sum_{h=1}^{k}k,\qquad
\prod_{k=1}^{3}\prod_{h=1}^{k}h,\qquad
\prod_{k=1}^{3}\prod_{h=1}^{k}k.
\end{gathered}
\]
"""),
    "3.19": curated(r"""
<p>Soient \(a_1,a_2,a_3,a_4\) quatre variables. Écrire à l’aide des symboles \(\sum\) et \(\prod\) les quantités suivantes.</p>
<ol class="mat101-statement-list">
<li>\(a_1+a_2+a_3+a_4\).</li>
<li>\(a_1+a_1a_2+a_1a_2a_3+a_1a_2a_3a_4\).</li>
<li>\(a_1a_2+a_2a_3+a_3a_4\).</li>
<li>\(a_1a_2a_3+a_2a_3a_4\).</li>
<li>\(a_1a_2+a_1a_3+a_1a_4+a_2a_3+a_2a_4+a_3a_4\).</li>
<li>\(a_1(a_1+a_2)(a_1+a_2+a_3)(a_1+a_2+a_3+a_4)\).</li>
</ol>
"""),
    "3.20": curated(r"""
<p>Démontrer par récurrence les assertions suivantes.</p>
<ol class="mat101-statement-list">
<li>\(\displaystyle\forall n\in\mathbb N,\quad\sum_{k=0}^{n}(k+1)=\frac{(n+1)(n+2)}2\).</li>
<li>\(\displaystyle\forall n\in\mathbb N,\quad\sum_{k=0}^{n}k^2=\frac{n(n+1)(2n+1)}6\).</li>
<li>\(\displaystyle\forall n\in\mathbb N,\quad\sum_{k=0}^{n}k^3=\frac{n^2(n+1)^2}4\).</li>
<li>\(\displaystyle\forall n\in\mathbb N,\quad\sum_{k=0}^{n}2^k=2^{n+1}-1\).</li>
<li>\(\displaystyle\forall n\in\mathbb N,\quad\sum_{k=0}^{n}k2^k=(n-1)2^{n+1}+2\).</li>
<li>\(\displaystyle\forall n\in\mathbb N,\ n\ge3,\quad\prod_{k=3}^{n}\frac{k^2-4}{k}=\frac{(n+2)!}{12n(n-1)}\).</li>
<li>\(\displaystyle\forall n\in\mathbb N^*,\quad\prod_{k=1}^{n}(n+k)=2^n\prod_{k=1}^{n}(2k-1)\).</li>
</ol>
"""),
    "3.21": curated(r"""
<p>Soient \(p,q\) deux entiers naturels non nuls et</p>
\[
\begin{aligned}
f:\{1,\ldots,p\}\times\{1,\ldots,q\}&\longrightarrow\{1,\ldots,pq\},\\
(i,j)&\longmapsto j+(i-1)q.
\end{aligned}
\]
<ol class="mat101-statement-list">
<li>Montrer que \(f\) est bien définie, c’est-à-dire que ses images sont dans \(\{1,\ldots,pq\}\), et que c’est une bijection.</li>
<li>Cette bijection correspond à énumérer les cases d’un tableau à \(p\) lignes et \(q\) colonnes de gauche à droite, ligne par ligne, en partant de la première ligne. Donner une bijection correspondant à l’énumération du même tableau de haut en bas, colonne par colonne, en partant de la première colonne.</li>
</ol>
"""),
    "3.22": curated(r"""
<p>Soit \(n\in\mathbb N^*\). On note \(\mathcal A_{n,2}\) l’ensemble des couples de deux éléments distincts de \(\{1,\ldots,n\}\). Pour \(a\in\{1,\ldots,n\}\), on note \(E_a\) l’ensemble des couples de \(\mathcal A_{n,2}\) dont la première coordonnée est \(a\).</p>
<ol class="mat101-statement-list">
<li>Quel est le cardinal de \(E_a\)&nbsp;?</li>
<li>Montrer que si \(a\ne a'\), alors \(E_a\cap E_{a'}=\varnothing\).</li>
<li>Montrer que
\[
\mathcal A_{n,2}=\bigsqcup_{a\in\{1,\ldots,n\}}E_a
\]
et représenter cette relation par un arbre de dénombrement.</li>
<li>En déduire que \(|\mathcal A_{n,2}|=n(n-1)\).</li>
<li>Montrer que \(\mathcal A_{n,2}\) est en bijection avec l’ensemble des applications injectives de \(\{1,2\}\) dans \(\{1,\ldots,n\}\).</li>
</ol>
"""),
    "3.23": curated(r"""
<p>Une entreprise veut se donner un nouveau sigle formé d’exactement trois lettres. De combien de façons peut-elle le faire&nbsp;? Combien reste-t-il de possibilités si l’on impose au sigle d’être formé de lettres distinctes&nbsp;?</p>
"""),
    "3.24": curated(r"""
<p>On met dans une boîte \(26\) jetons de Scrabble, portant chacun l’une des \(26\) lettres de l’alphabet&nbsp;: deux jetons distincts portent donc deux lettres distinctes. On en tire \(3\) à la fois. Combien de tirages différents peut-on obtenir&nbsp;?</p>
"""),
    "3.25": curated(r"""
<ol class="mat101-statement-list">
<li>Combien y a-t-il de nombres entre \(1\) et \(100\) qui ne sont divisibles ni par \(5\), ni par \(7\)&nbsp;?</li>
<li>Combien y a-t-il de nombres entre \(1\) et \(3000\) qui ne sont divisibles ni par \(3\), ni par \(5\)&nbsp;?</li>
</ol>
"""),
    "3.26": curated(r"""
<p>Démontrer les égalités suivantes en utilisant des manipulations et des identités algébriques, sans utiliser de récurrence.</p>
<ol class="mat101-statement-list">
<li>\(\displaystyle\prod_{k=1}^{n}(2k)=2^n n!,\quad\forall n\ge1\).</li>
<li>\(\displaystyle\prod_{k=1}^{n-1}(2k+1)=\frac{(2n)!}{2^n n!},\quad\forall n\ge2\).</li>
<li>\(\displaystyle\prod_{k=1}^{n}\frac{2k+1}{2k-1}=2n+1,\quad\forall n\ge1\).</li>
<li>\(\displaystyle\prod_{k=2}^{n}\frac{k^2-1}{k}=\frac{(n+1)!}{2n},\quad\forall n\ge2\).</li>
<li>\(\displaystyle\sum_{k=0}^{n}(n-k)=\frac{n(n+1)}2,\quad\forall n\in\mathbb N\).</li>
<li>\(\displaystyle\sum_{k=0}^{n}(k+1)=\frac{(n+1)(n+2)}2,\quad\forall n\in\mathbb N\).</li>
<li>\(\displaystyle\sum_{k=0}^{n}(2k+1)=(n+1)^2,\quad\forall n\in\mathbb N\).</li>
<li>\(\displaystyle\sum_{k=1}^{n-1}2^k=2^n-2,\quad\forall n\ge2\).</li>
<li>\(\displaystyle\sum_{k=0}^{2n-1}2^{k/2}=\frac{2^n-1}{\sqrt2-1},\quad\forall n\in\mathbb N^*\).</li>
<li>\(\displaystyle\sum_{k=0}^{2n}2^{2k-1}=\frac{4^{2n+1}-1}{6},\quad\forall n\in\mathbb N\).</li>
<li>\(\displaystyle\sum_{k=0}^{n}2^k3^{n-k}=3^{n+1}-2^{n+1},\quad\forall n\in\mathbb N\).</li>
<li>\(\displaystyle\sum_{k=0}^{n}(-1)^k2^{n-k}=\frac{2^{n+1}-(-1)^{n+1}}3\).</li>
</ol>
"""),
    "3.27": curated(r"""
<p>Démontrer, pour tout entier naturel \(n\), les égalités suivantes.</p>
<ol class="mat101-statement-list">
<li>\(\displaystyle\sum_{k=0}^{n}\binom nk=2^n\).</li>
<li>\(\displaystyle\sum_{k=0}^{n}(-1)^k\binom nk=0\).</li>
<li>\(\displaystyle\sum_{k=0}^{n}\binom{2n}{2k}=2^{2n-1}\). Ajouter les deux égalités précédentes.</li>
<li>\(\displaystyle\sum_{k=0}^{n}2^k\binom nk=3^n\).</li>
<li>\(\displaystyle\sum_{k=0}^{n}2^{3k-1}\binom nk=\frac{9^n}{2}\).</li>
<li>\(\displaystyle\sum_{k=0}^{n}2^{3k}3^{n-2k}\binom nk=\left(\frac{17}{3}\right)^n\).</li>
<li>\(\displaystyle\sum_{k=0}^{n}i^k\binom nk=2^{n/2}e^{ni\pi/4}\).</li>
<li>\(\displaystyle\sum_{k=0}^{n}3^{k/2}i^k\binom nk=2^ne^{ni\pi/3}\).</li>
</ol>
"""),
    "3.28": curated(r"""
<p>Soit \(n\in\mathbb N\) et \(f(x)=(1+x)^n\).</p>
<ol class="mat101-statement-list">
<li>En utilisant une formule du cours, écrire \(f(x)\) comme une somme faisant intervenir les puissances de \(x\).</li>
<li>La dérivée de \(f\) est \(f'(x)=n(1+x)^{n-1}\). L’intégrale de \(f\) sur \([0,1]\) vaut
\[
\int_0^1f(x)\,dx
=\left[\frac{(1+x)^{n+1}}{n+1}\right]_0^1
=\frac{2^{n+1}-1}{n+1}.
\]
En utilisant la question 1, donner une autre expression de \(f'(x)\) et de cette intégrale.</li>
<li>En déduire les valeurs de
\[
\sum_{k=0}^{n}\binom nk,\qquad
\sum_{k=0}^{n}k\binom nk,\qquad
\sum_{k=0}^{n}\frac1{k+1}\binom nk.
\]</li>
</ol>
"""),
    "3.29": curated(r"""
<p>Soient \(n,p\) deux entiers naturels. Cet exercice présente, dans le cas particulier \(p=2\), une méthode générale pour calculer \(\sum_{k=0}^{n}k^p\).</p>
<ol class="mat101-statement-list">
<li>Soit \(x\mapsto P(x)\) une fonction. Donner une expression plus simple de
\[
\sum_{k=0}^{n}\bigl(P(k+1)-P(k)\bigr).
\]</li>
<li>Soient \(a,b,c\) des réels et \(P(x)=ax^3+bx^2+cx\). Calculer \(P(x+1)-P(x)\).</li>
<li>Déterminer \(a,b,c\) de sorte que \(P(x+1)-P(x)=x^2\).</li>
<li>En déduire que
\[
\sum_{k=0}^{n}k^2=\frac{n(n+1)(2n+1)}6.
\]</li>
</ol>
"""),
    "3.30": curated(r"""
<p>Le but de l’exercice est de calculer, pour tout entier positif \(n\), la somme</p>
\[
\sum_{k=0}^{n}\binom{3n}{3k}.
\]
<ol class="mat101-statement-list">
<li>Calculer cette somme pour \(n=0,1,2,3\).</li>
<li>Utiliser la formule du binôme pour développer \((1+1)^n\) et en déduire
\[
\sum_{k=0}^{n}\binom nk=2^n.
\]</li>
<li>Pour tout entier \(n\), on note
\[
\begin{aligned}
T_0(n)&=\sum_{k=0}^{n}\binom{3n}{3k},\\
T_1(n)&=\sum_{k=0}^{n-1}\binom{3n}{3k+1},\\
T_2(n)&=\sum_{k=0}^{n-1}\binom{3n}{3k+2}.
\end{aligned}
\]
Que vaut \(T_0(n)+T_1(n)+T_2(n)\)&nbsp;?</li>
<li>On désigne par \(j\) le nombre complexe
\[
j=e^{2i\pi/3}=\frac{-1+i\sqrt3}{2}.
\]
Montrer que \(1+j+j^2=0\).</li>
<li>Démontrer
\[
(j+1)^{3n}=T_0(n)+jT_1(n)+j^2T_2(n)
\]
et
\[
(j^2+1)^{3n}=T_0(n)+j^2T_1(n)+jT_2(n).
\]</li>
<li>En déduire
\[
3T_0(n)=2^{3n}+(j+1)^{3n}+(j^2+1)^{3n}.
\]</li>
<li>Montrer que \(j+1=e^{i\pi/3}\) et \(j^2+1=e^{-i\pi/3}\), puis en déduire
\[
T_0(n)=\frac{2^{3n}+2(-1)^n}{3}.
\]</li>
</ol>
"""),
    "3.31": curated(r"""
<p><em>Construction de \(\mathbb Q\) à partir de \(\mathbb Z\).</em> Quand on définit les nombres rationnels à partir des entiers relatifs, on précise que si \((p,q),(p',q')\in\mathbb Z\times\mathbb N^*\), alors</p>
\[
\frac pq=\frac{p'}{q'}\Longleftrightarrow pq'=p'q, \tag{26}
\]
\[
\frac pq+\frac{p'}{q'}=\frac{pq'+p'q}{qq'}. \tag{27}
\]
\[
\frac pq\times\frac{p'}{q'}=\frac{pp'}{qq'}. \tag{28}
\]
<p>Cette manière de procéder demande de vérifier que l’égalité de fractions définie par (26) est compatible avec l’addition (27) et la multiplication (28). Dans la suite, \((s,t),(s',t')\in\mathbb Z\times\mathbb N^*\).</p>
<ol class="mat101-statement-list">
<li>Montrer que si \(\frac pq=\frac{p'}{q'}\) et \(\frac st=\frac{s'}{t'}\), alors
\[
\frac pq+\frac st=\frac{p'}{q'}+\frac{s'}{t'}
\quad\text{et}\quad
\frac pq\times\frac st=\frac{p'}{q'}\times\frac{s'}{t'}.
\]</li>
</ol>
<p>De manière plus abstraite, soit \(E\) un ensemble et \(\mathcal R\subset E\times E\). On dit que \(\mathcal R\) est une relation d’équivalence sur \(E\) si</p>
\[
\begin{aligned}
&\forall x\in E,\ (x,x)\in\mathcal R,\\
&\forall(x,y)\in E^2,\ (x,y)\in\mathcal R\Rightarrow(y,x)\in\mathcal R,\\
&\forall(x,y,z)\in E^3,\ ((x,y)\in\mathcal R\land(y,z)\in\mathcal R)
\Rightarrow(x,z)\in\mathcal R.
\end{aligned}
\]
<p>On note
\[
C_{\mathcal R}(x)=\{y\in E\mid(x,y)\in\mathcal R\},
\qquad
E/\mathcal R=\{C_{\mathcal R}(x)\mid x\in E\}.
\]</p>
<ol class="mat101-statement-list" start="2">
<li>Montrer que si \(\mathcal R\) est une relation d’équivalence sur \(E\), alors \(x\in C_{\mathcal R}(x)\).</li>
<li>Si \(E=\mathbb Z\times\mathbb N^*\) et
\[
\mathcal R=\{((p,q),(p',q'))\mid pq'=p'q\},
\]
montrer que \(\mathcal R\) est une relation d’équivalence sur \(E\).</li>
<li>Soit \(f:E\times E\to E\). On suppose que
\[
(x,x')\in\mathcal R\ \text{et}\ (y,y')\in\mathcal R
\Rightarrow f(x,y)=f(x',y'). \tag{29}
\]
Montrer que \(f(C_{\mathcal R}(x)\times C_{\mathcal R}(x'))\) est un singleton. On peut alors définir \(\overline f:(E/\mathcal R)^2\to E/\mathcal R\) par \(\overline f(C,C')=C_{\mathcal R}(y)\), où \(f(C\times C')=\{y\}\).</li>
<li>Avec \(E,\mathcal R\) définis comme à la question 3, montrer que
\[
f((p,q),(p',q'))=(pq'+p'q,qq')
\]
vérifie (29).</li>
<li>Vérifier la même propriété pour
\[
g((p,q),(p',q'))=(pp',qq').
\]</li>
</ol>
<p>On peut alors définir \(\mathbb Q\) comme \(\mathbb Z\times\mathbb N^*\) modulo \(\mathcal R\), muni des opérations \(\overline f\) et \(\overline g\), et vérifier les propriétés usuelles attendues.</p>
"""),
    "4.1": curated(r"""
<p>Dans chacun des cas suivants, dire si l’on a bien une approximation avec la marge indiquée, ou sinon la corriger.</p>
<ol class="mat101-statement-list">
<li>\(3{,}14\) est une approximation de \(\pi\) à \(0{,}01\) près.</li>
<li>\(3{,}1416\) est une approximation de \(\pi\) à \(0{,}001\) près.</li>
<li>\(3{,}1416\) est une approximation de \(\pi\) à \(10^{-5}\) près.</li>
<li>\(1{,}41\) est une approximation de \(\sqrt2\) à \(10^{-3}\) près.</li>
<li>\(2{,}72\) est une approximation de \(e\) à \(10^{-2}\) près.</li>
</ol>
"""),
    "4.2": curated(r"""
<p>Soit \(x\) un réel strictement positif.</p>
<ol class="mat101-statement-list">
<li>Montrer que
\[
x&gt;10\Rightarrow\left|\frac{2\sin x}{x}\right|\le\frac15.
\]</li>
<li>La réciproque est-elle vraie&nbsp;?</li>
</ol>
"""),
    "4.3": curated(r"""
<p>Soient \(a,b\in[1,+\infty[\).</p>
<ol class="mat101-statement-list">
<li>Montrer que
\[
a\ge b\Rightarrow
1-\frac1b\le1+\frac1a-\frac1{a^2}\le1+\frac1b.
\]</li>
<li>La réciproque est-elle vraie&nbsp;?</li>
</ol>
"""),
    "4.4": curated(r"""
<p>Soit \(a\in[0,\tfrac12]\). Montrer que</p>
\[
|b|\le\frac a2\Rightarrow
\frac a3\le\frac{a+b}{1+a}\le\frac{3a}{2}.
\]
"""),
    "4.5": curated(r"""
<p>Soit \(c\ge1\).</p>
<ol class="mat101-statement-list">
<li>Montrer que si \(0\le y\le1-\frac1c\), alors
\[
\frac1{1-y}\le1+cy.
\]</li>
<li>Soit \(b&gt;10\). Montrer que
\[
a\ge b\Rightarrow
a\le\frac{a^2+a+1}{a-5}\le a\left(1+\frac{13}{b}\right).
\]</li>
<li>Lorsqu’on approche un réel \(A\) par un réel \(B\), on appelle <em>erreur relative</em> la quantité \(|B-A|/|A|\). Montrer que si \(a\ge13\cdot10^k\), avec \(k\in\mathbb N\), alors on peut approcher
\[
\frac{a^2+a+1}{a-5}
\]
par \(a\) avec une erreur relative inférieure ou égale à \(10^{-k}\).</li>
</ol>
"""),
    "4.6": curated(r"""
<p>Pour tous \(i,j\in\mathbb N^*\), on note \(P(i,j)\) l’assertion «&nbsp;\(j\) est un multiple de \(i\)&nbsp;».</p>
<ol class="mat101-statement-list">
<li>Pour visualiser les choses, représenter \(P\) sous la forme d’un tableau de vrai (V) et de faux (F) ayant une infinité de lignes et de colonnes.</li>
<li>Les assertions suivantes sont-elles vraies&nbsp;?
<ol class="mat101-statement-sublist" type="a">
<li>\(\forall i\in\mathbb N^*,\ \exists J\in\mathbb N^*,\ \forall j\in\mathbb N^*,\ j\ge J\Rightarrow P(i,j)\)&nbsp;;</li>
<li>\(\forall i\in\mathbb N^*,\ \forall J\in\mathbb N^*,\ \exists j\in\mathbb N^*\ \text{tel que}\ j\ge J\ \text{et}\ P(i,j)\).</li>
</ol></li>
</ol>
"""),
    "4.7": curated(r"""
<p>Pour tous \(i,j\in\mathbb N^*\), on note \(P(i,j)\) l’assertion</p>
\[
\frac1{j^2}\le\frac1i.
\]
<ol class="mat101-statement-list">
<li>Représenter \(P\) sous la forme d’un tableau de vrai (V) et de faux (F) ayant une infinité de lignes et de colonnes.</li>
<li>Les assertions suivantes sont-elles vraies&nbsp;? Justifier la réponse.
<ol class="mat101-statement-sublist" type="a">
<li>\(\forall i\in\mathbb N^*,\ \exists J\in\mathbb N^*,\ \forall j\in\mathbb N^*,\ j\ge J\Rightarrow P(i,j)\)&nbsp;;</li>
<li>\(\forall i\in\mathbb N^*,\ \forall J\in\mathbb N^*,\ \exists j\in\mathbb N^*\ \text{tel que}\ j\ge J\ \text{et}\ P(i,j)\).</li>
</ol></li>
</ol>
"""),
    "4.8": curated(r"""
<p>Soit \(u\) une suite de nombres entiers dont toutes les valeurs sont dans \(\{0,1,2\}\). Pour tout \(j\ge3\) et tout \(i\ge1\), on note \(P(i,j)\) l’assertion</p>
\[
\left|\frac1{j-u_j}\right|\le\frac1i.
\]
<ol class="mat101-statement-list">
<li>Représenter \(P\) sous la forme d’un tableau de vrai (V) et de faux (F) ayant une infinité de lignes et de colonnes. Si l’on ne peut mettre vrai ou faux avec certitude, mettre un point d’interrogation.</li>
<li>Les assertions suivantes sont-elles vraies&nbsp;? Justifier la réponse.
<ol class="mat101-statement-sublist" type="a">
<li>\(\forall i\in\mathbb N^*,\ \exists J\in\mathbb N^*,\ \forall j\in\mathbb N^*\cap[3,+\infty[,\ j\ge J\Rightarrow P(i,j)\)&nbsp;;</li>
<li>\(\forall i\in\mathbb N^*,\ \forall J\in\mathbb N^*,\ \exists j\in\mathbb N^*\cap[3,+\infty[\ \text{tel que}\ j\ge J\ \text{et}\ P(i,j)\)&nbsp;;</li>
<li>La suite \(j\mapsto\dfrac1{j-u_j}\) admet-elle une limite&nbsp;? Si oui, que vaut-elle&nbsp;?</li>
</ol></li>
</ol>
"""),
    "4.9": curated(r"""
<p>Écrire le plus simplement possible les ensembles suivants. Justifier rigoureusement, en montrant séparément deux inclusions.</p>
<ol class="mat101-statement-list">
<li>\(\displaystyle\bigcup_{x\in\mathbb R}\{x^2\}\).</li>
<li>\(\displaystyle\bigcup_{x\in[0,1]}]x-1,x+1[\).</li>
<li>\(\displaystyle\bigcap_{x\in[0,1]}]x-1,x+1[\).</li>
<li>\(\displaystyle\bigcap_{x\in[0,1]}[x-1,x+1]\).</li>
<li>\(\displaystyle\bigcap_{n\in\mathbb N^*}\left[0,\frac1n\right]\).</li>
<li>\(\displaystyle\bigcup_{n\in\mathbb N^*}\left[\frac1{n+1},\frac1n\right]\).</li>
</ol>
"""),
    "4.10": curated(r"""
<p>Pour chacune des suites suivantes, trouver deux entiers \(N_{10}\) et \(N_{100}\) tels que</p>
\[
\forall n\ge N_{10},\ |u_n|&lt;\frac1{10},
\qquad
\forall n\ge N_{100},\ |u_n|&lt;\frac1{100}.
\]
<ol class="mat101-statement-list">
<li>\(u_n=\dfrac1n\).</li>
<li>\(u_n=\dfrac1{n^2}\).</li>
<li>\(u_n=\dfrac{(-1)^n}{n^2}\).</li>
<li>\(u_n=2^{-n}\).</li>
<li>\(u_n=10^{-n}\).</li>
<li>\(\displaystyle u_n=\begin{cases}1/n,&n\text{ pair},\\1/n^2,&n\text{ impair}.\end{cases}\)</li>
<li>\(\displaystyle u_n=\begin{cases}2^{-n},&n\text{ pair},\\3^{-n},&n\text{ impair}.\end{cases}\)</li>
<li>\(u_n=\dfrac{\cos n}{3^n}\).</li>
</ol>
"""),
    "4.11": curated(r"""
<p>Pour chacune des suites suivantes et pour tout réel \(\varepsilon&gt;0\), trouver un entier \(N_\varepsilon\) tel que</p>
\[
\forall n\ge N_\varepsilon,\qquad |u_n|&lt;\varepsilon.
\]
<ol class="mat101-statement-list">
<li>\(u_n=\dfrac1n\).</li>
<li>\(u_n=\dfrac1{n^2}\).</li>
<li>\(u_n=\dfrac{(-1)^n}{n^2}\).</li>
<li>\(u_n=2^{-n}\).</li>
<li>\(u_n=10^{-n}\).</li>
<li>\(\displaystyle u_n=\begin{cases}1/n,&n\text{ pair},\\1/n^2,&n\text{ impair}.\end{cases}\)</li>
<li>\(\displaystyle u_n=\begin{cases}2^{-n},&n\text{ pair},\\3^{-n},&n\text{ impair}.\end{cases}\)</li>
<li>\(u_n=\dfrac{\cos n}{3^n}\).</li>
</ol>
"""),
    "4.12": curated(r"""
<p>La phrase suivante est-elle vraie ou fausse&nbsp;? Justifier.</p>
<blockquote>Si une suite de nombres réels est périodique, alors elle est bornée.</blockquote>
"""),
    "4.13": curated(r"""
<p>Pour chacune des suites suivantes, dire si elle est périodique, majorée, minorée, bornée, convergente, si elle tend vers \(\pm\infty\), ou si elle diverge. Démontrer toutes les réponses. Si elle converge, déterminer sa limite.</p>
<ol class="mat101-statement-list">
<li>\(u_n=(-1)^n\).</li>
<li>\(u_n=\dfrac1n\).</li>
<li>\(u_n=\dfrac1{n^2}\).</li>
<li>\(u_n=\dfrac{n}{n+1}\).</li>
<li>\(u_n=(-1)^n+\dfrac1n\).</li>
<li>\(u_n=\cos n\).</li>
<li>\(u_n=2^{-n}\).</li>
<li>\(u_n=n+(-1)^n\).</li>
<li>\(u_n=n+(-1)^n n\).</li>
<li>\(u_n=\dfrac{n+1}{n^2}\).</li>
<li>\(u_n=\dfrac{2n^2+n+3}{n^2}\).</li>
</ol>
"""),
    "4.14": curated(r"""
<p>Soit \((u_n)_{n\in\mathbb N}\) une suite à valeurs entières. Montrer que si \((u_n)\) converge, alors elle est constante à partir d’un certain rang, ce que l’on peut traduire par</p>
\[
\exists n_0\in\mathbb N,\quad\forall n\ge n_0,\quad u_n=u_{n_0}.
\]
"""),
    "4.15": curated(r"""
<p><em>Le nombre d’or.</em></p>
<ol class="mat101-statement-list">
<li>Résoudre dans \(\mathbb R\) l’équation \(x^2-x-1=0\). La solution positive, notée \(\phi\), est appelée «&nbsp;nombre d’or&nbsp;».</li>
<li>Démontrer que \(\phi=1+\dfrac1\phi\).</li>
</ol>
<p>On définit une suite \((u_n)_{n\in\mathbb N}\) par \(u_0=2\) et, pour tout \(n\in\mathbb N^*\),</p>
\[
u_{n+1}=1+\frac1{u_n}.
\]
<ol class="mat101-statement-list" start="3">
<li>Montrer que, pour tout \(n\in\mathbb N^*\), \(\dfrac32\le u_n\le2\).</li>
<li>Montrer que, pour tout \(n\in\mathbb N^*\),
\[
|u_{n+1}-\phi|\le\frac49|u_n-\phi|.
\]
Utiliser la question 2.</li>
<li>En déduire par récurrence que, pour tout \(n\in\mathbb N^*\),
\[
|u_n-\phi|\le\left(\frac49\right)^n.
\]</li>
<li>Prouver que \((u_n)\) converge et déterminer sa limite.</li>
<li>Déterminer un entier \(n\) tel que \(u_n\) soit une approximation de \(\phi\) à \(10^{-6}\) près.</li>
</ol>
"""),
    "4.16": curated(r"""
<p><em>Racines carrées, méthode égyptienne.</em> On présente un algorithme pour obtenir des approximations de racines carrées. Soit \(a&gt;1\) un réel dont on cherche à déterminer la racine carrée. On suppose que l’on sait déterminer \(\lfloor\sqrt a\rfloor\). On définit une suite \((u_n)\) par</p>
\[
u_0=\lfloor\sqrt a\rfloor+1,
\qquad
u_{n+1}=\frac{u_n+a/u_n}{2}.
\]
<ol class="mat101-statement-list">
<li>Montrer par récurrence que \((u_n)\) est décroissante et que \(u_n&gt;\sqrt a\) pour tout \(n\in\mathbb N\).</li>
<li>Montrer que
\[
|u_{n+1}-\sqrt a|\le\frac{|u_n-\sqrt a|^2}{2\sqrt a}.
\]</li>
<li>En déduire que \(u_n\) tend vers \(\sqrt a\).</li>
<li>Déterminer un entier \(n\) tel que \(u_n\) soit une approximation de \(\sqrt a\) à \(10^{-6}\) près.</li>
</ol>
"""),
    "4.17": curated(r"""
<p>Soit \(u_0\) un entier positif quelconque. On considère la suite \((u_n)_{n\in\mathbb N}\) définie par</p>
\[
u_{n+1}=
\begin{cases}
u_n+1,&\text{si }n\text{ est impair},\\
u_n/2,&\text{si }n\text{ est pair}.
\end{cases}
\]
<ol class="mat101-statement-list">
<li>La suite \((u_n)\) est-elle croissante&nbsp;? Décroissante&nbsp;?</li>
<li>Montrer que, pour toute valeur initiale \(u_0\in\mathbb N^*\),
\[
\exists N\in\mathbb N,\qquad u_N=1.
\]</li>
</ol>
<p>Si l’on remplace \(u_n+1\) par \(3u_n+1\) dans la définition, savoir si cette assertion reste vraie est un problème ouvert appelé <em>problème de Syracuse</em>.</p>
"""),
}
