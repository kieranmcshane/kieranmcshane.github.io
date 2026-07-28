from pathlib import Path
import json
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "_data/mat101_exercises.json").read_text())
SOLUTIONS = json.loads((ROOT / "_data/mat101_solutions.json").read_text())
NATIVE = json.loads((ROOT / "_data/mat101_native.json").read_text())
TAGS = json.loads((ROOT / "_data/mat101_tags.json").read_text())["tags"]
PAGE = (ROOT / "mat101-exercises.md").read_text()
CONFIG = (ROOT / "_config.yml").read_text()
STYLES = (ROOT / "assets/main.scss").read_text()
SCRIPT = (ROOT / "assets/js/mat101-library.js").read_text()
ISSUE_FORM = (ROOT / ".github/ISSUE_TEMPLATE/mat101-correction.yml").read_text()
ERRATA = json.loads((ROOT / "_data/mat101_errata.json").read_text())
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
        self.assertEqual(max(solution["pdfPage"] for solution in SOLUTIONS), 59)

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

        for item in NATIVE:
            self.assertGreater(len(item["solutionHtml"]), 100)
            self.assertNotIn("TODO", item["solutionHtml"])
            self.assertGreater(len(item["statementHtml"]), 100)
            self.assertGreater(len(item["statementSearchText"]), 30)
            self.assertIn("mat101-statement-transcription", item["statementHtml"])
            self.assertNotIn("<img", item["statementHtml"])
            self.assertGreaterEqual(item["statementSourcePage"], 30)
            self.assertGreaterEqual(item["statementPdfPage"], 3)
            self.assertIn(item["transcriptionStatus"], {"extracted", "curated"})
            self.assertIn(
                item["mathematicalReviewStatus"], {"pending", "reviewed"}
            )

        curated = next(item for item in NATIVE if item["id"] == "3.3")
        self.assertEqual(curated["transcriptionStatus"], "curated")
        self.assertEqual(curated["mathematicalReviewStatus"], "reviewed")
        self.assertIn(r"\dfrac{p}{q}", curated["statementHtml"])
        self.assertIn(r"[\![2,5]\!]", curated["statementHtml"])
        self.assertNotIn("∞ p q", curated["statementSearchText"])
        self.assertNotIn("justifi ation", curated["statementSearchText"])

    def test_statement_images_are_not_primary_content(self):
        self.assertNotIn("statementImages", PAGE)
        self.assertNotIn("mat101-statement img", STYLES)
        statement_directory = ROOT / "assets/images/mat101/statements"
        self.assertFalse(statement_directory.exists())
        self.assertIn("mat101-erratum-badge", PAGE)
        self.assertIn(".mat101-erratum-badge", STYLES)

    def test_solution_tables_are_accessible_and_keep_row_numbers(self):
        tables = [
            item
            for item in NATIVE
            if "mat101-math-table" in item["solutionHtml"]
        ]
        self.assertEqual(len(tables), 5)
        self.assertTrue(
            all("mat101-table-scroll" in item["solutionHtml"] for item in tables)
        )
        exercise = next(item for item in NATIVE if item["id"] == "1.3")
        html = exercise["solutionHtml"]
        self.assertIn(">N°</th>", html)
        self.assertIn(">1</td>", html)
        self.assertIn(">13</td>", html)
        self.assertNotIn(">.</td>", html)

    def test_root_of_unity_exercises_have_lightweight_diagrams(self):
        cubic_roots = next(
            item["solutionHtml"] for item in NATIVE if item["id"] == "1.12"
        )
        fifth_roots = next(
            item["solutionHtml"] for item in NATIVE if item["id"] == "1.18"
        )
        self.assertEqual(cubic_roots.count("data-mat101-root-diagram"), 3)
        self.assertIn("Lecture géométrique", cubic_roots)
        self.assertIn("data-root-count=\"3\"", cubic_roots)
        self.assertIn("data-root-count=\"4\"", cubic_roots)
        self.assertEqual(fifth_roots.count("data-mat101-root-diagram"), 1)
        self.assertIn("data-root-count=\"5\"", fifth_roots)
        self.assertIn("data-muted-index=\"0\"", fifth_roots)
        self.assertNotIn("<svg", cubic_roots + fifth_roots)

    def test_difficulty_markers_match_the_source_booklet(self):
        markers = {item["id"]: item["difficulty"] for item in NATIVE}
        self.assertEqual(set(markers.values()), {"*", "**", "***", "*/**", None})
        self.assertEqual(markers["1.1"], "*")
        self.assertEqual(markers["2.5"], "*/**")
        self.assertEqual(markers["2.23"], "***")
        self.assertIsNone(markers["3.13"])
        self.assertEqual(markers["3.31"], "***")
        self.assertEqual(markers["4.17"], "**")

    def test_tag_index_covers_every_exercise(self):
        expected_ids = {
            exercise
            for chapter in DATA
            for page in chapter["pages"]
            for exercise in page["exercises"]
        }
        slugs = [tag["slug"] for tag in TAGS]
        labels = [tag["label"] for tag in TAGS]
        tagged_ids = {
            exercise
            for tag in TAGS
            for exercise in tag["exercises"]
        }
        self.assertEqual(len(TAGS), 50)
        self.assertEqual(len(slugs), len(set(slugs)))
        self.assertEqual(len(labels), len(set(labels)))
        self.assertEqual(tagged_ids, expected_ids)

        native_tags = {
            item["id"]: {tag["slug"] for tag in item["tags"]}
            for item in NATIVE
        }
        self.assertTrue(all(native_tags.values()))
        self.assertIn("invariants", native_tags["2.23"])
        self.assertIn("relations-equivalence", native_tags["3.31"])
        self.assertIn("methodes-numeriques", native_tags["4.16"])

    def test_polya_structure_is_targeted_and_visible_online(self):
        methods = sum(
            item["solutionHtml"].count('class="mat101-method"')
            for item in NATIVE
        )
        reviews = sum(
            item["solutionHtml"].count('class="mat101-solution-review"')
            for item in NATIVE
        )
        self.assertEqual(methods, 17)
        self.assertEqual(reviews, 16)
        self.assertIn('class="mat101-method"', next(
            item["solutionHtml"] for item in NATIVE if item["id"] == "2.23"
        ))
        self.assertNotIn('class="mat101-method"', next(
            item["solutionHtml"] for item in NATIVE if item["id"] == "2.2"
        ))

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
        self.assertIn("Corpus complet — relecture en cours", PAGE)
        self.assertIn("103 solutions · niveau L1", PAGE)
        self.assertNotIn("103 solutions · 59 pages", PAGE)
        self.assertIn("la vérification indépendante exercice par exercice n’est pas achevée", PAGE)
        self.assertIn("Afficher le corrigé détaillé", PAGE)
        self.assertIn("mat101-difficulty", PAGE)
        self.assertIn("Difficulté : {{ difficulty_label }}", PAGE)
        self.assertIn("Index des notions", PAGE)
        self.assertIn("data-mat101-tag", PAGE)
        self.assertIn("exercise.tags", PAGE)
        self.assertNotIn(
            "{{ chapter.count }} exercices · pages originales",
            PAGE,
        )
        self.assertIn("exercise.statementHtml", PAGE)
        self.assertIn("exercise.statementSearchText", PAGE)
        self.assertIn("Consulter la page source", PAGE)
        self.assertIn("exercise.solutionHtml", PAGE)
        self.assertNotIn("#page={{ source_page.pdfPage }}", PAGE)
        self.assertIn("mat101-exercises.md", CONFIG)

    def test_errata_register_is_versioned_and_linked(self):
        exercises = [entry["exercise"] for entry in ERRATA]
        self.assertEqual(len(ERRATA), 10)
        self.assertEqual(len(exercises), len(set(exercises)))
        self.assertIn("1.7", exercises)
        self.assertIn("3.31", exercises)
        self.assertIn("4.17", exercises)
        self.assertTrue(all(entry["version"] == "2026-07-28" for entry in ERRATA))
        self.assertIn("Errata du polycopié source", PAGE)
        self.assertIn("site.data.mat101_errata", PAGE)

    def test_credits_distinguish_original_adaptation_and_solution(self):
        self.assertIn("Énoncés originaux", PAGE)
        self.assertIn("Adaptation web et interface", PAGE)
        self.assertIn("Rédaction du corrigé", PAGE)
        self.assertIn("méthode de George Pólya", PAGE)
        self.assertIn("Raphaël Rossignol est indiqué comme responsable", PAGE)
        self.assertIn("Rédaction initiale assistée par OpenAI ChatGPT", PAGE)
        self.assertIn("ni d’un corrigé officiel de l’UGA", PAGE)
        self.assertIn("'/about/#contact'", PAGE)
        self.assertNotIn("Découpe fidèle des énoncés", PAGE)

    def test_citation_and_rights_language_is_precise(self):
        self.assertIn("Citations bibliographiques recommandées", PAGE)
        self.assertIn("Aucune licence de réutilisation explicite", PAGE)
        self.assertIn("ne constituent pas une publication de l’UGA", PAGE)
        bib = BIB.read_text()
        self.assertIn("@misc{collectif_mat101_2022", bib)
        self.assertIn("@misc{mcshane_recueil_mat101_2026", bib)
        self.assertIn("@misc{mcshane_corrige_mat101_2026", bib)
        self.assertIn("@book{polya_how_to_solve_it_1945", bib)

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
        self.assertEqual(tex.count(r"\begin{methode}"), 17)
        self.assertEqual(tex.count(r"\textbf{Examen de la solution.}"), 16)
        self.assertIn("George Pólya", tex)
        self.assertNotIn(r"\definecolor{UGAblue}", tex)

    def test_solution_source_follows_the_redaction_guidelines(self):
        tex = SOLUTION_TEX.read_text()
        self.assertIn(
            "Les transformations successives d'une même expression sont "
            "disposées sur plusieurs lignes",
            tex,
        )
        self.assertIn(
            "avec les signes d'égalité alignés",
            tex,
        )
        exercise_11 = tex.split(r"\begin{corrige}{1.1}", 1)[1].split(
            r"\end{corrige}",
            1,
        )[0]
        self.assertGreaterEqual(exercise_11.count(r"\begin{align*}"), 10)
        self.assertNotIn(
            r"\ii^{50}=\ii^{48}\ii^2=(\ii^4)^{12}(-1)",
            exercise_11,
        )
        self.assertIn(
            "Lorsqu'un objet est introduit ou identifié, sa nature "
            "mathématique est nommée explicitement",
            tex,
        )
        self.assertIn(
            "La notation ne doit pas porter seule cette information de catégorie",
            tex,
        )
        self.assertIn(
            "racine du polynôme $R(Y)=Y^2+Y-1$",
            tex,
        )
        self.assertIn(
            "Les racines du polynôme $R$ sont",
            tex,
        )
        self.assertNotIn(
            "racine de $R(Y)=Y^2+Y-1$",
            tex,
        )
        self.assertIn(
            r"Soient $n\in\N^*$, $\rho>0$ et $\theta\in\R$",
            tex,
        )
        self.assertIn("La loi de De Morgan montre", tex)
        self.assertNotIn(r"x>0\Rightarrow f(x)>0", tex)
        self.assertNotIn(r"P(i,j)\iff", tex)
        self.assertNotIn(
            r"f(x)\geq\frac32\iff x\in",
            tex,
        )
        self.assertIn(
            r"(z^5+z^4+z^3+z^2+z)-(z^4+z^3+z^2+z+1)",
            tex,
        )
        self.assertIn(
            "Les termes de degrés $1$ à $4$ s'annulent deux à deux",
            tex,
        )
        self.assertNotIn(
            "L'identité de la somme géométrique donne",
            tex,
        )
        self.assertNotIn(r"\sum_{k=0}na^{n-k}b^k", tex)
        self.assertIn(r"\sum_{k=0}^{n}a^{n-k}b^k", tex)
        self.assertIn("Écrivons d'abord les deux différences", tex)
        self.assertIn("Le dessin permet d'anticiper ce résultat", tex)

        with zipfile.ZipFile(SOLUTION_ARCHIVE) as archive:
            autonomous = archive.read(
                "Corrige_exercices_MAT101_autonome.tex"
            ).decode()
        self.assertEqual(autonomous, tex)

    def test_mobile_layout_keeps_exercises_accessible(self):
        self.assertIn(".mat101-native-list", STYLES)
        self.assertIn(".mat101-native-solution", STYLES)
        self.assertIn(".mat101-method", STYLES)
        self.assertIn(".mat101-solution-review", STYLES)
        self.assertIn(".mat101-difficulty-advanced", STYLES)
        self.assertIn(".mat101-tag-filter.is-active", STYLES)
        self.assertIn(".mat101-exercise-tags", STYLES)
        self.assertIn(".mat101-table-scroll", STYLES)
        self.assertIn(".mat101-math-table", STYLES)
        self.assertIn(".mat101-root-geometry", STYLES)
        self.assertIn(".mat101-root-diagram", STYLES)
        self.assertIn(".mat101-statement-transcription", STYLES)
        self.assertIn("body:has(.mat101-library) .post-header", STYLES)
        self.assertIn("@media screen and (max-width: 440px)", STYLES)
        self.assertIn("min-height: 44px", STYLES)

    def test_search_and_hash_navigation_are_progressive_enhancements(self):
        self.assertIn("mat101-search-input", PAGE)
        self.assertIn("data-mat101-exercise", PAGE)
        self.assertIn("normalize('NFD')", SCRIPT)
        self.assertIn("activeTag", SCRIPT)
        self.assertIn("searchParams.set('notion'", SCRIPT)
        self.assertIn("initializeRootDiagrams", SCRIPT)
        self.assertIn("data-mat101-root-diagram", SCRIPT)
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
