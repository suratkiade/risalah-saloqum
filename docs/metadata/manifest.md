---
title: "Manifest"
description: "Penjelasan CORPUS.manifest.json sebagai peta rilis dan aset yang diawasi untuk SEO dan LLM."
keywords: "manifest, CORPUS.manifest.json, metadata, releases, validation, Risalah Saloqum, The Cohesive Tetrad"
---

# Manifest

`CORPUS.manifest.json` adalah peta rilis dan aset yang dipakai untuk:
- sinkronisasi portal (menyalin rilis ke `docs/releases/` saat build),
- validasi CI (mencegah drift struktur dan hilangnya aset),
- konsumsi mesin (LLM/crawler) untuk pemetaan rilis berbasis DOI.

## Lokasi
- Repo root: `CORPUS.manifest.json`
- Terpublikasi di portal: `/CORPUS.manifest.json`

## Isi minimum yang diharapkan
- identitas korpus,
- daftar volume tetralogi,
- DOI per rilis (ID kanonik dan EN terjemahan),
- daftar berkas rilis dan path repo.
