#!/usr/bin/env python3
"""Move oversized SKILL.md bodies into progressive-disclosure references.

The command is deliberately a dry-run unless ``--write`` is supplied.  It
preserves the YAML frontmatter bytes exactly and stores the original Markdown
body, without additions or normalization, across ordered reference files.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
import sys
import tempfile
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from frontmatter import parse_frontmatter
from skill_discovery import CATEGORIES_DIR, iter_skills

SKILL_SIZE_LIMIT_BYTES = 100 * 1024
REFERENCE_SIZE_LIMIT_BYTES = 95 * 1024
GENERATED_PREFIX = "progressive-disclosure-part-"
GENERATED_GLOB = f"{GENERATED_PREFIX}*.md"
MARKER_NAME = "hawk-progressive-disclosure"
MARKER_PREFIX = f"<!-- {MARKER_NAME}:".encode()
MARKER_RE = re.compile(
    rb"\A<!-- hawk-progressive-disclosure:v1 "
    rb"body-sha256=([0-9a-f]{64}) parts=([1-9][0-9]*) -->\r?\n"
)
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*(?:\r?\n)?$")
REFERENCE_RE = re.compile(rb"@ref\(([^)\r\n]+)\)")
LINE_BREAK_RE = re.compile(r"\r\n|[\n\v\f\r\x1c-\x1e\x85\u2028\u2029]")


class MigrationError(RuntimeError):
    """A migration could not be planned or committed without data loss."""


@dataclass(frozen=True)
class MarkdownBlock:
    """A Markdown block and its one-based source line range."""

    content: bytes
    first_line: int
    last_line: int
    fenced: bool


@dataclass(frozen=True)
class ReferencePart:
    """One generated reference file."""

    path: Path
    content: bytes
    first_line: int
    last_line: int


@dataclass(frozen=True)
class MigrationPlan:
    """A fully preflighted, deterministic migration."""

    skill_file: Path
    original: bytes
    migrated_skill: bytes
    parts: tuple[ReferencePart, ...]


@dataclass(frozen=True)
class PlanResult:
    """Planning result for a single skill."""

    skill_file: Path
    status: str
    detail: str
    plan: Optional[MigrationPlan] = None  # noqa: UP045 - project supports Python 3.9


def _line_without_ending(line: bytes) -> bytes:
    return line.rstrip(b"\r\n")


def _split_frontmatter(content: bytes) -> tuple[bytes, bytes]:
    """Return the exact frontmatter prefix and exact Markdown body."""
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MigrationError(f"SKILL.md is not valid UTF-8: {exc}") from exc

    parsed, _ = parse_frontmatter(text)
    if parsed is None:
        raise MigrationError("SKILL.md has no valid YAML frontmatter")

    lines = content.splitlines(keepends=True)
    if not lines or _line_without_ending(lines[0]) != b"---":
        raise MigrationError("SKILL.md frontmatter must start with an exact '---' line")

    for index, line in enumerate(lines[1:], start=1):
        if _line_without_ending(line) == b"---":
            end = sum(len(item) for item in lines[: index + 1])
            return content[:end], content[end:]
    raise MigrationError("SKILL.md frontmatter has no closing '---' line")


def _closing_fence(line: str, marker: str, minimum: int) -> bool:
    pattern = rf"^ {{0,3}}{re.escape(marker)}{{{minimum},}}[ \t]*(?:\r?\n)?$"
    return re.match(pattern, line) is not None


def markdown_blocks(body: bytes) -> tuple[MarkdownBlock, ...]:
    """Tokenize a body into ordinary lines and indivisible fenced blocks."""
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MigrationError(f"SKILL.md body is not valid UTF-8: {exc}") from exc

    lines = text.splitlines(keepends=True)
    if not lines and text:
        lines = [text]

    blocks: list[MarkdownBlock] = []
    index = 0
    while index < len(lines):
        line_number = index + 1
        opener = FENCE_OPEN_RE.match(lines[index])
        if opener is None:
            blocks.append(
                MarkdownBlock(lines[index].encode("utf-8"), line_number, line_number, False)
            )
            index += 1
            continue

        marker_run = opener.group(1)
        marker = marker_run[0]
        fence_lines = [lines[index]]
        index += 1
        while index < len(lines):
            fence_lines.append(lines[index])
            is_close = _closing_fence(lines[index], marker, len(marker_run))
            index += 1
            if is_close:
                break
        blocks.append(
            MarkdownBlock(
                "".join(fence_lines).encode("utf-8"),
                line_number,
                index,
                True,
            )
        )

    if b"".join(block.content for block in blocks) != body:
        raise MigrationError("internal error: Markdown tokenization changed the body")
    return tuple(blocks)


def split_oversized_line(content: bytes, *, size_limit: int) -> tuple[bytes, ...]:
    """Split one non-fenced line below size_limit at valid UTF-8 boundaries.

    The latest whitespace boundary that fits is preferred. If the available
    prefix contains no whitespace, the split falls back to the latest complete
    UTF-8 codepoint. Concatenating the returned chunks always recreates content
    byte-for-byte.
    """
    if size_limit < 2:
        raise MigrationError("size limit must be at least 2 bytes")
    try:
        content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MigrationError(f"Markdown line is not valid UTF-8: {exc}") from exc
    if len(content) < size_limit:
        return (content,)

    maximum = size_limit - 1
    remaining = content
    chunks: list[bytes] = []
    while len(remaining) >= size_limit:
        # Ignoring only an incomplete trailing codepoint yields the largest
        # valid UTF-8 prefix within the strict byte limit.
        prefix_text = remaining[:maximum].decode("utf-8", errors="ignore")
        prefix = prefix_text.encode("utf-8")
        if not prefix:
            raise MigrationError(
                f"a single UTF-8 codepoint cannot fit below the {size_limit}-byte limit"
            )

        whitespace_end = 0
        byte_offset = 0
        for character in prefix_text:
            byte_offset += len(character.encode("utf-8"))
            if character.isspace():
                whitespace_end = byte_offset
        split_at = whitespace_end or len(prefix)
        chunks.append(remaining[:split_at])
        remaining = remaining[split_at:]
    if remaining:
        chunks.append(remaining)

    if b"".join(chunks) != content:
        raise MigrationError("internal error: splitting a long line changed its bytes")
    if any(len(chunk) >= size_limit for chunk in chunks):
        raise MigrationError("internal error: a split line chunk still exceeds the size limit")
    return tuple(chunks)


def _pack_parts(skill_dir: Path, body: bytes, *, size_limit: int) -> tuple[ReferencePart, ...]:
    if size_limit < 2:
        raise MigrationError("size limit must be at least 2 bytes")

    source_blocks = markdown_blocks(body)
    blocks: list[MarkdownBlock] = []
    for block in source_blocks:
        if len(block.content) < size_limit:
            blocks.append(block)
            continue
        if block.fenced:
            raise MigrationError(
                f"indivisible fenced code block at lines {block.first_line}-{block.last_line} "
                f"is {len(block.content)} bytes; it must be smaller than {size_limit} bytes"
            )
        blocks.extend(
            MarkdownBlock(chunk, block.first_line, block.last_line, False)
            for chunk in split_oversized_line(block.content, size_limit=size_limit)
        )

    if not blocks:
        raise MigrationError("oversized SKILL.md unexpectedly has an empty body")

    packed: list[tuple[bytes, int, int]] = []
    current: list[MarkdownBlock] = []
    current_size = 0
    for block in blocks:
        block_size = len(block.content)
        if current and current_size + block_size >= size_limit:
            packed.append(
                (
                    b"".join(item.content for item in current),
                    current[0].first_line,
                    current[-1].last_line,
                )
            )
            current = []
            current_size = 0
        current.append(block)
        current_size += block_size

    if current:
        packed.append(
            (
                b"".join(item.content for item in current),
                current[0].first_line,
                current[-1].last_line,
            )
        )

    references = skill_dir / "references"
    parts = tuple(
        ReferencePart(
            references / f"{GENERATED_PREFIX}{index:03d}.md",
            content,
            first_line,
            last_line,
        )
        for index, (content, first_line, last_line) in enumerate(packed, start=1)
    )
    if b"".join(part.content for part in parts) != body:
        raise MigrationError("internal error: reference parts do not reconstruct the body")
    return parts


def _headings(content: bytes, *, maximum: int = 2) -> tuple[str, ...]:
    """Extract a few headings outside fenced blocks for a useful route label."""
    headings: list[str] = []
    in_fence: Optional[tuple[str, int]] = None  # noqa: UP045 - Python 3.9
    for line in content.decode("utf-8").splitlines(keepends=True):
        if in_fence is not None:
            if _closing_fence(line, in_fence[0], in_fence[1]):
                in_fence = None
            continue
        opener = FENCE_OPEN_RE.match(line)
        if opener is not None:
            run = opener.group(1)
            in_fence = (run[0], len(run))
            continue
        heading = HEADING_RE.match(line)
        if heading is not None:
            label = heading.group(2).strip()
            if label:
                headings.append(label.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]"))
                if len(headings) == maximum:
                    break
    return tuple(headings)


def _declared_references(body: bytes) -> tuple[str, ...]:
    """Return source reference declarations once each, retaining source order."""
    names: list[str] = []
    seen: set[str] = set()
    for match in REFERENCE_RE.finditer(body):
        name = match.group(1).decode("utf-8")
        if name not in seen:
            seen.add(name)
            names.append(name)
    return tuple(names)


def _index_body(
    parts: tuple[ReferencePart, ...], body_hash: str, source_refs: tuple[str, ...]
) -> bytes:
    lines = [
        f"<!-- {MARKER_NAME}:v1 body-sha256={body_hash} parts={len(parts)} -->",
        "",
        "# Progressive disclosure index",
        "",
        "The complete skill instructions are preserved in the ordered references below.",
        "Open the part whose headings match the current task; read all parts in order when",
        "the task spans sections or requires the complete procedure.",
        "",
        "## Detailed instructions",
        "",
    ]
    for index, part in enumerate(parts, start=1):
        route = " → ".join(_headings(part.content)) or "continued instructions"
        relative = part.path.relative_to(part.path.parent.parent).as_posix()
        lines.append(
            f"- [Part {index}: {route}]({relative}) — original lines "
            f"{part.first_line}–{part.last_line} — @ref({part.path.name})"
        )
    if source_refs:
        lines.extend(["", "## Existing supporting references", ""])
        lines.extend(f"- @ref({name})" for name in source_refs)
    lines.append("")
    return "\n".join(lines).encode("utf-8")


def _generated_paths(skill_file: Path) -> tuple[Path, ...]:
    references = skill_file.parent / "references"
    if not references.exists():
        return ()
    if references.is_symlink() or not references.is_dir():
        raise MigrationError(f"references path is not a regular directory: {references}")
    return tuple(sorted(references.glob(GENERATED_GLOB)))


def _validate_source_references(skill_file: Path, body: bytes) -> tuple[str, ...]:
    """Ensure moving declarations out of SKILL.md cannot orphan existing refs."""
    declared = _declared_references(body)
    references = skill_file.parent / "references"
    actual: list[str] = []
    if references.exists():
        if references.is_symlink() or not references.is_dir():
            raise MigrationError(f"references path is not a regular directory: {references}")
        for path in sorted(references.iterdir()):
            if path.is_symlink():
                raise MigrationError(f"reference must not be a symbolic link: {path}")
            if path.is_file() and not path.match(GENERATED_GLOB):
                actual.append(path.name)

    missing = sorted(set(declared) - set(actual))
    orphaned = sorted(set(actual) - set(declared))
    if missing or orphaned:
        details: list[str] = []
        if missing:
            details.append(f"missing declared references: {', '.join(missing)}")
        if orphaned:
            details.append(f"orphaned reference files: {', '.join(orphaned)}")
        raise MigrationError("; ".join(details))
    return declared


def _validate_existing_migration(
    skill_file: Path,
    frontmatter: bytes,
    body: bytes,
    *,
    skill_size_limit: int,
    reference_size_limit: int,
) -> None:
    marker = MARKER_RE.match(body)
    if marker is None:
        raise MigrationError("generated migration marker is malformed")

    expected_hash = marker.group(1).decode("ascii")
    part_count = int(marker.group(2))
    expected_paths = tuple(
        skill_file.parent / "references" / f"{GENERATED_PREFIX}{index:03d}.md"
        for index in range(1, part_count + 1)
    )
    actual_paths = _generated_paths(skill_file)
    if actual_paths != expected_paths:
        raise MigrationError(
            "generated reference set does not match the migration index; refusing to overwrite it"
        )

    contents: list[bytes] = []
    for path in expected_paths:
        if path.is_symlink() or not path.is_file():
            raise MigrationError(f"generated reference is not a regular file: {path}")
        content = path.read_bytes()
        if len(content) >= reference_size_limit:
            raise MigrationError(
                f"generated reference is {len(content)} bytes, not smaller than "
                f"{reference_size_limit}: {path}"
            )
        try:
            content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise MigrationError(f"generated reference is not valid UTF-8: {path}") from exc
        contents.append(content)

    reconstructed = b"".join(contents)
    actual_hash = hashlib.sha256(reconstructed).hexdigest()
    if actual_hash != expected_hash:
        raise MigrationError(
            "generated references no longer match the source-body checksum; refusing to overwrite them"
        )
    first_line = 1
    indexed_parts: list[ReferencePart] = []
    for path, content in zip(expected_paths, contents):
        text = content.decode("utf-8")
        line_breaks = tuple(LINE_BREAK_RE.finditer(text))
        ends_with_line_break = bool(line_breaks and line_breaks[-1].end() == len(text))
        last_line = first_line + len(line_breaks) - int(ends_with_line_break)
        indexed_parts.append(ReferencePart(path, content, first_line, last_line))
        first_line += len(line_breaks)
    source_refs = _validate_source_references(skill_file, reconstructed)
    expected_body = _index_body(tuple(indexed_parts), expected_hash, source_refs)
    if body != expected_body:
        raise MigrationError(
            "generated SKILL.md index no longer matches its reference set; refusing to overwrite it"
        )
    if len(frontmatter + body) >= skill_size_limit:
        raise MigrationError(f"generated SKILL.md is not smaller than {skill_size_limit} bytes")


def plan_migration(
    skill: Path,
    *,
    skill_size_limit: int = SKILL_SIZE_LIMIT_BYTES,
    reference_size_limit: int = REFERENCE_SIZE_LIMIT_BYTES,
) -> PlanResult:
    """Preflight one skill without changing the filesystem."""
    if skill.is_symlink():
        raise MigrationError(f"skill path must not be a symbolic link: {skill}")
    skill_file = skill / "SKILL.md" if skill.is_dir() else skill
    if skill_file.name != "SKILL.md":
        raise MigrationError(f"expected a skill directory or SKILL.md path: {skill}")
    if skill_file.is_symlink():
        raise MigrationError(f"SKILL.md must not be a symbolic link: {skill_file}")
    skill_file = skill_file.resolve()
    if not skill_file.is_file():
        raise MigrationError(f"SKILL.md is not a regular file: {skill_file}")

    original = skill_file.read_bytes()
    frontmatter, body = _split_frontmatter(original)
    if not frontmatter.endswith(b"\n"):
        raise MigrationError(
            "frontmatter closing delimiter has no line ending; refusing to add one because "
            "frontmatter must remain byte-for-byte identical"
        )

    if body.startswith(MARKER_PREFIX):
        _validate_existing_migration(
            skill_file,
            frontmatter,
            body,
            skill_size_limit=skill_size_limit,
            reference_size_limit=reference_size_limit,
        )
        return PlanResult(
            skill_file,
            "already-migrated",
            "generated references are complete and match their checksum",
        )

    conflicts = _generated_paths(skill_file)
    if conflicts:
        rendered = ", ".join(str(path) for path in conflicts)
        raise MigrationError(f"conflicting generated reference files already exist: {rendered}")

    if len(original) < skill_size_limit:
        return PlanResult(
            skill_file,
            "within-limit",
            f"{len(original)} bytes is already smaller than {skill_size_limit}",
        )

    source_refs = _validate_source_references(skill_file, body)
    parts = _pack_parts(skill_file.parent, body, size_limit=reference_size_limit)
    body_hash = hashlib.sha256(body).hexdigest()
    migrated_skill = frontmatter + _index_body(parts, body_hash, source_refs)
    if len(migrated_skill) >= skill_size_limit:
        raise MigrationError(
            f"generated SKILL.md would be {len(migrated_skill)} bytes; frontmatter and index "
            f"must together be smaller than {skill_size_limit} bytes"
        )
    return PlanResult(
        skill_file,
        "planned",
        f"{len(original)} bytes -> {len(migrated_skill)} bytes plus {len(parts)} references",
        MigrationPlan(skill_file, original, migrated_skill, parts),
    )


def _stage_file(path: Path, content: bytes, *, mode: int) -> Path:
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    staged = Path(name)
    descriptor_open = True
    try:
        os.fchmod(descriptor, mode)
        stream = os.fdopen(descriptor, "wb")
        descriptor_open = False
        with stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        if descriptor_open:
            os.close(descriptor)
        staged.unlink(missing_ok=True)
        raise
    return staged


def apply_migration(plan: MigrationPlan) -> None:
    """Atomically replace each file, publishing SKILL.md only after its parts."""
    skill_file = plan.skill_file
    if skill_file.read_bytes() != plan.original:
        raise MigrationError(f"SKILL.md changed after planning: {skill_file}")
    if _generated_paths(skill_file):
        raise MigrationError("generated reference files appeared after planning")

    references = skill_file.parent / "references"
    if references.exists() and (references.is_symlink() or not references.is_dir()):
        raise MigrationError(f"references path is not a regular directory: {references}")
    created_references = not references.exists()
    references.mkdir(mode=0o755, exist_ok=True)

    staged: list[tuple[Path, Path]] = []
    published_parts: list[Path] = []
    skill_mode = stat.S_IMODE(skill_file.stat().st_mode)
    try:
        if _generated_paths(skill_file):
            raise MigrationError("generated reference files appeared while staging")
        for part in plan.parts:
            staged.append((part.path, _stage_file(part.path, part.content, mode=0o644)))
        staged_skill = _stage_file(skill_file, plan.migrated_skill, mode=skill_mode)
        staged.append((skill_file, staged_skill))

        if skill_file.read_bytes() != plan.original:
            raise MigrationError(f"SKILL.md changed while staging: {skill_file}")
        if _generated_paths(skill_file):
            raise MigrationError("generated reference files appeared before commit")

        for target, temporary in staged[:-1]:
            # A hard-link publishes the fully staged file atomically and, unlike
            # replace(), fails if a conflicting path appears after preflight.
            os.link(temporary, target)
            published_parts.append(target)
            temporary.unlink()
        os.replace(staged[-1][1], skill_file)
    except BaseException:
        for path in published_parts:
            with suppress(OSError):
                path.unlink()
        raise
    finally:
        for _, temporary in staged:
            temporary.unlink(missing_ok=True)
        if created_references:
            with suppress(OSError):
                references.rmdir()


def _selected_skills(
    skill: Optional[str],  # noqa: UP045 - project supports Python 3.9
    all_skills: bool,
) -> tuple[Path, ...]:
    if all_skills:
        return tuple(path / "SKILL.md" for path in iter_skills(CATEGORIES_DIR))
    if skill is None:
        raise MigrationError("provide one skill path or --all")
    return (Path(skill),)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Split oversized SKILL.md bodies into ordered progressive-disclosure references "
            "(dry-run by default)"
        )
    )
    parser.add_argument("skill", nargs="?", help="skill directory or SKILL.md path")
    parser.add_argument("--all", action="store_true", help="inspect every discovered skill")
    parser.add_argument(
        "--write",
        action="store_true",
        help="apply all successfully preflighted migrations",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:  # noqa: UP045 - Python 3.9
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.all and args.skill:
        parser.error("skill and --all are mutually exclusive")
    if not args.all and not args.skill:
        parser.error("provide one skill path or --all")

    selected = _selected_skills(args.skill, args.all)
    results: list[PlanResult] = []
    failures: list[tuple[Path, str]] = []
    for path in selected:
        try:
            results.append(plan_migration(path))
        except (MigrationError, UnicodeDecodeError, OSError) as exc:
            failures.append((path, str(exc)))

    planned = tuple(result.plan for result in results if result.plan is not None)
    action = "WRITE" if args.write else "DRY-RUN"
    for result in results:
        print(f"{action} {result.status}: {result.skill_file}: {result.detail}")

    for path, detail in failures:
        print(f"{action} blocked: {path}: {detail}", file=sys.stderr)

    if failures:
        print(
            f"preflight failed: {len(failures)} blocker(s); no migrations were written",
            file=sys.stderr,
        )
        return 1

    if args.write:
        try:
            for plan in planned:
                apply_migration(plan)
        except (MigrationError, OSError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(f"wrote {len(planned)} migration(s)")
    else:
        print(f"dry-run complete: {len(planned)} migration(s) would be written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
