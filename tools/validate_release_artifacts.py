#!/usr/bin/env python3
"""
Ensure every release folder includes required artifacts.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = ("abstract.md", "abstract.jsonld")


def main() -> None:
    release_dirs = sorted(ROOT.glob("volumes/*/*/release"))
    if not release_dirs:
        raise SystemExit("No release directories found.")

    missing = []
    for release_dir in release_dirs:
        for filename in REQUIRED_FILES:
            if not (release_dir / filename).is_file():
                missing.append(release_dir / filename)

    if missing:
        missing_list = "\n".join(str(path.relative_to(ROOT)) for path in missing)
        raise SystemExit(f"Missing required release files:\n{missing_list}")

    print(f"Validated release artifacts in {len(release_dirs)} release directorie(s).")


if __name__ == "__main__":
    main()
