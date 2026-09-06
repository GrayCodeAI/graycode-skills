---
name: web-data-workflows
description: "Use to run outcome-focused web-data workflows producing deliverables like research reports, SEO audits, QA reports, lead lists, or knowledge bases."
license: ISC
tags:
- workflows
- automation
- research
- deliverables
---

# Firecrawl Workflows

Use this when the user wants a finished deliverable powered by Firecrawl, not only raw web extraction and not product-code integration.

## Choose The Workflow

- Use firecrawl-website-design-clone to extract a website's colors, fonts, spacing, components, and layout patterns into an agent-ready `DESIGN.md`.
- Use firecrawl-research-papers for literature reviews and paper-backed synthesis, including biomedical, clinical, drug, gene, disease, epidemiology, and public-health topics. It queries Firecrawl's paper index — PubMed, bioRxiv, medRxiv, and arXiv abstracts with full text reachable per paper — rather than searching websites.
- Use firecrawl-deep-research for sourced multi-source research reports built from **web** evidence: market, policy, technical, or industry topics. Not for literature reviews — when the evidence base is published papers, use `firecrawl-research-papers` above.
- Use firecrawl-seo-audit for site structure, on-page SEO, keyword, and SERP audits.
- Use firecrawl-lead-research for pre-meeting company/person intelligence briefs.
- Use firecrawl-qa for live-site QA testing and bug reports.
- Use firecrawl-competitive-intel for recurring pricing, feature, and changelog monitoring.
- Use firecrawl-company-directories for directory extraction into company lists.
- Use firecrawl-dashboard-reporting for dashboard metrics extraction.
- Use firecrawl-knowledge-base for LLM-ready docs, RAG chunks, training data, or docs mirrors.
- Use firecrawl-knowledge-ingest for auth-gated or JS-heavy docs portal ingestion.
- Use firecrawl-lead-gen for prospect list generation.
- Use firecrawl-market-research for market, financial, and industry research.
- Use firecrawl-demo-walkthrough for product flow walkthroughs and UX teardown reports.
- Use firecrawl-shop for product research and shopping recommendations.

If no existing workflow fits, use this generic process and produce a reusable pattern that could become a new skill.

## Required Intake

Infer the workflow, inputs, audience, and output format from the user's request and surrounding context. If enough is clear, start immediately.

Ask at most 1-3 concise clarifying questions only when a missing input would block the work, such as:

- the URL, company, topic, or source to analyze
- the desired deliverable or output format
- a constraint that would materially change the workflow

Use the host agent's normal way to ask clarifying questions. Do not depend on a harness-specific function name.

## Default Process

1. Confirm the workflow and final artifact.
2. Collect web evidence with Firecrawl through the CLI or equivalent Firecrawl tool surface.
3. Save or cite source evidence so the final claims are traceable.
4. Run independent research units in parallel when available.
5. Synthesize findings into the requested deliverable.
6. Include a short "rerun inputs" block when the workflow could be automated.

## Parallel Work

If appropriate, use sub-agents or equivalent parallel task runners for independent units such as:

- one competitor per researcher
- one URL or page per researcher
- one source category per researcher
- one analysis dimension per reviewer

Keep the handoff generic: provide the unit of work, source URLs or search terms, expected extracted fields, and output format.

## Deliverable Standards

Every workflow should return:

- a concise executive summary
- the evidence base used
- the analysis or artifact requested by the user
- recommendations or next actions when useful
- automation inputs for reruns

For authoring new workflow skills, see workflow-authoring.md.
