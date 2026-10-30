"""Public pages must not link to articles moved into _drafts/."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
UNPUBLISHED = (
    "/2026/07/16/random-quantum-measurements-incompatibility/",
    "/2026/07/17/centered-correlation-tensors-separability/",
    "/2026/07/18/formalizing-xens-correction-in-lean/",
    "/2026/07/18/x-ens-2026-mathematics-b-complete-correction/",
    "/2026/07/27/galois-theory-without-detours/",
    "/2026/07/27/sha1-sha256-certificate-signatures/",
)
LINK = re.compile(
    r"""(?:href\s*=\s*["'][^"']*|\]\(\s*)("""
    + "|".join(re.escape(url) for url in UNPUBLISHED)
    + r")",
    re.IGNORECASE,
)
SCAN_SUFFIXES = {".md", ".html", ".js", ".yml", ".yaml"}
SKIP_PARTS = {"_drafts", "_site", "node_modules", ".git"}


class UnpublishedPostsTests(unittest.TestCase):
    def test_drafts_hold_every_unpublished_article(self) -> None:
        drafts = ROOT / "_drafts"
        for url in UNPUBLISHED:
            slug = url.strip("/").split("/")[-1]
            matches = list(drafts.glob(f"*-{slug}.md"))
            self.assertEqual(len(matches), 1, slug)
        self.assertFalse(any((ROOT / "_posts").glob("*.md")))

    def test_public_sources_do_not_link_to_unpublished_articles(self) -> None:
        offenders: list[str] = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
                continue
            if SKIP_PARTS.intersection(path.parts):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for match in LINK.finditer(text):
                offenders.append(f"{path.relative_to(ROOT)}: {match.group(0)}")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
