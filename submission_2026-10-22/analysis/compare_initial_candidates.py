"""Reproduce the sample A=4 challenger from the saved training outputs.

The long-only quadratic program is solved by enumerating feasible active sets
for ten securities. No unseen 2023-25 data and no extra position caps enter.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def optimum(mu: np.ndarray, cov: np.ndarray, a: float = 4.0) -> np.ndarray:
    n = len(mu)
    best = None
    best_u = -np.inf
    for size in range(1, n + 1):
        for active in itertools.combinations(range(n), size):
            ix = np.array(active)
            block = np.empty((size + 1, size + 1))
            block[:size, :size] = a * cov[np.ix_(ix, ix)]
            block[:size, size] = 1.0
            block[size, :size] = 1.0
            block[size, size] = 0.0
            try:
                solution = np.linalg.solve(block, np.r_[mu[ix], 1.0])
            except np.linalg.LinAlgError:
                continue
            positive = solution[:size]
            if np.min(positive) < -1e-8:
                continue
            w = np.zeros(n)
            w[ix] = np.maximum(positive, 0.0)
            w /= w.sum()
            utility = float(w @ mu - .5 * a * w @ cov @ w)
            if utility > best_u:
                best, best_u = w, utility
    if best is None:
        raise RuntimeError("No feasible long-only weight vector")
    return best


def portfolio_metrics(w: np.ndarray, mu: np.ndarray, cov: np.ndarray, a: float) -> dict:
    expected = float(w @ mu)
    variance = float(w @ cov @ w)
    return {"expected_return": expected, "volatility": variance ** .5,
            "variance": variance, "utility": expected - .5 * a * variance}


def capm_inputs(returns: pd.DataFrame, factors: pd.DataFrame):
    f = factors.loc[returns.index]
    market = f["Mkt-RF"].to_numpy(float)
    excess = returns.to_numpy(float) - f.RF.to_numpy(float)[:, None]
    beta = np.array([np.cov(excess[:, i], market, ddof=1)[0, 1] /
                     np.var(market, ddof=1) for i in range(excess.shape[1])])
    return .04 + .045 * beta, returns.cov().to_numpy(float) * 12


def main():
    returns = pd.read_csv(OUT / "training_monthly_returns.csv").set_index("month")
    factors = pd.read_csv(OUT / "training_ff3_decimal.csv").set_index("month")
    assert len(returns) == 96 and returns.index[0] == "2015-01" and returns.index[-1] == "2022-12"
    assert list(factors.index) == list(returns.index)
    mu96, cov96 = capm_inputs(returns, factors)
    w96 = optimum(mu96, cov96)
    mu60, cov60 = capm_inputs(returns.iloc[-60:], factors)
    w60 = optimum(mu60, cov60)
    metrics96 = portfolio_metrics(w96, mu96, cov96, 4.0)
    portfolio_return = metrics96["expected_return"]
    variance = metrics96["variance"]
    preference = []
    for a in (2.0, 4.0, 6.0, 8.0):
        w = optimum(mu96, cov96, a)
        metrics = portfolio_metrics(w, mu96, cov96, a)
        preference.append({"risk_aversion_A": int(a), **metrics,
                           "weights": dict(zip(returns.columns, map(float, w)))})
    preference_rows = [{k: row[k] for k in ("risk_aversion_A", "expected_return", "volatility", "variance", "utility")}
                       for row in preference]
    pd.DataFrame(preference_rows).to_csv(OUT / "max_utility_preference.csv", index=False,
                                         float_format="%.15g")
    weights_a4 = pd.DataFrame({"ticker": returns.columns, "weight": w96})
    weights_a4["initial_sleeve_usd"] = weights_a4["weight"] * 6_346_350.71328671
    weights_a4.to_csv(OUT / "max_utility_A4_weights.csv", index=False, float_format="%.15g")
    data = {
        "cutoff": "2022-12", "estimation_months": 96,
        "forecast_method": "CAPM RF 4%, ERP 4.5%, alpha 0",
        "risk_method": "annualized sample covariance from monthly adjusted returns",
        "objective": "maximum utility A=4, long-only, weights sum 1, no additional caps",
        "expected_return": portfolio_return,
        "volatility": variance ** .5,
        "utility_A4": metrics96["utility"],
        "weights_96m": dict(zip(returns.columns, map(float, w96))),
        "weights_60m": dict(zip(returns.columns, map(float, w60))),
        "one_way_turnover_96m_to_60m": float(np.abs(w96 - w60).sum() / 2),
        "risk_preference_grid": preference,
        "constraints": "long-only; weights sum to one; no additional security caps",
    }
    (OUT / "sample_utility_robustness.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: sample utility A4 {data['utility_A4']:.6f}; 60m switch {data['one_way_turnover_96m_to_60m']:.2%}")
    return data


if __name__ == "__main__":
    main()
