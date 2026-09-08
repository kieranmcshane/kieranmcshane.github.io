const { test, expect } = require("@playwright/test");
const { hasHorizontalOverflow } = require("./helpers");

async function gotoSessions(page) {
  await page.goto("/mat101/seances/");
  await expect(page.locator("[data-mat101-course]")).toBeVisible({
    timeout: 12000,
  });
}

test.describe("MAT101 nineteen-session student path", () => {
  test("shows all nineteen sessions behind one public MAT101 entry", async ({
    page,
  }) => {
    await gotoSessions(page);

    await expect(page.locator("[data-mat101-session-card]")).toHaveCount(19);
    await expect(page.locator("[data-mat101-session-card]:visible")).toHaveCount(19);
    await expect(page.locator("#mat101-session-count")).toHaveText(
      "19 séances affichées"
    );
    await expect(
      page.locator('a[href$="parcours-19-seances-mat101-ima02.pdf"]')
    ).toHaveCount(0);
    await expect(
      page.locator('[data-session-number="18"] .mat101-session-date-state.is-pending')
    ).toContainText("À confirmer");
    await expect(
      page.locator('[data-session-number="19"] .mat101-session-date-state.is-pending')
    ).toContainText("À confirmer");
    await expect(page.locator(".mat101-course-hero")).toHaveCount(0);
    await expect(page.locator(".mat101-course-status")).toHaveCount(0);
    await expect(page.getByText("19 séances pour progresser en MAT101")).toHaveCount(0);
    await expect(page.locator(".mat101-shell")).toBeVisible();
    await expect(page.locator(".mat101-shell-links a[href='/mat101/seances/']")).toHaveAttribute(
      "aria-current",
      "page"
    );
    await expect(page.locator(".site-header")).toHaveCount(0);
    await expect(page.locator(".site-footer")).toHaveCount(0);
    await expect(page.locator('.site-nav a[href="/rating-lab/"]')).toHaveCount(0);
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("renders competency math on session cards", async ({ page }) => {
    await gotoSessions(page);
    await page.waitForFunction(
      () => !document.documentElement.classList.contains("math-pending"),
      null,
      { timeout: 12000 }
    );

    const card = page.locator('[data-session-number="1"]');
    await expect(card.locator("mjx-container")).not.toHaveCount(0);
    await expect(card.locator(".mat101-session-skills")).toContainText("Situer un nombre");

    await page.locator('[data-mat101-session-filter="complexes"]').click();
    const card2 = page.locator('[data-session-number="2"]');
    await expect(card2.locator("mjx-container")).not.toHaveCount(0);
    await expect(card2.locator(".mat101-session-skills")).not.toContainText("\\bar");
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("marks session 10 as a one-hour interro with extended time", async ({ page }) => {
    await gotoSessions(page);

    const card = page.locator('[data-session-number="10"]');
    await expect(card.locator(".mat101-session-date-state.is-interro")).toHaveText(
      "Interro"
    );
    await expect(card.locator(".mat101-session-format")).toHaveText(
      "1 h · tiers temps 1 h 20"
    );

    await card.locator(":scope > a").click();
    await expect(page).toHaveURL(/\/mat101\/seances\/10-ensembles-appartenance-inclusion\/$/);
    await expect(page.locator(".mat101-session-detail-status.is-interro")).toContainText(
      "Interro"
    );
    await expect(page.locator(".mat101-session-detail-status.is-interro")).toContainText(
      "1 h · tiers temps 1 h 20"
    );
    await expect(page.locator(".mat101-session-source")).toContainText(
      "Durée 1 h · tiers temps 1 h 20"
    );
  });

  test("exposes mobile swipe affordances on small screens", async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== "mobile-390", "mobile viewport only");

    await gotoSessions(page);
    await expect(page.locator('[data-mat101-swipe="session-hub"]')).toBeVisible();
    await expect(page.locator(".mat101-swipe-hint")).toContainText("Glisser");

    await page.goto("/mat101/seances/02-conjugue-module-quotient/");
    await expect(page.locator('[data-mat101-swipe="session-detail"]')).toBeVisible();
    await expect(page.locator(".mat101-swipe-hint")).toContainText("séance");
  });

  test("filters and searches without losing shareable state", async ({ page }) => {
    await gotoSessions(page);

    await page.locator('[data-mat101-session-filter="complexes"]').click();
    await expect(page.locator("[data-mat101-session-card]:visible")).toHaveCount(8);
    await expect(page.locator("#mat101-session-count")).toHaveText(
      "8 séances affichées"
    );
    await expect(page).toHaveURL(/bloc=complexes/);

    await page.locator('[data-mat101-session-filter="langage"]').click();
    await expect(page.locator("[data-mat101-session-card]:visible")).toHaveCount(11);
    await expect(page.locator("#mat101-session-count")).toHaveText(
      "11 séances affichées"
    );

    await page.locator('[data-mat101-session-filter="complexes"]').click();
    await page.locator("#mat101-session-search-input").fill("racines n-ièmes");
    await expect(page.locator("[data-mat101-session-card]:visible")).toHaveCount(1);
    await expect(page.locator('[data-session-number="8"]')).toBeVisible();
    await expect(page).toHaveURL(/q=racines/);

    await page.reload();
    await expect(page.locator("[data-mat101-session-card]:visible")).toHaveCount(1);
    await expect(page.locator('[data-session-number="8"]')).toBeVisible();

    await page.locator("#mat101-session-search-input").fill("thème absent xyz");
    await expect(page.locator("#mat101-session-no-results")).toBeVisible();
    await expect(page.locator("#mat101-session-count")).toHaveText(
      "0 séances affichées"
    );
  });

  test("opens a student page without instructor material", async ({ page }) => {
    await gotoSessions(page);
    await page.locator('[data-session-number="1"] > a').click();

    await expect(page).toHaveURL(/\/mat101\/seances\/01-forme-algebrique\/$/);
    await expect(page.locator("[data-mat101-session-number='1']")).toBeVisible();
    await expect(page.getByRole("heading", { name: "À savoir faire" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Parcours" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Contrôle rapide" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Questions" })).toBeVisible();
    await expect(page.locator(".mat101-session-content")).not.toContainText(
      "Déroulé minute par minute"
    );
    await expect(page.locator("body")).not.toContainText("Fiche enseignant");
    await expect(page.locator('.mat101-session-pager a[rel="next"]')).toContainText(
      "Séance 2"
    );
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("labels the two unresolved schedule slots instead of inventing dates", async ({
    page,
  }) => {
    await page.goto("/mat101/seances/18-recurrence/");
    await expect(page.locator("[data-mat101-session-number='18']")).toBeVisible({
      timeout: 12000,
    });
    await expect(page.locator(".mat101-session-detail-status.is-pending")).toContainText(
      "Date à confirmer"
    );
    await expect(page.locator(".mat101-session-detail-status.is-pending")).toContainText(
      "Date et salle à confirmer"
    );
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("keeps the full path usable without JavaScript", async ({ browser }) => {
    const context = await browser.newContext({ javaScriptEnabled: false });
    const noScriptPage = await context.newPage();
    await noScriptPage.goto("/mat101/seances/");

    await expect(noScriptPage.locator("[data-mat101-session-card]")).toHaveCount(19);
    await noScriptPage.locator('[data-session-number="19"] > a').click();
    await expect(
      noScriptPage.locator("[data-mat101-session-number='19']")
    ).toBeVisible();
    await expect(
      noScriptPage.getByRole("heading", { name: "Révision mixte" })
    ).toBeVisible();
    expect(await hasHorizontalOverflow(noScriptPage)).toBe(false);
    await context.close();
  });
});
