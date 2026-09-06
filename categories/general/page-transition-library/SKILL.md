---
name: page-transition-library
description: "Add smooth page transitions and SPA-like navigation to multi-page sites with lifecycle hooks, views, and container-based routing."
license: MIT
tags:
- page-transitions
- navigation
- spa
- animation
---

# Barba.js

Modern page transition library for creating fluid, smooth transitions between website pages. Barba.js makes multi-page websites feel like Single Page Applications (SPAs) by hijacking navigation and managing transitions without full page reloads.

## Overview

Barba.js is a lightweight (7kb minified and compressed) JavaScript library that intercepts navigation between pages, fetches new content via AJAX, and smoothly transitions between old and new containers. It reduces page load delays and HTTP requests while maintaining the benefits of traditional multi-page architecture.

**Core Features**:
- Smooth page transitions without full reloads
- Lifecycle hooks for precise control over transition phases
- View-based logic for page-specific behaviors
- Built-in routing with @barba/router plugin
- Extensible plugin system
- Small footprint and high performance
- Framework-agnostic (works with vanilla JS, GSAP, anime.js, etc.)

## Core Concepts

### 1. Wrapper, Container, and Namespace

Barba.js uses a specific DOM structure to manage transitions:

**HTML Structure**:
```html
<body data-barba="wrapper">
  <!-- Static elements (header, nav) stay outside container -->
  <header>
    <nav>
      <a href="/">Home</a>
      <a href="/about">About</a>
    </nav>
  </header>

  <!-- Dynamic content goes in container -->
  <main data-barba="container" data-barba-namespace="home">
    <!-- This content changes on navigation -->
    <h1>Home Page</h1>
    <p>Content that will transition out...</p>
  </main>

  <!-- Static footer outside container -->
  <footer>© 2025</footer>
</body>
```

**Three Key Elements**:

1. **Wrapper** (`data-barba="wrapper"`)
   - Outermost container
   - Everything inside wrapper but outside container stays persistent
   - Ideal for headers, navigation, footers that don't change

2. **Container** (`data-barba="container"`)
   - Dynamic content area that updates on navigation
   - Only this section gets replaced during transitions
   - Must exist on every page

3. **Namespace** (`data-barba-namespace="home"`)
   - Unique identifier for each page type
   - Used in transition rules and view logic
   - Examples: "home", "about", "product", "blog-post"

### 2. Transition Lifecycle

Barba.js follows a precise lifecycle for each navigation:

**Default Async Flow**:
1. User clicks link
2. Barba intercepts navigation
3. Prefetch next page (via AJAX)
4. Cache new content
5. **Leave hook** - Animate current page out
6. Wait for leave animation to complete
7. Remove old container, insert new container
8. **Enter hook** - Animate new page in
9. Wait for enter animation to complete
10. Update browser history

**Sync Flow** (with `sync: true`):
1. User clicks link
2. Barba intercepts navigation
3. Prefetch next page
4. Wait for new page to load
5. **Leave and Enter hooks run simultaneously** (crossfade effect)
6. Swap containers
7. Update browser history

### 3. Hooks

Barba provides 11 lifecycle hooks for controlling transitions:

**Hook Execution Order**:
```
Initial page load:
  beforeOnce → once → afterOnce

Every navigation:
  before → beforeLeave → leave → afterLeave →
  beforeEnter → enter → afterEnter → after
```

**Hook Types**:
- **Global hooks**: Run on every transition (`barba.hooks.before()`)
- **Transition hooks**: Defined within specific transition objects
- **View hooks**: Defined within view objects for page-specific logic

**Common Hook Use Cases**:
- `beforeLeave` - Reset scroll position, prepare animations
- `leave` - Animate current page out
- `afterLeave` - Clean up old page
- `beforeEnter` - Prepare new page (hide elements, set initial states)
- `enter` - Animate new page in
- `afterEnter` - Initialize page scripts, analytics tracking

### 4. Views

Views are page-specific logic containers that run based on namespace:

```javascript
barba.init({
  views: [{
    namespace: 'home',
    beforeEnter() {
      // Home-specific setup
      console.log('Entering home page');
    },
    afterEnter() {
      // Initialize home page features
      initHomeSlider();
    }
  }, {
    namespace: 'product',
    beforeEnter() {
      console.log('Entering product page');
    },
    afterEnter() {
      initProductGallery();
    }
  }]
});
```

## Patterns & Reference

The full common patterns, integration recipes, performance guidance, and pitfall fixes for this library live in references/patterns.md. Read the section relevant to the current task instead of the whole file; each section is self-contained with runnable examples.

## Resources

- scripts/ - automation and generator utilities for this library.
- references/ - API reference and pattern docs (see patterns.md for the moved patterns sections).
- assets/ - starter templates and examples.