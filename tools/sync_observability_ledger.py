#!/usr/bin/env python3
"""Sync docs/telemetry/index-observability-ledger.md table from CSV metrics."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "docs" / "telemetry" / "observability-metrics.csv"
LEDGER_PATH = ROOT / "docs" / "telemetry" / "index-observability-ledger.md"

START_MARKER = "| Periode | Indexed pages | Coverage % | Top canonical query | Avg position | CTR | Crawl errors | Catatan aksi |"


def load_rows() -> list[dict[str, str]]:
    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return rows


def render_rows(rows: list[dict[str, str]]) -> list[str]:
    out = [
        "| Periode | Indexed pages | Coverage % | Top canonical query | Avg position | CTR | Crawl errors | Catatan aksi |",
        "| --- | ---: | ---: | --- | ---: | ---: | ---: | --- |",
    ]
    for r in rows:
        out.append(
            f"| {r['period']} | {r['indexed_pages']} | {r['coverage_pct']} | {r['top_canonical_query']} | {r['avg_position']} | {r['ctr_pct']} | {r['crawl_errors']} | {r['action_notes']} |"
        )
    return out


def main() -> None:
    rows = load_rows()
    text = LEDGER_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    start_idx = None
    for i, line in enumerate(lines):
        if line.strip() == START_MARKER:
            start_idx = i
            break
    if start_idx is None:
        raise SystemExit("Could not find observability table marker in ledger")

    end_idx = start_idx + 1
    while end_idx < len(lines) and lines[end_idx].strip().startswith("|"):
        end_idx += 1

    table_lines = render_rows(rows)
    new_lines = lines[:start_idx] + table_lines + lines[end_idx:]
    LEDGER_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"Synced observability ledger with {len(rows)} row(s).")


if __name__ == "__main__":
    main()
