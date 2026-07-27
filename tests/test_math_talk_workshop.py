from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTICLE = (
    ROOT / "_posts/2026-07-27-preparing-a-mathematics-research-talk.md"
).read_text()
STYLES = (ROOT / "assets/main.scss").read_text()
LLMS = (ROOT / "llms.txt").read_text()


class MathTalkWorkshopTests(unittest.TestCase):
    def test_workshop_contains_nine_ordered_stages(self):
        headings = re.findall(r"^## Stage (\d) —", ARTICLE, flags=re.MULTILINE)
        self.assertEqual(headings, [str(number) for number in range(1, 10)])

    def test_all_thirty_exercises_are_present_once(self):
        exercises = re.findall(r"^### Exercise (\d+) —", ARTICLE, flags=re.MULTILINE)
        self.assertEqual(exercises, [str(number) for number in range(1, 31)])

    def test_each_stage_has_a_concrete_deliverable(self):
        self.assertEqual(ARTICLE.count('class="talk-deliverable"'), 9)
        self.assertEqual(ARTICLE.count("**Done when:**"), 27)

    def test_method_keeps_core_mathematical_preferences(self):
        for phrase in (
            "Calibration before abstraction",
            "Counterexamples before confidence",
            "Bottom lines before transitions",
            "Backups instead of digressions",
            "The scope is mathematical",
        ):
            self.assertIn(phrase, ARTICLE)

    def test_compact_worksheet_covers_integrity_checks(self):
        self.assertIn("## Compact worksheet", ARTICLE)
        self.assertIn("Every main claim has exact hypotheses", ARTICLE)
        self.assertIn("The talk works at 100%, 85% and 60% length", ARTICLE)

    def test_workshop_navigation_is_responsive(self):
        self.assertIn(".talk-workshop-map", STYLES)
        self.assertRegex(
            STYLES,
            r"@media screen and \(max-width: 600px\)[\s\S]*?"
            r"\.talk-workshop-map[\s\S]*?grid-template-columns: 1fr;",
        )

    def test_workshop_is_exposed_in_machine_readable_site_index(self):
        self.assertIn(
            "/2026/07/27/preparing-a-mathematics-research-talk/",
            LLMS,
        )


if __name__ == "__main__":
    unittest.main()
