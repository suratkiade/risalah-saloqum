# The Cohesive Tetrad: Hakikat Kebenaran
Subjudul: Di Bawah Takhta Neraca

# The Cohesive Tetrad: The Nature of Truth
Subtitle: Beneath the Throne of the Measure

## Canonical identity (locked)
- Corpus (ID): Risalah Saloqum
- Corpus (EN): The Saloqum Treatise
- Framework: The Cohesive Tetrad
- Author: Ade Zaenal Mutaqin
- ORCID: 0009-0001-4114-3679
- Year: 2025
- License: CC BY 4.0 (SPDX: CC-BY-4.0)

## DOIs
- ID DOI (canonical): 10.17605/OSF.IO/G8NEH
- EN DOI (official translation): 10.17605/OSF.IO/SXZ9A

## Release structure
- `ID/release/`
  - `abstract.md`
  - `abstract.jsonld`
  - release PDF(s)
- `EN/release/`
  - `abstract.md`
  - `abstract.jsonld`
  - release PDF(s)

## Validation rules
This volume is validated against `CORPUS.lock.yaml`.
Any drift in title, subtitle, DOI, ORCID, year, or license will fail CI.

Practical checks before committing:
- In `abstract.md` front-matter, ensure `orcid` exists at root and matches ORCID lock.
- Ensure subtitle text matches the lock exactly, including punctuation.
- In `abstract.jsonld`, include the DOI URL in `@id` and `url`, and include ORCID at a stable location.
