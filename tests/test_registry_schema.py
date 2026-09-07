"""Tests for tools/registry_schema.py - JSON schema validation for registry entries."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from registry_schema import (
    SchemaError,
    load_and_validate_registry,
    validate_registry,
    validate_registry_entry,
)

# ---------------------------------------------------------------------------
# SchemaError
# ---------------------------------------------------------------------------


class TestSchemaError:
    def test_repr(self):
        err = SchemaError("$.name", "missing")
        assert "name" in repr(err)
        assert "missing" in repr(err)

    def test_equality(self):
        a = SchemaError("$.x", "msg")
        b = SchemaError("$.x", "msg")
        c = SchemaError("$.x", "other")
        assert a == b
        assert a != c
        assert a != "not a SchemaError"


# ---------------------------------------------------------------------------
# validate_registry_entry - valid entries
# ---------------------------------------------------------------------------


class TestValidEntries:
    def test_minimal_valid_entry(self):
        entry = {
            "name": "my-skill",
            "description": "Does things",
            "category": "python",
            "path": "categories/python/my-skill",
        }
        errors = validate_registry_entry(entry)
        assert errors == []

    def test_full_valid_entry(self):
        entry = {
            "name": "my-skill",
            "description": "Does things",
            "category": "python",
            "tags": ["python", "ml"],
            "path": "categories/python/my-skill",
            "file_count": 5,
            "has_scripts": True,
        }
        errors = validate_registry_entry(entry)
        assert errors == []

    def test_entry_with_provenance_fields(self):
        # Optional provenance metadata must validate without being required.
        entry = {
            "name": "my-skill",
            "description": "Does things",
            "category": "python",
            "path": "categories/python/my-skill",
            "source": "https://github.com/example/skills",
            "source_ref": "v1.2.0",
            "source_commit": "abc1234",
            "license": "Apache-2.0",
        }
        errors = validate_registry_entry(entry)
        assert errors == []

    def test_unknown_field_still_rejected(self):
        # additionalProperties:false must still reject typos / stray keys.
        entry = {
            "name": "my-skill",
            "description": "Does things",
            "category": "python",
            "path": "categories/python/my-skill",
            "sourceee": "typo",
        }
        errors = validate_registry_entry(entry)
        assert errors != []


# ---------------------------------------------------------------------------
# validate_registry_entry - missing required fields
# ---------------------------------------------------------------------------


class TestMissingFields:
    def test_missing_name(self):
        entry = {"description": "x", "category": "a", "path": "p"}
        errors = validate_registry_entry(entry)
        assert any("name" in e.message for e in errors)

    def test_missing_description(self):
        entry = {"name": "x", "category": "a", "path": "p"}
        errors = validate_registry_entry(entry)
        assert any("description" in e.message for e in errors)

    def test_missing_category(self):
        entry = {"name": "x", "description": "d", "path": "p"}
        errors = validate_registry_entry(entry)
        assert any("category" in e.message for e in errors)

    def test_missing_path(self):
        entry = {"name": "x", "description": "d", "category": "a"}
        errors = validate_registry_entry(entry)
        assert any("path" in e.message for e in errors)

    def test_empty_object(self):
        errors = validate_registry_entry({})
        assert len(errors) >= 4  # all four required fields


# ---------------------------------------------------------------------------
# validate_registry_entry - wrong types
# ---------------------------------------------------------------------------


class TestWrongTypes:
    def test_name_not_string(self):
        entry = {"name": 123, "description": "d", "category": "a", "path": "p"}
        errors = validate_registry_entry(entry)
        assert any("string" in e.message for e in errors)

    def test_tags_not_array(self):
        entry = {
            "name": "x",
            "description": "d",
            "category": "a",
            "path": "p",
            "tags": "not-a-list",
        }
        errors = validate_registry_entry(entry)
        assert any("array" in e.message for e in errors)

    def test_file_count_not_integer(self):
        entry = {
            "name": "x",
            "description": "d",
            "category": "a",
            "path": "p",
            "file_count": "five",
        }
        errors = validate_registry_entry(entry)
        assert any("integer" in e.message for e in errors)

    def test_has_scripts_not_boolean(self):
        entry = {
            "name": "x",
            "description": "d",
            "category": "a",
            "path": "p",
            "has_scripts": "yes",
        }
        errors = validate_registry_entry(entry)
        assert any("boolean" in e.message for e in errors)

    def test_category_pattern_violation(self):
        entry = {"name": "x", "description": "d", "category": "Bad Category!", "path": "p"}
        errors = validate_registry_entry(entry)
        assert any("pattern" in e.message for e in errors)


# ---------------------------------------------------------------------------
# validate_registry_entry - additional properties
# ---------------------------------------------------------------------------


class TestAdditionalProperties:
    def test_extra_field_rejected(self):
        entry = {
            "name": "x",
            "description": "d",
            "category": "a",
            "path": "p",
            "unknown_field": "oops",
        }
        errors = validate_registry_entry(entry)
        assert any("unexpected" in e.message for e in errors)


# ---------------------------------------------------------------------------
# validate_registry_entry - edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_name(self):
        entry = {"name": "", "description": "d", "category": "a", "path": "p"}
        errors = validate_registry_entry(entry)
        assert any("minLength" in e.message for e in errors)

    def test_empty_path(self):
        entry = {"name": "x", "description": "d", "category": "a", "path": ""}
        errors = validate_registry_entry(entry)
        assert any("minLength" in e.message for e in errors)

    def test_negative_file_count(self):
        entry = {
            "name": "x",
            "description": "d",
            "category": "a",
            "path": "p",
            "file_count": -1,
        }
        errors = validate_registry_entry(entry)
        assert any("minimum" in e.message for e in errors)

    def test_zero_file_count_ok(self):
        entry = {
            "name": "x",
            "description": "d",
            "category": "a",
            "path": "p",
            "file_count": 0,
        }
        errors = validate_registry_entry(entry)
        assert errors == []

    def test_tags_with_empty_strings(self):
        """Tags that are empty strings should still pass schema (content validation
        is handled elsewhere), but the items type check passes."""
        entry = {
            "name": "x",
            "description": "d",
            "category": "a",
            "path": "p",
            "tags": ["", "valid"],
        }
        errors = validate_registry_entry(entry)
        # Schema only checks that items are strings, not their content
        assert errors == []


# ---------------------------------------------------------------------------
# validate_registry (full registry)
# ---------------------------------------------------------------------------


class TestValidateRegistry:
    """The registry document is {version, skills[]} - the shape graycode-cli
    parses in internal/plugin/registry.go."""

    def test_valid_registry(self):
        data = {
            "version": 1,
            "skills": [
                {"name": "a", "description": "d", "category": "c", "path": "p"},
                {"name": "b", "description": "d", "category": "c", "path": "p"},
            ],
        }
        errors = validate_registry(data)
        assert errors == []

    def test_empty_registry(self):
        errors = validate_registry({"version": 1, "skills": []})
        assert errors == []

    def test_not_an_object(self):
        errors = validate_registry([{"name": "x"}])
        assert any("object" in e.message for e in errors)

    def test_missing_skills_key(self):
        errors = validate_registry({"version": 1})
        assert any("skills" in e.message for e in errors)

    def test_invalid_entry_in_list(self):
        data = {
            "version": 1,
            "skills": [
                {"name": "good", "description": "d", "category": "c", "path": "p"},
                {"name": 123},  # bad entry
            ],
        }
        errors = validate_registry(data)
        assert len(errors) > 0
        # Should reference the second entry
        assert any("[1]" in e.path for e in errors)

    def test_multiple_errors_across_entries(self):
        data = {
            "version": 1,
            "skills": [
                {},  # missing all required
                {"name": "x"},  # missing some required
            ],
        }
        errors = validate_registry(data)
        assert len(errors) >= 5  # at least 4 from first + some from second


# ---------------------------------------------------------------------------
# load_and_validate_registry
# ---------------------------------------------------------------------------


class TestLoadAndValidateRegistry:
    def test_load_valid_file(self, tmp_path: Path):
        data = {
            "version": 1,
            "skills": [{"name": "x", "description": "d", "category": "c", "path": "p"}],
        }
        path = tmp_path / "registry.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        result, errors = load_and_validate_registry(path)
        assert result == data
        assert errors == []

    def test_file_not_found(self, tmp_path: Path):
        path = tmp_path / "nonexistent.json"
        result, errors = load_and_validate_registry(path)
        assert result is None
        assert any("not found" in e.message for e in errors)

    def test_invalid_json(self, tmp_path: Path):
        path = tmp_path / "bad.json"
        path.write_text("{not valid json", encoding="utf-8")
        result, errors = load_and_validate_registry(path)
        assert result is None
        assert any("invalid JSON" in e.message for e in errors)

    def test_invalid_schema(self, tmp_path: Path):
        data = {"version": 1, "skills": [{"name": 123}]}  # wrong type
        path = tmp_path / "registry.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        result, errors = load_and_validate_registry(path)
        assert result is not None
        assert len(errors) > 0
