---
name: webgl-game-engine
description: "Build browser-based 3D games and interactive apps using entity-component architecture, WebGL/WebGPU rendering, and editor-first workflows."
license: MIT
tags:
- game-engine
- three-d
- webgl
- ecs
---

# PlayCanvas Engine Skill

Lightweight WebGL/WebGPU game engine with entity-component architecture, visual editor integration, and performance-focused design.

## When to Use This Skill

Trigger this skill when you see:
- "PlayCanvas engine"
- "WebGL game engine"
- "entity component system"
- "PlayCanvas application"
- "3D browser games"
- "online 3D editor"
- "lightweight 3D engine"
- Need for editor-first workflow

Compare with:
- **Three.js**: Lower-level, more flexible but requires more setup
- **Babylon.js**: Feature-rich but heavier, has editor but less mature
- **A-Frame**: VR-focused, declarative HTML approach
- Use PlayCanvas for: Game projects, editor-first workflow, performance-critical apps

---

## Core Concepts

### 1. Application

The root PlayCanvas application manages the rendering loop.

```javascript
import * as pc from 'playcanvas';

// Create canvas
const canvas = document.createElement('canvas');
document.body.appendChild(canvas);

// Create application
const app = new pc.Application(canvas, {
  keyboard: new pc.Keyboard(window),
  mouse: new pc.Mouse(canvas),
  touch: new pc.TouchDevice(canvas),
  gamepads: new pc.GamePads()
});

// Configure canvas
app.setCanvasFillMode(pc.FILLMODE_FILL_WINDOW);
app.setCanvasResolution(pc.RESOLUTION_AUTO);

// Handle resize
window.addEventListener('resize', () => app.resizeCanvas());

// Start the application
app.start();
```

---

### 2. Entity-Component System

PlayCanvas uses ECS architecture: Entities contain Components.

```javascript
// Create entity
const entity = new pc.Entity('myEntity');

// Add to scene hierarchy
app.root.addChild(entity);

// Add components
entity.addComponent('model', {
  type: 'box'
});

entity.addComponent('script');

// Transform
entity.setPosition(0, 1, 0);
entity.setEulerAngles(0, 45, 0);
entity.setLocalScale(2, 2, 2);

// Parent-child hierarchy
const parent = new pc.Entity('parent');
const child = new pc.Entity('child');
parent.addChild(child);
```

---

### 3. Update Loop

The application fires events during the update loop.

```javascript
app.on('update', (dt) => {
  // dt is delta time in seconds
  entity.rotate(0, 10 * dt, 0);
});

app.on('prerender', () => {
  // Before rendering
});

app.on('postrender', () => {
  // After rendering
});
```

---

### 4. Components

Core components extend entity functionality:

**Model Component**:
```javascript
entity.addComponent('model', {
  type: 'box',           // 'box', 'sphere', 'cylinder', 'cone', 'capsule', 'asset'
  material: material,
  castShadows: true,
  receiveShadows: true
});
```

**Camera Component**:
```javascript
entity.addComponent('camera', {
  clearColor: new pc.Color(0.1, 0.2, 0.3),
  fov: 45,
  nearClip: 0.1,
  farClip: 1000,
  projection: pc.PROJECTION_PERSPECTIVE  // or PROJECTION_ORTHOGRAPHIC
});
```

**Light Component**:
```javascript
entity.addComponent('light', {
  type: pc.LIGHTTYPE_DIRECTIONAL,  // DIRECTIONAL, POINT, SPOT
  color: new pc.Color(1, 1, 1),
  intensity: 1,
  castShadows: true,
  shadowDistance: 50
});
```

**Rigidbody Component** (requires physics):
```javascript
entity.addComponent('rigidbody', {
  type: pc.BODYTYPE_DYNAMIC,  // STATIC, DYNAMIC, KINEMATIC
  mass: 1,
  friction: 0.5,
  restitution: 0.3
});

entity.addComponent('collision', {
  type: 'box',
  halfExtents: new pc.Vec3(0.5, 0.5, 0.5)
});
```

---

## Patterns & Reference

The full common patterns, integration recipes, performance guidance, and pitfall fixes for this library live in references/patterns.md. Read the section relevant to the current task instead of the whole file; each section is self-contained with runnable examples.

## Resources

- scripts/ - automation and generator utilities for this library.
- references/ - API reference and pattern docs (see patterns.md for the moved patterns sections).
- assets/ - starter templates and examples.