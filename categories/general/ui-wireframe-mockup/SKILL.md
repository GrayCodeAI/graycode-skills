---
name: ui-wireframe-mockup
description: "Creates lo-fi wireframes for UI structure and hi-fi mockups for visual directions across landing pages, dashboards, and app screens."
license: MIT
tags:
- ui-design
- wireframes
- mockups
- prototyping
---

# Craft UI

Two phases over the brief and the other supplied inputs. The wireframe phase is optional: when it runs, it settles the arrangement and passes it to mockups through `structure.yaml`; without it, each mockup direction chooses its own arrangement.

## Triggers

- **Wireframes** ("plan the layout", "map the screen flow", "arrange the screens", "compare arrangements", "settle the structure first") → wireframes.md
- **Mockups** ("generate directions", "compare looks", "preview a direction", "try an editorial direction", "adjust the chosen look") → mockups.md

## Workflow

```text
[wireframes] → structure.yaml → mockups → docs/design/mockup.html
      └──────── skipped ────────┘  (each direction picks its own arrangement)
```

Final copy comes after the mockup and is an input to neither phase.
