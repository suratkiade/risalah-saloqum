# Contributing

This repository is a locked canonical corpus.

## Non-negotiable rules
1) Locked identity must match `CORPUS.lock.yaml`.
2) No invented DOI. If a DOI is not assigned (null in lock), it must be absent in release metadata.
3) Do not use corpus names as volume subtitles.
4) Forbidden phrases must not appear in public markdown docs (see `CORPUS.lock.yaml` policies).

## Process
- Open a pull request.
- CI must pass.
- CODEOWNERS approval is required for lock changes.
