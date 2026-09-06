---
name: web-search-discovery-integration
description: "Integrate web search into app code and agent workflows when a feature starts with a query and must discover sources before extracting content."
license: ISC
tags:
- web-search
- discovery
- integration
- web-scraping
---

# Firecrawl Build Search

Use this when the application starts with a query, not a URL.

## Use This When

- the user asks a question and the product must discover sources first
- the feature needs current web results
- you want to turn a search query into a shortlist of pages for later scraping

## Default Recommendations

- Use `/search` first when URL discovery is part of the product behavior.
- Keep search and extraction conceptually separate unless scraping search results is clearly required.
- Prefer selective follow-up extraction over broad hydration when cost or latency matters.

## Common Product Patterns

- answer generation with cited sources
- company, competitor, or topic discovery
- research workflows that produce a shortlist of **web pages** before deeper extraction
- query-to-URL pipelines for later `/scrape` or `/interact`

Note that "research workflow" here means discovering web pages. If the product is
searching **published papers**, that is a different surface — see the escalation
rules below.

## Escalation Rules

- If you already have the URL, use firecrawl-build-scrape.
- If the result page then requires clicks or form interaction, escalate to firecrawl-build-interact.
- If the feature searches **published research papers** — biomedical, clinical, and life-science literature (PubMed, bioRxiv, medRxiv) or arXiv preprints — `/search` is the wrong surface. Use the research paper index instead: firecrawl-research-index. Passing `categories: ["research"]` to `/search` does **not** query that index; it filters an ordinary web search to research-affiliated websites (the list includes PubMed, bioRxiv, medRxiv, arXiv, and publisher sites) and returns page results from them — no abstract search, related-paper expansion, or full-text passages.
- If the feature answers developer questions from issues, pull requests, READMEs, or documentation pages, use the developer index instead: firecrawl-developer-index. The same caveat applies to `categories: ["developer"]`.

## Implementation Notes

- Treat `/search` as discovery, ranking, and source selection.
- Be explicit about whether the product needs snippets, URLs, or full result content.
- Keep the query contract stable so downstream scraping logic stays predictable.

## Docs (Source of Truth)

Read the source-of-truth page for your project language before writing integration code:

- **Node / TypeScript**: [docs.firecrawl.dev/agent-source-of-truth/node](https://docs.firecrawl.dev/agent-source-of-truth/node)
- **Python**: [docs.firecrawl.dev/agent-source-of-truth/python](https://docs.firecrawl.dev/agent-source-of-truth/python)
- **Rust**: [docs.firecrawl.dev/agent-source-of-truth/rust](https://docs.firecrawl.dev/agent-source-of-truth/rust)
- **Java**: [docs.firecrawl.dev/agent-source-of-truth/java](https://docs.firecrawl.dev/agent-source-of-truth/java)
- **Elixir**: [docs.firecrawl.dev/agent-source-of-truth/elixir](https://docs.firecrawl.dev/agent-source-of-truth/elixir)
- **cURL / REST**: [docs.firecrawl.dev/agent-source-of-truth/curl](https://docs.firecrawl.dev/agent-source-of-truth/curl)

## See Also

- firecrawl-build
- firecrawl-build-scrape
- firecrawl-build-interact
- firecrawl-research-index
- firecrawl-developer-index
