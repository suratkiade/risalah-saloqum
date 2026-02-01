---
title: "Structured data"
description: "Dokumentasi structured data schema.org JSON-LD untuk korpus dan rilis. Diprioritaskan untuk mesin pencari dan LLM."
keywords: "structured data, JSON-LD, schema.org, ScholarlyArticle, Dataset, DOI, Risalah Saloqum, The Cohesive Tetrad"
---

# Structured data

Repositori ini menyiapkan structured data sebagai identitas utama untuk mesin pencari dan sistem AI.

## 1) Corpus JSON-LD
File: `corpus.jsonld` (root repo, dipublikasikan ke root portal)

## 2) Release JSON-LD
Setiap rilis di `volumes/**/release/` membawa `abstract.jsonld` yang mengikuti schema.org.

Di bawah ini adalah contoh JSON-LD untuk rilis Tetralogi 4 (ID) yang Anda gunakan.

```json
{
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  "@id": "https://doi.org/10.17605/OSF.IO/96BJ8",
  "url": "https://doi.org/10.17605/OSF.IO/96BJ8",
  "mainEntityOfPage": "https://osf.io/96bj8/",
  "name": "The Cohesive Tetrad: Bahasa Kebenaran",
  "headline": "Akhir dari Perdebatan adalah Awal dari Amal.",
  "inLanguage": "id",
  "version": "v1.0",
  "datePublished": "2025",
  "copyrightYear": 2025,
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "isAccessibleForFree": true,
  "creativeWorkStatus": "Preprint",
  "identifier": [
    {
      "@type": "PropertyValue",
      "propertyID": "DOI",
      "value": "10.17605/OSF.IO/96BJ8"
    }
  ],
  "author": {
    "@type": "Person",
    "name": "Ade Zaenal Mutaqin",
    "email": "suratkiade@gmail.com",
    "affiliation": {
      "@type": "Organization",
      "name": "Faculty of Economics and Business, Pakuan University, Bogor, Indonesia"
    },
    "identifier": "https://orcid.org/0009-0001-4114-3679"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Saloqum Institute",
    "location": {
      "@type": "Place",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Bogor",
        "addressCountry": "ID"
      }
    }
  },
  "isPartOf": {
    "@type": "CreativeWorkSeries",
    "name": "Risalah Saloqum",
    "isPartOf": {
      "@type": "CreativeWork",
      "name": "The Cohesive Tetrad"
    }
  },
  "sameAs": [
    "https://osf.io/96bj8/"
  ]
}
