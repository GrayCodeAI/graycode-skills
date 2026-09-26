# Changelog

All notable changes to graycode-skills are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Automated validation tooling for frontmatter, references, scripts, and content
- Registry generation from SKILL.md frontmatter
- CI/CD workflows for PR checks
- 14,015+ community skill packages across 27 categories

### Security
- `publish-registry.yml` no longer falls back to the literal `dev-fallback-key`
  when `SKILLS_ED25519_PRIVATE_KEY` / `SKILLS_SIGNING_KEY` are unconfigured. It
  previously published a `registry-signature.json` that looked authoritative but
  was forgeable by anyone who could read the workflow. `tools/sign_manifest.py`
  already exited non-zero without a key, so removing the fallback makes an
  unconfigured secret fail the release loudly instead of shipping a meaningless
  signature.

## [0.1.0] - 2026-05-26

### Changed
- Initial release with validation infrastructure

[Unreleased]: https://github.com/GrayCodeAI/graycode-skills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/GrayCodeAI/graycode-skills/releases/tag/v0.1.0
