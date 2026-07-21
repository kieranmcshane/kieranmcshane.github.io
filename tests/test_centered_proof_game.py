from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "play-centered-correlations.md").read_text()
SCRIPT = (ROOT / "assets/js/centered-correlation-game.js").read_text()
HEAD = (ROOT / "_includes/head-custom.html").read_text()
ARTICLE = (ROOT / "_posts/2026-07-17-centered-correlation-tensors-separability.md").read_text()


class CenteredProofGameTests(unittest.TestCase):
    def test_campaign_has_seven_missions_and_a_synthesis_boss(self):
        self.assertEqual(SCRIPT.count("id: '"), 7)
        self.assertIn("id: 'synthesis'", SCRIPT)
        self.assertIn("Mission 1 of 7", PAGE)

    def test_game_requires_neither_typing_nor_speaking(self):
        lowered = PAGE.lower()
        self.assertNotIn("<input", lowered)
        self.assertNotIn("<textarea", lowered)
        self.assertNotIn("microphone", lowered)
        self.assertIn("no typing or speaking", lowered)

    def test_fsrs_is_a_real_scheduler_not_a_label(self):
        self.assertIn("window.FSRS.fsrs", SCRIPT)
        self.assertIn("scheduler.next", SCRIPT)
        self.assertIn("request_retention: 0.9", SCRIPT)
        self.assertIn("ts-fsrs@5.4.1", HEAD)
        self.assertIn("page.url == '/play/centered-correlations/'", HEAD)

    def test_failure_state_and_persistent_campaign_are_present(self):
        self.assertIn("integrity -= 1", SCRIPT)
        self.assertIn("returning to this mission’s checkpoint", SCRIPT)
        self.assertIn("localStorage.setItem", SCRIPT)
        self.assertIn("localStorage.removeItem", SCRIPT)

    def test_core_mathematical_frontier_is_explicit(self):
        for phrase in (
            "projective norm = matrix nuclear norm",
            "every unfolding norm is bounded by the full projective norm",
            "one ensemble to generate all tensor orders",
        ):
            self.assertIn(phrase, SCRIPT)

    def test_article_links_to_game_and_game_links_back(self):
        self.assertIn("'/play/centered-correlations/'", ARTICLE)
        self.assertIn("'/2026/07/17/centered-correlation-tensors-separability/'", PAGE)

    def test_html_ids_are_unique(self):
        ids = re.findall(r'\bid="([^"]+)"', PAGE)
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
