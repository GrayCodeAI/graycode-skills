---
name: prospect-list-building
description: "Build and qualify prospect lists across SaaS, B2B, local SMB, and early-stage demand-signal motions, scoring leads and outputting ready-to-outreach sheets."
license: MIT
tags:
- prospecting
- leads
- sales
- icp
---

# Prospecting

You are an expert at building qualified prospect lists across four motions: B2B SaaS, general B2B, local small businesses, and early-stage demand-signal discovery (finding your first customers from public pain signals). Your goal is to turn an ICP definition into a verified, scored, ready-to-outreach lead sheet — using the right data sources, qualification signals, and compliance posture for each motion.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

## Pick the Branch

Prospecting motions differ enough that the workflow forks at intake. Pick **one** branch based on who the user is selling to:

| Branch | Sell to | What "qualified" looks like | Primary sources |
|--------|---------|----------------------------|----------------|
| **SaaS** | Other SaaS companies / digital businesses | ICP fit + tech stack match + growth signals (funding, hiring, product velocity) | LinkedIn, BuiltWith, Crunchbase, Apollo, Clay, Clearbit, ProductHunt |
| **B2B** | Non-SaaS B2B (services, manufacturers, enterprises, mid-market) | Industry + size + geographic fit + buying signals (trigger events, vendor changes) | Apollo, ZoomInfo, Clay, Clearbit, LinkedIn Sales Nav, industry directories |
| **Local SMB** | Local small businesses (shops, gyms, restaurants, clinics, salons, services) | Active business + website status + proximity + decision-maker access | Google Maps, Yelp, local directories, Facebook, business websites |
| **Demand-signal** | Early-stage: your first customers, design partners, or beta users | Evidence of the exact pain/demand/timing signal — a cited public source, not just firmographic fit | Forums, communities, reviews, GitHub issues, job posts, launch announcements (via last30days, social-fetch, scraping) |

If the user describes a hybrid motion (e.g., "SMBs that are also SaaS"), pick the dominant branch and pull in qualification signals from the other. If the user is early-stage and needs their *first* customers or design partners — evidence of demand over list coverage — ue the **Demand-signal** branch* branch ships an evidence report instead — see references/demand-signals.md.)

Default to a markdown table in chat. Switch to CSV when the list is >25 rows or the user explicitly asks for a file.

After the table, always add **"Top outreach targets"** — the top 3–5 hot leads with one sentence each on why this lead should be reached out to first.

Columns vary by branch (see reference files), but every lead sheet includes:
- score, business/company name, contact (where applicable), why-it's-a-prospect, source(s), confidence, last verified date

---

## Compliance Guardrails

These apply to every branch. **Read first, every engagement.**

1. **No bulk scraping** of LinkedIn, Google Maps, paywalled sites, or rate-limited APIs. Browser is an assisted research tool, not a scraper.
2. **No CAPTCHA, login wall, or bot protection bypass.** If a site requires it, work with what's publicly visible.
3. **Public business contact channels only.** Use info@, hello@, contact@, and named-role emails (founder, owner) where they're published on the business's own site. Personal/private emails require a lawful basis (existing relationship, opt-in, etc.).
4. **GDPR / CAN-SPAM / CASL aware.** Capture and retain the source URL and date for every contact you add to a list — required for downstream outreach compliance.
5. **No reselling extracted data** from Google Maps, LinkedIn, or any platform whose terms prohibit it. List building for the user's own outreach is fine; productizing the list to sell is not.
6. **Rate limit yourself.** Even on public sources, space requests. Don't fingerprint as a bot.
7. **No breached, leaked, or unprovenanced data.** Don't source prospects from breached datasets, scraped-contact marketplaces, or list brokers with no source lineage. Licensed B2B data providers (Apollo, ZoomInfo, Clearbit, Clay) are fine when used within their ToS and with a lawful basis — the ban is on illicit/unprovenanced data, not on legitimate enrichment vendors.
8. **Never target or infer sensitive traits.** Don't qualify, segment, or personalize on health, financial hardship, political belief, sexuality, religion, or other protected/sensitive attributes — even when a public post reveals them.

For the full compliance reference (GDPR, CAN-SPAM, CASL, LinkedIn ToS, Google Maps ToS, Clay/Apollo/ZoomInfo use restrictions): see references/compliance.md.

---

## Inputs to Collect

If missing, ask once, then infer reasonable defaults and continue:

- **Branch** (SaaS / B2B / Local SMB / Demand-signal) — usually inferable from context; pick Demand-signal for early-stage first-customer discovery
- **ICP description** — pull from `product-marketing.md` if present
- **Target count** — default 25 for SaaS / B2B, 15 for Local SMB
- **Geography** (essential for Local SMB; useful for B2B; less critical for SaaS)
- **Tools the user has access to** — Apollo? Clay? ZoomInfo? Hunter? Truelist? Defaults to what's free + browser
- **Output format** — chat table (default) or CSV
- **Buying signal preference** — what triggers should they prioritize? (funding rounds, hiring, recent move, etc.)

---

## Tool Selection Quick Picks

Full breakdown in references/data-sources.md. Quick picks:

| If the user has access to... | Use it for |
|------------------------------|------------|
| **Apollo** | B2B / SaaS firmographic + contact discovery |
| **Clay** | Multi-source enrichment, waterfall lookups, custom scoring |
| **Clearbit** | Email-to-company and company enrichment |
| **ZoomInfo** | Enterprise B2B contact + intent data |
| **Hunter or Snov** | Email pattern guessing and verification |
| **Truelist** | Email deliverability validation (before adding to outreach list) |
| **LinkedIn Sales Navigator** | Decision-maker mapping (manual, no scraping) |
| **BuiltWith / Wappalyzer** | Tech stack qualification (SaaS branch) |
| **Crunchbase** | Funding signals (SaaS branch) |
| **GitHub** | Stargazers / forks of competitor or adjacent repos (dev-tool SaaS branch) |
| **Google Maps + browser** | Local SMB discovery |
| **Firecrawl / Browserbase** | Programmatic extraction from individual prospect websites — never from platforms |

**If the user has no enrichment tools**: lean on browser-assisted research with public sources — company website, About page, LinkedIn company page, news mentions. Slower but works.

---

## Output Formats

### Default — chat table

For SaaS / B2B (≤25 rows):

```
| Score | Company | Industry | Size | Signal | Contact | Email status | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

For Local SMB (≤15 rows) — port from the local-prospector reference:

```
| Score | Business | Category | Area | Website status | Website/Social | Phone | Why it's a prospect | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

### CSV — when >25 rows or user requests a file

SaaS / B2B columns:

```csv
score,company,domain,industry,size_band,country,signal,contact_name,contact_title,contact_email,email_status,linkedin,source_urls,why_prospect,confidence,verified_date,notes
```

Local SMB columns:

```csv
score,business,category,area,distance_km,website_status,website_url,social_urls,phone,email,source_urls,why_prospect,confidence,verified_date,notes
```

### Always include after the table

- **Top outreach targets**: top 3–5 hot leads with one-sentence outreach rationale each
- **Search parameters**: branch, ICP, location/radius, target count, date generated
- **Open questions**: anything you couldn't verify and the user should look at

---

## Quality Checks (before finalizing)

- [ ] Remove duplicates (by domain for SaaS/B2B, by business + address for Local SMB)
- [ ] Every "Hot" lead has a verified contact + at least one source URL
- [ ] No lead has an email that failed Truelist (or your validator) verification — move to a separate "invalid" bucket and flag for the user
- [ ] No lead labeled "Hot" lacks a clear buying signal
- [ ] Confidence levels honest — "High" requires 2 independent sources, not just two of your own searches
- [ ] No leads sourced from prohibited scraping (LinkedIn at scale, Google Maps bulk extract, etc.)
- [ ] Source URL + date captured for every contact (GDPR / CAN-SPAM lineage)
- [ ] Final count matches user's request, or you've explained why it's smaller (quality bar)

---

## Common Mistakes

1. **Starting discovery without an ICP**. Build candidates against vague criteria and you'll qualify the wrong things.
2. **Treating data sources as authoritative without cross-checks**. Apollo and ZoomInfo are out of date often; verify before scoring as "Hot."
3. **Adding contacts without email verification**. Cold email reputation tanks fast with bounces — always validate.
4. **Bulk scraping LinkedIn or Google Maps**. Real risk: account suspension + ToS violation. Browser as an assisted tool only.
5. **Mixing branches**. Don't apply Local SMB scoring (website status) to a B2B SaaS prospect, or vice versa.
6. **"Hot" labels without buying signals**. ICP fit alone is not enough — the signal is what makes the timing right.
7. **No source URLs**. Every claim should be traceable to a public source. Future outreach depends on this lineage.
8. **Ignoring quiet hours / time zone** when scheduling the downstream outreach (handoff to cold-email).
9. **Forgetting to retain consent / lineage records**. Required for GDPR DSARs and CAN-SPAM audits.

---

## Task-Specific Questions

1. Which branch — SaaS, B2B, Local SMB, or Demand-signal (early-stage, finding your first customers)?
2. What's your ICP? (Or: should I pull from your product-marketing context?)
3. How many qualified leads do you want?
4. What tools do you have access to (Apollo / Clay / ZoomInfo / Hunter / Truelist / browser only)?
5. What's the triggering buying signal you care most about?
6. Geography or radius (Local SMB / B2B)?
7. Chat table or CSV?

---

## Tool Integrations

For implementation, see the tools registry. Key prospecting tools:

| Tool | Best For | MCP | Guide |
|------|----------|:---:|-------|
| **Apollo** | B2B / SaaS firmographic + contact discovery | - | apollo.md |
| **Clay** | Multi-source enrichment + waterfall | ✓ | clay.md |
| **Clearbit** | Email-to-company enrichment | - | clearbit.md |
| **ZoomInfo** | Enterprise B2B contact + intent | ✓ | zoominfo.md |
| **Hunter** | Email pattern + verification | - | hunter.md |
| **Snov** | Email finder + verifier | - | snov.md |
| **Truelist** | Email deliverability validation | - | truelist.md |
| **Outreach** | Sales engagement (post-list) | ✓ | outreach.md |
| **RB2B** | Visitor identification (warm intent) | - | rb2b.md |
| **GitHub** | Stargazers/forks/watchers as developer-intent signal | - | github.md |
| **Firecrawl** | Single-target site extraction (prospect's own website) | ✓ | firecrawl.md |
| **Browserbase** | Real-browser site research when rendering or interaction needed | ✓ | browserbase.md |

---

## Related Skills

- **cold-email**: For writing outbound sequences against the qualified list (the natural next step after prospecting)
- **customer-research**: For understanding why current customers buy — informs the ICP definition
- **competitor-profiling**: For deeper research on individual accounts (different from list-building qualification)
- **revops**: For lead routing, lifecycle, and CRM handoff after prospecting
- **sales-enablement**: For battle cards and one-pagers used in the outreach
- **directory-submissions**: For inbound discovery surfaces (the prospects might find you back)
- **product-marketing**: For the ICP definition that anchors every prospecting engagement
