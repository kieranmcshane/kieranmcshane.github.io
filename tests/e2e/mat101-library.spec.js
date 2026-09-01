const { test, expect } = require("@playwright/test");
const { hasHorizontalOverflow } = require("./helpers");

async function gotoLibrary(page) {
  await page.goto("/mat101/exercices/");
  await expect(page.locator(".mat101-library")).toBeVisible({ timeout: 12000 });
}

test.describe("MAT101 native library", () => {
  test("renders the mathematical corpus without MathJax or console errors", async ({
    page,
  }) => {
    const consoleErrors = [];
    page.on("console", (message) => {
      if (message.type() === "error") consoleErrors.push(message.text());
    });

    await gotoLibrary(page);
    await page.waitForFunction(
      () => !document.documentElement.classList.contains("math-pending"),
      null,
      { timeout: 12000 }
    );

    await expect(page.locator("mjx-merror")).toHaveCount(0);
    expect(consoleErrors).toEqual([]);
  });

  test("renders every statement and solution container without page overflow", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await expect(page.locator("[data-mat101-exercise]")).toHaveCount(103);
    await expect(page.locator(".mat101-difficulty")).toHaveCount(102);
    await expect(page.locator(".mat101-exercise-tags")).toHaveCount(103);
    await expect(page.locator(".mat101-statement img")).toHaveCount(0);
    await expect(page.locator(".mat101-statement-transcription")).toHaveCount(103);
    await expect(page.locator(".mat101-solution-body")).toHaveCount(103);
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("searches, opens a semantic statement, then reveals its solution", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await page.locator("#mat101-search-input").fill("3.31");

    await expect(page.locator("[data-mat101-exercise]:visible")).toHaveCount(1);
    await expect(page.locator("#mat101-result-count")).toHaveText(
      "1 exercice affiché"
    );

    const exercise = page.locator("#exercice-3-31");
    await expect(
      exercise.locator(".mat101-difficulty .mat101-level-advanced")
    ).toHaveCount(1);
    await expect(exercise.locator(".mat101-difficulty")).toHaveAttribute(
      "aria-label",
      "Difficulté : approfondissement"
    );
    await exercise.locator(":scope > summary").click();
    await expect(exercise).toHaveAttribute("open", "");
    await expect(exercise.locator(".mat101-statement-transcription")).toContainText(
      "relation d’équivalence"
    );

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
    await expect(
      page.locator("[data-mat101-toc-link]:not([hidden])")
    ).toHaveCount(1);
    await expect(
      page.locator("[data-mat101-toc-chapter]:not([hidden])")
    ).toHaveCount(1);
    await expect(
      page.locator(
        '[data-mat101-toc-chapter][data-chapter-id="ensembles"]'
      )
    ).toHaveClass(/is-active/);
    await expect(page).toHaveURL(/notion=invariants/);

    await page.locator('[data-mat101-tag=""]').click();
    await expect(page.locator("[data-mat101-exercise]:visible")).toHaveCount(103);
  });

  test("navigates and filters from the interactive table of contents", async ({
    page,
  }) => {
    test.setTimeout(120000);
    await gotoLibrary(page);

    const toc = page.locator("[data-mat101-toc]");
    const wide = page.viewportSize().width >= 1240;
    if (wide) {
      await expect(toc).toHaveAttribute("open", "");
      await expect(toc).toHaveAttribute("data-mat101-toc-locked", "");
    } else {
      await expect(toc).not.toHaveAttribute("open", "");
      await toc.locator(":scope > summary").click();
    }

    await expect(toc.locator("[data-mat101-toc-link]")).toHaveCount(103);
    await expect(toc.locator(".mat101-difficulty-legend")).toContainText(
      "Niveau examen"
    );
    if (wide) {
      await toc
        .locator('[data-mat101-toc-chapter-link][href="#fonctions"]')
        .click();
      await expect(
        toc.locator('[data-mat101-toc-chapter][data-chapter-id="fonctions"]')
      ).toHaveClass(/is-active/);
    }
    await toc.locator('[data-mat101-toc-link][data-exercise-id="3.16"]').click();

    await expect(page.locator("#exercice-3-16")).toHaveAttribute("open", "");
    if (wide) await expect(toc).toHaveAttribute("open", "");
    else await expect(toc).not.toHaveAttribute("open", "");
    await expect(
      toc.locator('[data-mat101-toc-link][data-exercise-id="3.16"]')
    ).toHaveAttribute("aria-current", "location");
    await expect(
      toc.locator('[data-mat101-toc-chapter-link][href="#fonctions"]')
    ).toHaveAttribute("aria-current", "location");
    await expect(page.locator("#mat101-toc-current")).toContainText(
      "Exercice 3.16"
    );

    await page
      .locator("#mat101-search-input")
      .fill("suite de nombres réels est périodique");
    await expect(
      toc.locator("[data-mat101-toc-link]:not([hidden])")
    ).toHaveCount(1);
    await expect(
      toc.locator('[data-mat101-toc-chapter][data-chapter-id="limites"]')
    ).toHaveClass(/is-active/);
    await expect(page.locator("#mat101-toc-current")).toHaveText(
      "1 exercice disponible"
    );
  });

  test("uses a bounded, non-overlapping left rail on wide screens", async ({
    page,
  }) => {
    test.skip(page.viewportSize().width < 1240, "wide-screen rail only");
    await gotoLibrary(page);

    const toc = page.locator("[data-mat101-toc]");
    const rail = page.locator(".mat101-toc");
    const content = page.locator(".mat101-study-content");
    await expect(toc).toHaveAttribute("open", "");
    await expect(toc.locator(":scope > summary")).toHaveAttribute(
      "aria-disabled",
      "true"
    );
    await expect(toc.locator(":scope > summary")).toHaveAttribute(
      "tabindex",
      "-1"
    );
    await expect(toc.locator("[data-mat101-toc-chapter-link]")).toHaveCount(4);
    await expect(toc.locator("[data-mat101-toc-chapter-link]:visible")).toHaveCount(4);
    await expect(toc.locator("[data-mat101-toc-link]")).toHaveCount(103);
    await expect(toc.locator("[data-mat101-toc-link]:visible")).toHaveCount(20);
    await expect(
      toc.locator('[data-mat101-toc-chapter][data-chapter-id="complexes"]')
    ).toHaveClass(/is-active/);

    await page.locator(".mat101-reading-note").evaluate((element) =>
      element.scrollIntoView({ block: "start" })
    );
    await expect(rail).toBeVisible();
    const initialRail = await rail.boundingBox();
    const contentBox = await content.boundingBox();
    expect(await rail.evaluate((element) => getComputedStyle(element).position)).toBe(
      "sticky"
    );
    expect(contentBox.width).toBeGreaterThanOrEqual(819);
    expect(contentBox.width).toBeLessThanOrEqual(821);
    expect(initialRail.x + initialRail.width).toBeLessThanOrEqual(contentBox.x - 12);

    await toc.locator('[data-mat101-toc-chapter-link][href="#ensembles"]').click();
    await expect(page).toHaveURL(/#ensembles$/);
    await expect(
      toc.locator('[data-mat101-toc-chapter][data-chapter-id="ensembles"]')
    ).toHaveClass(/is-active/);
    const stickyRail = await rail.boundingBox();
    expect(Math.abs(stickyRail.y - initialRail.y)).toBeLessThanOrEqual(1);

    await toc.locator(":scope > summary").click();
    await expect(toc).toHaveAttribute("open", "");

    await page.locator("#telechargements").evaluate((element) =>
      element.scrollIntoView({ block: "start" })
    );
    const stopped = await rail.evaluate((element) => {
      const railBox = element.getBoundingClientRect();
      const downloadsBox = document
        .getElementById("telechargements")
        .getBoundingClientRect();
      return {
        railBottom: railBox.bottom,
        downloadsTop: downloadsBox.top,
      };
    });
    expect(stopped.railBottom).toBeLessThanOrEqual(stopped.downloadsTop + 1);
  });

  test("keeps the compact disclosure keyboard-safe below the rail breakpoint", async ({
    page,
  }) => {
    test.skip(page.viewportSize().width >= 1240, "compact disclosure only");
    await gotoLibrary(page);

    const toc = page.locator("[data-mat101-toc]");
    const summary = toc.locator(":scope > summary");
    await expect(toc).not.toHaveAttribute("open", "");
    await expect(summary).not.toHaveAttribute("aria-disabled", "true");
    await expect(summary).not.toHaveAttribute("tabindex", "-1");
    await summary.click();
    await expect(toc).toHaveAttribute("open", "");
    await expect(toc.locator("[data-mat101-toc-link]")).toHaveCount(103);

    const panelBox = await toc.locator(".mat101-toc-panel").boundingBox();
    expect(panelBox.x).toBeGreaterThanOrEqual(0);
    expect(panelBox.x + panelBox.width).toBeLessThanOrEqual(
      page.viewportSize().width
    );

    await page.keyboard.press("Escape");
    await expect(toc).not.toHaveAttribute("open", "");
    await expect(summary).toBeFocused();

    await summary.click();
    await toc.locator('[data-mat101-toc-link][data-exercise-id="3.16"]').click();
    await expect(toc).not.toHaveAttribute("open", "");
    await expect(page.locator("#exercice-3-16")).toHaveAttribute("open", "");
    await expect(page.locator("#exercice-3-16 > summary")).toBeFocused();

    await summary.click();
    await toc.locator('[data-mat101-toc-chapter-link][href="#limites"]').click();
    await expect(toc).not.toHaveAttribute("open", "");
    await expect(page.locator("#limites")).toBeFocused();
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("keeps the exercise finder clear of the compact navigation", async ({
    page,
  }) => {
    test.skip(page.viewportSize().width >= 1240, "compact navigation only");
    await gotoLibrary(page);

    await page.locator(".mat101-primary-action").click();
    await expect(page).toHaveURL(/#bibliotheque$/);

    const layout = await page.evaluate(() => {
      const navigation = document.querySelector(".mat101-toc");
      const finder = document.getElementById("bibliotheque");
      const navigationBox = navigation.getBoundingClientRect();
      const finderBox = finder.getBoundingClientRect();
      return {
        navigationBottom: navigationBox.bottom,
        finderTop: finderBox.top,
      };
    });

    expect(layout.finderTop).toBeGreaterThanOrEqual(layout.navigationBottom + 8);
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("tracks the reading position without rewriting the URL", async ({ page }) => {
    await gotoLibrary(page);
    await expect(page).toHaveURL(/\/mat101\/exercices\/$/);

    await page.locator("#exercice-3-16").evaluate((element) =>
      element.scrollIntoView({ block: "start" })
    );
    await expect(
      page.locator('[data-mat101-toc-link][data-exercise-id="3.16"]')
    ).toHaveAttribute("aria-current", "location");
    await expect(
      page.locator('[data-mat101-toc-chapter-link][href="#fonctions"]')
    ).toHaveAttribute("aria-current", "location");
    await expect(page).toHaveURL(/\/mat101\/exercices\/$/);

    await page.locator("#exercice-2-5").evaluate((element) =>
      element.scrollIntoView({ block: "start" })
    );
    await expect(
      page.locator('[data-mat101-toc-link][data-exercise-id="2.5"]')
    ).toHaveAttribute("aria-current", "location");
    await expect(
      page.locator('[data-mat101-toc-chapter-link][href="#ensembles"]')
    ).toHaveAttribute("aria-current", "location");
    await expect(page).toHaveURL(/\/mat101\/exercices\/$/);

    await page.evaluate(() => window.scrollTo({ top: 0, behavior: "auto" }));
    await expect(
      page.locator('[data-mat101-toc-link][aria-current="location"]')
    ).toHaveCount(0);
    await expect(
      page.locator('[data-mat101-toc-chapter-link][href="#complexes"]')
    ).toHaveAttribute("aria-current", "location");
    await expect(page).toHaveURL(/\/mat101\/exercices\/$/);
  });

  test("synchronizes search, zero results, and the active rail chapter", async ({
    page,
  }) => {
    await gotoLibrary(page);
    const toc = page.locator("[data-mat101-toc]");
    const input = page.locator("#mat101-search-input");

    await input.fill("suite de nombres réels est périodique");
    await expect(toc.locator("[data-mat101-toc-link]:not([hidden])")).toHaveCount(1);
    await expect(toc.locator("[data-mat101-toc-chapter]:not([hidden])")).toHaveCount(1);
    await expect(
      toc.locator('[data-mat101-toc-chapter][data-chapter-id="limites"]')
    ).toHaveClass(/is-active/);

    await input.fill("aucun exercice ne contient cette recherche xyz");
    await expect(page.locator("[data-mat101-exercise]:visible")).toHaveCount(0);
    await expect(page.locator("#mat101-no-results")).toBeVisible();
    await expect(page.locator("#mat101-result-count")).toHaveText(
      "0 exercices affichés"
    );
    await expect(page.locator("#mat101-toc-current")).toHaveText(
      "0 exercices disponibles"
    );
    await expect(toc.locator("[data-mat101-toc-link]:not([hidden])")).toHaveCount(0);
    await expect(toc.locator("[data-mat101-toc-chapter]:not([hidden])")).toHaveCount(0);
    await expect(toc.locator("[data-mat101-toc-chapter].is-active")).toHaveCount(0);

    await input.fill("");
    await expect(page.locator("[data-mat101-exercise]:visible")).toHaveCount(103);
    await expect(
      toc.locator('[data-mat101-toc-chapter][data-chapter-id="complexes"]')
    ).toHaveClass(/is-active/);
  });

  test("searches the full wording of a statement", async ({ page }) => {
    await gotoLibrary(page);
    await page
      .locator("#mat101-search-input")
      .fill("suite de nombres réels est périodique");

    await expect(page.locator("[data-mat101-exercise]:visible")).toHaveCount(1);
    await expect(page.locator("#exercice-4-12")).toBeVisible();
  });

  test("a deep link clears incompatible filters and keeps the count accurate", async ({
    page,
  }) => {
    await page.goto("/mat101/exercices/?notion=invariants#exercice-3-16");
    await expect(page.locator(".mat101-library")).toBeVisible({ timeout: 12000 });

    await expect(page.locator("[data-mat101-exercise]:visible")).toHaveCount(103);
    await expect(page.locator("#mat101-result-count")).toHaveText(
      "103 exercices affichés"
    );
    await expect(page.locator("#exercice-3-16")).toHaveAttribute("open", "");
    await expect(
      page.locator('[data-mat101-toc-link][data-exercise-id="3.16"]')
    ).toHaveAttribute("aria-current", "location");
    await expect(
      page.locator('[data-mat101-toc-chapter-link][href="#fonctions"]')
    ).toHaveAttribute("aria-current", "location");
    await expect(page).not.toHaveURL(/notion=invariants/);
    await expect(page).toHaveURL(/#exercice-3-16$/);
  });

  test("shows every assigned tag and marks exercises with source errata", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await page.locator("#mat101-search-input").fill("1.18");
    await expect(
      page.locator("#exercice-1-18 .mat101-exercise-tags > span")
    ).toHaveCount(6);

    await page.locator("#mat101-search-input").fill("3.16");
    await expect(
      page.locator("#exercice-3-16 .mat101-erratum-badge")
    ).toHaveText("Erratum source");
  });

  test("keeps statements and corrections usable without JavaScript", async ({
    browser,
  }) => {
    const context = await browser.newContext({ javaScriptEnabled: false });
    const noScriptPage = await context.newPage();
    await noScriptPage.goto("/mat101/exercices/");

    const toc = noScriptPage.locator("[data-mat101-toc]");
    await expect(toc.locator("[data-mat101-toc-link]")).toHaveCount(103);
    if ((await toc.getAttribute("open")) === null) {
      await toc.locator(":scope > summary").click();
    }
    await expect(toc.locator(".mat101-toc-panel")).toBeVisible();

    const exercise = noScriptPage.locator("#exercice-1-1");
    await exercise.locator(":scope > summary").click();
    await expect(
      exercise.locator(".mat101-statement-transcription")
    ).toBeVisible();

    const solution = exercise.locator(".mat101-native-solution");
    await solution.locator(":scope > summary").click();
    await expect(solution.locator(".mat101-solution-body")).toBeVisible();
    await context.close();
  });

  test("renders the complex-number results table with useful row numbers", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await page.locator("#mat101-search-input").fill("1.3");

    const exercise = page.locator("#exercice-1-3");
    await exercise.locator(":scope > summary").click();
    const solution = exercise.locator(".mat101-native-solution");
    await solution.locator(":scope > summary").click();

    const table = solution.locator(".mat101-math-table");
    await expect(table).toBeVisible();
    await expect(table.locator("thead")).toContainText("N°");
    await expect(table.locator(".mat101-row-number")).toHaveCount(13);
    await expect(table.locator(".mat101-row-number").first()).toHaveText("1");
    await expect(table.locator(".mat101-row-number").last()).toHaveText("13");
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("draws the root-of-unity geometry in the relevant solutions", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await page.locator("#mat101-search-input").fill("1.12");

    const rootsExercise = page.locator("#exercice-1-12");
    await rootsExercise.locator(":scope > summary").click();
    const rootsSolution = rootsExercise.locator(".mat101-native-solution");
    await rootsSolution.locator(":scope > summary").click();

    await expect(rootsSolution.locator(".mat101-root-diagram canvas")).toHaveCount(3);
    await expect(rootsSolution.locator(".mat101-root-geometry")).toContainText(
      "polygone régulier"
    );
    expect(await hasHorizontalOverflow(page)).toBe(false);

    await page.locator("#mat101-search-input").fill("1.18");
    const pentagonExercise = page.locator("#exercice-1-18");
    await pentagonExercise.locator(":scope > summary").click();
    const pentagonSolution = pentagonExercise.locator(".mat101-native-solution");
    await pentagonSolution.locator(":scope > summary").click();

    await expect(pentagonSolution.locator(".mat101-root-diagram canvas")).toHaveCount(1);
    await expect(pentagonSolution.locator(".mat101-root-geometry")).toContainText(
      "pentagone régulier"
    );
    await expect(pentagonSolution.locator(".mat101-solution-body")).toContainText(
      "On développe directement le produit demandé"
    );
    await expect(pentagonSolution.locator(".mat101-solution-body")).toContainText(
      "s’annulent deux à deux"
    );
    await expect(pentagonSolution.locator(".mat101-solution-body")).toContainText(
      "racine du polynôme"
    );
    await expect(pentagonSolution.locator(".mat101-solution-body")).not.toContainText(
      "L’identité de la somme géométrique"
    );
    expect(await hasHorizontalOverflow(page)).toBe(false);
  });

  test("keeps provenance and the exercise-specific correction route visible", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await page.locator("#mat101-search-input").fill("1.1");
    const exercise = page.locator("#exercice-1-1");
    await exercise.locator(":scope > summary").click();

    await expect(exercise.locator(".mat101-exercise-footer")).toContainText(
      "Transcription mathématique relue"
    );
    await expect(exercise.locator(".mat101-statement mjx-container")).toHaveCount(
      20
    );
    await expect(
      exercise.getByRole("link", { name: "Consulter la page source" })
    ).toHaveAttribute("href", /recueil-exercices-mat101\.pdf#page=3/);
    await expect(
      exercise.getByRole("link", {
        name: "Signaler une erreur ou proposer une amélioration",
      })
    ).toHaveAttribute(
      "href",
      /template=mat101-correction\.yml.*MAT101.*1\.1/
    );
  });

  test("renders the reviewed fraction and integer interval in exercise 3.3", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await page.locator("#mat101-search-input").fill("3.3");
    const exercise = page.locator("#exercice-3-3");
    await exercise.locator(":scope > summary").click();

    await expect(exercise.locator(".mat101-statement")).toContainText(
      "aucune justification n’est attendue"
    );
    await expect(exercise.locator(".mat101-statement")).not.toContainText("∞ p q");
    await expect(exercise.locator(".mat101-exercise-footer")).toContainText(
      "Transcription mathématique relue"
    );
    await expect(exercise.locator(".mat101-exercise-footer")).toContainText(
      "Vérification effectuée sur le document source"
    );
  });

  test("replaces the dead Napoleon link with an accessible historical note", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await page.locator("#mat101-search-input").fill("1.19");

    const exercise = page.locator("#exercice-1-19");
    await exercise.locator(":scope > summary").click();
    const statement = exercise.locator(".mat101-statement");
    const note = statement.locator(".mat101-statement-note");

    await expect(statement).not.toContainText("node19.html");
    await expect(statement.locator('a[href*="node19.html"]')).toHaveCount(0);
    await expect(note).toContainText("L’appellation est traditionnelle");
    await expect(note).toContainText("n’apparaît qu’en 1911");
    await expect(note).toContainText("problème de Napoléon");
    await expect(
      statement.getByRole("link", {
        name: "Lire la note historique sur l’attribution du théorème",
      })
    ).toHaveAttribute("href", "#mat101-note-1-19-history");
    await expect(note.getByRole("link")).toHaveAttribute(
      "href",
      /fr\.wikipedia\.org.*%C3%89tymologie/
    );
    await expect(statement.locator("mjx-container")).toHaveCount(26);
  });

  test("shows the Polya plan and review only where they aid the reasoning", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await page.locator("#mat101-search-input").fill("2.23");

    const exercise = page.locator("#exercice-2-23");
    await exercise.locator(":scope > summary").click();
    const solution = exercise.locator(".mat101-native-solution");
    await solution.locator(":scope > summary").click();

    await expect(solution.locator(".mat101-method")).toContainText(
      "Idée et plan."
    );
    await expect(solution.locator(".mat101-solution-review")).toContainText(
      "Examen de la solution."
    );

    await page.locator("#mat101-search-input").fill("2.2");
    const routineExercise = page.locator("#exercice-2-2");
    await routineExercise.locator(":scope > summary").click();
    await routineExercise
      .locator(".mat101-native-solution > summary")
      .click();
    await expect(routineExercise.locator(".mat101-method")).toHaveCount(0);
  });

  test("renders the reviewed MathJax statement for exercise 2.23", async ({
    page,
  }) => {
    await gotoLibrary(page);
    await page.locator("#mat101-search-input").fill("2.23");

    const exercise = page.locator("#exercice-2-23");
    await exercise.locator(":scope > summary").click();
    const statement = exercise.locator(".mat101-statement");

    await expect(statement).toContainText("entre deux doigts");
    await expect(statement).toContainText("c’est-à-dire");
    await expect(statement).not.toContainText("centre deux doigts");
    await expect(statement).not.toContainText("repla e");
    await expect(statement.locator("mjx-container")).toHaveCount(3);
    await expect(exercise.locator(".mat101-exercise-footer")).toContainText(
      "Transcription mathématique relue"
    );
    await expect(exercise.locator(".mat101-exercise-footer")).toContainText(
      "Vérification effectuée sur le document source"
    );
  });
});

test.describe("MAT101 visual baselines", () => {
  test("navigation layout @visual", async ({ page }) => {
    await gotoLibrary(page);
    await page.locator(".mat101-reading-note").evaluate((element) =>
      element.scrollIntoView({ block: "start" })
    );
    await expect(page).toHaveScreenshot("mat101-navigation.png");
  });
});
