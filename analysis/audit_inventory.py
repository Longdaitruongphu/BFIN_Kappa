"""Create or verify a dated, non-destructive inventory of the current project.

Historical package manifests are intentionally kept as snapshots. This script
reports their drift rather than editing them. It excludes only the local virtual
environment, Git internals, bytecode/cache files, and its two self-referential
outputs from the current inventory.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "CURRENT_MANIFEST_2026-10-20.csv"
REPORT = ROOT / "logs/current_inventory_audit_2026-10-20.json"
EXCLUDED_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache"}
EXCLUDED_FILES = {MANIFEST.resolve(), REPORT.resolve()}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def inventory() -> list[dict[str, str | int]]:
    result = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in rel.parts) or path.resolve() in EXCLUDED_FILES:
            continue
        result.append({"path": rel.as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)})
    return result


def compare_manifest(path: Path) -> dict:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        entries = list(csv.DictReader(stream))
    missing, changed = [], []
    for entry in entries:
        target = ROOT / entry["path"]
        if not target.is_file():
            missing.append(entry["path"])
        elif target.stat().st_size != int(entry["bytes"]) or sha(target) != entry["sha256"].lower():
            changed.append(entry["path"])
    return {"listed": len(entries), "missing": missing, "changed": changed}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--create", action="store_true", help="Write a new current-state manifest and report")
    parser.add_argument("--verify", action="store_true", help="Verify the existing current-state manifest")
    args = parser.parse_args()
    if args.create == args.verify:
        parser.error("Choose exactly one of --create or --verify")
    report = {
        "historical_manifests": {
            name: compare_manifest(ROOT / name)
            for name in ["PACKAGE_MANIFEST.csv", "CODEX_HANDOFF_MANIFEST.csv"]
        },
        "excluded": [".git/", ".venv/", "__pycache__/", ".pytest_cache/",
                     MANIFEST.relative_to(ROOT).as_posix(), REPORT.relative_to(ROOT).as_posix()],
    }
    if args.create:
        entries = inventory()
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        with MANIFEST.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["path", "bytes", "sha256"])
            writer.writeheader()
            writer.writerows(entries)
        report["current_manifest"] = {"listed": len(entries), "missing": [], "changed": [],
                                      "total_bytes": sum(int(e["bytes"]) for e in entries)}
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    else:
        report["current_manifest"] = compare_manifest(MANIFEST)
    print(json.dumps(report, indent=2))
    assert not report["current_manifest"]["missing"] and not report["current_manifest"]["changed"]


if __name__ == "__main__":
    main()
