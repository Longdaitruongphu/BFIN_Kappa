"""Hypothetical revised mandates, NOT the unreleased lecturer mandate.

Case date remains 2022-12-31. Inputs are saved case quotes and 2015-2022 data.
Writes only outputs/mandate_preparedness; never amends the frozen policy.
"""
from pathlib import Path
import json
import hashlib
import numpy as np
import pandas as pd
from scipy.optimize import linprog, brentq
from bonds import BONDS, flows, curve
from portfolio_lab_scenarios import estimate
from interactive_surplus_portfolio_lab import optimize_weights, ASSETS, STOCKS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "mandate_preparedness"
FROZEN = ROOT / "policy/frozen_policy.json"
POL = json.loads(FROZEN.read_text())
FUND = POL["funding"]
BOND_FEE, EQUITY_FEE = .0005, .001
BASE_PAYMENTS = {2: 2.4e6, 5: 3.6e6}
PRICES = np.array([b[3] for b in BONDS])


def bond_cashflows(horizon=8):
    cfs = np.zeros((horizon, 5))
    for j, (_, n, c, _) in enumerate(BONDS):
        _, cf = flows(n, c)
        cfs[:min(n, horizon), j] = cf[:horizon]
    return cfs


def dedicated_plan(payments, horizon=8):
    """Separate payment rings, matching the original plan.

    For new year-6/7/8 spending: buy extra Delta, mature at year5,
    retain its proceeds in 0%-interest cash until the payment. Earlier
    coupons are surplus cash. No bond sale or assumed reinvestment.
    """
    units = np.zeros(5)
    maturity_map = {1: 0, 2: 1, 3: 2, 5: 3}
    for year, amount in payments.items():
        maturity = year if year in maturity_map else 5 if year >= 6 else 3
        j = maturity_map[maturity]
        units[j] += amount / (1000 * (1+BONDS[j][2]))
    cashflows = bond_cashflows(horizon) @ units
    withdrawals = np.array([payments.get(y, 0) for y in range(1, horizon+1)])
    cash = np.cumsum(cashflows - withdrawals)
    assert cash.min() >= -.00001, "Payment plan is not funded by due date"
    return units, cashflows, withdrawals, cash


def fixed_income_goal_cost(payments, target, horizon=8):
    """Least initial cost to fund all payments AND terminal nominal goal.

    Cash can carry at 0%; only instruments maturing no later than horizon.
    This deliberately differs from the original separate payment rings.
    """
    cfs = bond_cashflows(horizon)
    valid = [i for i, b in enumerate(BONDS) if b[1] <= horizon]
    matrix = np.column_stack([cfs[:, valid], np.r_[1., np.zeros(horizon-1)]])
    cum = matrix.cumsum(axis=0)
    costs = np.r_[PRICES[valid] * (1+BOND_FEE), 1.]
    required = np.cumsum([payments.get(y, 0) for y in range(1, horizon+1)])
    required[-1] += target
    result = linprog(costs, A_ub=-cum, b_ub=-required, bounds=(0, None), method="highs")
    assert result.success, result.message
    assert (cum @ result.x - required).min() > -.001
    return float(result.fun)


def build_scenario(sid, label, payments=None, capital=12e6, inflation=.025,
                   real_goal=8e6, horizon=8, reserve=0., equity_ceiling=None):
    payments = dict(BASE_PAYMENTS if payments is None else payments)
    assert horizon >= 1 and inflation > -1 and capital > 0 and real_goal >= 0
    assert all(isinstance(y, int) and 1 <= y <= horizon and a >= 0
               for y, a in payments.items()), "Payments must be nonnegative and inside the horizon"
    units, cfs, paid, cash = dedicated_plan(payments, horizon)
    bond_cost = float(units @ PRICES)
    surplus = (capital - bond_cost*(1+BOND_FEE) - reserve)/(1+EQUITY_FEE)
    if equity_ceiling is not None:
        surplus = min(surplus, equity_ceiling)
        reserve = capital - bond_cost*(1+BOND_FEE) - surplus*(1+EQUITY_FEE)
    assert surplus > 0 and reserve >= -.001
    fees = bond_cost*BOND_FEE + surplus*EQUITY_FEE
    terminal_cash = cash[-1] + reserve
    target = real_goal * (1+inflation)**horizon
    hurdle = ((target-terminal_cash)/surplus)**(1/horizon)-1 if target > terminal_cash else -1.
    assert abs(bond_cost + reserve + surplus + fees-capital) < .00001
    # Least capital required for a nominally dedicated goal is a separate solution.
    fixed_goal_cost = fixed_income_goal_cost(payments, target, horizon)
    row = dict(id=sid, scenario=label, initial_capital=capital, horizon_years=horizon,
               inflation=inflation, real_goal=real_goal, target_nominal=target,
               payment_bonds=bond_cost, initial_cash_reserve=reserve, equity_surplus=surplus,
               equity_share_initial=surplus/capital, execution_fees=fees,
               terminal_non_equity_cash=terminal_cash, required_equity_CAGR=hurdle,
               required_equity_real_CAGR=(1+hurdle)/(1+inflation)-1,
               fixed_income_goal_initial_cost=fixed_goal_cost,
               additional_capital_for_fixed_nominal_goal=max(0,fixed_goal_cost-capital),
               total_mandatory_payments=float(paid.sum()),
               **{b[0]+"_units": float(units[i]) for i,b in enumerate(BONDS)})
    paths = [dict(id=sid, year=2022+y, inflow=float(cfs[y-1]), payment=float(paid[y-1]),
                  dedicated_cash_after_payment=float(cash[y-1])) for y in range(1,horizon+1)]
    return row, paths


def stress_limits():
    _, d = curve()
    units, _, _, _ = dedicated_plan(BASE_PAYMENTS)
    bond_cost = float(units @ PRICES)
    rows = []
    for equity_shock, rate_shock in [(-.30,.01),(-.40,.02)]:
        stressed_prices = []
        for _, n,c,p in BONDS:
            tt,cf = flows(n,c)
            stressed_prices.append(float(cf @ (d[:n]*np.exp(-tt*rate_shock))))
        bond_loss = bond_cost - units @ np.array(stressed_prices)
        for loss_limit in [.15,.10]:
            # Fee-inclusive loss relative to contributed capital, before payments.
            q = max(0., (loss_limit*12e6 - bond_loss - BOND_FEE*bond_cost) / (-equity_shock+EQUITY_FEE))
            q = min(q,FUND["equity_investment"])
            cash = 12e6-bond_cost*(1+BOND_FEE)-q*(1+EQUITY_FEE)
            fees = bond_cost*BOND_FEE+q*EQUITY_FEE
            actual_loss = (bond_loss-equity_shock*q+fees)/12e6
            hurdle = ((FUND["nominal_goal"]-FUND["terminal_cash"]-cash)/q)**(1/8)-1
            rows.append(dict(equity_shock=equity_shock,continuous_curve_shock=rate_shock,
                whole_fund_stress_limit=loss_limit,equity_cap=q,cash_reserve=cash,
                equity_reduction=FUND["equity_investment"]-q,
                equity_share=q/12e6,bond_loss=float(bond_loss),fees=fees,loss_check=actual_loss,
                required_equity_CAGR=hurdle,scope="Specified initial stress only; not a drawdown guarantee"))
    return pd.DataFrame(rows)


def model_uncertainty():
    rows = []
    for months in (96,60):
        data = estimate(months)
        for risk in ("sample","single"):
            for erp in (.025,.045,.065):
                mu = .04+data["beta"]*erp
                for a in (2.,4.,8.):
                    w=optimize_weights(mu,data[risk],STOCKS,"utility",a,.04)
                    assert abs(w.sum()-1) < 1e-7 and w.min() >= -1e-7
                    rows.append(dict(months=months,risk=risk,ERP=erp,A=a,
                        expected_return=float(w@mu),volatility=float(np.sqrt(w@data[risk]@w)),
                        utility=float(w@mu-.5*a*w@data[risk]@w), **dict(zip(ASSETS,w))))
    frame=pd.DataFrame(rows)
    data=estimate(96); cov=data["sample"]; beta=data["beta"]
    v,u=ASSETS.index("VTI"),ASSETS.index("USMV")
    delta_var=cov[v,v]-cov[u,u]; delta_beta=beta[v]-beta[u]
    thresholds=dict(A_switch=2*.045*delta_beta/delta_var,
                    ERP_switch_at_A4=2*delta_var/delta_beta,
                    USMV_VTI_tracking_error=float(np.sqrt(cov[v,v]+cov[u,u]-2*cov[v,u])),
                    utility_USMV_minus_VTI_A4=float(.045*(beta[u]-beta[v])-2*(cov[u,u]-cov[v,v])))
    thresholds["volatility_multiplier_switch_at_A4"]=float(np.sqrt(thresholds["A_switch"]/4))
    # Example mandate: tracking error <=5% vs VTI, with the two ETFs only.
    te=thresholds["USMV_VTI_tracking_error"]
    min_vti=max(0,1-.05/te)
    w=np.zeros(len(ASSETS));w[v]=min_vti;w[u]=1-min_vti
    thresholds["TE5_minimum_VTI_weight"]=min_vti
    thresholds["TE5_USMV_weight"]=1-min_vti
    thresholds["TE5_boundary_return"]=float(w@(.04+beta*.045))
    thresholds["TE5_boundary_volatility"]=float(np.sqrt(w@cov@w))
    base=frame[(frame.months==96)&(frame.risk=="sample")&(frame.ERP==.045)&(frame.A==4)].iloc[0]
    alt=frame[(frame.months==96)&(frame.risk=="single")&(frame.ERP==.045)&(frame.A==4)].iloc[0]
    thresholds["uncapped_sample_vs_index_oneway_turnover"]=float(.5*np.abs(base[ASSETS].to_numpy(float)-alt[ASSETS].to_numpy(float)).sum())
    return frame,thresholds


def funding_drift_examples():
    """Illustrative paths, constant 5% equity CAGR; no invented bond resale history."""
    units,cfs,payments,cash=dedicated_plan(BASE_PAYMENTS)
    rows=[]
    for y in (0,2,5,8):
        growth=FUND["equity_investment"]*1.05**y
        retained=0 if y==0 else cash[y-1]
        # At year5 all payment bonds have matured. Earlier-year bond MTM unavailable.
        if y in (5,8):
            eqshare=growth/(growth+retained)
        elif y==0:
            eqshare=growth/(growth+FUND["bond_cost"])
        else:
            eqshare=None
        rows.append(dict(year=2022+y,equity_value=growth,surplus_cash=retained,
                         equity_share_remaining_NAV=eqshare,
                         whole_fund_loss_if_equities_drop30=(None if eqshare is None else .30*eqshare)))
    return pd.DataFrame(rows)


def one_year_shock_recovery():
    rows=[]
    for shock in (-.15,-.30,-.40):
        left=FUND["equity_investment"]*(1+shock)
        # Illustrative first-year equity return; seven years remain. No future cash spending added.
        hurdle=((FUND["nominal_goal"]-FUND["terminal_cash"])/left)**(1/7)-1
        rows.append(dict(first_year_equity_return=shock,remaining_equity=left,remaining_years=7,
                         required_future_CAGR=hurdle))
    return pd.DataFrame(rows)


def contribution_and_spending_math():
    q=FUND["equity_investment"]; coupons=FUND["terminal_cash"]
    rows=[]
    for pi in (.025,.04,.05):
        target=8e6*(1+pi)**8
        for g in (.04,.05,.06):
            needed=max(0, (target-coupons)/(1+g)**8-q)
            real_goal_supported=(q*(1+g)**8+coupons)/(1+pi)**8
            rows.append(dict(inflation=pi,assumed_net_equity_CAGR=g,
                            additional_invested_equity_needed=needed,
                            initial_donation_including_entry_fee=needed*(1+EQUITY_FEE),
                            supported_real_goal=real_goal_supported))
    # Repeated withdrawals paid from growth instead of dedicated: a distinct risky implementation.
    spending=[]
    for annual in (0,.3e6,.6e6):
        for pi in (.025,.04):
            target=8e6*(1+pi)**8
            f=lambda g:q*(1+g)**8+coupons-annual*sum((1+g)**(8-y) for y in (6,7,8))-target
            g=brentq(f,-.5,.5)
            spending.append(dict(annual_spend_2028_30=annual,inflation=pi,
                                 CAGR_if_funded_from_growth=g,
                                 warning="Constant-return solvency only, NOT assured cash-flow coverage"))
    return pd.DataFrame(rows),pd.DataFrame(spending)


def difficulty_context(frame):
    """Illustrative 5% net equity CAGR, not a newly adopted forecast."""
    rows=[]
    for sid in ["B0","L1","L4","L5","C1","G1","G2","R1"]:
        r=frame.set_index("id").loc[sid]
        nominal=r.equity_surplus*1.05**r.horizon_years+r.terminal_non_equity_cash
        real=nominal/(1+r.inflation)**r.horizon_years
        rows.append(dict(scenario_id=sid,assumed_constant_net_CAGR=.05,
            real_terminal=real,gap_to_real_goal=real-r.real_goal,gap_fraction=real/r.real_goal-1,
            required_CAGR=r.required_equity_CAGR,
            required_minus_assumed_percentage_points=(r.required_equity_CAGR-.05)*100,
            interpretation="Deterministic illustration, not a probability or a proven maximum attainable return"))
    q=FUND["equity_investment"]*.7
    real=(q*1.05**7+FUND["terminal_cash"])/1.025**8
    req=((FUND["nominal_goal"]-FUND["terminal_cash"])/q)**(1/7)-1
    rows.append(dict(scenario_id="First-year equity -30%",assumed_constant_net_CAGR=.05,
                     real_terminal=real,gap_to_real_goal=real-8e6,gap_fraction=real/8e6-1,
                     required_CAGR=req,required_minus_assumed_percentage_points=(req-.05)*100,
                     interpretation="One-year shock followed by seven years at 5%; no claim about future outcomes"))
    return pd.DataFrame(rows)


def evaluation_gap_bridge():
    """Evaluation only: frozen training exposures explain raw ETF mean-return difference.

    This is an accounting bridge, not causal attribution or an alpha significance test.
    Arithmetic mean-return difference is not a CAGR difference.
    """
    data=estimate(96)
    f=pd.read_csv(ROOT/"data/processed/eval_factors.csv",index_col="month",parse_dates=True)
    r=data["eval"]
    f=f.loc[r.index]
    u,v=ASSETS.index("USMV"),ASSETS.index("VTI")
    exposure_delta=data["ff3"][u]-data["ff3"][v]
    contributions=exposure_delta*f[["Mkt-RF","SMB","HML"]].mean().to_numpy()*12
    observed=float((r.USMV-r.VTI).mean()*12)
    residual=observed-contributions.sum()
    rows=[dict(component=label,annual_arithmetic_return_difference=float(x))
          for label,x in zip(["Market exposure","SMB exposure","HML exposure"],contributions)]
    rows.extend([dict(component="Unexplained difference incl. model error",annual_arithmetic_return_difference=float(residual)),
                 dict(component="Observed USMV minus VTI",annual_arithmetic_return_difference=observed)])
    assert abs(sum(x["annual_arithmetic_return_difference"] for x in rows[:-1])-observed)<1e-12
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    before=hashlib.sha256(FROZEN.read_bytes()).hexdigest()
    specs=[
        ("B0","Original case",{}),
        ("L1","2027 payment rises 20%",dict(payments={2:2.4e6,5:4.32e6})),
        ("L2","Second payment moves to 2025",dict(payments={2:2.4e6,3:3.6e6})),
        ("L3","Additional mandatory 1m in 2023",dict(payments={1:1e6,**BASE_PAYMENTS})),
        ("L4","Additional 0.3m annually 2028-2030",dict(payments={**BASE_PAYMENTS,6:.3e6,7:.3e6,8:.3e6})),
        ("L5","Additional 0.6m annually 2028-2030",dict(payments={**BASE_PAYMENTS,6:.6e6,7:.6e6,8:.6e6})),
        ("C1","Initial resources cut to 10m",dict(capital=10e6)),
        ("C2","Additional 2m received at inception",dict(capital=14e6)),
        ("G1","Inflation 4%",dict(inflation=.04)),
        ("G2","Inflation 5%",dict(inflation=.05)),
        ("G3","Real goal raised to 10m",dict(real_goal=10e6)),
        ("G4","Real goal due in 2028",dict(horizon=6)),
        ("Q1","Additional immediate 1m cash reserve",dict(reserve=1e6)),
        ("X1","2027 payment +20% AND inflation 4%",dict(payments={2:2.4e6,5:4.32e6},inflation=.04)),
    ]
    rows=[];paths=[]
    for sid,label,kwargs in specs:
        row,path=build_scenario(sid,label,**kwargs)
        rows.append(row); paths.extend(path)
    limits=stress_limits()
    for i,item in limits.iterrows():
        row,path=build_scenario(f"R{i+1}",f"Stress cap {item.whole_fund_stress_limit:.0%}; equities {item.equity_shock:.0%}; rates {item.continuous_curve_shock:.0%}",
                               equity_ceiling=float(item.equity_cap))
        rows.append(row);paths.extend(path)
    frame=pd.DataFrame(rows)
    base=frame.iloc[0]
    assert abs(base.equity_surplus-FUND["equity_investment"]) < .01
    assert abs(base.required_equity_CAGR-FUND["required_equity_cagr"]) < 1e-12
    assert abs(base.additional_capital_for_fixed_nominal_goal-480442.8390559964) < .01
    assert np.max(np.abs(limits.loss_check-limits.whole_fund_stress_limit)) < 1e-10
    frame["change_equity_vs_original"]=frame.equity_surplus-base.equity_surplus
    frame["change_hurdle_percentage_points"]=(frame.required_equity_CAGR-base.required_equity_CAGR)*100
    frame.to_csv(OUT/"mandate_scenarios.csv",index=False)
    pd.DataFrame(paths).to_csv(OUT/"payment_coverage_paths.csv",index=False)
    limits.to_csv(OUT/"stress_loss_limits.csv",index=False)
    uncertainty,thresholds=model_uncertainty()
    uncertainty.to_csv(OUT/"model_uncertainty_weights.csv",index=False)
    (OUT/"decision_reversal_thresholds.json").write_text(json.dumps(thresholds,indent=2),encoding="utf-8")
    funding_drift_examples().to_csv(OUT/"post_payment_risk_drift.csv",index=False)
    one_year_shock_recovery().to_csv(OUT/"shock_recovery_hurdles.csv",index=False)
    contributions,spending=contribution_and_spending_math()
    contributions.to_csv(OUT/"goal_or_donation_tradeoffs.csv",index=False)
    spending.to_csv(OUT/"spending_from_growth_alternative.csv",index=False)
    difficulty_context(frame).to_csv(OUT/"difficulty_context.csv",index=False)
    evaluation_gap_bridge().to_csv(OUT/"evaluation_gap_bridge.csv",index=False)
    draw(frame)
    after=hashlib.sha256(FROZEN.read_bytes()).hexdigest()
    assert before==after
    files=[FROZEN,ROOT/"data/processed/train_monthly_returns.csv",ROOT/"data/processed/train_factors.csv",
           ROOT/"data/processed/eval_monthly_returns.csv",ROOT/"data/processed/eval_factors.csv",
           Path(__file__),ROOT/"analysis/bonds.py",ROOT/"analysis/portfolio_lab_scenarios.py",
           ROOT/"analysis/interactive_surplus_portfolio_lab.py"]
    receipt=dict(status="computed hypothetical scenarios",case_date="2022-12-31",
                 prepared_date_HCMC="2026-10-21",actual_revised_mandate_received=False,
                 equity_estimation="2015-2022 only; 60/96 month windows",evaluation_data_used_for_selection=False,
                 evaluation_use="Separate observed return-gap bridge; never fitted into the 2022 choice",
                 frozen_policy_unchanged=True,sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
                 assumptions=["No borrowing/shorting/derivatives","case bonds default-free",
                              "0% reinvestment on coupon and reserve cash","5bp initial bond and 10bp initial equity cost",
                              "New annual spending ring-fenced using extra Delta proceeds carried at 0%",
                              "Stress cap is one specified price shock at inception; fees included in contributed-capital loss",
                              "All-bond terminal solution conditional on assumed inflation; no absolute real guarantee"],
                 checks=["Original funding and hurdle reproduced","LP all-bond additional capital reproduced",
                         "Nonnegative dedicated cash at every payment date","Full budgets reconcile",
                         "Stress limits independently reconcile to fees + bond repricing + equity loss",
                         "All 36 model combinations are fully invested and long-only",
                         "Evaluation factor-gap bridge sums to the observed arithmetic return gap"])
    (OUT/"calculation_receipt.json").write_text(json.dumps(receipt,indent=2),encoding="utf-8")
    print(frame[["id","scenario","equity_surplus","required_equity_CAGR","additional_capital_for_fixed_nominal_goal"]].to_string(index=False))
    print(json.dumps(thresholds,indent=2))


def draw(frame):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter
    subset=frame.set_index("id").loc[["B0","L1","L2","L3","L4","L5","C1","G1","G2","G3","G4","Q1","X1","R1"]]
    fig,axes=plt.subplots(1,2,figsize=(15,8),gridspec_kw={"width_ratios":[1.05,1]})
    yy=np.arange(len(subset))
    labels=[f"{i}  {r.scenario}" for i,r in subset.iterrows()]
    for ax in axes: ax.spines[["top","right"]].set_visible(False);ax.grid(axis="x",alpha=.15)
    axes[0].barh(yy,subset.equity_surplus/1e6,color="#087f8c")
    axes[0].set_yticks(yy,labels,fontsize=8);axes[0].invert_yaxis()
    axes[0].set_xlabel("Invested equity surplus ($m)")
    axes[1].barh(yy,subset.required_equity_CAGR,color="#c08b40")
    axes[1].set_yticks(yy,[]);axes[1].invert_yaxis()
    axes[1].xaxis.set_major_formatter(PercentFormatter(1))
    axes[1].set_xlabel("Required compound equity return per year")
    axes[1].axvline(frame.iloc[0].required_equity_CAGR,color="#445c6f",ls="--",lw=1)
    for i,(_,r) in enumerate(subset.iterrows()):
        axes[0].text(r.equity_surplus/1e6+.05,i,f"{r.equity_surplus/1e6:.3f}",va="center",fontsize=8)
        axes[1].text(r.required_equity_CAGR+.001,i,f"{r.required_equity_CAGR:.2%}",va="center",fontsize=8)
    axes[0].set_xlim(0,max(subset.equity_surplus)/1e6*1.14)
    axes[1].set_xlim(0,max(subset.required_equity_CAGR)*1.2)
    fig.suptitle("Kappa | Hypothetical revised mandates",fontsize=17,color="#18334c",x=.48,y=.98)
    fig.text(.03,.015,"Case date 31 Dec 2022. Dedicated payment cash flows, 0% cash reinvestment. Required return is a hurdle, not a forecast.",fontsize=9)
    fig.tight_layout(rect=[0,.04,1,.95])
    fig.savefig(OUT/"mandate_tradeoffs.png",dpi=180)
    plt.close(fig)


if __name__=="__main__":
    main()
