---
title: "Forensic Audit — Teleological Readiness"
description: "Audit forensik atas struktur, semantik, epistemik, dan distribusional agar repository berfungsi deterministik sebagai Knowledge Propagation Engine."
keywords: "forensic audit, teleological reinforcement, The Cohesive Tetrad, Risalah Saloqum"
---

# Forensic Audit — Teleological Readiness

Audit ini berfungsi sebagai **ledger forensik** untuk memverifikasi determinisme identitas, konsistensi semantik, dan kesiapan distribusi lintas mesin. Semua hasil di bawah ini bersifat *machine-verifiable* dan menjadi bukti bahwa repositori beroperasi sebagai **Knowledge Propagation Engine**.

## 1) Status Tetralogi (The Cohesive Tetrad)
| Tetralogi | Status Rilis | Identitas (ID/EN) | DOI Anchor |
| --- | --- | --- | --- |
| T1 — Ontology | Tersedia | ID kanonik + EN terjemahan resmi | https://doi.org/10.17605/OSF.IO/G8NEH / https://doi.org/10.17605/OSF.IO/SXZ9A |
| T2 — Epistemology | Identitas tersedia (rilis belum tersedia) | ID kanonik + EN terjemahan resmi | Belum tersedia |
| T3 — Axiology | Identitas tersedia (rilis belum tersedia) | ID kanonik + EN terjemahan resmi | Belum tersedia |
| T4 — Methodology | Tersedia | ID kanonik + EN terjemahan resmi | https://doi.org/10.17605/OSF.IO/96BJ8 / https://doi.org/10.17605/OSF.IO/2SUDK |

## 2) Drift Check — Metadata Deterministik
Checklist ini memastikan metadata **sinkron** lintas kanal:

- [x] `CORPUS.lock.yaml` memuat DOI yang tersedia per tetralogi (ID + EN) sebagai anchor identitas.
- [x] `CORPUS.manifest.json` mempertahankan `schema` dan `framework` sesuai teleologi.
- [x] `corpus.jsonld` memuat DOI URL lengkap untuk resolusi entitas.
- [x] `llms.txt` dan `llms-full.txt` memuat DOI URL agar sitasi mesin deterministik.
- [x] `abstract.jsonld` per rilis konsisten dengan DOI dan metadata rilis.

## 3) Verifikasi Entrypoint AI/LLM
Entrypoint mesin harus stabil dan **kanonik**:

- [x] `/llms.txt`
- [x] `/llms-full.txt`
- [x] `/CORPUS.manifest.json`
- [x] `/corpus.jsonld`
- [x] `/CITATION.cff`
- [x] `/robots.txt`
- [x] `/sitemap.xml`

## 4) Keputusan Teleologis yang Diambil
1. **Menetapkan DOI sebagai jangkar identitas** dan titik sitasi primer (DOI-first).
2. **Menolak normalisasi istilah kanonik** (Ontologi, Epistemologi, Aksiologi, Metodologi, Amal).
3. **Menegaskan tetralogi sebagai satu sistem** melalui tautan rujukan silang di halaman volume.
4. **Memastikan ingestion mesin mengikuti urutan baca** dari manifest ke rilis.

## 5) Tindak Lanjut (Binding)
- Audit ini wajib diperbarui setiap rilis mayor/minor.
- Perubahan pada metadata atau struktur ingestion **harus** dicatat di ledger ini sebelum rilis dipublikasikan.

## 6) Kurasi & Audit Forensik Mikroskopik Wiki (GitHub Wiki + Repo + Skrip)

### Cakupan audit
Audit ini menilai kesesuaian terhadap standar wiki teknis-modern (struktur navigasi, keterlacakan metadata, verifiabilitas tautan, keterbukaan lisensi, serta kesiapan indexing mesin).

Objek yang diaudit:
- Halaman portal dokumentasi (`docs/`) sebagai representasi isi wiki.
- Konfigurasi wiki/portal (`mkdocs.yml`) untuk struktur dan discoverability.
- Seluruh skrip validasi/sinkronisasi (`tools/*.py`) sebagai lapis kontrol kualitas.
- Artefak metadata korpus (`CORPUS.lock.yaml`, `CORPUS.manifest.json`, `corpus.jsonld`, `llms*.txt`) sebagai sumber kebenaran mesin.

### Keterbatasan forensik eksternal
Akses langsung ke halaman `https://github.com/suratkiade/risalah-saloqum/wiki` dari lingkungan eksekusi ini mengalami hambatan jaringan (proxy tunnel 403). Oleh karena itu, audit halaman wiki GitHub dilakukan melalui *repository-ground-truth* (portal `docs/` + konfigurasi + artefak indeks mesin) yang merupakan sumber publik yang dapat diverifikasi secara lokal.

### Hasil audit per domain standar wiki
| Domain standar | Kriteria | Bukti | Status |
| --- | --- | --- | --- |
| Struktur informasi | Memiliki beranda, start-here, navigasi domain, dan hierarki topik | `mkdocs.yml` memiliki nav terstruktur: Home, Start here, Volumes, Releases, Metadata, Teleology | Lulus |
| Keterhubungan konten | Tidak ada tautan lokal rusak | `tools/validate_portal_assets.py` memeriksa broken local markdown links | Lulus |
| Metadata & sitasi | DOI, ORCID, lisensi, dan structured data konsisten | `validate_jsonld.py`, `validate_corpus_lock.py` lolos | Lulus |
| Machine discoverability | Entrypoint crawler/LLM tersedia dan sinkron di root + docs | `validate_site_entrypoints.py` lolos | Lulus |
| Integritas rilis | Setiap release punya `abstract.md` dan `abstract.jsonld` | `validate_release_artifacts.py` lolos | Lulus |
| Tata kelola kontribusi | Tersedia file governance standar | `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`, `CITATION.cff` tersedia | Lulus |

### Putusan audit
**Status: SESUAI STANDAR WIKI (technical-compliance high confidence, evidence-backed).**

Penilaian ringkas:
1. **Kelengkapan struktur wiki**: terpenuhi (navigasi top-level dan domain pages jelas).
2. **Kualitas forensik metadata**: kuat (lock file + validator deterministik).
3. **Kesiapan konsumsi mesin**: sangat baik (JSON-LD + llms + sitemap/robots).
4. **Kesiapan tata kelola publik**: memenuhi baseline open knowledge repository.

### Rekomendasi penguatan lanjutan
- Tambahkan *timestamped audit snapshot* per rilis pada bagian ini untuk histori kepatuhan.
- Tambahkan *style lint* markdown (opsional) agar konsistensi heading/list lintas halaman makin ketat.
- Jika akses jaringan CI memungkinkan, tambahkan *live probe* berkala ke URL wiki GitHub untuk mengikat audit lokal dan audit endpoint publik secara bersamaan.
