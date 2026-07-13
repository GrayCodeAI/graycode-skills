---
name: std-ios-deployment
description: "Automate provisioning, signing, and deployment with Fastlane. Use when provisioning iOS apps, managing code signing, or automating deployments with Fastlane."
license: MIT
tags: [general]
metadata: None
triggers: None
keywords: None
---

# iOS Deployment

## **Priority: P1**

## Implementation Workflow

1. **Set up Match** — Use `fastlane match` for centralized certificate and profile management. Avoid manual signing.
2. **Configure build settings** — Set `PROVISIONING_PROFILE_SPECIFIER` explicitly if using manual/CI signing.
3. **Script Fastlane lanes** — Create `beta` (TestFlight) and `release` (App Store) lanes in your Fastfile.
4. **Automate versioning** — Use `increment_build_number` to auto-bump build numbers.
5. **Automate TestFlight uploads** — Trigger on every successful merge to staging.
6. **Set export compliance** — Automate in `Info.plist` or Fastlane to avoid metadata pauses.

See Fastlane and Match setup examples

## Anti-Patterns

- **No Manual CI Signing**: Use Match for automated certificate management
- **No Certificates in Repo**: Use private git repo for Match certificates
- **No Manual Versioning**: Use Fastlane `increment_build_number` for build numbers

## References

- Fastlane & Signing Setup