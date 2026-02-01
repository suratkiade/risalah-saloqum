# Risalah Saloqum / The Saloqum Treatise
Framework: The Cohesive Tetrad

Canonical corpus repository for the tetralogy of *The Cohesive Tetrad*, publishing canonical Indonesian (ID) editions and official English (EN) translations. This repo is designed for auditability, identity stability, and machine-readable dissemination (Markdown + JSON-LD).

Public identity (titles, subtitles, DOIs, author, ORCID, year, license) is strictly locked in `CORPUS.lock.yaml` and enforced by CI. Any drift will fail validation.

## What this repository publishes
Per volume and language, the repo publishes:
- `abstract.md` (human-readable abstract + locked front matter)
- `abstract_jsonld` (Schema.org JSON-LD for indexing and AI/SEO ingestion)
- release artifacts under `volumes/<T*>/<ID|EN>/release/`

## Locked identity (non-negotiable)
The following public identity fields must match `CORPUS.lock.yaml` and must remain consistent across:
- `abstract.md` front matter
- `abstract_jsonld`
- `CITATION.cff`

Locked identity:
- Author: Ade Zaenal Mutaqin
- ORCID: 0009-0001-4114-3679
- Year: 2025
- License: CC BY 4.0 (SPDX: CC-BY-4.0)

Institutional references:
- Affiliation: Faculty of Economics and Business, Pakuan University, Bogor, Indonesia
- Publisher: Saloqum Institute (Bogor, Indonesia)

## Canonical rule
- ID editions are canonical sources.
- EN editions are official translations derived from, and aligned to, the corresponding ID canonical edition.
- EN is not an independent canonical source for definitional, delimitative, or methodological references.

## Volumes (Tetralogy) and DOIs
| Volume | Domain | ID canonical DOI | EN official DOI |
|---|---|---|---|
| T1 | Ontology | 10.17605/OSF.IO/G8NEH | 10.17605/OSF.IO/SXZ9A |
| T4 | Methodology | 10.17605/OSF.IO/96BJ8 | 10.17605/OSF.IO/2SUDK |

## Repository structure
```
.github/workflows/
  validate-corpus-lock.yml
tools/
  validate_corpus_lock.py
volumes/
  T1-ontology/
    ID/release/
      abstract.md
      abstract_jsonld
    EN/release/
      abstract.md
      abstract_jsonld
  T2-epistemology/
    README.md
  T3-axiology/
    README.md
  T4-methodology/
    ID/release/
      abstract.md
      abstract_jsonld
    EN/release/
      abstract.md
      abstract_jsonld
CORPUS.lock.yaml
CITATION.cff
LICENSE
README.md
```

## Validation (CI lock enforcement)
CI rejects merges if any identity drift is detected.

- Workflow: `.github/workflows/validate-corpus-lock.yml`
- Validator: `tools/validate_corpus_lock.py`
- Lock source: `CORPUS.lock.yaml`

Run locally:
```bash
python tools/validate_corpus_lock.py
```

### Common failure causes
1. Missing `orcid` at root/front-matter level in `abstract.md`.
   - Validator expects `orcid:` to exist at the top level of YAML front matter, not only inside `author:`.
2. Subtitle drift (punctuation and whitespace included).
   - Example: trailing period vs no period.
   - Example: double space, different capitalization, or different quote character.
3. Identity mismatch between `abstract.md` and `CORPUS.lock.yaml`.
   - title, subtitle, doi, year, version, license
4. JSON-LD drift from locked identity.
   - `@id`, `url`, DOI value, author ORCID, language tag, or series fields differ.

## Authoring rules for `abstract.md`
Each `abstract.md` must:
- Start with YAML front matter (`---` ... `---`)
- Include required locked keys used by validation (exact keys and string values)
- Preserve exact subtitle spelling and punctuation as locked in `CORPUS.lock.yaml`
- Include `orcid:` at root/front-matter level (mandatory for CI)

Minimum required fields (typical):
- `schema`, `framework`, `corpus_id`, `tetralogy`, `title`, `subtitle`, `language`, `year`, `version`
- `doi`, `canonical_url`, (optional but recommended) `osf_landing_page`, `sameAs`
- `orcid` (root)
- `author` block with name, affiliation, email, orcid
- `license`, (recommended) `license_url`
- `keywords`, (optional) `osf_tags_suggested`

## JSON-LD rules (`abstract_jsonld`)
`abstract_jsonld` is Schema.org JSON-LD intended for:
- SEO and scholarly indexing
- AI ingestion (structured retrieval, metadata normalization)

To reduce validator brittleness and improve interoperability:
- Use `@type: "ScholarlyArticle"`
- Use DOI as both `@id` and `url` in `https://doi.org/<DOI>` form
- Represent ORCID as a URL: `https://orcid.org/0009-0001-4114-3679`
- Provide `identifier` array with DOI (PropertyValue)
- Provide `inLanguage` with BCP 47 tags:
  - ID: `id-ID`
  - EN: `en-US`
- Keep `publisher` consistent with locked identity (Organization recommended)
- Keep translation relation consistent:
  - EN should use `translationOfWork` pointing to the ID DOI
  - ID may use `workTranslation` pointing to the EN DOI

Recommended JSON-LD fields:
- `name`, `alternateName` (subtitle), `abstract`, `keywords`
- `datePublished`, `dateModified` (ISO 8601)
- `isAccessibleForFree: true`
- `license` (URL)

## Governance and contribution
- All changes must go through Pull Requests.
- Do not modify locked identity outside `CORPUS.lock.yaml`.
- If updating locked identity, update `CORPUS.lock.yaml` and all affected artifacts (both `abstract.md` and `abstract_jsonld`) in one PR, then confirm local validation passes.

## Citation
See `CITATION.cff`.

## License
This repository is licensed under CC BY 4.0. See `LICENSE`.

## Contact
Corresponding author: suratkiade@gmail.com  
ORCID: https://orcid.org/0009-0001-4114-3679  
