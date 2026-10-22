"""Reproduce the CPI-base / HEPI-stress goal arithmetic from frozen inputs.

This is a deterministic hurdle calculation, not a return forecast or success
probability. Surplus Delta coupons are held in cash at the frozen 0% base rate.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "policy" / "frozen_policy.json"
OUT = ROOT / "outputs" / "mandate_preparedness" / "inflation_goal_sensitivity.csv"


def main() -> None:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    assumptions = policy["forecast_assumptions"]
    funding = policy["funding"]
    bond_consideration = funding["bond_cost"]
    total_resources = assumptions["initial_wealth"]
    base_bond_rate = funding["bond_fees"] / bond_consideration
    base_growth_cost_rate = funding["equity_fees"] / funding["equity_investment"]
    retained_coupon_cash = funding["terminal_cash"]
    real_goal = assumptions["real_goal"]
    years = 8
    growth_sleeve_cagr_case = 0.05
    inflation_scenarios = [
        ("CPI primary", assumptions["inflation"]),
        ("HEPI education-cost stress", 0.03),
    ]
    fee_scenarios = [
        ("User-selected base", base_bond_rate, base_growth_cost_rate),
        ("Lower-friction sensitivity", 0.0, 0.0005),
    ]

    rows = []
    for fee_label, bond_rate, growth_cost_rate in fee_scenarios:
        bond_fee = bond_consideration * bond_rate
        growth_capital = (total_resources - bond_consideration - bond_fee) / (1 + growth_cost_rate)
        growth_fee = growth_capital * growth_cost_rate
        for inflation_label, planning_inflation in inflation_scenarios:
            nominal_goal = real_goal * (1 + planning_inflation) ** years
            required_cagr = ((nominal_goal - retained_coupon_cash) / growth_capital) ** (
                1 / years
            ) - 1
            terminal_wealth = growth_capital * (1 + growth_sleeve_cagr_case) ** years + retained_coupon_cash
            real_terminal_wealth = terminal_wealth / (1 + planning_inflation) ** years
            rows.append(
                {
                    "fee_scenario": fee_label,
                    "bond_transaction_cost_bps": bond_rate * 10_000,
                    "growth_asset_transaction_cost_bps": growth_cost_rate * 10_000,
                    "planning_inflation_scenario": inflation_label,
                    "planning_inflation": planning_inflation,
                    "real_goal_2022_usd": real_goal,
                    "years": years,
                    "bond_consideration_usd": bond_consideration,
                    "bond_transaction_cost_usd": bond_fee,
                    "initial_growth_capital_usd_net_of_entry_cost": growth_capital,
                    "growth_entry_cost_usd": growth_fee,
                    "surplus_coupon_cash_2030_usd_at_0pct": retained_coupon_cash,
                    "nominal_2030_goal_usd": nominal_goal,
                    "required_growth_sleeve_cagr_with_coupon_cash_0pct": required_cagr,
                    "illustrative_growth_cagr_not_forecast": growth_sleeve_cagr_case,
                    "illustrative_2030_nominal_wealth_usd": terminal_wealth,
                    "illustrative_2030_real_wealth_2022_usd": real_terminal_wealth,
                    "illustrative_nominal_gap_usd_positive_is_shortfall": nominal_goal - terminal_wealth,
                    "illustrative_real_gap_2022_usd_positive_is_shortfall": real_goal - real_terminal_wealth,
                }
            )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    # Guard against accidental drift in the reviewed base and fee-sensitivity arithmetic.
    base_cpi, base_hepi, alt_cpi, alt_hepi = rows
    assert abs(base_cpi["initial_growth_capital_usd_net_of_entry_cost"] - funding["equity_investment"]) < 0.02
    assert abs(base_cpi["nominal_2030_goal_usd"] - 9_747_223.18) < 0.02
    assert abs(base_cpi["required_growth_sleeve_cagr_with_coupon_cash_0pct"] - 0.0483648) < 1e-6
    assert abs(base_hepi["nominal_2030_goal_usd"] - 10_134_160.65) < 0.02
    assert abs(base_hepi["required_growth_sleeve_cagr_with_coupon_cash_0pct"] - 0.0537429) < 1e-6
    assert abs(alt_cpi["initial_growth_capital_usd_net_of_entry_cost"] - 6_352_343.13) < 0.02
    assert abs(alt_cpi["required_growth_sleeve_cagr_with_coupon_cash_0pct"] - 0.0482411) < 1e-6
    assert abs(alt_hepi["required_growth_sleeve_cagr_with_coupon_cash_0pct"] - 0.0536186) < 1e-6
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(rows)} fee/inflation combinations); arithmetic checks passed.")


if __name__ == "__main__":
    main()
