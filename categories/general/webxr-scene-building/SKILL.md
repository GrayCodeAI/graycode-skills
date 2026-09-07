---
name: webxr-scene-building
description: "Build browser-based 3D, VR, and AR experiences declaratively with HTML and entity-component scenes, including controllers, lighting, and 360-degree media."
license: MIT
tags:
- webxr
- vr
- ar
- three-d
- declarative
---

# A-Frame WebXR Skill

## When to Use This Skill
- Build VR/AR experiences with minimal JavaScript
- Create cross-platform WebXR applications (desktop, mobile, headset)
- Prototype 3D scenes quickly with HTML primitives
- Implement VR controller interactions
- Add 3D content to web pages declaratively
- Build 360° image/video experiences
- Develop AR experiences with hit testing

## Core Concepts

### 1. Entity-Component-System (ECS)

A-Frame uses an entity-component-system architecture where:
- **Entities** are containers (like `<div>` in HTML)
- **Components** add functionality/appearance to entities
- **Systems** provide global functionality

```html
<!-- Entity with components -->
<a-entity
  geometry="primitive: box; width: 2"
  material="color: red; metalness: 0.5"
  position="0 1.5 -3"
  rotation="0 45 0">
</a-entity>
```

**Primitives** are shortcuts for common entity + component combinations:

```html
<!-- Primitive (shorthand) -->
<a-box color="red" position="0 1.5 -3" rotation="0 45 0" width="2"></a-box>

<!-- Equivalent entity-component form -->
<a-entity
  geometry="primitive: box; width: 2"
  material="color: red"
  position="0 1.5 -3"
  rotation="0 45 0">
</a-entity>
```

### 2. Scene Setup

Every A-Frame app starts with `<a-scene>`:

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
  </head>
  <body>
    <a-scene>
      <!-- Entities go here -->
      <a-box position="-1 0.5 -3" color="#4CC3D9"></a-box>
      <a-sphere position="0 1.25 -5" radius="1.25" color="#EF2D5E"></a-sphere>
      <a-cylinder position="1 0.75 -3" radius="0.5" height="1.5" color="#FFC65D"></a-cylinder>
      <a-plane position="0 0 -4" rotation="-90 0 0" width="4" height="4" color="#7BC8A4"></a-plane>
      <a-sky color="#ECECEC"></a-sky>
    </a-scene>
  </body>
</html>
```

The scene automatically injects:
- Default camera (position: `0 1.6 0`)
- Look controls (mouse drag)
- WASD controls (keyboard movement)

### 3. Camera Systems

**Default Camera** (auto-injected if none specified):

```html
<a-entity camera="active: true" look-controls wasd-controls position="0 1.6 0"></a-entity>
```

**Custom Camera**:

```html
<a-camera position="0 2 5" look-controls wasd-controls="acceleration: 50"></a-camera>
```

**Camera Rig** (for independent movement and rotation):

```html
<a-entity id="rig" position="0 0 0">
  <!-- Camera for head tracking -->
  <a-camera look-controls></a-camera>

  <!-- Movement applied to rig, not camera -->
</a-entity>
```

**VR Camera Rig with Controllers**:

```html
<a-entity id="rig" position="0 0 0">
  <!-- Camera at eye level -->
  <a-camera position="0 1.6 0"></a-camera>

  <!-- Left hand controller -->
  <a-entity
    hand-controls="hand: left"
    laser-controls="hand: left">
  </a-entity>

  <!-- Right hand controller -->
  <a-entity
    hand-controls="hand: right"
    laser-controls="hand: right">
  </a-entity>
</a-entity>
```

### 4. Lighting

**Ambient Light** (global illumination):

```html
<a-entity light="type: ambient; color: #BBB; intensity: 0.5"></a-entity>
```

**Directional Light** (like sunlight):

```html
<a-entity light="type: directional; color: #FFF; intensity: 0.8" position="1 2 1"></a-entity>
```

**Point Light** (radiates in all directions):

```html
<a-entity light="type: point; color: #F00; intensity: 2; distance: 50" position="0 3 0"></a-entity>
```

**Spot Light** (cone-shaped beam):

```html
<a-entity light="type: spot; angle: 45; intensity: 1.5" position="0 5 0" rotation="-90 0 0"></a-entity>
```

### 5. Materials and Textures

**Standard Material**:

```html
<a-sphere
  material="color: #FF0000; metalness: 0.5; roughness: 0.3"
  position="0 1 -3">
</a-sphere>
```

**Textured Material**:

```html
<a-assets>
  <img id="woodTexture" src="wood.jpg">
</a-assets>

<a-box material="src: #woodTexture" position="0 1 -3"></a-box>
```

**Flat Shading** (no lighting):

```html
<a-plane material="shader: flat; color: #4CC3D9"></a-plane>
```

### 6. Animations

**Property Animation**:

```html
<a-box
  position="0 1 -3"
  animation="property: rotation; to: 0 360 0; loop: true; dur: 5000">
</a-box>
```

**Multiple Animations** (use `animation__*` naming):

```html
<a-sphere
  position="0 1 -3"
  animation__position="property: position; to: 0 3 -3; dir: alternate; loop: true; dur: 2000"
  animation__rotation="property: rotation; to: 360 360 0; loop: true; dur: 4000"
  animation__scale="property: scale; to: 1.5 1.5 1.5; dir: alternate; loop: true; dur: 1000">
</a-sphere>
```

**Event-Based Animation**:

```html
<a-box
  color="blue"
  animation__mouseenter="property: scale; to: 1.2 1.2 1.2; startEvents: mouseenter"
  animation__mouseleave="property: scale; to: 1 1 1; startEvents: mouseleave"
  animation__click="property: rotation; from: 0 0 0; to: 0 360 0; startEvents: click">
</a-box>
```

### 7. Assets Management

Preload assets for better performance:

```html
<a-scene>
  <a-assets>
    <!-- Images -->
    <img id="texture1" src="texture.jpg">
    <img id="skyTexture" src="sky.jpg">

    <!-- Videos -->
    <video id="video360" src="360video.mp4" autoplay loop></video>

    <!-- Audio -->
    <audio id="bgMusic" src="music.mp3" preload="auto"></audio>

    <!-- Models -->
    <a-asset-item id="tree" src="tree.gltf"></a-asset-item>

    <!-- Mixins (reusable component sets) -->
    <a-mixin id="redMaterial" material="color: red; metalness: 0.7"></a-mixin>
  </a-assets>

  <!-- Use assets -->
  <a-entity gltf-model="#tree" position="2 0 -5"></a-entity>
  <a-sphere mixin="redMaterial" position="0 1 -3"></a-sphere>
  <a-sky src="#skyTexture"></a-sky>
</a-scene>
```

### 8. Custom Components

Register custom components to encapsulate logic:

```javascript
AFRAME.registerComponent('rotate-on-click', {
  // Component schema (configuration)
  schema: {
    speed: {type: 'number', default: 1}
  },

  // Lifecycle: called once when component attached
  init: function() {
    this.el.addEventListener('click', () => {
      this.rotating = !this.rotating;
    });
  },

  // Lifecycle: called every frame
  tick: function(time, timeDelta) {
    if (this.rotating) {
      var rotation = this.el.getAttribute('rotation');
      rotation.y += this.data.speed;
      this.el.setAttribute('rotation', rotation);
    }
  }
});
```

```html
<a-box rotate-on-click="speed: 2" position="0 1 -3"></a-box>
```

## Patterns & Reference

The full common patterns, integration recipes, performance guidance, and pitfall fixes for this library live in references/patterns.md. Read the section relevant to the current task instead of the whole file; each section is self-contained with runnable examples.

## Resources

- scripts/ - automation and generator utilities for this library.
- references/ - API reference and pattern docs (see patterns.md for the moved patterns sections).
- assets/ - starter templates and examples.