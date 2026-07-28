const { test, expect } = require("@playwright/test");
const { hasHorizontalOverflow } = require("./helpers");

async function gotoRepertoire(page) {
  await page.goto("/repertoire-raisonne/");
  await expect(page.locator(".repertoire-library")).toBeVisible({
    timeout: 12000,
  });
}

test.describe("Répertoire raisonné", () => {
  test("renders all 127 indexed problems without overflow", async ({ page }) => {
    await gotoRepertoire(page);
    await expect(page.locator("[data-repertoire-problem]")).toHaveCount(127);
    await expect(page.locator("[data-repertoire-section]")).toHaveCount(5);
    await expect(page.locator("[data-repertoire-chapter]")).toHaveCount(14);
    await expect(
      page.locator("[data-repertoire-audit-problem]")
    ).toHaveCount(17);
    await expect(
      page.locator('[data-repertoire-audit-problem="121"]')
    ).toContainText("Les points de X y étant d’accumulation");
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("searches titles and updates the result count", async ({ page }) => {
    await gotoRepertoire(page);
    await page
      .locator("#repertoire-search-input")
      .fill("jet s’annule en chaque point");

    await expect(
      page.locator("[data-repertoire-problem]:visible")
    ).toHaveCount(1);
    await expect(page.locator("#probleme-121")).toBeVisible();
    await expect(page.locator("#repertoire-result-count")).toHaveText(
      "1 problème affiché"
    );
  });

  test("filters by editorial part and restores the full catalogue", async ({
    page,
  }) => {
    await gotoRepertoire(page);

    const analysis = page.locator(
      '[data-repertoire-part="analyse-reelle"]'
    );
    await analysis.click();
    await expect(analysis).toHaveAttribute("aria-pressed", "true");
    await expect(
      page.locator("[data-repertoire-problem]:visible")
    ).toHaveCount(20);

    await page.locator('[data-repertoire-part=""]').click();
    await expect(
      page.locator("[data-repertoire-problem]:visible")
    ).toHaveCount(127);
  });

  test("keeps the complete index usable without JavaScript", async ({
    browser,
  }) => {
    const context = await browser.newContext({ javaScriptEnabled: false });
    const noScriptPage = await context.newPage();
    await noScriptPage.goto("/repertoire-raisonne/");
    await expect(
      noScriptPage.locator("[data-repertoire-problem]")
    ).toHaveCount(127);
    await context.close();
  });
});
