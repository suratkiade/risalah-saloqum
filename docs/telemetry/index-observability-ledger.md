---
title: "Index Observability Ledger"
description: "Ledger metrik indeks dan distribusi untuk memastikan pertumbuhan otoritas digital The Cohesive Tetrad."
keywords: "index coverage, ctr, search performance, observability, seo telemetry"
---

# Index Observability Ledger

Ledger ini mengikat observabilitas performa indexing, crawling, dan discoverability lintas kuartal.

## KPI operasional (minimum)
- Coverage halaman strategis terindeks.
- CTR kueri utama bertema The Cohesive Tetrad.
- Posisi rata-rata untuk kueri kanonik.
- Stabilitas crawl (error rate, blocked path, latency anomali).

## Tabel pemantauan kuartalan
| Periode | Indexed pages | Coverage % | Top canonical query | Avg position | CTR | Crawl errors | Catatan aksi |
| --- | ---: | ---: | --- | ---: | ---: | ---: | --- |
| 2026-Q1 | 18 | 92.3 | The Cohesive Tetrad | 12.4 | 3.8 | 0 | Baseline kuartal awal setelah hardening semantic+LLM |
| 2026-Q1 | TBD | TBD | The Cohesive Tetrad | TBD | TBD | TBD | Baseline pengukuran awal |

## Audit checklist observability
1. Apakah semua halaman pilar masuk indeks publik?
2. Apakah glossary dan FAQ muncul pada kueri definisional?
3. Apakah `/ai-faq.jsonl` terjangkau crawler tanpa blok robots?
4. Apakah terjadi penurunan coverage atau CTR yang signifikan?

## Sinkronisasi data
- Single source of truth: `docs/telemetry/observability-metrics.csv`.
- Sinkronisasi tabel ledger: `python tools/sync_observability_ledger.py`.

## Binding policy
- Ledger diperbarui minimal sekali per kuartal.
- Setiap perubahan major pada struktur wiki harus menambahkan catatan dampak metrik.
