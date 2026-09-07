---
name: utility-first-css-styling
description: "Use when styling web UIs with Tailwind CSS v4, configuring @theme design tokens, adding custom utilities, handling responsive/dark states, or migrating a v3 project to v4."
license: MIT
tags:
- css
- styling
- design-system
- responsive
- theming
---

# Tailwind CSS v4

Build utility-first UIs with Tailwind CSS v4. This skill reflects current v4 conventions: CSS-first configuration, the new `@import "tailwindcss"` entry, `@theme` design tokens, and `@utility`.

## Setup

Tailwind v4 uses framework-specific plugins — no `tailwind.config.js` by default.

- **Vite**: `npm install tailwindcss @tailwindcss/vite`, add the plugin to `vite.config.ts`, then `@import "tailwindcss";` in your main CSS.
- **PostCSS**: `npm install tailwindcss @tailwindcss/postcss`, add `@tailwindcss/postcss` to your PostCSS config, then `@import "tailwindcss";` in your CSS.
- **CLI**: `npm install @tailwindcss/cli`, then `npx @tailwindcss/cli -i input.css -o output.css`.
- **Other frameworks**: use the framework-specific guide on tailwindcss.com.

The single `@import "tailwindcss"` replaces the old `@tailwind base; @tailwind components; @tailwind utilities;` directives.

## CSS-first configuration with `@theme`

Define design tokens in a `@theme` block. Each token generates a utility and/or variant.

```css
@import "tailwindcss";

@theme {
  --color-brand: #6c5ce7;
  --color-brand-light: oklch(0.72 0.18 300);
  --font-display: "Inter", sans-serif;
  --spacing-section: 6rem;
  --breakpoint-3xl: 120rem;
  --radius-card: 1.5rem;
}
```

- `--color-*` → `bg-brand`, `text-brand`, `border-brand`, etc.
- `--font-*` → `font-display`.
- `--spacing-*` → `p-section`, `mt-section`, etc.
- `--breakpoint-*` → `3xl:` variant.
- `--radius-*` → `rounded-card`.
- Use `oklch()`/`oklab()` colors for wide-gamut, future-proof palettes.

Use `@theme` only for tokens that should generate utilities/variants. For plain CSS variables that should NOT generate Tailwind APIs, define them in `:root` instead.

`@theme` variables must be top-level — never nested under selectors or media queries.

```css
:root {
  /* plain var, no utility generated */
  --site-bg: #f8fafc;
}
```

## Custom utilities

Define reusable custom utilities with `@utility` (replaces the old `@layer utilities`/`@layer components` approach):

```css
@utility text-balance {
  text-wrap: balance;
}

@utility section-pad {
  padding-inline: var(--spacing-section);
}
```

For utilities that need to respond to variants (`hover:`, `dark:`), use the functional form:

```css
@utility custom-shadow {
  box-shadow: 0 10px 40px -10px rgb(0 0 0 / 0.4);
}
```

## Variants and stacking

- Apply variants like `hover:`, `focus:`, `md:`, `dark:`, `group-hover:`.
- **Stacked variants apply left-to-right, which is the reverse order from v3.** `dark:hover:bg-white` means hover (inner) under dark (outer) — the rightmost applies to the element, leftmost is the outer context.
- Custom variants are registered in `@variant`, e.g. `@variant hover:hover`.

```css
@theme {
  --variant-hover: &:hover;
}
```

## Responsive design

- Mobile-first: write base styles, then use `sm:`, `md:`, `lg:`, `xl:`, `2xl:` variants to scale up.
- Breakpoints are CSS-first: override/define them in `@theme` with `--breakpoint-*`.

```html
<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
```

## Dark mode

Dark mode is configured via a `@custom-variant` so it uses your chosen strategy:

```css
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));
```

Then use `dark:` utilities — they activate whenever an ancestor has the `.dark` class. Pair with `@media (prefers-color-scheme: dark)` variant only if you want OS-based dark mode.

## Arbitrary values

- Arbitrary values: `bg-[#1e293b]`, `w-[300px]`, `grid-cols-[1fr_2fr]`.
- Arbitrary CSS variables (new syntax): `bg-(--brand-color)` — not `bg-[--brand-color]`.
- Underscores in arbitrary values become spaces: `p-[10px_20px]`.
- Use CSS variables as one-off values: `text-(--text-primary)`.

## Class detection and content scanning

- Tailwind scans your source files as **plain text**. Dynamically concatenated class fragments (`bg-${color}-500`) are NOT detected.
- Always write full class names literally in source.
- Use `@source` to add external or unusual source locations:

```css
@source "../node_modules/@my-lib";
```

- Use `@source inline("...")` only when safelisting is genuinely necessary (e.g. classes generated at runtime).

## Accessing theme values from CSS

- In CSS modules or component `<style>` blocks that are not processed together with your main CSS, use `@reference` to pull in the theme:

```css
@reference "../../app.css";

.card {
  color: var(--color-brand);
}
```

## Interop with JS/TS

- Common utility-first patterns compose cleanly: flex/grid layouts, spacing scale, `gap` (prefer `gap` over `space-*`/`divide-*` where selectors changed in v4).
- Type utilities come from the Tailwind package types (`tailwindcss` exports `Config` etc. when needed); CSS-first config usually needs no JS config file.

## Migration checklist (v3 → v4)

- PostCSS plugin is now `@tailwindcss/postcss`; CLI is `@tailwindcss/cli`; Vite plugin `@tailwindcss/vite` is recommended.
- Entry is `@import "tailwindcss";` — no `@tailwind` directives.
- Prefix syntax: `@import "tailwindcss" prefix(tw);` and classes use `tw:` at the start.
- The `!important` modifier goes at the end: `bg-red-500!`.
- Default border and ring colors now use `currentColor`; default ring width is 1px.
- `space-*` and `divide-*` selectors changed — if layouts break, use flex/grid with `gap`.
- Custom utilities use `@utility`, not `@layer utilities/components`.
- Transform resets: `scale-none`, `rotate-none`, `translate-none` (not `transform-none`).
- `hover:` only applies on devices that support hover — override if needed.
- Browser support is modern-only: Safari 16.4+, Chrome 111+, Firefox 128+.

See `references/gotchas.md` for the full quick-scan list.
