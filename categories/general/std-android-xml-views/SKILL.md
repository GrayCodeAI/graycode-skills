---
name: std-android-xml-views
description: "Implement ViewBinding, RecyclerView, and XML layouts correctly on Android. Use when working with XML layouts, ViewBinding, or RecyclerView adapters in legacy Android projects."
license: MIT
tags: [general]
metadata: None
triggers: None
files: None
keywords: None
---

# Android XML Views Standards

## **Priority: P1**

## Implementation Guidelines

### ViewBinding

- **Standard**: Use ViewBinding for all XML layouts.
- **Synthetics**: `kotlin-android-extensions` Dead. Remove it.
- **KAPT**: Avoid DataBinding unless strictly necessary (impacts build speed).

### RecyclerView

- **Adapter**: Always inherit `ListAdapter` (wraps AsyncListDiffer).
- **Updates**: Provide proper `DiffUtil.ItemCallback`. NEVER call `notifyDataSetChanged()`.

### Layouts

- **ConstraintLayout**: Use for complex flat hierarchies.
- **Performance**: Avoid deep nesting (LinearLayout inside LinearLayout).

## Anti-Patterns

- **No findViewById**: Deprecated. Use ViewBinding for all XML layouts.
- **No kotlin-android-extensions**: Deprecated. Remove all `import kotlinx.android.synthetic.*`.

## References

- ViewBinding & Adapter