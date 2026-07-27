from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "_data/mat101_exercises.json").read_text())
SOLUTIONS = json.loads((ROOT / "_data/mat101_solutions.json").read_text())
NATIVE = json.loads((ROOT / "_data/mat101_native.json").read_text())
PAGE = (ROOT / "mat101-exercises.md").read_text()
CONFIG = (ROOT / "_config.yml").read_text()
STYLES = (ROOT / "assets/main.scss").read_text()
SCRIPT = (ROOT / "assets/js/mat101-library.js").read_text()
ISSUE_FORM = (ROOT / ".github/ISSUE_TEMPLATE/mat101-correction.yml").read_text()
PDF = ROOT / "assets/documents/mat101/recueil-exercices-mat101.pdf"
TEX = ROOT / "assets/documents/mat101/recueil-exercices-mat101.tex"
ARCHIVE = ROOT / "assets/documents/mat101/recueil-exercices-mat101-sources.zip"
SOLUTION_PDF = ROOT / "assets/documents/mat101/corrige-exercices-mat101.pdf"
SOLUTION_TEX = ROOT / "assets/documents/mat101/corrige-exercices-mat101.tex"
SOLUTION_ARCHIVE = ROOT / "assets/documents/mat101/corrige-exercices-mat101-sources.zip"
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

    def test_every_exercise_has_one_solution_page(self):
        exercise_ids = {
            exercise
            for chapter in DATA
            for page in chapter["pages"]
            for exercise in page["exercises"]
        }
        solution_ids = [solution["id"] for solution in SOLUTIONS]
        self.assertEqual(len(solution_ids), 103)
        self.assertEqual(len(solution_ids), len(set(solution_ids)))
        self.assertEqual(set(solution_ids), exercise_ids)
        self.assertGreaterEqual(min(solution["pdfPage"] for solution in SOLUTIONS), 6)
        self.assertLessEqual(max(solution["pdfPage"] for solution in SOLUTIONS), 57)

    def test_every_exercise_has_native_statement_and_solution(self):
        expected_ids = [
            exercise
            for chapter in DATA
            for page in chapter["pages"]
            for exercise in page["exercises"]
        ]
        native_ids = [exercise["id"] for exercise in NATIVE]
        self.assertEqual(native_ids, expected_ids)
        self.assertEqual(len(NATIVE), 103)
        self.assertEqual(sum(len(item["statementImages"]) for item in NATIVE), 122)

        for item in NATIVE:
            self.assertGreater(len(item["solutionHtml"]), 100)
            self.assertNotIn("TODO", item["solutionHtml"])
            self.assertTrue(item["statementImages"])
            for image_url in item["statementImages"]:
                image = ROOT / image_url.lstrip("/")
                self.assertTrue(image.exists(), image)
                self.assertGreater(image.stat().st_size, 1_000)

    def test_difficulty_markers_match_the_source_booklet(self):
        markers = {item["id"]: item["difficulty"] for item in NATIVE}
        self.assertEqual(set(markers.values()), {"*", "**", "***", "*/**", None})
        self.assertEqual(markers["1.1"], "*")
        self.assertEqual(markers["2.5"], "*/**")
        self.assertEqual(markers["2.23"], "***")
        self.assertIsNone(markers["3.13"])
        self.assertEqual(markers["3.31"], "***")
        self.assertEqual(markers["4.17"], "**")

    def test_downloadable_artifacts_are_present(self):
        self.assertTrue(PDF.read_bytes().startswith(b"%PDF-"))
        self.assertGreater(PDF.stat().st_size, 500_000)
        self.assertIn(r"\includepdf[pages=61-70]", TEX.read_text())
        self.assertGreater(ARCHIVE.stat().st_size, 500_000)
        self.assertTrue(SOLUTION_PDF.read_bytes().startswith(b"%PDF-"))
        self.assertGreater(SOLUTION_PDF.stat().st_size, 400_000)
        self.assertIn(r"\begin{corrige}{4.17}", SOLUTION_TEX.read_text())
        self.assertGreater(SOLUTION_ARCHIVE.stat().st_size, 50_000)

    def test_section_is_visible_and_explains_solution_status(self):
        self.assertIn("permalink: /mat101/exercices/", PAGE)
        self.assertIn("math: true", PAGE)
        self.assertIn("103 exercices à travailler ici", PAGE)
        self.assertIn("Couverture complète", PAGE)
        self.assertIn("aucune relecture mathématique humaine intégrale", PAGE)
        self.assertIn("Afficher le corrigé détaillé", PAGE)
        self.assertIn("mat101-difficulty", PAGE)
        self.assertIn("Difficulté : {{ difficulty_label }}", PAGE)
        self.assertIn("exercise.statementImages", PAGE)
        self.assertIn("exercise.solutionHtml", PAGE)
        self.assertNotIn("#page={{ source_page.pdfPage }}", PAGE)
        self.assertIn("mat101-exercises.md", CONFIG)

    def test_credits_distinguish_original_adaptation_and_solution(self):
        self.assertIn("Énoncés originaux", PAGE)
        self.assertIn("Adaptation web et interface", PAGE)
        self.assertIn("Rédaction du corrigé", PAGE)
        self.assertIn("Raphaël Rossignol est indiqué comme responsable", PAGE)
        self.assertIn("Rédaction initiale assistée par OpenAI ChatGPT", PAGE)
        self.assertIn("ni d’un corrigé officiel de l’UGA", PAGE)

    def test_citation_and_rights_language_is_precise(self):
        self.assertIn("Citations bibliographiques recommandées", PAGE)
        self.assertIn("Aucune licence de réutilisation explicite", PAGE)
        self.assertIn("ne constituent pas une publication de l’UGA", PAGE)
        bib = BIB.read_text()
        self.assertIn("@misc{collectif_mat101_2022", bib)
        self.assertIn("@misc{mcshane_recueil_mat101_2026", bib)
        self.assertIn("@misc{mcshane_corrige_mat101_2026", bib)

    def test_pdf_metadata_credits_original_collective(self):
        tex = TEX.read_text()
        self.assertIn(
            "pdfauthor={Collectif MAT101, Université Grenoble Alpes}",
            tex,
        )
        self.assertIn("responsable de l'édition citée", tex)
        self.assertIn("avec l'assistance d'OpenAI Codex", tex)

    def test_solution_source_discloses_provenance_and_review_status(self):
        tex = SOLUTION_TEX.read_text()
        self.assertIn(
            "pdfauthor={Kieran McShane, avec l'assistance d'OpenAI ChatGPT et Codex}",
            tex,
        )
        self.assertIn("Ressource pédagogique non officielle", tex)
        self.assertIn("Rédaction initiale assistée par OpenAI ChatGPT", tex)
        self.assertIn("contenu mathématique non relu intégralement", tex)
        self.assertNotIn(r"\definecolor{UGAblue}", tex)

    def test_mobile_layout_keeps_exercises_accessible(self):
        self.assertIn(".mat101-native-list", STYLES)
        self.assertIn(".mat101-native-solution", STYLES)
        self.assertIn(".mat101-difficulty-advanced", STYLES)
        self.assertIn(".mat101-statement img", STYLES)
        self.assertIn("body:has(.mat101-library) .post-header", STYLES)
        self.assertIn("@media screen and (max-width: 440px)", STYLES)
        self.assertIn("min-height: 44px", STYLES)

    def test_search_and_hash_navigation_are_progressive_enhancements(self):
        self.assertIn("mat101-search-input", PAGE)
        self.assertIn("data-mat101-exercise", PAGE)
        self.assertIn("normalize('NFD')", SCRIPT)
        self.assertIn("window.location.hash.startsWith('#exercice-')", SCRIPT)
        self.assertIn("mat101-library.js", (ROOT / "_includes/head-custom.html").read_text())

    def test_correction_ticket_collects_verifiable_evidence(self):
        self.assertIn("Exercice concerné", ISSUE_FORM)
        self.assertIn("Passage exact", ISSUE_FORM)
        self.assertIn("Analyse et correction proposée", ISSUE_FORM)
        self.assertIn("Crédit, citation ou attribution", ISSUE_FORM)
        self.assertIn("mat101-correction.yml", PAGE)


if __name__ == "__main__":
    unittest.main()
