---
name: vue-fullstack-framework
description: "Use when building Nuxt full-stack Vue apps with SSR, file-based routing, auto-imports, useFetch data fetching, middleware, or hybrid rendering."
license: MIT
tags:
- vue
- ssr
- routing
- server-rendering
- fullstack
---

Nuxt is a full-stack Vue framework that provides server-side rendering, file-based routing, auto-imports, and a powerful module system. It uses Nitro as its server engine for universal deployment across Node.js, serverless, and edge platforms.

> The skill is based on Nuxt 4.x, generated at 2026-06-22.

> **Nuxt 4 note:** the default `srcDir` is `app/` — Vue app code (`app.vue`, `components/`, `composables/`, `pages/`, etc.) lives under `app/`, while `server/`, `shared/`, `public/`, `modules/`, `layers/` and `nuxt.config.ts` stay at the project root. The `~`/`@` aliases now point at `app/`; use `~~`/`@@` for the root.

## Core

| Topic | Description | Reference |
|-------|-------------|-----------|
| Directory Structure | Nuxt 4 `app/` srcDir, `shared/`, aliases, conventions | core-directory-structure |
| Configuration | nuxt.config.ts, app.config.ts, aliases, compatibilityVersion, experimental | core-config |
| CLI Commands | Dev server, build, generate, preview, and utility commands | core-cli |
| Routing | File-based routing, dynamic routes, named views, layout props, middleware | core-routing |
| Data Fetching | useFetch, useAsyncData, $fetch, createUseFetch factories, caching | core-data-fetching |
| Modules | Creating and using Nuxt modules, Nuxt Kit utilities | core-modules |
| Deployment | Platform-agnostic deployment with Nitro, Vercel, Netlify, Cloudflare | core-deployment |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Composables Auto-imports | Vue/Nuxt composables, custom composables, `shared/`, useAnnouncer | features-composables |
| Components Auto-imports | Component naming, lazy loading, hydration strategies | features-components-autoimport |
| Built-in Components | NuxtLink, NuxtPage, NuxtLayout, NuxtAnnouncer, ClientOnly, and more | features-components |
| State Management | useState composable, SSR-friendly state, Pinia integration | features-state |
| Server Routes | API routes, server middleware, Nitro server engine | features-server |

## Rendering

| Topic | Description | Reference |
|-------|-------------|-----------|
| Rendering Modes | Universal (SSR), client-side (SPA), hybrid rendering, route rules | rendering-modes |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Data Fetching Patterns | Efficient fetching, caching, parallel requests, error handling | best-practices-data-fetching |
| SSR & Hydration | Avoiding context leaks, hydration mismatches, composable patterns | best-practices-ssr |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Layers | Extending applications with reusable layers | advanced-layers |
| Lifecycle Hooks | Build-time, runtime, and server hooks | advanced-hooks |
| Module Authoring | Publishable modules with Nuxt Kit, keyed composables, dependencies | advanced-module-authoring |
