import importlib.util
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "mat101-sessions.md").read_text(encoding="utf-8")
INFORMATIONS = (ROOT / "_includes" / "mat101-informations.html").read_text(encoding="utf-8")
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
        required = {"À savoir faire", "Parcours", "Questions"}
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
            self.assertRegex(text, r"(?m)^layout: mat101$")
            self.assertNotIn('class="mat101-kicker"', text)
            self.assertNotIn("<strong>Parcours étudiant</strong>", text)
            self.assertIn('class="mat101-session-content"', text)
            self.assertTrue(required <= headings, path.name)
            self.assertTrue(headings <= allowed, f"{path.name}: {headings - allowed}")
            if number == 19:
                self.assertIn(
                    "[construction de R par les suites de Cauchy](/mat101/exercices/#facultatif)",
                    text,
                )

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

    def test_session_status_supports_interro_overrides(self):
        badge, css_class, detail = GENERATOR.session_status(
            {
                "number": 10,
                "scheduleConfirmed": True,
                "kind": "interro",
                "statusBadge": "Interro",
                "statusDetail": "1 h · tiers temps 1 h 20",
            }
        )
        self.assertEqual(badge, "Interro")
        self.assertEqual(css_class, " is-interro")
        self.assertEqual(detail, "1 h · tiers temps 1 h 20")

    def test_skill_markup_turns_backticks_into_mathjax_html(self):
        rendered = GENERATOR.skill_to_html(
            "Calculer `\\bar z`, `|z|` et poser `z=x+iy`"
        )
        self.assertIn('<span class="math inline">\\(\\bar z\\)</span>', rendered)
        self.assertIn('<span class="math inline">\\(|z|\\)</span>', rendered)
        self.assertIn('<span class="math inline">\\(z=x+iy\\)</span>', rendered)
        self.assertNotIn("`", rendered)

    def test_session_detail_pages_render_competency_math_with_mathjax_markup(self):
        session_one = (SESSION_DIR / "01-forme-algebrique.md").read_text(encoding="utf-8")
        self.assertIn(
            '<span class="math inline">$N⊂Z⊂Q⊂R⊂C$</span>',
            session_one,
        )
        self.assertNotIn("`N⊂Z⊂Q⊂R⊂C`", session_one)
        self.assertNotRegex(
            session_one,
            r"## À savoir faire[\s\S]*?`[^`]+`",
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
        self.assertIn('class="mat101-session-date-state is-pending"', PAGE)
        self.assertIn("{{ session.dateLabel }}", PAGE)
        self.assertNotIn("17 + 2", PAGE)
        self.assertNotIn("La date et la salle des séances 18 et 19 restent à confirmer.", PAGE)

    def test_hub_intro_is_compact(self):
        self.assertRegex(PAGE, r"(?m)^layout: mat101$")
        self.assertIn('<h1>Séances MAT101</h1>', PAGE)
        self.assertIn('id="informations"', INFORMATIONS)
        self.assertIn("Informations", INFORMATIONS)
        self.assertIn("Partiel prévu la semaine du 20 octobre.", INFORMATIONS)
        self.assertIn("mat101-informations.html", PAGE)
        self.assertIn("Note UE", INFORMATIONS)
        self.assertIn(
            r"\max\!\left(E,\ 0{,}4E + 0{,}3\,CC_1 + 0{,}3\,CC_2\right)",
            INFORMATIONS,
        )
        self.assertNotIn(r"\text{Note UE}=", INFORMATIONS)
        self.assertIn("Tutorat", INFORMATIONS)
        self.assertIn("Contrôle continu", INFORMATIONS)
        self.assertIn("12 h 30 à 13 h 30", INFORMATIONS)
        self.assertIn(".mat101-informations", STYLES)
        self.assertNotIn('class="mat101-page-links"', PAGE)
        self.assertNotIn("Feuille de route", PAGE)
        self.assertNotIn("parcours-19-seances-mat101-ima02.pdf", PAGE)
        self.assertNotIn("19 séances pour progresser en MAT101", PAGE)
        self.assertNotIn(
            "Retrouvez pour chaque cours-TD les compétences à acquérir",
            PAGE,
        )
        self.assertNotIn("Parcours chronologique", PAGE)
        self.assertNotIn("Retrouver une séance", PAGE)
        self.assertIn('<h2 id="mat101-session-browser-title">Séances</h2>', PAGE)
        self.assertNotIn("Choisir une séance", PAGE)
        self.assertNotIn('class="mat101-course-hero"', PAGE)
        self.assertNotIn('class="mat101-course-status"', PAGE)
        self.assertNotIn('class="mat101-stats"', PAGE)

    def test_session_ten_is_marked_as_an_interro(self):
        session = next(item for item in DATA if item["number"] == 10)
        self.assertEqual(session["kind"], "interro")
        self.assertEqual(session["title"], "Interro · nombres complexes")
        self.assertEqual(session["block"], "langage")
        self.assertEqual(session["dateIso"], "2026-09-29")
        self.assertEqual(session["status"], "past")
        self.assertEqual(session["statusBadge"], "Séance faite")
        self.assertEqual(session["statusDetail"], "1 h · tiers temps 1 h 20")
        self.assertEqual(session["room"], "DLST E201")
        self.assertIn("interro", session["search"])
        self.assertNotIn("exercice 2.1", session["search"])
        self.assertIn("séances 1 à 8", session["search"])

        page = (SESSION_DIR / "10-ensembles-appartenance-inclusion.md").read_text(
            encoding="utf-8"
        )
        self.assertIn('class="mat101-session-detail-status is-past"', page)
        self.assertIn("Séance faite", page)
        self.assertIn("1 h · tiers temps 1 h 20", page)
        self.assertIn("DLST E201", page)
        self.assertIn("<strong>Interro.</strong>", page)
        self.assertIn("séances 1 à 8", page)

    def test_public_schedule_has_rooms_past_tone_extra_session_and_no_partiel_td(self):
        by_number = {item["number"]: item for item in DATA}
        rooms_by_weekday = {1: "DLST E201", 3: "DLST B007", 4: "DLST D104"}
        times_by_weekday = {
            1: "09:45–11:15",
            3: "13:30–15:00",
            4: "15:15–16:45",
        }
        for item in DATA:
            iso = item.get("dateIso")
            if item["number"] == 19:
                self.assertIsNone(iso)
                self.assertFalse(item["scheduleConfirmed"])
                self.assertEqual(item["status"], "pending")
                self.assertIsNone(item["room"])
                self.assertEqual(item["dateLabel"], "Date et salle à confirmer")
                continue
            self.assertIsNotNone(iso, item["number"])
            self.assertFalse(
                "2026-10-19" <= iso <= "2026-10-25",
                f"session {item['number']} implies TD during the partiel week",
            )
            if iso < "2026-10-05":
                self.assertEqual(item["status"], "past")
                self.assertEqual(item["statusBadge"], "Séance faite")
            else:
                self.assertEqual(item["status"], "upcoming")
                self.assertEqual(item["statusBadge"], "À venir")
            if item["number"] != 18:
                weekday = GENERATOR.date.fromisoformat(iso).weekday()
                self.assertEqual(item["room"], rooms_by_weekday[weekday])
                self.assertEqual(item["timeLabel"], times_by_weekday[weekday])

        extra = by_number[18]
        self.assertEqual(extra["dateIso"], "2026-09-23")
        self.assertEqual(extra["dateLabel"], "mer. 23 sept. 2026")
        self.assertEqual(extra["timeLabel"], "13:30–15:00")
        self.assertEqual(extra["room"], "DLST E204")
        self.assertTrue(extra["scheduleConfirmed"])
        self.assertEqual(extra["status"], "past")

        self.assertEqual(by_number[1]["status"], "past")
        self.assertEqual(by_number[13]["dateIso"], "2026-10-06")
        self.assertEqual(by_number[13]["status"], "upcoming")
        self.assertEqual(by_number[13]["room"], "DLST E201")

        session_one = (SESSION_DIR / "01-forme-algebrique.md").read_text(encoding="utf-8")
        self.assertIn("mat101-session-page is-past", session_one)
        self.assertIn("Séance faite", session_one)
        self.assertIn("DLST E201", session_one)
        self.assertIn("09:45–11:15", session_one)
        self.assertIn("N⊂Z⊂Q⊂R⊂C", session_one)
        self.assertNotIn("plan complexe", session_one.casefold())

        session_eighteen = (SESSION_DIR / "18-recurrence.md").read_text(encoding="utf-8")
        self.assertIn("mer. 23 sept. 2026", session_eighteen)
        self.assertIn("DLST E204", session_eighteen)
        self.assertIn("mat101-session-page is-past", session_eighteen)
        self.assertNotIn("Date et salle à confirmer", session_eighteen)

        session_nineteen = (SESSION_DIR / "19-analyse-synthese-revision.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("mat101-session-page is-pending", session_nineteen)
        self.assertIn("Date et salle à confirmer", session_nineteen)
        self.assertNotIn("DLST", session_nineteen)

        upcoming = (SESSION_DIR / "13-assertions-variables.md").read_text(encoding="utf-8")
        self.assertIn("mat101-session-page is-upcoming", upcoming)
        self.assertIn("À venir", upcoming)
        self.assertIn("DLST E201", upcoming)

        self.assertIn("session.room", PAGE)
        self.assertIn('session.status == "past"', PAGE)
        self.assertIn('session.status == "upcoming"', PAGE)
        self.assertIn('class="mat101-session-date-state is-past"', PAGE)
        self.assertIn('class="mat101-session-date-state is-upcoming"', PAGE)
        self.assertIn('class="mat101-session-date-state is-pending"', PAGE)
        self.assertIn(".mat101-session-card.is-past", STYLES)
        self.assertIn(".mat101-session-card.is-upcoming", STYLES)
        self.assertIn("background: #f3f5f6;", STYLES)
        self.assertIn("border-color: #8fc9d0;", STYLES)
        self.assertIn("Partiel prévu la semaine du 20 octobre.", INFORMATIONS)
        self.assertIn("semaine du 19 octobre", INFORMATIONS)

        with self.assertRaisesRegex(ValueError, "partiel week"):
            GENERATOR.attach_public_schedule(
                {
                    "number": 16,
                    "dateLabel": "mar. 20 oct. 2026",
                    "scheduleConfirmed": True,
                    "search": "",
                }
            )

    def test_student_resources_are_linked_from_the_seances_page(self):
        resources = json.loads(
            (ROOT / "_data" / "mat101_resources.json").read_text(encoding="utf-8")
        )
        include = (ROOT / "_includes" / "mat101-resources.html").read_text(encoding="utf-8")
        archives = json.loads(
            (ROOT / "_data" / "mat101_archives.json").read_text(encoding="utf-8")
        )
        self.assertIn("include mat101-resources.html", PAGE)
        self.assertIn('id="documents"', include)
        self.assertIn("site.data.mat101_resources", include)
        self.assertIn('id="mat101-resources-title">Documents</h2>', include)
        self.assertNotIn("Afficher le corrigé", include)
        self.assertNotIn("corrige-exercices", include)
        self.assertNotIn("mat101_resources", (ROOT / "_data" / "mat101_archives.json").read_text())
        archive_files = [
            item.get("file")
            for group in archives["groups"]
            for item in group.get("items", [])
        ]
        self.assertEqual(
            sorted(archive_files),
            sorted(
                [
                    "ds1_2021_correction.pdf",
                    "partiel_2122_correction.pdf",
                    "MAT101_2020_CC1.pdf",
                    "MAT101_2020_CC1_corr.pdf",
                ]
            ),
        )

        items = [item for group in resources["groups"] for item in group["items"]]
        labels = [item["label"] for item in items]
        titles = [group["title"] for group in resources["groups"]]
        self.assertEqual(
            titles,
            [
                "Sujets d’interrogations",
                "Nombres complexes",
                "Fiche NAND (facultatif)",
            ],
        )
        self.assertEqual(
            labels,
            [
                "Bonus 1",
                "Bonus 2",
                "Bonus 3",
                "Interrogation du 2 octobre 2026",
                "Nombres complexes — 29 méthodes avec exemples corrigés",
                "De la logique à Tetris",
            ],
        )
        self.assertEqual(
            [item["file"] for item in items],
            [
                "interros/interrogation-bonus-1-sujet.pdf",
                "interros/interrogation-bonus-2-2026-09-22-sujet.pdf",
                "interros/interrogation-bonus-3-2026-09-29-sujet.pdf",
                "interros/interrogation-2026-10-02-sujet.pdf",
                "supports/nombres-complexes-29-methodes.pdf",
                "supports/fiche-nand.pdf",
            ],
        )
        for item in items:
            path = ROOT / "assets" / "documents" / "mat101" / item["file"]
            self.assertTrue(path.is_file(), item["file"])
            self.assertTrue(path.read_bytes().startswith(b"%PDF-"), item["file"])
            self.assertGreater(path.stat().st_size, 10_000, item["file"])
        self.assertIn(".mat101-course > .mat101-resources", STYLES)

    def test_planning_splits_eight_complex_sessions_and_eleven_language_sessions(self):
        complexes = [item for item in DATA if item["block"] == "complexes"]
        langage = [item for item in DATA if item["block"] == "langage"]
        self.assertEqual(len(complexes), 8)
        self.assertEqual(len(langage), 11)
        self.assertEqual([item["number"] for item in complexes], list(range(1, 9)))
        self.assertEqual([item["number"] for item in langage], list(range(9, 20)))
        self.assertEqual(DATA[8]["title"], "Géométrie et rédaction")
        self.assertEqual(DATA[18]["title"], "Analyse-synthèse et révision")
        self.assertIn('data-mat101-session-filter="complexes"', PAGE)
        self.assertIn('data-mat101-session-filter="langage"', PAGE)
        self.assertIn("Nombres complexes <span>8</span>", PAGE)
        self.assertIn("Ensembles et logique <span>11</span>", PAGE)
        self.assertNotIn('data-mat101-session-filter="synthese"', PAGE)

    def test_session_eleven_carries_describe_sets_content(self):
        session = next(item for item in DATA if item["number"] == 11)
        self.assertEqual(session["title"], "Décrire un ensemble")
        self.assertIn("extension, compréhension", session["search"])
        self.assertIn("exercice 2.1", session["search"])
        self.assertIn("exercice 2.3", session["search"])

    def test_hub_exposes_fast_search_filters_and_student_cards(self):
        self.assertIn("data-mat101-course", PAGE)
        self.assertIn("data-mat101-session-card", PAGE)
        self.assertIn("mat101-session-search-input", PAGE)
        self.assertIn('data-mat101-session-filter="complexes"', PAGE)
        self.assertIn('data-mat101-session-filter="langage"', PAGE)
        self.assertNotIn('data-mat101-session-filter="synthese"', PAGE)
        self.assertIn("session.skillsHtml", PAGE)
        self.assertIn("session.statusDetail", PAGE)
        self.assertIn('session.kind == "interro"', PAGE)
        self.assertIn("mat101-session-format", PAGE)
        self.assertNotIn("session.skillsPlain", PAGE)
        self.assertIn("page.layout == 'mat101'", HEAD)
        self.assertIn("mat101-mobile.js", HEAD)
        self.assertIn("mat101-sessions.js", HEAD)
        self.assertIn("cards.length !== 19", SCRIPT)
        self.assertIn(".mat101-session-grid", STYLES)
        self.assertIn(".mat101-library.mat101-course", STYLES)
        self.assertRegex(
            STYLES,
            r"body\.mat101-site \.mat101-library\.mat101-course \{\s*max-width: 1180px;",
        )
        self.assertRegex(
            STYLES,
            r"@media screen and \(min-width: 960px\)[\s\S]*?\.mat101-course \{\s*display: grid;",
        )
        self.assertRegex(
            STYLES,
            r"@media screen and \(min-width: 1100px\)[\s\S]*?grid-template-columns: repeat\(3, minmax\(0, 1fr\)\);",
        )
        self.assertIn(".mat101-session-content", STYLES)
        self.assertRegex(
            STYLES,
            r"@media screen and \(max-width: 700px\)[\s\S]*?\.mat101-session-card ul[\s\S]*?overflow-x: auto;",
        )
        self.assertRegex(
            STYLES,
            r"\.mat101-session-card mjx-container \{\s*display: inline;",
        )
        self.assertNotRegex(
            STYLES,
            r"\.mat101-session-card mjx-container \{[^}]*overflow-x: auto;",
        )
        self.assertIn(".mat101-swipe-hint", STYLES)

    def test_mat101_is_the_single_global_entry_and_pages_cross_link(self):
        header_block = CONFIG.split("header_pages:", 1)[1].split("plugins:", 1)[0]
        self.assertIn("- mat101-sessions.md", header_block)
        self.assertNotIn("- mat101-exercises.md", header_block)
        self.assertRegex(PAGE, r"(?m)^title: MAT101$")
        exercises = (ROOT / "mat101-exercises.md").read_text(encoding="utf-8")
        shell = (ROOT / "_includes" / "mat101-shell.html").read_text(encoding="utf-8")
        self.assertIn(">Séances</a>", shell)
        self.assertIn("'/mat101/seances/' | relative_url", shell)
        self.assertIn('href="#bibliotheque">103 exercices</a>', exercises)
        self.assertNotIn('href="#credits">', exercises)

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
