#!/usr/bin/env python3
"""Scan contributed skills for dangerous pipe-to-shell-interpreter commands.

A contribution registry merges third-party content; a skill that recommends
`curl <url> | bash` (or wget/PowerShell equivalents) hands a remote,
unreviewed script full execution on the user's machine the moment it's run.
This sweep flags that pattern across each skill's text files and reports the
offending file + line.

This corpus legitimately contains the pattern in two ways that are NOT
findings: (1) official installer one-liners for well-known tools (rustup,
uv, Docker rootless, Flux) that skills document as setup steps, and (2)
security/forensics skills that show the pattern as a worked example of what
an attacker's command looks like. See shell_command_allowlist.txt for (1)
and CONTEXT_SUPPRESSION_MARKERS below for (2).

It runs in warning mode by default (exit 0). Pass --strict to fail the
build on findings, once the corpus is known clean of unflagged instances.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_discovery import iter_skills

REPO_ROOT = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = REPO_ROOT / "categories"
ALLOWLIST_PATH = Path(__file__).resolve().parent / "shell_command_allowlist.txt"
PATH_ALLOWLIST_PATH = Path(__file__).resolve().parent / "shell_command_path_allowlist.txt"

# Extensions worth scanning inside a contributed skill directory. Mirrors
# check_secrets.py's SCAN_SUFFIXES — the pattern shows up in SKILL.md prose
# and reference docs at least as often as in shipped scripts.
SCAN_SUFFIXES = {
    ".md",
    ".py",
    ".sh",
    ".bash",
    ".js",
    ".ts",
    ".json",
    ".yaml",
    ".yml",
    ".txt",
}

# Files larger than this are skipped — same rationale as check_secrets.py.
MAX_SCAN_SIZE = 2 * 1024 * 1024  # 2MB

# Pipe-to-shell-interpreter patterns. Each entry: (name, compiled regex).
# Targets the specific "fetch, then hand the output straight to an
# interpreter with no inspection" shape, not every curl/wget mention.
SHELL_PIPE_PATTERNS = [
    (
        "curl piped to a shell interpreter",
        re.compile(r"\bcurl\b[^\n|]*\|\s*(?:sudo\s+)?(?:bash|sh|zsh)\b"),
    ),
    (
        "wget piped to a shell interpreter",
        re.compile(r"\bwget\b[^\n|]*\|\s*(?:sudo\s+)?(?:bash|sh|zsh)\b"),
    ),
    (
        "PowerShell download piped to Invoke-Expression",
        re.compile(
            r"\b(?:iwr|curl|wget|Invoke-WebRequest)\b[^\n|]*\|\s*(?:iex|Invoke-Expression)\b",
            re.IGNORECASE,
        ),
    ),
]

# Substrings that mark a match as documentation ABOUT the pattern (security/
# forensics teaching content showing what an attack looks like) rather than
# an instruction to actually run it. Mirrors check_secrets.py's
# PLACEHOLDER_MARKERS suppression approach.
CONTEXT_SUPPRESSION_MARKERS = (
    "indicator of",
    "indicator for",
    "detects",
    "detecting",
    "malicious",
    "e.g.",
    "example of",
    "for example",
    "such as",
    "attacker",
    "supply-chain attack",
    "supply chain attack",
    "never run",
    "don't run",
    "do not run",
    "avoid",
    "red flag",
    "warning sign",
    "anti-pattern",
    "always use a package manager",
)


def _load_lines(path: Path) -> tuple[str, ...]:
    if not path.exists():
        return ()
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        entries.append(line.lower())
    return tuple(entries)


ALLOWLISTED_DOMAINS = _load_lines(ALLOWLIST_PATH)
ALLOWLISTED_PATHS = _load_lines(PATH_ALLOWLIST_PATH)


def _is_path_suppressed(rel_path: str) -> bool:
    low = rel_path.lower()
    return any(low == p or low.startswith(p) for p in ALLOWLISTED_PATHS)


def _is_line_suppressed(line: str) -> bool:
    low = line.lower()
    return any(domain in low for domain in ALLOWLISTED_DOMAINS) or any(
        marker in low for marker in CONTEXT_SUPPRESSION_MARKERS
    )


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    """Return (line_no, pattern_name, snippet) findings for one file."""
    findings = []
    try:
        rel = path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        rel = path.as_posix()  # path outside REPO_ROOT (e.g. under test)
    if _is_path_suppressed(rel):
        return findings
    try:
        if path.stat().st_size > MAX_SCAN_SIZE:
            return findings
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings
    for i, line in enumerate(text.splitlines(), start=1):
        if _is_line_suppressed(line):
            continue
        for name, rx in SHELL_PIPE_PATTERNS:
            if rx.search(line):
                snippet = line.strip()
                if len(snippet) > 120:
                    snippet = snippet[:117] + "..."
                findings.append((i, name, snippet))
                break  # one finding per line is enough
    return findings


def iter_skill_files():
    for skill_dir in iter_skills(CATEGORIES_DIR):
        for f in sorted(skill_dir.rglob("*")):
            if f.is_file() and f.suffix.lower() in SCAN_SUFFIXES:
                yield f


def main():
    parser = argparse.ArgumentParser(
        description="Scan skills for dangerous pipe-to-shell-interpreter commands"
    )
    parser.add_argument(
        "--strict", action="store_true", help="exit non-zero when findings remain"
    )
    args = parser.parse_args()

    total = 0
    for f in iter_skill_files():
        for line_no, name, snippet in scan_file(f):
            rel = f.relative_to(REPO_ROOT)
            print(f"  ⚠ {rel}:{line_no}: {name}: {snippet}")
            total += 1

    if total == 0:
        print("✓ No unallowlisted pipe-to-shell commands detected")
        return

    print(f"\n{'✗' if args.strict else '⚠'} {total} pipe-to-shell command(s) found.")
    print(
        "  If this is a legitimate installer, add its domain to "
        "tools/shell_command_allowlist.txt. If this is a security/forensics "
        "reference showing the pattern as a worked example, add the file to "
        "tools/shell_command_path_allowlist.txt."
    )
    if args.strict:
        sys.exit(1)
    print("  (warning mode — pass --strict to fail CI)")


if __name__ == "__main__":
    main()
