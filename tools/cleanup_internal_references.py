#!/usr/bin/env python3
"""Remove dead local Markdown links without changing their readable content.

The validator treats local inline links as portable skill dependencies.  This
tool uses the same parser and path rules to de-link references that are missing
or escape their skill directory.  It is a dry run unless ``--write`` is given.
"""

from __future__ import annotations

import argparse
import os
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

# Allow direct execution from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from frontmatter import parse_frontmatter
from skill_discovery import iter_skills
from validate_skill import (
    CATEGORIES_DIR,
    _find_label_end,
    _inline_link_destination,
    _is_escaped,
    _local_link_path,
    _markdown_source_paths,
    _mask_fenced_code,
    _mask_inline_code,
    path_exists_with_exact_case,
)


@dataclass(frozen=True)
class LinkSpan:
    """Offsets and source text for one real inline Markdown link."""

    start: int
    end: int
    label: str
    target: str
    is_image: bool


@dataclass(frozen=True)
class FileChange:
    """One fully planned, byte-preserving file replacement."""

    path: Path
    original: bytes
    updated: bytes
    mode: int
    broken: int
    traversal: int


def iter_inline_link_spans(markdown: str):
    """Yield link spans using exactly the validator's Markdown parser."""
    visible = _mask_inline_code(_mask_fenced_code(markdown))
    position = 0
    while position < len(visible):
        label_start = visible.find("[", position)
        if label_start < 0:
            return
        if _is_escaped(visible, label_start):
            position = label_start + 1
            continue

        label_end = _find_label_end(visible, label_start)
        if label_end is None or label_end + 1 >= len(visible):
            position = label_start + 1
            continue
        if visible[label_end + 1] != "(":
            position = label_start + 1
            continue

        parsed = _inline_link_destination(visible, label_end + 1)
        if parsed is None:
            position = label_end + 1
            continue
        destination_start, destination_end, link_end = parsed

        is_image = (
            label_start > 0
            and visible[label_start - 1] == "!"
            and not _is_escaped(visible, label_start - 1)
        )
        start = label_start - 1 if is_image else label_start
        yield LinkSpan(
            start=start,
            end=link_end,
            label=markdown[label_start + 1 : label_end],
            target=markdown[destination_start:destination_end],
            is_image=is_image,
        )
        position = link_end


def _body_offset(content: str) -> int:
    """Return the exact body offset when valid frontmatter is present."""
    frontmatter, _body = parse_frontmatter(content)
    if frontmatter is None:
        return 0

    offset = 0
    for index, line in enumerate(content.splitlines(keepends=True)):
        offset += len(line)
        if index > 0 and line.strip() == "---":
            return offset
    return 0


def _replacement(span: LinkSpan) -> str:
    """Preserve readable label/alt text while removing dead link syntax."""
    if span.is_image and not span.label.strip():
        return ""
    return span.label


def _plan_source(source: Path, skill_root: Path) -> FileChange | None:
    original = source.read_bytes()
    content = original.decode("utf-8")
    body_offset = _body_offset(content)
    body = content[body_offset:]

    edits: list[tuple[int, int, str]] = []
    broken = 0
    traversal = 0
    for span in iter_inline_link_spans(body):
        local_path = _local_link_path(span.target)
        if local_path is None:
            continue
        try:
            target = (source.parent / local_path).resolve()
        except (OSError, RuntimeError):
            traversal += 1
        else:
            if not target.is_relative_to(skill_root):
                traversal += 1
            elif path_exists_with_exact_case(target, skill_root):
                continue
            else:
                broken += 1
        edits.append(
            (
                body_offset + span.start,
                body_offset + span.end,
                _replacement(span),
            )
        )

    if not edits:
        return None

    updated = content
    for start, end, replacement in reversed(edits):
        updated = updated[:start] + replacement + updated[end:]
    return FileChange(
        path=source,
        original=original,
        updated=updated.encode("utf-8"),
        mode=stat.S_IMODE(source.stat().st_mode),
        broken=broken,
        traversal=traversal,
    )


def plan_cleanup(skill_paths: list[Path]) -> list[FileChange]:
    """Plan all changes before touching disk; reject unsafe Markdown sources."""
    changes: list[FileChange] = []
    for skill_path in sorted(skill_paths, key=lambda path: path.as_posix()):
        skill_root = skill_path.resolve()
        for source in _markdown_source_paths(skill_path):
            resolved_source = source.resolve()
            if not resolved_source.is_relative_to(skill_root):
                relative = source.relative_to(skill_path).as_posix()
                raise ValueError(
                    f"{skill_path}: {relative} resolves outside the skill directory; "
                    "remove the unsafe symlink manually"
                )
            change = _plan_source(source, skill_root)
            if change is not None:
                changes.append(change)
    return changes


def _atomic_replace(path: Path, content: bytes, mode: int) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def apply_cleanup(changes: list[FileChange]) -> None:
    """Apply a preflighted batch and roll it back if any replacement fails."""
    for change in changes:
        if change.path.read_bytes() != change.original:
            raise RuntimeError(f"refusing to overwrite concurrently changed file: {change.path}")

    applied: list[FileChange] = []
    try:
        for change in changes:
            _atomic_replace(change.path, change.updated, change.mode)
            applied.append(change)
    except Exception:
        for change in reversed(applied):
            _atomic_replace(change.path, change.original, change.mode)
        raise


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="clean every discovered skill")
    parser.add_argument("paths", nargs="*", type=Path, help="skill directories to clean")
    parser.add_argument("--write", action="store_true", help="apply the planned changes")
    args = parser.parse_args()
    if args.all == bool(args.paths):
        parser.error("provide either --all or one or more skill directories")
    return args


def main() -> int:
    args = _parse_args()
    if args.all:
        skill_paths = list(iter_skills(CATEGORIES_DIR))
    else:
        skill_paths = [path.resolve() for path in args.paths]
        invalid = [path for path in skill_paths if not (path / "SKILL.md").is_file()]
        if invalid:
            raise ValueError(f"not a skill directory: {invalid[0]}")

    changes = plan_cleanup(skill_paths)
    broken = sum(change.broken for change in changes)
    traversal = sum(change.traversal for change in changes)
    action = "cleaned" if args.write else "would clean"
    if args.write:
        apply_cleanup(changes)
    print(
        f"{action} {len(changes)} Markdown files: "
        f"{broken} broken references, {traversal} traversal references"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
