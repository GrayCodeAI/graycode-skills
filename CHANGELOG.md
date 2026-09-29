# Changelog

All notable changes to graycode-skills are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

The next release is **0.2.0** (`VERSION`). `VERSION` had been reset to 0.0.1
below the published v0.1.0; do not tag anything lower than v0.2.0.

### Added
- Automated validation tooling for frontmatter, references, scripts, and content
- Registry generation from SKILL.md frontmatter
- CI/CD workflows for PR checks
- 14,014 community skill packages across 28 categories
- Ecosystem skills `rho-workflow`, `rover-verify` and `across-checkpoint` in a
  new `graycode` category, checked against the real CLIs and conformant with
  the Agent Skills standard (CI-gated).
- `tools/check_agentskills.py` (Agent Skills conformance report and strict
  gate) and `docs/AGENT_SKILLS.md`; skills may put tags in `metadata.tags`.
- `registry.json` entries now carry `license`, `author` and `source`
  (http(s) URLs only) from frontmatter.
- `./setup --host rho` installs into Rho's state directory (copies, because Rho
  skips symlinked skill directories).

### Changed
- `.claude-plugin/marketplace.json` publishes one Claude Code plugin per
  category (`graycode-skills-<category>`); the previous single plugin was
  rejected by `claude plugin validate`. **Breaking** for anyone referencing
  the old plugin.
- `manifest-schema.toml` is the only schema: the validator exits if it is
  missing or malformed, and reads the tag and invoke patterns from it.
- CI: every repository gate runs in the required `validate` job, the
  duplication gate can fail (ceiling 12%, jscpd pinned), and `BASE_REF`
  survives new branches and force-pushes.
- The Docker image's default command runs the full-corpus gate and passes;
  docker.yml smoke-tests it before pushing.
- CODEOWNERS names an existing account; issue templates, SECURITY.md,
  CODE_OF_CONDUCT, the OpenAPI reference and plugin manifests name Rho and
  the graycodeai.com contacts.

### Removed
- `scripts/validate-skill-manifest.py`, an unwired third validator whose
  schema contradicted the enforced one.
- The stray root `SKILL.md` (an unvalidated duplicate of a security skill).
- `.github/workflows/validate-skills.yml` (its steps moved into `ci.yml`).

### Fixed
- README and this changelog claimed 14,015 skills; the registry indexes 14,011.
- README Quick Start installed a skill that does not exist (`python-pandas`).
- `registry.json` `file_count` no longer depends on local `__pycache__`.
- `./setup` stopped after the first skill under `set -e`.
- The license gate now also rejects copyleft frontmatter `license` values
  (8 existing skills are listed for review in `tools/license_exceptions.txt`).

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
