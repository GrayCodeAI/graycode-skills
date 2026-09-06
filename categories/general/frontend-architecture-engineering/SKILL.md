---
name: frontend-architecture-engineering
description: "Use when designing or refactoring frontend architecture — components, state, styling, data fetching, accessibility, testing, and build tooling — for scalable client-side apps."
license: MIT
tags:
- frontend
- architecture
- components
- state-management
- accessibility
---

# Skills

This skill serves as the AI agent's comprehensive framework for tackling any frontend engineering challenge — from greenfield application architecture to component design, performance tuning, accessibility remediation, and frontend infrastructure decisions. The agent should treat each phase as a structured checkpoint, producing concrete recommendations, code patterns, or architectural artifacts before advancing. All guidance must be practical, implementation-ready, and grounded in modern frontend best practices.

## When to use

Activate this skill when any of the following conditions are detected:

- A user asks for help designing or structuring a frontend application from scratch.
- A user asks about frontend architecture decisions: component hierarchy, state management strategy, routing patterns, or rendering strategy (CSR, SSR, SSG, ISR).
- A user needs help designing, building, or refactoring UI components (atomic design, compound components, render props, headless components, etc.).
- A user asks about state management approaches (local state, context, Redux, Zustand, Jotka, signals, URL state, server state, etc.).
- A user needs guidance on styling strategy (CSS modules, CSS-in-JS, Tailwind, design tokens, theming).
- A user asks about data fetching, API integration, caching, or real-time data in the frontend.
- A user requests help with frontend performance optimization (bundle size, rendering performance, Core Web Vitals, lazy loading, code splitting).
- A user asks about accessibility (WCAG compliance, ARIA patterns, keyboard navigation, screen reader support).
- A user needs help with frontend testing strategy (unit, integration, E2E, visual regression, accessibility testing).
- A user asks about build tooling, bundling, CI/CD for frontend, or developer experience improvements.
- A user needs help with responsive design, cross-browser compatibility, or progressive enhancement.
- A user asks about frontend security (XSS prevention, CSP, CSRF, dependency security, input sanitization).
- A user asks about internationalization (i18n), localization (l10n), or RTL support.
- A user asks about design systems, component libraries, or shared UI infrastructure.
- A user asks about error handling, error boundaries, fallback UIs, or frontend resilience patterns.
- A user presents existing frontend code or architecture and asks for a review, critique, or refactoring guidance.
- A user asks to build or restyle a landing page, showcase, portfolio, marketing site, hero section, or any UI where visual craft, aesthetic polish, animations, or "not looking AI-generated" is a priority — in these cases ALSO load `frontend-craft` and complete its intent-first analysis before applying the engineering guidance here.
- A conversation involves terms such as "component," "React," "Vue," "Angular," "Svelte," "Next.js," "Nuxt," "SvelteKit," "Astro," "SPA," "SSR," "SSG," "hydration," "virtual DOM," "signals," "hooks," "state management," "CSS," "Tailwind," "Webpack," "Vite," "Turbopack," "tree shaking," "code splitting," "lazy loading," "Core Web Vitals," "LCP," "CLS," "INP," "accessibility," "ARIA," "responsive," "breakpoint," "design tokens," or similar frontend language.

Do NOT activate this skill for backend-only architecture questions with no frontend dimension (use product-architecture-design instead), pure requirements elicitation with no frontend implementation context (use requirements-analysis instead), or mobile-native development (Swift, Kotlin, Flutter, React Native) unless the question explicitly involves shared web/hybrid concerns.

## Instructions

The phases below are the execution checkpoints. Deep, step-by-step guidance for each phase lives in `references/`; the summary here gives the phase's intent and where to go for detail.

### Cross-Cutting Rules (Apply before and throughout all phases)

#### Mandatory UI Code Generation Defaults

These defaults exist to make LLM-generated frontend code consistent, modern, and production-ready when user requirements are incomplete.

- **Default UI Generation Profile (use unless user explicitly overrides):**
  - Framework/runtime: **React + TypeScript + Vite + NextJS**.
  - Styling: **Tailwind CSS + CSS custom properties design tokens**.
  - Component primitives: accessible, reusable primitives with variant-based APIs and tokenized styles.
  - Data fetching/server state: **TanStack Query**.
  - Forms/validation: **React Hook Form + Zod**.
  - Icons: one consistent icon set (e.g., Lucide) across the app.
  - Testing baseline: **Vitest + Testing Library + Playwright + axe-core**.
- **Fast-path implementation mode:** If the user asks to build UI code directly, generate code immediately using defaults. Ask clarifying questions only when blockers are critical (missing API contract, auth model, or deployment/runtime constraints that would make code incorrect).
- **Consistency-first rule:** The model must prioritize visual and structural consistency over novelty. Avoid one-off components and ad-hoc styles.

#### Non-Negotiable UI Quality Checklist (Must pass for generated code)

- Clean architecture: feature-oriented structure, reusable components, no duplicated patterns.
- Visual consistency: shared tokens for typography, spacing, radius, color, shadow, and motion.
- Component state coverage: `default`, `hover`, `focus-visible`, `active`, `disabled`, `loading`, `error`.
- Responsive integrity: mobile-first behavior validated across defined breakpoints.
- Accessibility baseline: semantic HTML, keyboard operability, visible focus, proper labels/ARIA, WCAG contrast.
- Production readiness: loading/empty/error states, defensive error handling, no placeholder-grade UI artifacts.
- Maintainability: strict typing, predictable naming, bounded component size, minimal prop complexity.

#### LLM Output Contract for UI Code Tasks (Required output shape)

For direct frontend code generation tasks, structure the output in this order:
1. Defaults selected (and why).
2. File tree.
3. Implemented components and layout primitives.
4. Accessibility notes.
5. Responsive behavior notes.
6. Quality checklist compliance summary.

#### Anti-Pattern Blacklist (Never generate these)

- Raw color/spacing/shadow/radius values in component code when tokens exist.
- Inconsistent spacing scale usage inside the same feature.
- Clickable non-semantic elements for primary actions (`div`/`span` instead of `button`/`a`).
- Custom interactive components without keyboard and ARIA behavior.
- Multiple divergent button/input/card styles across features without tokenized variants.
- Inline style sprawl in production components when a project styling system exists.

### Phase 1 — Frontend Context and Requirements Assessment

Classify the request (greenfield, feature, component, refactor, performance, a11y remediation, infra, review), gather frontend-specific requirements (product type, users, browser support, stack, team, design assets, perf/a11y/SEO/i18n targets, integration points, real-time/offline needs), and identify the 3–5 critical user interactions that will drive all later decisions.

See references/phase-1-context-and-requirements.md for the full step-by-step detail.

### Phase 2 — Frontend Architecture Design

Select the rendering strategy (CSR/SSR/SSG/ISR/streaming/islands/hybrid) with justification, choose the framework/meta-framework, design the project structure (feature-based vs. layer-based), and define the routing architecture (hierarchy, layouts, auth guards, dynamic routes, code splitting, navigation, data loading, error/404).

See references/phase-2-architecture-design.md for the full step-by-step detail, including comparison tables and file trees.

### Phase 3 — Component Architecture

Define the four-layer component hierarchy (primitives, composites, feature components, page/views), establish component design principles (single responsibility, props interfaces, composition, controlled/uncontrolled, extensibility), produce critical component API specifications, and use canonical blueprints (Button, FormField, Card, Modal, List/Table) with standardized state messaging.

See references/phase-3-component-architecture.md for the full step-by-step detail.

### Phase 4 — State Management Architecture

Classify state into eight categories (local, shared UI, server, global, URL, form, derived, persistent) with recommended approaches, design the server-state/data-fetching architecture (library, cache keys, staleness, optimistic updates, pagination, real-time sync, retries, prefetching), and design the global state architecture (store selection, structure, actions, selectors, persistence, devtools).

See references/phase-4-state-management.md for the full step-by-step detail, including the state category table and the "keep the global store small" rule.

### Phase 5 — Styling and Design System Architecture

Select and justify the styling approach, design the theming and design-token architecture (global/semantic/component tokens, dark mode, responsive tokens, type and spacing scales, mandatory token enforcement rules), and define the responsive design strategy (breakpoints, grid, container queries, touch targets, responsive images, strict layout primitives).

See references/phase-5-styling-design-system.md for the full step-by-step detail.

### Phase 6 — API Integration and Data Layer

Design the API integration layer (centralized HTTP client, per-domain service modules, type safety, unified error handling) and the form handling/validation architecture (form library, schema validation, validation timing, complex form patterns, consistent form UX).

See references/phase-6-api-integration.md for the full step-by-step detail, including the typed API module example.

### Phase 7 — Performance Architecture

Design the bundle optimization strategy (code splitting, tree shaking, bundle budgets, dependency audit, lazy loading, font optimization), the rendering performance strategy (avoiding re-renders, virtualization, debounce/throttle, web workers, animation and image optimization), and the Core Web Vitals optimization plan (LCP, INP, CLS targets with measurement).

See references/phase-7-performance.md for the full step-by-step detail.

### Phase 8 — Accessibility Architecture

Enforce semantic HTML first, apply WAI-ARIA patterns for custom widgets, define the focus management strategy, meet color/contrast requirements, define the screen reader strategy, respect reduced motion, and integrate automated and manual a11y testing.

See references/phase-8-accessibility.md for the full step-by-step detail.

### Phase 9 — Error Handling and Resilience

Design the layered error handling architecture (component error boundaries, API error handling with retry policy, unhandled error handlers, graceful degradation) and the error monitoring integration (capture payload, source maps, alerting thresholds).

See references/phase-9-error-handling.md for the full step-by-step detail.

### Phase 10 — Testing Strategy

Design the testing architecture across the testing trophy layers: static analysis, unit tests, component/integration tests, E2E tests for critical journeys, visual regression tests, and automated accessibility tests — with tools and coverage targets for each.

See references/phase-10-testing.md for the full step-by-step detail.

### Phase 11 — Frontend Security

Define protections against XSS (output encoding, CSP, sanitization), CSRF, insecure token storage and refresh flows, dependency vulnerabilities, and sensitive data handling.

See references/phase-11-security.md for the full step-by-step detail.

### Phase 12 — Build, Tooling, and Developer Experience

Design the frontend toolchain (build tool, TypeScript config, linting/formatting, git hooks, environment config, dev server, Storybook, monorepo tooling) and the CI/CD pipeline (checks per PR, staging on merge, production deployment with rollback, performance monitoring).

See references/phase-12-build-tooling.md for the full step-by-step detail.

### Phase 13 — Internationalization and Localization (if applicable)

Design the i18n/l10n architecture when multiple languages or locales are required: library, message format, translation file structure, key naming, locale detection/switching, RTL support, formatting via `Intl.*`, and the translation workflow.

See references/phase-13-internationalization.md for the full step-by-step detail.

### Phase 14 — Frontend Deliverable Assembly

Compose the structured frontend architecture document (17 sections mapping to prior steps), adapt depth to the user's need (quick consultation, component design, performance issue, full architecture, review, direct code), and maintain an iterative, collaborative approach that re-enters phases as requirements evolve.

See references/phase-14-deliverable.md for the full step-by-step detail.
