#!/usr/bin/env python3
"""Dependency-free sanity tests for the 21amG workflow package foundation."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schema" / "workflow-package.schema.json"
MANIFEST_PATH = ROOT / "templates" / "workflow-package" / "manifest.json"
INDUSTRIES_PATH = ROOT / "catalog" / "industries.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    manifest = load_json(MANIFEST_PATH)
    catalog = load_json(INDUSTRIES_PATH)

    assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    assert schema.get("$id", "").startswith("urn:21amg:")
    version_pattern = re.compile(schema["properties"]["version"]["pattern"])

    for valid in ("0.1.0", "1.2.3", "1.2.3-beta.1", "1.2.3+build.4"):
        assert version_pattern.fullmatch(valid), f"Valid version rejected: {valid}"
    for invalid in ("01.2.3", "1.2", "v1.2.3", "1.2.3-"):
        assert not version_pattern.fullmatch(invalid), f"Invalid version accepted: {invalid}"

    required = schema["required"]
    missing = sorted(set(required) - set(manifest))
    assert not missing, f"Template missing required fields: {missing}"
    assert manifest["lifecycle"] == "proposed", "Template must not claim implementation"
    assert manifest["validation"]["status"] == "not-run", "Template must not claim tests passed"
    assert manifest["distribution"]["license_id"] == "UNDECIDED", "Do not silently choose a release license"

    entries = catalog if isinstance(catalog, list) else catalog.get("industries", [])
    ids = [entry["id"] for entry in entries]
    assert entries, "Industry catalog is empty"
    assert len(ids) == len(set(ids)), "Duplicate industry IDs found"
    for industry_id in ids:
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", industry_id), (
            f"Invalid industry ID: {industry_id}"
        )

    print(
        "Shortcut Library sanity checks passed: "
        f"{len(ids)} industries, {len(required)} required manifest fields, "
        "semantic-version positive/negative cases."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Shortcut Library sanity checks failed: {error}", file=sys.stderr)
        raise SystemExit(1)
