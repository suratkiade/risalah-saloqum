#!/usr/bin/env python3
"""
sync_release_assets.py

Copy release assets from volumes/**/release into a target folder so the
GitHub Pages portal can serve PDFs/Markdown files directly.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def resolve_target_root(raw_target: str) -> Path:
    target_path = Path(raw_target)
    target_root = target_path if target_path.is_absolute() else (ROOT / target_path)
    target_root = target_root.resolve()
    try:
        target_root.relative_to(ROOT)
    except ValueError as exc:
        raise SystemExit(f"Refusing to write outside repo root: {target_root}") from exc
    return target_root


def copy_release_dir(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        if item.is_file() and not item.is_symlink():
            shutil.copy2(item, target / item.name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync release assets into a target folder.")
    parser.add_argument(
        "--target",
        default="site/releases",
        help="Target folder relative to repo root (default: site/releases).",
    )
    args = parser.parse_args()

    target_root = resolve_target_root(args.target)
    target_root.mkdir(parents=True, exist_ok=True)

    release_dirs = list(ROOT.glob("volumes/*/*/release"))
    if not release_dirs:
        print("No release directories found.")
        return

    for release_dir in release_dirs:
        volume = release_dir.parents[1].name.lower()
        lang = release_dir.parent.name.lower()
        dest = target_root / volume / lang
        copy_release_dir(release_dir, dest)
        print(f"Synced {release_dir.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
