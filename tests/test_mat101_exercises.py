from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "_data/mat101_exercises.json").read_text())
PAGE = (ROOT / "mat101-exercises.md").read_text()
CONFIG = (ROOT / "_config.yml").read_text()
STYLES = (ROOT / "assets/main.scss").read_text()
PDF = ROOT / "assets/documents/mat101/recueil-exercices-mat101.pdf"
TEX = ROOT / "assets/documents/mat101/recueil-exercices-mat101.tex"
ARCHIVE = ROOT / "assets/documents/mat101/recueil-exercices-mat101-sources.zip"
BIB = ROOT / "assets/documents/mat101/mat101-citations.bib"


class Mat101ExerciseLibraryTests(unittest.TestCase):
    def test_index_contains_exactly_103_unique_exercises(self):
        exercises = [
            exercise
            for chapter in DATA
            for page in chapter["pages"]
            for exercise in page["exercises"]
        ]
        self.assertEqual(len(exercises), 103)
        self.assertEqual(len(exercises), len(set(exercises)))

    def test_chapter_counts_match_declared_distribution(self):
        actual = [
            sum(len(page["exercises"]) for page in chapter["pages"])
            for chapter in DATA
        ]
        self.assertEqual(actual, [20, 35, 31, 17])
        self.assertEqual(actual, [chapter["count"] for chapter in DATA])

    def test_every_exercise_targets_a_valid_pdf_page(self):
        targets = [
            page["pdfPage"]
            for chapter in DATA
            for page in chapter["pages"]
            if page["exercises"]
        ]
        self.assertGreaterEqual(min(targets), 3)
        self.assertLessEqual(max(targets), 34)

    def test_downloadable_artifacts_are_present(self):
        self.assertTrue(PDF.read_bytes().startswith(b"%PDF-"))
        self.assertGreater(PDF.stat().st_size, 500_000)
        self.assertIn(r"\includepdf[pages=61-70]", TEX.read_text())
        self.assertGreater(ARCHIVE.stat().st_size, 500_000)

    def test_section_is_visible_and_explains_solution_status(self):
        self.assertIn("permalink: /mat101/exercices/", PAGE)
        self.assertIn("103 exercices de mathématiques", PAGE)
        self.assertIn("Un corrigé intégral ne sera publié", PAGE)
        self.assertIn("mat101-exercises.md", CONFIG)

    def test_credits_distinguish_original_adaptation_and_future_solutions(self):
        self.assertIn("Contenu mathématique original", PAGE)
        self.assertIn("Cette édition et cette interface", PAGE)
        self.assertIn("Futurs corrigés", PAGE)
        self.assertIn("Raphaël Rossignol comme dernier responsable", PAGE)
        self.assertIn("avec l’assistance d’OpenAI Codex", PAGE)
        self.assertIn("non officielles et non attribuées à l’UGA", PAGE)

    def test_citation_and_rights_language_is_precise(self):
        self.assertIn("Citation bibliographique recommandée", PAGE)
        self.assertIn("Aucune licence de réutilisation explicite", PAGE)
        self.assertIn("ni une édition officielle de l’UGA ni un corrigé officiel", PAGE)
        bib = BIB.read_text()
        self.assertIn("@misc{collectif_mat101_2022", bib)
        self.assertIn("@misc{mcshane_recueil_mat101_2026", bib)

    def test_pdf_metadata_credits_original_collective(self):
        tex = TEX.read_text()
        self.assertIn(
            "pdfauthor={Collectif MAT101, Université Grenoble Alpes}",
            tex,
        )
        self.assertIn("responsable de l'édition citée", tex)
        self.assertIn("avec l'assistance d'OpenAI Codex", tex)

    def test_mobile_layout_keeps_exercises_accessible(self):
        self.assertIn(".mat101-exercise-grid", STYLES)
        self.assertIn("body:has(.mat101-library) .post-header", STYLES)
        self.assertIn("@media screen and (max-width: 440px)", STYLES)
        self.assertIn("min-height: 44px", STYLES)


if __name__ == "__main__":
    unittest.main()
