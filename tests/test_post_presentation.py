from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTICLE = (ROOT / "_posts/2026-07-17-centered-correlation-tensors-separability.md").read_text()
FLOW = (ROOT / "assets/images/centered-correlation-flow.svg").read_text()
HEAD = (ROOT / "_includes/head-custom.html").read_text()
LAYOUT = (ROOT / "_layouts/post.html").read_text()
STYLES = (ROOT / "assets/main.scss").read_text()


class PostPresentationTests(unittest.TestCase):
    def test_flow_figure_carries_its_own_svg_styles(self):
        self.assertIn("<style>", FLOW)
        for selector in (".box", ".heading", ".flow-arrow", ".accent"):
            self.assertIn(selector, FLOW)

    def test_math_posts_hide_raw_tex_until_mathjax_is_ready(self):
        self.assertIn("math: true", ARTICLE)
        self.assertIn("document.documentElement.classList.add('math-pending')", HEAD)
        self.assertIn("MathJax.startup.defaultPageReady()", HEAD)
        self.assertIn("html.math-pending .post-content", STYLES)

    def test_display_math_and_tables_scroll_inside_article_width(self):
        self.assertRegex(
            STYLES,
            r'\.post-content mjx-container\[display="true"\][\s\S]*?overflow-x: auto;',
        )
        self.assertRegex(
            STYLES,
            r"\.post-content table[\s\S]*?overflow-x: auto;",
        )

    def test_regular_posts_use_readable_measure_and_shared_typography(self):
        self.assertRegex(
            STYLES,
            r"\.post\.h-entry > \.post-content[\s\S]*?max-width: 68ch;",
        )
        self.assertIn('font-family: Charter, "Bitstream Charter"', STYLES)

    def test_figure_captions_use_semantic_markup(self):
        self.assertEqual(ARTICLE.count('<figure class="post-figure">'), 2)
        self.assertEqual(ARTICLE.count("<figcaption>"), 2)

    def test_post_layout_renders_subtitle_and_modified_date(self):
        self.assertIn("page.subtitle", LAYOUT)
        self.assertIn('class="post-subtitle"', LAYOUT)
        self.assertIn("page.last_modified_at", LAYOUT)
        self.assertIn('itemprop="dateModified"', LAYOUT)


if __name__ == "__main__":
    unittest.main()
