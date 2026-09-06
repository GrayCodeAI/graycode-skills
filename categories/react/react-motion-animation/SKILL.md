---
name: react-motion-animation
description: "Add polished enter/exit, scroll, hover, and tap animations to React UIs with motion components, variants, springs, and layout transitions."
license: MIT
tags:
- react
- animation
- motion
- scroll
---

# Motion

Motion is the modern animation library for React (`motion/react`) and the framework-agnostic Web Animations API (`motion` / Motion One). This skill covers the React API, which is the standard for animated UIs.

## Setup

```bash
npm install motion
```

Import from `motion/react`:

```tsx
import { motion } from "motion/react"
```

## Core building blocks

**The `motion` component** turns any DOM element or component into an animatable one:

```tsx
<motion.div animate={{ x: 100 }} />
```

- `animate` — target values.
- `initial` — starting values (or `false` to inherit parent variant).
- `transition` — timing and easing for the animation.
- `whileHover`, `whileTap`, `whileFocus`, `whileInView`, `whileDrag` — gesture/scroll triggers.

**Style values** can be plain numbers (px) or strings; polygons for radii and transforms animate with keyframes/springs:

```tsx
<motion.div
  initial={{ opacity: 0, scale: 0.9 }}
  animate={{ opacity: 1, scale: 1 }}
  transition={{ duration: 0.4, ease: "easeOut" }}
/>
```

## The `animate` function (non-React)

Use `animate()` imperatively for one-off or Web-Animations-API work:

```tsx
import { animate } from "motion"
await animate("#target", { opacity: 1 })
animate("#box", { x: 100, rotate: 45 }, { duration: 0.5 })
```

## Transitions and springs

Common transition configs:
- `duration` (seconds) + `ease` (`"easeIn"`, `"easeOut"`, `"easeInOut"`, `"linear"`, a cubic bezier `[0.2, 0.8, 0.2, 1]`, an easing function).
- `spring`: `{ type: "spring", stiffness: 100, damping: 10 }` (or `type: "spring", bounce: 0.25`).
- `delay`, `repeat`, `repeatType`.
- `times` — distribute keyframes over the timeline.

```tsx
transition={{ type: "spring", stiffness: 260, damping: 20 }}
```

## AnimatePresence for enter/exit

Wrap conditional/keys in `<AnimatePresence>` to animate components being removed (exit):

```tsx
import { AnimatePresence, motion } from "motion/react"

{isOpen && (
  <AnimatePresence>
    <motion.div
      key="modal"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
    />
  </AnimatePresence>
)}
```

Use `mode="wait"` or `mode="sync"` to control timing of parallel leave/enter.

## Scroll-driven animation

Anchor animation to scroll position with `useScroll` + transforms:

```tsx
import { motion, useScroll, useSpring, useTransform } from "framer-motion"

function Hero() {
  const { scrollYProgress } = useScroll()
  const y = useTransform(scrollYProgress, [0, 1], [0, -200])
  return <motion.div style={{ y }} />
}
```

- `useScroll()` — observes page/element scroll progress (`0..1`), configurable `container`, `target`, `offset`.
- `useTransform(value, [inputRange], [outputRange])` — map a MotionValue to derived values.
- `useSpring(value, { stiffness, damping })` — make a MotionValue spring-smooth.

For scroll reveals, `whileInView` triggers when the element enters the viewport:

```tsx
<motion.div initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true, amount: 0.3 }} />
```

## Variants

Groups of named states (`visible`, `hidden`) that cascade to children with stagger:

```tsx
const container = {
  hidden: { opacity: 0, staggerChildren: 0.1 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1 } },
}
const item = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1 },
}

<motion.ul variants={container} initial="hidden" animate="visible">
  {items.map(i => <motion.li key={i} variants={item} />)}
</motion.ul>
```

## Layout animations

Animate layout changes when props/keys change:

```tsx
<motion.div layout transition={{ type: "spring", stiffness: 400, damping: 30 }} />
```

`layout` animates a component to any new position/size when it re-renders. Use `layoutId` + `<AnimatePresence>` to "morph" elements across the tree (shared layout transitions, e.g. exiting a card into a full-screen view).

## Keyframes and repeating

Pass arrays to cycle through values; add `repeat`:

```tsx
<motion.div animate={{ x: [0, 100, 0], rotate: [0, 360, 0] }} transition={{ duration: 2, repeat: Infinity }} />
```

## Gesture/best practices

- Use `whileHover`/`whileTap` for micro-interactions on buttons/cards (scale, shadow) — keeps UI feeling alive without heavy JS.
- Keep `transition.ease` deliberate; avoid over-animating every element (performance and taste).
- **Reduced motion:** respect `prefers-reduced-motion`. Check via `useReducedMotion` hook or a CSS media query and skip/harden non-essential animations.
- Animate transform and opacity for GPU-friendly performance (avoid animating `width/height/top/left` unless necessary).
- Use `MotionValue`s (`useMotionValue`) + `style={{ x }}`, and `motionValue.get()`/`.on("change")` only when needed; prefer declarative `animate` when possible.

## Anti-patterns

- Never animate elements the browser can't paint at 60fps (width/heights in loops, huge lists).
- Avoid nested full-page scroll listeners; rely on `useScroll` offset/progress instead of `window.addEventListener("scroll")` in event time.
- Respect `prefers-reduced-motion` for every scroll/animation effect.

## See also

- Enter/exit modal, accordion, and shared-layout transitions.
- Pair with Lenis for smooth scroll; Motion animations drive the reveal, Lenis drives the scroll.
- For 3D/motion composition, keep Motion for UI affordances and reserve WebGL (Three/R3F) for heavy visuals.