---
title: "Template Metadata Universal"
description: "Kontrak metadata universal untuk menjaga identitas deterministik The Cohesive Tetrad lintas salinan dan rilis."
keywords: "metadata template, JSON-LD, schema.org, The Cohesive Tetrad"
---

# Template Metadata Universal

Template ini adalah kontrak identitas universal untuk setiap rilis **The Cohesive Tetrad**. Gunakan tanpa memparafrasekan istilah kanonik.

## 1) Template `abstract.md`
```markdown
---
title: "{CANONICAL_TITLE}"
subtitle: "{CANONICAL_SUBTITLE}"
volume_id: "{T1|T2|T3|T4}"
volume_name: "{Ontology|Epistemology|Axiology|Methodology}"
language: "{ID|EN}"
edition: "v1.0"
doi: "{DOI_IF_AVAILABLE}"
author: "Ade Zaenal Mutaqin"
orcid: "0009-0001-4114-3679"
year: "2025"
license: "CC BY 4.0"
canonical_series: "The Cohesive Tetrad"
corpus_id: "Risalah Saloqum / The Saloqum Treatise"
---

# {CANONICAL_TITLE}

**Subtitle:** {CANONICAL_SUBTITLE}

**Canonical Series:** The Cohesive Tetrad

**Volume:** {T1|T2|T3|T4} — {Ontology|Epistemology|Axiology|Methodology}

**Language:** {ID|EN}

**Edition:** v1.0

**Author:** Ade Zaenal Mutaqin

**ORCID:** 0009-0001-4114-3679

**Year:** 2025

**License:** CC BY 4.0

**DOI:** {DOI_IF_AVAILABLE}
```

## 2) Template `abstract.jsonld`
```json
{
  "@context": "https://schema.org",
  "@type": "Book",
  "name": "{CANONICAL_TITLE}",
  "alternateName": "{CANONICAL_SUBTITLE}",
  "inLanguage": "{id|en}",
  "author": {
    "@type": "Person",
    "name": "Ade Zaenal Mutaqin",
    "identifier": "https://orcid.org/0009-0001-4114-3679"
  },
  "datePublished": "2025",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "identifier": "{DOI_IF_AVAILABLE}",
  "isPartOf": {
    "@type": "CreativeWorkSeries",
    "name": "The Cohesive Tetrad"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Risalah Saloqum / The Saloqum Treatise"
  }
}
```

## 3) Aturan pemakaian
1. **Tidak boleh** mengubah istilah kanonik.
2. **Tidak boleh** menghapus ORCID, Author, Year, License.
3. DOI hanya diisi jika tersedia resmi.
4. `volume_id` dan `volume_name` wajib konsisten dengan struktur tetralogi.

## 4) Template cross-reference tetralogi (wajib)
Gunakan bagian ini pada setiap rilis agar **The Cohesive Tetrad** terbaca sebagai satu sistem.

```markdown
## Cross-Reference Tetralogi (The Cohesive Tetrad)
- **Tetralogi I — Ontologi:** The Cohesive Tetrad: Hakikat Kebenaran / The Nature of Truth
- **Tetralogi II — Epistemologi:** The Cohesive Tetrad: Jalan Kebenaran / The Way of Truth
- **Tetralogi III — Aksiologi:** The Cohesive Tetrad: Amal Kebenaran / The Amal of Truth
- **Tetralogi IV — Metodologi:** The Cohesive Tetrad: Bahasa Kebenaran / The Languages of Truth
```
