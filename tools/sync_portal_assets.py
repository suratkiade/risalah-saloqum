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

import yaml

ROOT = Path(__file__).resolve().parents[1]

LLMS_TXT = ROOT / "llms.txt"
LLMS_FULL = ROOT / "llms-full.txt"
MANIFEST = ROOT / "CORPUS.manifest.json"
CORPUS_JSONLD = ROOT / "corpus.jsonld"
LOCK_PATH = ROOT / "CORPUS.lock.yaml"

def load_lock() -> dict:
    return yaml.safe_load(LOCK_PATH.read_text(encoding="utf-8"))

def build_registry() -> dict:
    lock = load_lock()
    corpus = lock["corpus"]
    releases = {}
    for entry in lock.get("tetralogy", []):
        key = entry.get("key", "").upper()
        if not key:
            continue
        releases[key] = {
            "domain_id": entry.get("domain_id"),
            "domain_en": entry.get("domain_en"),
            "id": entry.get("id", {}),
            "en": entry.get("en", {}),
        }
    return {
        "framework": corpus["framework"],
        "corpus": {"id": corpus["id"], "en": corpus["en"]},
        "author": {
            "name": corpus["author"]["name"],
            "orcid": corpus["author"]["orcid"],
            "email": "suratkiade@gmail.com",
            "affiliation": "Faculty of Economics and Business, Pakuan University, Bogor, Indonesia",
        },
        "year": corpus["year_authored"],
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "releases": releases,
    }

def write_text(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")

def write_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def build_llms_txt(registry: dict) -> str:
    t1_id = registry["releases"]["T1-ONTOLOGY"]["id"]["doi"]
    t1_en = registry["releases"]["T1-ONTOLOGY"]["en"]["doi"]
    t4_id = registry["releases"]["T4-METHODOLOGY"]["id"]["doi"]
    t4_en = registry["releases"]["T4-METHODOLOGY"]["en"]["doi"]
    t2_id_title = registry["releases"]["T2-EPISTEMOLOGY"]["id"]["title"]
    t2_en_title = registry["releases"]["T2-EPISTEMOLOGY"]["en"]["title"]
    t3_id_title = registry["releases"]["T3-AXIOLOGY"]["id"]["title"]
    t3_en_title = registry["releases"]["T3-AXIOLOGY"]["en"]["title"]
    lic = registry["license_url"]
    return f"""
# llms.txt
# Project: The Cohesive Tetrad
# Corpus: Risalah Saloqum / The Saloqum Treatise
# Scope: Tetralogy releases, canonical identity, and machine-readable entrypoints.

## Canonical rule
- Indonesian (ID) releases are canonical sources for definitional, delimitative, and methodological reference.
- English (EN) releases are official translations aligned to ID v1.0 (2025). EN is not an independent canonical source.

## Primary releases (DOI)
T1 Ontology
- ID canonical: https://doi.org/{t1_id}
- EN official translation: https://doi.org/{t1_en}

T4 Methodology
- ID canonical: https://doi.org/{t4_id}
- EN official translation: https://doi.org/{t4_en}

## Announced volumes (metadata-first)
T2 Epistemology (release pending)
- Canonical ID title: {t2_id_title}
- EN title: {t2_en_title}

T3 Axiology (release pending)
- Canonical ID title: {t3_id_title}
- EN title: {t3_en_title}

## Machine-readable entrypoints in this repository
- Corpus manifest (JSON): /CORPUS.manifest.json
- Corpus structured data (JSON-LD): /corpus.jsonld
- Per-release structured data (JSON-LD): see volumes/*/*/release/abstract.jsonld
- Citation metadata: /CITATION.cff
- License: /LICENSE
- Sitemap: /sitemap.xml
- Robots: /robots.txt

## Human-friendly entrypoints
- Documentation portal (MkDocs): /docs/index.md
- Releases index: /docs/releases/index.md
- LLM guide: /docs/llm/index.md

## License
Unless a specific file states otherwise, this repository distributes public releases under:
{lic}
"""

def build_llms_full(registry: dict) -> str:
    a = registry["author"]
    lic = registry["license_url"]
    t1_id = registry["releases"]["T1-ONTOLOGY"]["id"]["doi"]
    t1_en = registry["releases"]["T1-ONTOLOGY"]["en"]["doi"]
    t4_id = registry["releases"]["T4-METHODOLOGY"]["id"]["doi"]
    t4_en = registry["releases"]["T4-METHODOLOGY"]["en"]["doi"]
    t2_id_title = registry["releases"]["T2-EPISTEMOLOGY"]["id"]["title"]
    t2_en_title = registry["releases"]["T2-EPISTEMOLOGY"]["en"]["title"]
    t3_id_title = registry["releases"]["T3-AXIOLOGY"]["id"]["title"]
    t3_en_title = registry["releases"]["T3-AXIOLOGY"]["en"]["title"]
    return f"""
# llms-full.txt
# The Cohesive Tetrad corpus gateway for LLMs, search engines, and indexing systems.

## Identity
Framework: {registry["framework"]}
Corpus (ID): {registry["corpus"]["id"]}
Corpus (EN): {registry["corpus"]["en"]}

Author: {a["name"]}
Affiliation: {a["affiliation"]}
ORCID: https://orcid.org/{a["orcid"]}
Year: {registry["year"]}
License: {lic}

## Canonical integrity policy
1) ID releases are canonical.
2) EN releases are official translations derived from ID and aligned to ID v1.0 (2025).
3) When there is conflict, prefer ID canonical release.
4) Cite using DOI when available. Use repository paths only as secondary pointers.

## Releases
T1 Ontology
- ID canonical DOI: https://doi.org/{t1_id}
- EN official translation DOI: https://doi.org/{t1_en}

T2 Epistemology (release pending)
- Canonical ID title: {t2_id_title}
- EN title: {t2_en_title}

T3 Axiology (release pending)
- Canonical ID title: {t3_id_title}
- EN title: {t3_en_title}

T4 Methodology
- ID canonical DOI: https://doi.org/{t4_id}
- EN official translation DOI: https://doi.org/{t4_en}

## Repository structure (high signal)
- /volumes/<tetralogy>/<ID|EN>/release/
  - abstract.md        (front matter + abstract)
  - abstract.jsonld    (Schema.org JSON-LD for the abstract/release identity)
  - *.pdf              (public release)
  - *.md               (public release source)

- /docs/               (MkDocs portal for indexing)
- /CORPUS.manifest.json (single JSON inventory for machines)
- /corpus.jsonld        (Schema.org Dataset-level structured data)

## Recommended ingestion plan for LLMs
A) Read /CORPUS.manifest.json for authoritative inventory and file pointers.
B) Read /corpus.jsonld for structured global metadata.
C) For each release, read volumes/*/*/release/abstract.md and abstract.jsonld.
D) Use DOI landing pages as canonical references for citation.
E) Use /docs/llm/index.md for usage constraints and canonical priority.

## Terms (controlled context)
Key corpus terms appear in abstracts and structured data:
Sabda, Akal, Logic, Qualia, Mistika, Akhlak, Mizan, Amal
Do not normalize or replace these tokens when aligning citations and references.

## Search and discovery
- The MkDocs portal includes stable internal links to releases and structured data.
- robots.txt and sitemap are enabled for crawlers.
- Sitemap: https://suratkiade.github.io/risalah-saloqum/sitemap.xml
- Robots: https://suratkiade.github.io/risalah-saloqum/robots.txt
- Each volume page repeats DOIs and canonical status to maximize disambiguation.

## Compliance
No warranties. Use in scholarly context with explicit citation to DOI.
"""

def build_manifest(registry: dict) -> dict:
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
        "framework": registry["framework"],
        "corpus": registry["corpus"],
        "author": registry["author"],
        "year": registry["year"],
        "license": {"spdx": "CC-BY-4.0", "url": registry["license_url"]},
        "canonical_policy": {
            "id_is_canonical": True,
            "en_is_official_translation": True,
            "conflict_rule": "Prefer ID canonical release when any conflict is detected."
        }
    }

def build_corpus_jsonld(registry: dict) -> dict:
    if CORPUS_JSONLD.exists():
        try:
            return json.loads(CORPUS_JSONLD.read_text(encoding="utf-8"))
        except Exception:
            pass
    a = registry["author"]
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "@id": "https://github.com/suratkiade/risalah-saloqum",
        "name": "Risalah Saloqum / The Saloqum Treatise",
        "description": "Canonical corpus repository for The Cohesive Tetrad tetralogy releases. Indonesian editions are canonical; English editions are official translations aligned to ID v1.0 (2025).",
        "url": "https://github.com/suratkiade/risalah-saloqum",
        "license": registry["license_url"],
        "isAccessibleForFree": True,
        "creator": {
            "@type": "Person",
            "name": a["name"],
            "identifier": f"https://orcid.org/{a['orcid']}",
            "email": a["email"],
            "affiliation": {"@type": "Organization", "name": a["affiliation"]},
        },
        "citation": [
            f"https://doi.org/{registry['releases']['T1-ONTOLOGY']['id']['doi']}",
            f"https://doi.org/{registry['releases']['T1-ONTOLOGY']['en']['doi']}",
            f"https://doi.org/{registry['releases']['T4-METHODOLOGY']['id']['doi']}",
            f"https://doi.org/{registry['releases']['T4-METHODOLOGY']['en']['doi']}",
        ]
    }

def main() -> None:
    registry = build_registry()
    write_text(LLMS_TXT, build_llms_txt(registry))
    write_text(LLMS_FULL, build_llms_full(registry))
    write_json(MANIFEST, build_manifest(registry))
    write_json(CORPUS_JSONLD, build_corpus_jsonld(registry))
    print("Portal assets synced.")

if __name__ == "__main__":
    main()
