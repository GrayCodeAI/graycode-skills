---
name: multi-source-research
description: "Fan out across multiple web sources in parallel to gather quotable evidence and JSON research output for a topic."
license: MIT
tags:
- research
- web-scraping
- aggregation
---

# Deep Research — parallel multi-source orchestrator

🟢 **What this is.** A single Python script that fans out across 8 data sources in parallel and dumps quotable evidence into a research folder. Use it whenever you need cross-source convergence on a topic before writing anything substantive.

🔴 **What this is NOT.** It does not synthesize a brief, an opinion, or a post. The output is **raw evidence for the writer to read and synthesize**. Voice and structure happen downstream — never inside the orchestrator.

# When to use

| Triggering moment | Why this skill |
|---|---|
| User pastes a tweet/URL and says "research this topic" or "do a deep dive on this" | Run on the topic *before* manually pulling individual sources. Saves 5-10 sequential calls. |
| User asks "what's the discourse on X" / "what are people saying about Y" | This is literally what the tool does. |
| Pre-flight before any long-form artifact (deep post, briefing, founder profile, product comparison, ecosystem map) | The 8-source sweep finds links and quotes that one-source spelunking would miss. |
| Need to validate a thesis with cross-source convergence | If Reddit + HN + X all surface the same pattern, that's a real market signal worth a thesis. |

🟡 **Not the right tool for**: single-event news posts where the source is one tweet (just fetch that tweet directly), or re-research of topics already covered.

# How to invoke

```bash
cd skills/deep-research/scripts
python3 research.py "your topic in quotes" [flags]
```

Common flag combinations:

```bash
# Standard pre-flight (default depth, 30 days, ~$0.10-0.20/run)
python3 research.py "agent harness engineering"

# Quick scan (~30s, smaller limits)
python3 research.py "Stripe Sessions 2026 announcements" --depth=quick

# Deep dive (~3-4 min, deeper per-source limits, more YT transcripts)
python3 research.py "openai vs anthropic enterprise 2026" --depth=deep --yt-transcripts=4

# Specific sources only (skip the ones you know won't have signal)
python3 research.py "Mitchell Hashimoto" --sources=x,github_repos,github_issues,hn

# Short window for news-shape topics
python3 research.py "GPT-5.5 launch" --days=7

# Custom output directory
python3 research.py "claude code skills" --out=/path/to/research/claude-code-skills/
```

# Output

🟢 **Default output:** `./research/<slug>/research-<date>.{json,md}` (relative to current working directory).

🟢 **Override with `--out=<dir>`** for project-specific paths.

| File | What's in it | Use it for |
|---|---|---|
| `research-<date>.md` | Human-readable cluster, sorted by engagement | Read first to triage which threads are worth pulling |
| `research-<date>.json` | Full structured evidence with all fields | Pull verbatim quotes, engagement numbers, URLs into the downstream artifact |

The markdown groups results by source (X, Reddit, HN, GitHub repos, GitHub issues, Polymarket, YouTube, Exa) and within each section sorts by engagement signal. Each entry has the URL, engagement counts, author, date, and a quoted excerpt.

# The 8 sources, what they give you

| Source | Cost | Auth | What it's good for |
|---|---|---|---|
| 🟢 **X / Twitter** (via monid `tikhub/twitter/web/fetch_search_timeline`) | ~$0.0015/page | `MONID_API_KEY` | Verbatim tweets with real engagement (likes/RT/replies/views), ranked by engagement. ~20 tweets/page; deep depth pages + a Latest sweep. The single most valuable source for op-ed work. |
| 🟢 **Reddit** (via monid Apify `trudax/reddit-scraper-lite`) | ~$0.05-0.10/run | `MONID_API_KEY` | Operator/user opinion threads with top comments. Anti-corporate angle. |
| 🟢 **Hacker News** (via monid `exa/contents` → Algolia JSON) | ~$0.0022/call | `MONID_API_KEY` | Developer-community discussion. Great for tooling/product launches. |
| 🟢 **GitHub repos** (via monid `exa/contents` → api.github.com) | ~$0.0022/call | `MONID_API_KEY` | Star counts, release dates, license, related projects. Critical for ecosystem maps. |
| 🟢 **GitHub issues/PRs** (via monid `exa/contents` → api.github.com) | ~$0.0022/call | `MONID_API_KEY` | Active development threads, contested features, recent bugs. Ground-truth project status. |
| 🟢 **Polymarket** (via monid `exa/contents` → Gamma search) | ~$0.0022/call | `MONID_API_KEY` | Money-weighted predictions. Odds on regulatory deadlines, election outcomes, product launches. |
| 🟢 **YouTube** (via monid Apify: search + transcript) | ~$0.03 / 2 transcripts | `MONID_API_KEY` | Recent videos + full transcripts for the top N. Often game-changing for talk/interview-driven topics. |
| 🟢 **Exa neural web search** (via monid `blockrun.ai/api/v1/exa/search`) | ~$0.011/call | `MONID_API_KEY` | Recent grounded web content + research papers. Supports a `category` filter (research paper, news, github, tweet, …). Returns inline text + highlights. |

🟢 **Total per-run cost: ~$0.10-0.20** at default depth. No monthly subscription.

🟢 **EVERY source routes through monid** — one auth (`MONID_API_KEY`), one balance, zero per-vendor keys. Paid sources (X, Reddit, YouTube, Exa) use native monid endpoints; sources with no native monid endpoint (HN Algolia, GitHub REST, Polymarket Gamma) are proxied through `blockrun.ai/api/v1/exa/contents`, which returns the upstream JSON body **verbatim** (raw bytes, no markdown cleaning) for ~$0.0022/call.

🔴 **Do NOT proxy JSON through `blockrun.ai/api/v1/surf/web/fetch`** — it runs a markdown cleaner that collapses whitespace inside JSON strings and mangles embedded URLs, producing invalid JSON on large/prose-heavy responses (GitHub issue bodies, Polymarket descriptions). Use `exa/contents` (raw passthrough) instead — that's what `_monid.fetch_json` does.

🟡 **Per-source budget rules**:
- Reddit costs scale with results × 0.0057 + a base scrape fee. A "deep" run can hit $0.25.
- YouTube transcripts cost $0.0075 per video — start with `--yt-transcripts=2`, raise to 4+ only if the topic is YouTube-heavy.
- X (tikhub) is ~$0.0015/page; default depth pulls 2 pages (~$0.003), deep pulls 3 + a Latest sweep.
- HN/GitHub/Polymarket proxy calls are ~$0.0022 each. **Polymarket Gamma is capped at `limit_per_type=8`** — exa livecrawl 504s on the ~1MB payload above that.

# Example workflow

```
1. User: "do a deep dive on Greg Isenberg's agent agency podcast"
2. Read the source URL (the tweet, the YouTube link)
3. Run: python3 research.py "Greg Isenberg agent agency Hermes Orgo"
4. Wait ~60-90s for all 8 sources
5. Open research-<date>.md, scan the X + Reddit + Exa sections
6. For each high-signal post, pull the verbatim text from research-<date>.json
7. Draft your artifact with verbatim quotes lifted directly from the JSON
```

🔴 **Critical rule**: this skill produces **research input**, not draft output. Never copy/paste sentences from `research-<date>.md` into the artifact you're writing. Always pull the *underlying primary source* (tweet text, blog excerpt, GitHub description) from the .json and synthesize in your own voice downstream.

# Voice contract

This skill **must not** synthesize editorial prose or take positions. Its only job is to retrieve, normalize, and rank.

If the script ever starts emitting things like *"the takeaway is..."*, *"this represents a shift..."*, or *"the bottom line:"*, that's a bug — remove it. The synthesis is what humans (or downstream editorial workflows) do.

# Files

| Path | What |
|---|---|
| `SKILL.md` | This file |
| `scripts/research.py` | The orchestrator (CLI entry) |
| `scripts/sources/_monid.py` | Shared monid runner: `run_monid` (retry/backoff) + `fetch_json` (raw-JSON via exa/contents) — used by ALL sources |
| `scripts/sources/reddit.py` | Reddit via monid Apify |
| `scripts/sources/hackernews.py` | HN Algolia via monid exa/contents |
| `scripts/sources/polymarket.py` | Polymarket Gamma via monid exa/contents |
| `scripts/sources/github.py` | GitHub REST via monid exa/contents |
| `scripts/sources/x_twitter.py` | X via monid tikhub |
| `scripts/sources/youtube.py` | YouTube via monid Apify |
| `scripts/sources/exa.py` | Exa neural search via monid (blockrun.ai proxy) |

# Required env

| Env var | Used by | Required for |
|---|---|---|
| `MONID_API_KEY` | `_monid.py` → ALL sources | Everything — every source routes through monid |

🟢 **One key for everything.** Set `MONID_API_KEY` in your environment and ensure your monid balance is funded.

🟡 **Optional env var:** `MONID_BIN` — path to the `monid` CLI binary. Defaults to a `monid` lookup on `$PATH`. Set this if you've installed monid in a non-standard location.

🟡 **Missing-auth behavior:** if `MONID_API_KEY` is unset, sources return empty and the orchestrator logs warnings but still completes (with no data). Ensure the key + a funded monid balance before running.

# Installing monid

This skill depends on the `monid` CLI. Install it with:

```bash
npm install -g monid
# or, if you prefer a local install:
npm install monid
export MONID_BIN="$(pwd)/node_modules/.bin/monid"
```

Get an API key at [monid.dev](https://monid.dev) and export it:

```bash
export MONID_API_KEY=your_key_here
```

# Known gotchas

| Gotcha | Mitigation |
|---|---|
| 🔴 **Never proxy JSON through `surf/web/fetch`** — its markdown cleaner corrupts large/prose-heavy JSON (mangles embedded URLs → invalid JSON) | Use `exa/contents` (raw passthrough). `_monid.fetch_json` already does this. Verified clean on 166KB GitHub issue payloads. |
| 🔴 **exa/contents 504s (`CRAWL_LIVECRAWL_TIMEOUT`) on ~1MB+ responses**, and transiently even on small ones | `fetch_json` retries the no-results case with backoff (2 retries). Polymarket Gamma is capped at `limit_per_type=8`; keep GitHub `per_page<=15`. |
| 🟡 **Reddit's Apify `upVotes` field returns 1 as default** when the scraper skips engagement metadata | Module filters on "any score or any comments or has body or has top comments" instead of a hard floor. Trust the human reading the markdown to rank by relevance. |
| 🟡 **Reddit can return 0 results** for low-volume topics | Try a broader query, then filter manually. |
| 🔴 **GitHub /search/issues requires `is:issue` or `is:pr`** (returns 422 otherwise as of 2026-05) | Already handled in `github.py` — module appends `is:issue` automatically. |
| 🟡 **HN: web/fetch-style cleaners mangle Algolia `story_text`/`_highlightResult`** (legacy note; exa/contents avoids this) | `hackernews.py` still requests `attributesToHighlight=["none"]` + a tight field whitelist to keep payloads small and URL-free — defensive even with the raw path. |
| 🔴 **tikhub (X) intermittently returns an HTML error page** (`Unexpected token '<'`) under rate-limiting — ~1 in 3 calls | Already handled: `_monid.py` detects transient HTML/UNKNOWN errors and retries with exponential backoff (2 retries default). If X still returns 0, re-run or lower depth. |
| 🟡 **tikhub (X) has no date param** — date filtering is client-side from each tweet's `created_at` | `x_twitter.py` parses `created_at` and filters to the `--days` window; undated tweets are kept rather than dropped. Use short keywords (1-2 words), not sentences. |
| 🟡 **Polymarket Gamma keyword search ignores very short terms** (e.g. "AI") | Use longer queries ("artificial intelligence"); the orchestrator passes the full topic. |
| 🔴 **YouTube scraper input field is `searchQueries`, NOT `searchKeywords`** | Already handled in `youtube.py`. Apify schema change in Apr 2026. |
| 🟢 **No persistent state**. Each run is independent. | Re-running on the same topic costs the same as the first run — sources are not cached. Plan accordingly. |

# Updating this skill

When a source's input schema changes, GitHub adds a new search filter, or a monid endpoint changes — update the relevant `sources/*.py` and bump the `Known gotchas` section. Everything goes through `sources/_monid.py`:

- **Native monid endpoint** (X, Reddit, YouTube, Exa): call `run_monid(provider, endpoint, body=/query=/path=, retries=)` and normalize `result["output"]`.
- **No native endpoint** (HN, GitHub, Polymarket — arbitrary JSON REST): call `fetch_json(url)` which proxies through `exa/contents` and returns parsed JSON. NEVER use `surf/web/fetch` for JSON (markdown cleaner corrupts it).

To add a source: `monid discover` → `monid inspect` the schema → write a thin `sources/<name>.py` using whichever helper fits. Treat this SKILL.md as a living spec.

# Credits

Originally inspired by [`mvanhorn/last30days-skill`](https://github.com/mvanhorn/last30days-skill). The 30-day default window came from that upstream; everything else (the 8-source fan-out, the monid routing, the `_monid.py` helpers, the per-source modules) was rebuilt from scratch.
