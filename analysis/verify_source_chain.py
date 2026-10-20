"""Independent, read-only verification of saved Yahoo and French source chains.

This does not fetch data and does not import the production analysis modules.
It recalculates each month from saved daily observations and FF3 ZIP bytes.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/raw/retrieval_manifest.jsonl"
OUT = ROOT / "outputs/role_c_audit/source_chain_receipt.json"
TICKERS = ["AAPL", "MSFT", "JPM", "JNJ", "PG", "XOM", "CAT", "NEE", "VTI", "USMV"]
SLICES = {"train": ("2015-01", "2022-12", 96), "eval": ("2023-01", "2025-12", 36)}
FACTORS = ["Mkt-RF", "SMB", "HML", "RF"]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_processed(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    entries = [json.loads(s) for s in MANIFEST.read_text(encoding="utf-8").splitlines() if s.strip()]
    successes = [e for e in entries if e.get("event") == "success"]
    failures = [e for e in entries if e.get("event") == "run_complete" and e.get("failures")]
    assert len(successes) == 22, f"Expected 20 Yahoo and 2 FF3 successes, found {len(successes)}"
    assert not failures, failures
    manifest_files: dict[tuple[str, str], dict] = {}
    for e in successes:
        rel = Path(e["file"].replace("\\", "/"))
        source = ROOT / rel
        assert source.is_file(), source
        assert digest(source) == e["sha256"], source
        key = (e["phase"], e.get("ticker", "FF3"))
        assert key not in manifest_files, key
        manifest_files[key] = e

    price_max_error = 0.0
    return_max_error = 0.0
    factor_max_error = 0.0
    yahoo_checked = 0
    factors_checked = 0
    phase_details = {}
    for phase, (first, last, count) in SLICES.items():
        price_rows = read_processed(ROOT / f"data/processed/{phase}_month_end_adjusted_prices.csv")
        return_rows = read_processed(ROOT / f"data/processed/{phase}_monthly_returns.csv")
        p_lookup = {r["month"]: r for r in price_rows}
        r_lookup = {r["month"]: r for r in return_rows}
        assert len(r_lookup) == count and min(r_lookup) == first and max(r_lookup) == last
        for ticker in TICKERS:
            e = manifest_files[(phase, ticker)]
            settings = e["settings"]
            assert settings["interval"] == "1d" and settings["auto_adjust"] is False
            assert settings["back_adjust"] is False and settings["actions"] is True
            assert settings["repair"] is False and settings["keepna"] is True
            raw_rows = read_processed(ROOT / Path(e["file"].replace("\\", "/")))
            assert len(raw_rows) == e["rows"] and "Adj Close" in raw_rows[0]
            monthly: dict[str, tuple[str, float]] = {}
            seen_days: set[str] = set()
            for row in raw_rows:
                day = row["Date"][:10]
                assert day not in seen_days, (phase, ticker, "duplicate date", day)
                seen_days.add(day)
                assert settings["start"] <= day < settings["end"], (phase, ticker, "date outside request", day)
                month = day[:7]
                value = float(row["Adj Close"])
                assert value > 0, (ticker, day)
                if month not in monthly or day > monthly[month][0]:
                    monthly[month] = (day, value)
            for month in r_lookup:
                y, m = map(int, month.split("-"))
                prev = f"{y - 1}-12" if m == 1 else f"{y}-{m - 1:02d}"
                assert prev in monthly and month in monthly, (phase, ticker, month)
                actual_price = monthly[month][1]
                actual_return = actual_price / monthly[prev][1] - 1
                perr = abs(actual_price - float(p_lookup[month][ticker]))
                rerr = abs(actual_return - float(r_lookup[month][ticker]))
                price_max_error = max(price_max_error, perr)
                return_max_error = max(return_max_error, rerr)
                assert perr < 1e-9 and rerr < 1e-12, (phase, ticker, month, perr, rerr)
                yahoo_checked += 1

        factor_entry = manifest_files[(phase, "FF3")]
        factor_file = ROOT / Path(factor_entry["file"].replace("\\", "/"))
        with zipfile.ZipFile(factor_file) as z:
            assert len(z.namelist()) == 1
            contents = z.read(z.namelist()[0]).decode("utf-8-sig")
        raw_factors = {}
        for line in contents.splitlines():
            if re.match(r"^\s*\d{6},", line):
                parts = [p.strip() for p in line.split(",")]
                month = parts[0][:4] + "-" + parts[0][4:]
                raw_factors[month] = {k: float(v) / 100 for k, v in zip(FACTORS, parts[1:5])}
        processed = read_processed(ROOT / f"data/processed/{phase}_factors.csv")
        assert len(processed) == count and processed[0]["month"] == first and processed[-1]["month"] == last
        for row in processed:
            month = row["month"]
            assert month in raw_factors
            for factor in FACTORS:
                error = abs(raw_factors[month][factor] - float(row[factor]))
                factor_max_error = max(factor_max_error, error)
                assert error < 1e-14, (phase, month, factor, error)
                factors_checked += 1
        phase_details[phase] = {"months": count, "start": first, "end": last,
                                "yahoo_version": successes[0].get("versions", {}).get("yfinance"),
                                "ff3_sha256": factor_entry["sha256"]}

    receipt = {
        "status": "PASS",
        "scope": "saved raw bytes, manifest hashes, monthly Yahoo adjusted-close arithmetic, and FF3 ZIP conversion; no live vendor re-download",
        "source_files_hashed": len(successes),
        "yahoo_monthly_returns_recalculated": yahoo_checked,
        "factor_values_recalculated": factors_checked,
        "max_abs_adjusted_price_error": price_max_error,
        "max_abs_monthly_return_error": return_max_error,
        "max_abs_factor_error": factor_max_error,
        "phases": phase_details,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
