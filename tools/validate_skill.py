#!/usr/bin/env python3
"""Validate one or all skills against hawk-community-skills quality standards."""

import os
import re
import stat
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
except ImportError:
    print("Missing dependencies. Install with: pip install -r tools/requirements.txt")
    sys.exit(1)

# Add tools directory to path for shared imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from frontmatter import parse_frontmatter
from skill_discovery import iter_skills

REPO_ROOT = Path(__file__).resolve().parent.parent
CATEGORIES_DIR = REPO_ROOT / "categories"

REQUIRED_FIELDS = {"name", "description", "license"}
MAX_DESCRIPTION_LEN = 200
MAX_FILE_SIZE = 100 * 1024  # 100KB — warning threshold
# Hard limit for SKILL.md itself: a skill definition this large is almost
# certainly bulk content that belongs in reference files, and it bloats every
# consumer that loads the skill. Errors above this; warns above MAX_FILE_SIZE.
MAX_SKILL_MD_SIZE = 500 * 1024  # 500KB — error threshold
# Pre-existing oversized SKILL.md files are grandfathered (warning only) so
# the new error does not break CI on the existing corpus. Do not add new
# entries; shrink these skills instead.
SIZE_ALLOWLIST_PATH = Path(__file__).resolve().parent / "skill_size_allowlist.txt"
ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".pdf"}
TAG_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
MIN_TAGS = 1
MAX_TAGS = 5

console = Console()


def load_size_allowlist(path: Path = SIZE_ALLOWLIST_PATH) -> set:
    """Load grandfathered skill paths (repo-relative) allowed to exceed
    MAX_SKILL_MD_SIZE. Returns an empty set when the file is absent."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return set()
    return {line.strip() for line in lines if line.strip() and not line.strip().startswith("#")}


class ValidationResult:
    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.errors: list[str] = []
        self.warnings: list[str] = []

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)


def validate_skill(skill_path: Path) -> ValidationResult:
    """Run all validation checks on a single skill directory."""
    result = ValidationResult(skill_path)
    skill_name = skill_path.name

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        result.error("SKILL.md not found")
        return result

    # Read and parse SKILL.md
    try:
        content = skill_md.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        result.error("SKILL.md is not valid UTF-8")
        return result
    frontmatter, body = parse_frontmatter(content)

    if frontmatter is None:
        result.error("SKILL.md has no valid YAML frontmatter (must start with ---)")
        return result

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            result.error(f"Missing required frontmatter field: '{field}'")

    # Check description length
    desc = frontmatter.get("description", "")
    if isinstance(desc, str) and len(desc) > MAX_DESCRIPTION_LEN:
        result.warn(f"Description is {len(desc)} chars (max recommended: {MAX_DESCRIPTION_LEN})")

    # Validate tags
    tags = frontmatter.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    if not isinstance(tags, list):
        result.error("Frontmatter 'tags' must be a list or comma-separated string")
    else:
        # Filter out None/empty and normalize
        valid_tags = [t for t in tags if t]
        if len(valid_tags) < MIN_TAGS:
            result.error(f"Skill must have at least {MIN_TAGS} tag(s), found {len(valid_tags)}")
        if len(valid_tags) > MAX_TAGS:
            result.warn(f"Skill has {len(valid_tags)} tags (recommended max: {MAX_TAGS})")
        for tag in valid_tags:
            if not isinstance(tag, str):
                result.error(f"Tag must be a string, got {type(tag).__name__}: {repr(tag)}")
            elif tag.strip() == "":
                result.error("Tags must not be empty strings")
            elif not TAG_PATTERN.match(tag):
                result.error(
                    f"Tag '{tag}' is invalid: must be lowercase alphanumeric "
                    f"with hyphens (e.g. 'my-tag')"
                )

    # Check name matches directory
    fm_name = frontmatter.get("name", "")
    if fm_name and fm_name != skill_name:
        result.error(f"Frontmatter name '{fm_name}' does not match directory name '{skill_name}'")

    # Check for broken internal references (relative links in markdown)
    link_pattern = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
    for match in link_pattern.finditer(content):
        link_text, link_target = match.groups()
        # Skip external URLs
        if link_target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        # Resolve relative path
        target_path = (skill_path / link_target).resolve()
        if not target_path.is_relative_to(skill_path.resolve()):
            result.warn(
                f"Path traversal detected: [{link_text}]({link_target}) "
                f"resolves outside skill directory"
            )
        elif not target_path.exists():
            result.warn(f"Broken internal reference: [{link_text}]({link_target})")

    # Check scripts have shebang and are executable
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.iterdir():
            if script.is_file() and script.suffix in (".sh", ".py", ".bash"):
                # Check shebang
                first_line = script.read_text(encoding="utf-8", errors="ignore").split("\n", 1)[0]
                if not first_line.startswith("#!"):
                    result.warn(f"Script {script.name} missing shebang line")
                # Check executable bit
                mode = script.stat().st_mode
                if not (mode & stat.S_IXUSR):
                    result.warn(f"Script {script.name} is not executable (chmod +x)")

    # SKILL.md has a hard size limit: error above MAX_SKILL_MD_SIZE unless the
    # skill is grandfathered in the size allowlist (then it only warns).
    skill_md_size = skill_md.stat().st_size
    if skill_md_size > MAX_SKILL_MD_SIZE:
        resolved = skill_path.resolve()
        try:
            rel_skill = str(resolved.relative_to(REPO_ROOT))
        except ValueError:
            rel_skill = skill_path.name
        msg = (
            f"SKILL.md is {skill_md_size // 1024}KB "
            f"(max: {MAX_SKILL_MD_SIZE // 1024}KB); move bulk content to reference files"
        )
        if rel_skill in load_size_allowlist():
            result.warn(f"{msg} [grandfathered]")
        else:
            result.error(msg)

    # Check file size across all files in the skill directory
    for dirpath, _dirnames, filenames in os.walk(skill_path):
        for filename in filenames:
            filepath = Path(dirpath) / filename
            if (
                filepath.stat().st_size > MAX_FILE_SIZE
                and filepath.suffix.lower() not in ASSET_EXTENSIONS
            ):
                result.warn(f"File {filepath.relative_to(skill_path)} exceeds 100KB")

    return result


def find_all_skills() -> list[Path]:
    """Find all skill directories under categories/."""
    return list(iter_skills(CATEGORIES_DIR))


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate hawk-community-skills")
    parser.add_argument("path", nargs="?", help="Path to a specific skill directory")
    parser.add_argument("--all", action="store_true", help="Validate all skills")
    args = parser.parse_args()

    if not args.path and not args.all:
        parser.print_help()
        console.print("\n[yellow]Provide a skill path or use --all[/yellow]")
        sys.exit(1)

    if args.all:
        skills = find_all_skills()
        if not skills:
            console.print("[yellow]No skills found in categories/[/yellow]")
            sys.exit(0)
    else:
        skill_path = Path(args.path).resolve()
        if not skill_path.is_dir():
            console.print(f"[red]Not a directory: {args.path}[/red]")
            sys.exit(1)
        skills = [skill_path]

    total = len(skills)
    passed = 0
    failed = 0

    table = Table(title="Validation Results")
    table.add_column("Skill", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Errors", style="red")
    table.add_column("Warnings", style="yellow")

    for skill_path in skills:
        result = validate_skill(skill_path)
        if result.passed:
            passed += 1
            status = "[green]PASS[/green]"
        else:
            failed += 1
            status = "[red]FAIL[/red]"

        rel_path = (
            str(skill_path.relative_to(REPO_ROOT))
            if str(skill_path).startswith(str(REPO_ROOT))
            else skill_path.name
        )
        table.add_row(
            rel_path,
            status,
            str(len(result.errors)) if result.errors else "-",
            str(len(result.warnings)) if result.warnings else "-",
        )

        # Print details for failures
        if not result.passed or result.warnings:
            for err in result.errors:
                console.print(f"  ERROR {rel_path}: {err}", markup=False)
            for warn in result.warnings:
                console.print(f"  WARN  {rel_path}: {warn}", markup=False)

    console.print()
    console.print(table)
    console.print()
    console.print(f"[bold]Total: {total} | Passed: {passed} | Failed: {failed}[/bold]")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
