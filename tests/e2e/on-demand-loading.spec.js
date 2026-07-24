// On-demand data contract for /rating-lab/ and /rating-lab/players/.
//
// The pages must fetch only the split payloads they need — small per-sport
// cores plus the active ranking list, and the player index plus one cohort —
// and stream the rest in on interaction, never the full multi-megabyte files.

const { test, expect } = require("@playwright/test");
const { freezeClock } = require("./helpers");

const FULL_SPORT_FILE = /^(tennis|football|national-football|chess)\.json$/;

function isMobile(page) {
  return page.viewportSize().width <= 650;
}

function trackDataRequests(page) {
  const requests = [];
  page.on("request", (request) => {
    const url = request.url();
    if (url.includes("/assets/data/rating-lab/")) {
      requests.push(url.split("/assets/data/rating-lab/")[1]);
    }
  });
  return requests;
}

async function gotoRatingLab(page) {
  await freezeClock(page);
  await page.goto("/rating-lab/");
  await expect(page.locator("#ranking-body tr").first()).toBeVisible({
    timeout: 30000,
  });
  await expect(page.locator(".rating-lab")).not.toHaveAttribute(
    "aria-busy",
    "true"
  );
}

// Choose a leaderboard model through the control that exists at this width.
async function chooseModel(page, model, captionText) {
  if (isMobile(page)) {
    await page.locator("#rating-mobile-filters").click();
    await page
      .locator(`#rating-mobile-model-tabs [data-mobile-model="${model}"]`)
      .click();
    await page.locator("#rating-mobile-filter-apply").click();
  } else {
    await page.locator(`#model-tabs [data-model="${model}"]`).click();
  }
  await expect(page.locator("#ranking-caption")).toContainText(captionText, {
    timeout: 15000,
  });
}

test.describe("on-demand data loading", () => {
  test("rating lab loads cores and only the active ranking list up front", async ({
    page,
  }) => {
    const requests = trackDataRequests(page);
    await gotoRatingLab(page);
    expect(requests).toContain("manifest.json");
    expect(requests).toContain("split/tennis-core.json");
    expect(requests).toContain("split/tennis-rankings-elo.json");
    // No full sport payloads on first paint, and no non-default model lists.
    // (An extra sport's Elo list may stream in for the forecast section's
    // entity media — that is on-demand behaviour, not an upfront cost.)
    expect(requests.filter((name) => FULL_SPORT_FILE.test(name))).toEqual([]);
    expect(
      requests.filter((name) =>
        /-rankings-(glicko2|trueskill|robust)\.json$/.test(name)
      )
    ).toEqual([]);

    await chooseModel(page, "glicko2", "Glicko");
    expect(requests).toContain("split/tennis-rankings-glicko2.json");

    await page.locator('#sport-tabs [data-sport="chess"]').click();
    await expect(page.locator(".rating-lab")).not.toHaveAttribute(
      "aria-busy",
      "true"
    );
    await expect(page.locator("#ranking-body tr").first()).toBeVisible({
      timeout: 30000,
    });
    expect(requests).toContain("split/chess-rankings-glicko2.json");
    expect(requests.filter((name) => FULL_SPORT_FILE.test(name))).toEqual([]);
  });

  test("opening a leaderboard detail streams the remaining models in", async ({
    page,
  }) => {
    await gotoRatingLab(page);
    await page.locator("#ranking-body .rating-lab-entity").first().click();
    const detail = page.locator("#rating-detail");
    await expect(detail).toBeVisible();
    // The cross-model comparison completes once the lazy model files land.
    for (const label of ["Elo", "Glicko-2", "Gaussian", "Robust"]) {
      await expect(detail.locator("table")).toContainText(label, {
        timeout: 20000,
      });
    }
    await expect(async () => {
      expect(await detail.locator("table").innerText()).not.toContain("…");
    }).toPass({ timeout: 20000 });
  });

  test("player lab loads the index and one cohort, then streams cohorts on demand", async ({
    page,
  }) => {
    const requests = trackDataRequests(page);
    await freezeClock(page);
    await page.goto("/rating-lab/players/");
    await expect(
      page.locator("#player-ranking-body tr[data-player-row]").first()
    ).toBeVisible({ timeout: 30000 });
    expect(requests).toContain("split/player-index.json");
    expect(requests.filter((name) => name === "player-football.json")).toEqual(
      []
    );
    const cohortRequests = requests.filter((name) =>
      name.startsWith("split/player-cohort-")
    );
    expect(cohortRequests.length).toBe(1);

    const select = page.locator("#player-cohort");
    const values = await select
      .locator("option")
      .evaluateAll((options) => options.map((option) => option.value));
    const next = values.find((value) => !cohortRequests[0].includes(value));
    await select.selectOption(next);
    await expect(page.locator(".player-lab")).not.toHaveAttribute(
      "aria-busy",
      "true"
    );
    await expect(
      page.locator("#player-ranking-body tr[data-player-row]").first()
    ).toBeVisible({ timeout: 30000 });
    expect(requests).toContain(`split/player-cohort-${next}.json`);
    expect(requests.filter((name) => name === "player-football.json")).toEqual(
      []
    );
  });
});
