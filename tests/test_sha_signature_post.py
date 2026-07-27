"""Structural checks for the SHA-1/SHA-256 certificate-signature article."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
POST = ROOT / "_posts" / "2026-07-27-sha1-sha256-certificate-signatures.md"


class ShaSignaturePostTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = POST.read_text(encoding="utf-8")

    def test_front_matter_enables_math(self) -> None:
        self.assertIn("math: true", self.text)
        self.assertIn("title: \"From SHA-1 to SHA-256 in a Certificate Signature\"", self.text)

    def test_hashing_and_signing_are_distinguished(self) -> None:
        self.assertIn("Hashing is not signing", self.text)
        self.assertIn("SHA-256 is a hash function, not a signature algorithm", self.text)
        self.assertIn("signature primitive", self.text)

    def test_birthday_bound_is_derived(self) -> None:
        self.assertIn(r"q_{1/2}", self.text)
        self.assertIn(r"\sqrt{2\log 2}", self.text)
        self.assertIn(r"2^{n/2}", self.text)

    def test_primary_sources_are_linked_at_the_relevant_claims(self) -> None:
        required_links = (
            "fips180-4.pdf#page=14",
            "fips180-4.pdf#page=26",
            "rfc8017.html#section-8.2",
            "rfc5280.html#section-4.1",
            "shattered.io/static/shattered.pdf",
            "support.apple.com/en-gb/103769",
        )
        for link in required_links:
            with self.subTest(link=link):
                self.assertIn(link, self.text)

    def test_self_signed_certificate_is_not_equated_with_trust(self) -> None:
        self.assertIn("does **not** independently prove", self.text)
        self.assertIn("trust decision", self.text)

    def test_math_and_code_delimiters_are_balanced(self) -> None:
        self.assertEqual(self.text.count("$$") % 2, 0)
        self.assertEqual(self.text.count("```") % 2, 0)

    def test_no_bare_pkcs_identifier_can_trigger_markdown_emphasis(self) -> None:
        bare = re.compile(r"(?<!`)RSASSA-PKCS1-v1_5(?!`)")
        self.assertIsNone(bare.search(self.text))


if __name__ == "__main__":
    unittest.main()
