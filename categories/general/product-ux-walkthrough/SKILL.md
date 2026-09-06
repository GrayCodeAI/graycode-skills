---
name: product-ux-walkthrough
description: "Use to walk through a product's key flows with a browser and produce a structured UX walkthrough for signup, onboarding, pricing, docs, or dashboard."
license: ISC
tags:
- ux
- product
- walkthrough
- user-experience
---

# Firecrawl Demo Walkthrough

Use this to document a product experience step by step.

## Onboarding Interview

Infer the product URL, flow focus, and output format from context. If the URL is clear, proceed immediately.

Ask at most 1-3 concise questions only if blocked, such as the URL, desired flow focus, or credentials/constraints for protected areas.

## Firecrawl Collection Plan

Use Firecrawl browser to open the product and navigate key flows. Snapshot at each step, scrape pages when useful, and document what the user sees and can do.

Do not submit real credentials, purchases, or irreversible actions unless the user explicitly instructs and has permission.

## Parallel Work

If appropriate, use sub-agents or equivalent parallel task runners:

- Homepage and Marketing
- Signup and Onboarding
- Pricing and Plans
- Docs and Developer Experience
- Dashboard and Core Product
- Help and Support

Each walker should return screens visited, actions taken, observations, friction, and source URLs.

## Final Deliverable

```markdown
# Product Walkthrough: [Product]

## Product Overview
[What the product does]

## Flow Walkthroughs
### [Flow Name]
1. [Screen/Page] - what appears and what action is available
2. [Next Screen] - what changes

## Key Findings
[First impression, standout patterns, friction points]

## Recommendations
[UX/product improvements]

## Pages Visited
[URLs]

## Rerun Inputs
workflow: firecrawl-demo-walkthrough
url: [url]
focus: [full/signup/pricing/docs/dashboard]
```

## Quality Bar

- Be specific about screens, CTAs, forms, and transitions.
- Separate observation from opinion.
- Preserve every page visited.
