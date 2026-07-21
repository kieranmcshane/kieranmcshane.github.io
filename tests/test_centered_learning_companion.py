from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "explain-centered-correlations.md").read_text()
SCRIPT = (ROOT / "assets/js/centered-correlation-explain.js").read_text()
LEAN = (ROOT / "proofs/Proofs/CenteredCorrelationLearn.lean").read_text()


class CenteredLearningCompanionTests(unittest.TestCase):
    def test_five_stage_click_only_path_is_present(self):
        self.assertIn('aria-valuemax="5"', PAGE)
        self.assertIn('id="derive-bound"', PAGE)
        self.assertNotIn("<textarea", PAGE.lower())

    def test_six_bound_bottlenecks_feed_eight_fsrs_concepts(self):
        self.assertIn("var boundSteps = [", SCRIPT)
        self.assertEqual(SCRIPT.count("concept: 'triangle'"), 2)
        self.assertEqual(SCRIPT.count("concept: 'cauchy'"), 1)
        self.assertEqual(SCRIPT.count("concept: 'variance'"), 1)
        self.assertEqual(SCRIPT.count("concept: 'bound'"), 2)
        self.assertIn("var conceptIds = ['coordinates', 'identity', 'triangle', 'cauchy', 'variance', 'bound', 'norms', 'compatibility'];", SCRIPT)

    def test_wrong_bound_choices_are_routed_back_to_fsrs(self):
        self.assertIn("queueConceptNow(step.concept)", SCRIPT)
        self.assertIn("state.boundMistakes[step.concept]", SCRIPT)

    def test_new_formal_steps_have_no_placeholders(self):
        self.assertIn("theorem weighted_cauchy_schwarz", LEAN)
        self.assertIn("theorem weighted_variance_identity", LEAN)
        self.assertIsNone(re.search(r"\b(?:sorry|admit|axiom)\b", LEAN))

    def test_html_ids_remain_unique(self):
        ids = re.findall(r'\bid="([^"]+)"', PAGE)
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
