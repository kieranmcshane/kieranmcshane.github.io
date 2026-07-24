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

  test("team selector only renders for team-scoped models", async ({
    page,
  }) => {
    await gotoPlayerLab(page);
    // Default RAPM is cohort-wide: the field must be visually gone, not just
    // carrying a hidden attribute that CSS overrides.
    await expect(page.locator("#player-team-field")).toBeHidden();
    await page
      .locator('#player-model-tabs button[data-player-model="hapm"]')
      .click();
    await expect(page.locator("#player-team-field")).toBeVisible();
  });

  test("team-scoped empty search explains its scope", async ({ page }) => {
    await gotoPlayerLab(page);
    await page
      .locator('#player-model-tabs button[data-player-model="hapm"]')
      .click();
    await expect(
      page.locator("#player-ranking-body tr[data-player-row]").first()
    ).toBeVisible();
    await page.locator("#player-search").fill("zzzz-no-such-player");
    const empty = page.locator("#player-ranking-empty");
    await expect(empty).toBeVisible();
    await expect(empty).toContainText("within");
    await expect(empty).toContainText("whole cohort");
  });

  test("chart is one tab stop with arrow-key marker navigation", async ({
    page,
  }) => {
    await gotoPlayerLab(page);
    const chart = page.locator("#player-comparison-chart");
    const tabbable = chart.locator('.player-lab-point[tabindex="0"]');
    await expect(tabbable).toHaveCount(1);
    await tabbable.focus();
    await page.keyboard.press("ArrowRight");
    const focused = await page.evaluate(() => ({
      isPoint: document.activeElement.classList.contains("player-lab-point"),
      tabIndex: document.activeElement.tabIndex,
    }));
    expect(focused.isPoint).toBe(true);
    expect(focused.tabIndex).toBe(0);
    await expect(chart.locator('.player-lab-point[tabindex="0"]')).toHaveCount(
      1
    );
  });

  test("withheld banner collapses to a single summary line", async ({
    page,
  }) => {
    await gotoPlayerLab(page);
    const banner = page.locator("#player-source-status");
    if (await banner.isHidden()) return; // nothing withheld in this dataset
    await expect(banner.locator("summary")).toContainText("withheld");
    await expect(banner.locator("details > div")).toBeHidden();
    await banner.locator("summary").click();
    await expect(banner.locator("details > div")).toBeVisible();
  });

  test("a near-miss click still selects the closest marker", async ({
    page,
  }) => {
    await gotoPlayerLab(page);
    const frame = page.locator(".player-lab-chart-frame");
    const target = await page.evaluate(() => {
      const rect = document
        .querySelector(".player-lab-chart-frame")
        .getBoundingClientRect();
      const point = document.querySelectorAll(".player-lab-point")[40];
      const style = getComputedStyle(point);
      return {
        x: parseFloat(style.getPropertyValue("--point-x")) + 14,
        y: parseFloat(style.getPropertyValue("--point-y")) + 12,
        id: point.dataset.playerId,
      };
    });
    // Click 14px wide and 12px below the marker centre — a realistic trackpad miss.
    await frame.click({ position: { x: target.x, y: target.y } });
    await expect(page.locator(".player-lab-point.is-selected")).toHaveCount(1);
    await expect(page.locator(".player-lab-point-card")).toBeVisible();
    // Clicking inside the card is reading, not dismissing.
    await page.locator(".player-lab-point-card").click();
    await expect(page.locator(".player-lab-point-card")).toBeVisible();
    // Clicking far from any marker dismisses the card.
    await frame.click({ position: { x: 8, y: 8 } });
    await expect(page.locator(".player-lab-point-card")).toHaveCount(0);
  });

  test("hovering near a marker names it before any click", async ({
    page,
  }) => {
    await gotoPlayerLab(page);
    const target = await page.evaluate(() => {
      const point = document.querySelectorAll(".player-lab-point")[40];
      const style = getComputedStyle(point);
      return {
        x: parseFloat(style.getPropertyValue("--point-x")) + 10,
        y: parseFloat(style.getPropertyValue("--point-y")),
      };
    });
    const frame = page.locator(".player-lab-chart-frame");
    await frame.hover({ position: { x: target.x, y: target.y } });
    const tip = page.locator(".player-lab-hover-tip");
    await expect(tip).toBeVisible();
    await expect(tip).not.toHaveText("");
  });

  test("chart adapts to narrow desktop widths without overflow", async ({
    page,
  }) => {
    // Between the mobile breakpoint (650) and ~830 px — including zoomed-in
    // desktop windows — the chart previously stayed a fixed 760 px and pushed
    // labels past the section edge.
    for (const width of [700, 780, 860]) {
      await page.setViewportSize({ width, height: 900 });
      await gotoPlayerLab(page);
      const frame = page.locator(".player-lab-chart-frame");
      const box = await frame.boundingBox();
      expect(box.x + box.width, `chart frame exceeds ${width}px viewport`).toBeLessThanOrEqual(width + 1);
      const stray = await page.evaluate(() => {
        const limit = document.documentElement.clientWidth + 1;
        return [...document.querySelectorAll(".player-lab-point > small")].filter(
          (label) => label.getBoundingClientRect().right > limit
        ).length;
      });
      expect(stray, `labels poke outside a ${width}px viewport`).toBe(0);
      expect(await hasHorizontalOverflow(page)).toBe(false);
    }
  });

  test("player list @visual", async ({ page }) => {
    await gotoPlayerLab(page);
    await expect(page.locator(".player-lab-table")).toHaveScreenshot(
      "player-list.png"
    );
  });
});
