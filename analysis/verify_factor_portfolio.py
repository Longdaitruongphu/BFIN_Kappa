"""Independent numerical audit of FF3/CAPM and covariance portfolio outputs.

Uses saved processed observations but recomputes linear algebra independently
from the production analysis module. It does not reselect or alter the policy.
"""
from __future__ import annotations

import json
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data/processed"
TABLE = ROOT / "outputs/tables"
OUT = ROOT / "outputs/role_c_audit/factor_portfolio_receipt.json"


def max_error(a, b):
    return float(np.max(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))


def main():
    cfg = json.loads((ROOT / "analysis/config.json").read_text())
    tickers = cfg["stocks"] + cfg["etfs"]
    r = pd.read_csv(PROC / "train_monthly_returns.csv", index_col="month")[tickers]
    f = pd.read_csv(PROC / "train_factors.csv", index_col="month")
    assert list(r.index) == list(f.index) and len(r) == 96

    sample = np.cov(r.to_numpy(), rowvar=False, ddof=1) * 12
    mkt = f["Mkt-RF"].to_numpy()
    excess = r.to_numpy() - f["RF"].to_numpy()[:, None]
    beta = np.array([np.cov(excess[:, i], mkt, ddof=1)[0, 1] / np.var(mkt, ddof=1)
                     for i in range(len(tickers))])
    residual = excess - excess.mean(axis=0) - np.outer(mkt - mkt.mean(), beta)
    single = np.outer(beta, beta) * np.var(mkt, ddof=1) * 12 + np.diag(np.var(residual, axis=0, ddof=1) * 12)
    mu = cfg["forecast_rf"] + beta * cfg["forecast_erp"]

    saved_sample = pd.read_csv(TABLE / "sample_covariance.csv", index_col=0).loc[tickers, tickers].to_numpy()
    saved_single = pd.read_csv(TABLE / "single_index_covariance.csv", index_col=0).loc[tickers, tickers].to_numpy()
    saved_inputs = pd.read_csv(TABLE / "expected_return_inputs.csv").set_index("ticker").loc[tickers]
    covariance_error = max(max_error(sample, saved_sample), max_error(single, saved_single))
    beta_error = max_error(beta, saved_inputs["beta"])
    mu_error = max_error(mu, saved_inputs["expected_arithmetic_return"])
    assert covariance_error < 1e-10 and beta_error < 1e-10 and mu_error < 1e-10

    regressions = pd.read_csv(TABLE / "factor_regressions.csv")
    regression_error = 0.0
    regression_r2_error = 0.0
    hac_interval_error = 0.0
    hac_pvalue_error = 0.0
    normal = NormalDist()
    zcrit = normal.inv_cdf(0.975)
    for _, row in regressions.iterrows():
        security = row["security"]
        model = row["model"]
        predictors = ["Mkt-RF"] if model == "CAPM" else ["Mkt-RF", "SMB", "HML"]
        x = np.column_stack([np.ones(len(r)), f[predictors].to_numpy()])
        y = r[security].to_numpy() - f["RF"].to_numpy()
        coef = np.linalg.lstsq(x, y, rcond=None)[0]
        fitted = x @ coef
        error = y - fitted
        r2 = 1 - float(np.sum((y - fitted) ** 2) / np.sum((y - y.mean()) ** 2))
        regression_error = max(regression_error, abs(12 * coef[0] - float(row["alpha_annual"])))
        regression_r2_error = max(regression_r2_error, abs(r2 - float(row["r_squared"])))
        for i, name in enumerate(predictors, start=1):
            regression_error = max(regression_error, abs(coef[i] - float(row[name])))
        # Bartlett Newey-West covariance with three monthly lags and no
        # small-sample correction, matching the documented production setting.
        scores = x * error[:, None]
        meat = scores.T @ scores
        for lag in range(1, 4):
            weighted = scores[lag:].T @ scores[:-lag]
            meat += (1 - lag / 4) * (weighted + weighted.T)
        bread = np.linalg.inv(x.T @ x)
        se = np.sqrt(np.diag(bread @ meat @ bread))
        for i, name in enumerate(["alpha"] + predictors):
            multiplier = 12 if name == "alpha" else 1
            lower = (coef[i] - zcrit * se[i]) * multiplier
            upper = (coef[i] + zcrit * se[i]) * multiplier
            pvalue = 2 * (1 - normal.cdf(abs(coef[i] / se[i])))
            prefix = "alpha" if name == "alpha" else name
            hac_interval_error = max(hac_interval_error,
                                     abs(lower - float(row[prefix + "_low"])),
                                     abs(upper - float(row[prefix + "_high"])))
            hac_pvalue_error = max(hac_pvalue_error, abs(pvalue - float(row[prefix + "_pvalue"])))
        assert int(row["n"]) == 96
    assert regression_error < 1e-9 and regression_r2_error < 1e-9
    assert hac_interval_error < 1e-8 and hac_pvalue_error < 1e-8

    portfolios = pd.read_csv(TABLE / "portfolio_candidates.csv").set_index("strategy")
    portfolio_error = 0.0
    for name, row in portfolios.iterrows():
        w = row[tickers].to_numpy(dtype=float)
        assert np.all(w >= -1e-8) and abs(w.sum() - 1) < 1e-8, name
        assert np.max(w[:len(cfg["stocks"])]) <= cfg["individual_stock_limit"] + 1e-8, name
        assert w[:len(cfg["stocks"])].sum() <= cfg["aggregate_stock_limit"] + 1e-8, name
        portfolio_error = max(portfolio_error, abs(float(row["forecast_return"]) - w @ mu))
        portfolio_error = max(portfolio_error, abs(float(row["sample_vol"]) - np.sqrt(w @ sample @ w)))
        portfolio_error = max(portfolio_error, abs(float(row["index_vol"]) - np.sqrt(w @ single @ w)))
        if name != "Eta_historical_Sharpe":
            risk_matrix = sample if name.startswith("Sample_") else single
            ce = w @ mu - float(row["A"]) * (w @ risk_matrix @ w) / 2
            portfolio_error = max(portfolio_error, abs(float(row["model_CE"]) - ce))
    assert portfolio_error < 1e-9
    sw = portfolios.loc["Sample_A4", tickers].to_numpy(dtype=float)
    iw = portfolios.loc["Single_index_A4", tickers].to_numpy(dtype=float)
    turnover = float(np.abs(sw - iw).sum() / 2)
    decision = json.loads((TABLE / "decision_summary.json").read_text())
    assert abs(turnover - decision["sample_vs_index_weight_turnover"]) < 1e-9

    receipt = {
        "status": "PASS",
        "training_months": len(r),
        "candidate_count": len(tickers),
        "regressions_recomputed": len(regressions),
        "portfolio_rows_checked": len(portfolios),
        "max_abs_covariance_error": covariance_error,
        "max_abs_beta_error": beta_error,
        "max_abs_expected_return_error": mu_error,
        "max_abs_regression_coefficient_error": regression_error,
        "max_abs_regression_r_squared_error": regression_r2_error,
        "max_abs_hac_interval_error": hac_interval_error,
        "max_abs_hac_pvalue_error": hac_pvalue_error,
        "max_abs_portfolio_metric_error": portfolio_error,
        "sample_vs_index_one_way_turnover": turnover,
        "scope_limit": "Forecast calibration and simulation probabilities are not independently validated by this script",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
