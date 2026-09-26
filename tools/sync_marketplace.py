#!/usr/bin/env python3
"""Generate .claude-plugin/marketplace.json from the categories/ directory.

The marketplace publishes one Claude Code plugin per category, named
``graycode-skills-<category>``. Each plugin's ``source`` is its category
directory and its ``skills`` field is the directory path ``./`` (relative to
that source); Claude Code discovers every ``<skill>/SKILL.md`` below it and
caches only that category when the plugin is installed. This is the shape
`claude plugin validate --strict` accepts. The previous shape, a single plugin
whose ``skills`` held 14k ``{name, path, invoke}`` objects, was rejected with
``plugins.0.skills: Invalid input``.

Per-category plugins also let users enable only what they need: every
installed skill's description is added to each session's context.

Top-level keys already in marketplace.json (``name``, ``owner``,
``description``, ...) are preserved; ``plugins`` is regenerated. Every plugin
carries the version from the VERSION file.
"""

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = REPO_ROOT / "categories"
MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"
VERSION_FILE = REPO_ROOT / "VERSION"

PLUGIN_PREFIX = "graycode-skills-"
DEFAULT_TOP_LEVEL: dict[str, Any] = {
    "name": "graycode-skills",
    "owner": {"name": "GrayCode AI", "url": "https://github.com/GrayCodeAI"},
    "description": (
        "GrayCode Skills: community Agent Skills (SKILL.md) packages for Rho and "
        "other Agent Skills clients, one plugin per category."
    ),
}

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
    """Scan categories/ and return one {name, category, path} per skill.

    Raises SystemExit if two skills resolve to the same name: skill names are
    the user-facing identifiers, so a collision would make one unreachable.
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
        path = skill_dir.relative_to(REPO_ROOT).as_posix()
        if name in seen_names:
            raise SystemExit(f"✗ Duplicate skill name '{name}': {seen_names[name]} and {path}")
        seen_names[name] = path
        skills.append({"name": name, "category": skill_dir.parent.name, "path": path})
    return skills


def read_version(template: dict[str, Any]) -> str:
    """Return VERSION, falling back to the template's first plugin version."""
    try:
        version = VERSION_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        version = ""
    if version:
        return version
    plugins = template.get("plugins")
    if isinstance(plugins, list) and plugins and isinstance(plugins[0], dict):
        return str(plugins[0].get("version", "0.0.0"))
    return "0.0.0"


def build_plugins(skills: list[dict[str, str]], version: str) -> list[dict[str, Any]]:
    """Return one plugin entry per category, sorted by category."""
    counts: dict[str, int] = {}
    for skill in skills:
        counts[skill["category"]] = counts.get(skill["category"], 0) + 1
    plugins = []
    for category in sorted(counts):
        count = counts[category]
        noun = "skill" if count == 1 else "skills"
        plugins.append(
            {
                "name": f"{PLUGIN_PREFIX}{category}",
                "source": f"./categories/{category}",
                "description": f"GrayCode Skills, {category} category: {count} {noun}.",
                "version": version,
                "skills": ["./"],
            }
        )
    return plugins


def load_template() -> dict[str, Any]:
    """Read the existing marketplace.json (its top-level keys are preserved)."""
    try:
        raw = MARKETPLACE.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(
            f"✗ Marketplace template not found: {_display_path(MARKETPLACE)}"
        ) from None
    except OSError as exc:
        raise SystemExit(f"✗ Cannot read {_display_path(MARKETPLACE)}: {exc}") from None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"✗ {_display_path(MARKETPLACE)} is not valid JSON: {exc}") from None
    if not isinstance(data, dict):
        raise SystemExit(
            f"✗ {_display_path(MARKETPLACE)} has unexpected structure: "
            "expected a top-level JSON object"
        )
    return data


def render(skills: list[dict[str, str]]) -> str:
    """Return the marketplace.json text for the given skills."""
    template = load_template()
    document: dict[str, Any] = {}
    for key, default in DEFAULT_TOP_LEVEL.items():
        document[key] = template.get(key, default)
    for key, value in template.items():
        if key not in document and key != "plugins":
            document[key] = value
    document["plugins"] = build_plugins(skills, read_version(template))
    return json.dumps(document, indent=2) + "\n"


def main() -> None:
    check_only = "--check" in sys.argv[1:]
    skills = build_skills()
    rendered = render(skills)
    plugin_count = len(json.loads(rendered)["plugins"])
    summary = f"{len(skills)} skills in {plugin_count} category plugins"

    if check_only:
        current = MARKETPLACE.read_text(encoding="utf-8") if MARKETPLACE.exists() else ""
        if current != rendered:
            print(
                f"✗ marketplace.json is out of sync with categories/ "
                f"({summary}). Run: python3 tools/sync_marketplace.py"
            )
            sys.exit(1)
        print(f"✓ marketplace.json in sync ({summary})")
        return

    MARKETPLACE.write_text(rendered, encoding="utf-8")
    print(f"✓ Synced {summary} to marketplace.json")


if __name__ == "__main__":
    main()
