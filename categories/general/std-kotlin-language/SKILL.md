---
name: std-kotlin-language
description: "Skill: std-kotlin-language"
license: MIT
tags: [general]
---

# Kotlin Language Patterns

## **Priority: P0 (CRITICAL)**


## Implementation Guidelines

- **Immutability**: Use `val` by default. Only use `var` if mutation required locally.
- **Null Safety**: Use `?` for nullable types. Use safe call `?.` and Elvis `?:` over `!!`.
- **Expressions**: Prefer expression bodies `fun foo() = ...` for one-liners. Use `if`/`try` as expressions.
- **Classes**: Use `data class` for DTOs. Use `sealed interface/class` for state hierarchies (e.g., `Success`, `Error`, `Loading`). Access members as computed property rather than function.
- **Extension Functions**: Prefer over utility classes (`StringUtil`). Keep private/internal if module-specific.
- **Named Arguments**: Use for clarity, especially with booleans or multiple same-type params.
- **String Templates**: Use `"$var"` over concatenation. Use `""` for multiline strings (SQL/JSON).

## Anti-Patterns

- **No !! Operator**: Never use in production; prefer safe calls or requireNotNull.
- **No Java-isms**: Use properties not get/set; prefer top-level functions over companion object statics.
- **No Lateinit Abuse**: Prefer nullable types or lazy delegates instead.
- **No Silenced Errors**: Never swallow exceptions without logging or handling.

## References

- Sealed Class, When Expression & Extension Examples