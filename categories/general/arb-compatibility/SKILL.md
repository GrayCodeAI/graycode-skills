---
name: arb-compatibility
description: "Skill: arb-compatibility"
license: MIT
tags: [general]
---

# Book Rule Compatibility Matrix

This matrix compares the canonical `mini` rule sets and answers whether two books should be loaded together as active agent guidance.

## Legend

- ✅ Complementary: can be combined as equal active guidance without one book arbitrating the other.
- ❌ Conflicting: do not load together as equal active rule sets.
- 🔁 Overlap: choose one; they apply similar pressure, compete for the same decision layer, or one is a narrower substitute.
- `N/A`: same rule set.

## Matrix

| Book | APoSD | CleanA | CleanC | CodeC | DDIA | DDD | DDD Distilled | IDDD | PoEAA | Refactoring | Ref Guru | Release It | PragProg | WELC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APoSD | `N/A` | ✅ | 🔁 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| CleanA | ✅ | `N/A` | ✅ | ✅ | ✅ | ✅ | ✅ | 🔁 | 🔁 | ✅ | ✅ | ✅ | ✅ | ✅ |
| CleanC | 🔁 | ✅ | `N/A` | 🔁 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 🔁 | ✅ |
| CodeC | ✅ | ✅ | 🔁 | `N/A` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 🔁 | ✅ |
| DDIA | ✅ | ✅ | ✅ | ✅ | `N/A` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| DDD | ✅ | ✅ | ✅ | ✅ | ✅ | `N/A` | 🔁 | 🔁 | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| DDD Distilled | ✅ | ✅ | ✅ | ✅ | ✅ | 🔁 | `N/A` | 🔁 | 🔁 | ✅ | ✅ | ✅ | ✅ | ✅ |
| IDDD | ✅ | 🔁 | ✅ | ✅ | ✅ | 🔁 | 🔁 | `N/A` | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| PoEAA | ✅ | 🔁 | ✅ | ✅ | ✅ | ❌ | 🔁 | ❌ | `N/A` | ✅ | ✅ | ✅ | ✅ | ✅ |
| Refactoring | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | `N/A` | 🔁 | ✅ | ✅ | ✅ |
| Ref Guru | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 🔁 | `N/A` | ✅ | ✅ | ✅ |
| Release It | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | `N/A` | ✅ | ✅ |
| PragProg | ✅ | ✅ | 🔁 | 🔁 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | `N/A` | ✅ |
| WELC | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | `N/A` |

## Book Names

| Short | Book |
| --- | --- |
| APoSD | `a-philosophy-of-software-design` |
| CleanA | `clean-architecture` |
| CleanC | `clean-code` |
| CodeC | `code-complete` |
| DDIA | `designing-data-intensive-applications` |
| DDD | `domain-driven-design` |
| DDD Distilled | `domain-driven-design-distilled` |
| IDDD | `implementing-domain-driven-design` |
| PoEAA | `patterns-of-enterprise-application-architecture` |
| Refactoring | `refactoring` |
| Ref Guru | `refactoring-guru` |
| Release It | `release-it` |
| PragProg | `the-pragmatic-programmer` |
| WELC | `working-effectively-with-legacy-code` |

## Scores

- Conflict: how much active guidance can push opposite decisions.
- Overlap: how much guidance pushes the same decisions or covers the same failure modes.
- Complementarity: how much guidance works at different levels and strengthens the pair.

Scores are qualitative estimates grounded in cited `mini` evidence, with external context required for known high-risk pairs.

## Verdict Counts

- ✅ Complementary: 78
- ❌ Conflicting: 2
- 🔁 Overlap: 11