// Shared utilities for the Rating Lab regression suite.

const fs = require("fs");
const path = require("path");

const DATA_DIR = path.join(__dirname, "..", "..", "assets", "data", "rating-lab");

const manifest = JSON.parse(
  fs.readFileSync(path.join(DATA_DIR, "manifest.json"), "utf8")
);

// Freeze the browser clock a fixed offset after the committed dataset's
// generation time so freshness indicators are deterministic regardless of
// when the suite actually runs.
const FROZEN_TIME = new Date(
  new Date(manifest.generated_at).getTime() + 6 * 60 * 60 * 1000
);

async function freezeClock(page) {
  // setFixedTime pins Date.now()/new Date() while leaving timers running, so
  // rendering code that uses setTimeout/requestAnimationFrame is unaffected.
  await page.clock.setFixedTime(FROZEN_TIME);
}

function readDataFile(name) {
  return JSON.parse(fs.readFileSync(path.join(DATA_DIR, name), "utf8"));
}

// Serve a mutated copy of one data file for a single page, leaving all other
// requests untouched. mutate receives the parsed JSON and returns the object
// to serve (or mutates in place and returns nothing).
async function routeDataFile(page, name, mutate) {
  const original = readDataFile(name);
  const mutated = mutate(original) || original;
  await page.route(`**/assets/data/rating-lab/${name}`, (route) =>
    route.fulfill({
      contentType: "application/json",
      body: JSON.stringify(mutated),
    })
  );
}

// True when the document overflows its viewport horizontally — the core
// "layout is broken at this width" signal.
async function hasHorizontalOverflow(page) {
  return page.evaluate(
    () =>
      document.documentElement.scrollWidth >
      document.documentElement.clientWidth + 1
  );
}

module.exports = {
  manifest,
  FROZEN_TIME,
  freezeClock,
  readDataFile,
  routeDataFile,
  hasHorizontalOverflow,
};
