---
name: payment-docs-lookup
description: "Use to read, search, or look up payment documentation and API reference from the terminal via the CLI instead of curl or WebFetch."
license: MIT
tags:
- documentation
- cli
- api-reference
- search
---

Use `stripe docs` instead of fetching [docs.stripe.com](https://docs.stripe.com/.md) content directly with `curl` or `WebFetch`.

- Fetches Markdown automatically
- Purpose-built for agents and terminal workflows

## Read a page by its web path

```bash
stripe docs /payments
```

## Search documentation by keyword

```bash
stripe docs search "payment intents"
```

## Look up API reference

```bash
# By resource name
stripe docs api product

# By HTTP method and path
stripe docs api GET /v1/products

# By event type
stripe docs api product.created
```
