# URL Fetch Layer

Three strategies in escalating order of complexity. Use the simplest that works.

## Strategy 1: trafilatura (default for static pages)

```python
import trafilatura

def fetch_url(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise ValueError(f"Could not fetch {url}")
    text = trafilatura.extract(downloaded, include_tables=True, include_links=True)
    if not text:
        raise ValueError(f"No content extracted from {url}")
    return text
```

Returns clean article text with boilerplate stripped. Pass the result to `markitdown.convert_stream()` or write to a temp `.html` file then convert.

Best for: news articles, blog posts, documentation pages, any static HTML.

## Strategy 2: Playwright (JS-rendered pages)

Use when trafilatura returns empty or the page requires JavaScript (SPAs, dashboards, login-gated content with session access).

```python
from playwright.sync_api import sync_playwright

def fetch_js_page(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        html = page.content()
        browser.close()
    return html
```

Pass the returned HTML to markitdown for conversion.

Install:

```bash
uv pip install playwright && playwright install chromium
```

## Strategy 3: Authenticated session (user-managed)

Not automated by this skill. The pattern: user provides cookies or session storage, inject into Playwright browser context.

```python
context = browser.new_context(storage_state="auth.json")
```

Out of scope for general use. Point to [Playwright authentication docs](https://playwright.dev/python/docs/auth) if the user needs this.

## Selection Logic

```text
URL received
  Is YouTube URL?           -> skip fetch, markitdown handles directly
  Try trafilatura fetch
    Content extracted?      -> use it
    Empty/failed?           -> try Playwright
      Playwright succeeds?  -> use it
      Still empty?          -> report failure to user
```

## Paywall Handling

**This skill does not bypass paywalls.** Both trafilatura and Playwright return the regwall/paywall page for paywalled content. This is a fetch-layer limitation — no conversion tool solves it.

When the fetched content looks like a paywall page (short content, login prompts, subscription CTAs), report this clearly to the user:
- "The page returned a paywall. The conversion contains the paywall page, not the article."
- Do not retry or attempt workarounds.
