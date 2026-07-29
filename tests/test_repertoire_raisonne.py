from pathlib import Path
import json
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
            self.assertIn(item["chapterId"], REFERENCES)
            self.assertGreaterEqual(len(REFERENCES[item["chapterId"]]), 1)
            if item["number"] != 6:
                self.assertEqual(
                    item["transcription"],
                    "Transcription textuelle issue du fac-similé",
                )
        self.assertIn("pdftotext", EXTRACTOR)
        self.assertIn(r"\alpha^{q^{d-1}}", NATIVE[5]["solutionMathjax"])
        self.assertIn(r"\frac{d}{\gcd(d,r)}", NATIVE[5]["solutionMathjax"])
        self.assertEqual(
            NATIVE[5]["transcription"],
            "Formules recomposées et contrôlées",
        )
        self.assertIn("conjuguée de f", NATIVE[79]["solution"])

    def test_references_are_curated_for_every_editorial_chapter(self):
        chapter_ids = {
            chapter["id"]
            for part in DATA
            for chapter in part["chapters"]
        }
        self.assertEqual(set(REFERENCES), chapter_ids)
        for references in REFERENCES.values():
            self.assertGreaterEqual(len(references), 1)
            for reference in references:
                self.assertTrue(reference["url"].startswith("https://agreg-maths.fr/"))
                self.assertGreater(len(reference["title"]), 8)

    def test_page_exposes_navigation_review_and_download(self):
        self.assertIn("127 problèmes, un outil décisif à chaque fois", PAGE)
        self.assertIn("Corpus intégralement relu", PAGE)
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
        self.assertIn("https://agreg-maths.fr/ressources/retours", PAGE)
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
