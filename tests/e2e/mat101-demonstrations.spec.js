const { test, expect } = require("@playwright/test");
const { hasHorizontalOverflow } = require("./helpers");

test.describe("MAT101 essential demonstrations", () => {
  test("renders all demonstrations with MathJax and without overflow", async ({
    page,
  }) => {
    const consoleErrors = [];
    page.on("pageerror", (error) => consoleErrors.push(error.message));
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
    await expect(page.locator(".mat101-demonstrations mjx-container").first()).toBeVisible();
    await expect(page.locator("mjx-merror")).toHaveCount(0);
    expect(await hasHorizontalOverflow(page)).toBe(false);
    expect(consoleErrors).toEqual([]);
  });

  test("keeps every proof in its own card without leaking HTML", async ({ page }) => {
    await page.goto("/mat101/demonstrations/");
    await expect(page.locator(".mat101-demonstration-card .mat101-demonstration-card")).toHaveCount(0);
    await expect(page.locator(".mat101-demonstrations > .mat101-demonstrations-chapter")).toHaveCount(4);
    await expect(page.locator("#complexes > .mat101-demonstrations-list > article")).toHaveCount(3);
    await expect(page.locator("#fonctions > .mat101-demonstrations-list > article")).toHaveCount(4);
    await expect(page.locator("#suites > .mat101-demonstrations-list > article")).toHaveCount(2);
    await expect(page.locator(".mat101-demonstrations")).not.toContainText("</");
    await expect(page.locator(".mat101-demonstrations-count")).toHaveText(
      "9 démonstrations dans 3 chapitres du cours"
    );
  });

  test("all formula edges are reachable without clipping", async ({ page }, testInfo) => {
    await page.goto("/mat101/demonstrations/");
    await page.waitForFunction(() => window.MathJax?.startup?.document?.math);
    await page.evaluate(() => window.MathJax.startup.promise);
    await expect(page.locator('#demo-3-38 mjx-container[display="true"]').first())
      .toHaveCSS("text-align", "left");
    const clipped = await page.locator('.mat101-demonstrations mjx-container[display="true"]')
      .evaluateAll((containers) => containers.flatMap((container) => {
        const math = container.querySelector("mjx-math");
        if (!math) return ["Missing rendered formula"];
        container.scrollLeft = 0;
        const left = math.getBoundingClientRect().left;
        const box = container.getBoundingClientRect();
        container.scrollLeft = container.scrollWidth;
        const right = math.getBoundingClientRect().right;
        container.scrollLeft = 0;
        return left < box.left - 2 || right > box.right + 2
          ? [container.closest("article")?.id + ": " + math.textContent] : [];
      }));
    expect(clipped).toEqual([]);
    for (const id of ["1-3", "3-38", "3-40", "4-13"]) {
      await page.locator("#demo-" + id).screenshot({
        path: testInfo.outputPath("demo-" + id + ".png"),
      });
    }
  });

  test("all contents links navigate to the correct visible card", async ({ page }) => {
    await page.goto("/mat101/demonstrations/");
    const links = page.locator('.mat101-demonstrations-toc a[href^="#demo-"]');
    await expect(links).toHaveCount(9);
    for (const link of await links.all()) {
      const target = await link.getAttribute("href");
      await link.click();
      await expect(page).toHaveURL(new RegExp(target + "$"));
      await expect(page.locator(target)).toBeInViewport();
    }
  });

  test("a direct proof link stays aligned after math rendering", async ({ page }) => {
    await page.goto("/mat101/demonstrations/#demo-3-38");
    await page.waitForFunction(() => window.MathJax?.startup?.document?.math);
    await page.evaluate(() => window.MathJax.startup.promise);
    await expect(page.locator("#demo-3-38 .mat101-demonstration-header")).toBeInViewport();
  });

  test("statements and proofs remain readable without JavaScript", async ({ browser, baseURL }) => {
    const context = await browser.newContext({ javaScriptEnabled: false });
    const page = await context.newPage();
    await page.goto(baseURL + "/mat101/demonstrations/");
    await expect(page.locator(".mat101-demonstration-proof")).toHaveCount(9);
    await expect(page.locator("#demo-3-38")).toContainText("Hérédité.");
    await expect(page.locator("#demo-4-14")).toContainText("converge vers");
    await expect(page.locator(".mat101-demonstrations")).not.toContainText("</");
    await context.close();
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
