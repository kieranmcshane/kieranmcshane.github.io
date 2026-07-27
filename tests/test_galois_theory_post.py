"""Structural and mathematical checks for the Galois-theory article."""

from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
POST = ROOT / "_posts" / "2026-07-27-galois-theory-without-detours.md"
HEAD = ROOT / "_includes" / "head-custom.html"
NAVIGATION = ROOT / "assets" / "js" / "correction-navigation.js"
STYLES = ROOT / "assets" / "main.scss"
IMAGES = (
    ROOT / "assets" / "images" / "galois-v4-correspondence.svg",
    ROOT / "assets" / "images" / "galois-a4-correspondence.svg",
)


class GaloisTheoryPostTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = POST.read_text(encoding="utf-8")

    def test_front_matter_and_scope(self) -> None:
        self.assertIn('title: "Galois Theory Without Detours"', self.text)
        self.assertIn("math: true", self.text)
        self.assertIn("Fundamental theorem of finite Galois theory", self.text)
        body = self.text.split("---", 2)[-1]
        prose = re.sub(r"<[^>]+>", " ", body)
        words = re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)*|\d+", prose)
        self.assertGreaterEqual(len(words), 10_000)
        self.assertLessEqual(len(words), 15_000)

    def test_running_example_is_complete(self) -> None:
        required = (
            r"L=\mathbb Q(\sqrt2,\sqrt3)",
            r"L^{\langle\sigma\rangle}",
            r"\mathbb Q(\sqrt6)",
            r"G=\operatorname{Gal}(L/\mathbb Q)",
            r"\cong C_2\times C_2",
        )
        for expression in required:
            with self.subTest(expression=expression):
                self.assertIn(expression, self.text)

    def test_markdown_tables_do_not_use_raw_absolute_value_bars(self) -> None:
        table_lines = (
            line for line in self.text.splitlines() if line.startswith("|")
        )
        for line in table_lines:
            with self.subTest(line=line):
                self.assertNotIn("$|", line)
                self.assertNotIn("|$", line)
                self.assertNotIn(r"$\{", line)
        self.assertIn(
            r"| Subgroup $H\leq G$ | Order $\lvert H\rvert$ "
            r"| Fixed field $L^H$ | Degree $[L^H:\mathbb Q]$ |",
            self.text,
        )
        self.assertEqual(self.text.count(r"| $\lbrace 1\rbrace$ |"), 3)

    def test_interactive_table_of_contents_is_wired_for_long_reading(self) -> None:
        links = re.findall(r'<a href="#([^"]+)">', self.text)
        self.assertGreaterEqual(len(links), 16)
        self.assertEqual(len(links), len(set(links)))
        for target in (
            "the-destination",
            "proof-core-i-independence-of-homomorphisms",
            "decoding-an-a4-lattice",
            "comprehension-checks-with-solutions",
            "further-reading",
        ):
            with self.subTest(target=target):
                self.assertIn(target, links)

        self.assertIn('data-section-navigation', self.text)
        self.assertIn("longform-toc-details", self.text)
        self.assertIn(
            "page.url == '/2026/07/27/galois-theory-without-detours/'",
            HEAD.read_text(encoding="utf-8"),
        )
        navigation = NAVIGATION.read_text(encoding="utf-8")
        self.assertIn("configureResponsiveLongformIndex", navigation)
        self.assertIn("initializeSectionHighlighting(article, navigation)", navigation)
        self.assertIn(
            "document.getElementById(link.getAttribute('href').slice(1))",
            navigation,
        )
        styles = STYLES.read_text(encoding="utf-8")
        self.assertIn(".longform-reading-layout", styles)
        self.assertIn(".longform-toc a[aria-current=\"location\"]", styles)

    def test_proof_core_contains_required_lemmas(self) -> None:
        self.assertIn("Dedekind independence lemma", self.text)
        self.assertIn("Artin's fixed-field theorem", self.text)
        self.assertIn(r"[L:L^H]=|H|", self.text)
        self.assertIn(r"L^{\operatorname{Gal}(L/E)}=E", self.text)
        self.assertIn(r"\operatorname{Gal}(L/L^H)=H", self.text)

    def test_normal_subgroup_statement_and_quotient(self) -> None:
        self.assertIn(r"g(E)=g(L^H)=L^{gHg^{-1}}", self.text)
        self.assertIn(r"\operatorname{Gal}(E/K)\cong G/H", self.text)
        self.assertIn(r"H\trianglelefteq G", self.text)

    def test_a4_lattice_counts_and_degrees(self) -> None:
        self.assertIn("eight $3$-cycles", self.text)
        self.assertIn("three double transpositions", self.text)
        self.assertIn(r"\frac82=4", self.text)
        self.assertIn("| $C_2$ | $3$ | $2$ | $6$ |", self.text)
        self.assertIn("| $C_3$ | $4$ | $3$ | $4$ |", self.text)
        self.assertIn(r"A_4/V", self.text)

    def test_erroneous_polynomial_is_corrected(self) -> None:
        self.assertIn(r"X^4+8X^2+12", self.text)
        self.assertIn(r"(X^2+2)(X^2+6)", self.text)
        self.assertIn("degree $4$ and Galois group $V_4$, not $A_4$", self.text)

    def test_finite_and_infinite_theorems_are_distinguished(self) -> None:
        self.assertIn("closed** subgroups under the Krull topology", self.text)
        self.assertIn("stacks.math.columbia.edu/tag/0BML", self.text)

    def test_math_and_code_delimiters_are_balanced(self) -> None:
        self.assertEqual(self.text.count("$$") % 2, 0)
        self.assertEqual(self.text.count("```") % 2, 0)
        self.assertIsNone(re.search(r"(?<!\\)\$\$\$(?!\$)", self.text))

    def test_diagrams_exist_and_are_valid_svg(self) -> None:
        self.assertEqual(
            self.text.count('class="post-figure-media post-figure-media-wide"'),
            2,
        )
        for image in IMAGES:
            with self.subTest(image=image.name):
                self.assertTrue(image.exists())
                root = ET.parse(image).getroot()
                self.assertTrue(root.tag.endswith("svg"))
                self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}title"))
                self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}desc"))


if __name__ == "__main__":
    unittest.main()
