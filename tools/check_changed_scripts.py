#!/usr/bin/env python3
"""Ratchet quality and TLS safety for changed community-skill files.

The existing catalogue predates the current Ruff policy and contains legacy
violations. This checker prevents security debt from growing: every changed
script must be free of insecure TLS calls and basic syntax/name errors, and
changed skill documentation must not teach TLS verification bypasses. Full
style cleanup remains a separate, staged migration for the large corpus.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = re.compile(r"^categories/.+/scripts/.+\.py$")
DOC_PATH = re.compile(r"^categories/.+\.(md|mdx|txt)$")
INSECURE_TLS = re.compile(r"\bverify\s*=\s*False\b")


def changed_scripts(paths: list[str]) -> list[Path]:
    """Return existing community script paths from the supplied changed paths."""
    return [Path(path) for path in paths if SCRIPT_PATH.fullmatch(path) and Path(path).is_file()]


def changed_tls_docs(paths: list[str]) -> list[Path]:
    """Return changed category docs that can contain code examples."""
    return [Path(path) for path in paths if DOC_PATH.fullmatch(path) and Path(path).is_file()]


def find_insecure_tls(paths: list[Path]) -> list[str]:
    """Report every Requests call that disables certificate verification."""
    findings: list[str] = []
    for path in paths:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if INSECURE_TLS.search(line):
                findings.append(
                    f"{path}:{line_number}: do not disable TLS certificate verification"
                )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check changed community script quality and TLS safety"
    )
    parser.add_argument("paths", nargs="*", help="changed repository-relative paths")
    args = parser.parse_args()

    scripts = changed_scripts(args.paths)
    docs = changed_tls_docs(args.paths)
    if not scripts and not docs:
        print("✓ No changed community script or doc files to check")
        return 0

    tls_findings = find_insecure_tls([*scripts, *docs])
    if tls_findings:
        print("✗ Insecure TLS usage found:", file=sys.stderr)
        print("\n".join(tls_findings), file=sys.stderr)
        return 1

    if not scripts:
        print("✓ No changed community Python scripts to lint")
        return 0

    # Restrict the ratchet to correctness rules while legacy style debt is
    # migrated incrementally. These rules catch syntax and undefined names.
    command = [
        sys.executable,
        "-m",
        "ruff",
        "check",
        "--select",
        "E9,F63,F7,F82",
        *map(str, scripts),
    ]
    if subprocess.run(command, check=False).returncode != 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
