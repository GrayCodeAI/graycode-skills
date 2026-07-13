---
name: std-android-state
description: "Configure ViewModel state emission with StateFlow, sealed UiState classes, and lifecycle-safe collection in Android. Use when working with ViewModels, UiState patterns, or exposing state to Compose..."
license: MIT
tags: [general]
metadata: None
triggers: None
files: None
keywords: None
---

# Android State Management

## **Priority: P0**

## 1. Structure ViewModel

- Expose ONE `StateFlow<UiState>` via `.asStateFlow()`.
- Use `viewModelScope` for all coroutines.
- Trigger initial load in `init` block.

See templates for ViewModel and UiState examples.

## 2. Define UI State (LCE Pattern)

- Use sealed interface with Loading, Content, Error variants.
- Mark data classes `@Immutable`.

See templates for sealed UiState pattern.

## 3. Collect State Lifecycle-Safely

- Use `collectAsStateWithLifecycle()` in Compose.
- Use `SharingStarted.WhileSubscribed(5000)` for shared resources.

## Anti-Patterns

- **No LiveData for New Code**: Use StateFlow — lifecycle-safe and Compose-compatible.
- **No Public MutableStateFlow**: Expose only `.asStateFlow()` to consumers.
- **No Context in ViewModel**: Leaks Activity. Use Application context if truly needed.

## Verification

- [ ] Each ViewModel exposes exactly one `StateFlow<UiState>`.
- [ ] UiState is a sealed interface with Loading, Content, Error variants.
- [ ] UI collects with `collectAsStateWithLifecycle()`.
- [ ] `./gradlew test` passes for ViewModel tests.

## References

- Templates