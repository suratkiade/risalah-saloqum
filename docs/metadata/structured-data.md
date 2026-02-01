---
title: "Structured data"
description: "Panduan structured data (Schema.org JSON-LD) untuk SEO dan indexing LLM."
---

# Structured data

Repositori ini memakai Schema.org JSON-LD agar discovery oleh crawler, dataset indexer, dan LLM lebih presisi.

## Tingkat korpus (global)
- `/corpus.jsonld`  
Mewakili korpus sebagai Dataset dan menautkan semua DOI utama.

## Tingkat rilis (per volume, per bahasa)
Setiap folder rilis memuat:
- `abstract.jsonld` yang merepresentasikan ScholarlyArticle untuk DOI terkait.
- `abstract.md` sebagai sumber naratif dengan front matter.

Lokasi:
- `volumes/T1-ontology/ID/release/abstract.jsonld`
- `volumes/T1-ontology/EN/release/abstract.jsonld`
- `volumes/T4-methodology/ID/release/abstract.jsonld`
- `volumes/T4-methodology/EN/release/abstract.jsonld`

## Prinsip desain
1) DOI menjadi @id utama.
2) ID dan EN saling menaut via translationOfWork dan workTranslation.
3) Author dan ORCID selalu eksplisit.
4) License dan isAccessibleForFree selalu eksplisit.
