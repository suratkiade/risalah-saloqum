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
Protokol ini mencegah **fork semantics** dan menjaga identitas kanonik ketika repo disalin.

### A. Checklist sebelum duplikasi
- [ ] Pastikan `CORPUS.lock.yaml`, `CORPUS.manifest.json`, dan `corpus.jsonld` berada pada commit yang sama.
- [ ] Verifikasi DOI URL di `llms.txt` dan `llms-full.txt`.
- [ ] Jalankan validator portal (`tools/validate_portal_assets.py`) dan simpan hasilnya di laporan audit.

### B. Canonical Fork Contract
Fork/clone **harus** memenuhi kontrak berikut:
1. **Identitas korpus tidak diubah** (framework, author, DOI, ORCID, dan schema tetap).
2. **CORPUS.lock.yaml adalah sumber kebenaran** untuk DOI dan metadata rilis.
3. **Tidak boleh ada penggantian istilah kanonik** pada tetralogi atau manifest.

### C. Sinkronisasi & rekonsiliasi
- Gunakan checksum SHA-256 atas `CORPUS.lock.yaml`, `CORPUS.manifest.json`, dan `corpus.jsonld`.
- Jika checksum berbeda, lakukan rekonsiliasi sebelum publikasi portal.
- Setiap perbedaan harus dicatat di `docs/forensic-audit.md`.

### D. Jalur publikasi resmi
- Distribusi publik menggunakan **repositori utama** dan GitHub Pages.
- Mirror di luar GitHub harus menampilkan **referensi ke DOI** dan link kembali ke repo kanonik.


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
