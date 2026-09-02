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
    ).toHaveCount(2);
    await expect(
      page.getByText("La date et la salle des séances 18 et 19 restent à confirmer.")
    ).toBeVisible();
    await expect(
      page.locator('.site-nav a[href="/mat101/seances/"]')
    ).toHaveCount(1);
    await expect(
      page.locator('.site-nav a[href="/mat101/seances/"]')
    ).toHaveText("MAT101");
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("filters and searches without losing shareable state", async ({ page }) => {
    await gotoSessions(page);

    await page.locator('[data-mat101-session-filter="complexes"]').click();
    await expect(page.locator("[data-mat101-session-card]:visible")).toHaveCount(9);
    await expect(page.locator("#mat101-session-count")).toHaveText(
      "9 séances affichées"
    );
    await expect(page).toHaveURL(/bloc=complexes/);

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
    await expect(page.getByRole("heading", { name: "Ticket" })).toBeVisible();
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
