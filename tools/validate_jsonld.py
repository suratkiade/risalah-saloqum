#!/usr/bin/env python3
"""
Validate JSON-LD files for basic schema and release requirements.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS_URL = "https://github.com/suratkiade/risalah-saloqum"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require_field(data: dict, field: str, path: Path) -> None:
    if field not in data:
        raise SystemExit(f"{path}: missing required field '{field}'")


def has_doi_identifier(data: dict) -> bool:
    identifiers = data.get("identifier", [])
    for item in identifiers:
        if isinstance(item, dict) and item.get("propertyID") == "DOI" and item.get("value"):
            return True
    return False


def has_orcid_author(data: dict) -> bool:
    author = data.get("author", {})
    if isinstance(author, list):
        candidates = author
    else:
        candidates = [author]
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        identifiers = candidate.get("identifier", [])
        for item in identifiers:
            if isinstance(item, dict) and item.get("propertyID") == "ORCID" and item.get("value"):
                return True
        if candidate.get("sameAs") and any("orcid.org" in value for value in candidate.get("sameAs", [])):
            return True
    return False


def is_part_of_corpus(data: dict) -> bool:
    is_part_of = data.get("isPartOf", [])
    if isinstance(is_part_of, dict):
        is_part_of = [is_part_of]
    for item in is_part_of:
        if isinstance(item, dict) and item.get("@id") == CORPUS_URL:
            return True
    return False


def validate_release_jsonld(path: Path, data: dict) -> None:
    for field in ("@context", "@type", "name", "author", "datePublished", "inLanguage", "license", "identifier"):
        require_field(data, field, path)
    if not has_doi_identifier(data):
        raise SystemExit(f"{path}: missing DOI identifier")
    if not has_orcid_author(data):
        raise SystemExit(f"{path}: missing ORCID in author")
    if not is_part_of_corpus(data):
        raise SystemExit(f"{path}: isPartOf missing corpus reference")


def main() -> None:
    jsonld_files = sorted(ROOT.rglob("*.jsonld"))
    if not jsonld_files:
        raise SystemExit("No JSON-LD files found.")

    for path in jsonld_files:
        data = load_json(path)
        require_field(data, "@context", path)
        if "release/abstract.jsonld" in str(path):
            validate_release_jsonld(path, data)

    print(f"Validated {len(jsonld_files)} JSON-LD file(s).")


if __name__ == "__main__":
    main()
