"""Structural checks for the SHA-1/SHA-256 certificate-signature article."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
POST = ROOT / "_posts" / "2026-07-27-sha1-sha256-certificate-signatures.md"
STYLES = ROOT / "assets" / "main.scss"
SOURCE_EXCERPTS = ROOT / "assets" / "images" / "source-excerpts"


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

    def test_advanced_extensions_remain_conceptually_separated(self) -> None:
        self.assertIn("Length extension and why HMAC has two layers", self.text)
        self.assertIn("Bitcoin: hashing and signing are still different jobs", self.text)
        self.assertIn("What an ideal quantum computer would change", self.text)
        self.assertIn("This is a repeated preimage-style threshold search, not a birthday collision search", self.text)
        self.assertIn("SHA-256 itself is still not the signature", self.text)

    def test_official_sha256_test_vector_is_complete(self) -> None:
        digest = (
            "ba7816bf8f01cfea414140de5dae2223"
            "\n  b00361a396177a9cb410ff61f20015ad"
        )
        self.assertIn(digest, self.text)

    def test_primary_sources_are_linked_at_the_relevant_claims(self) -> None:
        required_links = (
            "fips180-4.pdf#page=14",
            "fips180-4.pdf#page=26",
            "rfc8017.html#section-8.2",
            "rfc5280.html#section-4.1",
            "rfc2104.html#section-2",
            "developer.bitcoin.org/reference/block_chain.html#block-headers",
            "secg.org/sec1-v2.pdf#page=51",
            "secg.org/sec2-v2.pdf#page=13",
            "bips.dev/340",
            "shattered.io/static/shattered.pdf",
            "support.apple.com/en-gb/103769",
        )
        for link in required_links:
            with self.subTest(link=link):
                self.assertIn(link, self.text)

    def test_only_essential_primary_sources_receive_previews(self) -> None:
        self.assertEqual(self.text.count('<figure class="source-facsimile '), 5)
        self.assertEqual(self.text.count("<figcaption><strong>Source excerpt.</strong>"), 5)
        self.assertEqual(self.text.count("Yellow highlighting added."), 5)
        self.assertEqual(self.text.count('class="source-facsimile-link"'), 5)

        preview_sources = (
            "csrc.nist.gov/Projects/hash-functions#security-strengths",
            "shattered.io/static/shattered.pdf#page=2",
            "rfc-editor.org/rfc/rfc8017.html#section-9.2",
            "rfc-editor.org/rfc/rfc5280.html#section-4.1",
            "support.apple.com/en-gb/103769",
        )
        for source in preview_sources:
            with self.subTest(source=source):
                self.assertIn(source, self.text)

        excerpt_files = (
            "sha256-nist-security-strengths.png",
            "sha1-shattered-abstract.png",
            "sha256-rfc8017-encoding.png",
            "sha256-rfc5280-certificate.png",
            "sha256-apple-tls-requirement.png",
        )
        for file_name in excerpt_files:
            with self.subTest(file_name=file_name):
                path = SOURCE_EXCERPTS / file_name
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 20_000)
                self.assertIn(file_name, self.text)

    def test_source_previews_have_responsive_book_like_styles(self) -> None:
        styles = STYLES.read_text(encoding="utf-8")
        required_rules = (
            ".source-facsimile-viewport",
            ".source-facsimile-link:focus-visible",
            ".source-facsimile img",
            ".source-facsimile--paper",
            ".source-facsimile--wide .source-facsimile-link",
            "@media (max-width: 560px)",
        )
        for rule in required_rules:
            with self.subTest(rule=rule):
                self.assertIn(rule, styles)

    def test_self_signed_certificate_is_not_equated_with_trust(self) -> None:
        self.assertIn("does **not** independently prove", self.text)
        self.assertIn("trust decision", self.text)

    def test_ecdsa_is_defined_before_bitcoin_uses_it(self) -> None:
        definition = self.text.index("### ECDSA in one calculation")
        bitcoin_use = self.text.index("Bitcoin historically—and still for many outputs—uses")
        self.assertLess(definition, bitcoin_use)
        self.assertIn("Q=dG", self.text)
        self.assertIn(r"s=k^{-1}(z+rd)\bmod n", self.text)
        self.assertIn(r"u_1G+u_2Q", self.text)
        self.assertIn(
            "**ECDSA is the signature scheme; `secp256k1` is the domain-parameter choice",
            self.text,
        )

    def test_acronyms_and_jargon_are_defined_contextually(self) -> None:
        required_expansions = (
            "SHA means **Secure Hash Algorithm**",
            "National Institute of Standards and Technology",
            "Federal Information Processing Standard",
            "RSA—named after Ron Rivest, Adi Shamir and Leonard Adleman",
            "**ASN.1** `DigestInfo`",
            "**Abstract Syntax Notation One**",
            "**PKCS #1**",
            "**Request for Comments**",
            "**Distinguished Encoding Rules**",
            "**Transport Layer Security**",
            "**Internet Printing Protocol**",
            "**Hash-based Message Authentication Code**",
            "**Elliptic Curve Digital Signature Algorithm**",
            "**Standards for Efficient Cryptography**",
            "**Bitcoin Improvement Proposal**",
        )
        for expansion in required_expansions:
            with self.subTest(expansion=expansion):
                self.assertIn(expansion, self.text)

    def test_interactive_definitions_have_valid_separate_targets(self) -> None:
        targets = set(re.findall(r'id="(definition-[^"]+)"', self.text))
        references = re.findall(
            r'<a class="(?:notation|concept)-ref" '
            r'href="#([^"]+)" data-definition="([^"]+)"',
            self.text,
        )

        self.assertGreaterEqual(len(references), 20)
        for target, definition in references:
            with self.subTest(target=target):
                self.assertIn(target, targets)
                self.assertGreaterEqual(len(definition.split()), 4)

        for match in re.finditer(
            r'<span id="(definition-[^"]+)" class="definition-target">(.*?)</span>',
            self.text,
            flags=re.DOTALL,
        ):
            target, body = match.groups()
            with self.subTest(self_link=target):
                self.assertNotIn(f'href="#{target}"', body)

    def test_math_and_code_delimiters_are_balanced(self) -> None:
        self.assertEqual(self.text.count("$$") % 2, 0)
        self.assertEqual(self.text.count("```") % 2, 0)

    def test_no_bare_pkcs_identifier_can_trigger_markdown_emphasis(self) -> None:
        bare = re.compile(r"(?<!`)RSASSA-PKCS1-v1_5(?!`)")
        self.assertIsNone(bare.search(self.text))


if __name__ == "__main__":
    unittest.main()
