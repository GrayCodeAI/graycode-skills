"""Tests for the safe oversized-SKILL progressive-disclosure migration."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import migrate_oversized_skills as migration
from migrate_oversized_skills import (
    GENERATED_GLOB,
    MigrationError,
    apply_migration,
    main,
    plan_migration,
)

FRONTMATTER = (
    b"---\r\n"
    b"name: oversized-example\r\n"
    b"description: >-\r\n"
    b"  Preserve this frontmatter exactly.\r\n"
    b"license: MIT\r\n"
    b"---\r\n"
)


def _write_skill(root: Path, body: bytes, *, category: str = "general", name: str = "demo"):
    skill_dir = root / "categories" / category / name
    skill_dir.mkdir(parents=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_bytes(FRONTMATTER + body)
    return skill_file


def _many_lines(size: int) -> bytes:
    line = "A useful instruction with Unicode café and hawk 🦅.\n".encode()
    return line * (size // len(line) + 1)


def test_plan_preserves_frontmatter_and_body_round_trip(tmp_path: Path):
    body = b"# Overview\n\n" + _many_lines(2_200) + b"\n## Deployment\n\n" + _many_lines(2_200)
    skill_file = _write_skill(tmp_path, body)

    result = plan_migration(
        skill_file,
        skill_size_limit=2_000,
        reference_size_limit=900,
    )

    assert result.status == "planned"
    assert result.plan is not None
    assert result.plan.migrated_skill.startswith(FRONTMATTER)
    assert result.plan.migrated_skill[: len(FRONTMATTER)] == FRONTMATTER
    assert b"# Progressive disclosure index" in result.plan.migrated_skill
    assert b"Part 1: Overview" in result.plan.migrated_skill
    assert b"@ref(progressive-disclosure-part-001.md)" in result.plan.migrated_skill
    assert all(not line.endswith((b" ", b"\t")) for line in result.plan.migrated_skill.splitlines())
    assert b"".join(part.content for part in result.plan.parts) == body
    assert all(len(part.content) < 900 for part in result.plan.parts)
    assert all(part.content.decode("utf-8") for part in result.plan.parts)

    apply_migration(result.plan)
    assert skill_file.read_bytes()[: len(FRONTMATTER)] == FRONTMATTER
    assert b"".join(part.path.read_bytes() for part in result.plan.parts) == body
    assert set(migration._declared_references(skill_file.read_bytes())) == {
        part.path.name for part in result.plan.parts
    }


def test_planning_is_deterministic_and_does_not_split_a_line_that_fits(tmp_path: Path):
    unique_line = ("λ" * 300 + " END-OF-INDIVISIBLE-LINE\n").encode()
    body = _many_lines(1_500) + unique_line + _many_lines(1_500)
    skill_file = _write_skill(tmp_path, body)

    first = plan_migration(
        skill_file,
        skill_size_limit=2_000,
        reference_size_limit=800,
    )
    second = plan_migration(
        skill_file,
        skill_size_limit=2_000,
        reference_size_limit=800,
    )

    assert first == second
    assert first.plan is not None
    assert sum(unique_line in part.content for part in first.plan.parts) == 1
    assert not any(
        b"END-OF-INDIVISIBLE-LINE" in part.content and unique_line not in part.content
        for part in first.plan.parts
    )


def test_long_ascii_word_hard_splits_below_limit_with_exact_round_trip():
    content = b"a" * 250

    chunks = migration.split_oversized_line(content, size_limit=100)

    assert tuple(map(len, chunks)) == (99, 99, 52)
    assert b"".join(chunks) == content


def test_long_unicode_line_splits_only_at_codepoint_boundaries():
    content = ("🦅" * 100).encode("utf-8")

    chunks = migration.split_oversized_line(content, size_limit=102)

    assert len(chunks) > 1
    assert all(len(chunk) < 102 for chunk in chunks)
    assert all(chunk.decode("utf-8") for chunk in chunks)
    assert b"".join(chunks) == content


def test_long_line_prefers_latest_whitespace_boundary():
    content = b"a" * 60 + b" " + b"b" * 50

    chunks = migration.split_oversized_line(content, size_limit=100)

    assert chunks == (b"a" * 60 + b" ", b"b" * 50)
    assert b"".join(chunks) == content


def test_long_unicode_line_migration_is_idempotent_and_exact(tmp_path: Path):
    body = b"# Large line\n" + ("λ" * 1_400).encode("utf-8") + b"\nTail\n"
    skill_file = _write_skill(tmp_path, body)

    result = plan_migration(
        skill_file,
        skill_size_limit=2_000,
        reference_size_limit=500,
    )

    assert result.plan is not None
    assert b"".join(part.content for part in result.plan.parts) == body
    assert all(len(part.content) < 500 for part in result.plan.parts)
    assert all(part.content.decode("utf-8") for part in result.plan.parts)
    apply_migration(result.plan)
    repeated = plan_migration(
        skill_file,
        skill_size_limit=2_000,
        reference_size_limit=500,
    )
    assert repeated.status == "already-migrated"


def test_default_parts_leave_five_kib_headroom(tmp_path: Path):
    body = _many_lines(230_000)
    skill_file = _write_skill(tmp_path, body)

    result = plan_migration(skill_file)

    assert result.plan is not None
    assert len(result.plan.parts) >= 3
    assert all(
        len(part.content) < migration.REFERENCE_SIZE_LIMIT_BYTES for part in result.plan.parts
    )
    assert migration.REFERENCE_SIZE_LIMIT_BYTES == 95 * 1024
    assert len(result.plan.migrated_skill) < migration.SKILL_SIZE_LIMIT_BYTES


def test_fenced_code_block_is_never_split(tmp_path: Path):
    fence = b"```python\n" + (b"print('do not split me')\n" * 24) + b"```\n"
    body = _many_lines(1_200) + fence + _many_lines(1_200)
    skill_file = _write_skill(tmp_path, body)

    result = plan_migration(
        skill_file,
        skill_size_limit=2_000,
        reference_size_limit=800,
    )

    assert result.plan is not None
    containing_parts = [part for part in result.plan.parts if fence in part.content]
    assert len(containing_parts) == 1
    assert not any(
        b"```python" in part.content and fence not in part.content for part in result.plan.parts
    )


def test_indivisible_oversized_fence_fails_safely(tmp_path: Path):
    body = b"```text\n" + b"x\n" * 400 + b"```\n"
    skill_file = _write_skill(tmp_path, body)
    original = skill_file.read_bytes()

    with pytest.raises(MigrationError, match="indivisible fenced code block"):
        plan_migration(
            skill_file,
            skill_size_limit=500,
            reference_size_limit=500,
        )

    assert skill_file.read_bytes() == original
    assert not (skill_file.parent / "references").exists()


def test_preexisting_generated_name_is_a_conflict_even_below_limit(tmp_path: Path):
    skill_file = _write_skill(tmp_path, b"# Short\n")
    references = skill_file.parent / "references"
    references.mkdir()
    conflict = references / "progressive-disclosure-part-001.md"
    conflict.write_text("user-owned content\n", encoding="utf-8")

    with pytest.raises(MigrationError, match="conflicting generated reference"):
        plan_migration(skill_file)

    assert conflict.read_text(encoding="utf-8") == "user-owned content\n"


def test_unrelated_existing_reference_is_preserved(tmp_path: Path):
    body = _many_lines(4_000) + b"@ref(api.md)\n"
    skill_file = _write_skill(tmp_path, body)
    references = skill_file.parent / "references"
    references.mkdir()
    existing = references / "api.md"
    existing.write_text("existing\n", encoding="utf-8")

    result = plan_migration(
        skill_file,
        skill_size_limit=2_000,
        reference_size_limit=900,
    )
    assert result.plan is not None
    apply_migration(result.plan)

    assert existing.read_text(encoding="utf-8") == "existing\n"
    assert b"## Existing supporting references" in skill_file.read_bytes()
    assert b"@ref(api.md)" in skill_file.read_bytes()
    actual_refs = {path.name for path in references.iterdir() if path.is_file()}
    assert set(migration._declared_references(skill_file.read_bytes())) == actual_refs


def test_reference_mismatch_fails_before_writing(tmp_path: Path):
    skill_file = _write_skill(tmp_path, _many_lines(4_000) + b"@ref(missing.md)\n")

    with pytest.raises(MigrationError, match="missing declared references"):
        plan_migration(
            skill_file,
            skill_size_limit=2_000,
            reference_size_limit=900,
        )

    assert not (skill_file.parent / "references").exists()


def test_cli_is_dry_run_by_default(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    skill_file = _write_skill(tmp_path, _many_lines(120_000))
    original = skill_file.read_bytes()

    assert main([str(skill_file)]) == 0

    output = capsys.readouterr().out
    assert "DRY-RUN planned" in output
    assert "would be written" in output
    assert skill_file.read_bytes() == original
    assert not (skill_file.parent / "references").exists()


def test_explicit_write_is_idempotent(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    skill_file = _write_skill(tmp_path, _many_lines(120_000))

    assert main([str(skill_file), "--write"]) == 0
    first_skill = skill_file.read_bytes()
    first_parts = {
        path.name: path.read_bytes()
        for path in sorted((skill_file.parent / "references").glob(GENERATED_GLOB))
    }
    assert first_parts

    assert main([str(skill_file), "--write"]) == 0
    second_output = capsys.readouterr().out

    assert "already-migrated" in second_output
    assert "wrote 0 migration(s)" in second_output
    assert skill_file.read_bytes() == first_skill
    assert {
        path.name: path.read_bytes()
        for path in sorted((skill_file.parent / "references").glob(GENERATED_GLOB))
    } == first_parts


def test_modified_generated_part_is_rejected(tmp_path: Path):
    skill_file = _write_skill(tmp_path, _many_lines(4_000))
    result = plan_migration(
        skill_file,
        skill_size_limit=2_000,
        reference_size_limit=900,
    )
    assert result.plan is not None
    apply_migration(result.plan)
    result.plan.parts[0].path.write_bytes(b"tampered\n")

    with pytest.raises(MigrationError, match="checksum"):
        plan_migration(
            skill_file,
            skill_size_limit=2_000,
            reference_size_limit=900,
        )


def test_modified_generated_index_is_rejected(tmp_path: Path):
    skill_file = _write_skill(tmp_path, _many_lines(4_000))
    result = plan_migration(
        skill_file,
        skill_size_limit=2_000,
        reference_size_limit=900,
    )
    assert result.plan is not None
    apply_migration(result.plan)
    skill_file.write_bytes(skill_file.read_bytes().replace(b"Detailed instructions", b"Changed"))

    with pytest.raises(MigrationError, match="index no longer matches"):
        plan_migration(
            skill_file,
            skill_size_limit=2_000,
            reference_size_limit=900,
        )


def test_apply_rolls_back_parts_if_skill_publish_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    skill_file = _write_skill(tmp_path, _many_lines(4_000))
    original = skill_file.read_bytes()
    result = plan_migration(
        skill_file,
        skill_size_limit=2_000,
        reference_size_limit=900,
    )
    assert result.plan is not None
    real_replace = os.replace

    def fail_skill_publish(source: Path, target: Path):
        if Path(target) == skill_file.resolve():
            raise OSError("simulated publish failure")
        real_replace(source, target)

    monkeypatch.setattr(migration.os, "replace", fail_skill_publish)

    with pytest.raises(OSError, match="simulated publish failure"):
        apply_migration(result.plan)

    assert skill_file.read_bytes() == original
    assert not tuple(skill_file.parent.glob("references/*"))
    assert not tuple(skill_file.parent.rglob("*.tmp"))


def test_all_discovers_skills_in_deterministic_order(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    first = _write_skill(tmp_path, b"# Small\n", category="z-last", name="small")
    second = _write_skill(
        tmp_path,
        _many_lines(120_000),
        category="a-first",
        name="large",
    )
    monkeypatch.setattr(migration, "CATEGORIES_DIR", tmp_path / "categories")

    assert main(["--all"]) == 0

    lines = [line for line in capsys.readouterr().out.splitlines() if line.startswith("DRY-RUN")]
    assert str(second.resolve()) in lines[0]
    assert str(first.resolve()) in lines[1]
    assert "planned" in lines[0]
    assert "within-limit" in lines[1]
    assert not (second.parent / "references").exists()


def test_all_reports_every_blocker_and_never_partially_writes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    missing_ref = _write_skill(
        tmp_path,
        b"x" * 110_000 + b"\n@ref(missing.md)\n",
        category="a-first",
        name="missing-ref",
    )
    oversized_fence = _write_skill(
        tmp_path,
        b"```text\n" + b"x" * 110_000 + b"\n```\n",
        category="b-second",
        name="large-fence",
    )
    originals = {path: path.read_bytes() for path in (missing_ref, oversized_fence)}
    monkeypatch.setattr(migration, "CATEGORIES_DIR", tmp_path / "categories")

    assert main(["--all"]) == 1

    captured = capsys.readouterr()
    assert captured.err.count("DRY-RUN blocked:") == 2
    assert "missing declared references: missing.md" in captured.err
    assert "indivisible fenced code block" in captured.err
    assert "preflight failed: 2 blocker(s); no migrations were written" in captured.err
    assert all(path.read_bytes() == original for path, original in originals.items())
    assert not tuple(tmp_path.rglob("progressive-disclosure-part-*.md"))


def test_invalid_utf8_is_rejected_without_writes(tmp_path: Path):
    skill_file = _write_skill(tmp_path, b"# Body\n")
    skill_file.write_bytes(FRONTMATTER + b"\xff\xfe")

    with pytest.raises(MigrationError, match="not valid UTF-8"):
        plan_migration(skill_file, skill_size_limit=1)

    assert not (skill_file.parent / "references").exists()


def test_frontmatter_without_final_line_ending_fails_instead_of_changing_it(tmp_path: Path):
    skill_dir = tmp_path / "skill"
    skill_dir.mkdir()
    skill_file = skill_dir / "SKILL.md"
    original = b"---\nname: demo\ndescription: demo\n---"
    skill_file.write_bytes(original)

    with pytest.raises(MigrationError, match="byte-for-byte identical"):
        plan_migration(skill_file, skill_size_limit=1)

    assert skill_file.read_bytes() == original
