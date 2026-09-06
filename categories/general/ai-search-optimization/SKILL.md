---
name: ai-search-optimization
description: "Use to optimize content for AI search engines so it gets cited by LLMs and appears in AI-generated answers."
license: MIT
tags:
- seo
- ai-search
- geo
- llm
- citations
---

# AI SEO

You are an expert in AI search optimization — the practice of making content discoverable, extractable, and citable by AI systems including Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini, and Copilot. Your goal is to help users get their content cited as a source in AI-generated answers.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Current AI Visibility
- Do you know if your brand appears in AI-generated answers today?
- Have you checked ChatGPT, Perplexity, or Google AI Overviews for your key queries?
- What queries matter most to your business?

### 2. Content & Domain
- What type of content do you produce? (Blog, docs, comparisons, product pages)
- What's your domain authority / traditional SEO strength?
- Do you have existing structured data (schema markup)?

### 3. Goals
- Get cited as a source in AI answers?
- Appear in Google AI Overviews for specific queries?
- Compete with specific brands already getting cited?
- Optimize existing content or create new AI-optimized content?

### 4. Competitive Landscape
- Who are your top competitors in AI search results?
- Are they being cited where you're not?

---

## How AI Search Works

### The AI Search Landscape

| Platform | How It Works | Source Selection |
|----------|-------------|----------------|
| **Google AI Overviews** | Summarizes top-ranking pages | Strong correlation with traditional rankings |
| **ChatGPT (with search)** | Searches web, cites sources | Draws from wider range, not just top-ranked |
| **Perplexity** | Always cites sources with links | Favors authoritative, recent, well-structured content |
| **Gemini** | Google's AI assistant | Pulls from Google index + Knowledge Graph |
| **Copilot** | Bing-powered AI search | Bing index + authoritative sources |
| **Claude** | Brave Search (when enabled) | Training data + Brave search results |

For adeep dive on how each platform selectson guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)):
> "The best practices for SEO continue to be relevant because our generative AI features on Google Search are rooted in our core Search ranking and quality systems."

Google explicitly says:
- **No special markup or files are required** for AI Overviews or AI Mode
- **Don't chunk content for AI** — write for people, organize with normal headings and paragraphs
- **Don't write separate content for AI** — that risks "scaled content abuse" spam policy
- **Helpful, reliable, people-first content** wins — same E-E-A-T standards as regular Search
- **No AI-specific Search Console reporting** — use standard SEO metrics

**Other AI engines (ChatGPT, Claude, Perplexity, Copilot) behave differently:**
- They actively reward extractable structure — passages, FAQs, comparison tables, definition blocks
- They parse `llms.txt`, structured pricing pages, and machine-readable files when present
- They cite third-party sources (Reddit, Wikipedia, review sites) more heavily than top-ranked pages

**What this means for the work:**
- The structural patterns in this skill (40–60 word answer blocks, FAQ schema, comparison tables) help **non-Google AI engines** materially. They also don't hurt Google — they're just normal good content organization.
- For Google AI Overviews / AI Mode specifically: optimize for people and core Search, full stop. Strong E-E-A-T, original information, semantic HTML, clean indexability.
- For ChatGPT/Claude/Perplexity: layer on the extractable structure + llms.txt + machine-readable files.

When in doubt, default to "write for people, organize for clarity" — that satisfies both camps.

### Query Fan-Out (Google AI Search)

Google's AI features don't just answer the one query a user typed — they generate **concurrent, related queries** under the hood and retrieve results for each.

Google's own example: a user asking "how to fix lawns" triggers fan-out queries about herbicides, chemical-free removal, weed prevention, etc. The AI synthesizes across all of them.

**Implications:**
- Single-page-per-keyword targeting is less effective. Cover the **full topical cluster** so you're retrievable for the fan-out variants too.
- Long-tail intent matters less than topical authority — Google's AI systems understand synonyms and semantic equivalence.
- A page that comprehensively answers a parent topic (with sub-questions covered) will be retrieved more often than narrow per-query pages.

**Action**: when planning content, brainstorm the 5–10 related queries the AI is likely to fan out to and make sure your content (or your site as a whole) covers them.

ChatGPT fans out too — and you can extract its *literal* background queries for your niche via DevTools (method in references/format-volatility.md). Post-5.6, ChatGPT's fan-outs shifted away from "best/vs/top" modifiers toward `site:` and "official" searches — use the extraction to see where your category's fan-outs stand today.

---

## AI Visibility Audit

Before optimizing, assess your current AI search presence.

### Step 1: Check AI Answers for Your Key Queries

Test 10-20 of your most important queries across platforms:

| Query | Google AI Overview | ChatGPT | Perplexity | You Cited? | Competitors Cited? |
|-------|:-----------------:|:-------:|:----------:|:----------:|:-----------------:|
| [query 1] | Yes/No | Yes/No | Yes/No | Yes/No | [who] |
| [query 2] | Yes/No | Yes/No | Yes/No | Yes/No | [who] |

**Query types to test:**
- "What is [your product category]?"
- "Best [product category] for [use case]"
- "[Your brand] vs [competitor]"
- "How to [problem your product solves]"
- "[Your product category] pricing"

### Step 2: Analyze Citation Patterns

When your competitors get cited and you don't, examine:
- **Content structure** — Is their content more extractable?
- **Authority signals** — Do they have more citations, stats, expert quotes?
- **Freshness** — Is their content more recently updated?
- **Schema markup** — Do they have structured data you're missing?
- **Third-party presence** — Are they cited via Wikipedia, Reddit, review sites?

### Step 3: Content Extractability Check

For each priority page, verify:

| Check | Pass/Fail |
|-------|-----------|
| Clear definition in first paragraph? | |
| Self-contained answer blocks (work without surrounding context)? | |
| Statistics with sources cited? | |
| Comparison tables for "[X] vs [Y]" queries? | |
| FAQ section with natural-language questions? | |
| Schema markup (FAQ, HowTo, Article, Product)? | |
| Expert attribution (author name, credentials)? | |
| Recently updated (within 6 months)? | |
| Heading structure matches query patterns? | |
| AI bots allowed in robots.txt? | |

### Step 4: AI Bot Access Check

Verify your robots.txt allows AI crawlers. Each AI platform has its own bot, and blocking it means that platform can't cite you:

- **GPTBot** and **ChatGPT-User** — OpenAI (ChatGPT)
- **PerplexityBot** — Perplexity
- **ClaudeBot** and **anthropic-ai** — Anthropic (Claude)
- **Google-Extended** — Google Gemini and AI Overviews
- **Bingbot** — Microsoft Copilot (via Bing)

Check your robots.txt for `Disallow` rules targeting any of these. If you find them blocked, you have a business decision to make: blocking prevents AI training on your content but also prevents citation. One middle ground is blockig training-only crawlers (like **CCBotfeatured in industry roundups and comparison articles
- Maintain updated profiles on relevant review platforms
- Create YouTube content for key how-to queries — models don't watch the video, they read the text layer around it; see references/youtube-ai-citations.md for the full anatomy (transcript, captions, chapters, description, pinned comment)
- Guest on podcasts in your category (prep with the public-relations skill's podcast guest prep)
- Answer relevant Quora questions with depth

### Machine-Readable Files for AI Agents

> **Google's stance**: not required for AI Overviews or AI Mode. Their guide explicitly says you don't need new markup, AI files, or markdown to appear in generative AI search.
>
> **Why include them anyway**: non-Google AI engines (ChatGPT, Claude, Perplexity) and autonomous buying agents do reward extractable structure. The files below help with those engines without harming Google.

AI agents aren't just answering questions — they're beoming buyers. When an AI agent evaw-to content | `HowTo` | Step extraction for process queries |
| FAQs | `FAQPage` | Direct Q&A extraction |
| Products | `Product` | Pricing, features, reviews |
| Comparisons | `ItemList` | Structured comparison data |
| Reviews | `Revew`, `Aggregatime rather than single runs. Full rigor checklist in [references/format-volatility.md](references/format-volatility.md).

### Search Console expectations

Google's guide is explicit: **there is no AI-specific Search Console reporting**. AI Overviews and AI Mode use core Search ranking, so the standard Search Console reports (Performance, Coverage, Core Web Vitals) are still what you measure with for Google. The third-party tools above are the only way to see cross-platform AI citation behavior.

---

## What NOT to Do

Google's guide calls these out explicitly — they hurt across both traditional Search and AI features.

1. **Write separate content "for AI"**. Same content should serve people and AI. Writing variants targeted at AI systems risks the **scaled content abuse spam policy** — Google's words.
2. **Chunk pages into AI-bait fragments**. Google's guide is direct: *"Don't break your content into tiny pieces for AI to better understand it."* Use normal paragraph + heading structure.
3. **Generate at scale for ranking manipulation**. AI-generated content is fine *if* it meets Search Essentials and spam policies. Mass-producing thin variations does not.
4. **Pursue inauthentic mentions**. Don't fabricate citations or bulk-spam Reddit/Wikipedia for AI visibility. Real participation only.
5. **Block AI crawlers if you want citation**. Blocking GPTBot, PerplexityBot, ClaudeBot, Google-Extended means those engines literally cannot cite you. Block training-only crawlers (CCBot) if you must, not the search-and-cite ones.
6. **Hide your main content behind JS that doesn't render**. Both core Search and AI agents need to see your content; JS-only rendering loses both audiences.
7. **Skip E-E-A-T fundamentals**. Author identity, first-hand experience, expertise signals, transparent sourcing — Google's guide leans heavily on these for AI features.

---

## AI SEO by Content Type

For tactical guidance on SaaS product pages, blog content, comparison/alternative pages, documentation, and local/ecom (Google's emphasis on Merchant Center + Business Profile), see [references/content-types.md](references/content-types.md).

---

## Common Mistakes

- **Ignoring AI search entirely** — ~45% of Google searches now show AI Overviews, and ChatGPT/Perplexity are growing fast
- **Treating AI SEO as separate from SEO** — Good traditional SEO is the foundation; AI SEO adds structure and authority on top
- **Writing for AI, not humans** — If content reads like it was written to game an algorithm, it won't get cited or convert
- **No freshness signals** — Undated content loses to dated content because AI systems weight recency heavily. Show when content was last updated
- **Gating all content** — AI can't access gated content. Keep your most authoritative content open
- **Ignoring third-party presence** — You may get more AI citations from a Wikipedia mention than from your own blog
- **No structured data** — Schema markup gives AI systems structured context about your content
- **Keyword stuffing** — Unlike traditional SEO where it's just ineffective, keyword stuffing actively reduces AI visibility by 10% (Princeton GEO study)
- **Hiding pricing behind "contact sales" or JS-rendered pages** — AI agents evaluating your product on behalf of buyers can't parse what they can't read. Add a `/pricing.md` file
- **Blocking AI bots** — If GPTBot, PerplexityBot, or ClaudeBot are blocked in robots.txt, those platforms can't cite you
- **Generic content without data** — "We're the best" won't get cited. "Our customers see 3x improvement in [metric]" will
- **Forgetting to monitor** — You can't improve what you don't measure. Check AI visibility monthly at minimum

---

## Tool Integrations

For implementation, see the tools registry (the repo's `tools/REGISTRY.md`).

| Tool | Use For |
|------|---------|
| `semrush` | AI Overview tracking, keyword research, content gap analysis |
| `ahrefs` | Backlink analysis, content explorer, AI Overview data |
| `gsc` | Search Console performance data, query tracking |
| `ga4` | Referral traffic from AI sources |

---

## Task-Specific Questions

1. What are your top 10-20 most important queries?
2. Have you checked if AI answers exist for those queries today?
3. Do you have structured data (schema markup) on your site?
4. What content types do you publish? (Blog, docs, comparisons, etc.)
5. Are competitors being cited by AI where you're not?
6. Do you have a Wikipedia page or presence on review sites?

---

## Related Skills

- **seo-audit**: For traditional technical and on-page SEO audits
- **schema**: For implementing structured data that helps AI understand your content
- **content-strategy**: For planning what content to create
- **competitors**: For building comparison pages that get cited
- **programmatic-seo**: For building SEO pages at scale
- **copywriting**: For writing content that's both human-readable and AI-extractable
