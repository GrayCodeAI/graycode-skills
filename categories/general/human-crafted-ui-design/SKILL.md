---
name: human-crafted-ui-design
description: "Produce human-crafted, non-template frontend UIs via intent-first analysis, mode classification, and library selection."
license: MIT
tags:
- ui
- design
- frontend
- animation
- aesthetics
---

# Skills

This skill is the agent's guarantee of **visual craft**. It exists so that any frontend the agent generates looks like a senior human designer/engineer built it on purpose for that specific product — never a recycled template with generic AI tells. The agent must treat this skill as mandatory whenever it is triggered, and it must complete the intent-first analysis below BEFORE writing any code. Skipping the analysis phase is forbidden.

## When to use

Activate this skill when the user's prompt contains ANY of the following terms or signals:

- `landing page`, `showcase`, `portfolio`, `personal website`, `marketing site`, `brand site`, `product page`, `pricing page`, `website`, `web design`, `redesign`.
- `hero section`, `navbar`, `footer`, `CTA`, `sections`, `page layout`, `UI`, `interface`, `frontend`, `component`, `mockup`, `wireframe`.
- `design`, `aesthetic`, `beautiful`, `elegant`, `premium`, `polished`, `clean`, `modern`, `minimal`, `creative`, `sleek`, `stunning`, `impressive`.
- `animation`, `micro-interaction`, `smooth scroll`, `parallax`, `scroll animation`, `hover effect`, `transition`, `motion`, `marquee`, `fade`, `reveal`.
- `doesn't look AI-generated`, `human made`, `human crafted`, `not AI generated`, `awwwards`, `showit`, `wow`, `eye-catching`, `attractive`.
- `SaaS`, `dashboard`, `app`, `product site`, `like Google`, `like Vercel`, `like Linear`, `like Stripe`, `like Apple`, `conversion-focused`.
- User pastes existing website code, a URL, a screenshot, or a design reference and asks to match or improve it.
- ANY task that involves building or restyling a user-facing website/interface, even if no style keyword is present.

When in doubt, activate. This skill composes with `frontend-core`, `ui-ux`, and `frontend-performance` — craft governs HOW it looks, the others govern correctness and speed.

## Instructions

### Phase 0 — Intent-First Analysis (MANDATORY, do this BEFORE any code)

Never generate UI directly from a prompt. Execute these steps in order and briefly state the outcome of each so the user can follow your reasoning.

1. **Deconstruct the project intent.**
   - What is being built? (portfolio, SaaS dashboard, product landing, marketing funnel, e-commerce, agency site, blog...)
   - Who is the audience and what is the primary goal — convert, inform, impress, or demonstrate capability?
   - What brand/product story should the visual voice carry?
   - Restate in one line: *"This site exists to help [audience] [outcome] by [mechanism], and should feel [3 emotion/quality words]."*

2. **Classify the mode.** Select exactly one and state it:
   - **Mode A — Showcase / Portfolio / Immersive (Awwwards-grade):** the site IS the product; the design must astonish. Full expressive freedom.
   - **Mode B — SaaS / Product / Utility (Google-Vercel-Stripe-Linear grade):** the product is the product; the design must be crisp, credible, restrained, and conversion-focused.
   - **Mode C — Marketing hybrid:** storytelling pages (hero, features, testimonials, pricing) with moderate flair and strong conversion structure.
   - If uncertain, ASK the user before proceeding.

3. **Decide structure and visual voice.** Based on intent + mode, commit to the hero composition, section rhythm, color voice, typographic voice, and motion language for THIS project. Document each decision with a one-line "why" (industry-level reasoning, as a senior designer would).

4. **Select libraries and components.** Choose the tooling that best fits the intent from the Human-Crafted Tooling Kit (below). State your choices and why.

5. **Take user input where ambiguous.** If style direction, hero disposition, color mood, section order, or page scope is unclear, ask the user targeted questions (2–4 max) so the output matches their expectation. Never silently pick a default when the user's intent is genuinely ambiguous.

6. **Run the MoodboardGate for award-level builds.** For Mode A (and Mode C with a premium client), calibrate the aesthetic direction before any UI layout:
   - **Positioning calibration:** Premium (sleek, functional, high-tech, accessible perfection — Apple / fintech) vs. Luxury (exclusive, artisanal, high-scarcity, heritage-driven — Rolex / haute couture). State which one and what it forbids (luxury forbids generic SaaS-meets-tech gloss; premium forbids heritage styling).
   - **Keyword direction:** Map client preferences into exact visual keywords — `Dark Mode Aesthetics`, `Modern Fintech Atmosphere`, `Clean & Immersive Layout`, `High Visual Hierarchy`, `Smooth Transitions` — and derive the palette, type mood, and motion language from those keywords.
   - **Dual moodboard:** Offer two concrete directions, Direction A (Bold & Cinematic — high-contrast type, large headlines, punchy visual energy) and Direction B (Minimal & Tech-Minimal — immersive micro-typography, subtle grids, refined dark-mode atmosphere). Require the client/user to pick a direction or specific reference shots BEFORE starting the layout.
   - **Artifact:** record the chosen direction, keywords, and reference shots in the project's design doc (e.g. `docs/DESIGN.md` `## Design Direction`).

7. **Only then generate code.**

### Human-Crafted Tooling Kit (use popular, production-grade libraries)

Never hand-roll polished primitives. Leverage proven libraries so the result looks professional:

- **Icons:** Lucide, Phosphor, Tabler, Heroicons, react-icons (one consistent set per project).
- **Component primitives:** shadcn/ui, Radix UI, Headless UI, MUI, Chakra UI, daisyUI (for Tailwind) — base these on tokens and restyle for uniqueness.
- **Styling:** Tailwind CSS with CSS custom-property design tokens (default), or CSS Modules / CSS-in-JS per project conventions.
- **Motion:** Framer Motion (React), GSAP + ScrollTrigger, Motion One, Lenis (smooth scroll), Web Animations API for light touches.
- **Typography:** pick a deliberate pairing (e.g., display serif + clean sans, or a distinctive grotesque + mono accents). Use Google Fonts / Fontsource, variable fonts.
- **Visual effects:** grain/noise overlays (SVG or CSS), gradient meshes, clip-path shapes, backdrop-blur, box-shadow layering, borders with alpha.
- Use `next/font` or equivalent for self-hosted, performant fonts.
- **Stack selection (award-level):** match the platform to project scale and client needs:
  - **Client-managed CMS + custom motion** → Webflow + GSAP / custom JS (agency marketing sites where the client edits content).
  - **Rapid interactive landing page** → Framer + React components (fast marketing pages with built-in interactive motion).
  - **Heavy 3D / custom WebGL engine** → Next.js + Three.js / GSAP / Lenis (ultra-high-performance, award-level 3D/WebGL apps).

### Library-First Principle (Human-Written Over Self-Written) — MANDATORY

Leverage the ecosystem so the output is crafted, maintainable, and human-looking rather than naive from-scratch code:

- **Use mature, maintained, human-written libraries for every standard concern** — icons, components, state, forms, validation, animation, smooth scroll, date/number formatting, toast, charts, code highlighting, image optimization. Do not reimplement what the ecosystem already solves.
- **Write custom code ONLY when** no suitable library exists, or the need is genuinely project-unique business/interaction logic (brand-specific pattern, proprietary behavior).
- **Decision gate per need:**
  1. Mature, popular, maintained library exists? → **USE it** (name it and say why).
  2. Library exists but is overkill → choose a smaller mainstream alternative first.
  3. No library, or need is genuinely unique → write custom, typed, documented code and state *why* no library was used.
- **Result:** the AI writes less code and leans more on proven human-written libraries, so the output is expected, production-grade, and looks genuinely hand-crafted.
- State in the output contract which libraries were used per concern and where custom code was deliberately written.

### Mode A — Showcase / Portfolio (Awwwards-grade)

Aim: the visitor should feel craft and intent on first paint. Guidelines:

- **Oversized, expressive typography:** large display type, tight leading, intentional line breaks, mixed-case accents. Break the 12-column norm with editorial, asymmetric layouts.
- **Smooth scroll & scroll choreography:** Lenis smooth scrolling; GSAP ScrollTrigger / Framer Motion `useScroll` reveals, parallax layers, pinned/sticky sections, scroll-driven marquees.
- **Motion language:** staggered entrances, magnetic hover, custom cursor, cursor-follow elements, button micro-interactions, animated counters, marquee text, hover-distortion on images.
- **Texture & depth:** grain/noise overlay, subtle gradients, layered shadows, borders, glassmorphism used deliberately (never default).
- **Immersive extras:** canvas/WebGL effects, shaders, particle systems, interactive hero — only where they serve the story and stay performant.
- **Dark/light interplay:** bold dark sections contrasted with light ones to control rhythm and focus.
- **Restraint rule:** even at this level, drama must be purposeful. One dominant effect per viewport; never animate everything at once.
- **Prototype before polishing code:** for scroll-driven animation, validate it as a motion prototype first — model section pin states, horizontal scroll triggers, and hover transitions — then export a short video walkthrough showing exact timing, easing, and spatial relationships for the developer to implement faithfully.

### Mode B — SaaS / Product (Google-Vercel-Stripe-Linear grade)

Aim: instant credibility, clarity, and trust. The UI must feel engineered, not decorated.

- **Restraint and precision:** crisp spacing system, clear hierarchy, one or two accent colors max, generous but disciplined whitespace.
- **Trust-building content:** real product screenshots or UI mockups (not browser-chrome placeholders), feature grid with concrete benefits, metrics/numbers, logos, testimonials, pricing tables, FAQ.
- **Subtle micro-interactions only:** button state changes, hover lifts, skeleton loaders, smooth accordions, toasts. No decorative overload, no gratuitous animation.
- **Consistent, tokenized components:** shadcn/ui/Radix-based components with strict tokens; everything must feel part of one system.
- **Functional clarity:** every section has one job; CTAs are unambiguous; copy is concrete (no empty marketing fluff).
- **Conversion-focused structure:** hero → social proof → problem/features → how it works → testimonials → pricing → FAQ → final CTA → footer.

### Anti-AI-Tell Checklist (NEVER ship these in any mode)

These patterns instantly signal "AI-generated." Audit your output against every item before presenting it.

- [ ] No centered-everything default layout (hero centered + all sections centered + centered footer). Vary alignment deliberately.
- [ ] No generic purple→blue full-hero gradient as the default look.
- [ ] No "Build something amazing", "Unlock your potential", "Welcome to X" placeholder copy. Write concrete, product-specific copy.
- [ ] No Inter/system-font-only flatness. Use a deliberate type pairing with real hierarchy.
- [ ] No boring 3-column card grid as the only layout (feature cards, stats, etc.). Vary the pattern per project.
- [ ] No stock browser-chrome screenshots / placeholder app mockups. Use real product UI or custom-crafted mockups.
- [ ] No identical buttons everywhere with no hover/depth/state treatment.
- [ ] No full-width symmetric coastline sections repeated top-to-bottom. Introduce asymmetry, overlap, varied rhythm.
- [ ] No default rounded-corner-everything cards with a flat 1px border. Use elevation, tinted backgrounds, layered borders.
- [ ] No generic stock-photo look or lorem-ipsum content when real content can be synthesized.
- [ ] No default dark-purple hero + white body combo as a crutch.
- [ ] No missing states: no focus rings, no hover states, no loading/empty/error treatment.

### Uniqueness Rule (every build differs from every other build)

No two websites this agent produces may look like variations of the same template. Variation must come from intent + explicit user input, not randomness:

- Before coding, deliberately vary the **Top-6 layout levers** and record the choices:
  1. Hero composition (split, asymmetric, full-bleed image, editorial, sticky-typography, bento, etc.)
  2. Section rhythm (alternating bands, staggered widths, overlapping blocks, numbered chapters, etc.)
  3. Color voice (dark-first, light-first, accent-driven, duotone, print-inspired, brand-locked)
  4. Motion direction (reveal axis, marquee speed/direction, parallax depth, hover behavior)
  5. Typographic scale and pairing (serif display, grotesque, mono accents, editorial caps)
  6. Content structure (case-study, bento, narrative, dashboard-like, magazine, single-scroll)
- Derive the choices from the user's stated intent and answered questions. If the user has no preference, pick the combination that best serves the product — and say why.
- Output statement: end each build with *"Why this design is unique to this project:"* + 2–3 bullets tying the levers to the specific product.

### Reference Handling (user pastes code / a URL / a screenshot)

When the user gives an existing hero section, component, or full site as a reference and asks you to match it:

1. **Deconstruct the reference.** Extract: layout system (grid/flex), spacing rhythm, colors, typography (families, sizes, weights, tracking), radii, shadows, borders, effects (blur, gradients, noise), and animations (triggers, durations, easings).
2. **Map it to tokens.** Convert the extracted values into your project's design tokens so the style is preserved and consistent.
3. **Rebuild faithfully.** Reproduce the same composition and feel for the user's requested area, adapted to the project context — keep the visual DNA, adjust only what the new content requires.
4. **Validate.** Confirm in your output that the final result matches the reference's style and note any intentional deviations and why.

### Output Contract

Every delivered UI must include:

1. **Mode selected + why** (Mode A / B / C).
2. **Intent analysis summary** (what was built, for whom, with which goal).
3. **Libraries/component set chosen + why.**
4. **Motion/animation plan** (what animates, trigger, easing, reduced-motion handling).
5. **Anti-AI-tell self-check** — confirm each checklist item passes.
6. **Uniqueness statement** — the varied Top-6 levers and why they fit this project.
7. **Accessibility + performance note** — semantic HTML, keyboard operability, `prefers-reduced-motion`, and GPU-friendly animation properties (see `frontend-performance` for the 95+ Lighthouse guarantee).
