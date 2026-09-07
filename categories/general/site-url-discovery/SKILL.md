---
name: site-url-discovery
description: "Use to discover and list a site's URLs, with search filtering, when the user knows the site but not the exact page or wants site structure."
license: ISC
tags:
- sitemap
- url-discovery
- web-scraping
---

# firecrawl map

Discover URLs on a site. Use `--search` to find a specific page within a large site.

**Prerequisite:** `map` requires authentication (no keyless free tier); without credentials the CLI prompts an interactive login.

## Quick start

```bash
# Find a specific page on a large site
firecrawl map "<url>" --search "authentication" -o .firecrawl/filtered.txt

# Get all URLs
firecrawl map "<url>" --limit 500 --json -o .firecrawl/urls.json
```

Run `firecrawl map --help` for the full option list (sitemap handling, subdomains, etc.).

**Done when:** the URL list is saved under `.firecrawl/` and you have selected the URLs to scrape or crawl next.

## Tips

- **Map + scrape is a common pattern**: use `map --search` to find the right URL, then `scrape` it.
- Example: `map https://docs.example.com --search "auth"` → found `/docs/api/authentication` → `scrape` that URL.

## See also

- firecrawl-scrape — scrape the URLs you discover
- firecrawl-crawl — bulk extract instead of map + scrape
- firecrawl-download — download entire site (uses map internally)
- [firecrawl-build-search](https://github.com/firecrawl/skills/tree/main/skills/build/firecrawl-build-search) — building URL discovery into an app instead of running it here
