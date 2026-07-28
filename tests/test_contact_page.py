from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ABOUT = (ROOT / "about.md").read_text()
MAT101 = (ROOT / "mat101-exercises.md").read_text()
CONTACT_FORM = (
    ROOT / ".github/ISSUE_TEMPLATE/site-contact.yml"
).read_text()
STYLES = (ROOT / "assets/main.scss").read_text()


class ContactPageTests(unittest.TestCase):
    def test_about_page_offers_two_explicit_contact_routes(self):
        self.assertIn("title: About & contact", ABOUT)
        self.assertIn('id="contact"', ABOUT)
        self.assertIn("mat101-correction.yml", ABOUT)
        self.assertIn("site-contact.yml", ABOUT)
        self.assertIn("publicly readable on GitHub", ABOUT)
        self.assertIn("requires a free GitHub account", ABOUT)
        self.assertNotIn("quantum theory and related mathematics", ABOUT)

    def test_general_contact_form_is_public_and_actionable(self):
        self.assertIn("Type of request", CONTACT_FORM)
        self.assertIn("Attribution, licensing, or removal request", CONTACT_FORM)
        self.assertIn("Message", CONTACT_FORM)
        self.assertIn("publicly visible", CONTACT_FORM)

    def test_mat101_rights_link_targets_contact_section(self):
        self.assertIn("'/about/#contact'", MAT101)

    def test_contact_routes_have_responsive_and_accessible_styles(self):
        self.assertIn(".contact-routes", STYLES)
        self.assertIn("min-height: 44px", STYLES)
        self.assertIn("@media screen and (max-width: 640px)", STYLES)


if __name__ == "__main__":
    unittest.main()
