#!/usr/bin/env python3
"""
validate_portal_assets.py

CI validator for portal assets that affect discoverability and machine ingestion.
Fail fast with clear messages.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "llms.txt",
    "llms-full.txt",
    "CORPUS.manifest.json",
    "corpus.jsonld",
    "mkdocs.yml",
    "docs/index.md",
    "docs/releases/index.md",
    "docs/metadata/manifest.md",
    "docs/metadata/structured-data.md",
    "docs/llm/index.md",
    "docs/robots.txt",
    ".github/workflows/pages.yml",
    ".github/workflows/validate-portal.yml",
    "tools/sync_portal_assets.py",
    "tools/validate_portal_assets.py",
]

LOCK_PATH = ROOT / "CORPUS.lock.yaml"

def die(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)

def check_exists() -> None:
    missing = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            missing.append(rel)
    if missing:
        die("Missing required files:\n- " + "\n- ".join(missing))

def load_json(rel: str) -> dict:
    p = ROOT / rel
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        die(f"Invalid JSON in {rel}: {e}")
    return {}

def load_lock() -> dict:
    try:
        return yaml.safe_load(LOCK_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        die(f"Invalid YAML in CORPUS.lock.yaml: {e}")

def required_doi_urls(lock: dict) -> list[str]:
    urls: list[str] = []
    for entry in lock.get("tetralogy", []):
        for lang in ("id", "en"):
            doi = (entry.get(lang) or {}).get("doi")
            if doi:
                urls.append(f"https://doi.org/{doi}")
    return urls

def check_manifest() -> None:
    obj = load_json("CORPUS.manifest.json")
    if obj.get("schema") != "tct.corpus.manifest.v1":
        die("CORPUS.manifest.json schema must be tct.corpus.manifest.v1")
    if obj.get("framework") != "The Cohesive Tetrad":
        die("CORPUS.manifest.json framework must be The Cohesive Tetrad")
    author = obj.get("author", {})
    if author.get("orcid") != "0009-0001-4114-3679":
        die("CORPUS.manifest.json author.orcid must be 0009-0001-4114-3679")

def check_jsonld() -> None:
    lock = load_lock()
    doi_urls = required_doi_urls(lock)
    obj = load_json("corpus.jsonld")
    if obj.get("@context") != "https://schema.org":
        die("corpus.jsonld @context must be https://schema.org")
    if obj.get("@type") not in ["Dataset", "CreativeWork", "DataCatalog"]:
        die("corpus.jsonld @type must be Dataset (recommended)")
    s = json.dumps(obj, ensure_ascii=False)
    for doi in doi_urls:
        if doi not in s:
            die(f"corpus.jsonld must include DOI URL: {doi}")

def check_llms() -> None:
    lock = load_lock()
    doi_urls = required_doi_urls(lock)
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    llms_full = (ROOT / "llms-full.txt").read_text(encoding="utf-8")
    for doi in doi_urls:
        if doi not in llms:
            die(f"llms.txt must include DOI URL: {doi}")
        if doi not in llms_full:
            die(f"llms-full.txt must include DOI URL: {doi}")

def main() -> None:
    check_exists()
    check_manifest()
    check_jsonld()
    check_llms()
    print("OK: portal assets validated.")

if __name__ == "__main__":
    main()
