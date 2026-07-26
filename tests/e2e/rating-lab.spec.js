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

  test("the sticky header never covers the first ranking row", async ({
    page,
  }) => {
    await gotoRatingLab(page);
    if (isMobile(page)) {
      await expect(page.locator("#ranking-body tr").first()).toBeVisible();
      return;
    }
    const headerBox = await page.locator("#ranking-table thead").boundingBox();
    const firstRowBox = await page
      .locator("#ranking-body tr")
      .first()
      .boundingBox();
    expect(headerBox).not.toBeNull();
    expect(firstRowBox).not.toBeNull();
    expect(firstRowBox.y).toBeGreaterThanOrEqual(
      headerBox.y + headerBox.height - 0.5
    );
  });

  test("shows the error notice when a sport feed fails", async ({ page }) => {
    await freezeClock(page);
    // The page loads the split core first and falls back to the full sport
    // file, so a real feed failure means both are unavailable.
    await page.route("**/assets/data/rating-lab/split/tennis-*.json", (route) =>
      route.fulfill({ status: 500, body: "boom" })
    );
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
  test("major competitions appear on the rating-history x-axis", async ({
    page,
  }) => {
    await routeDataFile(page, "split/tennis-rankings-elo.json", (payload) => {
      const row = payload.rankings[0];
      row.history_events = [
        {
          date: row.history[2][0],
          label: "Australian Open",
          short_label: "AO",
          season: "2024",
          matches: 7,
          wins: 7,
          draws: 0,
          losses: 0,
          result: "7W–0L",
        },
        {
          date: row.history[row.history.length - 3][0],
          label: "Wimbledon",
          short_label: "W",
          season: "2025",
          matches: 6,
          wins: 5,
          draws: 0,
          losses: 1,
          result: "5W–1L",
        },
      ];
    });
    await gotoRatingLab(page);
    await page
      .locator("#ranking-body button.rating-lab-entity")
      .first()
      .click();
    const events = page.locator("#rating-detail [data-history-event]");
    await expect(events).toHaveCount(2);
    await expect(events.first()).toHaveAttribute(
      "aria-label",
      /Australian Open 2024 · 7W–0L/
    );
    await events.first().click();
    await expect(
      page.locator("#rating-detail .rating-lab-chart-readout")
    ).toContainText("Australian Open 2024 · 7W–0L");
  });

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

  test("a live knockout shows forecasts and closed-record performance together", async ({
    page,
  }) => {
    const performanceRows = [
      {
        id: "atp:beta",
        name: "Beta Player",
        rank: 1,
        start_rating: 1900,
        start_sigma: null,
        start_volatility: null,
        start_score: 1900,
        end_rating: 1888,
        end_sigma: null,
        end_volatility: null,
        performance_rating: 1842,
        performance_rating_cap: null,
        performance_delta: -58,
        replay_rating: 1888,
        replay_change: -12,
        reset_rating: 1488,
        reset_rank: 1,
        matches: 1,
        wins: 0,
        draws: 0,
        losses: 1,
        points: 0,
        expected_score: 0.42,
        score_residual: -0.42,
        surprise_index: -0.86,
      },
      {
        id: "atp:gamma",
        name: "Gamma Player",
        rank: 2,
        start_rating: 1875,
        start_sigma: null,
        start_volatility: null,
        start_score: 1875,
        end_rating: 1867,
        end_sigma: null,
        end_volatility: null,
        performance_rating: 1810,
        performance_rating_cap: null,
        performance_delta: -65,
        replay_rating: 1867,
        replay_change: -8,
        reset_rating: 1480,
        reset_rank: 2,
        matches: 1,
        wins: 0,
        draws: 0,
        losses: 1,
        points: 0,
        expected_score: 0.35,
        score_residual: -0.35,
        surprise_index: -0.73,
      },
    ];
    const forecastRows = [
      {
        id: "atp:alpha",
        name: "Alpha Player",
        rating: 2010,
        reach_next_stage: 0.63,
        champion: 0.63,
        next_match: {
          opponent_id: "atp:delta",
          opponent_name: "Delta Player",
          round: "Final",
          surface: "Clay",
          win_probability: 0.63,
        },
        round_probabilities: [
          { stage: "Final", probability: 1 },
          { stage: "Champion", probability: 0.63 },
        ],
        surface_rating: 1995,
        surface_matches: 20,
      },
      {
        id: "atp:delta",
        name: "Delta Player",
        rating: 1940,
        reach_next_stage: 0.37,
        champion: 0.37,
        next_match: {
          opponent_id: "atp:alpha",
          opponent_name: "Alpha Player",
          round: "Final",
          surface: "Clay",
          win_probability: 0.37,
        },
        round_probabilities: [
          { stage: "Final", probability: 1 },
          { stage: "Champion", probability: 0.37 },
        ],
        surface_rating: 1925,
        surface_matches: 18,
      },
      ...performanceRows.map((row) => ({
        id: row.id,
        name: row.name,
        rating: row.start_rating,
        reach_next_stage: 0,
        champion: 0,
        next_match: null,
        round_probabilities: [
          { stage: "Final", probability: 0 },
          { stage: "Champion", probability: 0 },
        ],
        surface_rating: row.start_rating,
        surface_matches: 12,
      })),
    ];
    await routeDataFile(page, "split/tennis-core.json", (data) => {
      const competition = {
        id: "live-settled-test",
        label: "Live Settled Test",
        season: "2026",
        source_url: "https://example.test/draw",
        snapshot_sha256: "a".repeat(64),
        format: "tennis knockout draw",
        forecast_available: true,
        state: "live",
        status: "live",
        state_view: "conditional_forecast",
        state_message: "Two sourced results are locked.",
        completed_matches: 2,
        remaining_matches: 1,
        total_matches: 3,
        first_fixture: "2026-07-20",
        last_fixture: "2026-07-26",
        next_fixture: "2020-07-26",
        surface: "Clay",
        models: {},
        settled_performance: {
          status: "provisional_until_competition_finishes",
          settled_participants: 2,
          method: "Closed records only.",
          models: {},
        },
      };
      for (const model of ["elo", "glicko2", "trueskill", "robust"]) {
        competition.models[model] = {
          forecast_type: "tennis_draw",
          completed_matches: 2,
          current_stage: "Final",
          surface: "Clay",
          simulations: 1000,
          seed: "test",
          participants: forecastRows,
        };
        competition.settled_performance.models[model] = {
          rating_type: model === "elo" ? "elo" : "conservative_mu_minus_3_sigma",
          results: 2,
          surprise_method: "Chronological actual minus expected.",
          participants: performanceRows,
        };
      }
      const futureCompetition = JSON.parse(JSON.stringify(competition));
      futureCompetition.id = "future-next-event-test";
      futureCompetition.label = "Future Next Event Test";
      futureCompetition.state = "upcoming";
      futureCompetition.status = "upcoming";
      futureCompetition.next_fixture = "2099-07-26";
      data.tournament_predictor = {
        simulations_per_model: 1000,
        tennis_draw: "Published draw is locked.",
        knockout_draw: "Published draw is locked.",
        availability_rule: "Published fields only.",
        competitions: [competition, futureCompetition],
      };
    });

    await gotoRatingLab(page);
    await page.locator("#predictor-competition").selectOption("live-settled-test");
    await expect(page.locator("#predictor-state")).toContainText("Live");
    await expect(page.locator("#predictor-caption")).toContainText(
      "surface-aware progression"
    );
    await expect(page.locator("#predictor-metrics")).toContainText(
      "Next event"
    );
    await expect(page.locator("#predictor-metrics")).toContainText(
      "Update pending"
    );
    await expect(page.locator("#predictor-detail")).toContainText(
      "schedule update pending"
    );
    await expect(page.locator("#predictor-detail time")).toHaveAttribute(
      "datetime",
      "2020-07-26"
    );
    await expect(
      page.locator("#predictor-performance-title")
    ).toHaveText("Performance for eliminated players");
    const settledRows = page.locator("[data-settled-performance-team]");
    await expect(settledRows).toHaveCount(2);
    await settledRows.filter({ hasText: "Beta Player" }).click();
    await expect(page.locator("#predictor-detail")).toContainText(
      "Anchored performance rating"
    );
    await expect(page.locator("#predictor-detail")).toContainText(
      "Beta Player"
    );
    await page
      .locator("#predictor-competition")
      .selectOption("future-next-event-test");
    const alpha = page.locator('[data-predictor-team="atp:alpha"]');
    await expect(alpha).toHaveCount(1);
    await alpha.click();
    await expect(page.locator("#predictor-detail")).toContainText(
      "next event"
    );
    await expect(page.locator("#predictor-detail")).toContainText(
      "exact start time not published"
    );
    await expect(page.locator("#predictor-detail time")).toHaveAttribute(
      "datetime",
      "2099-07-26"
    );
    expect(await hasHorizontalOverflow(page)).toBe(false);
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

    if (isMobile(page)) {
      await expect(page.locator("#ranking-table thead")).toBeHidden();
    } else {
      const headerCellPosition = await page
        .locator("#ranking-table thead th")
        .first()
        .evaluate((el) => getComputedStyle(el).position);
      expect(headerCellPosition).toBe("sticky");
    }

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
    // The default view loads only the split Elo rankings, so mutate that file.
    const eloRankings = readDataFile("split/tennis-rankings-elo.json");
    const topId = eloRankings.rankings[0].id;
    await routeDataFile(page, "split/tennis-rankings-elo.json", (data) => {
      data.rankings.forEach((row) => {
        if (row.id === topId) row.name = LONG_NAME;
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
    // The forecast section reads competition and market data from the split
    // core file, so mutate that payload.
    const football = readDataFile("split/football-core.json");
    const emptyBenchmark = (benchmark) => {
      if (!benchmark) return benchmark;
      benchmark.competitions = [];
      benchmark.searches = [];
      benchmark.history = [];
      return benchmark;
    };
    await routeDataFile(page, "split/football-core.json", (data) => {
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
