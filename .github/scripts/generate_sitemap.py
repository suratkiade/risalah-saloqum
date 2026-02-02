#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# Direktori yang biasanya muncul di output MkDocs (site/)
EXCLUDE_DIRS = {
    "assets", "search", "stylesheets", "javascripts",
    ".git", ".github",
}

# File yang tidak perlu masuk sitemap
EXCLUDE_FILES = {
    "404.html",
    "sitemap.xml",
}

# File yang layak dipublikasikan dalam sitemap
INCLUDE_EXTS = {".html", ".pdf"}

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def iso_date_from_mtime(p: Path) -> str:
    dt = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
    return dt.date().isoformat()


def normalize_site_url(site_url: str) -> str:
    site_url = site_url.strip()
    if not site_url.endswith("/"):
        site_url += "/"
    return site_url


def iter_publish_files(site_dir: Path):
    # deterministik: urutkan berdasarkan path relatif
    for p in sorted(site_dir.rglob("*"), key=lambda x: x.as_posix()):
        if p.is_dir():
            continue
        if p.name in EXCLUDE_FILES:
            continue

        rel_parts = p.relative_to(site_dir).parts

        # skip hidden file/dir
        if any(part.startswith(".") for part in rel_parts):
            continue

        # skip folder tertentu dalam jalur
        if any(part in EXCLUDE_DIRS for part in rel_parts):
            continue

        if p.suffix.lower() not in INCLUDE_EXTS:
            continue

        yield p


def file_to_url(site_url: str, site_dir: Path, file_path: Path) -> str:
    rel = file_path.relative_to(site_dir).as_posix()

    # Normalisasi "pretty URL" MkDocs:
    # - index.html di root => base URL (tanpa path)
    # - folder/index.html => folder/
    if rel == "index.html":
        rel = ""
    elif rel.endswith("/index.html"):
        rel = rel[:-len("index.html")]

    # urljoin akan menjaga canonical base, tetapi pastikan rel tidak diawali slash
    rel = rel.lstrip("/")
    return urljoin(site_url, rel)


def build_sitemap(site_url: str, site_dir: Path, output: Path) -> int:
    site_url = normalize_site_url(site_url)
    site_dir = site_dir.resolve()
    output = output.resolve()

    urlset = ET.Element("urlset", {"xmlns": SITEMAP_NS})

    seen = set()
    count = 0

    for f in iter_publish_files(site_dir):
        loc = file_to_url(site_url, site_dir, f)

        # Guard duplikasi (misal karena variasi path)
        if loc in seen:
            continue
        seen.add(loc)

        lastmod = iso_date_from_mtime(f)

        url_el = ET.SubElement(urlset, "url")
        ET.SubElement(url_el, "loc").text = loc
        ET.SubElement(url_el, "lastmod").text = lastmod
        count += 1

    tree = ET.ElementTree(urlset)
    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding="utf-8", xml_declaration=True)
    return count


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-url", required=True, help="Base canonical URL, e.g. https://user.github.io/repo/")
    ap.add_argument("--site-dir", required=True, help="Built site directory, usually 'site'")
    ap.add_argument("--output", default=None, help="Output path, default: <site-dir>/sitemap.xml")
    args = ap.parse_args()

    site_dir = Path(args.site_dir)
    if not site_dir.exists() or not site_dir.is_dir():
        raise SystemExit(f"site-dir not found or not a directory: {site_dir}")

    output = Path(args.output) if args.output else (site_dir / "sitemap.xml")
    n = build_sitemap(args.site_url, site_dir, output)
    print(f"OK: wrote sitemap -> {output} ({n} urls)")


if __name__ == "__main__":
    main()
