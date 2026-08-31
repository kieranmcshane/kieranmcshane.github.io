from pathlib import Path
import json
import re
import unittest

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "_data/repertoire_raisonne.json").read_text())
NATIVE = json.loads(
    (ROOT / "_data/repertoire_native_transcriptions.json").read_text()
)
REFERENCES = json.loads((ROOT / "_data/repertoire_references.json").read_text())
PAGE = (ROOT / "repertoire-raisonne.md").read_text()
EXTRACTOR = (
    ROOT / "scripts/build_repertoire_native_transcriptions.py"
).read_text()
MATHJAX_SOURCE = (
    ROOT / "scripts/data/repertoire_raisonne_mathjax.md"
).read_text()
SCRIPT = (ROOT / "assets/js/repertoire-raisonne.js").read_text()
STYLES = (ROOT / "assets/main.scss").read_text()
HEAD = (ROOT / "_includes/head-custom.html").read_text()
CONFIG = (ROOT / "_config.yml").read_text()
PDF = ROOT / "assets/documents/repertoire-raisonne-algebre-analyse.pdf"


def all_problems():
    return [
        problem
        for part in DATA
        for chapter in part["chapters"]
        for problem in chapter["problems"]
    ]


class RepertoireRaisonneTests(unittest.TestCase):
    def test_catalogue_contains_every_problem_exactly_once(self):
        problems = all_problems()
        numbers = [problem[0] for problem in problems]
        self.assertEqual(len(problems), 127)
        self.assertEqual(sorted(numbers), list(range(1, 128)))
        self.assertEqual(len(numbers), len(set(numbers)))

    def test_editorial_architecture_is_complete(self):
        self.assertEqual(len(DATA), 5)
        self.assertEqual(sum(len(part["chapters"]) for part in DATA), 14)
        self.assertEqual(
            [part["title"] for part in DATA],
            [
                "Structures algébriques",
                "Algèbre linéaire et opérateurs",
                "Analyse réelle",
                "Analyse complexe et harmonique",
                "Topologie, analyse fonctionnelle et probabilités",
            ],
        )

        real_sequences = next(
            chapter
            for part in DATA
            for chapter in part["chapters"]
            if chapter["id"] == "suites-fonctions-reelles"
        )
        self.assertEqual(
            [problem[0] for problem in real_sequences["problems"]],
            [108, 109, 110, 126, 127],
        )

    def test_every_problem_has_a_title_and_valid_pdf_target(self):
        for number, title, page in all_problems():
            self.assertIsInstance(number, int)
            self.assertGreater(len(title), 8)
            self.assertGreaterEqual(page, 5)
            self.assertLessEqual(page, 64)

    def test_pdf_is_the_reviewed_sixty_six_page_document(self):
        self.assertTrue(PDF.is_file())
        self.assertGreater(PDF.stat().st_size, 400_000)
        reader = PdfReader(PDF)
        self.assertEqual(len(reader.pages), 66)
        self.assertEqual(
            reader.metadata.title,
            "Répertoire raisonné d'algèbre et d'analyse",
        )

    def test_first_110_problems_have_complete_native_transcriptions(self):
        self.assertEqual(len(NATIVE), 110)
        self.assertEqual(
            [item["number"] for item in NATIVE],
            list(range(1, 111)),
        )
        for item in NATIVE:
            self.assertGreater(len(item["statement"]), 8)
            self.assertGreater(len(item["solution"]), 40)
            self.assertGreater(len(item["statementMathjax"]), 15)
            self.assertGreater(len(item["solutionMathjax"]), 50)
            self.assertEqual(
                item["transcription"],
                "Transcription mathématique issue du fac-similé",
            )
            self.assertEqual(item["statement"].count("$") % 2, 0)
            self.assertEqual(item["solution"].count("$") % 2, 0)
        self.assertIn("DEFAULT_SOURCE", EXTRACTOR)
        self.assertIn("--check", EXTRACTOR)
        self.assertNotIn("subprocess.run", EXTRACTOR)
        self.assertGreater(len(MATHJAX_SOURCE), 120_000)
        self.assertEqual(
            len(
                re.findall(
                    r"(?:\*\*|^#{2,3} )Problème\s+\d+",
                    MATHJAX_SOURCE,
                    re.M,
                )
            ),
            127,
        )
        self.assertIn(r"\alpha^{q^{d-1}}", NATIVE[5]["solutionMathjax"])
        self.assertIn(r"\frac{d}{\gcd(d, r)}", NATIVE[5]["solutionMathjax"])
        self.assertIn(r"\frac{1}{qN}", NATIVE[69]["statementMathjax"])
        self.assertIn(r"\frac{1}{qN}", NATIVE[69]["solutionMathjax"])
        self.assertIn(r"\frac{1}{q^2}", NATIVE[69]["statementMathjax"])
        self.assertNotIn(r"\frac{1}{q^N}", NATIVE[69]["solutionMathjax"])
        self.assertIn(r"\bar{f}", NATIVE[79]["solutionMathjax"])
        self.assertIn(r"\partial \Delta", NATIVE[94]["solutionMathjax"])
        self.assertIn(r"\frac{1}{n \sin n}", NATIVE[109]["statementMathjax"])
        self.assertIn("$A^* = A$", NATIVE[14]["solutionMathjax"])
        self.assertIn("$u^* :", NATIVE[39]["solutionMathjax"])
        self.assertIn("$f * g$", NATIVE[81]["statementMathjax"])
        for item in NATIVE:
            item_math_spans = []
            for field in ("statementMathjax", "solutionMathjax"):
                self.assertNotRegex(
                    item[field],
                    r"<p>[^<]*\$\$",
                    msg=(
                        "Display math remained in prose for problem "
                        f"{item['number']} {field}"
                    ),
                )
                math_spans = re.findall(
                    r"\$(?!\$).*?\$|\\\[.*?\\\]",
                    item[field],
                    re.S,
                )
                item_math_spans.extend(math_spans)
                for math_span in math_spans:
                    self.assertNotRegex(
                        math_span,
                        r"</?(?:em|strong)>",
                        msg=(
                            "Markdown emphasis split problem "
                            f"{item['number']} {field}"
                        ),
                    )
            self.assertGreater(
                len(item_math_spans),
                0,
                msg=f"Problem {item['number']} has no MathJax expression",
            )

    def test_reviewed_mathjax_source_keeps_complete_problems_and_clean_structure(self):
        expected_phrases = {
            (13, "statementMathjax"): "Quand  $q$  possède-t-elle",
            (33, "solutionMathjax"): "Il y en a exactement trois",
            (45, "solutionMathjax"): "Il reste donc un point",
            (49, "statementMathjax"): "caractériser le cas d'égalité",
            (63, "statementMathjax"): r"\|AB\|_F \leq \|A\|_F \|B\|_F",
            (71, "solutionMathjax"): "Ainsi  $L$  est transcendant",
            (82, "solutionMathjax"): "l'inégalité de Young",
            (107, "solutionMathjax"): "n'est pas intégrable à l'infini",
        }
        for (number, field), phrase in expected_phrases.items():
            self.assertIn(phrase, NATIVE[number - 1][field])

        for item in NATIVE:
            for field in ("statement", "solution", "statementMathjax", "solutionMathjax"):
                self.assertNotRegex(
                    item[field],
                    r'<span id="page-|(?m:^#{1,6}\s+)|\*\*Deuxième partie',
                    msg=f"Page-conversion debris in problem {item['number']} {field}",
                )
            for field in ("statementMathjax", "solutionMathjax"):
                self.assertNotRegex(
                    item[field],
                    r"<p>\s*(?:\||[-*+]\s+|\d+[.)]\s+)",
                    msg=f"Unrendered Markdown in problem {item['number']} {field}",
                )

        rendered = "".join(
            item[field]
            for item in NATIVE
            for field in ("statementMathjax", "solutionMathjax")
        )
        self.assertEqual(rendered.count("<table>"), 2)
        self.assertEqual(rendered.count("<ul>"), 3)
        self.assertEqual(rendered.count("<ol>"), 4)
        self.assertEqual(rendered.count('scope="col"'), 5)
        self.assertNotIn('<span id="page-', MATHJAX_SOURCE)

    def test_hand_composed_problems_have_balanced_mathjax_delimiters(self):
        for number in range(111, 128):
            start = PAGE.index(f'id="probleme-natif-{number}"')
            next_marker = f'id="probleme-natif-{number + 1}"'
            end = PAGE.find(next_marker, start) if number < 127 else len(PAGE)
            card = PAGE[start:end]
            self.assertEqual(
                card.count(r"\("),
                card.count(r"\)"),
                msg=f"Unbalanced inline MathJax in problem {number}",
            )
            self.assertEqual(
                card.count(r"\["),
                card.count(r"\]"),
                msg=f"Unbalanced display MathJax in problem {number}",
            )
            self.assertGreater(
                card.count(r"\(") + card.count(r"\["),
                0,
                msg=f"Problem {number} has no MathJax expression",
            )

    def test_oral_references_are_problem_specific_and_evidenced(self):
        self.assertEqual(
            set(REFERENCES),
            {"5", "9", "25", "47", "100", "101", "102", "107"},
        )
        for problem_number, references in REFERENCES.items():
            self.assertTrue(problem_number.isdigit())
            self.assertEqual(len(references), 1)
            for reference in references:
                self.assertTrue(
                    reference["url"].startswith(
                        "https://agreg-maths.fr/ressources/retours#collapse_panel_"
                    )
                )
                self.assertGreater(len(reference["title"]), 8)
                self.assertGreater(len(reference["evidence"]), 30)
                self.assertIn("Retour d’oral 2026", reference["source"])

    def test_page_exposes_navigation_review_and_download(self):
        self.assertIn(
            "title: Problèmes corrigés",
            PAGE,
        )
        self.assertIn(
            "Algèbre · analyse · topologie · probabilités",
            PAGE,
        )
        self.assertIn("<h1>127 problèmes corrigés de mathématiques</h1>", PAGE)
        self.assertNotIn("127 problèmes, un outil décisif à chaque fois", PAGE)
        self.assertIn("Corpus complet en ligne", PAGE)
        self.assertIn("transcription mathématique structurée", PAGE)
        self.assertNotIn("Corpus intégralement relu", PAGE)
        self.assertIn("data-repertoire-problem", PAGE)
        self.assertIn("data-repertoire-part", PAGE)
        self.assertIn("data-repertoire-preset", PAGE)
        self.assertIn("127 problèmes à travailler directement ici", PAGE)
        self.assertIn("onze énoncés et solutions", PAGE)
        self.assertIn("quatre énoncés et solutions", PAGE)
        self.assertIn("deux énoncés et solutions", PAGE)
        self.assertEqual(PAGE.count("data-repertoire-audit-problem="), 17)
        # One Liquid template renders 1–110; the 17 reviewed MathJax cards
        # remain hand-composed below it.
        self.assertEqual(PAGE.count("data-repertoire-native-problem="), 18)
        self.assertIn(
            'href="#probleme-natif-{{ problem[0] }}"',
            PAGE,
        )
        for number in range(111, 128):
            self.assertIn(
                f'data-repertoire-audit-problem="{number}"',
                PAGE,
            )
            self.assertIn(
                f'data-repertoire-native-problem="{number}"',
                PAGE,
            )
            self.assertIn(f'id="probleme-natif-{number}"', PAGE)
        self.assertEqual(PAGE.count("Afficher la solution"), 18)
        self.assertIn("repertoire-native-references", PAGE)
        self.assertIn(
            "lorsqu’un retour d’oral contient effectivement la question correspondante",
            PAGE,
        )
        self.assertNotIn("Références et prolongements du chapitre", PAGE)
        self.assertNotIn("chapter_id=", PAGE)
        self.assertIn(r"\lVert f(x)-f(y)\rVert", PAGE)
        self.assertIn(r"\varnothing\ne X\cap I\subset S_n", PAGE)
        self.assertIn(r"A_{jk}=\frac{j^k}{k!}", PAGE)
        self.assertIn(
            "Le fac-similé PDF n’apparaît qu’en source primaire de contrôle",
            PAGE,
        )
        self.assertIn("Une correction, quatre précisions", PAGE)
        self.assertIn("Correction mathématique", PAGE)
        self.assertIn(r"\overline f\,P_k", PAGE)
        self.assertIn("Problème 4 · page 3 du livre", PAGE)
        self.assertIn("Problème 6 · page 3 du livre", PAGE)
        self.assertIn("Problème 80 · page 37 du livre", PAGE)
        self.assertIn("Problème 91 · page 43 du livre", PAGE)
        self.assertIn("Problème 106 · page 51 du livre", PAGE)
        self.assertIn("repertoire-raisonne-algebre-analyse.pdf", PAGE)

    def test_interaction_and_styling_are_scoped_to_the_page(self):
        self.assertIn("repertoire-library", STYLES)
        self.assertIn("repertoire-problem-list", STYLES)
        self.assertIn("repertoire-native-list", STYLES)
        self.assertIn("repertoire-native-solution", STYLES)
        self.assertIn("repertoire-native-transcription", STYLES)
        self.assertIn("repertoire-native-equation", STYLES)
        self.assertIn("repertoire-native-table-wrap", STYLES)
        self.assertIn(".repertoire-native-transcription ol", STYLES)
        self.assertIn("white-space: normal", STYLES)
        self.assertIn("repertoire-native-references", STYLES)
        self.assertIn("repertoire-search-input", SCRIPT)
        self.assertIn("nativeSearch", SCRIPT)
        self.assertIn("normalize", SCRIPT)
        self.assertIn("data-repertoire-section", SCRIPT)
        self.assertIn("repertoire-raisonne.js", HEAD)
        self.assertIn("repertoire-raisonne.md", CONFIG)


if __name__ == "__main__":
    unittest.main()
