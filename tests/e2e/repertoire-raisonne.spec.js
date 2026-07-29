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
      page.locator("[data-repertoire-native-problem]")
    ).toHaveCount(127);
    await expect(
      page.locator('[data-repertoire-native-problem="1"]')
    ).toContainText("Un corps fini peut-il être algébriquement clos");
    await expect(
      page.locator('[data-repertoire-native-problem="121"]')
    ).toContainText("Chaque point de X∩I est un point d’accumulation");
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("opens a transcribed problem from the catalogue and reveals its solution", async ({
    page,
  }) => {
    await gotoRepertoire(page);
    await page.locator("#probleme-1 a").click();
    await expect(page).toHaveURL(/#probleme-natif-1$/);
    const problem = page.locator('[data-repertoire-native-problem="1"]');
    const solution = problem.locator(".repertoire-native-solution");
    await solution.locator("summary").click();
    await expect(solution).toContainText("Pour tout");
    await expect(solution).toContainText("n’est pas algébriquement clos");
  });

  test("renders the corrected finite-field formulas with MathJax", async ({
    page,
  }) => {
    await gotoRepertoire(page);
    const problem = page.locator('[data-repertoire-native-problem="6"]');
    const solution = problem.locator(".repertoire-native-solution");
    await solution.locator("summary").click();
    expect(await solution.locator("mjx-container").count()).toBeGreaterThan(12);
    await expect(solution).toContainText(
      "Chaque facteur irréductible a donc degré"
    );
    await expect(problem).toContainText("Formules recomposées et contrôlées");
  });

  test("reads a complete native statement and reveals its solution", async ({
    page,
  }) => {
    await gotoRepertoire(page);
    const problem = page.locator('[data-repertoire-native-problem="125"]');
    await expect(problem).toContainText(
      "Construire une famille de lois distinctes"
    );
    const solution = problem.locator(".repertoire-native-solution");
    await expect(solution).not.toHaveAttribute("open", "");
    await solution.locator("summary").click();
    await expect(solution).toHaveAttribute("open", "");
    await expect(solution).toContainText("Famille de Stieltjes log-normale");
    await expect(solution).toContainText("rend cette espérance réelle");
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

  test("searches inside a transcribed solution from problems 1–110", async ({
    page,
  }) => {
    await gotoRepertoire(page);
    await page.locator("#repertoire-search-input").fill("conjuguée de f");
    await expect(
      page.locator("[data-repertoire-problem]:visible")
    ).toHaveCount(1);
    await expect(page.locator("#probleme-80")).toBeVisible();
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
    await expect(
      noScriptPage.locator("[data-repertoire-native-problem]")
    ).toHaveCount(127);
    await context.close();
  });
});
