#!/usr/bin/env python3
"""Regenerate registry.json from all skill directories."""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from rich.console import Console
except ImportError:
    print("Missing dependencies. Install with: pip install -r tools/requirements.txt")
    sys.exit(1)

# Add tools directory to path for shared imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from frontmatter import parse_frontmatter
from registry_schema import validate_registry_entry
from skill_discovery import iter_skills

REPO_ROOT = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = REPO_ROOT / "categories"
REGISTRY_PATH = REPO_ROOT / "registry.json"

console = Console()


def _display_path(path: Path) -> str:
    """Return a repo-relative path when possible, else a stable absolute path."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


# parse_frontmatter is now imported from frontmatter module


def count_files(path: Path) -> int:
    """Count files in a directory recursively."""
    return sum(len(files) for _, _, files in os.walk(path))


def has_scripts_dir(path: Path) -> bool:
    """Check if skill has a scripts/ directory with files."""
    scripts_dir = path / "scripts"
    if not scripts_dir.exists():
        return False
    return any(scripts_dir.iterdir())


def _build_registry_with_duplicates() -> tuple[list[dict], list[tuple[str, str, str]]]:
    """Walk all categories and build registry entries.

    Returns (entries, duplicates) where duplicates is a list of
    (name, winning_path, losing_path) tuples for skipped duplicate names.
    """
    entries = []
    seen_names: dict[str, str] = {}  # name -> path that won
    duplicates: list[tuple[str, str, str]] = []

    if not CATEGORIES_DIR.exists():
        console.print("[yellow]No categories/ directory found[/yellow]")
        return entries, duplicates

    for skill_dir in iter_skills(CATEGORIES_DIR):
        category_name = skill_dir.parent.name
        skill_md = skill_dir / "SKILL.md"

        try:
            content = skill_md.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            print(
                f"⚠ Skipping unreadable skill {_display_path(skill_md)}: {exc}",
                file=sys.stderr,
            )
            continue
        frontmatter, _ = parse_frontmatter(content)

        if frontmatter is None:
            continue

        # Keep frontmatter `name` precedence for compatibility with
        # registry consumers and existing tests, but warn on mismatch so
        # drift is still visible.
        fm_name = frontmatter.get("name")
        if fm_name and fm_name != skill_dir.name:
            print(
                f"⚠ {_display_path(skill_md)}: frontmatter name "
                f"'{fm_name}' does not match directory name "
                f"'{skill_dir.name}'; using frontmatter name",
                file=sys.stderr,
            )
        name = fm_name or skill_dir.name
        description = frontmatter.get("description", "")
        # Truncate multi-line descriptions for registry
        if isinstance(description, str):
            description = " ".join(description.split())[:200]

        tags = frontmatter.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        # Generate a default tag from category if tags are empty
        if not tags:
            tags = [category_name.lower().replace(" ", "-")]

        path = f"categories/{category_name}/{skill_dir.name}"

        # Skip duplicate names (keep first occurrence), but record them
        if name in seen_names:
            duplicates.append((name, seen_names[name], path))
            continue
        seen_names[name] = path

        entry = {
            "name": name,
            "description": description,
            "category": category_name,
            "tags": tags,
            "path": path,
            "file_count": count_files(skill_dir),
            "has_scripts": has_scripts_dir(skill_dir),
        }
        entries.append(entry)

    # Sort alphabetically by name
    entries.sort(key=lambda e: e["name"].lower())
    return entries, duplicates


def build_registry() -> list[dict]:
    """Walk all categories and build registry entries."""
    entries, _duplicates = _build_registry_with_duplicates()
    return entries


def report_duplicates(duplicates: list[tuple[str, str, str]]) -> None:
    """Print a summary of duplicate skill names to stderr."""
    if not duplicates:
        return
    print(
        f"⚠ {len(duplicates)} duplicate skill name(s) skipped (first occurrence wins):",
        file=sys.stderr,
    )
    for name, won, lost in duplicates:
        print(f"  - '{name}': kept {won}, skipped {lost}", file=sys.stderr)


def validate_entries(entries: list[dict]) -> list[str]:
    """Validate each registry entry against the schema.

    Returns a list of human-readable violation strings (empty when valid).
    """
    violations: list[str] = []
    for entry in entries:
        label = entry.get("path") or entry.get("name") or "<unknown entry>"
        for err in validate_registry_entry(entry, path=str(label)):
            violations.append(f"{err.path}: {err.message}")
    return violations


def render_registry(entries: list[dict]) -> str:
    """Render registry entries in the canonical on-disk format."""
    return json.dumps(entries, indent=2, ensure_ascii=False) + "\n"


def registry_is_current(expected: str) -> bool:
    """Return whether registry.json exactly matches the generated registry."""
    try:
        actual = REGISTRY_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        console.print(
            f"[bold red]Registry check failed:[/bold red] "
            f"cannot read {_display_path(REGISTRY_PATH)}: {exc}"
        )
        return False

    if actual == expected:
        return True

    console.print(
        f"[bold red]Registry check failed:[/bold red] {_display_path(REGISTRY_PATH)} is stale."
    )
    console.print("  Regenerate it with: [cyan]python3 tools/update_registry.py[/cyan]")
    return False


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(
        description="Regenerate registry.json from all skill directories"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if registry.json is stale without modifying it",
    )
    args = parser.parse_args([] if argv is None else argv)

    console.print("[dim]Scanning categories for skills...[/dim]")
    entries, duplicates = _build_registry_with_duplicates()

    if not entries:
        if args.check:
            console.print("[bold red]Registry check failed:[/bold red] no valid skills found.")
            sys.exit(1)
        console.print("[yellow]No valid skills found.[/yellow]")
        sys.exit(0)

    # Duplicate skill names are a registry-integrity failure (name-squatting,
    # or two contributions silently colliding): fail the build instead of
    # silently picking a winner.
    if duplicates:
        console.print(
            f"[bold red]{len(duplicates)} duplicate skill name(s) found; "
            f"registry.json not written:[/bold red]"
        )
        report_duplicates(duplicates)
        sys.exit(1)

    # Enforce the registry schema before writing anything
    violations = validate_entries(entries)
    if violations:
        console.print(
            f"[bold red]Schema validation failed "
            f"({len(violations)} violation(s)); registry.json not written:[/bold red]"
        )
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        sys.exit(1)

    rendered = render_registry(entries)
    if args.check:
        if not registry_is_current(rendered):
            sys.exit(1)
        console.print("[bold green]Registry is current.[/bold green]")
        console.print(f"  Skills indexed: [cyan]{len(entries)}[/cyan]")
        return

    # Write registry
    REGISTRY_PATH.write_text(rendered, encoding="utf-8")

    console.print("[bold green]Registry updated![/bold green]")
    console.print(f"  Skills indexed: [cyan]{len(entries)}[/cyan]")
    console.print(f"  Output: [cyan]{REGISTRY_PATH.relative_to(REPO_ROOT)}[/cyan]")

    # Summary by category
    categories = {}
    for entry in entries:
        cat = entry["category"]
        categories[cat] = categories.get(cat, 0) + 1
    console.print("\n[bold]By category:[/bold]")
    for cat in sorted(categories):
        console.print(f"  {cat}: {categories[cat]}")


if __name__ == "__main__":
    main(sys.argv[1:])
