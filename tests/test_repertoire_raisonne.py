from pathlib import Path
import json
import unittest

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "_data/repertoire_raisonne.json").read_text())
PAGE = (ROOT / "repertoire-raisonne.md").read_text()
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

    def test_page_exposes_navigation_review_and_download(self):
        self.assertIn("127 problèmes, un outil décisif à chaque fois", PAGE)
        self.assertIn("Corpus intégralement relu", PAGE)
        self.assertIn("data-repertoire-problem", PAGE)
        self.assertIn("data-repertoire-part", PAGE)
        self.assertIn("data-repertoire-preset", PAGE)
        self.assertIn("Relecture détaillée des 17 derniers problèmes", PAGE)
        self.assertIn("Problèmes 111–121", PAGE)
        self.assertIn("Problèmes 122–125", PAGE)
        self.assertIn("Problèmes 126–127", PAGE)
        self.assertEqual(PAGE.count("data-repertoire-audit-problem="), 17)
        for number in range(111, 128):
            self.assertIn(
                f'data-repertoire-audit-problem="{number}"',
                PAGE,
            )
        self.assertIn("L’itération", PAGE)
        self.assertIn("Les formules de Taylor aux points", PAGE)
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
        self.assertIn("repertoire-audit-list", STYLES)
        self.assertIn("repertoire-search-input", SCRIPT)
        self.assertIn("normalize", SCRIPT)
        self.assertIn("data-repertoire-section", SCRIPT)
        self.assertIn("repertoire-raisonne.js", HEAD)
        self.assertIn("repertoire-raisonne.md", CONFIG)


if __name__ == "__main__":
    unittest.main()
