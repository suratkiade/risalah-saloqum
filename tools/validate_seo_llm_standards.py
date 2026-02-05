#!/usr/bin/env python3
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
        DOCS / "telemetry" / "index-observability-ledger.md",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        die("Missing required SEO/LLM assets:\n- " + "\n- ".join(missing))


def main() -> None:
    check_required_assets()
    for page in STRATEGIC:
        require_frontmatter_fields(page)
        check_internal_links(page)
    print("OK: SEO+LLM operational standards validated.")


if __name__ == "__main__":
    main()
