// Playwright configuration for Rating Lab visual and interaction regression.
//
// Three viewport projects (mobile 390, tablet 768, desktop 1280) run the same
// specs against the statically served Jekyll build in _site/.
//
// Screenshot assertions (@visual) compare against Linux baselines committed
// under __screenshots__/. They only run in CI (Linux) so that local macOS
// runs do not fight font-rendering differences; local runs still execute
// every behavioral assertion.

const { defineConfig, devices } = require("@playwright/test");

const PORT = 4173;

module.exports = defineConfig({
  testDir: ".",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 1,
  // The static file server struggles when many workers pull multi-megabyte
  // JSON payloads at once; cap local parallelism to keep runs stable.
  workers: process.env.CI ? undefined : 4,
  reporter: process.env.CI ? [["list"], ["html", { open: "never" }]] : "list",
  timeout: 60000,
  expect: {
    timeout: 10000,
    toHaveScreenshot: {
      animations: "disabled",
      caret: "hide",
      maxDiffPixelRatio: 0.002,
    },
  },
  snapshotPathTemplate:
    "{testDir}/__screenshots__/{projectName}/{arg}{ext}",
  ignoreSnapshots: !process.env.CI,
  use: {
    baseURL: `http://127.0.0.1:${PORT}`,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    timezoneId: "Europe/Paris",
    locale: "en-US",
  },
  webServer: {
    command: `node serve-site.js ${PORT}`,
    url: `http://127.0.0.1:${PORT}/rating-lab/`,
    reuseExistingServer: !process.env.CI,
    timeout: 30000,
  },
  projects: [
    {
      name: "mobile-390",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 390, height: 844 },
        hasTouch: true,
        isMobile: true,
      },
    },
    {
      name: "tablet-768",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 768, height: 1024 },
      },
    },
    {
      name: "desktop-1280",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 1280, height: 900 },
      },
    },
  ],
});
