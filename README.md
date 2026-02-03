# Risalah Saloqum / The Saloqum Treatise
Framework: The Cohesive Tetrad

Canonical corpus repository. Public identity (titles, subtitles, DOIs, author, ORCID, year, license) is locked in `CORPUS.lock.yaml` and enforced by CI (`validate-corpus-lock`). Any drift is rejected.

## Canonical identity (locked)
- Author: Ade Zaenal Mutaqin
- ORCID: 0009-0001-4114-3679
- Affiliation: Faculty of Economics and Business, Pakuan University, Bogor, Indonesia
- Year: 2025
- License: CC BY 4.0 (SPDX: CC-BY-4.0)

## Teleological manifesto and governance
- Read the teleological mandate in `README_MANIFESTO.md`.

## Repository structure
This repository is organized per Tetralogy volume. Each volume contains:
- `ID/release/` for the Indonesian canonical edition (source of record)
- `EN/release/` for the official English translation aligned to the Indonesian canonical edition
- `abstract.md` and `abstract.jsonld` as machine-readable identity and discovery metadata (SEO and AI indexing)
- the corresponding `.pdf` and `.md` release artifacts

Quick navigation:
- T1 Ontology: `volumes/T1-ontology/`
- T2 Epistemology: `volumes/T2-epistemology/`
- T3 Axiology: `volumes/T3-axiology/`
- T4 Methodology: `volumes/T4-methodology/`

## Canonical references (DOI)
The following items are part of the locked public identity for discovery, citation, and cross-repository consistency.

### Tetralogy 1 (Ontology)
- ID canonical: "The Cohesive Tetrad: Hakikat Kebenaran" (Di Bawah Takhta Neraca)  
  DOI: 10.17605/OSF.IO/G8NEH
- EN official translation: "The Cohesive Tetrad: The Nature of Truth" (Beneath the Throne of the Measure)  
  DOI: 10.17605/OSF.IO/SXZ9A

### Tetralogy 4 (Methodology)
- ID canonical: "The Cohesive Tetrad: Bahasa Kebenaran" (Akhir dari Perdebatan adalah Awal dari Amal.)  
  DOI: 10.17605/OSF.IO/96BJ8
- EN official translation: "The Cohesive Tetrad: The Languages of Truth" (The end of debate is the beginning of Amal)  
  DOI: 10.17605/OSF.IO/2SUDK

## Release artifacts and metadata paths
Each release folder contains four core files: the release text, the PDF, `abstract.md`, and `abstract.jsonld`.

### T1 Ontology
- ID: `volumes/T1-ontology/ID/release/`
  - `Risalah-Saloqum_The-Cohesive-Tetrad-Hakikat-Kebenaran_ID_v1.0.md`
  - `Risalah-Saloqum_The-Cohesive-Tetrad-Hakikat-Kebenaran_ID_v1.0.pdf`
  - `abstract.md`
  - `abstract.jsonld`
- EN: `volumes/T1-ontology/EN/release/`
  - `Saloqum-Treatise_The-Cohesive-Tetrad-The-Nature-of-Truth_EN_v1.0.md`
  - `Saloqum-Treatise_The-Cohesive-Tetrad-The-Nature-of-Truth_EN_v1.0.pdf`
  - `abstract.md`
  - `abstract.jsonld`

### T4 Methodology
- ID: `volumes/T4-methodology/ID/release/`
  - `Risalah-Saloqum_The-Cohesive-Tetrad-Bahasa-Kebenaran_ID_v1.0.md`
  - `Risalah-Saloqum_The-Cohesive-Tetrad-Bahasa-Kebenaran_ID_v1.0.pdf`
  - `abstract.md`
  - `abstract.jsonld`
- EN: `volumes/T4-methodology/EN/release/`
  - `Saloqum-Treatise_The-Cohesive-Tetrad-The-Languages-of-Truth_EN_v1.0.md`
  - `Saloqum-Treatise_The-Cohesive-Tetrad-The-Languages-of-Truth_EN_v1.0.pdf`
  - `abstract.md`
  - `abstract.jsonld`

## Citation
Use the repository-level `CITATION.cff` as the authoritative citation entry for GitHub and reference managers.

## Governance and integrity rules
- Do not modify locked identity outside `CORPUS.lock.yaml`.
- If locked identity changes are required, update `CORPUS.lock.yaml` and all affected release metadata files in a single PR.
- Keep `abstract.md` and `abstract.jsonld` consistent with each other and with `CORPUS.lock.yaml`.
- Prefer minimal, auditable diffs: identity changes must be explicit, intentional, and reviewable.

## License
CC BY 4.0. See `LICENSE` for details.
