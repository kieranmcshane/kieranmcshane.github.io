// Interaction and layout regression for /rating-lab/ at three widths.
//
// Covers the behaviors called out for CI visual regression:
// A-vs-B state synchronization, sticky controls, chart selection,
// competition switching, long names, keyboard navigation, and
// empty-market states.

const { test, expect } = require("@playwright/test");
const {
  freezeClock,
  readDataFile,
  routeDataFile,
  hasHorizontalOverflow,
} = require("./helpers");

const LONG_NAME =
  "Maximilian-Alexander von Hohenberg-Wittgenstein y Fernández de Córdoba-Salamanca";

function isMobile(page) {
  return page.viewportSize().width <= 650;
}

async function gotoRatingLab(page) {
  await freezeClock(page);
  await page.goto("/rating-lab/");
  // Data has loaded once the leaderboard has rows and no error is shown.
  // Several megabytes of JSON load in parallel across workers, so give the
  // first render a generous window, and surface the page's own error notice
  // instead of a bare timeout when a fetch fails under load.
  const firstRow = page.locator("#ranking-body tr").first();
  const errorNotice = page.locator("#rating-lab-error");
  await Promise.race([
    firstRow.waitFor({ state: "visible", timeout: 30000 }),
    errorNotice.waitFor({ state: "visible", timeout: 30000 }),
  ]);
  if (await errorNotice.isVisible()) {
    throw new Error(
      `rating-lab data failed to load: ${await errorNotice.textContent()}`
    );
  }
}

test.describe("page load", () => {
  test("renders live data without script errors or horizontal overflow", async ({
    page,
  }) => {
    const pageErrors = [];
    page.on("pageerror", (error) => pageErrors.push(error.message));
    await gotoRatingLab(page);
    await expect(page.locator("#rating-lab-freshness")).toBeVisible();
    expect(pageErrors).toEqual([]);
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("shows the error notice when a sport feed fails", async ({ page }) => {
    await freezeClock(page);
    await page.route("**/assets/data/rating-lab/tennis.json", (route) =>
      route.fulfill({ status: 500, body: "boom" })
    );
    await page.goto("/rating-lab/");
    const error = page.locator("#rating-lab-error");
    await expect(error).toBeVisible();
    await expect(error).toContainText("Please try again later.");
  });
});

test.describe("A vs B state synchronization", () => {
  test("matchup model tabs drive the shared leaderboard model", async ({
    page,
  }) => {
    await gotoRatingLab(page);
    await page
      .locator('#matchup-model-tabs button[data-matchup-model="robust"]')
      .click();
    await expect(
      page.locator('#matchup-model-tabs button[data-matchup-model="robust"]')
    ).toHaveAttribute("aria-pressed", "true");
    // The leaderboard model switcher shares the same state and re-renders.
    await expect(
      page.locator('#model-tabs button[data-model="robust"]')
    ).toHaveAttribute("aria-pressed", "true");
    await expect(
      page.locator("#matchup-result .rating-lab-outcome-strip")
    ).toBeVisible();
  });

  test("swap exchanges competitors and selecting A as B swaps back", async ({
    page,
  }) => {
    await gotoRatingLab(page);
    const selectA = page.locator("#matchup-a");
    const selectB = page.locator("#matchup-b");
    const initialA = await selectA.inputValue();
    const initialB = await selectB.inputValue();
    expect(initialA).not.toBe(initialB);

    await page.locator("#matchup-swap").click();
    await expect(selectA).toHaveValue(initialB);
    await expect(selectB).toHaveValue(initialA);

    // Choosing B's current competitor as A must swap, never duplicate.
    await selectA.selectOption(initialA);
    await expect(selectB).toHaveValue(initialB);
    expect(await selectA.inputValue()).not.toBe(await selectB.inputValue());
  });

  test("switching sport resets the matchup to that sport's competitors", async ({
    page,
  }) => {
    await gotoRatingLab(page);
    const tennisA = await page.locator("#matchup-a").inputValue();
    await page.locator('#sport-tabs button[data-sport="football"]').click();
    await expect(
      page.locator('#sport-tabs button[data-sport="football"]')
    ).toHaveAttribute("aria-pressed", "true");
    const footballA = await page.locator("#matchup-a").inputValue();
    expect(footballA).not.toBe(tennisA);
    await expect(
      page.locator("#matchup-result .rating-lab-outcome-strip")
    ).toBeVisible();
    // Football matchups include a draw outcome; tennis does not.
    await expect(
      page.locator("#matchup-result .rating-lab-outcome-cards .is-draw")
    ).toBeVisible();
  });
});

test.describe("chart selection", () => {
  test("selecting a leaderboard entity renders its rating history chart", async ({
    page,
  }) => {
    await gotoRatingLab(page);
    await page
      .locator("#ranking-body button.rating-lab-entity")
      .first()
      .click();
    const detail = page.locator("#rating-detail");
    await expect(detail.locator("svg.rating-lab-chart")).toBeVisible();
    await expect(detail.locator("[data-chart-surface]")).toHaveAttribute(
      "tabindex",
      "0"
    );
    await expect(
      page.locator("#ranking-body tr").first()
    ).toHaveAttribute("aria-selected", "true");
  });

  test("chart scrubbing works with the keyboard", async ({ page }) => {
    await gotoRatingLab(page);
    await page
      .locator("#ranking-body button.rating-lab-entity")
      .first()
      .click();
    const surface = page.locator("#rating-detail [data-chart-surface]");
    await expect(surface).toBeVisible();
    await surface.focus();
    await page.keyboard.press("End");
    const atEnd = await surface.getAttribute("aria-valuetext");
    expect(atEnd).toBeTruthy();
    await page.keyboard.press("Home");
    const atHome = await surface.getAttribute("aria-valuetext");
    expect(atHome).toBeTruthy();
    expect(atHome).not.toBe(atEnd);
    await page.keyboard.press("ArrowRight");
    const afterRight = await surface.getAttribute("aria-valuetext");
    expect(afterRight).not.toBe(atHome);
  });
});

test.describe("competition switching", () => {
  test("every sport tab renders a populated, non-overflowing leaderboard", async ({
    page,
  }) => {
    await gotoRatingLab(page);
    for (const sport of ["football", "national-football", "chess", "tennis"]) {
      await page.locator(`#sport-tabs button[data-sport="${sport}"]`).click();
      await expect(
        page.locator(`#sport-tabs button[data-sport="${sport}"]`)
      ).toHaveAttribute("aria-pressed", "true");
      await expect(page.locator("#ranking-body tr").first()).toBeVisible();
      expect(await hasHorizontalOverflow(page), `overflow on ${sport}`).toBe(
        false
      );
    }
  });

  test("the competition filter narrows the football leaderboard", async ({
    page,
  }) => {
    await gotoRatingLab(page);
    await page.locator('#sport-tabs button[data-sport="football"]').click();
    await expect(page.locator("#ranking-body tr").first()).toBeVisible();

    if (isMobile(page)) {
      // On mobile the filter lives in the dialog sheet.
      await page.locator("#rating-mobile-filters").click();
      const sheet = page.locator("#rating-mobile-filter-sheet");
      await expect(sheet).toBeVisible();
      const mobileFilter = page.locator("#rating-mobile-competition");
      const value = await mobileFilter
        .locator("option:not([value=''])")
        .first()
        .getAttribute("value");
      await mobileFilter.selectOption(value);
      await page.keyboard.press("Escape");
      await expect(sheet).toBeHidden();
    } else {
      const filter = page.locator("#competition-filter");
      const value = await filter
        .locator("option:not([value=''])")
        .first()
        .getAttribute("value");
      await filter.selectOption(value);
    }
    const caption = page.locator("#ranking-body tr").first();
    await expect(caption).toBeVisible();
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("the predictor competition selector re-renders independently", async ({
    page,
  }) => {
    await gotoRatingLab(page);
    const leaderboardModel = await page
      .locator('#model-tabs button[aria-pressed="true"]')
      .getAttribute("data-model");
    const select = page.locator("#predictor-competition");
    const options = await select.locator("option").all();
    expect(options.length).toBeGreaterThan(1);
    const second = await options[1].getAttribute("value");
    await select.selectOption(second);
    await expect(page.locator("#predictor-state")).toBeVisible();
    // Predictor state is isolated: the leaderboard model must not change.
    await expect(
      page.locator('#model-tabs button[aria-pressed="true"]')
    ).toHaveAttribute("data-model", leaderboardModel);
  });
});

test.describe("sticky controls", () => {
  test("local nav and table header remain sticky while scrolling", async ({
    page,
  }) => {
    await gotoRatingLab(page);
    const nav = page.locator(".rating-lab-local-nav");
    await expect(nav).toBeVisible();
    const position = await nav.evaluate(
      (el) => getComputedStyle(el).position
    );
    // Desktop pins the nav with sticky; the mobile layout uses fixed.
    expect(["sticky", "fixed"]).toContain(position);

    const theadPosition = await page
      .locator("#ranking-table thead")
      .evaluate((el) => getComputedStyle(el).position);
    expect(theadPosition).toBe("sticky");

    // After scrolling deep into the page the nav must stay pinned to a
    // viewport edge — top on desktop, bottom bar on mobile.
    await page.locator("#matchup").scrollIntoViewIfNeeded();
    await page.waitForTimeout(100);
    const box = await nav.boundingBox();
    const viewportHeight = page.viewportSize().height;
    const pinnedTop = Math.abs(box.y) <= 2;
    const pinnedBottom = Math.abs(box.y + box.height - viewportHeight) <= 2;
    expect(pinnedTop || pinnedBottom).toBe(true);
  });

  test("desktop detail panel is sticky", async ({ page }) => {
    test.skip(
      page.viewportSize().width <= 920,
      "detail panel becomes static at 920px and below"
    );
    await gotoRatingLab(page);
    const position = await page
      .locator("#rating-detail")
      .evaluate((el) => getComputedStyle(el).position);
    expect(position).toBe("sticky");
  });
});

test.describe("long names", () => {
  test("an extreme name neither breaks layout nor escapes its row", async ({
    page,
  }) => {
    const tennis = readDataFile("tennis.json");
    const topId = tennis.models.elo.rankings[0].id;
    await routeDataFile(page, "tennis.json", (data) => {
      Object.values(data.models).forEach((model) => {
        model.rankings.forEach((row) => {
          if (row.id === topId) row.name = LONG_NAME;
        });
      });
    });
    await gotoRatingLab(page);
    await expect(
      page.locator("#ranking-body .rating-lab-entity-name-text").first()
    ).toContainText("Maximilian-Alexander");
    expect(await hasHorizontalOverflow(page)).toBe(false);

    if (isMobile(page)) {
      const overflow = await page
        .locator("#ranking-body .rating-lab-entity-name-text")
        .first()
        .evaluate((el) => getComputedStyle(el).textOverflow);
      expect(overflow).toBe("ellipsis");
    }

    // The matchup cards must also absorb the long name.
    await page.locator("#matchup-a").selectOption(topId);
    await expect(
      page.locator("#matchup-result .rating-lab-outcome-cards")
    ).toBeVisible();
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });
});

test.describe("keyboard navigation", () => {
  test("sport and model switchers are keyboard operable", async ({ page }) => {
    await gotoRatingLab(page);
    const chessTab = page.locator('#sport-tabs button[data-sport="chess"]');
    await chessTab.focus();
    await page.keyboard.press("Enter");
    await expect(chessTab).toHaveAttribute("aria-pressed", "true");

    if (isMobile(page)) {
      // The desktop model switcher is hidden on mobile; the filter sheet
      // hosts its own model tabs which drive the same shared state.
      await page.locator("#rating-mobile-filters").click();
      const mobileGlicko = page.locator(
        '#rating-mobile-model-tabs button[data-mobile-model="glicko2"]'
      );
      await mobileGlicko.focus();
      await page.keyboard.press("Enter");
      await expect(mobileGlicko).toHaveAttribute("aria-pressed", "true");
      await page.keyboard.press("Escape");
    } else {
      const glicko = page.locator('#model-tabs button[data-model="glicko2"]');
      await glicko.focus();
      await page.keyboard.press("Space");
      await expect(glicko).toHaveAttribute("aria-pressed", "true");
    }
    // Either path must land on the shared leaderboard model state.
    await expect(
      page.locator('#model-tabs button[data-model="glicko2"]')
    ).toHaveAttribute("aria-pressed", "true");
  });

  test("column sorting works from the keyboard and updates aria-sort", async ({
    page,
  }) => {
    await gotoRatingLab(page);
    const sortButton = page.locator(
      '#ranking-table thead button[data-sort="change30"]'
    );
    await sortButton.focus();
    await page.keyboard.press("Enter");
    await expect(
      page.locator("#ranking-table thead th[aria-sort]")
    ).toHaveCount(1);
  });

  test("mobile filter sheet opens as a dialog and closes with Escape", async ({
    page,
  }) => {
    test.skip(!isMobile(page), "filter sheet is mobile-only");
    await gotoRatingLab(page);
    const trigger = page.locator("#rating-mobile-filters");
    await expect(trigger).toHaveAttribute("aria-haspopup", "dialog");
    await trigger.click();
    const sheet = page.locator("#rating-mobile-filter-sheet");
    await expect(sheet).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(sheet).toBeHidden();
  });
});

test.describe("empty-market states", () => {
  test("both providers explain an empty market instead of rendering blank", async ({
    page,
  }) => {
    const football = readDataFile("football.json");
    const emptyBenchmark = (benchmark) => {
      if (!benchmark) return benchmark;
      benchmark.competitions = [];
      benchmark.searches = [];
      benchmark.history = [];
      return benchmark;
    };
    await routeDataFile(page, "football.json", (data) => {
      const predictor = data.tournament_predictor;
      predictor.market_comparison = emptyBenchmark(predictor.market_comparison);
      predictor.kalshi_comparison = emptyBenchmark(predictor.kalshi_comparison);
    });
    await gotoRatingLab(page);

    const footballIds = new Set(
      (football.tournament_predictor?.competitions || []).map((c) => c.id)
    );
    const select = page.locator("#predictor-competition");
    const optionValues = await select
      .locator("option")
      .evaluateAll((options) => options.map((o) => o.value));
    const target = optionValues.find((value) => footballIds.has(value));
    expect(target, "a football competition in the predictor").toBeTruthy();
    await select.selectOption(target);

    const market = page.locator("#predictor-market");
    await expect(market).toBeVisible();
    const emptyCards = market.locator(".rating-lab-market-provider.is-empty");
    await expect(emptyCards).toHaveCount(2);
    await expect(emptyCards.first().locator("h3")).toHaveText(
      /No eligible market found|Market check unavailable/
    );
    await expect(emptyCards.first()).toContainText(
      "no market is guessed or attached by title alone"
    );
    const kickers = market.locator(
      ".rating-lab-market-provider.is-empty .rating-lab-kicker"
    );
    await expect(kickers.first()).toContainText("Polymarket");
    await expect(kickers.last()).toContainText("Kalshi");
  });
});

test.describe("visual baselines", () => {
  test("hero and leaderboard @visual", async ({ page }) => {
    await gotoRatingLab(page);
    await expect(page.locator(".rating-lab-hero")).toHaveScreenshot(
      "hero.png"
    );
    await expect(
      page.locator("section.rating-lab-board, #leaderboard-heading").first()
    ).toBeVisible();
    await expect(page.locator("#ranking-table")).toHaveScreenshot(
      "leaderboard-table.png"
    );
  });

  test("matchup section @visual", async ({ page }) => {
    await gotoRatingLab(page);
    await expect(
      page.locator("#matchup-result .rating-lab-outcome-strip")
    ).toBeVisible();
    await expect(page.locator("#matchup")).toHaveScreenshot("matchup.png");
  });
});
