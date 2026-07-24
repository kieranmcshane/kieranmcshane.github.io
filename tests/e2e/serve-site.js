// Minimal static file server for the built Jekyll site.
//
// python -m http.server buckles when several Playwright workers pull the
// multi-megabyte rating datasets concurrently; Node's streaming server
// handles that load without dropped connections.

const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = Number(process.argv[2] || 4173);
const ROOT = path.resolve(__dirname, "..", "..", "_site");

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
  ".txt": "text/plain; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
  ".woff2": "font/woff2",
};

http
  .createServer((req, res) => {
    const urlPath = decodeURIComponent(new URL(req.url, "http://x").pathname);
    let filePath = path.normalize(path.join(ROOT, urlPath));
    if (!filePath.startsWith(ROOT)) {
      res.writeHead(403).end();
      return;
    }
    let stat = fs.statSync(filePath, { throwIfNoEntry: false });
    if (stat && stat.isDirectory()) {
      filePath = path.join(filePath, "index.html");
      stat = fs.statSync(filePath, { throwIfNoEntry: false });
    }
    if (!stat || !stat.isFile()) {
      res.writeHead(404, { "content-type": "text/plain" }).end("not found");
      return;
    }
    res.writeHead(200, {
      "content-type":
        TYPES[path.extname(filePath).toLowerCase()] ||
        "application/octet-stream",
      "content-length": stat.size,
      "cache-control": "no-store",
    });
    fs.createReadStream(filePath).pipe(res);
  })
  .listen(PORT, "127.0.0.1", () => {
    console.log(`serving ${ROOT} on http://127.0.0.1:${PORT}`);
  });
