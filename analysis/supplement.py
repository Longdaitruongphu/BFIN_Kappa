"""Offline robustness checks, source audit and executable assertions."""
from analyze import *
from bonds import BONDS,flows,root,curve

def main():
    cfg=CFG;fund=json.loads((TABLE/'funding_summary.json').read_text());decision=json.loads((TABLE/'decision_summary.json').read_text())
    # All-bond cash-flow dedication, allowing zero-interest cash carry.
    cfs=np.zeros((8,6));costs=[]
    for j,(_,n,c,p) in enumerate(BONDS):
        _,cf=flows(n,c);cfs[:n,j]=cf;costs.append(p*(1+cfg['bond_cost_per_dollar_traded']))
    cfs[0,5]=1;costs.append(1.) # initial cash can be carried with no interest
    cum=cfs.cumsum(axis=0);ob=np.array([0,2.4e6,2.4e6,2.4e6,6e6,6e6,6e6,6e6])
    res=opt.linprog(-cum[-1],A_ub=np.vstack([-cum[:7],costs]),b_ub=np.r_[-ob[:7],12e6],bounds=(0,None),method='highs')
    assert res.success
    terminal=float(cum[-1]@res.x-6e6)
    goal=8e6*1.025**8
    req=opt.linprog(costs,A_ub=-cum,b_ub=-(ob+np.r_[np.zeros(7),goal]),bounds=(0,None),method='highs')
    assert req.success
    save(pd.DataFrame({'instrument':[b[0] for b in BONDS]+['Cash'],'units':res.x,'unit_cost_with_fee':costs,'initial_dollars':np.array(costs)*res.x}),
         'all_bond_alternative.csv')
    save(pd.DataFrame({'year':range(1,9),'bond_cashflow':cfs@res.x,'cumulative_inflow':cum@res.x,'cumulative_obligation':ob,'remaining_cash':cum@res.x-ob}),
         'all_bond_cashflows.csv')
    summary=dict(max_fixed_nominal_terminal_2030=terminal,real_terminal_at_assumed_2_5pct_inflation=terminal/1.025**8,
                 initial_capital_for_original_real_goal_at_assumed_inflation=float(req.fun),additional_initial_capital=float(req.fun-12e6),
                 real_goal_reduction_fraction=1-terminal/1.025**8/8e6,
                 inflation_ceiling_for_8m_real=(terminal/8e6)**(1/8)-1,
                 limitation='Nominal cashflows assured under case default-free assumptions and zero-interest cash custody. Real value depends on future inflation. Mark-to-market loss limit is not guaranteed.')
    (TABLE/'all_bond_summary.json').write_text(json.dumps(summary,indent=2))
    # Verify standard YTM duration/convexity separately against exact YTM repricing.
    metrics=pd.read_csv(TABLE/'bond_metrics.csv').set_index('bond');rows=[]
    for name,n,c,p in BONDS:
        t,cf=flows(n,c);m=metrics.loc[name]
        for dy in [-.01,.01,.02]:
            exact=float(np.sum(cf/(1+m.ytm+dy)**t));approx=p*(1-m.modified_duration*dy+.5*m.yield_convexity*dy*dy)
            rows.append(dict(bond=name,ytm_change=dy,exact_price=exact,approx_price=approx,error=approx-exact))
    save(pd.DataFrame(rows),'ytm_duration_validation.csv')
    # Exact repricing under both calibrated interpolation conventions.
    t,d=curve();_,da=curve('linear_zero');rows=[]
    for name,n,c,p in BONDS:
        tt,cf=flows(n,c)
        for label,shock in [('parallel_100bp',np.full(n,.01)),('steepener',np.interp(tt,[1,8],[-.01,.01]))]:
            rows.append(dict(bond=name,scenario=label,log_discount_price=float(cf@(d[:n]*np.exp(-tt*shock))),
                  linear_zero_price=float(cf@(da[:n]*np.exp(-tt*shock)))))
    save(pd.DataFrame(rows),'curve_interpolation_sensitivity.csv')
    # Correct conventional historical excess-return Sharpe as an extra diagnostic.
    r=pd.read_csv(PROC/'train_monthly_returns.csv',index_col=0);f=pd.read_csv(PROC/'train_factors.csv',index_col=0)
    cov=r.cov().values*12
    excess_cov=r.sub(f.RF,axis=0).cov().values*12
    eta=optimize(r.mean().values*12,excess_cov,sharpe=True,sharpe_rf=float(f.RF.mean()*12))
    old=json.loads((POL/'frozen_policy.json').read_text())['alternatives']['Eta_historical_Sharpe']
    save(pd.DataFrame({'ticker':TICKERS,'frozen_weights':list(old.values()),'monthly_rf_sharpe_weights':eta}), 'historical_sharpe_definition_audit.csv')
    # Portfolio-level factor variance decomposition, allowing covariance cross-terms.
    r.index=pd.PeriodIndex(r.index,freq='M');f.index=r.index
    fac,res=regress(r[decision['recommended_ticker']],f,['Mkt-RF','SMB','HML'])
    x=f[['Mkt-RF','SMB','HML']];b=res.params.iloc[1:].values;fc=x.cov().values
    contributions=b*(fc@b);tot=(r[decision['recommended_ticker']]-f.RF).var(ddof=1)
    save(pd.DataFrame({'component':['Market','Size','Value','Residual'],'share_of_variance':np.r_[contributions,res.resid.var(ddof=1)]/tot,
                       'annual_variance_contribution':np.r_[contributions,res.resid.var(ddof=1)]*12}), 'factor_variance_decomposition.csv')
    # Unitized loss accounting example prevents programme payments being counted as investment losses.
    # Ex-ante -30% equity / +100bp rates stress was chosen before evaluation.
    stress=pd.read_csv(TABLE/'whole_fund_stress.csv')
    stressrow=stress[(stress.rate_scenario=='Parallel +100bp')&(stress.equity_shock==-.3)].iloc[0]
    eq_cap=(.15*12e6+stressrow.bond_value_change)/.3
    cut=max(0,fund['equity_investment']-eq_cap)
    tighter_cash=fund['terminal_cash']+cut
    reqg=((fund['nominal_goal']-tighter_cash)/eq_cap)**(1/8)-1
    # Coupon cash is already an asset in the baseline. Equity-to-cash reduction occurs at inception.
    # This is an indicative gross-of-extra-restructuring-cost sensitivity, not a revised mandate.
    (TABLE/'risk_limit_sensitivity.json').write_text(json.dumps(dict(
        specific_stress_equity_cap=eq_cap,equity_reduction=cut,extra_cash=cut,required_cagr_on_reduced_equity=reqg,
        baseline_stress_loss=float(stressrow.loss_fraction_initial_wealth),
        limitation='This cap satisfies only the specified instantaneous stress. It cannot guarantee a 15% maximum drawdown, especially after liabilities are paid.'),indent=2))
    # Audit raw file integrity against the actual successful online retrieval manifest.
    manifests=[json.loads(x) for x in (ROOT/'data/raw/retrieval_manifest.jsonl').read_text().splitlines()]
    checks=[]
    for entry in manifests:
        if entry.get('event')=='success':
            p=ROOT/entry['file'].replace('\\','/');checks.append(dict(check='raw_sha256',item=entry['file'],passed=digest(p)==entry['sha256']))
    frozen=POL/'frozen_policy.json';expected=(POL/'frozen_policy.sha256').read_text().split()[0]
    checks.append(dict(check='policy_sha256',item='frozen_policy.json',passed=digest(frozen)==expected))
    checks.append(dict(check='initial_budget',item='USD 12m',passed=abs(pd.read_csv(TABLE/'initial_allocation.csv').market_value.sum()-12e6)<.01))
    checks.append(dict(check='bond_repricing',item='all five bonds',passed=float(metrics.calibration_error.abs().max())<1e-7))
    for phase,n in [('train',96),('eval',36)]:
        rr=pd.read_csv(PROC/f'{phase}_monthly_returns.csv',index_col=0)
        checks.append(dict(check='common_months',item=phase,passed=len(rr)==n and not rr.isna().any().any() and rr.shape[1]==10))
    checks.append(dict(check='no_cash_shortfall',item='fixed payment funding',passed=pd.read_csv(TABLE/'funding_cashflows.csv').cumulative_cash_zero_reinvestment.min()>=0))
    save(pd.DataFrame(checks),'reproduction_checks.csv')
    assert all(x['passed'] for x in checks)
    print(json.dumps({'all_bond_alternative':summary,'checks_passed':len(checks),'eta_max_weight_difference':float(max(abs(eta-np.array(list(old.values())))))},indent=2))

if __name__=='__main__':main()
