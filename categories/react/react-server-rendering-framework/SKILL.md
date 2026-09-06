---
name: react-server-rendering-framework
description: "Use when scaffolding Next.js App Router apps, creating routes/layouts, choosing Server vs Client Components, caching, streaming, metadata, or deploying."
license: MIT
tags:
- react
- ssr
- app-router
- server-components
- caching
---

# Next.js (App Router)

Build production-grade, server-rendered websites and applications with Next.js 16. This skill encodes current App Router conventions from the official Next.js docs.

## Principles

- **File-system routing.** Folders define URL segments; special files (`page`, `layout`, `loading`, `error`, `not-found`, `route`) define UI/behavior for that segment.
- **Server-first.** Layouts and Pages are React Server Components by default. Add `"use client"` only where you need interactivity, browser APIs, or state.
- **Caching is opt-in and explicit.** Cache with the `use cache` directive + `cacheLife`, stream fresh data with `<Suspense>`, and revalidate with `cacheTag`/`updateTag`.
- **Navigation is optimized.** `<Link>` prefetches and performs client-side transitions; add `loading.tsx` for streaming and partial prefetch of dynamic routes.

## Scaffolding a project

```bash
npx create-next-app@latest my-app
# --yes: TypeScript, ESLint, Tailwind CSS, App Router, Turbopack, import alias @/*
cd my-app && npm run dev
```

Recommend **TypeScript + App Router + Turbopack** for new builds. Minimum Node.js 20.9.

- `next dev` — dev server (Turbopack by default).
- `next build` — production build.
- `next start` — production server.
- `eslint` / `biome check` — linting (Next 16 no longer lints during `next build`).

Project layout:

```
app/
  layout.tsx        # root layout: REQUIRED, holds <html> and <body>
  page.tsx          # the '/' route
  blog/
    page.tsx        # '/blog'
    [slug]/page.tsx # '/blog/console.log(seg)
    loading.tsx     # route loading UI (streaming fallback)
    error.tsx       # route error UI
public/             # static assets referenced from '/'
```

## Routes: layouts and pages

- **Page**: default-export a component from `page.{js,jsx,ts,tsx}` to make the folder's route public.
- **Layout**: default-exports a component that accepts `children`; preserves state and stays mounted across navigations. May be nested.
- **Root layout** (`app/layout.tsx`) is required and must render `<html>` and `<body>`.

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

- **Dynamic segment**: wrap a folder in brackets, e.g. `blog/[slug]`. Read the resolved value from an awaited `params`.

```tsx
// app/blog/[slug]/page.tsx
export default async function Page(props: PageProps<'/blog/[slug]'>) {
  const { slug } = await props.params
  const post = await getPost(slug)
  return <h1>{post.title}</h1>
}
```

- **Route props**: use the global `PageProps<'/path'>` and `LayoutProps<'/path'>` helpers for typed `params`/`searchParams`. Static routes resolve `params` to `{}`.
- **Search params** in a Server Component page travel via the `searchParams` prop (awaited); for client-only filtering read them from `useSearchParams`.

## Server and Client Components

Keep components Server by default. Add a Client Component only when you need state, event handlers, lifecycle hooks, custom hooks, or browser-only APIs.

- Add `"use client"` at the very top of a file to mark a Client Component and a boundary.
- Code **outside** the boundary (parents) stays on the server and is not in the client bundle; all imports of a client file join the client bundle.
- Pass data Server → Client via serializable props.

```tsx
// app/ui/counter.tsx
'use client'
import { useState } from 'react'
export default function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

- **Pass server-rendered UI into a client component** using `children` (slot pattern) so it renders on the server even inside client chrome.
- **Context providers** must be Client Components; wrap `{children}` and render as deep as possible (never around the whole `<html>`).
- **Third-party client libraries**: wrap them in your own client wrapper (`'use client'` + re-export) before importing into a Server Component.
- Keep client bundles small: add `"use client"` to small leaf components (`<Search/>`), not the whole layout.
- Use `server-only` / `client-only` packages to prevent environment poisoning; only `NEXT_PUBLIC_*` vars reach the client.
- About secrets: `process.env.API_KEY` without a `NEXT_PUBLIC_` prefix is emptied client-side — always keep secrets in Server Components.

## Data fetching and streaming

Pages are server components, so fetch directly in them.

```tsx
// app/blog/page.tsx
export default async function Page() {
  const posts = await getPosts()
  return <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>
}
```

For data that must be fresh per request, do **not** cache; instead wrap it in `<Suspense>` so the shell renders first and the content streams in at request time:

```tsx
import { Suspense } from 'react'

async function LatestPosts() {
  const res = await fetch('https://api.example.com/posts')
  const posts = await res.json()
  return <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>
}

export default function Page() {
  return (
    <Suspense fallback={<p>Loading posts...</p>}>
      <LatestPosts />
    </Suspense>
  )
}
```

- **Streaming**: components that access runtime APIs (`cookies`, `headers`, `searchParams`, dynamic `params`) must be wrapped in `<Suspense>`.
- **Non-deterministic data** (`Date.now()`, `crypto.randomUUID()`, `Math.random()`) must call `await connection()` before use and be wrapped in Suspense — otherwise `next build` errors with "Uncached data was accessed outside of `<Suspense>`".

## Caching with Cache Components (enable `cacheComponents: true`)

```ts
// next.config.ts
const nextConfig = { cacheComponents: true }
export default nextConfig
```

- **Data-level**: put `"use cache"` at the top of an async function body, then set a `cacheLife`:

```tsx
import { cacheLife } from 'next/cache'

export async function getUsers() {
  'use cache'
  cacheLife('hours')
  return db.query('SELECT * FROM users')
}
```

- **UI-level**: put `"use cache"` at the top of a component/page/layout body to cache the whole rendered unit. Different inputs (args/closed-over values) produce separate cache entries automatically.
- **Lifecycles**: `cacheLife('seconds' | 'minutes' | 'hours' | 'days' | 'weeks' | 'max')`.
- **Tagging/revalidation**: `cacheTag('posts')` to group, and `updateTag('posts')` from a Server Action/form submission to invalidate on mutation:

```tsx
import { cacheLife, cacheTag, updateTag } from 'next/cache'

async function BlogPosts() {
  'use cache'
  cacheLife('hours')
  cacheTag('posts')
  const res = await fetch('https://api.vercel.app/blog')
  return (await res.json()).slice(0, 5).map((p) => <li key={p.id}>{p.title}</li>)
}

async function createPost(formData: FormData) {
  'use server'
  await db.post.create({ data: { title: formData.get('title') } })
  updateTag('posts')
}
```

- Passing runtime values into cached work: read cookies/headers in a non-cached component, extract the value, and pass it as an argument — it joins the cache key (enables personalization).
- Default `use cache` stores entries in-memory. For durable shared caching across serverless requests use `use cache: remote` and a remote cache handler.

## Navigation and linking

- Use `next/link`'s `<Link>` for prefetching + client-side transitions; plain `<a>` does not prefetch.

```tsx
import Link from 'next/link'
<Link href="/blog">Blog</Link>
```

- **Prefetching**: static routes are fully prefetched when the Link enters the viewport. Dynamic routes are skipped or partially prefetched (only when `loading.tsx` exists).
- Add `app/<route>/loading.tsx` to enable immediate navigation, streaming fallback, and partial prefetch of dynamic routes — improves TTFB/FCP/TTI and avoids "app not responding".
- Add `generateStaticParams` so generate-able dynamic segments prerender at build time instead of falling back to request-time rendering:

```tsx
export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map((p) => ({ slug: p.slug }))
}
```

- Disable prefetching when needed: `<Link prefetch={false} href="/blog">`.
- Use `useLinkStatus` (from `next/link`) to show immediate pending feedback on slow networks.
- For advanced transitions, use `useRouter` from `next/navigation`; use `window.history.pushState`/`replaceState` to update URL while syncing `usePathname`/`useSearchParams`.

## Metadata and OG images

- Define static metadata (title, description, Open Graph) by exporting `metadata` from a server layout/page.
- Generate dynamic `generateMetadata` per request/params, and `generateViewport` for viewport/theme color.
- For dynamic OG images, generate image files at build using the `ImageResponse` API and export them from the route so social platforms render a per-page preview.

## Loading, error, and not-found states

- `loading.tsx` — Suspense fallback shown during navigation/render.
- `error.tsx` — a client component that receives `error` and `reset`, shown when a segment throws; always show a friendly message + retry.
- `not-found.tsx` — 404 UI; `notFound()` thrown to trigger it.

## Backend / data access

- **Server Actions** are async functions marked `"use server"` (or defined in a `'use server'` file) called from a `<form action={fn}>` or client event. Use them for mutations and call `utils/revalidatePath`, `revalidateTag`, or `updateTag` after mutations.
- **Route Handlers** for custom API endpoints: define `export async function GET/POST...` in `app/api/<name>/route.ts`. Do not call Route Handlers from Server Components — call the business logic directly.

## Configuration and deployment

- Turbopack is the default bundler (`next dev`, `next build`). Use `--webpack` to opt out.
- TypeScript is built in; rename files to `.ts/.tsx` to opt in. Enable the TS+Next plugin in VS Code.
- Deploy: Vercel is the zero-config host; self-hosting with `node` servers also supported. Keep `cacheComponents` behavior in mind for caching semantics across serverless/edge.