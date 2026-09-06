---
name: two-d-rendering-entry-point
description: "Route and apply 2D rendering tasks covering application setup, scene graph, sprites, graphics, text, events, and the per-frame ticker."
license: MIT
tags:
- two-d
- rendering
- webgl
- scene-graph
---

Entry point for the PixiJS v8 skill collection. PixiJS is the fastest library available for the web, working across all devices and allowing you to create rich, interactive graphics and cross-platform applications using WebGL, WebGPU, and Canvas as a fallback.

## How to use this skill

1. Find the specialized skill in the router below that best matches the task.
2. Load that skill's `SKILL.md` and follow its guidance.
3. If no sub-skill fits (the task references a specific class, function, option, or API surface not listed below), **WebFetch `https://pixijs.download/release/docs/llms.txt`**. That file is the auto-generated, always-current index of the full PixiJS API and guides. Each entry links to a `.html.md` page you can WebFetch for the detailed content.

## Skill router

### Foundations

| Skill | Load when... |
|---|---|
| pixijs-application | Creating or configuring a PixiJS `Application`, calling `app.init()`, accessing `app.stage`/`renderer`/`canvas`/`screen`, resize/ticker plugins, `app.destroy()`. |
| pixijs-core-concepts | Understanding the renderer pipeline, choosing WebGL/WebGPU/Canvas, render loop internals, systems and pipes. |

### Scene Objects

| Skill | Load when... |
|---|---|
| pixijs-scene-container | Working with `Container`: `addChild`/`removeChild`, transforms, `zIndex`, bounds, `toGlobal`/`toLocal`, `destroy`. |
| pixijs-scene-sprite | Drawing images: `Sprite`, `AnimatedSprite`, `NineSliceSprite`, `TilingSprite`. |
| pixijs-scene-graphics | Drawing vector shapes or paths: `Graphics`, `GraphicsContext`, `fill`/`stroke`, `FillGradient`, SVG. |
| pixijs-scene-text | Rendering text: `Text`, `BitmapText`, `HTMLText`, `SplitText`, `TextStyle`. |

### Utilities

| Skill | Load when... |
|---|---|
| pixijs-assets | Loading resources: `Assets.init`, `Assets.load`, bundles, manifests, spritesheets, caching. |
| pixijs-events | Handling pointer/mouse/touch/wheel input: `eventMode`, `FederatedEvent`, `hitArea`, `cursor`, drag. |
| pixijs-ticker | Per-frame logic or controlling the render loop: `Ticker`, `deltaTime`, `UPDATE_PRIORITY`, `maxFPS`. |

### Effects

| Skill | Load when... |
|---|---|
| pixijs-filters | Applying visual effects: `BlurFilter`, `ColorMatrixFilter`, `DisplacementFilter`, `Filter.from`, `pixi-filters`. |

## Fallback: canonical PixiJS docs

If the task references a class, function, option, or API surface not covered by any sub-skill above, **WebFetch `https://pixijs.download/release/docs/llms.txt`**. It's the auto-generated index of the full PixiJS API and guides, regenerated on every release. Each entry links to a `.html.md` page you can WebFetch for the detailed content. Use this fallback whenever the router table doesn't point at an obvious match.
