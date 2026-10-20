"""Read-only, standard-library checks of key case and evaluation equations."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "outputs/tables"
OUT = ROOT / "outputs/role_c_audit/core_equations_receipt.json"


def rows(name):
    with (TABLE / name).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def close(actual, expected, tolerance=1e-8):
    assert math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance), (actual, expected)


def main():
    cfg = json.loads((ROOT / "analysis/config.json").read_text())
    summary = json.loads((TABLE / "funding_summary.json").read_text())
    decision = json.loads((TABLE / "decision_summary.json").read_text())
    p_beta, p_delta = 922.78, 986.07
    beta_units = cfg["payment_year_2"] / 1000
    delta_coupon_per_unit = 35
    delta_units = cfg["payment_year_5"] / (1000 + delta_coupon_per_unit)
    beta_cost = beta_units * p_beta
    delta_cost = delta_units * p_delta
    bond_fee = cfg["bond_cost_per_dollar_traded"] * (beta_cost + delta_cost)
    equity = (cfg["initial_wealth"] - beta_cost - delta_cost - bond_fee) / (1 + cfg["equity_cost_per_dollar_traded"])
    equity_fee = cfg["equity_cost_per_dollar_traded"] * equity
    surplus = 4 * delta_units * delta_coupon_per_unit
    nominal_goal = cfg["real_goal"] * (1 + cfg["inflation"]) ** 8
    required_cagr = ((nominal_goal - surplus) / equity) ** (1 / 8) - 1
    for key, value in {
        "beta_face": beta_units * 1000,
        "delta_face": delta_units * 1000,
        "beta_cost": beta_cost,
        "delta_cost": delta_cost,
        "bond_fees": bond_fee,
        "equity_investment": equity,
        "equity_fees": equity_fee,
        "terminal_cash": surplus,
        "nominal_goal": nominal_goal,
        "required_equity_cagr": required_cagr,
    }.items():
        close(float(summary[key]), value, 1e-9)
    close(beta_cost + delta_cost + bond_fee + equity + equity_fee, 12_000_000)
    cashflows = rows("funding_cashflows.csv")
    assert len(cashflows) == 8
    close(float(cashflows[1]["beta_maturity"]), 2_400_000)
    close(float(cashflows[1]["mandatory_payment"]), 2_400_000)
    close(float(cashflows[4]["delta_coupon"]) + float(cashflows[4]["delta_principal"]), 3_600_000)
    close(float(cashflows[4]["mandatory_payment"]), 3_600_000)
    assert min(float(r["cumulative_cash_zero_reinvestment"]) for r in cashflows) >= -1e-7

    for bond in rows("bond_metrics.csv"):
        n = int(bond["maturity"])
        coupon = float(bond["coupon"]) * 1000
        ytm = float(bond["ytm"])
        price = sum((coupon + (1000 if t == n else 0)) / (1 + ytm) ** t for t in range(1, n + 1))
        close(price, float(bond["price"]), 1e-8)

    pref = {(r["strategy"], float(r["risk_aversion"])): r for r in rows("risk_preference.csv")}
    for (ticker, aversion), r in pref.items():
        mu = float(r["expected_return"])
        variance = float(r["annual_variance"])
        close(float(r["certainty_equivalent"]), mu - aversion * variance / 2)
    u, v = pref[("USMV", 4.0)], pref[("VTI", 4.0)]
    close(float(decision["recommended_CE"]), float(u["certainty_equivalent"]))
    close(float(decision["alternative_CE"]), float(v["certainty_equivalent"]))
    threshold = 2 * (float(v["expected_return"]) - float(u["expected_return"])) / (
        float(v["annual_variance"]) - float(u["annual_variance"])
    )
    close(float(decision["risk_aversion_threshold"]), threshold, 1e-8)

    factors = {r["month"]: float(r["RF"]) for r in csv.DictReader((ROOT / "data/processed/eval_factors.csv").open())}
    reported = {r["strategy"]: r for r in rows("evaluation_performance.csv")}
    eval_results = {}
    for strategy, filename in [("Recommended", "evaluation_Recommended_path.csv"),
                               ("Benchmark VTI", "evaluation_Benchmark_VTI_path.csv")]:
        path = rows(filename)
        assert len(path) == 36 and path[0]["month"] == "2023-01" and path[-1]["month"] == "2025-12"
        monthly = [float(r["return_net"]) for r in path]
        excess = [float(r["return_net"]) - factors[r["month"]] for r in path]
        terminal = math.prod(1 + x for x in monthly)
        close(terminal, float(path[-1]["wealth"]), 1e-9)
        stats = reported[strategy]
        close(float(stats["total_return"]), terminal - 1, 1e-9)
        close(float(stats["cagr"]), terminal ** (12 / 36) - 1, 1e-9)
        close(float(stats["annual_volatility"]), statistics.stdev(monthly) * math.sqrt(12), 1e-9)
        close(float(stats["annual_sharpe"]),
              statistics.mean(excess) / statistics.stdev(excess) * math.sqrt(12), 1e-9)
        eval_results[strategy] = {"terminal_per_initial_dollar": terminal,
                                  "cagr": float(stats["cagr"]),
                                  "sharpe": float(stats["annual_sharpe"])}

    receipt = {"status": "PASS", "bond_quotes_revalued": 5,
               "checks": ["full USD 12m cost-inclusive budget", "fixed payment coverage",
                          "zero-reinvestment surplus", "2030 inflation and CAGR",
                          "certainty-equivalent and aversion threshold",
                          "36-month cost-inclusive compounded evaluation and RF Sharpe"],
               "nominal_goal": nominal_goal, "required_equity_cagr": required_cagr,
               "evaluation": eval_results}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
