#!/usr/bin/env python3
"""Build _data/mat101_demonstrations.json for the MAT101 demonstrations page."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_data/mat101_demonstrations.json"


def m_inline(tex: str) -> str:
    return f'<span class="math inline">\\({tex}\\)</span>'


def m_display(tex: str) -> str:
    return f'<span class="math display">\\[{tex}\\]</span>'


def p(*parts: str) -> str:
    return "".join(parts)


DEMONSTRATIONS = {
    "chapters": [
        {
            "id": "complexes",
            "number": "1",
            "title": "Nombres complexes",
            "demonstrations": [
                {
                    "id": "1.3",
                    "kind": "proposition",
                    "label": "Proposition 1.3",
                    "subtitle": "Conjugué de la somme et du produit, module du produit",
                    "statementHtml": p(
                        "<p>Soient ",
                        m_inline("z_1"),
                        " et ",
                        m_inline("z_2"),
                        " deux nombres complexes. Alors&nbsp;:</p>",
                        "<ol>",
                        "<li>",
                        m_inline("\\overline{z_1+z_2}=\\overline{z_1}+\\overline{z_2}"),
                        "</li>",
                        "<li>",
                        m_inline("\\overline{z_1 z_2}=\\overline{z_1}\\,\\overline{z_2}"),
                        "</li>",
                        "<li>",
                        m_inline("|z_1 z_2|=|z_1|\\,|z_2|"),
                        "</li>",
                        "</ol>",
                    ),
                    "proofHtml": p(
                        "<p>On écrit ",
                        m_inline("z_1=a_1+\\mathrm ib_1"),
                        " et ",
                        m_inline("z_2=a_2+\\mathrm ib_2"),
                        " avec ",
                        m_inline("a_1,a_2,b_1,b_2\\in\\mathbb R"),
                        ".</p>",
                        "<ol>",
                        "<li><p>On a ",
                        m_display(
                            "\\overline{z_1+z_2}"
                            "=\\overline{(a_1+a_2)+\\mathrm i(b_1+b_2)}"
                            "=(a_1+a_2)-\\mathrm i(b_1+b_2)"
                            "=(a_1-\\mathrm ib_1)+(a_2-\\mathrm ib_2)"
                            "=\\overline{z_1}+\\overline{z_2}."
                        ),
                        "</p></li>",
                        "<li><p>On calcule ",
                        m_display(
                            "z_1 z_2=(a_1+\\mathrm ib_1)(a_2+\\mathrm ib_2)"
                            "=a_1a_2-b_1b_2+\\mathrm i(a_1b_2+a_2b_1)."
                        ),
                        " Donc ",
                        m_display(
                            "\\overline{z_1 z_2}=a_1a_2-b_1b_2-\\mathrm i(a_1b_2+a_2b_1)."
                        ),
                        " D’autre part ",
                        m_display(
                            "\\overline{z_1}\\,\\overline{z_2}"
                            "=(a_1-\\mathrm ib_1)(a_2-\\mathrm ib_2)"
                            "=a_1a_2-b_1b_2-\\mathrm i(a_1b_2+a_2b_1)."
                        ),
                        " Ainsi ",
                        m_inline("\\overline{z_1 z_2}=\\overline{z_1}\\,\\overline{z_2}"),
                        ".</p></li>",
                        "<li><p>On obtient ",
                        m_display(
                            "|z_1 z_2|^2=(a_1a_2-b_1b_2)^2+(a_1b_2+a_2b_1)^2"
                            "=a_1^2a_2^2+b_1^2a_2^2+a_1^2b_2^2+b_1^2b_2^2."
                        ),
                        " Et ",
                        m_display(
                            "(|z_1|\\,|z_2|)^2=(a_1^2+b_1^2)(a_2^2+b_2^2)"
                            "=a_1^2a_2^2+b_1^2a_2^2+a_1^2b_2^2+b_1^2b_2^2."
                        ),
                        " Les deux carrés sont égaux et les modules sont positifs ou nuls, donc ",
                        m_inline("|z_1 z_2|=|z_1|\\,|z_2|"),
                        ".</p></li>",
                        "</ol>",
                    ),
                },
                {
                    "id": "1.14",
                    "kind": "theorem",
                    "label": "Théorème 1.14",
                    "subtitle": "Racines des polynômes de degré 2",
                    "statementHtml": p(
                        "<p>Soient ",
                        m_inline("a,b,c\\in\\mathbb C"),
                        " avec ",
                        m_inline("a\\neq0"),
                        ". Notons ",
                        m_inline("\\delta"),
                        " un nombre complexe tel que ",
                        m_inline("\\delta^2=b^2-4ac"),
                        ". Alors le polynôme ",
                        m_inline("az^2+bz+c"),
                        " admet pour racines ",
                        m_display(
                            "z_1=\\frac{-b+\\delta}{2a}"
                            "\\qquad\\text{et}\\qquad "
                            "z_2=\\frac{-b-\\delta}{2a},"
                        ),
                        " et se factorise sous la forme ",
                        m_inline("az^2+bz+c=a(z-z_1)(z-z_2)"),
                        ". Le discriminant est ",
                        m_inline("\\Delta=b^2-4ac"),
                        ".</p>",
                    ),
                    "proofHtml": p(
                        "<p>Pour tout ",
                        m_inline("z\\in\\mathbb C"),
                        ", on complète le carré&nbsp;:</p>",
                        m_display(
                            "\\begin{aligned}"
                            "az^2+bz+c"
                            "&=a\\left(z^2+\\frac{b}{a}z+\\frac{c}{a}\\right)\\\\"
                            "&=a\\left(\\left(z+\\frac{b}{2a}\\right)^2-\\frac{\\Delta}{4a^2}\\right)\\\\"
                            "&=a\\left(\\left(z+\\frac{b}{2a}\\right)^2-\\left(\\frac{\\delta}{2a}\\right)^2\\right)\\\\"
                            "&=a\\left(z+\\frac{b}{2a}-\\frac{\\delta}{2a}\\right)"
                            "\\left(z+\\frac{b}{2a}+\\frac{\\delta}{2a}\\right)\\\\"
                            "&=a(z-z_1)(z-z_2)."
                            "\\end{aligned}"
                        ),
                        "<p>Un produit est nul si et seulement si l’un de ses facteurs est nul. Comme ",
                        m_inline("a\\neq0"),
                        ", on en déduit ",
                        m_display(
                            "az^2+bz+c=0"
                            "\\iff z=z_1\\text{ ou }z=z_2."
                        ),
                        "</p>",
                    ),
                },
                {
                    "id": "1.18",
                    "kind": "theorem",
                    "label": "Théorème 1.18",
                    "subtitle": "Racines n-ièmes complexes",
                    "statementHtml": p(
                        "<p>Soit ",
                        m_inline("z_0=\\rho\\mathrm e^{\\mathrm i\\theta}"),
                        " un nombre complexe non nul écrit sous forme polaire et ",
                        m_inline("n\\in\\mathbb N^*"),
                        ". L’équation ",
                        m_inline("z^n=z_0"),
                        " admet pour solutions les ",
                        m_inline("n"),
                        " nombres ",
                        m_display(
                            "\\sqrt[n]{\\rho}\\,\\mathrm e^{\\mathrm i(\\theta+2k\\pi)/n},"
                            "\\qquad k=0,1,\\ldots,n-1."
                        ),
                        "</p><p>En particulier, les solutions de ",
                        m_inline("z^n=1"),
                        " sont les racines ",
                        m_inline("n"),
                        "-ièmes de l’unité ",
                        m_display("\\mathrm e^{2\\mathrm ik\\pi/n},\\qquad k=0,1,\\ldots,n-1."),
                        "</p>",
                    ),
                    "proofHtml": p(
                        "<p>Pour ",
                        m_inline("k\\in\\{0,\\ldots,n-1\\}"),
                        ", on vérifie ",
                        m_display(
                            "\\left(\\sqrt[n]{\\rho}\\,\\mathrm e^{\\mathrm i(\\theta+2k\\pi)/n}\\right)^n"
                            "=\\rho\\,\\mathrm e^{\\mathrm i(\\theta+2k\\pi)}"
                            "=\\rho\\mathrm e^{\\mathrm i\\theta}=z_0."
                        ),
                        "</p><p>Comme ",
                        m_inline("z_0\\neq0"),
                        ", ces ",
                        m_inline("n"),
                        " nombres sont deux à deux distincts&nbsp;: si ",
                        m_inline("k\\neq j"),
                        " dans ",
                        m_inline("\\{0,\\ldots,n-1\\}"),
                        ", alors ",
                        m_display(
                            "\\sqrt[n]{\\rho}\\,\\mathrm e^{\\mathrm i(\\theta+2k\\pi)/n}"
                            "=\\sqrt[n]{\\rho}\\,\\mathrm e^{\\mathrm i(\\theta+2j\\pi)/n}"
                            "\\iff \\mathrm e^{2\\mathrm i(k-j)\\pi/n}=1"
                            "\\iff \\frac{k-j}{n}\\in\\mathbb Z"
                            "\\iff k=j."
                        ),
                        "</p><p>On a ainsi ",
                        m_inline("n"),
                        " racines distinctes du polynôme ",
                        m_inline("P(z)=z^n-z_0"),
                        " de degré ",
                        m_inline("n"),
                        ", donc ce sont toutes ses racines.</p>",
                    ),
                },
            ],
        },
        {
            "id": "ensembles",
            "number": "2",
            "title": "Ensembles et langage mathématique",
            "demonstrations": [],
            "emptyMessage": "Aucune démonstration essentielle n’est retenue pour ce chapitre dans le polycopié.",
        },
        {
            "id": "fonctions",
            "number": "3",
            "title": "Fonctions et dénombrement",
            "demonstrations": [
                {
                    "id": "3.36",
                    "kind": "proposition",
                    "label": "Proposition 3.36",
                    "subtitle": "Formule du triangle de Pascal",
                    "statementHtml": p(
                        "<p>Pour tout ",
                        m_inline("n\\in\\mathbb N"),
                        " et pour ",
                        m_inline("k\\in\\{1,\\ldots,n-1\\}"),
                        ", on a ",
                        m_display(
                            "\\binom{n}{k}"
                            "=\\binom{n-1}{k-1}+\\binom{n-1}{k}."
                        ),
                        "</p>",
                    ),
                    "proofHtml": p(
                        "<p><strong>Justification combinatoire.</strong> Parmi ",
                        m_inline("n"),
                        " objets, on doit en choisir ",
                        m_inline("k"),
                        ". Supposons qu’un objet soit distingué (rouge). Les choix de ",
                        m_inline("k"),
                        " objets se répartissent en deux cas&nbsp;:</p>",
                        "<ul>",
                        "<li>l’objet rouge n’est pas choisi&nbsp;: on choisit ",
                        m_inline("k"),
                        " objets parmi les ",
                        m_inline("n-1"),
                        " restants, soit ",
                        m_inline("\\binom{n-1}{k}"),
                        " possibilités&nbsp;;</li>",
                        "<li>l’objet rouge est choisi&nbsp;: il reste ",
                        m_inline("k-1"),
                        " objets à choisir parmi les ",
                        m_inline("n-1"),
                        " autres, soit ",
                        m_inline("\\binom{n-1}{k-1}"),
                        " possibilités.</li>",
                        "</ul>",
                        "<p>En comptant toutes les possibilités, on obtient la formule annoncée.</p>",
                        "<p><strong>Justification calculatoire.</strong> À partir des expressions ",
                        m_inline("\\binom{n}{k}=\\dfrac{n!}{k!(n-k)!}"),
                        " et ",
                        m_inline("\\binom{n}{k}=\\dfrac{n}{k}\\binom{n-1}{k-1}"),
                        ", on calcule ",
                        m_display(
                            "\\binom{n-1}{k-1}+\\binom{n-1}{k}"
                            "=\\frac{(n-1)!}{(k-1)!(n-k)!}"
                            "+\\frac{(n-1)!}{k!(n-k-1)!}"
                            "=\\frac{(n-1)!}{k!(n-k)!}\\,(k+n-k)"
                            "=\\binom{n}{k}."
                        ),
                        "</p>",
                    ),
                },
                {
                    "id": "3.37",
                    "kind": "theorem",
                    "label": "Théorème 3.37",
                    "subtitle": "Somme des entiers de 1 à n",
                    "statementHtml": p(
                        "<p>Pour tout ",
                        m_inline("n\\geqslant1"),
                        ", la somme des ",
                        m_inline("n"),
                        " premiers entiers vaut ",
                        m_display(
                            "\\sum_{k=1}^{n}k=1+2+\\cdots+n=\\frac{n(n+1)}{2}."
                        ),
                        "</p>",
                    ),
                    "proofHtml": p(
                        "<p>On pose, pour ",
                        m_inline("n\\in\\mathbb N^*"),
                        ", ",
                        m_display("H(n):\\quad \\sum_{k=1}^{n}k=\\frac{n(n+1)}{2}."),
                        "<p><strong>Initialisation.</strong> Pour ",
                        m_inline("n=1"),
                        ", ",
                        m_inline("\\sum_{k=1}^{1}k=1=\\dfrac{1\\cdot2}{2}"),
                        ".</p>",
                        "<p><strong>Hérédité.</strong> Supposons ",
                        m_inline("H(n)"),
                        " vraie. Alors ",
                        m_display(
                            "\\sum_{k=1}^{n+1}k"
                            "=\\sum_{k=1}^{n}k+(n+1)"
                            "=\\frac{n(n+1)}{2}+(n+1)"
                            "=\\frac{(n+1)(n+2)}{2}."
                        ),
                        " Donc ",
                        m_inline("H(n+1)"),
                        " est vraie.</p>",
                        "<p><strong>Conclusion.</strong> Par récurrence, ",
                        m_inline("H(n)"),
                        " est vraie pour tout ",
                        m_inline("n\\in\\mathbb N^*"),
                        ".</p>",
                    ),
                },
                {
                    "id": "3.38",
                    "kind": "theorem",
                    "label": "Théorème 3.38",
                    "subtitle": "Identité remarquable généralisée",
                    "statementHtml": p(
                        "<p>Pour tout ",
                        m_inline("n\\in\\mathbb N"),
                        " et pour tous ",
                        m_inline("a,b"),
                        " (réels, complexes, ou plus généralement commutatifs), ",
                        m_display(
                            "a^{n+1}-b^{n+1}=(a-b)\\sum_{k=0}^{n}a^{n-k}b^k"
                            "=(a-b)\\left(a^n+a^{n-1}b+\\cdots+ab^{n-1}+b^n\\right)."
                        ),
                        " On convient que ",
                        m_inline("a^0=b^0=1"),
                        ".</p>",
                    ),
                    "proofHtml": p(
                        "<p>On pose, pour ",
                        m_inline("n\\in\\mathbb N"),
                        ", ",
                        m_display(
                            "H(n):\\quad a^{n+1}-b^{n+1}"
                            "=(a-b)\\sum_{k=0}^{n}a^{n-k}b^k."
                        ),
                        "<p><strong>Initialisation.</strong> Pour ",
                        m_inline("n=0"),
                        ", les deux membres valent ",
                        m_inline("a-b"),
                        ".</p>",
                        "<p><strong>Hérédité.</strong> Supposons ",
                        m_inline("H(n)"),
                        " vraie. Alors ",
                        m_display(
                            "(a-b)\\sum_{k=0}^{n+1}a^{n+1-k}b^k"
                            "=a(a-b)\\sum_{k=0}^{n}a^{n-k}b^k+b^{n+1}"
                            "=a(a^{n+1}-b^{n+1})+(a-b)b^{n+1}"
                            "=a^{n+2}-b^{n+2}."
                        ),
                        " Donc ",
                        m_inline("H(n+1)"),
                        " est vraie.</p>",
                        "<p><strong>Conclusion.</strong> Par récurrence, ",
                        m_inline("H(n)"),
                        " est vraie pour tout ",
                        m_inline("n\\in\\mathbb N"),
                        ".</p>",
                    ),
                },
                {
                    "id": "3.40",
                    "kind": "theorem",
                    "label": "Théorème 3.40",
                    "subtitle": "Formule du binôme de Newton",
                    "statementHtml": p(
                        "<p>Pour tout ",
                        m_inline("n\\geqslant1"),
                        " et pour tous ",
                        m_inline("a,b"),
                        ", ",
                        m_display(
                            "(a+b)^n=\\sum_{k=0}^{n}\\binom{n}{k}a^k b^{n-k}"
                            "=b^n+nb^{n-1}a+\\cdots+nba^{n-1}+a^n."
                        ),
                        "</p>",
                    ),
                    "proofHtml": p(
                        "<p>On pose, pour ",
                        m_inline("n\\in\\mathbb N^*"),
                        ", ",
                        m_display("H(n):\\quad (a+b)^n=\\sum_{k=0}^{n}\\binom{n}{k}a^k b^{n-k}."),
                        "<p><strong>Initialisation.</strong> Pour ",
                        m_inline("n=1"),
                        ", ",
                        m_inline("(a+b)^1=a+b"),
                        ".</p>",
                        "<p><strong>Hérédité.</strong> Supposons ",
                        m_inline("H(n)"),
                        " vraie. Alors ",
                        m_display(
                            "\\begin{aligned}"
                            "(a+b)^{n+1}"
                            "&=(a+b)(a+b)^n\\\\"
                            "&=(a+b)\\sum_{k=0}^{n}\\binom{n}{k}a^k b^{n-k}\\\\"
                            "&=\\sum_{k=0}^{n}\\binom{n}{k}a^{k+1}b^{n-k}"
                            "+\\sum_{k=0}^{n}\\binom{n}{k}a^k b^{n-k+1}\\\\"
                            "&=a^{n+1}+b^{n+1}"
                            "+\\sum_{k=1}^{n}\\left(\\binom{n}{k-1}+\\binom{n}{k}\\right)a^k b^{n+1-k}\\\\"
                            "&=\\sum_{k=0}^{n+1}\\binom{n+1}{k}a^k b^{n+1-k},"
                            "\\end{aligned}"
                        ),
                        " en utilisant la formule du triangle de Pascal. Donc ",
                        m_inline("H(n+1)"),
                        " est vraie.</p>",
                        "<p><strong>Conclusion.</strong> Par récurrence, ",
                        m_inline("H(n)"),
                        " est vraie pour tout ",
                        m_inline("n\\in\\mathbb N^*"),
                        ".</p>",
                    ),
                },
            ],
        },
        {
            "id": "suites",
            "number": "4",
            "title": "Limites de suites",
            "demonstrations": [
                {
                    "id": "4.13",
                    "kind": "proposition",
                    "label": "Proposition 4.13",
                    "subtitle": "Toute suite convergente est bornée",
                    "statementHtml": p(
                        "<p>Soit ",
                        m_inline("(u_n)_{n\\in\\mathbb N}"),
                        " une suite convergente. Alors ",
                        m_inline("(u_n)_{n\\in\\mathbb N}"),
                        " est bornée.</p>",
                    ),
                    "proofHtml": p(
                        "<p>Notons ",
                        m_inline("\\ell\\in\\mathbb R"),
                        " la limite de ",
                        m_inline("(u_n)"),
                        ". Comme la suite converge, il existe ",
                        m_inline("n_0\\in\\mathbb N"),
                        " tel que, pour tout ",
                        m_inline("n\\geqslant n_0"),
                        ", ",
                        m_inline("u_n\\in]\\ell-1,\\ell+1["),
                        ".</p>",
                        "<p>Avant le rang ",
                        m_inline("n_0"),
                        ", la suite ne prend qu’un nombre fini de valeurs. Posons ",
                        m_inline("S=\\{u_0,\\ldots,u_{n_0-1}\\}"),
                        " et ",
                        m_display("M=\\max\\bigl(S\\cup\\{\\ell+1\\}\\bigr),\\qquad m=\\min\\bigl(S\\cup\\{\\ell-1\\}\\bigr)."),
                        "<p>Pour ",
                        m_inline("n\\geqslant n_0"),
                        ", on a ",
                        m_inline("\\ell-1\\leqslant u_n\\leqslant\\ell+1"),
                        ", donc ",
                        m_inline("m\\leqslant u_n\\leqslant M"),
                        ". Pour ",
                        m_inline("n\\leqslant n_0-1"),
                        ", ",
                        m_inline("u_n\\in S"),
                        ", donc encore ",
                        m_inline("m\\leqslant u_n\\leqslant M"),
                        ". La suite est bornée.</p>",
                    ),
                },
                {
                    "id": "4.14",
                    "kind": "theorem",
                    "label": "Théorème 4.14",
                    "subtitle": "Théorème des gendarmes",
                    "statementHtml": p(
                        "<p>Soient ",
                        m_inline("(u_n)"),
                        ", ",
                        m_inline("(v_n)"),
                        " et ",
                        m_inline("(w_n)"),
                        " des suites réelles et ",
                        m_inline("\\ell\\in\\mathbb R"),
                        ". On suppose&nbsp;:</p>",
                        "<ol>",
                        "<li>il existe ",
                        m_inline("N\\in\\mathbb N"),
                        " tel que, pour tout ",
                        m_inline("n\\geqslant N"),
                        ", ",
                        m_inline("u_n\\leqslant v_n\\leqslant w_n"),
                        "&nbsp;;</li>",
                        "<li>",
                        m_inline("(u_n)"),
                        " et ",
                        m_inline("(w_n)"),
                        " convergent vers ",
                        m_inline("\\ell"),
                        ".</li>",
                        "</ol>",
                        "<p>Alors ",
                        m_inline("(v_n)"),
                        " converge et ",
                        m_inline("\\lim_{n\\to\\infty} v_n=\\ell"),
                        ".</p>",
                    ),
                    "proofHtml": p(
                        "<p>Soit ",
                        m_inline("\\varepsilon>0"),
                        ". Par définition de la limite, il existe ",
                        m_inline("n_1"),
                        " et ",
                        m_inline("n_2"),
                        " tels que, pour ",
                        m_inline("n\\geqslant n_1"),
                        ", ",
                        m_inline("|u_n-\\ell|<\\varepsilon"),
                        ", et pour ",
                        m_inline("n\\geqslant n_2"),
                        ", ",
                        m_inline("|w_n-\\ell|<\\varepsilon"),
                        ".</p>",
                        "<p>Posons ",
                        m_inline("n_0=\\max(n_1,n_2,N)"),
                        ". Pour ",
                        m_inline("n\\geqslant n_0"),
                        ", on a ",
                        m_inline("u_n\\leqslant v_n\\leqslant w_n"),
                        ", donc ",
                        m_display("u_n-\\ell\\leqslant v_n-\\ell\\leqslant w_n-\\ell."),
                        "<p>Il en résulte ",
                        m_display("|v_n-\\ell|\\leqslant\\max\\bigl(|u_n-\\ell|,|w_n-\\ell|\\bigr)<\\varepsilon."),
                        "<p>Donc ",
                        m_inline("(v_n)"),
                        " converge vers ",
                        m_inline("\\ell"),
                        ".</p>",
                    ),
                },
            ],
        },
    ]
}


def main() -> None:
    OUTPUT.write_text(
        json.dumps(DEMONSTRATIONS, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
