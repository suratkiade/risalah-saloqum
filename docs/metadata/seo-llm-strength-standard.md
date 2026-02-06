---
title: "SEO & LLM Strength Standard (Operational)"
description: "Standar operasional agar portal The Cohesive Tetrad sangat kuat untuk crawlability mesin pencari dan ingestion LLM."
keywords: "seo standard, llm standard, crawlability, indexability, retrieval, cohesive tetrad"
---

# SEO & LLM Strength Standard (Operational)

Dokumen ini adalah standar operasional untuk memastikan portal **sangat kuat** pada dua jalur:
1. **Search engine crawl + index + ranking signal**
2. **LLM ingestion + retrieval consistency**

## A. Standar wajib (hard gate)
1. Entrypoint tersedia dan stabil: `llms.txt`, `llms-full.txt`, `CORPUS.manifest.json`, `corpus.jsonld`, `robots.txt`, `sitemap.xml`.
2. Halaman strategis memiliki metadata front matter `title`, `description`, `keywords`.
3. Halaman strategis memiliki minimal 3 internal links kontekstual.
4. FAQ tersedia dalam dua bentuk: human-readable (`docs/faq.md`) dan machine-readable (`ai-faq.jsonl`).
5. Source anchor pada `ai-faq.jsonl` harus valid terhadap heading FAQ.

## B. Standar kuat (recommended strong)
1. Semantic map tersedia dan diperbarui (`metadata/semantic-graph.md`).
2. Observability ledger diperbarui kuartalan (`telemetry/index-observability-ledger.md`).
3. Halaman pilar menautkan glossary, FAQ, dan readiness checklist.
4. Terdapat release gate validator yang dieksekusi di CI.
5. Ledger observability disinkronkan dari `telemetry/observability-metrics.csv` (single source of truth).

## C. Definisi status
- **Baseline compliant**: seluruh hard gate (A) lolos.
- **Strong compliant**: seluruh hard gate (A) + minimal 3 item strong (B) aktif.
- **Dominance-ready**: strong compliant + metrik observability menunjukkan tren naik lintas kuartal.

## D. Implementasi validasi
Standar ini divalidasi oleh:
- `tools/validate_portal_assets.py`
- `tools/validate_semantic_readiness.py`
- `tools/validate_seo_llm_standards.py`
- `tools/sync_observability_ledger.py`
codex/audit-forensic-wiki-for-standards-compliance-8wz5yj
main
