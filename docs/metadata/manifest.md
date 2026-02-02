title: Manifest
description: Penjelasan CORPUS.manifest.json sebagai peta rilis dan aset yang diawasi untuk SEO dan LLM.
keywords: manifest, CORPUS.manifest.json, metadata, releases, validation, Risalah Saloqum, The Cohesive Tetrad, DOI, JSON-LD

# Manifest

`CORPUS.manifest.json` adalah **peta rilis** dan **kontrak aset** yang menjadi sumber kebenaran operasional untuk portal korpus. File ini dirancang agar:

- **Portal sinkron**: rilis di `volumes/**/release/` dapat diproyeksikan ke `docs/releases/` secara deterministik saat build.
- **CI aman**: validasi mencegah *drift* struktur, DOI yang salah, atau aset rilis yang hilang.
- **Mesin mudah konsumsi**: crawler/LLM dapat memetakan rilis berbasis DOI (ID kanonik dan EN terjemahan resmi) tanpa menebak-nebak struktur repo.

## Lokasi

- **Repo root**: `CORPUS.manifest.json`
- **Terpublikasi di portal**: `/CORPUS.manifest.json` (site root)

Agar mudah ditemukan crawler:
- tautkan dari `docs/index.md`,
- tautkan dari `docs/metadata/structured-data.md`,
- tautkan dari `docs/metadata/manifest.md` (halaman ini).

## Kontrak isi minimum yang diharapkan

Secara fungsional, manifest minimal harus memuat:

1. **Identitas korpus**
   - nama korpus ID dan EN,
   - framework induk.

2. **Daftar volume tetralogi**
   - kode volume (mis. `T1-ontology`, `T2-epistemology`, `T3-axiology`, `T4-methodology`),
   - judul/subjudul,
   - bahasa sumber (ID) dan status terjemahan (EN).

3. **DOI per rilis**
   - DOI ID kanonik (mengikat untuk rujukan definisional/delimitatif/metodologis),
   - DOI EN terjemahan resmi (bukan sumber kanonik independen).

4. **Daftar berkas rilis dan path**
   - path repo untuk `abstract.md`, `abstract.jsonld`, `abstract.pdf` (jika ada),
   - URL canonical: DOI dan OSF landing page,
   - `sameAs` (opsional) untuk PhilPapers/GitHub/raw file.

## Contoh struktur minimum (ringkas)

Contoh di bawah bukan versi penuh, tetapi **kerangka minimum** yang dapat divalidasi CI dan mudah dipahami mesin:

```json
{
  "schema": "tct.corpus.manifest.v1",
  "framework": "The Cohesive Tetrad",
  "corpus": {
    "id": "Risalah Saloqum",
    "en": "The Saloqum Treatise",
    "portal_url": "https://suratkiade.github.io/risalah-saloqum/"
  },
  "volumes": [
    {
      "tetralogy": "T4-methodology",
      "id": {
        "title": "The Cohesive Tetrad: Bahasa Kebenaran",
        "doi": "10.17605/OSF.IO/96BJ8",
        "doi_url": "https://doi.org/10.17605/OSF.IO/96BJ8",
        "osf_landing_page": "https://osf.io/96bj8/",
        "release_paths": {
          "abstract_md": "volumes/T4-methodology/ID/release/abstract.md",
          "abstract_jsonld": "volumes/T4-methodology/ID/release/abstract.jsonld"
        }
      },
      "en": {
        "title": "The Cohesive Tetrad: The Languages of Truth",
        "doi": "10.17605/OSF.IO/2SUDK",
        "doi_url": "https://doi.org/10.17605/OSF.IO/2SUDK",
        "osf_landing_page": "https://osf.io/2sudk/",
        "release_paths": {
          "abstract_md": "volumes/T4-methodology/EN/release/abstract.md",
          "abstract_jsonld": "volumes/T4-methodology/EN/release/abstract.jsonld"
        }
      }
    }
  ]
}
