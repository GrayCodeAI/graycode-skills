#!/usr/bin/env python3
"""Check skills against the Agent Skills open standard (agentskills.io).

The specification allows only these top-level frontmatter fields: name,
description, license, compatibility, metadata (a string-to-string map) and
allowed-tools. `name` must be 1-64 lowercase letters, digits and single
hyphens, must not start or end with a hyphen, and must match the directory.
`description` must be 1-1024 characters and `compatibility` 1-500 characters.
These rules mirror the reference validator (`skills-ref validate`).

The corpus predates the standard: nearly every skill carries a top-level
`tags` list, so most skills are not strictly conformant. This tool therefore
has two modes:

* ``--all`` prints a per-rule summary for the whole corpus and exits 0. It
  measures the gap; it is not a gate.
* ``--strict PATH...`` checks the given skill or category directories and
  exits 1 on any violation. CI uses it for first-party skills, which must
  stay conformant.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from frontmatter import parse_frontmatter  # noqa: E402
from skill_discovery import iter_skills  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = REPO_ROOT / "categories"

ALLOWED_FIELDS = frozenset(
    {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
)
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500


def check_skill(skill_dir: Path) -> list[tuple[str, str]]:
    """Return [(rule_id, message)] for one skill directory."""
    skill_md = skill_dir / "SKILL.md"
    try:
        frontmatter, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as exc:
        return [("unreadable", f"cannot read SKILL.md: {exc}")]
    if frontmatter is None:
        return [("frontmatter", "SKILL.md has no YAML frontmatter mapping")]

    problems: list[tuple[str, str]] = []
    extra = sorted(str(key) for key in frontmatter if key not in ALLOWED_FIELDS)
    if extra:
        problems.append(("unexpected-field", f"non-spec top-level fields: {', '.join(extra)}"))

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name:
        problems.append(("name", "name must be a non-empty string"))
    else:
        if len(name) > MAX_NAME:
            problems.append(("name-length", f"name is {len(name)} chars (max {MAX_NAME})"))
        if not NAME_RE.match(name):
            problems.append(
                ("name-format", f"name {name!r} must be lowercase a-z/0-9 with single inner hyphens")
            )
        if name != skill_dir.name:
            problems.append(("name-directory", f"name {name!r} != directory {skill_dir.name!r}"))

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        problems.append(("description", "description must be a non-empty string"))
    elif len(description) > MAX_DESCRIPTION:
        problems.append(
            ("description-length", f"description is {len(description)} chars (max {MAX_DESCRIPTION})")
        )

    if "compatibility" in frontmatter:
        compatibility = frontmatter["compatibility"]
        if not isinstance(compatibility, str) or not 1 <= len(compatibility) <= MAX_COMPATIBILITY:
            problems.append(("compatibility", f"compatibility must be 1-{MAX_COMPATIBILITY} chars"))

    if "metadata" in frontmatter:
        metadata = frontmatter["metadata"]
        if not isinstance(metadata, dict) or not all(
            isinstance(k, str) and isinstance(v, str) for k, v in metadata.items()
        ):
            problems.append(("metadata", "metadata must map string keys to string values"))

    if "allowed-tools" in frontmatter and not isinstance(frontmatter["allowed-tools"], str):
        problems.append(("allowed-tools", "allowed-tools must be a space-separated string"))
    if "license" in frontmatter and not isinstance(frontmatter["license"], str):
        problems.append(("license", "license must be a string"))
    return problems


def expand(paths: list[Path]) -> list[Path]:
    """Expand category directories into their skill directories."""
    skills: list[Path] = []
    for path in paths:
        if (path / "SKILL.md").is_file():
            skills.append(path)
        elif path.is_dir():
            skills.extend(p for p in sorted(path.iterdir()) if (p / "SKILL.md").is_file())
    return skills


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--all", action="store_true", help="summarize the whole corpus (exit 0)")
    mode.add_argument(
        "--strict", nargs="+", type=Path, metavar="PATH",
        help="skill or category directories that must conform (exit 1 on violations)",
    )
    args = parser.parse_args(argv)

    if args.all:
        total = 0
        conformant = 0
        rules: Counter[str] = Counter()
        for skill_dir in iter_skills(CATEGORIES_DIR):
            total += 1
            problems = check_skill(skill_dir)
            if not problems:
                conformant += 1
            rules.update({rule for rule, _ in problems})
        print(f"Agent Skills conformance: {conformant}/{total} skills conform")
        for rule, count in sorted(rules.items(), key=lambda item: (-item[1], item[0])):
            print(f"  {rule}: {count}")
        return 0

    skills = expand(args.strict)
    if not skills:
        print("✗ no skills found in the given paths")
        return 1
    failures = 0
    for skill_dir in skills:
        for rule, message in check_skill(skill_dir):
            failures += 1
            print(f"✗ {skill_dir}: [{rule}] {message}")
    if failures:
        return 1
    print(f"✓ {len(skills)} skill(s) conform to the Agent Skills specification")
    return 0


if __name__ == "__main__":
    sys.exit(main())
