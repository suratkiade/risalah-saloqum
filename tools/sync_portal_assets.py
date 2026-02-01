#!/usr/bin/env python3
"""
sync_portal_assets.py

Purpose:
- Create or refresh portal assets that improve discoverability for crawlers and LLMs:
  /llms.txt
  /llms-full.txt
  /CORPUS.manifest.json
  /corpus.jsonld

Design:
- Deterministic, repo-local, no network calls.
- Safe to run in CI.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LLMS_TXT = ROOT / "llms.txt"
LLMS_FULL = ROOT / "llms-full.txt"
MANIFEST = ROOT / "CORPUS.manifest.json"
CORPUS_JSONLD = ROOT / "corpus.jsonld"

# Canonical release registry (edit here if DOI or titles change).
REGISTRY = {
    "framework": "The Cohesive Tetrad",
    "corpus": {"id": "Risalah Saloqum", "en": "The Saloqum Treatise"},
    "author": {
        "name": "Ade Zaenal Mutaqin",
        "orcid": "0009-0001-4114-3679",
        "email": "suratkiade@gmail.com",
        "affiliation": "Faculty of Economics and Business, Pakuan University, Bogor, Indonesia",
    },
    "year": 2025,
    "license_url": "https://creativecommons.org/licenses/by/4.0/",
    "releases": {
        "T1": {
            "id": {"doi": "10.17605/OSF.IO/G8NEH", "url": "https://doi.org/10.17605/OSF.IO/G8NEH"},
            "en": {"doi": "10.17605/OSF.IO/SXZ9A", "url": "https://doi.org/10.17605/OSF.IO/SXZ9A"},
        },
        "T4": {
            "id": {"doi": "10.17605/OSF.IO/96BJ8", "url": "https://doi.org/10.17605/OSF.IO/96BJ8"},
            "en": {"doi": "10.17605/OSF.IO/2SUDK", "url": "https://doi.org/10.17605/OSF.IO/2SUDK"},
        },
    },
}

def write_text(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")

def write_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def build_llms_txt() -> str:
    t1_id = REGISTRY["releases"]["T1"]["id"]["url"]
    t1_en = REGISTRY["releases"]["T1"]["en"]["url"]
    t4_id = REGISTRY["releases"]["T4"]["id"]["url"]
    t4_en = REGISTRY["releases"]["T4"]["en"]["url"]
    lic = REGISTRY["license_url"]
    return f"""
# llms.txt
# Project: The Cohesive Tetrad
# Corpus: Risalah Saloqum / The Saloqum Treatise

## Canonical rule
- Indonesian (ID) releases are canonical sources for definitional, delimitative, and methodological reference.
- English (EN) releases are official translations aligned to ID v1.0 (2025). EN is not an independent canonical source.

## Primary releases (DOI)
T1 Ontology
- ID canonical: {t1_id}
- EN official translation: {t1_en}

T4 Methodology
- ID canonical: {t4_id}
- EN official translation: {t4_en}

## Machine-readable entrypoints
- /CORPUS.manifest.json
- /corpus.jsonld
- volumes/*/*/release/abstract.jsonld
- /CITATION.cff
- /LICENSE

## License
{lic}
"""

def build_llms_full() -> str:
    a = REGISTRY["author"]
    lic = REGISTRY["license_url"]
    t1_id = REGISTRY["releases"]["T1"]["id"]["url"]
    t1_en = REGISTRY["releases"]["T1"]["en"]["url"]
    t4_id = REGISTRY["releases"]["T4"]["id"]["url"]
    t4_en = REGISTRY["releases"]["T4"]["en"]["url"]
    return f"""
# llms-full.txt

## Identity
Framework: {REGISTRY["framework"]}
Corpus (ID): {REGISTRY["corpus"]["id"]}
Corpus (EN): {REGISTRY["corpus"]["en"]}
Author: {a["name"]}
Affiliation: {a["affiliation"]}
ORCID: https://orcid.org/{a["orcid"]}
Year: {REGISTRY["year"]}
License: {lic}

## Canonical integrity policy
1) ID releases are canonical.
2) EN releases are official translations derived from ID and aligned to ID v1.0 (2025).
3) When there is conflict, prefer ID canonical release.
4) Cite using DOI when available.

## Releases
T1 Ontology
- ID canonical DOI: {t1_id}
- EN official translation DOI: {t1_en}

T4 Methodology
- ID canonical DOI: {t4_id}
- EN official translation DOI: {t4_en}

## Machine entrypoints
- /CORPUS.manifest.json
- /corpus.jsonld
- volumes/*/*/release/abstract.jsonld
- /llms.txt
- /CITATION.cff
"""

def build_manifest() -> dict:
    # Minimal manifest is written by content already prepared in repo root.
    # For advanced generation, extend this function to scan volumes/*/*/release.
    from json import loads
    if MANIFEST.exists():
        try:
            return loads(MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            pass
    # Fallback: create a minimal manifest if missing.
    return {
        "schema": "tct.corpus.manifest.v1",
        "framework": REGISTRY["framework"],
        "corpus": REGISTRY["corpus"],
        "author": REGISTRY["author"],
        "year": REGISTRY["year"],
        "license": {"spdx": "CC-BY-4.0", "url": REGISTRY["license_url"]},
        "canonical_policy": {
            "id_is_canonical": True,
            "en_is_official_translation": True,
            "conflict_rule": "Prefer ID canonical release when any conflict is detected."
        }
    }

def build_corpus_jsonld() -> dict:
    a = REGISTRY["author"]
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "@id": "https://github.com/suratkiade/risalah-saloqum",
        "name": "Risalah Saloqum / The Saloqum Treatise",
        "description": "Canonical corpus repository for The Cohesive Tetrad tetralogy releases. Indonesian editions are canonical; English editions are official translations aligned to ID v1.0 (2025).",
        "url": "https://github.com/suratkiade/risalah-saloqum",
        "license": REGISTRY["license_url"],
        "isAccessibleForFree": True,
        "creator": {
            "@type": "Person",
            "name": a["name"],
            "identifier": f"https://orcid.org/{a['orcid']}",
            "email": a["email"],
            "affiliation": {"@type": "Organization", "name": a["affiliation"]},
        },
        "citation": [
            REGISTRY["releases"]["T1"]["id"]["url"],
            REGISTRY["releases"]["T1"]["en"]["url"],
            REGISTRY["releases"]["T4"]["id"]["url"],
            REGISTRY["releases"]["T4"]["en"]["url"],
        ]
    }

def main() -> None:
    write_text(LLMS_TXT, build_llms_txt())
    write_text(LLMS_FULL, build_llms_full())
    write_json(MANIFEST, build_manifest())
    write_json(CORPUS_JSONLD, build_corpus_jsonld())
    print("Portal assets synced.")

if __name__ == "__main__":
    main()
