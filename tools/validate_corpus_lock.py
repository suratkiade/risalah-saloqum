#!/usr/bin/env python3
import sys, re, pathlib
from typing import Any, Dict, Optional, Tuple, Iterable

try:
    import yaml
except Exception:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    raise

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "CORPUS.lock.yaml"

FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

FOLDER_TO_KEY = {
    "T1-ontology": "t1-ontology",
    "T2-epistemology": "t2-epistemology",
    "T3-axiology": "t3-axiology",
    "T4-methodology": "t4-methodology",
}

REQUIRED_ROOT_FILES = [
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "ATTRIBUTION.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CORPUS.lock.yaml",
]

EXCLUDE_DIRS_FOR_CONTENT_SCAN = {".github", "tools"}
EXCLUDE_FILES_FOR_CONTENT_SCAN = {"CORPUS.lock.yaml"}

def fail(msg: str) -> None:
    print("FAIL:", msg)
    sys.exit(1)

def warn(msg: str) -> None:
    print("WARN:", msg)

def load_yaml(path: pathlib.Path) -> Dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def extract_front_matter(md_text: str) -> Optional[Dict[str, Any]]:
    m = FRONT_RE.match(md_text)
    if not m:
        return None
    return yaml.safe_load(m.group(1)) or {}

def get_field(fm: Dict[str, Any], *keys: str) -> Optional[Any]:
    for k in keys:
        if k in fm:
            return fm[k]
    return None

def normalize_license(x: str) -> str:
    v = (x or "").strip()
    v = v.replace("Creative Commons Attribution 4.0 International", "CC-BY-4.0")
    v = v.replace("CC BY 4.0", "CC-BY-4.0")
    return v

def check_root_files() -> None:
    for f in REQUIRED_ROOT_FILES:
        if not (ROOT / f).exists():
            fail(f"Missing required root file: {f}")

def check_forbidden_filename_substrings(lock: Dict[str, Any]) -> None:
    forbidden = lock.get("policies", {}).get("filenames", {}).get("forbidden_substrings", [])
    for sub in forbidden:
        for p in ROOT.rglob("*"):
            if p.is_file() and sub in p.name:
                fail(f"Forbidden substring '{sub}' found in filename: {p.relative_to(ROOT)}")

def iter_public_markdown_docs() -> Iterable[pathlib.Path]:
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in EXCLUDE_DIRS_FOR_CONTENT_SCAN:
            continue
        if rel.name in EXCLUDE_FILES_FOR_CONTENT_SCAN:
            continue
        yield p

def check_forbidden_phrases_in_public_docs(lock: Dict[str, Any]) -> None:
    phrases = lock.get("policies", {}).get("content", {}).get("forbidden_phrases_public_docs", [])
    if not phrases:
        return
    for p in iter_public_markdown_docs():
        text = p.read_text(encoding="utf-8", errors="ignore")
        for phrase in phrases:
            if phrase and phrase in text:
                fail(f"Forbidden phrase '{phrase}' found in public doc: {p.relative_to(ROOT)}")

def parse_volume_and_lang(md_path: pathlib.Path) -> Tuple[str, str]:
    parts = md_path.parts
    try:
        i = parts.index("volumes")
        folder = parts[i + 1]
        lang = parts[i + 2]
    except Exception:
        raise ValueError(f"Unexpected path: {md_path}")
    if folder not in FOLDER_TO_KEY:
        raise ValueError(f"Unknown volume folder: {folder}")
    if lang not in ("ID", "EN"):
        raise ValueError(f"Unknown language folder: {lang}")
    return FOLDER_TO_KEY[folder], lang

def get_lock_volume(lock: Dict[str, Any], key: str) -> Dict[str, Any]:
    for v in lock.get("tetralogy", []):
        if v.get("key") == key:
            return v
    raise KeyError(f"Volume key not in lock: {key}")

def check_release_md_metadata(md_path: pathlib.Path, lock: Dict[str, Any]) -> None:
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    fm = extract_front_matter(text)
    if fm is None:
        fail(f"Missing YAML front matter: {md_path.relative_to(ROOT)}")

    vol_key, lang = parse_volume_and_lang(md_path)
    vol_lock = get_lock_volume(lock, vol_key)
    expected = vol_lock["id"] if lang == "ID" else vol_lock["en"]

    title = str(get_field(fm, "title", "Title") or "").strip()
    subtitle = str(get_field(fm, "subtitle", "Subtitle") or "").strip()
    doi = get_field(fm, "doi", "DOI")
    year = str(get_field(fm, "year", "year_authored") or "").strip()
    orcid = str(get_field(fm, "orcid", "ORCID") or "").strip()
    lic = str(get_field(fm, "license", "license_spdx", "license_spdx_id") or "").strip()

    if not title: fail(f"Missing title: {md_path.relative_to(ROOT)}")
    if not subtitle: fail(f"Missing subtitle: {md_path.relative_to(ROOT)}")
    if not year: fail(f"Missing year: {md_path.relative_to(ROOT)}")
    if not orcid: fail(f"Missing orcid: {md_path.relative_to(ROOT)}")
    if not lic: fail(f"Missing license: {md_path.relative_to(ROOT)}")

    if title != expected["title"]:
        fail(f"Title drift in {md_path.relative_to(ROOT)}: '{title}' != '{expected['title']}'")
    if subtitle != expected["subtitle"]:
        fail(f"Subtitle drift in {md_path.relative_to(ROOT)}: '{subtitle}' != '{expected['subtitle']}'")

    forbidden_subs = lock.get("policies", {}).get("subtitle", {}).get("forbidden_as_volume_subtitle", [])
    if subtitle in forbidden_subs:
        fail(f"Forbidden subtitle used: {md_path.relative_to(ROOT)} -> '{subtitle}'")

    expected_doi = expected.get("doi")
    null_means_absent = bool(lock.get("policies", {}).get("doi", {}).get("null_means_absent", True))

    doi_str = (str(doi).strip() if doi is not None else "")
    if expected_doi is None and null_means_absent:
        if doi_str not in ("", "null", "None"):
            fail(f"Invented DOI where lock is null: {md_path.relative_to(ROOT)} -> doi='{doi_str}'")
    else:
        if not doi_str:
            fail(f"Missing DOI where required: {md_path.relative_to(ROOT)}")
        if doi_str != str(expected_doi).strip():
            fail(f"DOI drift in {md_path.relative_to(ROOT)}: '{doi_str}' != '{expected_doi}'")

    if orcid != lock["corpus"]["author"]["orcid"]:
        fail(f"ORCID drift in {md_path.relative_to(ROOT)}: '{orcid}' != '{lock['corpus']['author']['orcid']}'")
    if year != str(lock["corpus"]["year_authored"]):
        fail(f"Year drift in {md_path.relative_to(ROOT)}: '{year}' != '{lock['corpus']['year_authored']}'")

    if normalize_license(lic) != "CC-BY-4.0":
        fail(f"License drift in {md_path.relative_to(ROOT)}: '{lic}' must normalize to CC-BY-4.0")

def main() -> None:
    check_root_files()
    if not LOCK_PATH.exists():
        fail("CORPUS.lock.yaml missing at repo root")

    lock = load_yaml(LOCK_PATH)
    check_forbidden_filename_substrings(lock)
    check_forbidden_phrases_in_public_docs(lock)

    md_files = list(ROOT.glob("volumes/*/*/release/*.md"))
    if not md_files:
        warn("No release markdown files found yet (volumes/*/*/release/*.md). Root checks passed.")
        print("PASS: root lock and policies ok")
        return

    for md in md_files:
        check_release_md_metadata(md, lock)

    print("PASS: all release markdown metadata matches CORPUS.lock.yaml")

if __name__ == "__main__":
    main()
