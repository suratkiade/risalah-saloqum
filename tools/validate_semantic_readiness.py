#!/usr/bin/env python3
"""
Validate semantic readiness signals for SEO and LLM ingestion.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

STRATEGIC_PAGES = [
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


def extract_markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)


def count_internal_links(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    links = extract_markdown_links(text)
    total = 0
    for link in links:
        link = link.strip()
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue
        total += 1
    return total


def github_slug(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"[^\w\-\s]", "", slug)
    slug = slug.replace(" ", "-")
    slug = re.sub(r"-+", "-", slug)
    return slug


def faq_anchor_set() -> set[str]:
    faq = (DOCS / "faq.md").read_text(encoding="utf-8")
    anchors = set()
    for line in faq.splitlines():
        if line.startswith("## "):
            anchors.add(github_slug(line[3:]))
    return anchors


def check_min_internal_links() -> None:
    violations = []
    for page in STRATEGIC_PAGES:
        if not page.exists():
            violations.append(f"missing strategic page: {page.relative_to(ROOT)}")
            continue
        count = count_internal_links(page)
        if count < 3:
            violations.append(f"{page.relative_to(ROOT)} has only {count} internal links (min 3)")
    if violations:
        die("Semantic link density check failed:\n- " + "\n- ".join(violations))


def check_ai_faq_sources() -> None:
    anchors = faq_anchor_set()
    lines = (ROOT / "ai-faq.jsonl").read_text(encoding="utf-8").strip().splitlines()
    if not lines:
        die("ai-faq.jsonl empty")

    missing = []
    for idx, line in enumerate(lines, start=1):
        obj = json.loads(line)
        src = str(obj.get("source", ""))
        if not src.startswith("docs/faq.md#"):
            missing.append(f"line {idx}: source must start with docs/faq.md#")
            continue
        anchor = src.split("#", 1)[1]
        if anchor not in anchors:
            missing.append(f"line {idx}: unknown FAQ anchor '{anchor}'")
    if missing:
        die("ai-faq source anchor check failed:\n- " + "\n- ".join(missing))


def check_entrypoint_mentions() -> None:
    index = (DOCS / "index.md").read_text(encoding="utf-8")
    start = (DOCS / "start-here.md").read_text(encoding="utf-8")
    required_index = ["glossary.md", "faq.md", "ai-faq.jsonl"]
    required_start = ["/glossary/", "/faq/", "/ai-faq.jsonl"]

    miss = []
    for token in required_index:
        if token not in index:
            miss.append(f"docs/index.md missing '{token}'")
    for token in required_start:
        if token not in start:
            miss.append(f"docs/start-here.md missing '{token}'")

    if miss:
        die("Entrypoint semantic mentions missing:\n- " + "\n- ".join(miss))


def main() -> None:
    check_min_internal_links()
    check_ai_faq_sources()
    check_entrypoint_mentions()
    print("OK: semantic readiness validated.")


if __name__ == "__main__":
    main()
