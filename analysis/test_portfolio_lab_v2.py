"""Numerical regression, scenario, export and Tk layout checks; no network access."""
from dataclasses import replace, asdict
from pathlib import Path
import hashlib
import json
import tempfile
import time
import unittest
import numpy as np
import pandas as pd

import interactive_surplus_portfolio_lab as core
import portfolio_lab_scenarios as model
from portfolio_lab_charts import draw_figure, VIEWS


class LabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = model.calculate(model.Settings())

    def test_default_matches_saved_estimates(self):
        _, _, capm, _, sample, single = core.load_local_inputs()
        d = self.result["data"]
        np.testing.assert_allclose(d["sample"], sample.to_numpy(), atol=1e-11)
        np.testing.assert_allclose(d["single"], single.to_numpy(), atol=1e-11)
        np.testing.assert_allclose(d["beta"], capm.beta, atol=1e-10)

    def test_window_and_factor_regression(self):
        d = model.estimate(60)
        self.assertEqual(len(d["train"]), 60)
        self.assertEqual(str(d["train"].index[0].to_period("M")), "2018-01")
        self.assertEqual(str(d["train"].index[-1].to_period("M")), "2022-12")
        factors = pd.read_csv(core.DATA/"train_factors.csv", parse_dates=["month"]).set_index("month").loc[d["train"].index]
        x = np.column_stack([np.ones(60), factors[["Mkt-RF","SMB","HML"]]])
        y = d["train"].AAPL.to_numpy()-factors.RF.to_numpy()
        independently_solved = np.linalg.solve(x.T@x, x.T@y)
        np.testing.assert_allclose(d["ff3"][0], independently_solved[1:], atol=1e-10)

    def test_covariance_stress(self):
        cov = self.result["cov"]
        stressed = model.stressed_covariance(cov, 1.5, .4, .2)
        self.assertGreaterEqual(np.linalg.eigvalsh(stressed).min(), -1e-12)
        np.testing.assert_allclose(np.diag(stressed), np.diag(cov)*2.25)
        perfect = model.stressed_covariance(cov, 1, 1, 0)
        np.testing.assert_allclose(perfect, np.outer(np.sqrt(np.diag(cov)), np.sqrt(np.diag(cov))))
        diagonal = model.stressed_covariance(cov, 1, 0, 1)
        np.testing.assert_allclose(diagonal, np.diag(np.diag(cov)))

    def test_radar_drawdown_direction_and_selection_invariance(self):
        metrics = {k: dict(v) for k,v in list(self.result["metrics"].items())[:2]}
        names = list(metrics)
        metrics[names[0]]["training_max_drawdown"] = -.05
        metrics[names[1]]["training_max_drawdown"] = -.25
        scores = model.radar_scores(metrics)
        self.assertEqual(scores.loc[names[0],"training_max_drawdown"],100)
        self.assertEqual(scores.loc[names[1],"training_max_drawdown"],0)

    def test_invalid_inputs_and_combined_caps(self):
        for s in [model.Settings(model="FF3"), model.Settings(rf=float("nan")),
                  model.Settings(asset_cap=.2, stock_cap=.1), model.Settings(shocks=[-1.1]*10),
                  model.Settings(custom_weights=[.2]*10)]:
            with self.assertRaises(ValueError): s.validate()
        # ETFs only is feasible and no silently imposed stock cap exists by default.
        s = model.Settings(stock_cap=0)
        r = model.calculate(s)
        w = r["candidates"]["Sample Max Utility A=4"]
        self.assertLess(w[:8].sum(), 1e-7)
        self.assertIsNone(self.result["settings"].asset_cap)

    def test_risk_contributions_and_shock_identity(self):
        for w in self.result["candidates"].values():
            self.assertAlmostEqual(float(w.sum()),1)
            self.assertTrue((w>=0).all())
            self.assertAlmostEqual(float(model.risk_contributions(w,self.result["cov"]).sum()),1)
            self.assertAlmostEqual(float(w @ np.full(10,-.3)), -.3)

    def test_rebalance_cash_accounting(self):
        dates = pd.to_datetime(["2023-11-01", "2023-12-01", "2024-01-01"])
        r = pd.DataFrame([[0,0],[.2,0],[.1,-.1]], index=dates)
        w = np.array([.5,.5])
        no_trade = core.rebalanced_monthly_returns(r,w,0,"Buy and hold")
        # 0.5*1.2*1.1 + 0.5*1*0.9 = 1.11.
        self.assertAlmostEqual(float(np.prod(1+no_trade)),1.11)
        annual = core.rebalanced_monthly_returns(r,w,.01,"Annual")
        # After Dec, holdings (.6,.5), rebalance costs .001; value1.099.
        self.assertAlmostEqual(float(np.prod(1+annual)),1.099)
        monthly = core.rebalanced_monthly_returns(r,w,.01,"Monthly")
        np.testing.assert_allclose(monthly, annual)

    def test_baseline_keeps_weights_and_inflation_is_not_return(self):
        base = self.result
        baseline = {k: base[k] for k in ("settings","mu","cov","candidates")}
        r = model.calculate(replace(base["settings"], vol_mult=1.5), baseline)
        name = "Sample Max Utility A=4"
        comp = model.baseline_comparison(r,[name]).iloc[0]
        self.assertAlmostEqual(comp.fixed_weight_vol, 1.5*comp.baseline_vol)
        self.assertGreater(comp.one_way_turnover, .001)
        high_pi = replace(base["settings"],inflation=.05)
        np.testing.assert_array_equal(model.forecast(high_pi,base["data"]),base["mu"])
        self.assertEqual(model.baseline_comparison(r,[name]).shape[0],1)

    def test_ff3_explicit_inputs_and_zero_alpha(self):
        d = self.result["data"]
        s = model.Settings(model="FF3",smb=0,hml=0)
        s.validate()
        np.testing.assert_allclose(model.forecast(s,d),s.rf+d["ff3"][:,0]*s.erp)

    def test_export_selected_and_reproducible_settings(self):
        with tempfile.TemporaryDirectory(dir=core.ROOT/"tmp") as tmp:
            model.export_bundle(self.result,["100% USMV"],Path(tmp))
            frame = pd.read_csv(Path(tmp)/"selected_metrics_weights.csv")
            self.assertEqual(frame.portfolio.tolist(),["100% USMV"])
            receipt = json.loads((Path(tmp)/"scenario.json").read_text())
            s = model.Settings(**receipt["settings"]); s.validate()
            self.assertEqual(asdict(s),asdict(self.result["settings"]))
            self.assertFalse("eval" in str(receipt.get("training_end")))

    def test_every_chart_draws(self):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        names = ["Sample GMV","Sample Max Sharpe","Sample Max Utility A=4","100% USMV","100% VTI"]
        for view in VIEWS:
            fig=Figure(figsize=(12,8))
            draw_figure(fig,view,self.result,names)
            FigureCanvasAgg(fig).draw()

    def test_unchecked_benchmark_not_plotted(self):
        from matplotlib.figure import Figure
        fig = Figure(figsize=(12,8))
        draw_figure(fig,"2023-25 wealth",self.result,["100% USMV"])
        self.assertEqual(len(fig.axes[0].lines), 1)
        self.assertEqual(str(fig.axes[0].lines[0].get_xdata()[-1])[:10], "2025-12-31")


def export_previews():
    from matplotlib.figure import Figure
    folder = core.DEFAULT_OUTPUT/"portfolio_lab_v2"
    r = model.calculate(model.Settings())
    selected = ["Sample GMV","Sample Max Sharpe","Sample Max Utility A=4","100% USMV","100% VTI"]
    model.export_bundle(r,selected,folder)
    for view in VIEWS:
        fig=Figure(figsize=(14,10))
        draw_figure(fig,view,r,selected)
        name=view.lower().replace(" / ","_").replace(" ","_")
        fig.savefig(folder/f"{name}.png",dpi=150)
    return folder


def check_tk_layout():
    import tkinter as tk
    from portfolio_lab_desktop import ModernPortfolioLab
    root=tk.Tk(); root.withdraw()
    app=ModernPortfolioLab(root,auto_start=False)
    app.accept(LabTests.result)
    # Calculate requested dimensions without depending on a desktop screenshot.
    root.update_idletasks()
    assert app.sidebar.winfo_reqwidth() < 430, app.sidebar.winfo_reqwidth()
    app.read_settings().validate()
    for view in ["Scorecard","Baseline comparison",*VIEWS]:
        app.view.set(view); app.draw(); root.update_idletasks()
    app.pin()
    app.vars["inflation"].set("5")
    assert app.read_settings().inflation == .05
    app.recalculate()
    deadline = time.time() + 30
    while app.progress.instate(["!disabled"]) and app.future and not app.future.done() and time.time() < deadline:
        root.update()
        time.sleep(.02)
    assert app.future.done(), "Background calculation timed out"
    app.poll()
    assert app.result["settings"].inflation == .05
    app.close()
    return "Tk construction, pane requested width, chart/table switching, pin, input parsing and background recalculation passed; not a manual usability test."


if __name__=="__main__":
    started=time.time()
    before=hashlib.sha256((core.ROOT/"policy/frozen_policy.json").read_bytes()).hexdigest()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(LabTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful(): raise SystemExit(1)
    ui=check_tk_layout()
    previews=export_previews()
    after=hashlib.sha256((core.ROOT/"policy/frozen_policy.json").read_bytes()).hexdigest()
    assert before==after=="21b4ec3fb864144e7b56e54c668ebaed9c96d5a1771564b50c892700978c9f5c"
    receipt=dict(tests=result.testsRun,passed=True,tk_checks=ui,frozen_policy_sha256=after,
                 seconds=round(time.time()-started,2),previews=str(previews),
                 scope="Saved-data model checks; no new download and no human investment-policy approval.")
    (core.ROOT/"logs/portfolio_lab_v2_checks.json").write_text(json.dumps(receipt,indent=2),encoding="utf-8")
    print(json.dumps(receipt,indent=2))
