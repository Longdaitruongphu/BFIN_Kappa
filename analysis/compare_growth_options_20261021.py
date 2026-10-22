"""Frozen-2022 advisory comparison; does not rewrite the approved initial policy.

All portfolio formation uses the saved 2015-2022 Yahoo/French-derived series.
The 2023-2025 columns are evaluation only. No extra asset-weight caps are set.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

import interactive_surplus_portfolio_lab as lab

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/decision_review_20261021"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    train, evaluation, capm, _, sample, sim = lab.load_local_inputs()
    mu = lab.forecast_returns("CAPM", .04, .045, 0, 0, capm, None)
    candidates = lab.make_candidates(mu, sample.to_numpy(), sim.to_numpy(), .04, 4, None, None)
    historical_rf = pd.read_csv(ROOT / "data/processed/train_factors.csv").RF.mean() * 12
    candidates["Historical max Sharpe (Eta)"] = lab.optimize_weights(
        train.mean().to_numpy() * 12, sample.to_numpy(), lab.STOCKS,
        "sharpe", 4, historical_rf)
    names = ["100% USMV", "100% VTI", "ETF mix VTI 50% / USMV 50%",
             "Equal-weight 1/N", "Historical max Sharpe (Eta)", "Sample GMV", "Sample Max Sharpe",
             "Sample Max Utility A=4", "Single-index GMV",
             "Single-index Max Sharpe", "Single-index Max Utility A=4"]
    rows = []
    weight_rows = []
    eval_factors = pd.read_csv(ROOT / "data/processed/eval_factors.csv", parse_dates=["month"]).set_index("month")
    eval_rf = eval_factors.loc[evaluation.index, "RF"].to_numpy(float)
    wealth_frame = pd.DataFrame({"month": ["2022-12", *evaluation.index.strftime("%Y-%m").tolist()]})
    for name in names:
        w = candidates[name]
        m = lab.portfolio_metrics(name, w, mu, sample.to_numpy(), .04, 4,
                                  train, evaluation, .001, frequency="Annual")
        # The lab path charges turnover when resetting weights; add a 10bp
        # formation cost here so evaluation is on the initial cash budget.
        m["evaluation_CAGR_after_entry_cost"] = ((1 + m["evaluation_CAGR_2023_25"]) ** 3 / 1.001) ** (1 / 3) - 1
        monthly = lab.rebalanced_monthly_returns(evaluation, w, .001, frequency="Annual")
        # Charge the 10bp entry friction in the first evaluation month so all
        # out-of-sample metrics and the wealth path use a single convention.
        monthly[0] = (1 - .001) * (1 + monthly[0]) - 1
        wealth = np.r_[1.0, np.cumprod(1 + monthly)]
        dd = wealth / np.maximum.accumulate(wealth) - 1
        excess = monthly - eval_rf
        m["evaluation_vol_after_cost"] = float(np.std(monthly, ddof=1) * np.sqrt(12))
        m["evaluation_sharpe_after_cost"] = float(np.mean(excess) / np.std(monthly, ddof=1) * np.sqrt(12))
        m["evaluation_max_drawdown_after_cost"] = float(dd.min())
        wealth_frame[name] = np.r_[.999, wealth[1:]]
        m["model_used_to_form"] = "sample" if name.startswith("Sample") else "single-index" if name.startswith("Single-index") else "rule"
        m["utility_scored_on"] = "common 96-month sample covariance"
        sim_var = float(w @ sim.to_numpy() @ w)
        m["single_index_variance"] = sim_var
        m["single_index_volatility"] = float(np.sqrt(max(sim_var, 0.0)))
        m["single_index_sharpe"] = float((m["expected_return"] - .04) / m["single_index_volatility"])
        m["single_index_utility_A4"] = float(m["expected_return"] - 2 * sim_var)
        m["sim_utility_A4"] = m["single_index_utility_A4"]
        rows.append(m)
        weight_rows.append({"portfolio": name, **dict(zip(lab.ASSETS, w))})
    weight_frame = pd.DataFrame(weight_rows)
    asset_cols = lab.ASSETS
    weight_values = weight_frame[asset_cols].to_numpy(float)
    if not np.isfinite(weight_values).all() or (weight_values < -1e-9).any():
        raise ValueError("A candidate weight is missing, non-finite, or negative")
    if not np.allclose(weight_values.sum(axis=1), 1.0, atol=1e-8):
        raise ValueError("Candidate weights do not sum to 100%")
    if (weight_values > 1.0 + 1e-8).any():
        raise ValueError("A candidate exceeds the fully-invested single-asset limit")
    pd.DataFrame(rows).to_csv(OUT / "growth_candidate_comparison.csv", index=False)
    weight_frame.to_csv(OUT / "growth_candidate_weights.csv", index=False)
    wealth_frame.to_csv(OUT / "growth_candidate_evaluation_wealth.csv", index=False)

    # Factor explanation for the recommended target-weight growth portfolio.
    # This applies the 31-Dec-2022 decision weights retrospectively to the
    # training returns for diagnosis; it is not represented as a live history.
    rec_w = candidates["Sample Max Utility A=4"]
    factor_frame = pd.read_csv(ROOT / "data/processed/train_factors.csv", parse_dates=["month"]).set_index("month")
    factor_frame = factor_frame.loc[train.index, ["Mkt-RF", "SMB", "HML", "RF"]]
    portfolio_total = train.to_numpy(float) @ rec_w
    factor_rows = []
    for model, factors_used in (("CAPM", ["Mkt-RF"]), ("FF3", ["Mkt-RF", "SMB", "HML"])):
        x = sm.add_constant(factor_frame[factors_used])
        fit = sm.OLS(portfolio_total - factor_frame["RF"].to_numpy(float), x).fit(
            cov_type="HAC", cov_kwds={"maxlags": 3})
        alpha = float(fit.params["const"] * 12)
        alpha_ci = fit.conf_int().loc["const"].to_numpy(float) * 12
        row = {"security": "Recommended A=4 portfolio (retrospective target weights)",
               "model": model, "n": int(fit.nobs), "r_squared": float(fit.rsquared),
               "adjusted_r_squared": float(fit.rsquared_adj), "alpha_annual": alpha,
               "alpha_low": float(alpha_ci[0]), "alpha_high": float(alpha_ci[1]),
               "alpha_pvalue": float(fit.pvalues["const"])}
        for factor in ["Mkt-RF", "SMB", "HML"]:
            if factor in fit.params.index:
                ci = fit.conf_int().loc[factor].to_numpy(float)
                row[factor] = float(fit.params[factor])
                row[f"{factor}_low"] = float(ci[0]); row[f"{factor}_high"] = float(ci[1])
                row[f"{factor}_pvalue"] = float(fit.pvalues[factor])
        factor_rows.append(row)
    pd.DataFrame(factor_rows).to_csv(OUT / "growth_portfolio_factor_regressions.csv", index=False)

    # Window-stability check of the fixed model, with no post-2022 observations.
    factors = pd.read_csv(ROOT / "data/processed/train_factors.csv").set_index("month")
    last60 = train.tail(60)
    f60 = factors.loc[last60.index.strftime("%Y-%m")]
    excess = last60.to_numpy() - f60.RF.to_numpy()[:, None]
    mkt = f60["Mkt-RF"].to_numpy()
    beta60 = np.cov(excess.T, mkt, ddof=1)[:-1, -1] / np.var(mkt, ddof=1)
    mu60 = .04 + .045 * beta60
    cov60 = last60.cov().to_numpy() * 12
    w60 = lab.optimize_weights(mu60, cov60, lab.STOCKS, "utility", 4, .04)
    w96 = candidates["Sample Max Utility A=4"]
    sample_w = candidates["Sample Max Utility A=4"]
    index_w = candidates["Single-index Max Utility A=4"]
    window = {"formation_end": "2022-12", "comparison_start_96m": "2015-01",
              "comparison_start_60m": "2018-01", "absolute_weight_change_sum": float(np.abs(w60 - w96).sum()),
              "one_way_turnover_to_switch": float(np.abs(w60 - w96).sum() / 2),
              "sample_vs_single_index_one_way_turnover": float(np.abs(sample_w-index_w).sum()/2),
              "candidate_count": int(len(lab.ASSETS)),
              "candidate_asset_names": lab.ASSETS,
              "portfolio_count": int(len(weight_frame)),
              "weights_nonnegative": bool(min(sample_w.min(),index_w.min()) >= -1e-10),
              "weight_totals": {"sample_A4": float(sample_w.sum()), "single_index_A4": float(index_w.sum())},
              "extra_position_caps": None,
              "evaluation_convention": {"months": int(len(evaluation)), "frequency": "annual",
                                        "rebalance_cost_bps": 10, "entry_cost_bps": 10},
              "weights_60m": dict(zip(lab.ASSETS, map(float, w60))),
              "weights_96m": dict(zip(lab.ASSETS, map(float, w96)))}

    # Independently check all workbook FF3 intercept claims against its own price/factor cells.
    croot = ROOT / "outputs/role_c_audit/expanded"
    creturns = pd.read_csv(croot / "expanded_recomputed_returns.csv").set_index("month").loc["2015-01":"2022-12"]
    cfactors = pd.read_csv(croot / "expanded_factors.csv").set_index("month")
    claims = pd.read_csv(croot / "expanded_regression_claims.csv").set_index("ticker")
    x = sm.add_constant(cfactors[["Mkt-RF", "SMB", "HML"]])
    regrows = []
    for ticker, claim in claims.iterrows():
        fit = sm.OLS(creturns[ticker] - cfactors.RF, x).fit()
        regrows.append({"ticker": ticker, "claimed_alpha_monthly": claim.reported_alpha_monthly,
                        "recomputed_alpha_monthly": fit.params["const"],
                        "claimed_p": claim.reported_alpha_p, "recomputed_p": fit.pvalues["const"],
                        "abs_alpha_error": abs(claim.reported_alpha_monthly - fit.params["const"]),
                        "abs_p_error": abs(claim.reported_alpha_p - fit.pvalues["const"])})
    reg = pd.DataFrame(regrows)
    reg.to_csv(OUT / "role_c_ff3_independent_recalculation.csv", index=False)
    window["role_c_regressions_checked"] = len(reg)
    window["role_c_max_alpha_abs_error"] = float(reg.abs_alpha_error.max())
    window["role_c_max_p_abs_error"] = float(reg.abs_p_error.max())
    window["role_c_p_below_0_05"] = int((reg.recomputed_p < .05).sum())
    window["role_c_p_below_bonferroni_0_05_over_39"] = int((reg.recomputed_p < .05 / 39).sum())
    (OUT / "verification_receipt.json").write_text(json.dumps(window, indent=2), encoding="utf-8")
    print(json.dumps({k: window[k] for k in ["one_way_turnover_to_switch", "role_c_regressions_checked", "role_c_max_alpha_abs_error", "role_c_p_below_0_05", "role_c_p_below_bonferroni_0_05_over_39"]}, indent=2))


if __name__ == "__main__":
    main()
