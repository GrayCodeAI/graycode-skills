from __future__ import annotations

import os
from pathlib import Path

import pytest
from cleanup_internal_references import apply_cleanup, plan_cleanup
from validate_skill import validate_skill


def write_skill(root: Path, body: str) -> Path:
    skill = root / "test-skill"
    skill.mkdir()
    (skill / "SKILL.md").write_bytes(
        (
            "---\r\n"
            "name: test-skill\r\n"
            "description: '[frontmatter](missing.md)'\r\n"
            "license: MIT\r\n"
            "tags: [testing]\r\n"
            "---\r\n" + body
        ).encode()
    )
    return skill


def test_cleanup_preserves_frontmatter_code_and_readable_labels(tmp_path: Path):
    skill = write_skill(
        tmp_path,
        'Read [the guide](missing.md "title") and ![diagram](missing.png).\r\n'
        "Remove ![](gone.png). Keep [valid](exists.md), [web](https://example.com), "
        "[anchor](#part), and `[example](missing.md)`.\r\n"
        "```markdown\r\n[fenced](missing.md)\r\n```\r\n",
    )
    (skill / "exists.md").write_text("valid\n", encoding="utf-8")
    before = (skill / "SKILL.md").read_bytes()

    changes = plan_cleanup([skill])

    assert len(changes) == 1
    assert changes[0].broken == 3
    assert changes[0].traversal == 0
    assert changes[0].updated.startswith(before[: before.index(b"---\r\n", 4) + 5])
    apply_cleanup(changes)
    content = (skill / "SKILL.md").read_bytes().decode()
    assert "description: '[frontmatter](missing.md)'" in content
    assert "Read the guide and diagram." in content
    assert "Remove ." in content
    assert "[valid](exists.md)" in content
    assert "[web](https://example.com)" in content
    assert "[anchor](#part)" in content
    assert "`[example](missing.md)`" in content
    assert "[fenced](missing.md)" in content


def test_cleanup_handles_nested_sources_exact_case_and_traversal(tmp_path: Path):
    skill = write_skill(tmp_path, "# Test\n")
    references = skill / "references"
    references.mkdir()
    (references / "Guide.md").write_text("# Guide\n", encoding="utf-8")
    index = references / "index.md"
    index.write_text(
        "[wrong case](guide.md) [outside](../../outside.md) [skill](../SKILL.md)\n",
        encoding="utf-8",
    )

    changes = plan_cleanup([skill])

    assert [(change.broken, change.traversal) for change in changes] == [(1, 1)]
    apply_cleanup(changes)
    assert index.read_text(encoding="utf-8") == ("wrong case outside [skill](../SKILL.md)\n")
    result = validate_skill(skill)
    assert result.warning_counts["broken-internal-reference"] == 0
    assert result.warning_counts["path-traversal"] == 0
    assert plan_cleanup([skill]) == []


def test_cleanup_refuses_markdown_source_symlink_escape(tmp_path: Path):
    skill = write_skill(tmp_path, "# Test\n")
    outside = tmp_path / "outside.md"
    outside.write_text("[missing](missing.md)\n", encoding="utf-8")
    references = skill / "references"
    references.mkdir()
    try:
        (references / "outside.md").symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"symlinks unavailable: {exc}")

    with pytest.raises(ValueError, match="resolves outside"):
        plan_cleanup([skill])


def test_apply_rejects_concurrent_change_without_overwrite(tmp_path: Path):
    skill = write_skill(tmp_path, "[missing](missing.md)\n")
    changes = plan_cleanup([skill])
    skill_md = skill / "SKILL.md"
    concurrent = skill_md.read_bytes() + b"concurrent\n"
    skill_md.write_bytes(concurrent)

    with pytest.raises(RuntimeError, match="concurrently changed"):
        apply_cleanup(changes)

    assert skill_md.read_bytes() == concurrent


def test_cleanup_preserves_executable_mode(tmp_path: Path):
    skill = write_skill(tmp_path, "[missing](missing.md)\n")
    skill_md = skill / "SKILL.md"
    os.chmod(skill_md, 0o754)

    changes = plan_cleanup([skill])
    apply_cleanup(changes)

    assert skill_md.stat().st_mode & 0o777 == 0o754
