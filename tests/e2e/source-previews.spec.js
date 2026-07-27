const { test, expect } = require("@playwright/test");
const { hasHorizontalOverflow } = require("./helpers");

const ARTICLE =
  "/2026/07/27/sha1-sha256-certificate-signatures/";

test.describe("primary-source previews", () => {
  test("remain selective, readable, and fully clickable", async ({ page }) => {
    await page.goto(ARTICLE);
    await expect(page.locator("html")).not.toHaveClass(/math-pending/);

    const previews = page.locator(".source-preview");
    await expect(previews).toHaveCount(5);
    await expect(page.locator(".source-preview figcaption")).toHaveCount(5);

    for (let index = 0; index < 5; index += 1) {
      const preview = previews.nth(index);
      const link = preview.locator(".source-preview-link");
      await expect(link).toHaveAttribute("href", /^https:\/\//);
      await expect(link).toHaveAttribute("target", "_blank");
      await expect(link).toHaveAttribute("rel", /noopener/);
      await expect(preview.locator("mark").first()).toBeVisible();
      await expect(preview.locator("figcaption")).toContainText(
        "What to notice."
      );
    }

    const firstLink = previews.first().locator(".source-preview-link");
    await firstLink.focus();
    await expect(firstLink).toBeFocused();

    expect(await hasHorizontalOverflow(page)).toBe(false);

    const viewportWidth = page.viewportSize().width;
    const paperWidths = await page
      .locator(".source-preview-paper")
      .evaluateAll((papers) => papers.map((paper) => paper.getBoundingClientRect().width));
    for (const width of paperWidths) {
      expect(width).toBeLessThanOrEqual(viewportWidth);
    }
  });
});
