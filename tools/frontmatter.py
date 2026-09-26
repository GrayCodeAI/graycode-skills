"""Shared YAML frontmatter parsing for skill files."""

from __future__ import annotations

import re
from typing import Any

import yaml


def parse_frontmatter(content: str) -> tuple[dict[str, Any] | None, str]:
    """Extract YAML frontmatter from markdown content.

    Returns (frontmatter_dict, body_text). If no valid frontmatter is found,
    returns (None, original_content).
    """
    lines = content.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, content

    # Find the closing --- on its own line (skip line 0 which is the opener)
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return None, content

    fm_text = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1 :])
    try:
        fm = yaml.safe_load(fm_text)
        return fm if isinstance(fm, dict) else None, body
    except yaml.YAMLError:
        return None, content


def parse_frontmatter_dict(content: str) -> dict[str, Any] | None:
    """Extract YAML frontmatter from markdown content, returning only the dict.

    Returns the frontmatter dict or None if not found/invalid.
    """
    fm, _ = parse_frontmatter(content)
    return fm


def frontmatter_tags(frontmatter: dict[str, Any]) -> Any:
    """Return a skill's raw tags value.

    Top-level ``tags`` (a list or comma-separated string) is the corpus
    convention. The Agent Skills specification (agentskills.io) allows only
    name, description, license, compatibility, metadata and allowed-tools at
    the top level, so a spec-conformant skill may instead put a comma- or
    space-separated string in ``metadata.tags``. Top-level ``tags`` wins when
    both are present. Returns None when neither is set; other types are
    returned unchanged so callers can report them.
    """
    if "tags" in frontmatter:
        return frontmatter["tags"]
    metadata = frontmatter.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("tags"), str):
        return [tag for tag in re.split(r"[,\s]+", metadata["tags"]) if tag]
    return None
