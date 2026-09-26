#!/usr/bin/env python3
"""License-compatibility gate for ingested third-party skills.

The repository is MIT-licensed, so copyleft (GPL/LGPL/AGPL family) content
copied into a skill directory would create a license-contamination problem.
This check fails when either

* a per-skill LICENSE file contains a copyleft license text, or
* a skill's SKILL.md frontmatter declares a copyleft ``license`` value,

encoding the policy documented in the root NOTICE. Skills that were reviewed
and are known to declare a copyleft value for a documented reason are listed
in ``tools/license_exceptions.txt``; an exception that no longer matches a
violation is an error too, so the list can only shrink.

Unlike the secret scan, this is strict by default: copyleft content under an
MIT repo is a clear, actionable defect rather than a likely false positive.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from frontmatter import parse_frontmatter  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = REPO_ROOT / "categories"
EXCEPTIONS_PATH = Path(__file__).resolve().parent / "license_exceptions.txt"

# Copyleft signatures that must not appear in a skill's LICENSE. CC-BY-SA is a
# prose share-alike and is allowed for documentation skills, so it is not listed.
COPYLEFT_PATTERNS = [
    ("GPL", re.compile(r"GNU GENERAL PUBLIC LICENSE", re.IGNORECASE)),
    ("LGPL", re.compile(r"GNU LESSER GENERAL PUBLIC LICENSE", re.IGNORECASE)),
    ("AGPL", re.compile(r"GNU AFFERO GENERAL PUBLIC LICENSE", re.IGNORECASE)),
]

# Copyleft identifiers in a frontmatter `license` value: SPDX ids such as
# GPL-3.0, AGPL-3.0-only, LGPL-2.1, spellings like "GPLv3", and full names.
FRONTMATTER_COPYLEFT = re.compile(
    r"(?<![A-Za-z])(?:A|L)?GPL(?:v\d)?(?![A-Za-z])"
    r"|GNU\s+(?:AFFERO\s+|LESSER\s+)?GENERAL\s+PUBLIC\s+LICEN[CS]E",
    re.IGNORECASE,
)


def iter_license_files():
    if not CATEGORIES_DIR.exists():
        return
    for path in sorted(CATEGORIES_DIR.rglob("LICENSE")):
        if path.is_file():
            yield path


def iter_skill_manifests():
    if not CATEGORIES_DIR.exists():
        return
    for path in sorted(CATEGORIES_DIR.glob("*/*/SKILL.md")):
        if path.is_file():
            yield path


def frontmatter_license(skill_md: Path) -> str | None:
    """Return the frontmatter `license` value as text, or None."""
    try:
        frontmatter, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return None
    if not frontmatter:
        return None
    value = frontmatter.get("license")
    return value if isinstance(value, str) else None


def is_copyleft_license_value(value: str) -> bool:
    return bool(FRONTMATTER_COPYLEFT.search(value))


def load_exceptions(path: Path | None = None) -> set[str]:
    """Load reviewed exceptions: one repo-relative skill directory per line."""
    path = EXCEPTIONS_PATH if path is None else path
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return set()
    entries = set()
    for line in lines:
        entry = line.split("#", 1)[0].strip()
        if entry:
            entries.add(entry)
    return entries


def find_violations() -> tuple[list[tuple[str, str]], int]:
    """Return ([(skill_or_file, reason)], number_of_sources_checked)."""
    violations: list[tuple[str, str]] = []
    checked = 0
    for lic in iter_license_files():
        checked += 1
        try:
            text = lic.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, rx in COPYLEFT_PATTERNS:
            if rx.search(text):
                violations.append((str(lic.relative_to(REPO_ROOT)), f"LICENSE file is {name}"))
                break
    for skill_md in iter_skill_manifests():
        checked += 1
        value = frontmatter_license(skill_md)
        if value and is_copyleft_license_value(value):
            skill_dir = str(skill_md.parent.relative_to(REPO_ROOT))
            violations.append((skill_dir, f"frontmatter license: {value!r}"))
    return violations, checked


def main():
    parser = argparse.ArgumentParser(description="Check skill licenses for copyleft contamination")
    parser.add_argument(
        "--warn", action="store_true", help="report but do not fail (default: fail)"
    )
    args = parser.parse_args()

    violations, checked = find_violations()
    exceptions = load_exceptions()
    new = [(where, why) for where, why in violations if where not in exceptions]
    stale = sorted(exceptions - {where for where, _ in violations})

    if not new and not stale:
        print(
            f"✓ No unreviewed copyleft-licensed skills found ({checked} LICENSE files and "
            f"SKILL.md frontmatter checked; {len(exceptions)} reviewed exception(s))"
        )
        return

    mark = "⚠" if args.warn else "✗"
    if new:
        print(f"{mark} {len(new)} copyleft-licensed skill(s) under an MIT repo:")
        for where, why in new:
            print(f"  - {where}: {why}")
        print("  Copyleft (GPL/LGPL/AGPL) content must not be vendored — see NOTICE.")
    if stale:
        print(f"{mark} {len(stale)} stale entr(y/ies) in {EXCEPTIONS_PATH.name}; remove:")
        for where in stale:
            print(f"  - {where}")
    if not args.warn:
        sys.exit(1)


if __name__ == "__main__":
    main()
