---
title: "Semantic Graph Map"
description: "Peta relasi antardokumen untuk memperkuat pemahaman semantik mesin pencari dan LLM pada korpus The Cohesive Tetrad."
keywords: "semantic graph, json-ld, hasPart, isPartOf, mentions, about, cohesive tetrad"
---

# Semantic Graph Map

Halaman ini mendefinisikan relasi antardokumen secara eksplisit agar ingestion mesin menjadi lebih kaya konteks.

## Tujuan
1. Menguatkan *document-to-document relation* untuk crawler semantik.
2. Mengurangi ambiguity saat retrieval oleh LLM.
3. Menstandarkan relasi yang harus dipertahankan di rilis berikutnya.

## Relasi inti (wajib)
- `isPartOf`: setiap halaman volume dan release harus menunjuk ke korpus utama.
- `hasPart`: halaman pilar menautkan cluster/faq/glossary yang menjadi bagian ekosistem.
- `about`: halaman FAQ dan glossary mendeklarasikan topik The Cohesive Tetrad.
- `mentions`: halaman readiness/audit menyebut entitas kunci volume dan DOI.

## Contoh pola JSON-LD dokumen
```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "name": "Glossary Kanonik — The Cohesive Tetrad",
  "about": {
    "@type": "DefinedTermSet",
    "name": "The Cohesive Tetrad"
  },
  "isPartOf": {
    "@id": "https://github.com/suratkiade/risalah-saloqum"
  },
  "hasPart": [
    {"@id": "https://suratkiade.github.io/risalah-saloqum/volumes/t1-ontology/"},
    {"@id": "https://suratkiade.github.io/risalah-saloqum/faq/"}
  ]
}
```

## Halaman strategis yang harus saling terkait
- `index.md`
- `start-here.md`
- `glossary.md`
- `faq.md`
- `llm/index.md`
- `llm/readiness.md`
- `forensic-audit.md`

## Gate validasi semantik
- Setiap halaman strategis memiliki minimal 3 tautan internal kontekstual.
- Sumber pada `ai-faq.jsonl` harus menunjuk anchor FAQ yang valid.
- Link semantik utama (`/glossary/`, `/faq/`, `/ai-faq.jsonl`) wajib muncul di entrypoint.
