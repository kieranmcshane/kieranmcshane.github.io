const { test, expect } = require("@playwright/test");
const { hasHorizontalOverflow } = require("./helpers");

test.describe("MAT101 essential demonstrations", () => {
  test("renders all demonstrations with MathJax and without overflow", async ({
    page,
  }) => {
    const consoleErrors = [];
    page.on("console", (message) => {
      if (message.type() === "error") consoleErrors.push(message.text());
    });

    await page.goto("/mat101/demonstrations/");
    await expect(page.locator(".mat101-demonstrations")).toBeVisible({
      timeout: 12000,
    });

    await page.waitForFunction(
      () => !document.documentElement.classList.contains("math-pending"),
      null,
      { timeout: 12000 }
    );

    await expect(page.locator(".mat101-demonstration-card")).toHaveCount(9);
    await expect(page.locator(".mat101-demonstration-proof")).toHaveCount(9);
    await expect(page.locator("mjx-merror")).toHaveCount(0);
    expect(await hasHorizontalOverflow(page)).toBe(false);
    expect(consoleErrors).toEqual([]);
  });

  test("navigation highlights the demonstrations page", async ({ page }) => {
    await page.goto("/mat101/demonstrations/");
    await expect(
      page.locator('.mat101-shell-links a[href$="/mat101/demonstrations/"]')
    ).toHaveAttribute("aria-current", "page");
  });

  test("chapter two shows the empty state message", async ({ page }) => {
    await page.goto("/mat101/demonstrations/");
    await expect(page.locator("#ensembles .mat101-demonstrations-empty")).toContainText(
      "Aucune démonstration essentielle"
    );
  });
});
