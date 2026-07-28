/**
 * Rebuild the primary-source facsimiles used by the SHA article.
 *
 * Run from the repository root after installing tests/e2e dependencies:
 *
 *   npm --prefix tests/e2e ci
 *   node assets/code/build_sha_source_facsimiles.mjs
 *
 * The yellow overlays are editorial highlights; the underlying text and
 * typography are captured directly from the linked source pages.
 */

import fs from "node:fs/promises";
import { execFile } from "node:child_process";
import path from "node:path";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import { chromium } from "../../tests/e2e/node_modules/playwright/index.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(scriptDir, "../..");
const outputDir = path.join(repoRoot, "assets/images/source-excerpts");
const temporaryDir = path.join(repoRoot, "tmp/source-facsimiles");
const runFile = promisify(execFile);

const highlightColor = "rgba(250, 209, 72, 0.38)";
const highlightOutline = "rgba(173, 125, 0, 0.36)";

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(temporaryDir, { recursive: true });

const browser = await chromium.launch({ headless: true });

async function newPage() {
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1100 },
    deviceScaleFactor: 2,
    colorScheme: "light",
  });
  await page.emulateMedia({ colorScheme: "light", reducedMotion: "reduce" });
  return page;
}

async function saveNistTable() {
  const page = await newPage();
  await page.goto("https://csrc.nist.gov/Projects/hash-functions", {
    waitUntil: "networkidle",
    timeout: 60_000,
  });

  const cell = page.getByRole("cell", { name: "SHA-256", exact: true });
  const row = cell.locator("xpath=ancestor::tr");
  const table = row.locator("xpath=ancestor::table");
  await row.scrollIntoViewIfNeeded();

  await row.evaluate(
    (element, colors) => {
      element.style.background = colors.fill;
      element.style.boxShadow = `inset 0 0 0 2px ${colors.outline}`;
    },
    { fill: highlightColor, outline: highlightOutline }
  );

  const tableBox = await table.boundingBox();
  const rowBox = await row.boundingBox();
  if (!tableBox || !rowBox) throw new Error("NIST table bounds unavailable");

  await page.screenshot({
    path: path.join(outputDir, "sha256-nist-security-strengths.png"),
    clip: {
      x: tableBox.x,
      y: tableBox.y,
      width: tableBox.width,
      height: rowBox.y + rowBox.height - tableBox.y,
    },
  });
  await page.close();
}

async function preTextRect(pre, text) {
  return pre.evaluate((element, wanted) => {
    const content = element.textContent || "";
    const start = content.indexOf(wanted);
    if (start < 0) throw new Error(`Text not found: ${wanted}`);

    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
    let offset = 0;
    let startNode = null;
    let startOffset = 0;
    let endNode = null;
    let endOffset = 0;

    while (walker.nextNode()) {
      const node = walker.currentNode;
      const length = node.textContent.length;
      if (!startNode && start <= offset + length) {
        startNode = node;
        startOffset = start - offset;
      }
      const end = start + wanted.length;
      if (startNode && end <= offset + length) {
        endNode = node;
        endOffset = end - offset;
        break;
      }
      offset += length;
    }

    if (!startNode || !endNode) throw new Error(`Range unavailable: ${wanted}`);
    const range = document.createRange();
    range.setStart(startNode, startOffset);
    range.setEnd(endNode, endOffset);
    const rect = range.getBoundingClientRect();
    const style = getComputedStyle(element);
    const parsedLineHeight = Number.parseFloat(style.lineHeight);
    const lineHeight = Number.isFinite(parsedLineHeight)
      ? parsedLineHeight
      : Number.parseFloat(style.fontSize) * 1.2;
    return {
      x: rect.x,
      y: rect.y,
      width: rect.width,
      height: rect.height,
      lineHeight,
    };
  }, text);
}

async function addHighlight(page, rect) {
  await page.evaluate(
    ({ box, fill, outline }) => {
      const overlay = document.createElement("div");
      Object.assign(overlay.style, {
        position: "absolute",
        left: `${box.x - 4 + window.scrollX}px`,
        top: `${box.y - 2 + window.scrollY}px`,
        width: `${box.width + 8}px`,
        height: `${box.height + 4}px`,
        background: fill,
        boxShadow: `inset 0 0 0 1px ${outline}`,
        pointerEvents: "none",
        zIndex: "1000",
      });
      document.body.appendChild(overlay);
    },
    { box: rect, fill: highlightColor, outline: highlightOutline }
  );
}

async function saveRfcExcerpt({
  url,
  pageText,
  highlights,
  fileName,
  beforeLines,
  afterLines,
  clipWidth,
}) {
  const page = await newPage();
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60_000 });
  const candidates = page.locator("pre.newpage").filter({ hasText: pageText });
  const count = await candidates.count();
  if (count !== 1) {
    throw new Error(`${fileName}: expected one source page, found ${count}`);
  }
  const pre = candidates;
  let rects = [];
  for (const text of highlights) {
    rects.push(await preTextRect(pre, text));
  }
  await page.evaluate((targetY) => {
    window.scrollTo({ top: window.scrollY + targetY - 260, behavior: "instant" });
  }, rects[0].y);
  rects = [];
  for (const text of highlights) {
    rects.push(await preTextRect(pre, text));
  }
  for (const rect of rects) await addHighlight(page, rect);

  const preBox = await pre.boundingBox();
  if (!preBox) throw new Error(`${fileName}: page bounds unavailable`);
  const lineHeight = rects[0].lineHeight;
  const top = Math.max(preBox.y, rects[0].y - beforeLines * lineHeight);
  const bottom = Math.min(
    preBox.y + preBox.height,
    rects.at(-1).y + rects.at(-1).height + afterLines * lineHeight
  );

  await page.screenshot({
    path: path.join(outputDir, fileName),
    clip: {
      x: preBox.x,
      y: top,
      width: Math.min(preBox.width, clipWidth ?? preBox.width),
      height: bottom - top,
    },
  });
  await page.close();
}

async function saveAppleRequirement() {
  const page = await newPage();
  await page.goto("https://support.apple.com/en-gb/103769", {
    waitUntil: "networkidle",
    timeout: 60_000,
  });

  const paragraph = page
    .locator("p")
    .filter({ hasText: "must use a hash algorithm from the SHA-2 family" });
  const count = await paragraph.count();
  if (count !== 1) throw new Error(`Apple requirement matches: ${count}`);
  await paragraph.scrollIntoViewIfNeeded();

  await paragraph.evaluate(
    (element, colors) => {
      element.style.background = colors.fill;
      element.style.boxShadow = `0 0 0 6px ${colors.fill}, inset 0 0 0 1px ${colors.outline}`;
    },
    { fill: highlightColor, outline: highlightOutline }
  );

  const box = await paragraph.boundingBox();
  if (!box) throw new Error("Apple requirement bounds unavailable");
  await page.screenshot({
    path: path.join(outputDir, "sha256-apple-tls-requirement.png"),
    clip: {
      x: Math.max(0, box.x - 24),
      y: Math.max(0, box.y - 6),
      width: Math.min(1100, box.width + 48),
      height: box.height + 12,
    },
  });
  await page.close();
}

async function saveShatteredAbstract() {
  const pdfPath = path.join(temporaryDir, "shattered.pdf");
  const pagePrefix = path.join(temporaryDir, "shattered-page-1");
  const response = await fetch("https://shattered.io/static/shattered.pdf");
  if (!response.ok) {
    throw new Error(`SHAttered download failed: ${response.status}`);
  }
  await fs.writeFile(pdfPath, Buffer.from(await response.arrayBuffer()));

  await runFile("pdftoppm", [
    "-f",
    "1",
    "-singlefile",
    "-png",
    "-r",
    "180",
    pdfPath,
    pagePrefix,
  ]);

  await runFile("ffmpeg", [
    "-y",
    "-hide_banner",
    "-loglevel",
    "error",
    "-i",
    `${pagePrefix}.png`,
    "-vf",
    [
      "crop=1070:930:210:120",
      // Highlight only the two claims quoted by the article: practicality
      // and the measured computational effort. Avoid starting mid-sentence
      // or highlighting the separate PDF-construction claim.
      "drawbox=x=35:y=632:w=1000:h=27:color=yellow@0.28:t=fill",
      "drawbox=x=35:y=659:w=570:h=30:color=yellow@0.28:t=fill",
      "drawbox=x=575:y=768:w=425:h=28:color=yellow@0.28:t=fill",
      "drawbox=x=35:y=796:w=445:h=28:color=yellow@0.28:t=fill",
    ].join(","),
    "-frames:v",
    "1",
    path.join(outputDir, "sha1-shattered-abstract.png"),
  ]);
}

await saveNistTable();
await saveShatteredAbstract();
await saveRfcExcerpt({
  url: "https://www.rfc-editor.org/rfc/rfc8017.html#section-9.2",
  pageText: "EM = 0x00 || 0x01 || PS || 0x00 || T",
  highlights: [
    "digestAlgorithm AlgorithmIdentifier",
    "EM = 0x00 || 0x01 || PS || 0x00 || T",
  ],
  fileName: "sha256-rfc8017-encoding.png",
  beforeLines: 5,
  afterLines: 2,
  // The RFC's <pre> spans the browser viewport although the relevant text
  // occupies only its left side. Cropping the empty right margin keeps the
  // source legible when the image is fitted to the article column.
  clipWidth: 700,
});
await saveRfcExcerpt({
  url: "https://www.rfc-editor.org/rfc/rfc5280.html#section-4.1",
  pageText: "The X.509 v3 certificate basic syntax is as follows",
  highlights: ["tbsCertificate       TBSCertificate"],
  fileName: "sha256-rfc5280-certificate.png",
  beforeLines: 4,
  afterLines: 5,
});
await saveAppleRequirement();

await browser.close();
