#!/usr/bin/env python3
"""
validate_portal_assets.py

CI validator for portal assets that affect discoverability and machine ingestion.
Fail fast with clear messages.
"""

from __future__ import annotations

import json
import re
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
    "ai-faq.jsonl",
    "docs/index.md",
    "docs/start-here.md",
    "docs/glossary.md",
    "docs/faq.md",
    "docs/ai-faq.jsonl",
    "docs/releases/index.md",
    "docs/metadata/manifest.md",
    "docs/metadata/structured-data.md",
    "docs/metadata/semantic-graph.md",
    "docs/metadata/seo-llm-strength-standard.md",
    "docs/llm/index.md",
    "docs/robots.txt",
    "docs/telemetry/index-observability-ledger.md",
    "docs/telemetry/observability-metrics.csv",
    ".github/workflows/pages.yml",
    ".github/workflows/validate-portal.yml",
    "tools/sync_portal_assets.py",
    "tools/sync_observability_ledger.py",
    "tools/audit_repo_scripts.py",
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
    lock = load_lock()
    obj = load_json("CORPUS.manifest.json")
    if obj.get("schema") != "tct.corpus.manifest.v1":
        die("CORPUS.manifest.json schema must be tct.corpus.manifest.v1")
    if obj.get("framework") != "The Cohesive Tetrad":
        die("CORPUS.manifest.json framework must be The Cohesive Tetrad")
    author = obj.get("author", {})
    expected_orcid = lock.get("corpus", {}).get("author", {}).get("orcid")
    if expected_orcid and author.get("orcid") != expected_orcid:
        die(f"CORPUS.manifest.json author.orcid must be {expected_orcid}")


def check_jsonld() -> None:
    lock = load_lock()
    doi_urls = required_doi_urls(lock)
    obj = load_json("corpus.jsonld")
    if obj.get("@context") != "https://schema.org":
        die("corpus.jsonld @context must be https://schema.org")
    if obj.get("@type") not in ["Dataset", "CreativeWork", "DataCatalog"]:
        die("corpus.jsonld @type must be Dataset (recommended)")
    citations = obj.get("citation")
    if isinstance(citations, list):
        missing = [doi for doi in doi_urls if doi not in citations]
        if missing:
            die("corpus.jsonld citation missing DOI URLs:\n- " + "\n- ".join(missing))
    else:
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


def check_local_links() -> None:
    md_files = list((ROOT / "docs").rglob("*.md"))
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    missing: list[str] = []
    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        for raw_link in pattern.findall(text):
            link = raw_link.strip()
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            link = link.strip("`")
            link = link.split("#", 1)[0]
            if not link:
                continue
            target = (md_file.parent / link).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                continue
            if not target.exists():
                missing.append(f"{md_file.relative_to(ROOT)} -> {raw_link}")
    if missing:
        die("Broken local markdown links:\n- " + "\n- ".join(missing))


def check_ai_faq_jsonl() -> None:
    root_lines = (ROOT / "ai-faq.jsonl").read_text(encoding="utf-8").strip().splitlines()
    docs_lines = (ROOT / "docs/ai-faq.jsonl").read_text(encoding="utf-8").strip().splitlines()
    if not root_lines:
        die("ai-faq.jsonl must not be empty")
    if root_lines != docs_lines:
        die("docs/ai-faq.jsonl must match ai-faq.jsonl")

    required_keys = {"id", "question", "answer", "source"}
    for idx, line in enumerate(root_lines, start=1):
        try:
            obj = json.loads(line)
        except Exception as e:
            die(f"ai-faq.jsonl line {idx} invalid JSON: {e}")
        missing = required_keys - set(obj.keys())
        if missing:
            die(f"ai-faq.jsonl line {idx} missing keys: {sorted(missing)}")
        source = str(obj.get("source", ""))
        if not source.startswith("docs/"):
            die(f"ai-faq.jsonl line {idx} source must start with docs/: {source}")


def check_semantic_pages_linked() -> None:
    index_text = (ROOT / "docs/index.md").read_text(encoding="utf-8")
    start_text = (ROOT / "docs/start-here.md").read_text(encoding="utf-8")
    for required in ("glossary.md", "faq.md"):
        if required not in index_text:
            die(f"docs/index.md must reference {required}")
    for required in ("/glossary/", "/faq/"):
        if required not in start_text:
            die(f"docs/start-here.md must reference {required}")


def check_semantic_readiness_script() -> None:
    script = ROOT / "tools/validate_semantic_readiness.py"
    if not script.exists():
        die("Missing semantic readiness validator script")


def check_operational_standards_script() -> None:
    script = ROOT / "tools/validate_seo_llm_standards.py"
    if not script.exists():
        die("Missing SEO+LLM operational standards validator script")


def main() -> None:
    check_exists()
    check_manifest()
    check_jsonld()
    check_llms()
    check_local_links()
    check_ai_faq_jsonl()
    check_semantic_pages_linked()
    check_semantic_readiness_script()
    check_operational_standards_script()
    print("OK: portal assets validated.")


if __name__ == "__main__":
    main()
