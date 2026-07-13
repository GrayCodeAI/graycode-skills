---
name: std-quality-engineering-appium-mcp
description: "Drives iOS/Android mobile devices via Appium MCP. Use for verifying mobile bugs, E2E tests, and navigating real device clouds (LambdaTest/BrowserStack)."
license: MIT
tags: [general]
metadata: None
triggers: None
keywords: None
---

# 📱 Appium MCP (Mobile Automation)

## **Priority: P1 (HIGH)**

> [!IMPORTANT]
> **Tier 0 (Infrastructure)**: Session creation, device farm connectivity, basic OS interactions.
> **Tier 1 (Core Gestures)**: Taps, swipes, text input for native mobile elements.
> **Tier 2 (Flutter/Single-Canvas)**: Visual-first automation via screenshot + coordinate taps.

## 🔌 Activation

**Triggers**: `appium`, `mobile verify`, `android verify`, `ios verify`, `lambdatest`, `real device cloud`, `flutter widget tap`.

## 🛠 Core Workflow (Goal-Oriented)

| Step | Tool | Purpose |
| :--- | :--- | :--- |
| 1 | `appium_session_management` (`create`) | Open session. **Resiliency**: Retry with `noReset: true` on failure. |
| 2 | `appium_get_window_size` | Scale coordinates for high-density displays. |
| 3 | `appium_screenshot` | Capture visual state for **Semantic Reasoning**. |
| 4 | `appium_gesture` / `appium_set_value` | Interact. **Self-Healing**: Re-scan hierarchy if UUID stale. |
| 5 | `appium_session_management` (`delete`) | **MANDATORY Cleanup**. |

## 💡 AI-Driven Methodologies
- **Semantic Intent**: Find element in hierarchy (e.g., "Login button") instead of raw coordinates. Resilient to layout shifts.
- **Dynamic Handling**: Unexpected pop-up appears? Pause, reason about alert, dismiss, resume.
- **Visual Anchors**: Find stable "Anchor" (e.g., Header) and derive coordinates relative to it.

## 🚫 Anti-Patterns (Zero-Tolerance)

- **Hardcoded XPaths**: Use `accessibility id` or `uiautomator`. XPath flaky.
- **Implicit Wait-Only**: Never assume page loaded. Poll for "Source of Truth" element.
- **Ignoring QoS**: Audit CPU/Memory via `appium_mobile_performance_data`. Prevent lag/crashes.
- **Orphaned Sessions**: Teardown mandatory. Call `delete` in cleanup block.

## ✅ Evaluation Criteria

- **Cleanup Rate**: 100% session closure.
- **Visual Accuracy**: Coordinate-based taps land within 5% of target center.
- **Security**: No secrets in tool arguments or logs.

## 🔗 References

- **Visual Testing**: [common-mobile-visual-testing](SKILL.md) — Methodology for what to verify.
- **LambdaTest Setup**: lambdatest-cloud-setup — RDC configuration.
- **Tool Cheatsheet**: tool-cheatsheet — Fast copy-paste args.
- **Project Context**: project-context — Project-specific overlays/macros.