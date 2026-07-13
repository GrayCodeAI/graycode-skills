---
name: minimax-flutter-dev
description: "Skill: minimax-flutter-dev"
license: MIT
tags: [mobile]
Use when: building Flutter apps, implementing state management (Riverpod/Bloc), setting up GoRouter navigation, creating custom widgets, optimizing performance, writing widget tests, cross-platform development.
metadata: None
version: 1.0.0
category: mobile
sources: [{'flutter-expert by Jeff Smolinski (https': '//github.com/Jeffallan/claude-skills) — Flutter expert skill framework'}]
---

# Flutter Development Guide

A practical guide for building cross-platform applications with Flutter 3 and Dart. Focuses on proven patterns, state management, and performance optimization.

## Quick Reference

### Widget Patterns

| Purpose | Component |
|---------|-----------|
| State management (simple) | `StateProvider` + `ConsumerWidget` |
| State management (complex) | `NotifierProvider` / `Bloc` |
| Async data | `FutureProvider` / `AsyncNotifierProvider` |
| Real-time streams | `StreamProvider` |
| Navigation | `GoRouter` + `context.go/push` |
| Responsive layout | `LayoutBuilder` + breakpoints |
| List display | `ListView.builder` |
| Complex scrolling | `CustomScrollView` + Slivers |
| Hooks | `HookWidget` + `useState/useEffect` |
| Forms | `Form` + `TextFormField` + validation |

### Performance Patterns

| Purpose | Solution |
|---------|----------|
| Prevent rebuilds | `const` constructors |
| Selective updates | `ref.watch(provider.select(...))` |
| Isolate repaints | `RepaintBoundary` |
| Lazy lists | `ListView.builder` |
| Heavy computation | `compute()` isolate |
| Image caching | `cached_network_image` |

## Core Principles

### Widget Optimization
- Use `const` constructors wherever possible
- Extract static widgets to separate const classes
- Use `Key` for list items (ValueKey, ObjectKey)
- Prefer `ConsumerWidget` over `StatefulWidget` for state

### State Management
- Riverpod for dependency injection and simple state
- Bloc/Cubit for event-driven workflows and complex logic
- Never mutate state directly (create new instances)
- Use `select()` to minimize rebuilds

### Layout
- 8pt spacing increments (8, 16, 24, 32, 48)
- Responsive breakpoints: mobile (<650), tablet (650-1100), desktop (>1100)
- Support all screen sizes with flexible layouts
- Follow Material 3 / Cupertino design guidelines

### Performance
- Profile with DevTools before optimizing
- Target <16ms frame time for 60fps
- Use `RepaintBoundary` for complex animations
- Offload heavy work with `compute()`

## Checklist

### Widget Best Practices
- [ ] `const` constructors on all static widgets
- [ ] Proper `Key` on list items
- [ ] `ConsumerWidget` for state-dependent widgets
- [ ] No widget building inside `build()` method
- [ ] Extract reusable widgets to separate files

### State Management
- [ ] Immutable state objects
- [ ] `select()` for granular rebuilds
- [ ] Proper provider scoping
- [ ] Dispose controllers and subscriptions
- [ ] Handle loading/error states

### Navigation
- [ ] GoRouter with typed routes
- [ ] Auth guards via redirect
- [ ] Deep linking support
- [ ] State preservation across routes

### Performance
- [ ] Profile mode testing (`flutter run --profile`)
- [ ] <16ms frame rendering time
- [ ] No unnecessary rebuilds (DevTools check)
- [ ] Images cached and resized
- [ ] Heavy computation in isolates

### Testing
- [ ] Widget tests for UI components
- [ ] Unit tests for business logic
- [ ] Integration tests for user flows
- [ ] Bloc tests with `blocTest()`

## References

| Topic | Reference |
|-------|-----------|
| Widget patterns, const optimization, responsive layout | Widget Patterns |
| Riverpod providers, notifiers, async state | Riverpod State Management |
| Bloc, Cubit, event-driven state | Bloc State Management |
| GoRouter setup, routes, deep linking | GoRouter Navigation |
| Feature-based structure, dependencies | Project Structure |
| Profiling, const optimization, DevTools | Performance Optimization |
| Widget tests, integration tests, mocking | Testing Strategies |
| iOS/Android/Web specific implementations | Platform Integration |
| Implicit/explicit animations, Hero, transitions | Animations |
| Dio, interceptors, error handling, caching | Networking |
| Form validation, FormField, input formatters | Forms |
| i18n, flutter_localizations, intl | Localization |

---

Flutter, Dart, Material Design, and Cupertino are trademarks of Google LLC and Apple Inc. respectively. Riverpod, Bloc, and GoRouter are open-source packages by their respective maintainers.