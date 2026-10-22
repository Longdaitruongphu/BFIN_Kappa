"""Rebuild the 22 October initial decision from saved pre-2023 raw files.

Run from the package root: python analysis/run_initial.py
No network access, evaluation-period prices, or portfolio optimizer are used.
"""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "analysis/config.json").read_text(encoding="utf-8"))
TICKERS = CFG["stocks"] + CFG["etfs"]
RAW = ROOT / "data/raw/train"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest() -> dict:
    """Check the saved downloads against the dated, original retrieval record."""
    manifest = ROOT / "data/raw/retrieval_manifest.jsonl"
    entries = [json.loads(s) for s in manifest.read_text(encoding="utf-8").splitlines() if s.strip()]
    success = [e for e in entries if e.get("event") == "success"]
    assert len(success) == len(TICKERS) + 1, "Expected ten Yahoo files and one French ZIP"
    assert not any(e.get("event") == "run_complete" and e.get("failures") for e in entries)
    seen = set()
    for e in success:
        assert e.get("phase") == "train"
        rel = Path(e["file"].replace("\\", "/"))
        assert rel.parts[:3] == ("data", "raw", "train")
        assert rel not in seen
        seen.add(rel)
        assert sha256(ROOT / rel) == e["sha256"], f"Raw checksum mismatch: {rel}"
        if e.get("ticker"):
            assert e["ticker"] in TICKERS
            s = e["settings"]
            assert s["start"] == "2014-12-01" and s["end"] == "2023-01-01"
            assert s["interval"] == "1d" and s["auto_adjust"] is False
            assert s["actions"] is True and s["repair"] is False
    support_records = json.loads((ROOT / "data/raw/supporting/source_register.json").read_text(encoding="utf-8"))
    support_ok = support_failed = 0
    for item in support_records:
        if item["status"] == "downloaded":
            path = ROOT / Path(item["filename"].replace("\\", "/"))
            assert path.is_file() and sha256(path) == item["sha256"]
            support_ok += 1
        elif item["status"] == "failed":
            assert item.get("error")
            support_failed += 1
        else:
            raise AssertionError("Unexpected supporting-source status")
    assert support_ok == 4 and support_failed == 10
    return {"files_verified": len(success), "supporting_files_verified": support_ok,
            "supporting_download_failures_logged": support_failed,
            "retrieved_utc": min(e["recorded_utc"] for e in success)}


def monthly_returns() -> tuple[pd.DataFrame, dict]:
    """Use final trading-day adjusted prices; Dec 2014 is a return baseline only."""
    prices = {}
    last_days = {}
    first_last = {}
    for ticker in TICKERS:
        frame = pd.read_csv(RAW / f"{ticker}_daily.csv")
        assert "Adj Close" in frame and "Date" in frame
        frame["day"] = pd.to_datetime(frame["Date"].astype(str).str[:10])
        assert not frame["day"].duplicated().any(), ticker
        assert frame["day"].max() <= pd.Timestamp("2022-12-31"), ticker
        assert frame["Adj Close"].notna().all() and (frame["Adj Close"] > 0).all(), ticker
        frame = frame.sort_values("day")
        month = frame["day"].dt.to_period("M")
        ends = frame.groupby(month, sort=True).tail(1)
        idx = ends["day"].dt.to_period("M")
        prices[ticker] = pd.Series(ends["Adj Close"].to_numpy(), index=idx.to_numpy())
        last_days[ticker] = pd.Series(ends["day"].dt.strftime("%Y-%m-%d").to_numpy(), index=idx.to_numpy())
        first_last[ticker] = [str(frame["day"].min().date()), str(frame["day"].max().date())]
    panel = pd.DataFrame(prices)
    expected = pd.period_range("2015-01", "2022-12", freq="M")
    returns = panel.pct_change(fill_method=None).reindex(expected)
    assert returns.shape == (96, 10) and not returns.isna().any().any()
    dates = pd.DataFrame(last_days).reindex(expected)
    assert (dates.nunique(axis=1) == 1).all(), "Candidate month-end trading dates differ"
    returns.index.name = "month"
    returns.to_csv(OUT / "training_monthly_returns.csv", float_format="%.15g")
    return returns, first_last


def french_factors(months: pd.PeriodIndex) -> pd.DataFrame:
    path = RAW / "F-F_Research_Data_Factors_CSV.zip"
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        assert len(names) == 1
        lines = archive.read(names[0]).decode("utf-8-sig").splitlines()
    header = next(line for line in lines if "Mkt-RF" in line and "SMB" in line)
    rows = [line for line in lines if re.match(r"^\s*\d{6},", line)]
    factors = pd.read_csv(io.StringIO(header + "\n" + "\n".join(rows)), index_col=0)
    factors.columns = factors.columns.str.strip()
    factors.index = pd.PeriodIndex(factors.index.astype(str), freq="M")
    assert not factors.index.duplicated().any()
    factors = factors.astype(float).loc[months, ["Mkt-RF", "SMB", "HML", "RF"]] / 100.0
    assert not factors.isna().any().any()
    factors.index.name = "month"
    factors.to_csv(OUT / "training_ff3_decimal.csv", float_format="%.15g")
    return factors


def candidate_statistics(returns: pd.DataFrame, factors: pd.DataFrame) -> pd.DataFrame:
    """CAPM is a scenario forecast; FF3 in the source set is explanatory only."""
    market_excess = factors["Mkt-RF"].to_numpy()
    risk_free = factors["RF"].to_numpy()
    x = np.column_stack([np.ones(len(market_excess)), market_excess])
    records = []
    for ticker in TICKERS:
        r = returns[ticker].to_numpy()
        alpha_monthly, beta = np.linalg.lstsq(x, r - risk_free, rcond=None)[0]
        mu = CFG["forecast_rf"] + beta * CFG["forecast_erp"]
        sigma = np.std(r, ddof=1) * np.sqrt(12)
        records.append({"ticker": ticker, "capm_beta": beta,
                        "historical_alpha_annual_descriptive": 12 * alpha_monthly,
                        "forecast_return_annual": mu, "historical_volatility_annual": sigma,
                        "utility_A4": mu - 0.5 * CFG["risk_aversion"] * sigma**2})
    table = pd.DataFrame(records)
    table.to_csv(OUT / "candidate_statistics.csv", index=False, float_format="%.15g")
    return table


def allocation() -> dict:
    """Dedicate full Beta face and Delta final payment; four early coupons stay cash."""
    wealth = CFG["initial_wealth"]
    beta_units = CFG["payment_2024"] / 1000
    delta_units = CFG["payment_2027"] / 1035
    beta_value = beta_units * 922.78
    delta_value = delta_units * 986.07
    bond_value = beta_value + delta_value
    bond_fee = bond_value * CFG["bond_cost_rate"]
    growth_investment = (wealth - bond_value - bond_fee) / (1 + CFG["equity_cost_rate"])
    growth_fee = growth_investment * CFG["equity_cost_rate"]
    coupon = delta_units * 35
    goal = CFG["real_goal"] * (1 + CFG["inflation_base"]) ** 8
    stress_goal = CFG["real_goal"] * (1 + CFG["inflation_education_stress"]) ** 8
    def required_cagr(target: float) -> float:
        # Coupon at each Dec 2023..26 remains uninvested cash earning zero.
        return ((target - 4 * coupon) / growth_investment) ** (1 / 8) - 1
    assert abs(beta_units * 1000 - CFG["payment_2024"]) < 1e-7
    assert abs(delta_units * 1035 - CFG["payment_2027"]) < 1e-7
    assert abs(beta_value + delta_value + bond_fee + growth_investment + growth_fee - wealth) < 1e-6
    result = {
        "beta_units": beta_units, "beta_initial_value": beta_value,
        "delta_units": delta_units, "delta_initial_value": delta_value,
        "bond_fee": bond_fee, "growth_etf": CFG["selected_growth_etf"],
        "growth_initial_value": growth_investment, "growth_fee": growth_fee,
        "total_initial_budget": wealth, "delta_coupon_annual": coupon,
        "four_early_coupons_cash_2030_zero_interest": 4 * coupon,
        "payment_2024_covered": beta_units * 1000,
        "payment_2027_covered": delta_units * 1035,
        "nominal_goal_2030_base": goal,
        "nominal_goal_2030_education_stress": stress_goal,
        "required_growth_cagr_base": required_cagr(goal),
        "required_growth_cagr_education_stress": required_cagr(stress_goal),
    }
    return result


def main() -> None:
    policy_path = ROOT / "policy/initial_policy_proposed.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    assert policy["case_decision_date"] == CFG["case_date"]
    assert policy["additional_stock_or_etf_weight_caps"] is None
    assert policy["initial_decision"]["growth"] == "100% USMV after stated entry costs"
    assert policy["base_assumptions"]["CPI_planning"] == CFG["inflation_base"]
    assert policy["base_assumptions"]["education_cost_stress"] == CFG["inflation_education_stress"]
    assert policy["base_assumptions"]["bond_execution_cost"] == CFG["bond_cost_rate"]
    assert policy["base_assumptions"]["equity_execution_cost"] == CFG["equity_cost_rate"]
    source = verify_manifest()
    returns, dates = monthly_returns()
    factors = french_factors(returns.index)
    candidates = candidate_statistics(returns, factors)
    alloc = allocation()
    growth_weights = {ticker: float(ticker == CFG["selected_growth_etf"]) for ticker in TICKERS}
    benchmark_weights = {ticker: float(ticker == CFG["growth_benchmark"]) for ticker in TICKERS}
    assert sum(growth_weights.values()) == sum(benchmark_weights.values()) == 1.0
    pd.DataFrame([{"ticker": ticker, "growth_weight": growth_weights[ticker],
                   "growth_initial_dollars": growth_weights[ticker] * alloc["growth_initial_value"],
                   "benchmark_weight": benchmark_weights[ticker]} for ticker in TICKERS]).to_csv(
        OUT / "growth_portfolio_weights.csv", index=False, float_format="%.15g")
    pick = candidates.set_index("ticker").loc[["USMV", "VTI"]]
    mu_u, mu_v = pick["forecast_return_annual"]
    var_u, var_v = pick["historical_volatility_annual"] ** 2
    crossover = 2 * (mu_v - mu_u) / (var_v - var_u)
    assert 2.0 < crossover < 3.2
    assert pick.loc["USMV", "utility_A4"] > pick.loc["VTI", "utility_A4"]
    risk_rows = []
    for aversion in (2, 4, 6, 8):
        usmv_utility = mu_u - 0.5 * aversion * var_u
        vti_utility = mu_v - 0.5 * aversion * var_v
        risk_rows.append({"risk_aversion_A": aversion, "USMV_utility": usmv_utility,
                          "VTI_utility": vti_utility,
                          "higher_utility_of_two_ETFs": "USMV" if usmv_utility > vti_utility else "VTI"})
    pd.DataFrame(risk_rows).to_csv(OUT / "risk_preference.csv", index=False, float_format="%.15g")
    alloc.update({"growth_weights": growth_weights, "benchmark_weights": benchmark_weights,
                  "data_source": source, "policy_sha256": sha256(policy_path),
                  "config_sha256": sha256(ROOT / "analysis/config.json"),
                  "training_months": len(returns),
                  "training_start": str(returns.index.min()), "training_end": str(returns.index.max()),
                  "raw_date_ranges": dates, "utility_crossover_A_usmv_vs_vti": crossover,
                  "forecast_comparison": pick[["capm_beta", "forecast_return_annual",
                                               "historical_volatility_annual", "utility_A4"]].to_dict(orient="index"),
                  "caveat": "Retrospective case; saved 2026 vendor histories may be revised. The 2023-25 evaluation is excluded."})
    (OUT / "initial_decision_rebuild.json").write_text(json.dumps(alloc, indent=2) + "\n", encoding="utf-8")
    # Reproduce the material sample-utility comparator printed on the PDF.
    from compare_initial_candidates import main as compare_initial_candidates
    compare_initial_candidates()
    print("PASS: 11 training raw sources + 4 supporting files checked; 10 SEC failures logged; 96 training months; no evaluation data or network used.")
    print(f"Initial USMV ${alloc['growth_initial_value']:,.2f}; Beta ${alloc['beta_initial_value']:,.2f}; Delta ${alloc['delta_initial_value']:,.2f}.")
    print(f"CPI goal ${alloc['nominal_goal_2030_base']:,.2f}; required sleeve CAGR {100*alloc['required_growth_cagr_base']:.4f}%.")


if __name__ == "__main__":
    main()
