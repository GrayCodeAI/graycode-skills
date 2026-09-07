#!/usr/bin/env python3
"""Validate SKILL.md frontmatter against manifest-schema.toml.

Usage:
    python3 scripts/validate-skill-manifest.py path/to/SKILL.md [...]

Exits 0 if all manifests are valid, 1 otherwise.
Designed to be called from CI (lefthook, GitHub Actions).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).parent.parent

# ── Schema (hand-coded from manifest-schema.toml for zero-dep validation) ─────

# version and domain are agentskills.io v2.0 fields — optional but validated
# when present. Not in REQUIRED to avoid breaking existing v1.1 skills.
REQUIRED = {"name", "description", "author", "license", "tags"}

DOMAIN_ENUM = {
    "coding",
    "cybersecurity",
    "data-science",
    "devops",
    "documentation",
    "research",
    "testing",
    "other",
}

LICENSE_ENUM = {
    "MIT",
    "Apache-2.0",
    "GPL-3.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "CC0-1.0",
    "MPL-2.0",
}

PHASE_ENUM = {"localize", "repair", "validate", "review", "planning", "any"}

# Agent Skills spec (agentskills.io) enums
CATEGORY_ENUM = {
    "engineering",
    "ops",
    "testing",
    "security",
    "devtools",
    "workflow",
}

AGENT_ENUM = {
    "graycode",
    "claude-code",
    "codex",
    "cursor",
    "windsurf",
    "github-actions",
}

INVOKE_RE = re.compile(r"^[a-z0-9][a-z0-9-]*:[a-z0-9][a-z0-9-]*$")

MODEL_ENUM = {"haiku", "sonnet", "opus", "any"}

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,79}$")
VERSION_RE = re.compile(r"^\d+\.\d+(\.\d+)?$")


def parse_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str]:
    """Extract YAML frontmatter from a Markdown file.

    Returns (parsed_dict, error_message). On success error_message is empty.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None, "no YAML frontmatter (file must start with ---)"
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, "malformed frontmatter (no closing ---)"
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return None, f"YAML parse error: {e}"
    if not isinstance(data, dict):
        return None, "frontmatter must be a YAML mapping"
    return data, ""


def validate(data: dict[str, Any], path: Path) -> list[str]:
    """Return a list of validation error messages, or an empty list if valid."""
    errors: list[str] = []

    # Required fields
    for field in REQUIRED:
        if field not in data:
            errors.append(f"missing required field: {field!r}")

    name = data.get("name", "")
    if name and not NAME_RE.match(str(name)):
        errors.append(f"name {name!r} must match ^[a-z0-9][a-z0-9-]{{2,79}}$")

    desc = data.get("description", "")
    if desc and len(str(desc)) > 280:
        errors.append(f"description exceeds 280 chars ({len(str(desc))})")

    version = data.get("version", "")
    if version and not VERSION_RE.match(str(version)):
        errors.append(f"version {version!r} must match semver (e.g. '1.0' or '2.3.1')")

    domain = data.get("domain", "")
    if domain and domain not in DOMAIN_ENUM:
        errors.append(f"domain {domain!r} not in {sorted(DOMAIN_ENUM)}")

    license_ = data.get("license", "")
    if license_ and license_ not in LICENSE_ENUM:
        errors.append(f"license {license_!r} not in {sorted(LICENSE_ENUM)}")

    tags = data.get("tags", [])
    if not isinstance(tags, list):
        errors.append("tags must be a list")
    elif len(tags) < 1:
        errors.append("tags must have at least 1 item")
    elif len(tags) > 12:
        errors.append(f"tags must have at most 12 items, got {len(tags)}")

    phase = data.get("phase")
    if phase is not None and phase not in PHASE_ENUM:
        errors.append(f"phase {phase!r} not in {sorted(PHASE_ENUM)}")

    min_model = data.get("min_model")
    if min_model is not None and min_model not in MODEL_ENUM:
        errors.append(f"min_model {min_model!r} not in {sorted(MODEL_ENUM)}")

    ctx = data.get("context_tokens")
    if ctx is not None and (not isinstance(ctx, int) or ctx < 256 or ctx > 200_000):
        errors.append(f"context_tokens must be an integer in [256, 200000], got {ctx!r}")

    # ── Agent Skills spec (agentskills.io) validation ──────────────────────

    category = data.get("category")
    if category is not None and category not in CATEGORY_ENUM:
        errors.append(f"category {category!r} not in {sorted(CATEGORY_ENUM)}")

    auto_invoke = data.get("auto_invoke")
    if auto_invoke is not None and not isinstance(auto_invoke, bool):
        errors.append(f"auto_invoke must be a boolean, got {type(auto_invoke).__name__}")

    compatibility = data.get("compatibility")
    if compatibility is not None and len(str(compatibility)) > 200:
        errors.append(f"compatibility exceeds 200 chars ({len(str(compatibility))})")

    allowed_tools = data.get("allowed_tools")
    if allowed_tools is not None and not isinstance(allowed_tools, str):
        errors.append(f"allowed_tools must be a string, got {type(allowed_tools).__name__}")

    agents = data.get("agents")
    if agents is not None:
        if not isinstance(agents, list):
            errors.append("agents must be a list")
        else:
            for agent in agents:
                if agent not in AGENT_ENUM:
                    errors.append(f"agent {agent!r} not in {sorted(AGENT_ENUM)}")

    invoke = data.get("invoke")
    if invoke is not None and not INVOKE_RE.match(str(invoke)):
        errors.append(f"invoke {invoke!r} must match ^[a-z0-9][a-z0-9-]*:[a-z0-9][a-z0-9-]*$")

    for chain_field in ("chain_after", "chain_before", "chain_conflicts", "chain_enhances"):
        val = data.get(chain_field)
        if val is not None and not isinstance(val, list):
            errors.append(f"{chain_field} must be a list")

    return errors


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: validate-skill-manifest.py <SKILL.md> [...]", file=sys.stderr)
        return 1

    all_ok = True
    for arg in argv:
        path = Path(arg)
        if not path.exists():
            print(f"ERROR {path}: file not found")
            all_ok = False
            continue
        data, err = parse_frontmatter(path)
        if err:
            print(f"ERROR {path}: {err}")
            all_ok = False
            continue
        errors = validate(data, path)
        if errors:
            all_ok = False
            for e in errors:
                print(f"ERROR {path}: {e}")
        else:
            print(f"  OK  {path}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
