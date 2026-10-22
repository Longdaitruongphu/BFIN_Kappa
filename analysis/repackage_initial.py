"""Refresh the prepared (not submitted) 22-Oct archive after an audited edit."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "submission_2026-10-22"
MANIFEST = PACKAGE / "submission_manifest.json"
ARCHIVE = ROOT / "BFIN_Kappa_Initial_22Oct2026.zip"


def sha(data: bytes):
    return hashlib.sha256(data).hexdigest()


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    required_new = ["analysis/compare_initial_candidates.py", "outputs/sample_utility_robustness.json"]
    known = {entry["path"] for entry in manifest["files"]}
    for rel in required_new:
        if rel not in known:
            manifest["files"].append({"path": rel})
    manifest["files"].sort(key=lambda item: item["path"])
    for entry in manifest["files"]:
        source = PACKAGE / entry["path"]
        payload = source.read_bytes()
        entry["bytes"] = len(payload)
        entry["sha256"] = sha(payload)
    manifest["prepared_utc"] = datetime.now(timezone.utc).isoformat()
    manifest["status"] = "prepared; not uploaded or authorized"
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with ZipFile(ARCHIVE, "w", compression=ZIP_DEFLATED) as z:
        for entry in manifest["files"]:
            z.write(PACKAGE / entry["path"], entry["path"])
        z.write(MANIFEST, "submission_manifest.json")
    with ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        for entry in manifest["files"]:
            assert sha(z.read(entry["path"])) == entry["sha256"]
        assert json.loads(z.read("submission_manifest.json"))["files"] == manifest["files"]
    print(f"PASS: {len(manifest['files'])} hashed files + manifest in {ARCHIVE}")


if __name__ == "__main__":
    main()
