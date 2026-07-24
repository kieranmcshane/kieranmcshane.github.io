// Interaction and layout regression for /rating-lab/players/ at three widths.

const { test, expect } = require("@playwright/test");
const { freezeClock, hasHorizontalOverflow } = require("./helpers");

function isMobile(page) {
  return page.viewportSize().width <= 650;
}

async function gotoPlayerLab(page) {
  await freezeClock(page);
  await page.goto("/rating-lab/players/");
  await expect(
    page.locator("#player-ranking-body tr[data-player-row]").first()
  ).toBeVisible({ timeout: 30000 });
  await expect(page.locator("#player-lab-error")).toBeHidden();
}

test.describe("player lab", () => {
  test("loads without script errors or horizontal overflow", async ({
    page,
  }) => {
    const pageErrors = [];
    page.on("pageerror", (error) => pageErrors.push(error.message));
    await gotoPlayerLab(page);
    expect(pageErrors).toEqual([]);
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("search filters the list and shows the empty state", async ({
    page,
  }) => {
    await gotoPlayerLab(page);
    const rows = page.locator("#player-ranking-body tr[data-player-row]");
    const initialCount = await rows.count();
    expect(initialCount).toBeGreaterThan(0);

    await page.locator("#player-search").fill("zzzz-no-such-player");
    await expect(page.locator("#player-ranking-empty")).toBeVisible();
    await expect(page.locator("#player-ranking-empty")).toContainText(
      "No eligible player matches this search."
    );

    await page.locator("#player-search").fill("");
    await expect(rows.first()).toBeVisible();
  });

  test("RAPM is the default ranking and its tab is pressed", async ({
    page,
  }) => {
    await gotoPlayerLab(page);
    await expect(
      page.locator('#player-model-tabs button[data-player-model="rapm"]')
    ).toHaveAttribute("aria-pressed", "true");
    await expect(page.locator("#player-ranking-caption")).toContainText(
      "RAPM"
    );
    // The noise-domination note is reserved for the Lineup baseline.
    await expect(page.locator("#player-ordering-note")).toBeHidden();
  });

  test("model tabs toggle aria-pressed and re-render the list", async ({
    page,
  }) => {
    await gotoPlayerLab(page);
    const lineup = page.locator(
      '#player-model-tabs button[data-player-model="lineup-trueskill"]'
    );
    await lineup.click();
    await expect(lineup).toHaveAttribute("aria-pressed", "true");
    await expect(
      page.locator('#player-model-tabs button[data-player-model="rapm"]')
    ).toHaveAttribute("aria-pressed", "false");
    await expect(
      page.locator("#player-ranking-body tr[data-player-row]").first()
    ).toBeVisible();
    // Switching to the Lineup baseline surfaces the honest ordering caveat.
    const note = page.locator("#player-ordering-note");
    await expect(note).toBeVisible();
    await expect(note).toContainText("noise-dominated");
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("selecting a scatter point highlights it and opens its card", async ({
    page,
  }) => {
    await gotoPlayerLab(page);
    const chart = page.locator("#player-comparison-chart");
    await expect(chart.locator("svg")).toBeVisible();
    // Point buttons are 0×0 anchors whose visible dot is a positioned child
    // span, so Playwright's actionability check never sees them as visible.
    const point = chart.locator("button.player-lab-point").first();
    await point.dispatchEvent("click");
    await expect(
      chart.locator("button.player-lab-point.is-selected")
    ).toHaveCount(1);
    await expect(chart.locator(".player-lab-point-card")).toBeVisible();
  });

  test("switching cohort re-renders the leaderboard", async ({ page }) => {
    await gotoPlayerLab(page);
    const cohort = page.locator("#player-cohort");
    const values = await cohort
      .locator("option")
      .evaluateAll((options) => options.map((o) => o.value));
    expect(values.length).toBeGreaterThan(1);
    const initialFirstRow = await page
      .locator("#player-ranking-body tr[data-player-row]")
      .first()
      .getAttribute("data-player-row");
    await cohort.selectOption(values[1]);
    await expect(
      page.locator("#player-ranking-body tr[data-player-row]").first()
    ).toBeVisible();
    const newFirstRow = await page
      .locator("#player-ranking-body tr[data-player-row]")
      .first()
      .getAttribute("data-player-row");
    expect(newFirstRow).not.toBe(initialFirstRow);
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("mobile list header is sticky", async ({ page }) => {
    test.skip(!isMobile(page), "sticky list header is mobile-only");
    await gotoPlayerLab(page);
    const position = await page
      .locator(".player-lab-list-head")
      .evaluate((el) => getComputedStyle(el).position);
    expect(position).toBe("sticky");
  });

  test("player list @visual", async ({ page }) => {
    await gotoPlayerLab(page);
    await expect(page.locator(".player-lab-table")).toHaveScreenshot(
      "player-list.png"
    );
  });
});
