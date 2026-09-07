---
name: agent-friendly-web-content
description: "Use when building or launching websites, landing pages, or docs sites so AI agents read them cheaply by shipping clean Markdown mirrors, meta tags, JSON-LD, and an llms.txt index."
license: MIT
tags:
- markdown
- llms-txt
- ai-crawlers
- documentation
- structured-data
---

# Markdown for Agents

## What it is

AI agents parse Markdown far more reliably than HTML: explicit structure means better results and less token waste. On real sites, the HTML-to-Markdown difference is an order of magnitude — Cloudflare's own example shows ~725 tokens for the Markdown version of a page whose HTML carried ~12,345 tokens. This skill makes every page you build ship a clean Markdown version agents can read cheaply and correctly.

**Core principle: structure is the feature.** A Markdown version saves tokens only if it is *clean* — real heading hierarchy, prose stripped of nav/footer/scripts, frontmatter metadata, and preserved JSON-LD. A dump of raw HTML wrapped in backticks saves nothing.

## When to use

Activate this skill when any of the following is true:

- You are building, launching, or redesigning a website, landing page, or docs site.
- The site may be consumed by AI agents, LLM crawlers, or AI search tools.
- The user wants to reduce token costs for AI systems reading their content.
- The user mentions "Markdown for Agents", "llms.txt", "AI crawlers", "AI-ready site", or "let agents read my site efficiently".
- A page already exists but has no meta tags, no JSON-LD, or no Markdown-accessible version.

Do NOT activate this skill for general SEO keyword work, visual design, or pure frontend build tasks with no public content.

## Instructions

Run these phases in order. Skip Phase 4 (Cloudflare) unless the site is hosted on Cloudflare with a Pro or Business plan.

### Phase 1 — Meta foundation

Every page gets all three meta tags. They become the YAML frontmatter of the converted Markdown, and without them the frontmatter block is omitted entirely.

```html
<meta name="title" content="Markdown for Agents · Cloudflare Docs">
<meta name="description" content="A short, accurate summary of this page.">
<meta property="og:image" content="https://example.com/cover.png">
```

- `title` and `description`: prefer the standard `<meta name="...">` form; Open Graph (`og:`) values are only fallbacks.
- Write the title and description as real copy an agent can trust — no clickbait, no keyword stuffing.
- `image` is optional; include it when the page has a meaningful cover.

### Phase 2 — JSON-LD structured data

Add one or more `<script type="application/ld+json">` blocks per page with the schema types that fit: `Organization`, `WebSite`, `WebPage`, `Article`, `Product`, `FAQPage`, `BreadcrumbList`, etc. JSON-LD is the only script content preserved in Markdown conversion — it is appended verbatim at the end of the output inside a single fenced `json` block.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "description": "A short, accurate summary.",
  "author": { "@type": "Person", "name": "Jane Doe" },
  "datePublished": "2026-01-15",
  "image": "https://example.com/cover.png"
}
</script>
```

- Multiple JSON-LD scripts are concatenated into the one code block, each on its own line.
- Validate with Google's Rich Results Test or Schema.org validator.

### Phase 3 — Serve the Markdown (provider-neutral, default)

For every page, generate a static Markdown mirror an agent can fetch directly. This works on any host — no Cloudflare required.

**Naming:** expose each page as `/{page}.md` (or `/page.md` at the root of a single-page site). Keep the URL identical to the HTML version minus the extension so agents can find it predictably.

**What the Markdown must contain:**
- YAML frontmatter with `title` and `description` (from Phase 1).
- The page content as clean Markdown: proper `#`/`##`/`###` heading hierarchy matching the visible page, prose as paragraphs, lists as real bullets.
- The JSON-LD from Phase 2 appended at the end in a fenced `json` block.
- **Nothing else.** Strip header, footer, navigation, scripts, styles, widgets, and cookie banners — same stripping an edge converter performs.

**Delivery:**
- Serve with `Content-Type: text/markdown; charset=utf-8`.
- Cache the Markdown mirror aggressively: `Cache-Control: max-age=31536000, immutable` if content is immutable; otherwise a short TTL with revalidation, same as the HTML page.
- Where practical, also honor content negotiation: if a client sends `Accept: text/markdown`, respond with the Markdown version instead of HTML.

**If content is generated dynamically:** render the Markdown server-side from the same content model that produces the HTML (SSR or build step), never as an afterthought that can drift from the live page.

### Phase 4 — Cloudflare Markdown for Agents (optional)

If the site is on Cloudflare with a Pro, Business, or Enterprise plan, you can let Cloudflare convert HTML to Markdown at the edge instead of maintaining static mirrors.

**Enable via dashboard:**
1. Cloudflare dashboard → select the zone → **AI Crawl Control** section.
2. Enable **Markdown for Agents**.

**Enable for specific subdomains/paths:** Rules → Configuration Rules → match expression (e.g. `http.host eq "docs.example.com"` or `starts_with(http.request.uri.path, "/blog/")`) → setting **Markdown for Agents** → On.

**Enable via API:**
```bash
curl -X PATCH 'https://api.cloudflare.com/client/v4/zones/{zone_tag}/settings/content_converter' \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer {api_token}" --data-raw '{"value": "on"}'
```

**Verify** the conversion works (see Phase 5) before treating this as done. Note the 2 MB origin-response limit and that only HTML is converted.

### Phase 5 — Verify

For each representative page, confirm the Markdown output is clean and token-efficient.

```bash
curl https://example.com/some-page \
  -H "Accept: text/markdown"
```

Check the response:
- `Content-Type` is `text/markdown; charset=utf-8`.
- YAML frontmatter with `title` and `description` is present at the top.
- The body reads as clean Markdown with real heading hierarchy — no stray `<div>`, `class=`, or inline styles.
- JSON-LD appears at the end inside a fenced `json` block.
- Token savings are real: compare `x-markdown-tokens` against `x-original-tokens` (present on Cloudflare-converted responses) — the Markdown should be a fraction of the HTML token count.
- The `content-signal` header allows use: default is `ai-train=yes, search=yes, ai-input=yes`; preserve any origin-set value as authoritative.

If any check fails, fix the page (usually a missing meta tag, heavy markup in the body, or no JSON-LD) and re-verify.

### Phase 6 — Sitemap and discoverability

- Add each Markdown mirror's URL to the XML sitemap (alongside its HTML twin).
- Serve an `/llms.txt` index that lists the Markdown pages (see "The `/llms.txt` file" below).
- Submit the sitemap to Google Search Console so AI crawlers and search engines index the agent-friendly versions.

## The `/llms.txt` file

An `/llms.txt` file is the site-level index for LLMs: a single markdown file at the root path (`/llms.txt`) that gives a short summary of the site and links to the clean markdown pages agents should read. It is a community proposal by AnswerDotAI (Jeremy Howard), Apache-2.0, published September 2024 at llmstxt.org. It standardizes a path (like `/robots.txt`) so any agent can find the curated content without crawling HTML.

The spec defines the file contents, in this order:

1. **H1** — the name of the project or site. This is the only required section.
2. **A blockquote** — a short summary containing the key information needed to understand the rest of the file.
3. **Zero or more markdown sections** (paragraphs, lists) of any type except headings — more detail about the project and how to interpret the files.
4. **Zero or more H2 sections** containing "file lists" of URLs where further detail is available. Each file list is a markdown list of hyperlinks `[name](url)`, optionally followed by `:` and notes.

The `## Optional` section has special meaning: URLs there can be skipped if a shorter context is needed. Use it for secondary information.

Mock example:

```text
# Title

> Optional description goes here

Optional details go here

## Section name

- [Link title](https://link_url): Optional link details

## Optional

- [Link title](https://link_url)
```

Guidelines from the spec for an effective `/llms.txt`:

- Use concise, clear language.
- When linking to resources, include brief, informative descriptions.
- Avoid ambiguous terms or unexplained jargon.
- Run a tool that expands the index into an LLM context file and test whether models can answer questions about your content.

Tools and plugins:

- `llms_txt2ctx` (pip, from the AnswerDotAI repo) — parses `/llms.txt` and expands linked pages into a single LLM context file.
- `vitepress-plugin-llms` — generates an llms.txt file for VitePress docs sites.
- `docusaurus-plugin-llms` — generates an llms.txt file for Docusaurus docs sites.

### Relationship: `/llms.txt` vs page-level delivery

The two approaches compose; one is not a replacement for the other.

| Concern | `/llms.txt` | Page-level phases (1–3) |
|---|---|---|
| Scope | Site index: one file pointing at the important pages | Per-page delivery: every page is AI-readable |
| Headers | None — plain markdown links | Meta tags, JSON-LD, YAML frontmatter |
| Role | "Here is the site, start with these pages" | "Here is exactly this page, clean and cheap" |
| Composition | Lists the `.md` mirrors as its file lists | Produces the `.md` mirrors the index links to |

Ship both: Phases 1–3 make each page a clean `.md` mirror; the `/llms.txt` file curates which mirrors matter and in what order.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Missing `<meta name="title">`/`description` | Frontmatter block is omitted entirely — no metadata for agents. Add Phase 1 tags. |
| Wrapping raw HTML in a Markdown file | Saves no tokens; agents still parse HTML. Convert to real Markdown structure. |
| Including nav, footer, scripts, cookie banners in the Markdown | Wasted tokens and noise. Strip everything non-content (Phase 3). |
| Heading hierarchy that drifts from the visible page | Agents trust the Markdown structure — keep it identical to the rendered page. |
| No JSON-LD | Structured data is lost on conversion. Add per-page schema (Phase 2). |
| Static mirrors that go stale | Render from the same content model as the HTML; never maintain by hand. |
| Forgetting cache headers | Every agent fetch re-renders/hits origin. Cache the Markdown mirror. |
| Assuming Cloudflare is required | The provider-neutral core (Phases 1–3, 5–6) works on any host. |

## Exit Checklist

- [ ] Every page has `title`, `description`, and (where relevant) `og:image` meta tags
- [ ] Every page carries valid JSON-LD structured data
- [ ] Each page is reachable as clean Markdown (`/{page}.md` or `Accept: text/markdown` on Cloudflare)
- [ ] Markdown contains only frontmatter, content, and JSON-LD — no boilerplate
- [ ] Token savings verified: `x-markdown-tokens` is a small fraction of `x-original-tokens`
- [ ] Markdown URLs are in the sitemap and submitted to Search Console
- [ ] An `/llms.txt` index exists, follows the spec order, and links to the Markdown mirrors

## Related skills

- `technical-writer` — writes the docs-site content (Docusaurus/VitePress/MkDocs frontmatter and navigation) that pairs with `/llms.txt` generation.
- `code-documenter` — for docstrings and OpenAPI specs that feed API reference pages.
