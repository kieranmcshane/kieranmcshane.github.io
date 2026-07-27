const { test, expect } = require("@playwright/test");
const { hasHorizontalOverflow } = require("./helpers");

const ARTICLE =
  "/2026/07/27/sha1-sha256-certificate-signatures/";

test.describe("primary-source facsimiles", () => {
  test("remain selective, readable, and clickable without overflowing the page", async ({
    page,
  }) => {
    await page.goto(ARTICLE);
    await expect(page.locator("html")).not.toHaveClass(/math-pending/);

    const previews = page.locator(".source-facsimile");
    await expect(previews).toHaveCount(5);
    await expect(page.locator(".source-facsimile figcaption")).toHaveCount(5);

    for (let index = 0; index < 5; index += 1) {
      const preview = previews.nth(index);
      await preview.scrollIntoViewIfNeeded();
      const link = preview.locator(".source-facsimile-link");
      await expect(link).toHaveAttribute("href", /^https:\/\//);
      await expect(link).toHaveAttribute("target", "_blank");
      await expect(link).toHaveAttribute("rel", /noopener/);
      const image = preview.locator("img");
      await expect(image).toBeVisible();
      expect(await image.evaluate((node) => node.naturalWidth)).toBeGreaterThan(
        500
      );
      await expect(preview.locator("figcaption")).toContainText(
        "Source excerpt."
      );
      await expect(preview.locator("figcaption")).toContainText(
        "Yellow highlighting added."
      );
      await expect(preview.locator("figcaption a")).toHaveAttribute(
        "href",
        /^https:\/\//
      );
    }

    const firstLink = previews.first().locator(".source-facsimile-link");
    await firstLink.focus();
    await expect(firstLink).toBeFocused();

    expect(await hasHorizontalOverflow(page)).toBe(false);

    const viewportWidth = page.viewportSize().width;
    const frameWidths = await page
      .locator(".source-facsimile-viewport")
      .evaluateAll((frames) =>
        frames.map((frame) => frame.getBoundingClientRect().width)
      );
    for (const width of frameWidths) {
      expect(width).toBeLessThanOrEqual(viewportWidth);
    }
  });
});
