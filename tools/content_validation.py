#!/usr/bin/env python3
"""Content/body validation for starling SKILL.md files.

Checks that the markdown body after frontmatter contains required sections
and follows expected formatting conventions.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Add tools directory to path for shared imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from frontmatter import parse_frontmatter  # noqa: E402

# --- Constants ---

REQUIRED_SECTIONS = {"overview", "instructions"}
RECOMMENDED_SECTIONS = {"when to use", "references"}

# Display names for sections (avoids .title() capitalizing short words like "to")
_SECTION_DISPLAY: dict[str, str] = {
    "overview": "Overview",
    "instructions": "Instructions",
    "when to use": "When to Use",
    "references": "References",
}


def _section_display(name: str) -> str:
    """Return a nicely formatted display name for a section heading."""
    return _SECTION_DISPLAY.get(name, name.title())


VALID_LICENSES = {"MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "CC-BY-4.0", "Unlicense"}
MIN_BODY_LENGTH = 50  # characters of real content (after stripping whitespace/comments)


# --- Prompt Injection Detection ---

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"disregard\s+(all\s+)?previous\s+instructions",
    r"you\s+are\s+now\s+(a|an)\s+",
    r"system\s*prompt\s*:",
    r"new\s+instructions?\s*:",
    r"override\s+(all\s+)?instructions",
    r"forget\s+(all\s+)?(your\s+)?instructions",
    r"act\s+as\s+if\s+you\s+(are|were)",
    r"pretend\s+you\s+(are|were)\s+",
    r"from\s+now\s+on\s+you\s+(are|will)\s+",
    r"\[INST\]",
    r"\[/INST\]",
    r"<\|im_start\|>",
    r"<\|im_end\|>",
    r"###\s*system\s*",
    r"ADMIN\s+OVERRIDE",
    r"jailbreak",
]

_injection_re = re.compile("|".join(PROMPT_INJECTION_PATTERNS), re.IGNORECASE | re.MULTILINE)


def check_prompt_injection(content: str, result: BodyValidationResult) -> None:
    """Scan skill content for common prompt injection patterns.

    Flags matches as warnings (not errors) for human review, since some
    patterns may appear legitimately in skill instructions.
    """
    unique_patterns: set[str] = set()
    for m in _injection_re.finditer(content):
        matched_text = m.group(0).strip()
        unique_patterns.add(matched_text)
    for pattern in sorted(unique_patterns):
        result.warn(
            f"Possible prompt injection pattern detected: '{pattern}'. "
            "Please review this content manually."
        )


class BodyValidationResult:
    """Result of validating the body/content of a SKILL.md file."""

    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.errors: list[str] = []
        self.warnings: list[str] = []

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def _extract_headings(body: str) -> list[str]:
    """Return a list of heading text (without # prefixes) from markdown body."""
    headings: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            # Strip leading # and whitespace
            heading = re.sub(r"^#+\s*", "", stripped).strip()
            if heading:
                headings.append(heading)
    return headings


def _strip_comments_and_whitespace(body: str) -> str:
    """Remove HTML comments and collapse whitespace for length check."""
    no_comments = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    return no_comments.strip()


def validate_content_body(skill_path: Path) -> BodyValidationResult:
    """Validate the content body of a SKILL.md file.

    Checks:
    - Frontmatter exists and contains required fields
    - Body has minimum content length
    - Body contains required sections (headings)
    - Body contains recommended sections (warning if missing)
    - Frontmatter license is valid
    - No duplicate headings
    - Body is not just placeholder text
    """
    result = BodyValidationResult(skill_path)
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        result.error("SKILL.md not found")
        return result

    try:
        content = skill_md.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        result.error("SKILL.md is not valid UTF-8")
        return result

    frontmatter, body = parse_frontmatter(content)

    # --- Frontmatter checks ---
    if frontmatter is None:
        result.error("SKILL.md has no valid YAML frontmatter")
        return result

    # License validation
    license_val = frontmatter.get("license", "")
    if license_val and license_val not in VALID_LICENSES:
        result.warn(
            f"License '{license_val}' is not a common open-source license. "
            f"Common choices: {', '.join(sorted(VALID_LICENSES))}"
        )

    # --- Body checks ---
    clean_body = _strip_comments_and_whitespace(body)

    if len(clean_body) < MIN_BODY_LENGTH:
        result.error(
            f"Body content is too short ({len(clean_body)} chars, minimum {MIN_BODY_LENGTH}). "
            "Add meaningful instructions to your skill."
        )

    # Check for placeholder-only content
    body_no_placeholders = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL).strip()
    if len(body_no_placeholders) < 20:
        result.error("Body appears to be only placeholder comments with no real content")

    # Extract headings and check sections
    headings = _extract_headings(body)
    heading_set_lower = {h.lower() for h in headings}

    for section in REQUIRED_SECTIONS:
        if section not in heading_set_lower:
            result.error(f"Missing required section: '{_section_display(section)}'")

    for section in RECOMMENDED_SECTIONS:
        if section not in heading_set_lower:
            result.warn(f"Missing recommended section: '{_section_display(section)}'")

    # Check for duplicate headings
    seen_headings: dict[str, int] = {}
    for h in headings:
        key = h.lower()
        seen_headings[key] = seen_headings.get(key, 0) + 1
    for h, count in seen_headings.items():
        if count > 1:
            result.warn(f"Duplicate heading: '{h}' (appears {count} times)")

    # Scan for prompt injection patterns
    check_prompt_injection(content, result)

    return result
