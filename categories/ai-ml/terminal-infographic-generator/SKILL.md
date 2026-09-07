---
name: terminal-infographic-generator
description: "Generate dense retro-cyberpunk terminal-style infographic posters (ASCII, orange-on-charcoal) for architecture and launch visuals."
license: MIT
tags:
- image-generation
- infographic
- design
---

# Terminal Poster

Generate dense, on-brand infographic posters in a **terminal-aesthetic visual style** — dark + orange + pixel-bitmap + ASCII + brutalist minimalism. The look popularized by [@shannholmberg](https://x.com/shannholmberg) for his viral Hermes Agent posts on X, generalized into a reusable system.

Pattern reverse-engineered from 27 image-summary posts (12 of them deep-audited). 5 reusable templates — A, B, C, D, E — share one design DNA. Cluster C and D each have 2 sub-modes (C1 painterly / C2 pixel, D1 step pipeline / D2 terminal-window). Tested live with Nano Banana Pro — Cluster A audited hit **99%**, Cluster C1 painterly hit **95.6%**.

> **Fresh agent? Start here:** 1) Read this SKILL.md top-to-bottom. 2) Pick a cluster using the decision tree below. 3) **Fast path** — for any cluster (A–E), write a YAML spec and run `scripts/make-poster.sh spec.yaml out.png`. See example-specs/. 4) **Manual path** — for custom edits beyond what the spec covers, open the matching `references/templates/cluster-X-*.md`, fill placeholders, run `scripts/generate.sh`. 5) Vision-audit the output. The full design rules live in `references/design-dna.md` — read it once for context.

# Decision tree — which template to use?

```
What is the topic?
├── Pure system architecture / framework / diagram (org charts, pipelines)
│   └── 🔴 USE CLUSTER A (ASCII Terminal) — highest fidelity (94-99% audited), cheapest to nail
│
├── Leveled comparison / maturity model / "5 ways to X"
│   └── 🟡 USE CLUSTER B (Color-Coded Levels)
│
├── Feature launch / viral hook / "X changed how I work"
│   └── 🔴 USE CLUSTER C (Cyborg Hero) — pick a sub-mode:
│       ├── 🔴 Mode C1 — PAINTERLY HERO (viral, 4/6 of Shann's Cluster C)
│       │     Use for serious launches, agent reveals, big-deal announcements
│       └── 🟡 Mode C2 — FLAT PIXEL HERO (whimsical, 2/6)
│             Use for lighter / playful / less-serious topics
│
├── Step-by-step tutorial / blueprint / process flow
│   └── 🟡 USE CLUSTER D (Blueprint) — pick a sub-mode:
│       ├── 🔴 Mode D1 — STEP PIPELINE (brand-book / playbook style)
│       │     Green-dominant, 4-7 step cards, macOS chrome dots
│       │     Use for sequential processes ("do X, then Y, then Z")
│       └── 🟡 Mode D2 — TERMINAL-WINDOW MOCKUP (premium thought-piece)
│             Fake terminal floating over painterly canvas
│             Use for single concepts framed as "the rule"
│
└── Brand identity / design system / voice doc
    └── 🟢 USE CLUSTER E (Editorial) — rare, only when topic is literally brand
```

**Default:** When in doubt, use **Cluster A**. It's the cheapest to nail and matches the highest share of the source corpus.

# Topic → Cluster lookup (common cases)

| Topic shape | Use | Why |
|---|---|---|
| "the X agent stack" / layers / architecture | 🔴 **A** | Hierarchical, fits stacked ASCII panels |
| "the X system explained" | 🔴 **A** | Brutalist clarity is the right register |
| "introducing X" / "we just shipped X" | 🔴 **C1** | Viral hero painterly = launch energy |
| "X is whimsical / playful" / mascot reveal | 🟡 **C2** | Flat pixel hero = lighter feel |
| "4 levels of X" / "the L1-L4 of X" | 🟡 **B** | Color-coded spine handles levels well |
| "10 ways to do X" / "the X playbook" | 🔴 **D1** | Step pipeline reads left-to-right |
| "5 steps to ship X" / sequential tutorial | 🔴 **D1** | Temporal flow = pipeline |
| "the rule about X" / "X vs Y" thought-piece | 🟡 **D2** | Terminal-window framing = premium |
| "the X brand book" / design system | 🟢 **E** | Editorial spread for brand artifacts |
| Org chart / "who reports to whom" | 🔴 **A** (right-rail variant) | Box-drawing handles hierarchy |
| Tool/skill catalog | 🔴 **C1** | Card grid = catalog |

🟢 **Quick rule:** Architecture → A. Launch → C1. Playbook → D1. Levels → B. Brand → E.

# The common design DNA (applies to all 5 clusters)

> ⚠️ **Audited May 24, 2026 against 12 real images.** Many rules are CLUSTER-SPECIFIC, not universal. See `references/design-dna.md` for the full breakdown. Below is the abridged "what really holds" version.

| Element | Rule | Cluster-specific notes |
|---|---|---|
| Background | Dark — `#0E0E0E` warm charcoal default | Pure `#000` OK for high-neon B + composite canvas E |
| Foreground | Bone `#EAEAEA` off-white (or `#F0E6D2` cream for C cards) | NEVER pure `#FFF` |
| Primary accent | Orange — but the **hex varies by cluster** | `#F26B1F` for C, `#B8541F` rust for B, `#FC4A2B` red-orange for E, phosphor green `#A8E060` for D1 |
| Body text case | Lowercase | Cluster E uses sentence case |
| Section labels | ALL CAPS | Cluster A uses inline `LEVEL N:` in panel borders |
| List bullets | Cluster A: `›` right-angle quote (canonical) OR `·` middle-dot inline. Cluster B/C/D/E: `→` arrows. | NEVER `•` standard bullets in any cluster |
| Numbered badges | **`[1] [2] [3]` brackets are Cluster C ONLY** | Cluster A uses inline `LEVEL N:` labels instead |
| Bottom tagline | Always present + handle right-aligned | A/B = lowercase manifesto, C = ALL CAPS, E = editorial italic |
| Gradients | Forbidden in body cards/grids | ALLOWED for hero radial glow (C Mode C1), aura gradient (E), painterly canvas (D2) |
| Drop shadows | Forbidden | Exception: subtle glow on hero illustration in C Mode C1 |
| Rounded corners | Forbidden | Exception: 8px on Cluster B cards, dashed-border step cards on D1 |
| Style references | Hacker zine, Pip-Boy, Bloomberg Terminal, 1990s computer manuals | Cluster E: high-end editorial magazine |

# 🚀 Fast path — use the CLI

If you know which cluster you want, the fastest way to generate a poster is the `make-poster.sh` CLI:

```bash
bash scripts/make-poster.sh \
  scripts/example-specs/your-spec.yaml \
  /tmp/output.png
```

The CLI takes a YAML spec, picks the right cluster template, fills placeholders, calls `generate.sh`, and saves the prompt next to the output for reproducibility.

**Supported clusters via CLI:** `a` (ASCII Terminal) and `c` (Cyborg Hero — both `c1` painterly and `c2` flat pixel).
**Manual fill:** `b`, `d`, `e` — use the template files directly (see Step 2 below).

**Example specs:** `scripts/example-specs/`
- `cluster-a-stack.yaml` — Cluster A engineer-poet zine, 3-panel agent stack
- `cluster-b-maturity.yaml` — Cluster B color-coded 4-level maturity ladder
- `cluster-d-playbook.yaml` — Cluster D blueprint 5-step playbook
- `c2-smoketest.yaml` — Cluster C2 whimsical flat-pixel hero

**YAML spec format (Cluster C1):**

```yaml
cluster: c
mode: c1                     # c1 painterly OR c2 flat pixel
topic: yourapp               # top-left terminal prompt subject
status: shipping             # top-left terminal status
status_2: 6 agents online    # top-right MIRRORED status (NOT a version stamp)
handle: "@yourhandle"
eyebrow: AGENT-NATIVE
brand: YOURAPP
subtitle: 6 AGENTS · ONE BRAIN
hero_subject: >
  (multi-line painterly hero description — model fills in details from the 5 composition rules)
cards:
  - {header: AGENT ONE,   icon: clipboard,        body: "..."}
  - {header: AGENT TWO,   icon: magnifying-glass, body: "..."}
  # ... exactly 6 cards
tagline_separator: star      # star | pipe | period
tagline_phrases:
  - SHIP A BRAIN NOT A PROMPT
  - PROOF OVER PROMISES
  - ONE BRAIN. SIX AGENTS.
```

**YAML spec format (Cluster A):**

```yaml
cluster: a
title: a typical agent stack
bottom_tagline: "spec in. action out. ship it."
handle: "@yourhandle"
panels:
  - label: PERCEPTION
    subject: input layer
    tagline: structured intent in
    flow: "user prompt ──▶ parser ──▶ structured spec"
    prose: "turns ambient natural-language input into a machine-readable plan."
    items: ["yaml or natural-language spec", "schema validation", "intent classification", "skill routing"]
  # ... 3-5 panels total
```

The CLI takes ~5 seconds + the generate.sh API call (~30 seconds). Cost ≈ $0.002.

# Manual workflow (when CLI doesn't fit)

## Step 1 — Gather inputs from the user

Ask for:
1. **Topic / brand name** — what the poster is about (e.g. "MarketIntell", "Hermes Agent", "Bookmark Brain")
2. **Eyebrow/kicker** — short framing label above the brand (e.g. "AGENT-NATIVE", "OPEN SOURCE")
3. **Subtitle** — what it is in 4-6 words (e.g. "the AI analyst desk")
4. **3-6 content blocks** — for the body. Each block needs: a short ALL-CAPS header, an icon concept, and 1-3 lines of body copy.
5. **Manifesto tagline** — 1-3 phrases for the bottom bar
6. **Handle / status string** — for top-right corner. Cluster C uses a mirrored `> sys$ [STATUS_2] @handle` terminal prompt (e.g. "@ravidsrk uptime 47h" or "@ravidsrk ready"). NOT a version stamp — that was wave-1 thinking, audit replaced it with a second terminal prompt.
7. **Cluster choice** — A/B/C/D/E. If unsure, suggest Cluster A.

If user already gave most of this, infer the rest. Don't re-ask.

## Step 2 — Gather accurate facts (if applicable)

If the topic is a real product/project, look up any existing notes or docs first so the poster reflects real numbers and taglines. Don't invent data.

## Step 3 — Fill the prompt template

Use one of the 5 templates in `references/templates/`. Replace `[BRACKETED PLACEHOLDERS]` with the user's content.

Templates available:
- `references/templates/cluster-a-ascii-terminal.md` — default
- `references/templates/cluster-b-color-coded.md`
- `references/templates/cluster-c-cyborg-hero.md` — viral version
- `references/templates/cluster-d-blueprint.md`
- `references/templates/cluster-e-editorial.md`

## Step 4 — Generate via Nano Banana Pro

Run the helper script:

```bash
bash scripts/generate.sh \
  /path/to/prompt.txt \
  /path/to/output.png
```

The script handles: JSON escaping → OpenRouter POST → base64 decode → save PNG.

**Always use Nano Banana Pro** (`google/gemini-3-pro-image-preview`) as default. Don't downgrade silently — Nano Banana 2 hallucinates duplicate cards on Cluster C.

## Step 5 — Verify with vision

Use `read(path, prompt="...")` to grade the output. Vision-check for:
1. Tagline typos (the word "PERIOD" appearing literally — known model failure)
2. Duplicate cards
3. Painterly hero (when prompt asks for flat pixel-art)
4. Wrong palette (drift to pure black or pure white)

If score < 80%, regenerate with tighter constraints.

## Step 6 — Preview

```
previewFile("/path/to/output.png")
```

# ⚠️ Critical pitfalls (learned the hard way)

🔴 **Forbid the word "PERIOD" explicitly.** Models spell it out as filler text in tagline bars, even when given literal `.` examples. Always include this block in any prompt with a tagline:

```
⚠️ CRITICAL TEXT RULES — read carefully before rendering letters:
• Spell every word completely. Do NOT abbreviate. Do NOT drop letters.
• The word "PERIOD" must NEVER appear in the tagline. Use a literal "." punctuation mark, not the spelled-out word.
• Each sentence ends with a single period character "." — not the word PERIOD.
• Render the dot as a small square pixel, not as letters.
• Avoid any duplicate or stuttered words.
```

🔴 **Always specify EXACT grid dimensions** for Cluster C. Say "EXACTLY a 3 columns × 2 rows = 6 cards" — not "6 cards in a grid". Models otherwise produce 4+3 asymmetric layouts or duplicate cards.

🔴 **Scope "no painterly" to the Cluster C BODY CARD GRID only.** The hero zone in Mode C1 SHOULD be painterly — that's the viral pattern (see line below). But inside the 3×2 card grid, explicitly say: "Cards are FLAT — no painterly, no shadows, no gradients inside cards." Without this scoping, the model bleeds painterly texture into the body cards and they stop reading as engineered chrome.

🟡 **Brand names with short letters** (e.g. "Polymarket") sometimes get a single glyph corrupted. If brand name is critical, either spell it out in the prompt OR run a 2nd pass.

🟡 **Use OpenRouter, not direct Google API.** The default Google `GOOGLE_GENERATIVE_AI_API_KEY` is project-blocked → 403. OpenRouter route is the reliable path.

🟢 **Cluster A is the cheapest to nail** — pure ASCII, two-tone, easy for the model. 94-99% on first try (audited). Default to it.

🔴 **For viral Cluster C posters (gBrain, control-room, skill-bundles-ship style), ALLOW painterly hero illustration.** An earlier version of this skill forbade "painterly" globally — that rule was wrong. The viral Cluster C images USE painterly cyborg portraits with radial orange glow. Forbid painterly only inside the body card grid; hero illustration may be painterly + radial glow. See cluster-c-cyborg-hero.md for the two hero modes (C1 painterly / C2 pixel-flat).

🔴 **Pick the right orange for the cluster.** `#F26B1F` is the Cluster C canonical (gBrain). Cluster B uses muted rust `#B8541F`. Cluster E uses red-orange `#FC4A2B`. Cluster D1 uses phosphor green `#A8E060` as primary, not orange. Don't reach for `#F26B1F` reflexively.

🟡 **Cluster A signature motifs are non-negotiable** — `◆` diamond separator in panel headers, `›` right-angle quote bullets, "what runs here:" ritual line, inline `LEVEL N:` labels. The skill template includes these; if a Cluster A generation lacks them, regenerate.

# Cost

- Nano Banana Pro: ~$0.002 / image
- Nano Banana 2: ~$0.0005 / image (use only for drafts)
- Typical session (3 iterations): ~$0.006

# Files in this skill

```
terminal-poster/
├── SKILL.md                         ← this file
├── scripts/
│   ├── generate.sh                  ← Low-level bash helper, takes prompt text + output path
│   ├── make-poster.sh               ← 🚀 High-level CLI, takes YAML spec + output path (recommended)
│   └── example-specs/
│       ├── cluster-a-stack.yaml     ← Cluster A engineer-poet (3-panel agent stack)
│       ├── cluster-b-maturity.yaml  ← Cluster B color-coded (4-level ladder)
│       ├── cluster-d-playbook.yaml  ← Cluster D blueprint (5-step playbook)
│       └── c2-smoketest.yaml        ← Cluster C2 whimsical flat-pixel hero
└── references/
    ├── design-dna.md                ← full pattern doc (palette, fonts, layout rules)
    ├── templates/
    │   ├── cluster-a-ascii-terminal.md  ← DEFAULT
    │   ├── cluster-b-color-coded.md
    │   ├── cluster-c-cyborg-hero.md     ← VIRAL
    │   ├── cluster-d-blueprint.md
    │   └── cluster-e-editorial.md
    └── worked-examples.md           ← real test results, lessons learned
```

# Worked examples

See `references/worked-examples.md` for an iteration log — scores from 70% (Nano Banana 2 first try) → 99% (audited Cluster A), with the lessons that produced each jump.

# Credits

Visual pattern reverse-engineered from [@shannholmberg](https://x.com/shannholmberg) on X. He didn't design this skill — he designed the look. This skill just makes the look reproducible across topics.
