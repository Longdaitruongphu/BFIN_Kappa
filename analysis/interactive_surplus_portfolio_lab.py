"""Interactive, editable surplus-portfolio comparison for the Kappa case.

The assignment forbids borrowing, short selling and derivatives, but does not
prescribe an optimal portfolio or additional security-weight limits. This tool
therefore defaults to long-only with NO extra per-asset or direct-stock caps.
Any optional limits entered in the GUI are scenario assumptions, not approved
IPS rules. All estimation data stop at 2022-12; 2023-25 is evaluation only.

Run from the project root:
    .venv\\Scripts\\python.exe analysis\\interactive_surplus_portfolio_lab.py
Headless calculation checks:
    .venv\\Scripts\\python.exe analysis\\interactive_surplus_portfolio_lab.py --self-test
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import numpy as np
import pandas as pd
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
TABLE = ROOT / "outputs" / "tables"
DEFAULT_OUTPUT = ROOT / "outputs" / "figures"
CONFIG = json.loads((ROOT / "analysis" / "config.json").read_text(encoding="utf-8"))
STOCKS = list(CONFIG["stocks"])
ETFS = list(CONFIG["etfs"])
ASSETS = STOCKS + ETFS
SURPLUS_USD = 6_346_350.713286715
SURPLUS_COUPONS_USD = 486_956.52
REAL_GOAL_USD = 8_000_000.0
YEARS = 8


def load_local_inputs():
    """Load only saved project data; never fetch data or use evaluation returns for fitting."""
    train_df = pd.read_csv(DATA / "train_monthly_returns.csv", parse_dates=["month"])
    train_df = train_df.set_index("month").loc[:, ASSETS].sort_index()
    if not train_df.index.to_period("M").equals(pd.period_range("2015-01", "2022-12", freq="M")):
        raise ValueError("Training input must contain 96 months ending no later than Dec 2022")
    eval_df = pd.read_csv(DATA / "eval_monthly_returns.csv", parse_dates=["month"])
    eval_df = eval_df.set_index("month").loc[:, ASSETS].sort_index()
    if not eval_df.index.to_period("M").equals(pd.period_range("2023-01", "2025-12", freq="M")):
        raise ValueError("Evaluation input must be the separate Jan 2023-Dec 2025 window")
    if not np.isfinite(train_df.to_numpy()).all() or not np.isfinite(eval_df.to_numpy()).all():
        raise ValueError("Returns contain missing or non-finite values; no filling is allowed")
    capm = pd.read_csv(TABLE / "expected_return_inputs.csv").set_index("ticker").loc[ASSETS]
    factors = pd.read_csv(DATA / "train_factors.csv", parse_dates=["month"]).set_index("month").sort_index()
    factors = factors.loc[train_df.index, ["Mkt-RF", "SMB", "HML", "RF"]]
    x = np.column_stack([np.ones(len(factors)), factors[["Mkt-RF", "SMB", "HML"]].to_numpy(float)])
    ff3 = {}
    for ticker in ASSETS:
        excess = train_df[ticker].to_numpy(float) - factors["RF"].to_numpy(float)
        ff3[ticker] = np.linalg.lstsq(x, excess, rcond=None)[0][1:]
    ff3 = pd.DataFrame(ff3, index=["Mkt-RF", "SMB", "HML"]).T.loc[ASSETS]
    sample_cov = pd.read_csv(TABLE / "sample_covariance.csv", index_col=0).loc[ASSETS, ASSETS]
    index_cov = pd.read_csv(TABLE / "single_index_covariance.csv", index_col=0).loc[ASSETS, ASSETS]
    for label, matrix in (("sample", sample_cov), ("single-index", index_cov)):
        a = matrix.to_numpy(float)
        if not np.allclose(a, a.T, atol=1e-9) or np.linalg.eigvalsh(a).min() < -1e-8:
            raise ValueError(f"{label} covariance must be symmetric and positive semidefinite")
    return train_df, eval_df, capm, ff3, sample_cov, index_cov


def forecast_returns(model, rf, market_erp, smb_premium, hml_premium, capm, ff3):
    """Annual arithmetic forecast; alpha is deliberately zero and stated explicitly."""
    if model == "CAPM":
        return rf + capm.beta.to_numpy(float) * market_erp
    return (rf + ff3["Mkt-RF"].to_numpy(float) * market_erp
            + ff3["SMB"].to_numpy(float) * smb_premium
            + ff3["HML"].to_numpy(float) * hml_premium)


def rebalanced_monthly_returns(returns, weights, cost_per_dollar=0.001, frequency="Annual"):
    """Fixed starting weights; rebalance after each December return, with explicit trade cost."""
    from scipy.optimize import brentq
    w = np.asarray(weights, float); w = w / w.sum()
    holdings = w.copy(); prior_value = 1.0; result = []
    for month, row in returns.iterrows():
        holdings *= 1 + row.to_numpy(float)
        value = float(holdings.sum())
        rebalance = (frequency == "Monthly" or frequency == "Quarterly" and month.month % 3 == 0
                     or frequency == "Annual" and month.month == 12)
        if rebalance and month != returns.index[-1]:
            post_cost = brentq(lambda x: x + cost_per_dollar * np.abs(x * w - holdings).sum() - value,
                               0.0, value)
            holdings = post_cost * w; value = post_cost
        result.append(value / prior_value - 1)
        prior_value = value
    return np.asarray(result)


def optimize_weights(mu, covariance, stocks, objective, risk_aversion, rf,
                     max_asset=None, max_direct_stock=None):
    """Long-only optimizer; optional caps are scenarios, blank means no extra cap."""
    n = len(mu)
    bounds = [(0.0, float(max_asset) if max_asset is not None else 1.0) for _ in range(n)]
    constraints = [{"type": "eq", "fun": lambda w: float(np.sum(w) - 1.0)}]
    stock_indices = np.array([ASSETS.index(s) for s in stocks], dtype=int)
    if max_direct_stock is not None:
        constraints.append({"type": "ineq", "fun": lambda w: float(max_direct_stock - w[stock_indices].sum())})
    if max_asset is not None and max_asset * n < 1 - 1e-10:
        raise ValueError("Individual-asset maximum is too low for weights to sum to 100%")
    cap = 1.0 if max_asset is None else max_asset
    stock_capacity = min(len(stocks) * cap, 1.0 if max_direct_stock is None else max_direct_stock)
    if stock_capacity + (n - len(stocks)) * cap < 1 - 1e-10:
        raise ValueError("Combined caps cannot fund 100%: increase the asset or stock-group cap")

    def loss(w):
        ret = float(w @ mu)
        variance = max(float(w @ covariance @ w), 1e-14)
        if objective == "gmv":
            return variance
        if objective == "sharpe":
            return -(ret - rf) / np.sqrt(variance)
        if objective == "utility":
            return -(ret - 0.5 * risk_aversion * variance)
        if objective == "max_return":
            return -ret
        raise ValueError(objective)

    starts = [np.full(n, 1 / n), np.eye(n)[int(np.argmax(mu))]]
    best = None
    for start in starts:
        if max_asset is not None:
            start = np.minimum(start, max_asset)
            if start.sum() == 0:
                continue
            start = start / start.sum()
        if max_direct_stock is not None and start[stock_indices].sum() > max_direct_stock:
            scale = max_direct_stock / start[stock_indices].sum()
            start[stock_indices] *= scale
            nonstocks = np.array([i for i in range(n) if i not in stock_indices])
            if not len(nonstocks):
                continue
            start[nonstocks] += (1 - start.sum()) / len(nonstocks)
        result = minimize(loss, start, method="SLSQP", bounds=bounds, constraints=constraints,
                          options={"ftol": 1e-11, "maxiter": 3000})
        if result.success and (best is None or result.fun < best.fun):
            best = result
    if best is None:
        raise RuntimeError("Optimizer failed for these settings; relax optional caps or check inputs")
    w = np.maximum(best.x, 0.0)
    w[w < 1e-9] = 0.0
    w /= w.sum()
    if w.max() > cap + 1e-7 or (max_direct_stock is not None and w[stock_indices].sum() > max_direct_stock + 1e-7):
        raise RuntimeError("Optimizer returned weights outside the requested caps")
    return w


def portfolio_metrics(name, weights, mu, cov, rf, risk_aversion, train, eval_returns, transaction_cost,
                      max_asset=None, max_direct_stock=None, inflation=None, frequency="Annual",
                      real_goal=REAL_GOAL_USD):
    w = np.asarray(weights, float)
    ret = float(w @ mu)
    variance = float(w @ cov @ w)
    volatility = float(np.sqrt(max(variance, 0)))
    utility = ret - 0.5 * risk_aversion * variance
    realized_train = rebalanced_monthly_returns(train, w, transaction_cost, frequency)
    realized_eval = rebalanced_monthly_returns(eval_returns, w, transaction_cost, frequency)
    vti_w = np.zeros(len(ASSETS)); vti_w[ASSETS.index("VTI")] = 1.0
    vti_eval = rebalanced_monthly_returns(eval_returns, vti_w, transaction_cost, frequency)
    train_wealth = np.r_[1.0, np.cumprod(1 + realized_train)]
    eval_wealth = np.r_[1.0, np.cumprod(1 + realized_eval)]
    train_dd = train_wealth / np.maximum.accumulate(train_wealth) - 1
    eval_dd = eval_wealth / np.maximum.accumulate(eval_wealth) - 1
    cagr = lambda x: float(x[-1] ** (12 / (len(x) - 1)) - 1)
    geometric_approx = ret - 0.5 * variance
    future_nominal = SURPLUS_USD * max(0.0, 1 + geometric_approx) ** YEARS + SURPLUS_COUPONS_USD
    inflation = float(UI_STATE.get("inflation", 0.025) if inflation is None else inflation)
    future_real = future_nominal / (1 + inflation) ** YEARS
    return {
        "portfolio": name, "expected_return": ret, "annual_variance": variance,
        "annual_volatility": volatility, "forecast_sharpe": (ret - rf) / volatility if volatility else np.nan,
        "utility_at_A": utility, "training_CAGR_2015_22": cagr(train_wealth),
        "training_max_drawdown": float(train_dd.min()), "evaluation_CAGR_2023_25": cagr(eval_wealth),
        "evaluation_CAGR_minus_VTI_pp": float(cagr(eval_wealth) - cagr(np.r_[1.0, np.cumprod(1 + vti_eval)])),
        "evaluation_max_drawdown": float(eval_dd.min()), "direct_stock_weight": float(w[:len(STOCKS)].sum()),
        "largest_asset_weight": float(w.max()), "projected_2030_real_USD_rough": future_real,
        "rough_goal_gap_USD": future_real - real_goal,
        "weight_sum": float(w.sum()),
        "optional_limits_feasible": bool((max_asset is None or w.max() <= max_asset + 1e-8)
                                          and (max_direct_stock is None or w[:len(STOCKS)].sum() <= max_direct_stock + 1e-8)),
    }


# The goal projection uses this only as an in-process scenario value, never as a persisted policy.
UI_STATE = {"inflation": 0.025}


def make_candidates(mu, cov_sample, cov_index, rf, a, max_asset, max_direct_stock):
    candidates = {}
    def add(name, w):
        candidates[name] = np.asarray(w, float)
    for label, matrix in (("Sample", cov_sample), ("Single-index", cov_index)):
        add(f"{label} GMV", optimize_weights(mu, matrix, STOCKS, "gmv", a, rf, max_asset, max_direct_stock))
        add(f"{label} Max Sharpe", optimize_weights(mu, matrix, STOCKS, "sharpe", a, rf, max_asset, max_direct_stock))
        add(f"{label} Max Utility A={a:g}", optimize_weights(mu, matrix, STOCKS, "utility", a, rf, max_asset, max_direct_stock))
        for av in (1., 2., 4., 6., 8.):
            add(f"{label} Utility A={av:g}", optimize_weights(mu, matrix, STOCKS, "utility", av, rf, max_asset, max_direct_stock))
    add("Equal-weight 1/N", np.full(len(ASSETS), 1 / len(ASSETS)))
    for ticker in ASSETS:
        w = np.zeros(len(ASSETS)); w[ASSETS.index(ticker)] = 1.
        add(f"100% {ticker}", w)
    for vti_weight in (0.2, 0.5, 0.8):
        w = np.zeros(len(ASSETS)); w[ASSETS.index("VTI")] = vti_weight; w[ASSETS.index("USMV")] = 1 - vti_weight
        add(f"ETF mix VTI {vti_weight:.0%} / USMV {1-vti_weight:.0%}", w)
    return candidates


def efficient_frontier(mu, cov, a, rf, max_asset, max_direct_stock):
    gmv = optimize_weights(mu, cov, STOCKS, "gmv", a, rf, max_asset, max_direct_stock)
    high = optimize_weights(mu, cov, STOCKS, "max_return", a, rf, max_asset, max_direct_stock)
    s0 = np.sqrt(gmv @ cov @ gmv)
    s1 = np.sqrt(high @ cov @ high)
    targets = np.linspace(s0, max(s0 + 1e-5, s1), 55)
    points = []
    n = len(mu)
    bounds = [(0, max_asset if max_asset is not None else 1.0)] * n
    stock_ix = np.array([ASSETS.index(s) for s in STOCKS], int)
    base_cons = [{"type": "eq", "fun": lambda w: float(w.sum() - 1)}]
    if max_direct_stock is not None:
        base_cons.append({"type": "ineq", "fun": lambda w: float(max_direct_stock - w[stock_ix].sum())})
    for target in targets:
        cons = base_cons + [{"type": "ineq", "fun": lambda w, t=target: float(t*t - w @ cov @ w)}]
        result = minimize(lambda w: -float(w @ mu), gmv.copy(), method="SLSQP", bounds=bounds, constraints=cons,
                          options={"ftol": 1e-10, "maxiter": 1500})
        if result.success:
            w = np.maximum(result.x, 0); w /= w.sum()
            points.append((float(np.sqrt(w @ cov @ w)), float(w @ mu)))
    return np.asarray(points)


def plot_point(ax, candidates, selected, metrics, frontier, mu, rf):
    from matplotlib.ticker import PercentFormatter
    ax.clear()
    fig = ax.figure
    ax.set_position([.07, .11, .53, .80])
    keyax = getattr(fig, "_portfolio_key_ax", None)
    if keyax is None:
        keyax = fig.add_axes([.63, .08, .36, .84]); fig._portfolio_key_ax = keyax
    keyax.clear(); keyax.axis("off")
    if len(frontier):
        order = np.argsort(frontier[:, 0])
        fv = frontier[order, 0]
        fr = frontier[order, 1]
        ax.plot(fv, fr, color="#008080", lw=2.4, label="Efficient frontier", zorder=2)
        ax.fill_between(fv, fr, min(rf, float(fr.min())), color="#008080", alpha=0.06, zorder=1)
    feasible_metrics = [m for m in metrics.values() if m["optional_limits_feasible"]]
    tangent = max(feasible_metrics, key=lambda m: m["forecast_sharpe"]) if feasible_metrics else None
    if tangent:
        ax.plot([0, tangent["annual_volatility"]], [rf, tangent["expected_return"]],
                color="#64748b", ls=(0, (4, 3)), lw=1.6, label="CAL to highest-Sharpe candidate", zorder=2)
    ax.scatter([0], [rf], marker="D", color="#0f172a", s=45, edgecolors="#ffffff",
               linewidths=1.5, label=f"Forecast RF {rf:.1%}", zorder=5)
    colors = plt_colors(len(selected))
    for display_index, (color, name) in enumerate(zip(colors, selected)):
        m = metrics[name]
        is_feasible = m["optional_limits_feasible"]
        marker = "o" if is_feasible else "X"
        size = 85 if is_feasible else 95
        ax.scatter(m["annual_volatility"], m["expected_return"], s=size, marker=marker,
                   color=color, edgecolor="#ffffff", linewidths=1.8, zorder=4)
        if tangent and name == tangent["portfolio"]:
            ax.scatter(m["annual_volatility"], m["expected_return"], s=210, facecolors="none",
                       edgecolors="#d97706", linewidths=2.0, ls="--", zorder=3)
        portfolio_id = f"P{list(candidates).index(name)+1:02d}"
        offsets = [(12, 14), (14, -26), (-54, 24), (-60, -20), (18, 30), (-62, 6), (12, -42), (-58, 40)]
        dx, dy = offsets[display_index % len(offsets)]
        ax.annotate(portfolio_id, (m["annual_volatility"], m["expected_return"]), xytext=(dx, dy),
                    textcoords="offset points", fontsize=8, ha="center", va="center",
                    bbox={"boxstyle": "round,pad=.28,rounding_size=0.25", "fc": "#ffffff",
                          "ec": color, "lw": 1.1, "alpha": 0.95},
                    arrowprops={"arrowstyle": "->", "lw": .8, "color": color, "shrinkA": 2, "shrinkB": 3})
    ax.set_xlabel("Annualized standard deviation σp", fontsize=10, color="#1e293b", labelpad=6)
    ax.set_ylabel("Forecast arithmetic return E(Rp)", fontsize=10, color="#1e293b", labelpad=6)
    ax.set_title("Selected portfolios (ID labels match the scorecard)", fontsize=12, fontweight="bold", color="#0f172a")
    ax.grid(color="#e2e8f0", linestyle="--", linewidth=0.7, alpha=0.8)
    ax.legend(fontsize=8.5, loc="best", frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0")
    ax.xaxis.set_major_formatter(PercentFormatter(1)); ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#94a3b8")
    keyax.text(.01, .99, "ID Portfolio | (σ; E[R]) | Var | SR | U(A) | Stocks / max asset | Δ CAGR vs VTI (pp)",
               transform=keyax.transAxes, va="top", fontsize=7.2, fontweight="bold", color="#0f172a")
    y = .95
    for name in selected:
        m = metrics[name]
        portfolio_id = f"P{list(candidates).index(name)+1:02d}"
        suffix = " CAP BREACH" if not m["optional_limits_feasible"] else ""
        line = (f"{portfolio_id} {name} | ({m['annual_volatility']:.2%}; {m['expected_return']:.2%}) | "
                f"{m['annual_variance']:.5f} | {m['forecast_sharpe']:.3f} | {m['utility_at_A']:.2%} | "
                f"{m['direct_stock_weight']:.0%}/{m['largest_asset_weight']:.0%} | "
                f"{m['evaluation_CAGR_minus_VTI_pp']*100:+.1f} pp{suffix}")
        keyax.text(.01, y, line, transform=keyax.transAxes, va="top", fontsize=6.4,
                   color="#dc2626" if suffix else "#1e293b")
        y -= min(.045, .88 / max(len(selected), 1))


def plt_colors(n):
    base_palette = [
        "#008080", "#2563eb", "#d97706", "#db2777", "#059669",
        "#7c3aed", "#dc2626", "#0891b2", "#ea580c", "#4f46e5",
        "#0d9488", "#c026d3", "#65a30d", "#e11d48", "#0284c7"
    ]
    if n <= len(base_palette):
        return base_palette[:n]
    from matplotlib import colormaps
    return [colormaps["tab20"](i) for i in np.linspace(0, 1, n)]


def plot_radar(ax, selected, metrics):
    ax.clear()
    if not selected:
        ax.set_title("Tick one or more portfolios to display", fontsize=11, color="#64748b")
        return
    columns = ["expected_return", "utility_at_A", "forecast_sharpe", "annual_volatility",
               "training_max_drawdown"]
    labels = ["Forecast return ↑", "Utility at A ↑", "Sharpe ↑", "Forecast volatility ↓", "Training drawdown ↑"]
    feasible_names = [name for name in metrics if metrics[name]["optional_limits_feasible"]]
    raw_all = pd.DataFrame({name: [metrics[name][c] for c in columns] for name in metrics}, index=labels)
    for row in ("Forecast volatility ↓",):
        raw_all.loc[row] = -raw_all.loc[row]
    raw_feasible = raw_all[feasible_names].copy() if feasible_names else raw_all.copy()
    mins = raw_feasible.min(axis=1); spans = (raw_feasible.max(axis=1) - mins).replace(0, 1)
    values = (raw_all.sub(mins, axis=0).div(spans, axis=0) * 100)
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist(); angles += angles[:1]
    colors = plt_colors(len(selected))
    for color, name in zip(colors, selected):
        vals = values[name].to_list(); vals += vals[:1]
        suffix = " (cap breach)" if not metrics[name]["optional_limits_feasible"] else ""
        ax.fill(angles, vals, color=color, alpha=0.18)
        ax.plot(angles, vals, label=name + suffix, color=color, marker="o", lw=1.8,
                markersize=4.5, markeredgecolor="#ffffff", markeredgewidth=1.2, ls="--" if suffix else "-")
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels, fontsize=8.5, fontweight="bold", color="#1e293b")
    ax.set_ylim(0, 100); ax.set_yticks([20, 40, 60, 80, 100])
    ax.tick_params(axis="y", labelsize=8, colors="#64748b")
    ax.grid(color="#cbd5e1", linestyle="--", linewidth=0.7, alpha=0.8)
    ax.set_title("Selected portfolios: relative profiles (0–100, higher is better)", fontsize=11, fontweight="bold", color="#0f172a")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.05), fontsize=7.5, frameon=True,
              facecolor="#ffffff", edgecolor="#e2e8f0")
    ax.text(.5, -.16, "Scores scale against all feasible candidates for current inputs. Do not sum axes or rank by polygon area.",
            transform=ax.transAxes, ha="center", fontsize=8, color="#64748b")


def self_test():
    train, eval_returns, capm, ff3, sample_cov, index_cov = load_local_inputs()
    rf, erp, a = .04, .045, 4.
    mu = forecast_returns("CAPM", rf, erp, 0, 0, capm, ff3)
    weights = optimize_weights(mu, sample_cov.to_numpy(float), STOCKS, "utility", a, rf)
    assert np.isclose(weights.sum(), 1) and (weights >= -1e-9).all()
    assert weights.max() <= 1 + 1e-9  # no invented single-name cap
    candidates = make_candidates(mu, sample_cov.to_numpy(float), index_cov.to_numpy(float), rf, a, None, None)
    assert len(candidates) >= 20
    for w in candidates.values(): assert np.isclose(w.sum(), 1) and (w >= -1e-8).all()
    constrained = optimize_weights(mu, sample_cov.to_numpy(float), STOCKS, "utility", a, rf, .25, .50)
    assert constrained.max() <= .25 + 1e-6 and constrained[:len(STOCKS)].sum() <= .50 + 1e-6
    ff3_mu = forecast_returns("FF3", rf, erp, 0.0, 0.0, capm, ff3)
    assert np.isfinite(ff3_mu).all() and not np.allclose(ff3_mu, mu)
    m = portfolio_metrics("test", weights, mu, sample_cov.to_numpy(float), rf, a, train, eval_returns, .001)
    assert m["weight_sum"] > .999999 and np.isfinite(m["projected_2030_real_USD_rough"])
    os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "logs" / "matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib.figure import Figure
    demo_metrics = {name: portfolio_metrics(name, w, mu, sample_cov.to_numpy(float), rf, a,
                                             train, eval_returns, .001) for name, w in candidates.items()}
    fig = Figure(); ax = fig.add_subplot(111)
    plot_point(ax, candidates, list(candidates)[:3], demo_metrics, np.array([[.1,.06],[.2,.08]]), mu, rf)
    fig2 = Figure(); ax2 = fig2.add_subplot(111, polar=True)
    plot_radar(ax2, list(candidates)[:3], demo_metrics)
    print(f"PASS: 96 training months; {len(eval_returns)} evaluation months; {len(candidates)} candidates; no extra weight caps by default; optional caps work; CAPM/FF3 forecast and both charts render.")


def export_default_examples():
    """Export the modern v2 charts and their calculation receipt."""
    from test_portfolio_lab_v2 import export_previews
    print(f"Exported modern default charts and settings to {export_previews()}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run calculation checks without opening the GUI")
    parser.add_argument("--export-defaults", action="store_true", help="export the default no-extra-cap charts and metrics")
    args = parser.parse_args()
    if args.self_test:
        self_test(); return
    if args.export_defaults:
        export_default_examples(); return
    root = tk.Tk()
    from portfolio_lab_desktop import ModernPortfolioLab
    ModernPortfolioLab(root)
    root.mainloop()


if __name__ == "__main__":
    main()
