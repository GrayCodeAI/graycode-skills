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
- The registry is now signed with **Ed25519 only**. The HMAC-SHA256 scheme and
  `SKILLS_SIGNING_KEY` were removed from `tools/sign_manifest.py`, and the
  pinned public key is committed at `keys/registry-ed25519.pub`. The publish
  job fails when `SKILLS_ED25519_PRIVATE_KEY` is unset and verifies its own
  signature with the committed key before uploading. Registries published
  before this change carry a forgeable `hmac-sha256` signature; clients must
  not trust them. **Breaking:** `sign`/`verify` reject HMAC secrets.
- `publish-registry.yml` pins every action to a commit SHA, installs only
  hash-locked dependencies (`tools/requirements.lock`,
  `tools/requirements-sign.lock`), keeps the signing key in a separate job
  that installs nothing but the `cryptography` stack, and serialises runs
  with a `publish-registry` concurrency group.
- `verify --signature-file` checks a published `registry-signature.json`
  end to end (algorithm, target, SHA-256, signature). See `docs/REGISTRY.md`.

## [0.1.0] - 2026-05-26

### Changed
- Initial release with validation infrastructure

[Unreleased]: https://github.com/GrayCodeAI/graycode-skills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/GrayCodeAI/graycode-skills/releases/tag/v0.1.0
