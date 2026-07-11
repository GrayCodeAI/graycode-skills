#!/usr/bin/env python3
"""Interactive CLI to scaffold a new skill in hawk-community-skills."""

import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Confirm, Prompt
except ImportError:
    print("Missing dependencies. Install with: pip install -r tools/requirements.txt")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = REPO_ROOT / "categories"

console = Console()

KEBAB_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


def get_existing_skills() -> set:
    """Walk all categories and collect existing skill names."""
    names = set()
    if not CATEGORIES_DIR.exists():
        return names
    for category_dir in CATEGORIES_DIR.iterdir():
        if category_dir.is_dir():
            for skill_dir in category_dir.iterdir():
                if skill_dir.is_dir():
                    names.add(skill_dir.name)
    return names


def validate_name(name: str, existing: set) -> str | None:
    """Return error message if name is invalid, else None."""
    if not KEBAB_RE.match(name):
        return (
            "Name must be kebab-case (lowercase letters, numbers, "
            "hyphens only, starting with a letter)."
        )
    if name in existing:
        return f"Skill '{name}' already exists."
    return None


def get_categories() -> list:
    """List available categories."""
    if not CATEGORIES_DIR.exists():
        return []
    return sorted(d.name for d in CATEGORIES_DIR.iterdir() if d.is_dir())


def main():
    console.print(Panel("[bold cyan]Hawk Community Skills - New Skill Scaffolder[/bold cyan]"))

    existing = get_existing_skills()
    categories = get_categories()

    # --- Name ---
    while True:
        name = Prompt.ask("[bold]Skill name[/bold] (kebab-case)")
        err = validate_name(name, existing)
        if err:
            console.print(f"[red]{err}[/red]")
        else:
            break

    # --- Category ---
    if categories:
        console.print(f"[dim]Available categories: {', '.join(categories)}[/dim]")
    category = Prompt.ask("[bold]Category[/bold]")
    if not re.match(r"^[a-z][a-z0-9-]*$", category):
        console.print("[yellow]Warning: category name should be lowercase with hyphens.[/yellow]")

    # --- Description ---
    description = Prompt.ask("[bold]Short description[/bold] (under 200 chars)")
    if len(description) > 200:
        console.print(
            "[yellow]Warning: description exceeds 200 characters, consider shortening.[/yellow]"
        )

    # --- Tags ---
    tag_re = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
    while True:
        tags_raw = Prompt.ask(
            "[bold]Tags[/bold] (comma-separated, 1-5 lowercase kebab-case)", default="general"
        )
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        if len(tags) < 1:
            console.print("[red]At least 1 tag is required.[/red]")
        elif len(tags) > 5:
            console.print("[red]Maximum 5 tags allowed.[/red]")
        elif any(not tag_re.match(t) for t in tags):
            bad = [t for t in tags if not tag_re.match(t)]
            console.print(
                f"[red]Invalid tag(s): {', '.join(bad)}. "
                f"Must be lowercase alphanumeric with hyphens.[/red]"
            )
        else:
            break

    # --- Author ---
    author = Prompt.ask("[bold]Author[/bold]", default="community")

    # --- Optional subdirectories ---
    create_scripts = Confirm.ask("Create [bold]scripts/[/bold] directory?", default=False)
    create_examples = Confirm.ask("Create [bold]examples/[/bold] directory?", default=False)
    create_assets = Confirm.ask("Create [bold]assets/[/bold] directory?", default=False)

    # --- Build directory ---
    skill_dir = CATEGORIES_DIR / category / name
    skill_dir.mkdir(parents=True, exist_ok=True)

    if create_scripts:
        (skill_dir / "scripts").mkdir(exist_ok=True)
        (skill_dir / "scripts" / ".gitkeep").touch()
    if create_examples:
        (skill_dir / "examples").mkdir(exist_ok=True)
        (skill_dir / "examples" / ".gitkeep").touch()
    if create_assets:
        (skill_dir / "assets").mkdir(exist_ok=True)
        (skill_dir / "assets" / ".gitkeep").touch()

    # --- Generate SKILL.md ---
    today = date.today().isoformat()
    frontmatter = {
        "name": name,
        "description": description,
        "domain": category,
        "subdomain": "",
        "tags": tags,
        "version": "1.0",
        "author": author,
        "license": "MIT",
        "date_added": today,
    }

    yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)

    skill_md = f"""---
{yaml_str.strip()}
---

# {name.replace("-", " ").title()}

## Overview

<!-- Describe what this skill does in 2-3 sentences. -->

## When to Use

<!-- List specific scenarios where this skill is useful. -->

## Instructions

<!-- Provide detailed instructions for how the skill should behave. -->

## References

<!-- Link to relevant docs, APIs, or related skills. Remove this section if not needed. -->
"""

    (skill_dir / "SKILL.md").write_text(skill_md)

    console.print()
    console.print("[bold green]Skill scaffolded successfully![/bold green]")
    console.print(f"  Path: [cyan]{skill_dir.relative_to(REPO_ROOT)}[/cyan]")
    console.print("  SKILL.md created with frontmatter")
    if create_scripts:
        console.print("  scripts/ directory created")
    if create_examples:
        console.print("  examples/ directory created")
    if create_assets:
        console.print("  assets/ directory created")
    console.print()
    console.print(
        "[dim]Next steps: edit SKILL.md, then run python tools/validate_skill.py to check[/dim]"
    )


if __name__ == "__main__":
    main()
