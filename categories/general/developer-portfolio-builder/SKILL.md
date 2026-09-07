---
name: developer-portfolio-builder
description: "Use to build or overhaul a personal developer or designer portfolio; gathers project details, structures hero, projects, experience, and contact sections for hiring conversion."
license: MIT
tags:
- portfolio
- personal-branding
- freelancing
- career
- conversion
---

# High-Converting Portfolio Builder

Guides an AI agent in collecting, structuring, and presenting a developer or designer's portfolio content to maximize hiring and freelancing conversion rates. The agent gathers deep project details interactively before generating any content or code, then structures the result around the sections that make a portfolio convert.

## When to Use

- Building a personal portfolio website from scratch or overhauling an existing one.
- The user wants to present 3-4 flagship projects, past roles, or freelance work to clients or employers.
- The user says any variation of "make my portfolio stand out" or "build me a portfolio".

For a general marketing site or landing page that is not a personal portfolio, run `create-website` instead — its ten-phase journey covers message, design, and conversion.

## Core Principles (Why Portfolios Fail)

- **Originality over clones.** Cool animations and 3D effects do not convert clients if the design looks identical to every other template. Focus on original design choices and problem-solving thinking.
- **The 5-second rule.** A client decides whether to stay or leave within 5 seconds. The top fold (hero) must immediately communicate: (1) who you are, (2) what exact services or role you specialize in, (3) a direct, frictionless CTA to contact or hire you. Run `storybrand-messaging` to write the headline, one-liner, and CTA with the client as hero.
- **Quality over quantity.** Limit the portfolio to **3-4** outstanding projects. Avoid displaying 15-20 average projects, unfinished experiments, or standard tutorial clones (Todo app, Weather app, basic Calculator).

## Intake

The agent **must** interactively prompt the user to collect deep details about their projects and work history before generating portfolio content or code. For extended conversational extraction, invoke `requirements-analysis`; for niche and USP work, invoke `one-page-marketing`.

### Role & Value Proposition

- "What is your primary domain or specialization (e.g., Frontend Developer, Full-Stack Engineer, Creative Developer, UI/UX Designer)?"
- "What specific business or technical problems do you solve for clients or employers?"

### Deep-Dive into Top 3-4 Projects

- "Please share details for your top 3-4 projects. For each project, provide:"
  - **Project title & live link / GitHub**
  - **Problem statement:** What problem did this project solve, or what need did it fulfill?
  - **Your role & key contributions:** What specific parts did you architect, build, or design?
  - **Tech stack & architecture decisions:** Why did you choose specific tools, frameworks, or databases?
  - **Key challenges & solutions:** What was the hardest technical or design obstacle, and how did you solve it?
  - **Results & impact:** e.g., improved load time by 40%, served 1,000+ active users, increased conversion rates.

### Past Work & Professional Experience (if applicable)

- "If you have past company, agency, or freelance client work, please provide:"
  - **Company / client name & role**
  - **Responsibilities & deliverables:** What key features or systems did you build?
  - **Standout work details:** How did your work stand out, add business value, or improve user experience?
  - **Client/employer metrics or testimonials:** Any measurable outcomes or feedback?

## Content Structure

### A. Hero Section (Above the Fold)

- **Headline:** Bold, clear statement of your specialization — no vague filler like *"I build memorable digital experiences"* without context.
- **Sub-headline:** Summary of your value proposition and primary tech stack.
- **Primary CTA:** Direct contact button (e.g., "Hire Me", "Let's Talk", "Book a Call") plus a downloadable resume link.

Draft this section with `storybrand-messaging`: one repeatable one-liner, the customer-as-hero frame, and one obvious Direct CTA. Design it with `top-design` and `web-typography` (invoked through `create-website`).

### B. Curated Projects Section

- Display only 3-4 flagship projects from the intake.
- **Each project card links to a dedicated project detail page or modal**, containing:
  - High-level summary and visual preview.
  - Problem statement and target audience.
  - Deep-dive into technical architecture and design decisions.
  - Key achievements, metrics, and live demo / repository links.

### C. Experience & Impact Section

- Detail past full-time roles, internships, or high-stakes freelance contracts.
- Highlight specific contributions, business outcomes, and real-world results rather than generic job responsibilities.
- Make every claim concrete and verifiable: pass the copy through `made-to-stick` to replace abstractions with specific numbers and named outcomes, and never invent metrics that the user did not provide.

### D. Contact & Conversion Section

- Frictionless contact options: email, LinkedIn, Twitter/X, Calendly booking link.
- Explicit response timeframe expectation (e.g., *"Replies within 24 hours"*).

## The 1-Minute Non-Tech Friend Test

Before finalizing the portfolio layout or text, run this test:

- **Verification rule:** Can a non-technical person review the hero section for 10 seconds and accurately explain what you do and how to hire you?
- If **no**, simplify the jargon, clarify the headline, and make the primary CTA more visible.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---|---|---|
| Template-look design | Blends in with every other portfolio | Drive original design via `top-design` in `create-website` |
| Vague headline | Visitor cannot tell what you do in 5 seconds | Write a specific one-liner with `storybrand-messaging` |
| 15-20 average projects | Dilutes the flagship work | Curate to 3-4 outstanding projects |
| Tutorial-clone projects | Signals inexperience, not skill | Drop Todo/Weather/Calculator-style projects |
| Features over outcomes | Reads like a resume, not proof | Lead with problem, role, and measurable results |
| Invented metrics | Kills trust the moment they are checked | Use only results the user confirmed in intake |
| Hidden or weak CTA | No obvious way to hire or contact | Add a direct, frictionless CTA above the fold |

## Hand-Off

After the intake and content structure are approved, hand the actual build to `create-website`, which sequences message, design, and conversion phases and records decisions in the project `docs/` folder. Pass the final copy through `technical-writer` for professional polish across the pages.
