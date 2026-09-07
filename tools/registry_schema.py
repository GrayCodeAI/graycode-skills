#!/usr/bin/env python3
"""JSON schema validation for graycode-skills registry entries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "registry.json"

# --- Schema definition ---

REGISTRY_ENTRY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["name", "description", "category", "path"],
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120,
            # Deliberately permissive (existing entries use snake_case and
            # mixed case), but forbids path separators and whitespace so a
            # malicious or malformed name can never be used to escape a
            # filesystem path built from it downstream (e.g. package
            # archive naming).
            "pattern": r"^[^/\\\s]+$",
            "description": "Human-readable skill name",
        },
        "description": {
            "type": "string",
            "description": "Short description of the skill",
        },
        "category": {
            "type": "string",
            "pattern": "^[a-z][a-z0-9-]*$",
            "description": "Category slug (lowercase, hyphens)",
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of tag strings",
        },
        "path": {
            "type": "string",
            "minLength": 1,
            "description": "Relative path to the skill directory",
        },
        "file_count": {
            "type": "integer",
            "minimum": 0,
            "description": "Number of files in the skill",
        },
        "has_scripts": {
            "type": "boolean",
            "description": "Whether the skill has a scripts/ directory",
        },
        # --- Optional provenance fields ---
        # This registry is largely a bulk ingestion of third-party skills.
        # These fields record where an ingested skill came from so the registry
        # is auditable and offline-reproducible. They are optional: existing
        # first-party entries omit them.
        "source": {
            "type": "string",
            "description": "Upstream source URL the skill was ingested from",
        },
        "source_ref": {
            "type": "string",
            "description": "Upstream version/tag/branch the skill was taken at",
        },
        "source_commit": {
            "type": "string",
            "description": "Upstream commit SHA the skill was taken at",
        },
        "license": {
            "type": "string",
            "description": "SPDX license identifier of the ingested skill",
        },
        "repo": {
            "type": "string",
            "description": "GitHub owner/repo slug the skill is installed from",
        },
    },
    "additionalProperties": False,
}

REGISTRY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "version": {"type": "integer"},
        "skills": {"type": "array", "items": REGISTRY_ENTRY_SCHEMA},
    },
    "required": ["version", "skills"],
    "additionalProperties": False,
}


# --- Pure-Python validator (no jsonschema dependency) ---


class SchemaError:
    """A single validation error."""

    def __init__(self, path: str, message: str):
        self.path = path
        self.message = message

    def __repr__(self) -> str:
        return f"SchemaError({self.path!r}, {self.message!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SchemaError):
            return NotImplemented
        return self.path == other.path and self.message == other.message


def _validate_type(value: Any, expected: str, path: str) -> list[SchemaError]:
    """Check that *value* matches the JSON-schema type name."""
    type_map = {
        "string": str,
        "integer": int,
        "boolean": bool,
        "array": list,
        "object": dict,
    }
    py_type = type_map.get(expected)
    if py_type is None:
        return []
    # bool is a subclass of int, so check bool first
    if expected == "boolean":
        if not isinstance(value, bool):
            return [SchemaError(path, f"expected boolean, got {type(value).__name__}")]
    elif expected == "integer":
        if isinstance(value, bool) or not isinstance(value, int):
            return [SchemaError(path, f"expected integer, got {type(value).__name__}")]
    elif not isinstance(value, py_type):
        return [SchemaError(path, f"expected {expected}, got {type(value).__name__}")]
    return []


def _validate_string(value: str, schema: dict, path: str) -> list[SchemaError]:
    errors: list[SchemaError] = []
    min_len = schema.get("minLength")
    if min_len is not None and len(value) < min_len:
        errors.append(SchemaError(path, f"string length {len(value)} < minLength {min_len}"))
    pattern = schema.get("pattern")
    if pattern is not None:
        import re

        if not re.search(pattern, value):
            errors.append(SchemaError(path, f"value '{value}' does not match pattern '{pattern}'"))
    return errors


def _validate_array(value: list, schema: dict, path: str) -> list[SchemaError]:
    errors: list[SchemaError] = []
    items_schema = schema.get("items")
    if items_schema:
        for i, item in enumerate(value):
            errors.extend(_validate_value(item, items_schema, f"{path}[{i}]"))
    return errors


def _validate_object(value: dict, schema: dict, path: str) -> list[SchemaError]:
    errors: list[SchemaError] = []
    props = schema.get("properties", {})
    required = schema.get("required", [])
    additional = schema.get("additionalProperties", True)

    # Required fields
    for field in required:
        if field not in value:
            errors.append(SchemaError(f"{path}.{field}", f"missing required field '{field}'"))

    # Validate each present property
    for key, val in value.items():
        child_path = f"{path}.{key}"
        if key in props:
            errors.extend(_validate_value(val, props[key], child_path))
        elif additional is False:
            errors.append(SchemaError(child_path, f"unexpected field '{key}'"))

    return errors


def _validate_value(value: Any, schema: dict, path: str) -> list[SchemaError]:
    """Recursively validate a single value against its schema node."""
    errors: list[SchemaError] = []

    # Type check
    expected_type = schema.get("type")
    if expected_type:
        errors.extend(_validate_type(value, expected_type, path))
        if errors:
            return errors  # stop early on type mismatch

    # Type-specific checks
    if expected_type == "string" and isinstance(value, str):
        errors.extend(_validate_string(value, schema, path))
    elif expected_type == "integer" and isinstance(value, int) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        if minimum is not None and value < minimum:
            errors.append(SchemaError(path, f"value {value} < minimum {minimum}"))
    elif expected_type == "array" and isinstance(value, list):
        errors.extend(_validate_array(value, schema, path))
    elif expected_type == "object" and isinstance(value, dict):
        errors.extend(_validate_object(value, schema, path))

    return errors


def validate_registry_entry(entry: Any, path: str = "$") -> list[SchemaError]:
    """Validate a single registry entry dict against the schema."""
    return _validate_value(entry, REGISTRY_ENTRY_SCHEMA, path)


def validate_registry(data: Any) -> list[SchemaError]:
    """Validate the full registry document ({version, skills[]})."""
    return _validate_value(data, REGISTRY_SCHEMA, "$")


def load_and_validate_registry(
    registry_path: Path | None = None,
) -> tuple[dict | None, list[SchemaError]]:
    """Load registry.json and validate it. Returns (data_or_None, errors)."""
    path = registry_path or REGISTRY_PATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [SchemaError("$", f"registry file not found: {path}")]
    except json.JSONDecodeError as exc:
        return None, [SchemaError("$", f"invalid JSON: {exc}")]
    errors = validate_registry(data)
    return data, errors
