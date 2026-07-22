import { defineConfig, devices } from "@playwright/test";

// Playwright config for the README preview app. The webServer block boots
// the Node/Express preview so `npm test` is a one-shot: start server, run
// tests, tear down. No baseURL config file needed for the tests themselves;
// they use PREVIEW_URL below.

const PORT = Number(process.env.PORT ?? 5178);
const BASE_URL = `http://localhost:${PORT}`;

export default defineConfig({
  testDir: "./tests",
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: false, // single preview server, keep tests serial
  workers: 1,
  reporter: [["list"]],
  use: {
    baseURL: BASE_URL,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    // shields.io images can be slow on cold cache — the app itself is
    // static, so a healthy timeout here is fine.
    navigationTimeout: 20_000,
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: {
    command: "node server.js",
    url: `${BASE_URL}/health`,
    reuseExistingServer: !process.env.CI,
    timeout: 20_000,
    stdout: "pipe",
    stderr: "pipe",
    env: { PORT: String(PORT) },
  },
});
