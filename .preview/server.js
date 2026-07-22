// Minimal server that renders the generated profile README with a
// GitHub-dark-mode approximation. Intentionally boring — the goal is a
// faithful preview, not novel art.
//
// Layout:
//   GET /            → HTML shell with rendered README injected
//   GET /raw         → raw README markdown (debug)
//   GET /assets/*    → github-markdown-css, favicon
//
// The README path resolves to ../README.md relative to this file, which
// matches the generator's default output (@TheBranchDriftCatalyst/README.md).

const express = require("express");
const fs = require("fs");
const path = require("path");
const MarkdownIt = require("markdown-it");

const README_PATH = path.resolve(__dirname, "..", "README.md");
const PORT = Number(process.env.PORT) || 5178;

const md = new MarkdownIt({
  html: true, // README contains raw <div>, <img>, <table>, <details>, <br/>
  linkify: true,
  typographer: false,
  breaks: false,
});

// GitHub renders fenced code blocks with syntax highlighting; we're
// intentionally not doing that here — a monospace <pre> block is close
// enough for layout verification, which is what the preview is for.

const shell = (bodyHtml) => `<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>catalyst · README preview</title>
  <link rel="stylesheet" href="/assets/github-markdown-dark.css" />
  <style>
    /* Approximate GitHub's profile page chrome around the .markdown-body. */
    :root {
      --bg-canvas: #0d1117;
      --bg-panel: #010409;
      --fg-default: #e6edf3;
      --border-muted: #30363d;
    }
    html, body {
      margin: 0;
      padding: 0;
      background: var(--bg-canvas);
      color: var(--fg-default);
      font-family:
        -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans",
        Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
      -webkit-font-smoothing: antialiased;
    }
    .page {
      max-width: 1012px; /* GitHub profile README container width */
      margin: 0 auto;
      padding: 32px 16px 96px;
    }
    .frame {
      background: var(--bg-panel);
      border: 1px solid var(--border-muted);
      border-radius: 6px;
      padding: 32px 32px 40px;
    }
    /* github-markdown-css targets .markdown-body; make sure our copy sits
       on the same dark canvas so images with transparent backgrounds don't
       look washed out. */
    .markdown-body {
      background: transparent !important;
      color: var(--fg-default) !important;
      font-size: 16px;
    }
    /* README uses <div align="center">; keep centered blocks centered. */
    .markdown-body div[align="center"] { text-align: center; }
    .markdown-body div[align="center"] img,
    .markdown-body div[align="center"] table { margin-inline: auto; }
    .markdown-body img { max-width: 100%; }
    /* Badge <img> tags from shields.io should inline like text badges do
       on the real GitHub. */
    .markdown-body p img,
    .markdown-body td img { display: inline-block; vertical-align: middle; }
    /* <details><summary><h2> is used for the collapsible catalog; keep the
       h2 inline with the disclosure triangle. */
    .markdown-body details > summary > h2 {
      display: inline-block;
      margin: 0;
      padding-left: 4px;
      border-bottom: none;
    }
    /* Muted footer meta */
    .meta {
      max-width: 1012px;
      margin: 8px auto 0;
      padding: 0 16px;
      color: #7d8590;
      font-size: 12px;
      text-align: right;
    }
  </style>
</head>
<body>
  <main class="page">
    <div class="frame">
      <article class="markdown-body">
${bodyHtml}
      </article>
    </div>
    <div class="meta">
      preview · <a href="/raw" style="color:#7d8590">raw markdown</a>
    </div>
  </main>
</body>
</html>
`;

function readReadme() {
  if (!fs.existsSync(README_PATH)) {
    return "# README.md not found\n\nRun `./generate.sh` from `.bin/` first.";
  }
  return fs.readFileSync(README_PATH, "utf8");
}

const app = express();

app.get("/", (_req, res) => {
  const source = readReadme();
  const html = md.render(source);
  res.set("Cache-Control", "no-store");
  res.type("html").send(shell(html));
});

app.get("/raw", (_req, res) => {
  res.type("text/plain; charset=utf-8").send(readReadme());
});

// Serve the github-markdown-dark.css bundled with github-markdown-css.
app.get("/assets/github-markdown-dark.css", (_req, res) => {
  const cssPath = require.resolve(
    "github-markdown-css/github-markdown-dark.css",
  );
  res.type("text/css").sendFile(cssPath);
});

app.get("/health", (_req, res) => res.json({ ok: true, readme: README_PATH }));

app.listen(PORT, () => {
  console.log(`preview  http://localhost:${PORT}/`);
  console.log(`readme   ${README_PATH}`);
});
