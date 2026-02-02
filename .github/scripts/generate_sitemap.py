#!/usr/bin/env python3
import argparse
from pathlib import Path
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# Files we never want in sitemap
EXCLUDE_FILES = {
    "404.html",
    "sitemap.xml",
}

# Only publishable formats
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
    for p in site_dir.rglob("*"):
        if p.is_dir():
            continue

        if p.name in EXCLUDE_FILES:
            continue

        # skip hidden files/dirs
        rel_parts = p.relative_to(site_dir).parts
        if any(part.startswith(".") for part in rel_parts):
            continue

        if p.suffix.lower() not in INCLUDE_EXTS:
            continue

        yield p


def file_to_url(site_url: str, site_dir: Path, file_path: Path) -> str:
    rel = file_path.relative_to(site_dir).as_posix()

    # MkDocs directory URLs: folder/index.html -> folder/
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]

    return urljoin(site_url, rel)


def indent_xml(elem: ET.Element, level: int = 0):
    # small pretty printer without extra deps
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent_xml(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def build_sitemap(site_url: str, site_dir: Path, output: Path):
    site_url = normalize_site_url(site_url)
    site_dir = site_dir.resolve()
    output = output.resolve()

    if not site_dir.exists():
        raise SystemExit(f"site-dir not found: {site_dir}")

    ET.register_namespace("", SITEMAP_NS)
    urlset = ET.Element(f"{{{SITEMAP_NS}}}urlset")

    files = sorted(iter_publish_files(site_dir))
    for f in files:
        loc = file_to_url(site_url, site_dir, f)
        lastmod = iso_date_from_mtime(f)

        url_el = ET.SubElement(urlset, f"{{{SITEMAP_NS}}}url")
        ET.SubElement(url_el, f"{{{SITEMAP_NS}}}loc").text = loc
        ET.SubElement(url_el, f"{{{SITEMAP_NS}}}lastmod").text = lastmod

    indent_xml(urlset)
    tree = ET.ElementTree(urlset)
    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding="utf-8", xml_declaration=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-url", required=True, help="Base canonical URL, e.g. https://user.github.io/repo/")
    ap.add_argument("--site-dir", required=True, help="Built site directory, usually 'site'")
    ap.add_argument("--output", default=None, help="Output path, default: <site-dir>/sitemap.xml")
    args = ap.parse_args()

    site_dir = Path(args.site_dir)
    output = Path(args.output) if args.output else (site_dir / "sitemap.xml")
    build_sitemap(args.site_url, site_dir, output)
    print(f"OK: wrote sitemap -> {output}")


if __name__ == "__main__":
    main()
