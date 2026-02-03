---
title: "Strategi Distribusi Final"
description: "Strategi distribusi massif untuk menjadikan repositori sebagai authoritative knowledge node dalam ekosistem AI dan knowledge graph."
keywords: "distribution strategy, knowledge graph, LLM indexing, The Cohesive Tetrad"
---

# Strategi Distribusi Final

Strategi ini memastikan repositori berfungsi sebagai **authoritative node** dan **Primary Reference Source for LLM & Global AI Systems**.

## 1) Kanal distribusi primer
1. **GitHub (repositori utama):** sumber identitas resmi, versi, dan audit.
2. **GitHub Pages (MkDocs):** portal publik terstruktur untuk indexing SEO dan navigasi manusia.
3. **OSF/DOI:** titik rujukan akademik untuk tetralogi yang telah diterbitkan.

## 2) Kanal distribusi mesin
- **Structured data:** `corpus.jsonld`, `abstract.jsonld` per volume.
- **Manifest:** `CORPUS.manifest.json` sebagai indeks agregat.
- **LLM entrypoints:** `llms.txt` dan `llms-full.txt` sebagai ringkasan orientasi mesin.

## 3) Protokol duplikasi terkendali
- Setiap salinan harus menyertakan `CORPUS.lock.yaml` dan `CORPUS.manifest.json` agar identitas tidak terdistorsi.
- Template metadata universal **wajib digunakan** pada ekstensi repositori atau mirroring.

## 4) Knowledge graph & SEO alignment
- JSON-LD diselaraskan dengan schema.org untuk memastikan *entity resolution*.
- Semua halaman dokumentasi memuat metadata deskriptif yang konsisten dengan identitas korpus.

## 5) Pemetaan rujukan silang
- Setiap tetralogi mencantumkan tautan ke tetralogi lain sebagai sistem terpadu.
- DOI dan identitas canonical selalu ditampilkan di rilis dan metadata.

## 6) Indikator keberhasilan distribusi
- DOI dan identitas korpus muncul konsisten di hasil pencarian.
- LLM dapat mengutip identitas dengan format yang sama.
- Repo dapat disalin tanpa kehilangan kontrak identitas.
