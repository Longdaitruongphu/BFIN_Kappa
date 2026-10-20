"""Pure scenario calculations for the desktop lab. No network and no policy writes."""
from dataclasses import dataclass, asdict, field
from functools import lru_cache
import hashlib
import json

import numpy as np
import pandas as pd

import interactive_surplus_portfolio_lab as core


@dataclass
class Settings:
    model: str = "CAPM"
    risk: str = "Sample"
    months: int = 96
    rf: float = .04
    erp: float = .045
    smb: float | None = None
    hml: float | None = None
    a: float = 4
    inflation: float = .025
    vol_mult: float = 1
    corr_stress: float = 0
    shrink: float = 0
    return_shift: float = 0
    asset_cap: float | None = None
    stock_cap: float | None = None
    cost: float = .001
    frequency: str = "Annual"
    real_goal: float = 8_000_000
    shocks: list = field(default_factory=lambda: [-.30] * len(core.ASSETS))
    custom_weights: list | None = None

    def validate(self):
        for key, value in asdict(self).items():
            if isinstance(value, (int, float)) and not np.isfinite(value):
                raise ValueError(f"{key}: a finite number is required")
        if self.model not in ("CAPM", "FF3") or self.risk not in ("Sample", "Single-index"):
            raise ValueError("Choose a supported return / covariance model")
        if self.model == "FF3" and (self.smb is None or self.hml is None):
            raise ValueError("FF3 needs explicit annual SMB and HML expected premiums (0 is an explicit scenario).")
        if self.months not in (60, 72, 84, 96):
            raise ValueError("Window must be 60, 72, 84 or 96 months, always ending Dec 2022.")
        if self.a < 0 or self.vol_mult <= 0 or self.inflation <= -1 or self.real_goal <= 0:
            raise ValueError("A >= 0, volatility multiplier > 0, inflation > -100%, real goal > 0 required.")
        if not 0 <= self.corr_stress <= 1 or not 0 <= self.shrink <= 1:
            raise ValueError("Correlation stress and diagonal shrinkage must be between 0% and 100%.")
        if not 0 <= self.cost < .1:
            raise ValueError("Cost must be between 0 and 1,000 bps (exclusive).")
        if self.frequency not in ("Annual", "Quarterly", "Monthly", "Buy and hold"):
            raise ValueError("Unknown rebalance frequency")
        for cap in (self.asset_cap, self.stock_cap):
            if cap is not None and not 0 <= cap <= 1:
                raise ValueError("Optional caps must be between 0% and 100%; blank means none.")
        per_asset = self.asset_cap if self.asset_cap is not None else 1
        capacity = min(len(core.STOCKS) * per_asset, self.stock_cap if self.stock_cap is not None else 1)
        if capacity + len(core.ETFS) * per_asset < 1 - 1e-10:
            raise ValueError("Optional caps are infeasible: the available assets cannot add up to 100%.")
        shock = np.asarray(self.shocks, float)
        if shock.shape != (len(core.ASSETS),) or not np.isfinite(shock).all() or (shock < -1).any():
            raise ValueError("Provide one finite price shock per asset, each at least -100%.")
        if self.custom_weights is not None:
            w = np.asarray(self.custom_weights, float)
            if w.shape != shock.shape or not np.isfinite(w).all() or (w < 0).any() or not np.isclose(w.sum(), 1, atol=1e-8):
                raise ValueError("Custom weights must be nonnegative and total exactly 100%. No automatic normalization.")


@lru_cache(maxsize=4)
def estimate(months):
    """Re-estimate all exposures and risk from the SAME selected historical window."""
    train, evaluation, *_ = core.load_local_inputs()
    train = train.iloc[-months:].copy()
    factors = pd.read_csv(core.DATA / "train_factors.csv", index_col="month", parse_dates=True).loc[train.index]
    if not np.isfinite(factors.to_numpy()).all():
        raise ValueError("Missing factor data; do not interpolate")
    y = train.to_numpy() - factors.RF.to_numpy()[:, None]
    market = factors["Mkt-RF"].to_numpy()
    x = np.column_stack([np.ones(months), market])
    coefficients = np.linalg.lstsq(x, y, rcond=None)[0]
    residuals = y - x @ coefficients
    beta = coefficients[1]
    single = np.outer(beta, beta) * np.var(market, ddof=1) * 12
    single += np.diag(np.var(residuals, axis=0, ddof=1) * 12)
    x3 = np.column_stack([np.ones(months), factors[["Mkt-RF", "SMB", "HML"]].to_numpy()])
    b3 = np.linalg.lstsq(x3, y, rcond=None)[0][1:].T
    return {
        "train": train, "eval": evaluation, "beta": beta, "ff3": b3,
        "sample": train.cov().to_numpy() * 12, "single": single,
    }


def stressed_covariance(cov, vol_mult=1, corr_stress=0, shrink=0):
    """Shrink toward diagonal; then blend correlation toward +1; finally scale volatility."""
    sd = np.sqrt(np.diag(cov))
    correlation = cov / np.outer(sd, sd)
    correlation = (1 - shrink) * correlation + shrink * np.eye(len(sd))
    correlation = (1 - corr_stress) * correlation + corr_stress * np.ones_like(correlation)
    result = np.outer(sd * vol_mult, sd * vol_mult) * correlation
    if np.linalg.eigvalsh(result).min() < -1e-9:
        raise ValueError("Invalid covariance stress")
    return result


def forecast(settings, data):
    if settings.model == "CAPM":
        return settings.rf + data["beta"] * settings.erp + settings.return_shift
    return settings.rf + data["ff3"] @ np.array([settings.erp, settings.smb, settings.hml]) + settings.return_shift


def summarize(weights, mu, cov, s):
    ret = float(weights @ mu)
    var = max(float(weights @ cov @ weights), 0)
    return ret, np.sqrt(var), ret - .5 * s.a * var


def risk_contributions(weights, cov):
    """Euler contributions to variance, expressed as shares; may be negative for hedges."""
    variance = float(weights @ cov @ weights)
    return weights * (cov @ weights) / variance if variance > 1e-14 else np.full(len(weights), np.nan)


def radar_scores(metrics):
    """Frozen universe within a scenario; negative drawdown has 'higher is better' direction."""
    keys = ["expected_return", "utility_at_A", "forecast_sharpe", "annual_volatility", "training_max_drawdown"]
    frame = pd.DataFrame(metrics).T[keys].astype(float)
    frame["annual_volatility"] *= -1
    feasible = [n for n, m in metrics.items() if m["optional_limits_feasible"]]
    lo = frame.loc[feasible].min()
    span = frame.loc[feasible].max() - lo
    scores = 100 * (frame - lo) / span.replace(0, np.nan)
    scores.loc[:, span == 0] = 50
    return scores


def calculate(s, baseline=None):
    s.validate()
    data = estimate(s.months)
    mu = forecast(s, data)
    sample = stressed_covariance(data["sample"], s.vol_mult, s.corr_stress, s.shrink)
    single = stressed_covariance(data["single"], s.vol_mult, s.corr_stress, s.shrink)
    cov = sample if s.risk == "Sample" else single
    candidates = core.make_candidates(mu, sample, single, s.rf, s.a, s.asset_cap, s.stock_cap)
    # Identical A is useful once, not as two apparent independent alternatives.
    for prefix in ("Sample", "Single-index"):
        candidates.pop(f"{prefix} Utility A={s.a:g}", None)
    if s.custom_weights is not None:
        candidates["Custom portfolio"] = np.array(s.custom_weights, float)
    metrics = {}
    for name, w in candidates.items():
        metrics[name] = core.portfolio_metrics(name, w, mu, cov, s.rf, s.a, data["train"], data["eval"],
            s.cost, s.asset_cap, s.stock_cap, inflation=s.inflation, frequency=s.frequency, real_goal=s.real_goal)
    frontier = core.efficient_frontier(mu, cov, s.a, s.rf, s.asset_cap, s.stock_cap)
    # CAL is analytical only; cash is not a decision variable in this equity-sleeve optimizer.
    tangent_w = core.optimize_weights(mu, cov, core.STOCKS, "sharpe", s.a, s.rf, s.asset_cap, s.stock_cap)
    tangent = summarize(tangent_w, mu, cov, s)
    result = dict(settings=s, data=data, mu=mu, cov=cov, candidates=candidates, metrics=metrics,
                  frontier=frontier, tangent=tangent, baseline=baseline)
    result["sensitivity"] = sensitivity(s, data)
    return result


def sensitivity(s, data):
    """Reoptimize utility across a predeclared A / market-premium grid. No OOS selection."""
    from dataclasses import replace
    aversions = [1., 2., 4., 6., 8., 12.]
    premiums = np.array([0., .02, .045, .06, .08])
    cov = stressed_covariance(data["sample"] if s.risk == "Sample" else data["single"],
                              s.vol_mult, s.corr_stress, s.shrink)
    rows = []
    for a in aversions:
        for premium in premiums:
            scenario = replace(s, a=a, erp=float(premium))
            mu = forecast(scenario, data)
            w = core.optimize_weights(mu, cov, core.STOCKS, "utility", a, s.rf, s.asset_cap, s.stock_cap)
            ret, vol, utility = summarize(w, mu, cov, scenario)
            rows.append({"A": a, "ERP": premium, "volatility": vol, "return": ret, "utility": utility,
                         **{ticker: float(w[i]) for i, ticker in enumerate(core.ASSETS)}})
    return pd.DataFrame(rows)


def baseline_comparison(result, names):
    baseline = result.get("baseline")
    if baseline is None:
        return pd.DataFrame()
    rows = []
    s = result["settings"]
    for name in names:
        # Dynamic A labels refer to the same optimization objective, not a new strategy identity.
        old_name = name
        if "Max Utility A=" in name:
            old_name = name.split(" A=")[0] + f" A={baseline['settings'].a:g}"
        if old_name not in baseline["candidates"]:
            continue
        old_w = baseline["candidates"][old_name]
        new_w = result["candidates"][name]
        old = summarize(old_w, baseline["mu"], baseline["cov"], s)
        frozen = summarize(old_w, result["mu"], result["cov"], s)
        reopt = summarize(new_w, result["mu"], result["cov"], s)
        rows.append({
            "portfolio": name, "baseline_return": old[0], "baseline_vol": old[1],
            "fixed_weight_return": frozen[0], "fixed_weight_vol": frozen[1], "fixed_weight_U": frozen[2],
            "current_candidate_return": reopt[0], "current_candidate_vol": reopt[1], "current_candidate_U": reopt[2],
            "one_way_turnover": float(.5 * np.abs(new_w - old_w).sum()),
            "hypothetical_switch_cost_USD": float(s.cost * np.abs(new_w - old_w).sum() * core.SURPLUS_USD),
            "fixed_weight_shock": float(old_w @ s.shocks),
            "current_candidate_shock": float(new_w @ s.shocks),
        })
    return pd.DataFrame(rows)


def export_bundle(result, names, folder):
    """Only checked portfolios, plus exact assumptions, hashes and audit data."""
    folder.mkdir(parents=True, exist_ok=True)
    s = result["settings"]
    rows = []
    for name in names:
        w = result["candidates"][name]
        pid = f"P{list(result['candidates']).index(name)+1:02d}"
        rows.append({"ID": pid, **result["metrics"][name], "instantaneous_shock": float(w @ s.shocks),
                     **dict(zip(core.ASSETS, map(float, w)))})
    pd.DataFrame(rows).to_csv(folder / "selected_metrics_weights.csv", index=False)
    comparison = baseline_comparison(result, names)
    if comparison.empty:
        comparison = pd.DataFrame({"status": ["No matching pinned baseline; pin a baseline before changing inputs."]})
    comparison.to_csv(folder / "baseline_comparison.csv", index=False)
    result["sensitivity"].to_csv(folder / "sensitivity_grid_all.csv", index=False)
    inputs = [core.DATA / f for f in ("train_monthly_returns.csv", "train_factors.csv", "eval_monthly_returns.csv")]
    inputs += [core.ROOT / "policy/frozen_policy.json"]
    code = [core.ROOT/"analysis"/f for f in ("interactive_surplus_portfolio_lab.py",
             "portfolio_lab_scenarios.py", "portfolio_lab_charts.py", "portfolio_lab_desktop.py")]
    settings = asdict(s)
    receipt = {
        "version": 2, "settings": settings, "selected": names,
        "id_map": {f"P{i+1:02d}": n for i, n in enumerate(result["candidates"])},
        "training_end": "2022-12", "evaluation": "2023-01 to 2025-12; evaluation only",
        "source_hashes": {str(p.relative_to(core.ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
        "code_hashes": {str(p.relative_to(core.ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in code},
        "scope": "Equity growth sleeve only; case bonds excluded from plotted volatility/drawdown/stress.",
        "limits": "No guaranteed loss floor; scenario probabilities not estimated; radar is descriptive.",
        "historical_cost_convention": "Per dollar bought plus sold at scheduled rebalances; no entry/exit costs.",
        "baseline": None,
    }
    base = result.get("baseline")
    if base:
        receipt["baseline"] = {"settings": asdict(base["settings"]),
                               "weights": {n: w.tolist() for n, w in base["candidates"].items()}}
    (folder / "scenario.json").write_text(json.dumps(receipt, indent=2, allow_nan=False), encoding="utf-8")
