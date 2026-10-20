"""Build one self-contained Codex handoff ZIP with hashes and essential QA evidence."""
from pathlib import Path
import csv, datetime, hashlib, json, zipfile

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
TARGET = WORKSPACE / "Kappa_Codex_Handoff_2026-10-16.zip"
TEMP_TARGET = WORKSPACE / "Kappa_Codex_Handoff_2026-10-16.building"
MANIFEST = ROOT / "CODEX_HANDOFF_MANIFEST.csv"

EXCLUDED_PARTS = {"__pycache__", "node_modules", ".yf_cache", "matplotlib"}
EXCLUDED_SUFFIXES = {".pyc"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def include(path):
    rel = path.relative_to(ROOT)
    if not path.is_file() or path.is_symlink():
        return False
    if path == MANIFEST:
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    if any(part in EXCLUDED_PARTS for part in rel.parts):
        return False
    if rel.parts and rel.parts[0].startswith(".chart-data-"):
        return False
    if rel.parts and rel.parts[0] == ".slide_build":
        allowed = (
            rel.as_posix() == ".slide_build/validation.json"
            or rel.as_posix() == ".slide_build/candidate.pptx.inspect.ndjson"
            or rel.as_posix().startswith(".slide_build/final/")
        )
        return allowed
    return True


def main():
    files = [p for p in sorted(ROOT.rglob("*")) if include(p)]
    with MANIFEST.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "bytes", "sha256"])
        for path in files:
            writer.writerow([path.relative_to(ROOT).as_posix(), path.stat().st_size, sha256(path)])

    metadata = {
        "handoff_created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "project_root_in_archive": "BFIN_Kappa",
        "start_here": "BFIN_Kappa/CODEX_HANDOFF.md",
        "confirmed_language": "English",
        "confirmed_recommendation": "Payment bonds plus USMV",
        "frozen_policy_sha256": "21b4ec3fb864144e7b56e54c668ebaed9c96d5a1771564b50c892700978c9f5c",
        "included_files_excluding_manifest": len(files),
    }

    if TEMP_TARGET.exists():
        raise FileExistsError(f"Refusing to overwrite stale temporary handoff: {TEMP_TARGET}")
    with zipfile.ZipFile(TEMP_TARGET, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=7) as archive:
        archive.writestr("HANDOFF_METADATA.json", json.dumps(metadata, indent=2))
        for path in files + [MANIFEST]:
            archive.write(path, "BFIN_Kappa/" + path.relative_to(ROOT).as_posix())

    with zipfile.ZipFile(TEMP_TARGET) as archive:
        assert archive.testzip() is None
        names = set(archive.namelist())
        required = {
            "HANDOFF_METADATA.json",
            "BFIN_Kappa/CODEX_HANDOFF.md",
            "BFIN_Kappa/CHECKPOINT.md",
            "BFIN_Kappa/reference/BFIN-WS2026-Group_Assignment.pdf",
            "BFIN_Kappa/policy/frozen_policy.json",
            "BFIN_Kappa/deliverables/Kappa_Committee_Memo.pdf",
            "BFIN_Kappa/deliverables/Kappa_Committee_Presentation.pptx",
            "BFIN_Kappa/data/raw/retrieval_manifest.jsonl",
            "BFIN_Kappa/CODEX_HANDOFF_MANIFEST.csv",
        }
        missing = required - names
        assert not missing, sorted(missing)

    TEMP_TARGET.replace(TARGET)
    receipt = {
        **metadata,
        "archive": TARGET.name,
        "archive_bytes": TARGET.stat().st_size,
        "archive_sha256": sha256(TARGET),
        "zip_integrity": "passed",
        "required_file_check": "passed",
    }
    (WORKSPACE / "Kappa_Codex_Handoff_2026-10-16.receipt.json").write_text(
        json.dumps(receipt, indent=2), encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
