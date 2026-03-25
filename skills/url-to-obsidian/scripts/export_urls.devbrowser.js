function guessSourceType(url) {
  try {
    const { hostname } = new URL(url);
    if (hostname === "mp.weixin.qq.com" || hostname.endsWith(".weixin.qq.com")) {
      return "wechat";
    }
    if (hostname === "github.com" || hostname.endsWith(".github.com")) {
      return "github";
    }
    if (
      hostname === "x.com" ||
      hostname.endsWith(".x.com") ||
      hostname === "twitter.com" ||
      hostname.endsWith(".twitter.com")
    ) {
      return "x";
    }
  } catch {}
  return "web";
}

function uniqueStrings(values, limit = 20) {
  const seen = new Set();
  const result = [];
  for (const value of values) {
    if (typeof value !== "string") {
      continue;
    }
    const trimmed = value.trim();
    if (!trimmed || seen.has(trimmed)) {
      continue;
    }
    seen.add(trimmed);
    result.push(trimmed);
    if (result.length >= limit) {
      break;
    }
  }
  return result;
}

const page = await browser.getPage("url-to-obsidian-export");

let requestedUrls = [];
try {
  let raw = "";
  try {
    raw = await readFile("url-to-obsidian-urls.json");
  } catch {
    raw = "";
  }
  const parsed = JSON.parse(raw);
  if (Array.isArray(parsed)) {
    requestedUrls = parsed.filter((item) => typeof item === "string" && item.trim());
  }
} catch {}

if (requestedUrls.length === 0) {
  throw new Error("No URLs found in url-to-obsidian-urls.json");
}

const items = [];

for (const requestedUrl of requestedUrls) {
  const sourceType = guessSourceType(requestedUrl);

  try {
    await page.goto(requestedUrl);
    await page.waitForTimeout(3500);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(1200);
    await page.evaluate(() => window.scrollBy(0, Math.min(window.innerHeight * 1.5, 1200)));
    await page.waitForTimeout(1400);

    const extracted = await page.evaluate(() => {
      const uniqueStrings = (values, limit = 20) => {
        const seen = new Set();
        const result = [];
        for (const value of values) {
          if (typeof value !== "string") {
            continue;
          }
          const trimmed = value.trim();
          if (!trimmed || seen.has(trimmed)) {
            continue;
          }
          seen.add(trimmed);
          result.push(trimmed);
          if (result.length >= limit) {
            break;
          }
        }
        return result;
      };

      const pickMeta = (...selectors) => {
        for (const selector of selectors) {
          const node = document.querySelector(selector);
          const value = node?.getAttribute("content") || "";
          if (value.trim()) {
            return value.trim();
          }
        }
        return "";
      };

      const root =
        document.querySelector("article") ||
        document.querySelector("main") ||
        document.querySelector("[role='main']") ||
        document.body;

      const text = ((root?.innerText || document.body?.innerText || "").trim()).slice(0, 12000);
      const headings = Array.from(
        document.querySelectorAll("article h1, article h2, article h3, main h1, main h2, main h3, h1, h2, h3"),
      )
        .map((node) => (node.textContent || "").trim())
        .filter(Boolean);

      const links = Array.from(document.querySelectorAll("a[href]"))
        .map((anchor) => anchor.href)
        .filter(Boolean);

      return {
        finalUrl: window.location.href,
        title: document.title || "",
        metaTitle: pickMeta("meta[property='og:title']", "meta[name='twitter:title']"),
        metaDescription: pickMeta(
          "meta[name='description']",
          "meta[property='og:description']",
          "meta[name='twitter:description']",
        ),
        publishedTime: pickMeta("meta[property='article:published_time']", "meta[name='publishdate']"),
        siteName: pickMeta("meta[property='og:site_name']"),
        headings: uniqueStrings(headings, 12),
        links: uniqueStrings(links, 20),
        excerpt: text,
      };
    });

    items.push({
      key: extracted.finalUrl || requestedUrl,
      requestedUrl,
      finalUrl: extracted.finalUrl || requestedUrl,
      sourceType: guessSourceType(extracted.finalUrl || requestedUrl),
      title: extracted.title,
      metaTitle: extracted.metaTitle,
      metaDescription: extracted.metaDescription,
      siteName: extracted.siteName,
      headings: extracted.headings,
      links: extracted.links,
      excerpt: extracted.excerpt,
      publishedTime: extracted.publishedTime,
      capturedAt: new Date().toISOString(),
    });
  } catch (error) {
    items.push({
      key: requestedUrl,
      requestedUrl,
      finalUrl: requestedUrl,
      sourceType,
      title: "",
      metaTitle: "",
      metaDescription: "",
      siteName: "",
      headings: [],
      links: [],
      excerpt: "",
      publishedTime: "",
      capturedAt: new Date().toISOString(),
      error: String(error),
    });
  }
}

const savedPath = await writeFile("url-to-obsidian-export.json", JSON.stringify(items, null, 2));
console.log(
  JSON.stringify(
    {
      count: items.length,
      savedPath,
    },
    null,
    2,
  ),
);
