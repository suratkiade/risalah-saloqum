#!/usr/bin/env python3

"""Validate operational SEO+LLM standards for strategic docs pages."""

from __future__ import annotations

import csv
"""
Validate operational SEO+LLM standards for strategic docs pages.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

STRATEGIC = [
    DOCS / "index.md",
    DOCS / "start-here.md",
    DOCS / "glossary.md",
    DOCS / "faq.md",
    DOCS / "llm" / "index.md",
    DOCS / "llm" / "readiness.md",
    DOCS / "forensic-audit.md",
]

METRICS_CSV = DOCS / "telemetry" / "observability-metrics.csv"
LEDGER_MD = DOCS / "telemetry" / "index-observability-ledger.md"

def die(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)


def require_frontmatter_fields(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        die(f"{path.relative_to(ROOT)} missing YAML front matter")
    end = text.find("\n---\n", 4)
    if end == -1:
        die(f"{path.relative_to(ROOT)} malformed YAML front matter")
    fm = text[4:end]
    for key in ("title:", "description:", "keywords:"):
        if key not in fm:
            die(f"{path.relative_to(ROOT)} missing front matter field: {key[:-1]}")


def check_internal_links(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
    internal = [
        l for l in links
        if not l.startswith(("http://", "https://", "mailto:", "#"))
    ]
    if len(internal) < 3:
        die(f"{path.relative_to(ROOT)} must have at least 3 internal markdown links")


def check_required_assets() -> None:
    required = [
        ROOT / "llms.txt",
        ROOT / "llms-full.txt",
        ROOT / "CORPUS.manifest.json",
        ROOT / "corpus.jsonld",
        DOCS / "robots.txt",
        DOCS / "faq.md",
        DOCS / "glossary.md",
        ROOT / "ai-faq.jsonl",
        DOCS / "metadata" / "semantic-graph.md",
        DOCS / "metadata" / "seo-llm-strength-standard.md",
        METRICS_CSV,
        LEDGER_MD,
        DOCS / "telemetry" / "index-observability-ledger.md",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        die("Missing required SEO/LLM assets:\n- " + "\n- ".join(missing))


def check_observability_metrics() -> None:
    with METRICS_CSV.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        die("docs/telemetry/observability-metrics.csv must have at least 1 data row")

    required_cols = {
        "period",
        "indexed_pages",
        "coverage_pct",
        "top_canonical_query",
        "avg_position",
        "ctr_pct",
        "crawl_errors",
        "action_notes",
    }
    if set(rows[0].keys()) != required_cols:
        die("observability metrics csv headers must match required schema")

    last = rows[-1]
    try:
        int(last["indexed_pages"])
        float(last["coverage_pct"])
        float(last["avg_position"])
        float(last["ctr_pct"])
        int(last["crawl_errors"])
    except ValueError as e:
        die(f"latest observability row has invalid numeric values: {e}")

    ledger = LEDGER_MD.read_text(encoding="utf-8")
    for val in (
        last["period"],
        last["indexed_pages"],
        last["coverage_pct"],
        last["top_canonical_query"],
        last["avg_position"],
        last["ctr_pct"],
        last["crawl_errors"],
    ):
        if str(val) not in ledger:
            die(f"ledger is not synced with latest metrics value: {val}")


def main() -> None:
    check_required_assets()
    check_observability_metrics()
def main() -> None:
    check_required_assets()
    for page in STRATEGIC:
        require_frontmatter_fields(page)
        check_internal_links(page)
    print("OK: SEO+LLM operational standards validated.")


if __name__ == "__main__":
    main()
