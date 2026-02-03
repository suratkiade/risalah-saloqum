"""MkDocs sitemap plugin that emits sitemap.xml after build."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urljoin

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin


class SitemapPlugin(BasePlugin):
    config_scheme = (
        ("changefreq", config_options.Type(str, default=None)),
        ("priority", config_options.Type(float, default=None)),
    )

    def on_post_build(self, config) -> None:
        site_url = config.get("site_url")
        if not site_url:
            return

        site_dir = Path(config["site_dir"])
        urls = []
        for path in site_dir.rglob("*.html"):
            rel = path.relative_to(site_dir).as_posix()
            if rel.endswith("404.html"):
                continue
            url = urljoin(site_url.rstrip("/") + "/", rel)
            urls.append(url)

        urls.sort()
        lines = [
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">",
        ]
        changefreq = self.config.get("changefreq")
        priority = self.config.get("priority")
        for url in urls:
            lines.append("  <url>")
            lines.append(f"    <loc>{url}</loc>")
            if changefreq:
                lines.append(f"    <changefreq>{changefreq}</changefreq>")
            if priority is not None:
                lines.append(f"    <priority>{priority:.1f}</priority>")
            lines.append("  </url>")
        lines.append("</urlset>")
        sitemap_path = site_dir / "sitemap.xml"
        sitemap_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
