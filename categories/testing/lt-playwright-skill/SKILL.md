---
name: lt-playwright-skill
description: 'Skill: lt-playwright-skill'
license: MIT
tags:
- testing
tests, mock APIs, or do visual regression. Triggers on: Playwright",
languages: None
category: e2e-testing
metadata: None
author: TestMu AI
version: 1.0
---

## Reference Files

| File | When to read |
|------|-------------|
| reference/cloud-integration.md | Cloud execution, 3 integration patterns, parallel browsers |
| reference/page-object-model.md | POM architecture, base page, fixtures, full examples |
| reference/mobile-testing.md | Android + iOS real device testing |
| reference/debugging-flaky.md | Flaky test checklist, common fixes |
| reference/api-mocking-visual.md | API mocking + visual regression patterns |
| reference/python-patterns.md | Python-specific: pytest-playwright, sync/async |
| reference/java-patterns.md | Java-specific: Maven, JUnit, Gradle |
| reference/csharp-patterns.md | C#-specific: NUnit, MSTest, .NET config |
| shared/testmu-cloud-reference.md | Full device catalog, capabilities, geo-location |

## Advanced Playbook

For production-grade patterns, see `reference/playbook.md`:

| Section | What's Inside |
|---------|--------------|
| §1 Production Config | Multi-project, reporters, retries, webServer |
| §2 Auth Fixture Reuse | storageState, multi-role fixtures |
| §3 Page Object Model | BasePage, LoginPage with fluent API |
| §4 Network Interception | Mock, modify, HAR replay, block resources |
| §5 Visual Regression | Screenshot comparison, masks, thresholds |
| §6 File Upload/Download | fileChooser, setInputFiles, download events |
| §7 Multi-Tab & Dialogs | Popup handling, alert/confirm/prompt |
| §8 Geolocation & Emulation | Location, timezone, locale, color scheme |
| §9 Custom Fixtures | DB seeding, API context, auto-teardown |
| §10 API Testing | Request context, end-to-end API+UI |
| §11 Accessibility | axe-core integration, WCAG audits |
| §12 Sharding | CI matrix sharding, report merging |
| §13 CI/CD | GitHub Actions with artifacts |
| §14 Debugging Toolkit | Debug, UI mode, trace viewer, codegen |
| §15 Debugging Table | 10 common problems with fixes |
| §16 Best Practices | 17-item production checklist |
