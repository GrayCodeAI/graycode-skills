# graycode-skills status: 0.2.0 (unreleased; latest published release v0.1.0)

As of 2026-09-27:

- 14,014 skills across 28 categories. Validation zero-warning gate (`tools/validation_warning_budget.json`); schema in `manifest-schema.toml` `[enforced]`.
- Install with `rho skills install GrayCodeAI/graycode-skills <name>` (into Rho's state directory), or `./setup --host rho` from a checkout.
- `registry.json` is generated, not committed. CI publishes it with an Ed25519 signature on the `registry-latest` release (docs/REGISTRY.md).
- Claude Code marketplace: one plugin per category (`graycode-skills-<category>`).
- Ecosystem skills shipped: `rho-workflow`, `rover-verify`, `across-checkpoint` (`categories/graycode/`, Agent Skills-conformant).

Known gaps:

- Most legacy skills are not strictly Agent Skills-conformant (top-level `tags`, 3,297 non-conforming names); see docs/AGENT_SKILLS.md.
- 8 skills declare a copyleft `license` value and await review (`tools/license_exceptions.txt`).
- The duplication ceiling is 12% (measured 11.4%); the old 5% target was never enforced.
- `examples/` authoring samples.
