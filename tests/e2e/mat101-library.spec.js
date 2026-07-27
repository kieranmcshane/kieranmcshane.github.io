const { test, expect } = require("@playwright/test");
const { hasHorizontalOverflow } = require("./helpers");

async function gotoLibrary(page) {
  await page.goto("/mat101/exercices/");
  await expect(page.locator(".mat101-library")).toBeVisible({ timeout: 12000 });
}

test.describe("MAT101 native library", () => {
  test("renders every statement and solution container without page overflow", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await expect(page.locator("[data-mat101-exercise]")).toHaveCount(103);
    await expect(page.locator(".mat101-difficulty")).toHaveCount(102);
    await expect(page.locator(".mat101-exercise-tags")).toHaveCount(103);
    await expect(page.locator(".mat101-statement img")).toHaveCount(122);
    await expect(page.locator(".mat101-solution-body")).toHaveCount(103);
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("searches, opens a multipage statement, then reveals its solution", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await page.locator("#mat101-search-input").fill("3.31");

    await expect(page.locator("[data-mat101-exercise]:visible")).toHaveCount(1);
    await expect(page.locator("#mat101-result-count")).toHaveText(
      "1 exercice affiché"
    );

    const exercise = page.locator("#exercice-3-31");
    await expect(exercise.locator(".mat101-difficulty")).toHaveText("***");
    await expect(exercise.locator(".mat101-difficulty")).toHaveAttribute(
      "aria-label",
      "Difficulté : approfondissement"
    );
    await exercise.locator(":scope > summary").click();
    await expect(exercise).toHaveAttribute("open", "");
    await expect(exercise.locator(".mat101-statement img")).toHaveCount(2);

    const solution = exercise.locator(".mat101-native-solution");
    await solution.locator(":scope > summary").click();
    await expect(solution).toHaveAttribute("open", "");
    await expect(solution.locator(".mat101-solution-body")).toContainText(
      "Supposons"
    );
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("filters the library from the notion index", async ({ page }) => {
    await gotoLibrary(page);

    const index = page.locator(".mat101-tag-index");
    await index.locator(":scope > summary").click();

    const invariantTag = page.locator('[data-mat101-tag="invariants"]');
    await invariantTag.click();

    await expect(invariantTag).toHaveAttribute("aria-pressed", "true");
    await expect(page.locator("[data-mat101-exercise]:visible")).toHaveCount(1);
    await expect(page.locator("#exercice-2-23")).toBeVisible();
    await expect(page).toHaveURL(/notion=invariants/);

    await page.locator('[data-mat101-tag=""]').click();
    await expect(page.locator("[data-mat101-exercise]:visible")).toHaveCount(103);
  });

  test("keeps provenance and the exercise-specific correction route visible", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await page.locator("#mat101-search-input").fill("1.1");
    const exercise = page.locator("#exercice-1-1");
    await exercise.locator(":scope > summary").click();

    await expect(exercise.locator(".mat101-exercise-footer")).toContainText(
      "Collectif MAT101, UGA (2022)"
    );
    await expect(
      exercise.getByRole("link", {
        name: "Signaler une erreur ou proposer une amélioration",
      })
    ).toHaveAttribute(
      "href",
      /template=mat101-correction\.yml.*MAT101.*1\.1/
    );
  });
});
