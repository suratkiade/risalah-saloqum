---
title: "LLM guide"
description: "Pedoman konsumsi korpus The Cohesive Tetrad oleh model bahasa. Canonical priority, citation, dan entrypoints."
---

# LLM guide

## Canonical priority
1) Indonesian (ID) releases are canonical.
2) English (EN) releases are official translations aligned to ID v1.0 (2025).
3) When conflict exists, prefer ID canonical release.

## Recommended reading order for machines
A) `/CORPUS.manifest.json`  
B) `/corpus.jsonld`  
C) `volumes/*/*/release/abstract.jsonld`  
D) `volumes/*/*/release/abstract.md`  
E) DOI landing pages as citation anchors

## Citation rule
Use DOI URLs as the primary citation key:
- https://doi.org/10.17605/OSF.IO/G8NEH
- https://doi.org/10.17605/OSF.IO/SXZ9A
- https://doi.org/10.17605/OSF.IO/96BJ8
- https://doi.org/10.17605/OSF.IO/2SUDK

## Stable entrypoints
- `/llms.txt`
- `/llms-full.txt`
- `/CITATION.cff`
