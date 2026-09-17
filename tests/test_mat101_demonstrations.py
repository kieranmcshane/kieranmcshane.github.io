from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "_data/mat101_demonstrations.json").read_text())
PAGE = (ROOT / "mat101-demonstrations.md").read_text()
SHELL = (ROOT / "_includes/mat101-shell.html").read_text()
STYLES = (ROOT / "assets/main.scss").read_text()
BUILDER = (ROOT / "scripts/build_mat101_demonstrations.py").read_text()

EXPECTED_IDS = [
    "1.3",
    "1.14",
    "1.18",
    "3.36",
    "3.37",
    "3.38",
    "3.40",
    "4.13",
    "4.14",
]


class Mat101DemonstrationsTests(unittest.TestCase):
    def test_data_contains_nine_essential_demonstrations(self):
        demos = [
            demo
            for chapter in DATA["chapters"]
            for demo in chapter["demonstrations"]
        ]
        self.assertEqual(len(demos), 9)
        self.assertEqual([demo["id"] for demo in demos], EXPECTED_IDS)

    def test_chapter_two_has_no_demonstrations(self):
        chapter_two = next(ch for ch in DATA["chapters"] if ch["number"] == "2")
        self.assertEqual(chapter_two["demonstrations"], [])
        self.assertIn("emptyMessage", chapter_two)

    def test_every_demonstration_has_statement_and_proof_html(self):
        for chapter in DATA["chapters"]:
            for demo in chapter["demonstrations"]:
                self.assertTrue(demo["statementHtml"].strip())
                self.assertTrue(demo["proofHtml"].strip())
                self.assertIn(demo["kind"], {"proposition", "theorem"})
                self.assertRegex(demo["label"], r"^(Proposition|Théorème) ")

    def test_page_and_navigation_reference_demonstrations(self):
        self.assertIn("permalink: /mat101/demonstrations/", PAGE)
        self.assertIn("site.data.mat101_demonstrations.chapters", PAGE)
        self.assertIn("/mat101/demonstrations/", SHELL)
        self.assertIn("Démonstrations", SHELL)
        self.assertIn("mat101-demonstrations", PAGE)
        self.assertIn("mat101-demonstrations", STYLES)

    def test_builder_script_writes_the_data_file(self):
        self.assertIn("_data/mat101_demonstrations.json", BUILDER)
        self.assertRegex(BUILDER, r'"id": "1\.3"')
        self.assertRegex(BUILDER, r'"id": "4\.14"')

    def test_theorem_1_14_statement_does_not_concatenate_latex_commands(self):
        theorem = next(
            demo
            for chapter in DATA["chapters"]
            for demo in chapter["demonstrations"]
            if demo["id"] == "1.14"
        )
        self.assertNotIn("\\qquadz_2", theorem["statementHtml"])
        self.assertIn("\\qquad z_2", theorem["statementHtml"])


if __name__ == "__main__":
    unittest.main()
