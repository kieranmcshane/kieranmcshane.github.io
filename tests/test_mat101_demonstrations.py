from __future__ import annotations

import json
import re
import runpy
import unittest
from html import unescape
from html.parser import HTMLParser
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

class StrictFragmentParser(HTMLParser):
    """Do not let browser error recovery hide unclosed/nested paragraphs."""

    def __init__(self):
        super().__init__()
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag == "p" and "p" in self.stack:
            raise AssertionError("Nested paragraph")
        if tag not in {"p", "span", "ol", "ul", "li", "strong"}:
            raise AssertionError(f"Unexpected tag: {tag}")
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag:
            raise AssertionError(f"Unbalanced closing tag: {tag}")


class Mat101DemonstrationsTests(unittest.TestCase):
    def demonstration(self, demo_id):
        return next(
            demo for chapter in DATA["chapters"]
            for demo in chapter["demonstrations"] if demo["id"] == demo_id
        )

    def test_fragments_have_balanced_html_without_nested_paragraphs(self):
        for chapter in DATA["chapters"]:
            for demo in chapter["demonstrations"]:
                for field in ("statementHtml", "proofHtml"):
                    with self.subTest(demo=demo["id"], field=field):
                        parser = StrictFragmentParser()
                        parser.feed(demo[field])
                        parser.close()
                        self.assertEqual(parser.stack, [])

    def test_generated_data_matches_the_source(self):
        source = runpy.run_path(str(ROOT / "scripts/build_mat101_demonstrations.py"))
        self.assertEqual(DATA, source["DEMONSTRATIONS"])
        self.assertIn("&lt;", source["m_inline"]("n<n_0"))
        self.assertIn("&amp;", source["m_display"](r"\begin{aligned}a&=b\end{aligned}"))

    def test_generalized_identity_preserves_factor_in_induction(self):
        proof = unescape(self.demonstration("3.38")["proofHtml"])
        self.assertIn(
            r"a(a-b)\sum_{k=0}^{n}a^{n-k}b^k+(a-b)b^{n+1}",
            proof,
        )
        self.assertNotIn(r"a^{n-k}b^k+b^{n+1}", proof)

    def test_statements_define_domains_and_avoid_invalid_small_n_expansions(self):
        for demo_id in ("3.37", "3.40"):
            self.assertIn(r"n\in\mathbb N^*", self.demonstration(demo_id)["statementHtml"])
        for demo_id in ("3.38", "3.40"):
            statement = self.demonstration(demo_id)["statementHtml"]
            self.assertIn(r"a,b\in\mathbb C", statement)
            self.assertNotIn(r"\cdots", statement)
            self.assertIn("a^0=b^0=1", statement)

    def test_boundedness_proof_handles_initial_rank_zero(self):
        proof = unescape(self.demonstration("4.13")["proofHtml"])
        self.assertIn(r"S=\{u_k\mid k\in\mathbb N,\ k<n_0\}", proof)
        self.assertIn("ensemble vide", proof)
        self.assertIn("finis et non vides", proof)

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

    def test_proposition_4_13_splits_bound_definitions_for_narrow_layouts(self):
        proposition = next(
            demo
            for chapter in DATA["chapters"]
            for demo in chapter["demonstrations"]
            if demo["id"] == "4.13"
        )
        self.assertIn("M=\\max", proposition["proofHtml"])
        self.assertIn("m=\\min", proposition["proofHtml"])
        self.assertNotIn("M=\\max\\bigl(S\\cup\\{\\ell+1\\}\\bigr),\\qquad m=", proposition["proofHtml"])


if __name__ == "__main__":
    unittest.main()
