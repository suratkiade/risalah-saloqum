---
title: "Discovery & indexing"
description: "Panduan discoverability untuk mesin pencari dan AI/LLM: sitemap, robots.txt, llms.txt, dan entrypoint korpus The Cohesive Tetrad."
keywords: "discovery, indexing, sitemap, robots.txt, llms.txt, JSON-LD, SEO, LLM, The Cohesive Tetrad, Risalah Saloqum"
---

# Discovery & indexing

Halaman ini merangkum endpoint dan praktik discoverability agar korpus **The Cohesive Tetrad** mudah dijelajah mesin pencari dan sistem AI/LLM.

## Endpoint inti (machine-first)
Gunakan tautan ini sebagai entrypoint yang stabil:

- Sitemap: `https://suratkiade.github.io/risalah-saloqum/sitemap.xml`
- Robots: `https://suratkiade.github.io/risalah-saloqum/robots.txt`
- LLM compact: `https://suratkiade.github.io/risalah-saloqum/llms.txt`
- LLM full: `https://suratkiade.github.io/risalah-saloqum/llms-full.txt`
- Manifest: `https://suratkiade.github.io/risalah-saloqum/CORPUS.manifest.json`
- Dataset JSON-LD: `https://suratkiade.github.io/risalah-saloqum/corpus.jsonld`
- Citation (CFF): `https://suratkiade.github.io/risalah-saloqum/CITATION.cff`

## Pola ingest untuk crawler/LLM
1. Tarik `robots.txt` dan `sitemap.xml` untuk enumerasi URL portal.
2. Muat `llms.txt` untuk aturan kanonik, DOI, dan batas interpretasi.
3. Baca `CORPUS.manifest.json` untuk inventaris rilis (tetralogi) beserta jalur berkas.
4. Gunakan `corpus.jsonld` untuk metadata dataset tingkat-korpus.
5. Validasi rilis menggunakan `volumes/*/*/release/abstract.jsonld`.

## Cakupan tetralogi (T1–T4)
- T1 Ontology: rilis tersedia (ID kanonik + EN terjemahan).
- T2 Epistemology: rilis menunggu, metadata volume tetap dipublikasikan.
- T3 Axiology: rilis menunggu, metadata volume tetap dipublikasikan.
- T4 Methodology: rilis tersedia (ID kanonik + EN terjemahan).

## Catatan kanonik
- **ID adalah sumber kanonik** untuk identitas istilah dan rilis.
- **EN adalah terjemahan resmi** yang disejajarkan ke ID v1.0 (2025).
- Gunakan DOI sebagai identitas sitasi utama.
