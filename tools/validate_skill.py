#!/usr/bin/env python3
"""Validate one or all skills against graycode-skills quality standards."""

from __future__ import annotations

import json
import os
import re
import stat
import sys
from collections import Counter
from collections.abc import Iterator, Mapping
from pathlib import Path
from urllib.parse import unquote, urlsplit

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

# Agent Skills spec (agentskills.io) — recognized optional frontmatter fields.
# These are informational for graycode-skills but must be well-formed
# if present. See manifest-schema.toml for the full schema.
AGENTSKILLS_OPTIONAL_FIELDS = frozenset(
    {
        "category",
        "auto_invoke",
        "compatibility",
        "allowed_tools",
        "agents",
        "invoke",
        "refs",
        "chain_after",
        "chain_before",
        "chain_conflicts",
        "chain_enhances",
    }
)
CATEGORY_ENUM = {"engineering", "ops", "testing", "security", "devtools", "workflow"}
AGENT_ENUM = {"graycode", "claude-code", "codex", "cursor", "windsurf", "github-actions"}
INVOKE_RE = re.compile(r"^[a-z0-9][a-z0-9-]*:[a-z0-9][a-z0-9-]*$")

# Warning categories are stable machine-readable identifiers. Keep warning text
# human-friendly, but use these identifiers for the checked-in CI ratchet so a
# wording change cannot silently reset the quality baseline.
WARNING_CATEGORIES = frozenset(
    {
        "broken-internal-reference",
        "description-too-long",
        "oversized-file",
        "oversized-skill-md",
        "path-traversal",
        "script-missing-shebang",
        "script-not-executable",
        "too-many-tags",
        "uncategorized",
    }
)

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
        self.warning_counts: Counter[str] = Counter()

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str, *, category: str = "uncategorized"):
        if category not in WARNING_CATEGORIES:
            raise ValueError(f"unknown warning category: {category}")
        self.warnings.append(msg)
        self.warning_counts[category] += 1


def load_warning_budget(path: Path) -> dict[str, int]:
    """Load and validate an exact per-category warning budget."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read warning budget {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ValueError("warning budget must be a JSON object")

    keys = set(raw)
    missing = WARNING_CATEGORIES - keys
    unknown = keys - WARNING_CATEGORIES
    if missing:
        raise ValueError(f"warning budget is missing categories: {', '.join(sorted(missing))}")
    if unknown:
        raise ValueError(f"warning budget has unknown categories: {', '.join(sorted(unknown))}")

    for category, value in raw.items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"warning budget for {category!r} must be a non-negative integer")
    return raw


def compare_warning_budget(actual: Mapping[str, int], budget: Mapping[str, int]) -> list[str]:
    """Return actionable differences from the exact checked-in warning snapshot.

    Decreases intentionally require a budget update in the same change. That
    locks improvements in immediately instead of leaving capacity that a later
    warning could consume unnoticed.
    """
    differences = []
    for category in sorted(WARNING_CATEGORIES):
        current = actual.get(category, 0)
        expected = budget.get(category, 0)
        if current > expected:
            differences.append(
                f"{category}: {current} warnings exceeds the checked-in budget of {expected}"
            )
        elif current < expected:
            differences.append(
                f"{category}: {current} warnings is below the checked-in budget of {expected}; "
                "lower the budget to lock in the improvement"
            )
    return differences


def path_exists_with_exact_case(path: Path, root: Path) -> bool:
    """Check an in-root path using case-sensitive component matching.

    GitHub Actions uses a case-sensitive filesystem, while many contributor
    machines do not. Walking directory entries makes reference counts stable
    across both environments.
    """
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False

    current = root
    for part in relative.parts:
        try:
            if part not in {entry.name for entry in current.iterdir()}:
                return False
        except OSError:
            return False
        current /= part
    return current.exists()


def _is_escaped(markdown: str, position: int) -> bool:
    """Return whether the character at ``position`` has an odd backslash prefix."""
    backslashes = 0
    position -= 1
    while position >= 0 and markdown[position] == "\\":
        backslashes += 1
        position -= 1
    return backslashes % 2 == 1


_MARKDOWN_ESCAPABLE_CHARACTERS = frozenset(r"!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\\")


def _starts_markdown_escape(markdown: str, position: int) -> bool:
    """Return whether ``position`` starts a valid Markdown backslash escape."""
    return (
        markdown[position] == "\\"
        and position + 1 < len(markdown)
        and markdown[position + 1] in _MARKDOWN_ESCAPABLE_CHARACTERS
    )


def _fence_at_line_start(line: str) -> tuple[str, int] | None:
    """Return a CommonMark-style fence marker at the start of ``line``."""
    content = line.rstrip("\r\n")
    indent = len(content) - len(content.lstrip(" "))
    if indent > 3 or indent == len(content):
        return None

    marker = content[indent]
    if marker not in ("`", "~"):
        return None

    end = indent
    while end < len(content) and content[end] == marker:
        end += 1
    length = end - indent
    if length < 3:
        return None
    if marker == "`" and "`" in content[end:]:
        return None
    return marker, length


def _code_mask(markdown: str) -> str:
    """Replace non-newline characters with spaces while retaining offsets."""
    return "".join(char if char in "\r\n" else " " for char in markdown)


def _mask_fenced_code(markdown: str) -> str:
    """Mask fenced code while retaining source offsets and line boundaries."""
    visible: list[str] = []
    fence_marker: str | None = None
    fence_length = 0

    for line in markdown.splitlines(keepends=True):
        fence = _fence_at_line_start(line)
        if fence_marker is None:
            if fence is None:
                visible.append(line)
                continue
            fence_marker, fence_length = fence
        elif fence is not None:
            marker, length = fence
            remainder = line.rstrip("\r\n").lstrip(" ")[length:]
            if marker == fence_marker and length >= fence_length and not remainder.strip():
                fence_marker = None
                fence_length = 0

        visible.append(_code_mask(line))

    return "".join(visible)


def _find_matching_backtick_run(markdown: str, start: int, run_length: int) -> int | None:
    """Find the end of a matching inline-code delimiter run."""
    position = start
    while True:
        position = markdown.find("`", position)
        if position < 0:
            return None
        end = position
        while end < len(markdown) and markdown[end] == "`":
            end += 1
        if end - position == run_length:
            return end
        position = end


def _mask_inline_code(markdown: str) -> str:
    """Mask complete inline-code spans, including spans crossing newlines."""
    visible: list[str] = []
    copied_until = 0
    position = 0
    while position < len(markdown):
        if markdown[position] != "`" or _is_escaped(markdown, position):
            position += 1
            continue

        delimiter_end = position
        while delimiter_end < len(markdown) and markdown[delimiter_end] == "`":
            delimiter_end += 1
        closing_end = _find_matching_backtick_run(markdown, delimiter_end, delimiter_end - position)
        if closing_end is None:
            position = delimiter_end
            continue

        visible.append(markdown[copied_until:position])
        visible.append(_code_mask(markdown[position:closing_end]))
        copied_until = closing_end
        position = closing_end

    visible.append(markdown[copied_until:])
    return "".join(visible)


def _find_label_end(markdown: str, start: int) -> int | None:
    """Find the matching bracket for an inline Markdown link label."""
    depth = 1
    position = start + 1
    while position < len(markdown):
        char = markdown[position]
        if _starts_markdown_escape(markdown, position):
            position += 2
            continue
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return position
        position += 1
    return None


def _optional_title_end(markdown: str, position: int) -> int | None:
    """Consume whitespace, an optional Markdown link title, and ``)``."""
    while position < len(markdown) and markdown[position].isspace():
        position += 1
    if position >= len(markdown):
        return None
    if markdown[position] == ")":
        return position + 1

    opener = markdown[position]
    closer = {'"': '"', "'": "'", "(": ")"}.get(opener)
    if closer is None:
        return None

    position += 1
    while position < len(markdown):
        if _starts_markdown_escape(markdown, position):
            position += 2
            continue
        if markdown[position] == closer:
            position += 1
            break
        position += 1
    else:
        return None

    while position < len(markdown) and markdown[position].isspace():
        position += 1
    if position < len(markdown) and markdown[position] == ")":
        return position + 1
    return None


def _inline_link_destination(markdown: str, start: int) -> tuple[int, int, int] | None:
    """Return the destination bounds and ending offset of an inline link."""
    position = start + 1
    while position < len(markdown) and markdown[position].isspace():
        position += 1
    if position >= len(markdown):
        return None

    if markdown[position] == "<":
        destination_start = position + 1
        position += 1
        while position < len(markdown):
            if _starts_markdown_escape(markdown, position):
                position += 2
                continue
            if markdown[position] == ">":
                link_end = _optional_title_end(markdown, position + 1)
                if link_end is None:
                    return None
                return destination_start, position, link_end
            if markdown[position] in "\r\n":
                return None
            position += 1
        return None

    destination_start = position
    nested_parentheses = 0
    while position < len(markdown):
        char = markdown[position]
        if _starts_markdown_escape(markdown, position):
            position += 2
            continue
        if char == "(":
            nested_parentheses += 1
        elif char == ")":
            if nested_parentheses == 0:
                return destination_start, position, position + 1
            nested_parentheses -= 1
        elif char.isspace() and nested_parentheses == 0:
            link_end = _optional_title_end(markdown, position)
            if link_end is None:
                return None
            return destination_start, position, link_end
        position += 1
    return None


def iter_markdown_inline_links(markdown: str) -> Iterator[tuple[str, str]]:
    """Yield real inline Markdown links while ignoring code and escaped syntax.

    This intentionally covers inline links and images, the forms whose local
    destinations are portable skill dependencies. It does not mistake examples
    inside fenced/inline code or escaped ``\\[label](target)`` text for links.
    """
    source = markdown
    markdown = _mask_inline_code(_mask_fenced_code(markdown))
    position = 0
    while position < len(markdown):
        label_start = markdown.find("[", position)
        if label_start < 0:
            return
        if _is_escaped(markdown, label_start):
            position = label_start + 1
            continue

        label_end = _find_label_end(markdown, label_start)
        if label_end is None or label_end + 1 >= len(markdown) or markdown[label_end + 1] != "(":
            position = label_start + 1
            continue

        parsed = _inline_link_destination(markdown, label_end + 1)
        if parsed is None:
            position = label_end + 1
            continue
        destination_start, destination_end, link_end = parsed
        yield source[label_start + 1 : label_end], source[destination_start:destination_end]
        position = link_end


_MARKDOWN_ESCAPABLE = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~])")
_URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _local_link_path(destination: str) -> str | None:
    """Return a decoded local path, excluding URI, anchor, and same-file links."""
    destination = _MARKDOWN_ESCAPABLE.sub(r"\1", destination.strip())
    if not destination or destination.startswith(("#", "//")):
        return None
    if _URI_SCHEME.match(destination):
        return None

    # Split before decoding so encoded ``#`` and ``?`` remain filename bytes,
    # while real fragments and queries are not included in filesystem checks.
    path = unquote(urlsplit(destination).path)
    if not path:
        return None
    # Normalize Windows-style separators as well as POSIX ones so traversal
    # detection is independent of the validator host operating system.
    return path.replace("\\", "/")


def _markdown_source_paths(skill_path: Path) -> list[Path]:
    """Return in-tree Markdown entries in deterministic source-relative order.

    Directory symlinks are never followed. File symlinks remain in the list so
    validation can reject any that resolve outside the skill boundary.
    """
    sources: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(skill_path, followlinks=False):
        directory = Path(dirpath)
        dirnames[:] = sorted(name for name in dirnames if not (directory / name).is_symlink())
        for filename in sorted(filenames):
            source = directory / filename
            if source.suffix.lower() == ".md":
                sources.append(source)
    return sorted(sources, key=lambda path: path.relative_to(skill_path).as_posix())


def _scan_markdown_references(
    *,
    skill_path: Path,
    skill_root: Path,
    skill_md: Path,
    skill_body: str,
    result: ValidationResult,
) -> None:
    """Validate local links in every Markdown source without escaping the skill."""
    for source in _markdown_source_paths(skill_path):
        source_relative = source.relative_to(skill_path).as_posix()
        try:
            resolved_source = source.resolve()
        except (OSError, RuntimeError) as exc:
            result.error(f"{source_relative}: cannot resolve Markdown source safely: {exc}")
            continue
        if not resolved_source.is_relative_to(skill_root):
            result.warn(
                f"{source_relative}: Markdown source resolves outside skill directory",
                category="path-traversal",
            )
            continue

        if source == skill_md:
            markdown = skill_body
        else:
            try:
                content = source.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                result.error(f"{source_relative}: Markdown file is not valid UTF-8")
                continue
            except OSError as exc:
                result.error(f"{source_relative}: cannot read Markdown file: {exc}")
                continue
            nested_frontmatter, nested_body = parse_frontmatter(content)
            markdown = nested_body if nested_frontmatter is not None else content

        for link_text, link_target in iter_markdown_inline_links(markdown):
            local_path = _local_link_path(link_target)
            if local_path is None:
                continue
            try:
                target_path = (source.parent / local_path).resolve()
            except (OSError, RuntimeError):
                result.warn(
                    f"{source_relative}: Path traversal detected: "
                    f"[{link_text}]({link_target}) cannot be resolved safely",
                    category="path-traversal",
                )
                continue
            if not target_path.is_relative_to(skill_root):
                result.warn(
                    f"{source_relative}: Path traversal detected: "
                    f"[{link_text}]({link_target}) resolves outside skill directory",
                    category="path-traversal",
                )
            elif not path_exists_with_exact_case(target_path, skill_root):
                result.warn(
                    f"{source_relative}: Broken internal reference: [{link_text}]({link_target})",
                    category="broken-internal-reference",
                )


def validate_skill(skill_path: Path) -> ValidationResult:
    """Run all validation checks on a single skill directory."""
    result = ValidationResult(skill_path)
    skill_name = skill_path.name

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        result.error("SKILL.md not found")
        return result

    skill_root = skill_path.resolve()
    try:
        resolved_skill_md = skill_md.resolve()
    except (OSError, RuntimeError) as exc:
        result.error(f"SKILL.md cannot be resolved safely: {exc}")
        return result
    if not resolved_skill_md.is_relative_to(skill_root):
        result.error("SKILL.md resolves outside skill directory")
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
        result.warn(
            f"Description is {len(desc)} chars (max recommended: {MAX_DESCRIPTION_LEN})",
            category="description-too-long",
        )

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
            result.warn(
                f"Skill has {len(valid_tags)} tags (recommended max: {MAX_TAGS})",
                category="too-many-tags",
            )
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

    # ── Agent Skills spec (agentskills.io) validation ──────────────────────
    # Note: 'category' is an optional agentskills.io field. Existing skills
    # use their own category taxonomy, so we only validate well-formedness
    # of agentskills.io-specific fields when present, not the category value
    # against the agentskills.io enum (which would break existing skills).

    auto_invoke = frontmatter.get("auto_invoke")
    if auto_invoke is not None and not isinstance(auto_invoke, bool):
        result.error(f"auto_invoke must be a boolean, got {type(auto_invoke).__name__}")

    compatibility = frontmatter.get("compatibility")
    if compatibility is not None and not isinstance(compatibility, str):
        result.error(f"compatibility must be a string, got {type(compatibility).__name__}")

    allowed_tools = frontmatter.get("allowed_tools")
    if allowed_tools is not None and not isinstance(allowed_tools, str):
        result.error(f"allowed_tools must be a string, got {type(allowed_tools).__name__}")

    agents = frontmatter.get("agents")
    if agents is not None:
        # Accept both string and list forms for backward compatibility
        if isinstance(agents, str):
            agents = [agents]
        if not isinstance(agents, list):
            result.error(f"agents must be a list or string, got {type(agents).__name__}")
        else:
            for agent in agents:
                if not isinstance(agent, str):
                    result.error(f"agent must be a string, got {type(agent).__name__}: {repr(agent)}")
                # Only warn on unknown agents, don't error — existing skills
                # may use agent names not in the agentskills.io enum

    invoke = frontmatter.get("invoke")
    if invoke is not None and not isinstance(invoke, str):
        result.error(f"invoke must be a string, got {type(invoke).__name__}")
    elif invoke is not None and not INVOKE_RE.match(invoke):
        result.error(
            f"invoke {invoke!r} must match pattern vendor:skill "
            f"(e.g. 'cursor:drizzle')"
        )

    for chain_field in ("chain_after", "chain_before", "chain_conflicts", "chain_enhances"):
        val = frontmatter.get(chain_field)
        if val is not None and not isinstance(val, list):
            result.error(f"{chain_field} must be a list")

    # Check real relative links in every Markdown file. Frontmatter and code
    # examples are metadata/content, not portable file dependencies.
    _scan_markdown_references(
        skill_path=skill_path,
        skill_root=skill_root,
        skill_md=skill_md,
        skill_body=body,
        result=result,
    )

    # Check scripts have shebang and are executable
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.iterdir():
            if script.is_file() and script.suffix in (".sh", ".py", ".bash"):
                # Check shebang
                first_line = script.read_text(encoding="utf-8", errors="ignore").split("\n", 1)[0]
                if not first_line.startswith("#!"):
                    result.warn(
                        f"Script {script.name} missing shebang line",
                        category="script-missing-shebang",
                    )
                # Check executable bit
                mode = script.stat().st_mode
                if not (mode & stat.S_IXUSR):
                    result.warn(
                        f"Script {script.name} is not executable (chmod +x)",
                        category="script-not-executable",
                    )

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
            result.warn(f"{msg} [grandfathered]", category="oversized-skill-md")
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
                result.warn(
                    f"File {filepath.relative_to(skill_path)} exceeds 100KB",
                    category="oversized-file",
                )

    return result


def find_all_skills() -> list[Path]:
    """Find all skill directories under categories/."""
    return list(iter_skills(CATEGORIES_DIR))


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate graycode-skills")
    parser.add_argument("path", nargs="?", help="Path to a specific skill directory")
    parser.add_argument("--all", action="store_true", help="Validate all skills")
    parser.add_argument(
        "--warning-budget",
        type=Path,
        help="Enforce an exact per-category warning budget (requires --all)",
    )
    args = parser.parse_args()

    if not args.path and not args.all:
        parser.print_help()
        console.print("\n[yellow]Provide a skill path or use --all[/yellow]")
        sys.exit(1)

    if args.warning_budget and not args.all:
        parser.error("--warning-budget requires --all")

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
    warning_counts: Counter[str] = Counter()

    table = Table(title="Validation Results")
    table.add_column("Skill", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Errors", style="red")
    table.add_column("Warnings", style="yellow")

    for skill_path in skills:
        result = validate_skill(skill_path)
        warning_counts.update(result.warning_counts)
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

    warning_table = Table(title="Warning Summary")
    warning_table.add_column("Category", style="yellow")
    warning_table.add_column("Count", justify="right")
    for category in sorted(WARNING_CATEGORIES):
        warning_table.add_row(category, str(warning_counts[category]))
    warning_table.add_row("TOTAL", str(sum(warning_counts.values())), style="bold")
    console.print()
    console.print(warning_table)

    budget_failed = False
    if args.warning_budget:
        try:
            budget = load_warning_budget(args.warning_budget)
        except ValueError as exc:
            console.print(f"\n[red]Warning budget error: {exc}[/red]")
            budget_failed = True
        else:
            differences = compare_warning_budget(warning_counts, budget)
            if differences:
                budget_failed = True
                console.print("\n[red]Warning budget mismatch:[/red]")
                for difference in differences:
                    console.print(f"  {difference}")
            else:
                console.print("\n[green]Warning budget matches the checked-in baseline.[/green]")

    if failed > 0 or budget_failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
