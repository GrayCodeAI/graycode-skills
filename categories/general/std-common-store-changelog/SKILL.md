---
name: std-common-store-changelog
description: "Generate user-facing release notes for the Apple App Store and Google Play Store by collecting git history, triaging user-impacting changes, and drafting store-compliant changelogs. Enforces charac..."
license: MIT
tags: [general]
metadata: None
triggers: None
keywords: None
---

# Store Changelog Standard

## **Priority: P1**


## Always-Apply Rules

- **Character limits**: App Store ≤ 4000 chars. Google Play ≤ 500 chars — validate before output.
- **Benefit language**: Write what user gains, not what code changed. "Faster checkout" not "refactored cart service".
- **Bullet-only format**: One sentence per bullet. No paragraphs. No headers inside notes.
- **Drop internal commits**: Exclude `chore`, `refactor`, `ci`, `build`, `test`, dependency bumps, and config changes — no user impact.
- **Deduplicate**: Merge commits touching same feature into one bullet.

## Workflow

1. **Collect**: Run `git log <last-tag>..HEAD --oneline` (or use provided commit list). If no tag exists, use full history.
2. **Triage**: Scan commits and touched files. Group by theme: `New`, `Improved`, `Fixed`. Drop internal-only.
3. **Draft — App Store**: Write 5–10 benefit-focused bullets. Optional `What's New in [Version]` header.
4. **Draft — Google Play**: Compress App Store draft to ≤ 500 chars. Prioritise top 3–5 user-facing changes.
5. **Validate**: Count characters per store. Check every bullet maps to real commit. Remove jargon.

See Commit-to-Bullet Examples for mapping patterns.

## Output Format

**App Store** (≤ 4000 chars):

```
What's New in Version X.Y
• [New] <user benefit — one sentence>
• [Improved] <user benefit — one sentence>
• [Fixed] <user benefit — one sentence>
```

**Google Play** (≤ 500 chars):

```
• <highest-impact change>
• <second change>
• <third change>
[Bug fixes and performance improvements.]
```

## Anti-Patterns

- **No jargon**: Never use `refactor`, `migrated`, `deprecated`, `PR`, `hotfix`, or internal ticket IDs.
- **No chore bullets**: `chore: upgrade Gradle` → drop entirely, never paraphrase as user feature.
- **No bundled bullets**: "Fixed login and improved search and added dark mode" → three separate bullets.
- **No character overrun**: Validate Play Store notes ≤ 500 chars before returning — truncate + rewrite if needed.

## References

- Commit-to-Bullet Examples — load when mapping specific commits to bullets