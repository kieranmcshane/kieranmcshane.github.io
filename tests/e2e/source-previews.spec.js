const { test, expect } = require("@playwright/test");

// These articles live in _drafts/ and must stay out of the built site.
// The facsimile checks that used to render the SHA-1 article now live in
// tests/test_sha_signature_post.py, which reads the unpublished source.
const UNPUBLISHED_ARTICLES = [
  "/2026/07/16/random-quantum-measurements-incompatibility/",
  "/2026/07/17/centered-correlation-tensors-separability/",
  "/2026/07/18/formalizing-xens-correction-in-lean/",
  "/2026/07/18/x-ens-2026-mathematics-b-complete-correction/",
  "/2026/07/27/galois-theory-without-detours/",
  "/2026/07/27/sha1-sha256-certificate-signatures/",
];

test.describe("unpublished articles stay offline", () => {
  for (const url of UNPUBLISHED_ARTICLES) {
    test(`${url} is not served`, async ({ request }) => {
      const response = await request.get(url);
      expect(response.status()).toBe(404);
    });
  }

  test("home, feed, and sitemap do not link to them", async ({ request }) => {
    const home = await request.get("/");
    expect(home.status()).toBe(200);
    const homeBody = await home.text();

    const feed = await request.get("/feed.xml");
    expect(feed.status()).toBe(200);
    const feedBody = await feed.text();

    const sitemap = await request.get("/sitemap.xml");
    expect(sitemap.status()).toBe(200);
    const sitemapBody = await sitemap.text();

    for (const url of UNPUBLISHED_ARTICLES) {
      expect(homeBody).not.toContain(url);
      expect(feedBody).not.toContain(url);
      expect(sitemapBody).not.toContain(url);
    }

    expect(homeBody).not.toContain("post-list");
  });
});
