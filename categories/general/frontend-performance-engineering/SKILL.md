---
name: frontend-performance-engineering
description: "Use when auditing, diagnosing, and optimizing frontend performance — Core Web Vitals, bundles, rendering, memory, budgets, and monitoring — targeting 95+ Lighthouse scores."
license: MIT
tags:
- performance
- core-web-vitals
- optimization
- monitoring
- lighthouse
---

# Skill

This skill serves as the AI agent's comprehensive framework for diagnosing, analyzing, and resolving any frontend performance challenge — from initial audit through root cause analysis, optimization implementation, and continuous monitoring. The agent should approach performance work empirically: measure first, hypothesize, implement targeted fixes, and verify with data. Every recommendation must be tied to a measurable metric and prioritized by user impact. The agent must resist premature optimization and instead focus effort where measured data indicates the highest return.

### Non-Negotiable Lighthouse Default (Apply to every build, every page, every delivered UI)

The agent's default performance target is a **Lighthouse score of 95/100 or higher in EVERY category — Performance, Accessibility, Best Practices, and SEO** — for every page or interface it produces, alongside smooth, fluid interactions. "Good" Core Web Vitals alone is not enough; the floor is a 95-grade page. This default applies to showcase, marketing, and SaaS UI alike.

- **Always verify.** After generating or refactoring any frontend, run Lighthouse (or Lighthouse CI) against each delivered page, record all four category scores, and include them in the output. Do not claim completion without the measurement.
- **Green means ship.** A page is only "done" when Performance, Accessibility, Best Practices, and SEO each report ≥ 95/100 and all Core Web Vitals pass at the stricter 95-grade thresholds defined in Step 4 below.
- **Optimize until 95.** If any category or Core Web Vital falls below the 95-grade line, apply the relevant optimization steps in this skill (Steps 6–8 for LCP/INP/CLS, Steps 15–20 for assets and rendering, Step 23 for budgets) and re-measure until it passes.
- **Stay smooth.** Also confirm `prefers-reduced-motion` is honored and animations only use GPU-friendly properties (`transform`/`opacity`) from Step 27, so the UI is not only 95+ in lab tests but also jank-free in real usage.

## When to use

Activate this skill when any of the following conditions are detected:

- A user reports a slow website, application, or specific page/interaction and wants help diagnosing or fixing it.
- A user asks about Core Web Vitals (LCP, INP, CLS, TTFB, FCP, TBT) — measurement, interpretation, or optimization.
- A user asks about bundle size reduction, code splitting, tree shaking, or lazy loading strategies.
- A user reports rendering performance issues (jank, dropped frames, slow scrolling, unresponsive interactions, excessive re-renders).
- A user asks about image optimization, font loading, asset delivery, or CDN caching strategies.
- A user asks about JavaScript execution performance, long tasks, main thread blocking, or web worker offloading.
- A user asks about memory leaks, memory bloat, garbage collection pressure, or detached DOM node issues.
- A user asks about performance budgets, performance CI gates, or performance regression detection.
- A user asks about Real User Monitoring (RUM), synthetic monitoring, or performance observability.
- A user asks about server-side rendering performance, hydration cost, streaming SSR, or partial hydration.
- A user asks about caching strategies (HTTP caching, service workers, application-level caching, CDN configuration).
- A user asks about third-party script performance impact (analytics, ads, chat widgets, tag managers).
- A user asks about network performance (request waterfall, connection management, prefetching, preloading, resource hints).
- A user asks about animation performance, CSS vs. JS animations, compositor layers, or paint optimization.
- A user asks about perceived performance, loading UX patterns (skeleton screens, progressive loading, optimistic UI).
- A user asks how to set up performance testing, benchmarking, or load testing for frontend applications.
- A conversation involves terms such as "Lighthouse," "PageSpeed," "WebPageTest," "performance budget," "bundle size," "chunk," "lazy load," "code split," "tree shake," "re-render," "virtualization," "throttle," "debounce," "requestIdleCallback," "requestAnimationFrame," "layout shift," "paint," "composite," "critical rendering path," "resource hint," "preload," "prefetch," "preconnect," "service worker," "cache," "CDN," "compression," "minification," "source map," "profiler," "flame chart," "heap snapshot," "memory leak," "jank," "frame rate," "long task," or similar performance language.

Do NOT activate this skill for backend performance or database optimization questions with no frontend dimension, general frontend architecture decisions without a performance focus, pure UX/design discussions without performance implications, or SEO questions that do not involve performance metrics.

## Instructions

Work through the six phases below. Phase 3 is the largest and is split across three reference files. Every phase's full, step-by-step detail lives in its reference file; the summaries here identify the decision points at each stage.

### Phase 1 — Performance Context and Baseline Assessment

First **classify the engagement** (reactive diagnosis, proactive audit, optimization planning, performance infrastructure, or focused technique question) and **state it explicitly** — this sets depth and sequence. Then **gather context** (app type, tech stack, available performance data, audience/devices, hosting/CDN, traffic, targets, constraints). **Baseline before optimizing:** collect lab data (Lighthouse with mobile throttling, DevTools Performance/Network panels, bundle analysis) and field data (CrUX, RUM), documented in a standard format. Finally **define 95-grade targets and budgets** (Core Web Vitals, bundle size, interaction responsiveness) and validate them with the user.

See references/phase1-context-and-baselines.md for the full baseline methodology, thresholds, budget tables, and documentation format.

### Phase 2 — Performance Diagnosis and Root Cause Analysis

Diagnose systematically, metric by metric: map the **critical rendering path** (Step 5); diagnose **LCP** by decomposing it into TTFB, load delay, load duration, and render delay (Step 6); diagnose **INP** as input delay, processing time, and presentation delay (Step 7); diagnose **CLS** from its sources (Step 8). Then analyze the **JS bundle** (treemap, code-splitting, parse cost — Step 9), the **network waterfall** (request count, chains, origins, prioritization, compression, resource hints — Step 10), **rendering/paint** (layout reflow, thrashing, compositor layers, CSS — Step 11), **memory** (heap snapshots, leak patterns — Step 12), and **third-party script impact** (inventory, load method, optimization strategies — Step 13).

See references/phase2-diagnosis.md for the complete diagnostic procedures, decomposition formulas, root-cause tables, code samples, and tooling for each step.

### Phase 3 — Optimization Implementation

**Prioritize optimizations by impact and effort** using the P0–P3 priority matrix, and document each fix in a standardized PERF-format (Step 14). Then implement in dependency order: **resource loading** — critical CSS inlining, JS loading strategy, resource hints, HTTP caching (Step 15); **images** (format decision tree, responsive `srcset`, loading strategy, CDN, Step 16) and **fonts** (self-hosting, WOFF2/subsetting, font-display/FOUT, Step 17); **code splitting and lazy loading** (React lazy/Suspense, IntersectionObserver, dynamic import — Step 18); **rendering** (re-render prevention, state colocation, virtualization, Web Workers — Step 19); and **perceived performance** (skeletons, optimistic UI, instant navigation, progressive loading — Step 20).

Because this phase is dense, its detail is split across files, each with copy-paste code:
- Prioritization and resource loading: references/phase3-planning-and-resource-loading.md
- Images, fonts, and code splitting: references/phase3-assets-images-fonts-splitting.md
- Rendering and perceived performance: references/phase3-rendering-and-perceived-performance.md

### Phase 4 — Performance Monitoring and Regression Prevention

Instrument **RUM** continuously (web-vitals library, custom metrics, segmentation dimensions, SLOs/alerting — Step 21), add **synthetic monitoring** (Lighthouse CI assertions, scheduled tests — Step 22), enforce **performance budgets in CI** (bundlesize/size-limit, import-cost guards, regression gates — Step 23), and run a recurring **review and improvement process** (weekly reviews, per-release validation, quarterly audits, culture practices — Step 24).

See references/phase4-monitoring.md for the RUM code, Lighthouse CI configuration, budget tooling, CI pipelines, and review process.

### Phase 5 — Advanced Performance Patterns

Go beyond basic fixes: layer **caching** across the stack (browser HTTP, service worker, application-level, CDN/edge — Step 25); optimize **SSR/hydration** (diagnose hydration cost; streaming, selective, progressive, partial hydration, resumability, server components — Step 26); implement **animation/visual** performance (compositor-friendly properties, CSS/JS animation, scroll-driven animation, `content-visibility`, `will-change` rules — Step 27); and apply **advanced network** patterns (Speculation Rules API, request batching/deduplication/prioritization, Brotli compression — Step 28).

See references/phase5-advanced-patterns.md for the caching layers, hydration strategy tables, animation property rules, and speculation-rules code.

### Phase 6 — Performance Deliverable Assembly

**Compose the report** in a fixed structure (executive summary, context, baselines, targets, diagnosis findings per metric, prioritized plan, implementation guidance, monitoring plan, expected results, open questions — Step 29). **Adapt depth to the user's need** (quick question, metric optimization, bundle optimization, full audit, infrastructure setup, code review — Step 30). Operate an **empirical, iterative loop** — measure → hypothesize → optimize → verify — tying every recommendation to measured evidence (Step 31).

See references/phase6-deliverable.md for the full report outline, depth-adaptation matrix, and the iterative approach details.

## Cross-Cutting Rules

These apply across all phases:

- **Measure before experimenting.** Never recommend an optimization without measured evidence of a problem; premature optimization adds complexity without proven benefit.
- **Verify after every change.** Re-measure the affected metrics after each change to confirm improvement and catch regressions, and invite the user to share updated measurements so recommendations can be refined.
- **Ship 95+. (New build / delivered UI)** Whenever the agent generates or refactors any frontend, self-verify every page against the Non-Negotiable Lighthouse Default — run Lighthouse (or Lighthouse CI), confirm all four categories ≥ 95/100 at the stricter 95-grade thresholds and run the Steps 6–8 / 14–20 / 23 optimizations, re-measure, and report the four scores plus Core Web Vitals as proof of a smooth, consistent UI.
- **Stay current.** New browser APIs (`Speculation Rules`, `scheduler.yield()`, `Popover`, `View Transitions`, CSS `content-visibility`, `@scope`, `@layer`) can obsolete older techniques — recommend modern approaches where browser support matches the user's support matrix.