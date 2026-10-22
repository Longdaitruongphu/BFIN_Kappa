"""Hash and archive only the documented 22 October submission files.

This does not rewrite the original case decision, raw data, or report content.
Run after run_initial.py, both report builders, and verify_submission.py.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
MANIFEST = ROOT / "submission_manifest.json"
ARCHIVE = PROJECT / "deliverables/Kappa_Initial_22Oct2026_Submission.zip"
NEW = [
    "SUBMISSION_CHECKLIST.md",
    "analysis/build_initial_docx.py",
    "analysis/build_release_archive.py",
    "analysis/verify_submission.py",
    "deliverables/Kappa_Initial_Decision_Record_22Oct2026.docx",
    "outputs/max_utility_A4_weights.csv",
    "outputs/max_utility_preference.csv",
    "outputs/sample_utility_robustness.json",
    "outputs/submission_readiness_20261021.json",
    "requirements-document.txt",
]


def main():
    old = json.loads(MANIFEST.read_text(encoding="utf-8"))
    paths = sorted(set(row["path"] for row in old["files"]) | set(NEW))
    files = []
    for name in paths:
        path = ROOT / name
        if not path.is_file():
            raise FileNotFoundError(path)
        payload = path.read_bytes()
        files.append({"path": name, "bytes": len(payload),
                      "sha256": hashlib.sha256(payload).hexdigest()})
    manifest = {
        "prepared_utc": datetime.now(timezone.utc).isoformat(),
        "status": "prepared; not uploaded or trustee-authorized",
        "case_information_cutoff": "2022-12-31",
        "initial_record_pages": 2,
        "word_record_pages_checked_in_microsoft_word": 2,
        "files": files,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    ARCHIVE.parent.mkdir(exist_ok=True)
    with ZipFile(ARCHIVE, "w", compression=ZIP_DEFLATED, compresslevel=9) as zipfile:
        for row in files:
            zipfile.write(ROOT / row["path"], "Kappa_Initial_22Oct2026/" + row["path"])
        zipfile.write(MANIFEST, "Kappa_Initial_22Oct2026/submission_manifest.json")
    with ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(files) + 1
    print(f"PASS: {len(files)} files hashed; archive {ARCHIVE}")


if __name__ == "__main__":
    main()
