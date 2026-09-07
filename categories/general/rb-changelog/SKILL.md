---
name: rb-changelog
description: "Maintain a project changelog with structured entries for each release."
license: MIT
tags: [general]
---

## Overview

Create and maintain a project changelog that records all significant changes in a structured format. Use this skill when:
- Adding a new feature or fixing a bug that should be documented
- Preparing for a release
- Reviewing what has changed since the last version

## Changelog Format

Use Keep a Changelog format with structured entries:

```markdown
## [1.2.0] - 2025-06-15

### Added
- New CLI command for database migrations (`graycode db migrate`) (#245)
- Support for TypeScript 5.4 in IDE linting

### Fixed
- Crash when parsing malformed JSON in `.graycoderc` config file (#243)
- Memory leak in long-running agent sessions

### Changed
- Default log level changed from `INFO` to `WARN` for production
```

## Verification

- [ ] Changelog updated for the current version
- [ ] Each entry has a reference number (issue, PR, commit)
- [ ] Categorized as Added/Fixed/Changed/Removed

