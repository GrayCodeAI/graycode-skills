#!/usr/bin/env python3
"""Generate marketplace.json skills array from categories/ directory."""

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = REPO_ROOT / "categories"
MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"

# Add tools directory to path for shared imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from frontmatter import parse_frontmatter_dict  # noqa: E402
from skill_discovery import iter_skills  # noqa: E402


def _display_path(path: Path) -> str:
    """Return a repo-relative path when possible, else a stable absolute path."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def extract_frontmatter(skill_md: Path) -> dict[str, Any]:
    """Extract YAML frontmatter from a skill markdown file."""
    content = skill_md.read_text(encoding="utf-8", errors="ignore")
    fm = parse_frontmatter_dict(content)
    return fm if fm else {}


def build_skills() -> list[dict[str, str]]:
    """Scan categories/ and return the marketplace skills array.

    Raises SystemExit if two skills resolve to the same name — a silent
    collision would make one skill's marketplace entry unreachable.
    """
    skills = []
    seen_names: dict[str, str] = {}  # name -> path that claimed it
    for skill_dir in iter_skills(CATEGORIES_DIR):
        skill_md = skill_dir / "SKILL.md"
        try:
            fm = extract_frontmatter(skill_md)
        except (UnicodeDecodeError, OSError) as exc:
            print(
                f"⚠ Skipping unreadable skill {_display_path(skill_md)}: {exc}",
                file=sys.stderr,
            )
            continue
        fm_name = fm.get("name")
        if fm_name and fm_name != skill_dir.name:
            print(
                f"⚠ {_display_path(skill_md)}: frontmatter name "
                f"'{fm_name}' does not match directory name "
                f"'{skill_dir.name}'; using frontmatter name",
                file=sys.stderr,
            )
        name = fm_name or skill_dir.name
        path = str(skill_dir.relative_to(REPO_ROOT))
        if name in seen_names:
            raise SystemExit(f"✗ Duplicate skill name '{name}': {seen_names[name]} and {path}")
        seen_names[name] = path
        invoke = fm.get("invoke", f"/graycode:{name}")
        skills.append(
            {
                "name": name,
                "path": path,
                "invoke": invoke,
            }
        )
    return skills


def render(skills: list[dict[str, str]]) -> str:
    """Return the marketplace.json text with skills populated."""
    try:
        raw = MARKETPLACE.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(
            f"✗ Marketplace template not found: {MARKETPLACE.relative_to(REPO_ROOT)}"
        ) from None
    except OSError as exc:
        raise SystemExit(f"✗ Cannot read {MARKETPLACE.relative_to(REPO_ROOT)}: {exc}") from None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"✗ {MARKETPLACE.relative_to(REPO_ROOT)} is not valid JSON: {exc}"
        ) from None

    plugins = data.get("plugins") if isinstance(data, dict) else None
    if not isinstance(plugins, list) or not plugins or not isinstance(plugins[0], dict):
        raise SystemExit(
            f"✗ {MARKETPLACE.relative_to(REPO_ROOT)} has unexpected structure: "
            "expected a top-level object with a non-empty 'plugins' array of objects"
        )
    plugins[0]["skills"] = skills
    return json.dumps(data, indent=2) + "\n"


def main() -> None:
    check_only = "--check" in sys.argv[1:]
    skills = build_skills()
    rendered = render(skills)

    if check_only:
        current = MARKETPLACE.read_text() if MARKETPLACE.exists() else ""
        if current != rendered:
            print(
                f"✗ marketplace.json is out of sync with categories/ "
                f"({len(skills)} skills). Run: python3 tools/sync_marketplace.py"
            )
            sys.exit(1)
        print(f"✓ marketplace.json in sync ({len(skills)} skills)")
        return

    MARKETPLACE.write_text(rendered)
    print(f"✓ Synced {len(skills)} skills to marketplace.json")


if __name__ == "__main__":
    main()
