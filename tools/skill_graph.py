#!/usr/bin/env python3
"""Project the public community-skill registry as a portable graph document."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from update_registry import REPO_ROOT, build_registry, validate_entries

DEFAULT_OUTPUT = REPO_ROOT / "skill-graph.json"
SCHEMA_VERSION = "community-skills.graph/v1"
PRODUCER = "starling"


def _stable_id(prefix: str, *parts: str) -> str:
    value = "\x00".join(parts).encode("utf-8")
    return f"{prefix}/{hashlib.sha256(value).hexdigest()[:24]}"


def _provenance(
    version: str,
    source_id: Optional[str] = None,  # noqa: UP045 -- project supports Python 3.9
) -> dict[str, str]:
    value = {"producer": PRODUCER, "version": version}
    if source_id:
        value["source_id"] = source_id
    return value


def _node(
    node_id: str,
    kind: str,
    created_at: str,
    version: str,
    attributes: dict[str, str],
    source_id: Optional[str] = None,  # noqa: UP045 -- project supports Python 3.9
) -> dict[str, Any]:
    return {
        "id": node_id,
        "kind": kind,
        "created_at": created_at,
        "provenance": _provenance(version, source_id),
        "attributes": attributes,
    }


def _edge(
    kind: str,
    from_id: str,
    from_kind: str,
    to_id: str,
    to_kind: str,
    created_at: str,
    version: str,
) -> dict[str, Any]:
    return {
        "id": _stable_id("edge", kind, from_id, to_id),
        "kind": kind,
        "from": {"kind": from_kind, "id": from_id},
        "to": {"kind": to_kind, "id": to_id},
        "created_at": created_at,
        "provenance": _provenance(version),
    }


def build_skill_graph(
    entries: list[dict[str, Any]],
    *,
    generated_at: str,
    version: str,
    limit: int = 0,
) -> dict[str, Any]:
    """Build a deterministic graph projection from validated registry entries.

    A zero limit means all entries. A positive limit selects the first entries
    after the registry's canonical case-insensitive name ordering.
    """
    if limit < 0:
        raise ValueError("limit must be zero or greater")

    violations = validate_entries(entries)
    if violations:
        raise ValueError("invalid registry entries: " + "; ".join(violations))

    selected = sorted(entries, key=lambda entry: entry["name"].lower())
    if limit:
        selected = selected[:limit]

    canonical_input = json.dumps(
        selected, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    query_sha256 = hashlib.sha256(canonical_input).hexdigest()

    root_id = _stable_id("system", "community-skill-registry")
    nodes = [
        _node(
            root_id,
            "system",
            generated_at,
            version,
            {
                "name": "Community Skill Registry",
                "projection": "category-skill-tag",
                "skill_count": str(len(selected)),
            },
        )
    ]
    edges: list[dict[str, Any]] = []

    categories = sorted({entry["category"] for entry in selected})
    tags = sorted(
        {
            tag
            for entry in selected
            for tag in entry.get("tags", [])
            if isinstance(tag, str) and tag
        },
        key=str.lower,
    )

    category_ids: dict[str, str] = {}
    for category in categories:
        category_id = _stable_id("knowledge", "category", category)
        category_ids[category] = category_id
        nodes.append(
            _node(
                category_id,
                "knowledge",
                generated_at,
                version,
                {"entity": "category", "name": category},
            )
        )
        edges.append(
            _edge(
                "contains",
                root_id,
                "system",
                category_id,
                "knowledge",
                generated_at,
                version,
            )
        )

    tag_ids: dict[str, str] = {}
    for tag in tags:
        tag_id = _stable_id("knowledge", "tag", tag)
        tag_ids[tag] = tag_id
        nodes.append(
            _node(
                tag_id,
                "knowledge",
                generated_at,
                version,
                {"entity": "tag", "name": tag},
            )
        )
        edges.append(
            _edge(
                "contains",
                root_id,
                "system",
                tag_id,
                "knowledge",
                generated_at,
                version,
            )
        )

    for entry in selected:
        skill_id = _stable_id("knowledge", "skill", entry["name"])
        nodes.append(
            _node(
                skill_id,
                "knowledge",
                generated_at,
                version,
                {
                    "entity": "skill",
                    "name": entry["name"],
                    "description": entry["description"],
                    "path": entry["path"],
                    "file_count": str(entry.get("file_count", 0)),
                    "has_scripts": str(bool(entry.get("has_scripts", False))).lower(),
                },
                entry["path"],
            )
        )
        edges.append(
            _edge(
                "contains",
                category_ids[entry["category"]],
                "knowledge",
                skill_id,
                "knowledge",
                generated_at,
                version,
            )
        )
        for tag in sorted(
            (tag for tag in entry.get("tags", []) if tag in tag_ids),
            key=str.lower,
        ):
            edges.append(
                _edge(
                    "references",
                    skill_id,
                    "knowledge",
                    tag_ids[tag],
                    "knowledge",
                    generated_at,
                    version,
                )
            )

    event = {
        "id": _stable_id("event", "observed", root_id, query_sha256),
        "type": "observed",
        "subject": {"kind": "system", "id": root_id},
        "occurred_at": generated_at,
        "idempotency_key": query_sha256,
        "provenance": _provenance(version),
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "query_sha256": query_sha256,
        "nodes": nodes,
        "edges": edges,
        "events": [event],
    }


def main(argv: Optional[list[str]] = None) -> int:  # noqa: UP045 -- Python 3.9
    parser = argparse.ArgumentParser(
        description="Project the community skill registry as a portable graph"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="output path (default: skill-graph.json)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="maximum skills to project; zero includes the full registry",
    )
    parser.add_argument(
        "--generated-at",
        help="UTC RFC3339 timestamp; defaults to the current time",
    )
    args = parser.parse_args(argv)

    generated_at = args.generated_at or datetime.now(timezone.utc).isoformat().replace(
        "+00:00", "Z"
    )
    version = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    graph = build_skill_graph(
        build_registry(),
        generated_at=generated_at,
        version=version,
        limit=args.limit,
    )
    args.output.write_text(
        json.dumps(graph, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {args.output}: {len(graph['nodes'])} nodes, "
        f"{len(graph['edges'])} edges, {len(graph['events'])} event"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
