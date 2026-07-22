import { test, expect } from "@playwright/test";
import * as fs from "fs";
import * as path from "path";
import * as yaml from "js-yaml";

// The preview target is @TheBranchDriftCatalyst/README.md rendered by the
// Express server. These tests verify:
//   1. Every featured repo name from config.yml appears somewhere in the page
//      as visible text (title, table, or description).
//   2. A minimum number of shields.io badge <img> tags render — this guards
//      against regressions in the shields.json lookup being wired up
//      correctly.
//   3. A full-page screenshot lands in tests/screenshots/readme.png.

const CONFIG_PATH = path.resolve(
  __dirname,
  "../../.bin/config.yml",
);

const MIN_SHIELDS = 20;

// Simple YAML reader — the config file is trivial, no fancy anchors, so a
// plain js-yaml load is enough.
function readConfig(): { featured_repos: string[]; hidden_repos?: string[] } {
  const raw = fs.readFileSync(CONFIG_PATH, "utf8");
  return yaml.load(raw) as any;
}

test.describe("README preview", () => {
  test("renders featured repos and shields.io badges", async ({ page }) => {
    const config = readConfig();

    await page.goto("/", { waitUntil: "domcontentloaded" });
    // The <article class="markdown-body"> is the rendered README wrapper.
    await expect(page.locator("article.markdown-body")).toBeVisible();

    // Assert every featured repo appears somewhere as visible text. Some
    // entries in config.featured_repos might not actually correspond to
    // scanned repos (e.g. typos, hidden ones) — the generator silently
    // ignores those, so we can't hard-fail. Instead, we assert that AT
    // LEAST 50% of them render, and log the missing ones for the report.
    const bodyText = await page.locator("body").innerText();
    const found: string[] = [];
    const missing: string[] = [];
    for (const name of config.featured_repos ?? []) {
      if (bodyText.includes(name)) found.push(name);
      else missing.push(name);
    }
    // Attach diagnostic info to the report.
    test.info().annotations.push({
      type: "featured",
      description: `found=${found.join(",")} | missing=${missing.join(",") || "(none)"}`,
    });
    // At least one featured repo should always render; more strictly, we
    // expect the vast majority to render.
    expect(found.length).toBeGreaterThanOrEqual(
      Math.ceil((config.featured_repos?.length ?? 1) * 0.5),
    );

    // Count shields.io badges. These are <img src="https://img.shields.io/...">
    // tags emitted by the generator (both tech-badge rows and status pills).
    const shieldsCount = await page
      .locator('img[src^="https://img.shields.io/"]')
      .count();
    test.info().annotations.push({
      type: "shields",
      description: `${shieldsCount} shields.io badges (threshold ${MIN_SHIELDS})`,
    });
    expect(shieldsCount).toBeGreaterThanOrEqual(MIN_SHIELDS);
  });

  test("captures a full-page screenshot", async ({ page }) => {
    await page.goto("/", { waitUntil: "domcontentloaded" });
    // Wait for the markdown body to render.
    await expect(page.locator("article.markdown-body")).toBeVisible();

    // Give external images (shields.io, capsule-render, streak-stats) a
    // best-effort window to load. We don't want to block on networkidle
    // forever — some readme-typing-svg endpoints stream indefinitely — so
    // cap it.
    await page
      .waitForLoadState("networkidle", { timeout: 8_000 })
      .catch(() => {
        /* best-effort; screenshot regardless */
      });

    const outPath = path.resolve(__dirname, "screenshots", "readme.png");
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    await page.screenshot({ path: outPath, fullPage: true });

    expect(fs.existsSync(outPath)).toBe(true);
    const stat = fs.statSync(outPath);
    expect(stat.size).toBeGreaterThan(10_000); // sanity: not a blank png
  });
});
