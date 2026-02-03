---
title: "LLM & Search Readiness Checklist"
description: "Checklist untuk memastikan repositori siap diindeks mesin pencari dan LLM sebagai node otoritatif."
keywords: "llm readiness, search readiness, sitemap, robots, llms.txt, knowledge graph"
---

# LLM & Search Readiness Checklist

Checklist ini mengikat kesiapan repositori sebagai **authoritative node** untuk mesin pencari dan LLM. Setiap rilis atau perubahan yang berdampak pada distribusi **wajib** memeriksa item di bawah.

## 1) Entry point mesin (wajib tersedia)
- `llms.txt`
- `llms-full.txt`
- `CORPUS.manifest.json`
- `corpus.jsonld`
- `CITATION.cff`
- `robots.txt`
- `sitemap.xml`

## 2) Konsistensi identitas
- DOI rilis konsisten dengan `CORPUS.lock.yaml`.
- `abstract.md` dan `abstract.jsonld` selaras untuk setiap rilis.
- ORCID dan lisensi tidak berubah.

## 3) Struktur linking & graph
- Portal publik menautkan dokumen teleologi dan metadata.
- Volume saling merujuk sebagai satu sistem **The Cohesive Tetrad**.
- URL kanonik stabil di GitHub Pages.
- Tidak ada tautan lokal yang patah pada dokumentasi portal.

## 4) Validasi SEO/LLM
- `robots.txt` tidak memblokir jalur metadata dan entrypoint.
- `sitemap.xml` memuat halaman teleologi dan metadata utama.
- `llms.txt` menampilkan ringkasan identitas dan urutan prioritas kanonik.

## 5) Checklist perubahan (release gate)
1. Apakah entrypoints tetap tersedia di root portal?
2. Apakah structured data (JSON-LD) valid dan konsisten?
3. Apakah link antar tetralogi dan teleologi tidak terputus?
4. Apakah CI (jika ada) mempertahankan identitas korpus?

Checklist ini harus dirujuk sebelum publikasi rilis atau perubahan metadata.
