#!/usr/bin/env python3
"""Scan contributed skills for hardcoded credentials.

A contribution registry merges third-party content; a leaked key in a merged
skill is a realistic incident. This sweep flags high-confidence credential
signatures across each skill's text files and reports the offending file + line.

It runs in warning mode by default (exit 0) so it can be introduced without
breaking CI on the security/malware-analysis skills that legitimately contain
token-shaped example strings. Pass --strict to fail the build on findings, and
ratchet to that once the corpus is known clean.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_discovery import iter_skills

REPO_ROOT = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = REPO_ROOT / "categories"

# Extensions worth scanning inside a contributed skill directory.
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
    ".env",
    ".txt",
}

# Files larger than this are skipped (with a warning): credential leaks live
# in source/config files, not multi-megabyte bulk content, and scanning them
# dominates runtime over a ~12k-skill corpus.
MAX_SCAN_SIZE = 2 * 1024 * 1024  # 2MB

# High-confidence credential signatures. Each entry: (name, compiled regex).
# Patterns target real key shapes (provider prefixes, AWS access keys, PEM
# private-key headers, explicit bearer tokens) rather than generic high-entropy
# strings, to keep the false-positive rate low.
# Patterns with a fixed, unambiguous key shape (provider prefixes, PEM
# headers). Clearly labelled teaching examples are suppressed below; real
# credentials must never be accompanied by an example marker.
STRUCTURAL_SECRET_PATTERNS = [
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("OpenAI/Stripe-style secret key", re.compile(r"\bsk-[A-Za-z0-9]{32,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    (
        "Private key block",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
    ),
    ("Explicit bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{20,}\b")),
]

# Patterns matched by shape alone (any quoted string assigned to a
# key/secret/token/password-looking variable name), which do legitimately
# collide with placeholder/example values in documentation. Placeholder
# suppression only applies to these.
GENERIC_SECRET_PATTERNS = [
    (
        "Generic assigned api key",
        re.compile(
            r"""(?i)\b(?:api[_-]?key|secret|password|token)\b\s*[:=]\s*['"][A-Za-z0-9._\-]{16,}['"]"""
        ),
    ),
]

SECRET_PATTERNS = STRUCTURAL_SECRET_PATTERNS + GENERIC_SECRET_PATTERNS

# Substrings that mark a match as an obvious placeholder/example, not a real
# leak. Structural matches are also suppressed when the line explicitly
# labels the value as a fake/example, which is common in security training.
PLACEHOLDER_MARKERS = (
    "example",
    "placeholder",
    "your-",
    "your_",
    "xxxx",
    "...",
    "<",
    "redacted",
    "dummy",
    "sample",
    "sk-test",
    "sk_test",
    "changeme",
    "fake",
    "exposedkey",
    "hardcoded",
    "never do this",
    "bad:",
    "expired",
    "invalid",
    "super-secret",
    "supersecret",
    "valid-chat-token",
    "initial-password",
    "cracked_secret",
    "signature",
    "eyjh",
    "eyjg",
    "eyjhb",
    "pem format",
    "1234567890abcdef",
    "abcdef1234567890",
    "abc123xyz",
    "replace",
    "env[",
    "getenv",
    "os.environ",
    "${",
    "{{",
)


def _looks_placeholder(line: str) -> bool:
    low = line.lower()
    return any(m in low for m in PLACEHOLDER_MARKERS)


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    """Return (line_no, pattern_name, snippet) findings for one file."""
    findings = []
    try:
        if path.stat().st_size > MAX_SCAN_SIZE:
            return findings
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings
    for i, line in enumerate(text.splitlines(), start=1):
        is_placeholder = _looks_placeholder(line)
        for name, rx in STRUCTURAL_SECRET_PATTERNS:
            if rx.search(line):
                if is_placeholder:
                    continue
                snippet = line.strip()
                if len(snippet) > 120:
                    snippet = snippet[:117] + "..."
                findings.append((i, name, snippet))
                break  # one finding per line is enough
        else:
            if is_placeholder:
                continue
            for name, rx in GENERIC_SECRET_PATTERNS:
                if rx.search(line):
                    snippet = line.strip()
                    if len(snippet) > 120:
                        snippet = snippet[:117] + "..."
                    findings.append((i, name, snippet))
                    break
    return findings


def iter_skill_files():
    for skill_dir in iter_skills(CATEGORIES_DIR):
        for f in sorted(skill_dir.rglob("*")):
            if f.is_file() and f.suffix.lower() in SCAN_SUFFIXES:
                yield f


def main():
    parser = argparse.ArgumentParser(description="Scan skills for hardcoded secrets")
    parser.add_argument(
        "--strict", action="store_true", help="exit non-zero when secrets are found"
    )
    args = parser.parse_args()

    total = 0
    for f in iter_skill_files():
        for line_no, name, snippet in scan_file(f):
            rel = f.relative_to(REPO_ROOT)
            print(f"  ⚠ {rel}:{line_no}: possible {name}: {snippet}")
            total += 1

    if total == 0:
        print("✓ No hardcoded secrets detected")
        return

    print(f"\n{'✗' if args.strict else '⚠'} {total} possible secret(s) found.")
    print("  Secrets must come from environment variables, never hardcoded.")
    if args.strict:
        sys.exit(1)
    print("  (warning mode — pass --strict to fail CI)")


if __name__ == "__main__":
    main()
