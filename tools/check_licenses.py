#!/usr/bin/env python3
"""License-compatibility gate for ingested third-party skills.

The repository is MIT-licensed, so copyleft (GPL/LGPL family) content copied
into a skill directory would create a license-contamination problem. This check
scans every per-skill LICENSE file for copyleft signatures and fails when one is
found, encoding the policy documented in the root NOTICE.

Unlike the secret scan, this is strict by default: a GPL/LGPL LICENSE under an
MIT repo is a clear, actionable defect rather than a likely false positive.
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = REPO_ROOT / "categories"

# Copyleft signatures that must not appear in a skill's LICENSE. CC-BY-SA is a
# prose share-alike and is allowed for documentation skills, so it is not listed.
COPYLEFT_PATTERNS = [
    ("GPL", re.compile(r"GNU GENERAL PUBLIC LICENSE", re.IGNORECASE)),
    ("LGPL", re.compile(r"GNU LESSER GENERAL PUBLIC LICENSE", re.IGNORECASE)),
    ("AGPL", re.compile(r"GNU AFFERO GENERAL PUBLIC LICENSE", re.IGNORECASE)),
]


def iter_license_files():
    if not CATEGORIES_DIR.exists():
        return
    for path in sorted(CATEGORIES_DIR.rglob("LICENSE")):
        if path.is_file():
            yield path


def main():
    parser = argparse.ArgumentParser(description="Check skill licenses for copyleft contamination")
    parser.add_argument(
        "--warn", action="store_true", help="report but do not fail (default: fail)"
    )
    args = parser.parse_args()

    violations = []
    checked = 0
    for lic in iter_license_files():
        checked += 1
        try:
            text = lic.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, rx in COPYLEFT_PATTERNS:
            if rx.search(text):
                violations.append((lic.relative_to(REPO_ROOT), name))
                break

    if not violations:
        print(f"✓ No copyleft-licensed skills found ({checked} LICENSE files checked)")
        return

    print(
        f"{'⚠' if args.warn else '✗'} {len(violations)} copyleft-licensed "
        f"skill(s) under an MIT repo:"
    )
    for rel, name in violations:
        print(f"  - {rel}: {name}")
    print("  Copyleft (GPL/LGPL/AGPL) content must not be vendored — see NOTICE.")
    if not args.warn:
        sys.exit(1)


if __name__ == "__main__":
    main()
