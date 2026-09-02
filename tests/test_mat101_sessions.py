import importlib.util
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "mat101-sessions.md").read_text(encoding="utf-8")
DATA_TEXT = (ROOT / "_data" / "mat101_sessions.json").read_text(encoding="utf-8")
DATA = json.loads(DATA_TEXT)
SESSION_DIR = ROOT / "_mat101_sessions"
SESSION_FILES = sorted(SESSION_DIR.glob("[0-9][0-9]-*.md"))
HEAD = (ROOT / "_includes" / "head-custom.html").read_text(encoding="utf-8")
STYLES = (ROOT / "assets" / "main.scss").read_text(encoding="utf-8")
SCRIPT = (ROOT / "assets" / "js" / "mat101-sessions.js").read_text(
    encoding="utf-8"
)
CONFIG = (ROOT / "_config.yml").read_text(encoding="utf-8")

GENERATOR_SPEC = importlib.util.spec_from_file_location(
    "build_mat101_sessions", ROOT / "scripts" / "build_mat101_sessions.py"
)
GENERATOR = importlib.util.module_from_spec(GENERATOR_SPEC)
assert GENERATOR_SPEC.loader is not None
GENERATOR_SPEC.loader.exec_module(GENERATOR)

WORKBOOK_TEXT = "\n\n".join(
    f"""## Séance {number} — Séance {number}

### À savoir faire

- Première compétence.
- Deuxième compétence.

### Parcours

- Poly p. {number}.

### Ticket

Question {number}."""
    for number in range(1, 20)
)
SCHEDULE_TEXT = "\n".join(
    f"| {number} | {'**à fixer avant la coupure**' if number >= 18 else f'mar. {number} sept.'} | 1 | Séance | 1 |"
    for number in range(1, 20)
)


class Mat101SessionsTests(unittest.TestCase):
    def test_index_contains_exactly_nineteen_ordered_sessions(self):
        self.assertEqual(len(DATA), 19)
        self.assertEqual([item["number"] for item in DATA], list(range(1, 20)))
        self.assertEqual(len(SESSION_FILES), 19)
        self.assertEqual(
            [int(path.name[:2]) for path in SESSION_FILES], list(range(1, 20))
        )
        self.assertEqual(len({item["url"] for item in DATA}), 19)
        self.assertEqual(
            DATA[-1]["url"], "/mat101/seances/19-analyse-synthese-revision/"
        )

    def test_every_detail_page_contains_only_allowlisted_student_sections(self):
        required = {"À savoir faire", "Parcours", "Ticket"}
        allowed = required | {
            "Activité",
            "Contrôle rapide",
            "Contrôle formatif",
            "Révision mixte",
        }
        for number, path in enumerate(SESSION_FILES, start=1):
            text = path.read_text(encoding="utf-8")
            headings = set(re.findall(r"^## (.+?)\s*$", text, re.MULTILINE))
            self.assertIn(f"mat101_session_number: {number}", text)
            self.assertIn("Parcours étudiant", text)
            self.assertIn('class="mat101-session-content"', text)
            self.assertTrue(required <= headings, path.name)
            self.assertTrue(headings <= allowed, f"{path.name}: {headings - allowed}")

    def test_public_output_contains_no_instructor_or_assessment_material(self):
        public_text = "\n".join(
            [PAGE, DATA_TEXT]
            + [path.read_text(encoding="utf-8") for path in SESSION_FILES]
        ).casefold()
        forbidden = (
            "fiche enseignant",
            "réponses et corrections",
            "préparation matérielle",
            "déroulé minute par minute",
            "plan de tableau",
            "erreurs fréquentes",
            "après la séance",
            "correction complète",
            "passation",
            "mock-cc1-key",
            "quiz-a-complexes-base-key",
            "quiz-b-complexes-synthese-key",
            "quiz-c-ensembles-logique-key",
        )
        for marker in forbidden:
            self.assertNotIn(marker, public_text)
        self.assertFalse(
            (
                ROOT
                / "assets"
                / "documents"
                / "mat101"
                / "MAT101-IMA02-guide-professeur.pdf"
            ).exists()
        )

    def test_generator_rejects_a_new_unreviewed_public_section(self):
        modified = WORKBOOK_TEXT.replace(
            "### Ticket\n", "### Corrigé\n\nContenu privé.\n\n### Ticket\n", 1
        )
        with self.assertRaisesRegex(ValueError, "unexpected public sections"):
            GENERATOR.parse_workbook(modified)

    def test_schedule_uncertainty_is_visible_and_bounded(self):
        parsed = GENERATOR.parse_schedule(SCHEDULE_TEXT)
        self.assertEqual(
            [number for number, row in parsed.items() if row["scheduleConfirmed"]],
            list(range(1, 18)),
        )
        self.assertEqual(
            [number for number, row in parsed.items() if not row["scheduleConfirmed"]],
            [18, 19],
        )
        self.assertTrue(
            all(
                row["dateLabel"] == "Date et salle à confirmer"
                for number, row in parsed.items()
                if number in {18, 19}
            )
        )
        self.assertIn("17 + 2", PAGE)
        self.assertIn("La date et la salle des séances 18 et 19", PAGE)

    def test_hub_exposes_fast_search_filters_and_student_cards(self):
        self.assertIn("data-mat101-course", PAGE)
        self.assertIn("data-mat101-session-card", PAGE)
        self.assertIn("mat101-session-search-input", PAGE)
        self.assertIn('data-mat101-session-filter="complexes"', PAGE)
        self.assertIn('data-mat101-session-filter="langage"', PAGE)
        self.assertIn('data-mat101-session-filter="synthese"', PAGE)
        self.assertIn("session.skillsPlain", PAGE)
        self.assertIn("mat101-sessions.js", HEAD)
        self.assertIn("cards.length !== 19", SCRIPT)
        self.assertIn(".mat101-session-grid", STYLES)
        self.assertIn(".mat101-session-content", STYLES)

    def test_mat101_is_the_single_global_entry_and_pages_cross_link(self):
        header_block = CONFIG.split("header_pages:", 1)[1].split("plugins:", 1)[0]
        self.assertIn("- mat101-sessions.md", header_block)
        self.assertNotIn("- mat101-exercises.md", header_block)
        self.assertRegex(PAGE, r"(?m)^title: MAT101$")
        exercises = (ROOT / "mat101-exercises.md").read_text(encoding="utf-8")
        self.assertIn("Voir les 19 séances", exercises)
        self.assertIn("'/mat101/seances/' | relative_url", exercises)

    def test_student_pdf_and_stable_collection_routes_are_present(self):
        workbook = (
            ROOT
            / "assets"
            / "documents"
            / "mat101"
            / "parcours-19-seances-mat101-ima02.pdf"
        )
        self.assertTrue(workbook.is_file())
        self.assertTrue(workbook.read_bytes().startswith(b"%PDF"))
        self.assertIn("mat101_sessions:", CONFIG)
        self.assertIn("permalink: /mat101/seances/:name/", CONFIG)
        for item in DATA:
            self.assertRegex(
                item["url"], rf"^/mat101/seances/{item['number']:02d}-[^/]+/$"
            )


if __name__ == "__main__":
    unittest.main()
