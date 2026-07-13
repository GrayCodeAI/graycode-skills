---
name: ag-astro
description: Build content-focused websites with Astro — zero JS by default, islands
  architecture, multi-framework components, and Markdown/MDX support.
license: MIT
tags:
- astro
- ssg
- ssr
- islands
- content
category: frontend
risk: safe
source: community
date_added: 2026-03-18
author: suhaibjanjua
tools:
- claude
- cursor
- gemini
---

<!-- Hydrated immediately — this island is interactive -->
<SearchBox client:load />
```

## Best Practices

- ✅ Keep most components as static `.astro` files — only hydrate what must be interactive
- ✅ Use content collections for all Markdown/MDX content — you get type safety and auto-validation
- ✅ Prefer `client:visible` over `client:load` for below-the-fold components to reduce initial JS
- ✅ Use `import.meta.env` for environment variables — prefix public vars with `PUBLIC_`
- ✅ Add `<ViewTransitions />` from `astro:transitions` for smooth page navigation without a full SPA
- ❌ Don't use `client:load` on every component — this defeats Astro's performance advantage
- ❌ Don't put secrets in `.astro` frontmatter that gets used in client-facing templates
- ❌ Don't skip `getStaticPaths` for dynamic routes in static mode — builds will fail

## Security & Safety Notes

- Frontmatter code in `.astro` files runs server-side only and is never exposed to the browser.
- Use `import.meta.env.PUBLIC_*` only for non-sensitive values. Private env vars (no `PUBLIC_` prefix) are never sent to the client.
- When using SSR mode, validate all `Astro.request` inputs before database queries or API calls.
- Sanitize any user-supplied content before rendering with `set:html` — it bypasses auto-escaping.

## Common Pitfalls

- **Problem:** JavaScript from a React/Vue component doesn't run in the browser
  **Solution:** Add a `client:` directive (`client:load`, `client:visible`, etc.) — without it, components render as static HTML only.

- **Problem:** `getStaticPaths` data is stale after content updates during dev
  **Solution:** Astro's dev server watches content files — restart if changes to `content/config.ts` are not reflected.

- **Problem:** `Astro.props` type is `any` — no autocomplete
  **Solution:** Define a `Props` interface or type in the frontmatter and Astro will infer it automatically.

- **Problem:** CSS from a `.astro` component bleeds into other components
  **Solution:** Styles in `.astro` `<style>` tags are automatically scoped. Use `:global()` only when intentionally targeting children.

## Related Skills

- `@sveltekit` — When you need a full-stack framework with reactive UI (vs Astro's content focus)
- `@nextjs-app-router-patterns` — When you need a React-first full-stack framework
- `@tailwind-patterns` — Styling Astro sites with Tailwind CSS
- `@progressive-web-app` — Adding PWA capabilities to an Astro site

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
