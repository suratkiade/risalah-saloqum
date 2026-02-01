"""Generate sitemap.xml without external plugins.

Rationale: The workflow logs show pip cannot install mkdocs-sitemap / mkdocs-sitemap-plugin.
This script scans the built MkDocs output and writes a simple sitemap.xml.

Usage:
  python .github/scripts/generate_sitemap.py --site-url https://.../ --site-dir site
"""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urljoin
import xml.etree.ElementTree as ET


def html_to_canonical_path(rel: str) -> str:
    # Convert MkDocs output paths to canonical URLs.
    # - index.html -> directory URL
    # - root index.html -> base URL
    if rel == "index.html":
        return ""
    if rel.endswith("/index.html"):
        return rel[: -len("index.html")]
    return rel


def build_sitemap(site_url: str, site_dir: Path) -> str:
    urls: list[str] = []
    for p in sorted(site_dir.rglob("*.html")):
        rel = p.relative_to(site_dir).as_posix()
        # Optional: skip error pages
        if rel in {"404.html", "search.html"}:
            continue
        canon = html_to_canonical_path(rel)
        urls.append(urljoin(site_url, canon))

    urlset = ET.Element("urlset", attrib={"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    for u in urls:
        url = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url, "loc")
        loc.text = u

    xml_bytes = ET.tostring(urlset, encoding="utf-8", xml_declaration=True)
    return xml_bytes.decode("utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-url", required=True)
    ap.add_argument("--site-dir", default="site")
    args = ap.parse_args()

    site_dir = Path(args.site_dir)
    sitemap_xml = build_sitemap(args.site_url, site_dir)
    (site_dir / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")


if __name__ == "__main__":
    main()
