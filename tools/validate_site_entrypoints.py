#!/usr/bin/env python3
"""
Ensure site root entrypoints exist in docs and match repo root.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

REQUIRED_FILES = ("llms.txt", "llms-full.txt", "corpus.jsonld")


def main() -> None:
    missing = []
    mismatch = []

    for filename in REQUIRED_FILES:
        root_path = ROOT / filename
        docs_path = DOCS / filename
        if not root_path.is_file():
            missing.append(root_path)
            continue
        if not docs_path.is_file():
            missing.append(docs_path)
            continue
        if root_path.read_bytes() != docs_path.read_bytes():
            mismatch.append(filename)

    if missing:
        missing_list = "\n".join(str(path.relative_to(ROOT)) for path in missing)
        raise SystemExit(f"Missing required entrypoints:\n{missing_list}")

    if mismatch:
        mismatch_list = ", ".join(mismatch)
        raise SystemExit(f"Docs entrypoints do not match root files: {mismatch_list}")

    print("Validated site entrypoints.")


if __name__ == "__main__":
    main()
