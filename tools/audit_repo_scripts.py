#!/usr/bin/env python3
"""Forensic audit for Python scripts in repository (syntax + structure checks)."""

import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXCLUDE_PARTS = {"__pycache__", "build", ".egg-info", "site", ".git"}
SEARCH_DIRS = [ROOT / "tools", ROOT / ".github" / "scripts"]


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDE_PARTS or part.endswith('.egg-info') for part in path.parts)


def gather_scripts() -> list[Path]:
    scripts: list[Path] = []
    for base in SEARCH_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*.py"):
            if is_excluded(p.relative_to(ROOT)):
                continue
            scripts.append(p)
    return sorted(scripts)


def audit_syntax(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for p in paths:
        try:
            py_compile.compile(str(p), doraise=True)
        except Exception as e:
            errors.append(f"{p.relative_to(ROOT)}: {e}")
    return errors


def main() -> None:
    paths = gather_scripts()
    if not paths:
        print("ERROR: no scripts found for audit")
        sys.exit(1)

    errors = audit_syntax(paths)
    if errors:
        print("ERROR: script forensic audit failed:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print(f"OK: audited {len(paths)} Python script(s) with zero syntax errors.")


if __name__ == "__main__":
    main()
