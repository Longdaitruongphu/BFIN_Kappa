"""Case bonds only: contractual cash flows, calibrated curve, risk, funding.
No market price history is fabricated for these fictional instruments.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

BONDS=[('Alpha',1,0.,958.77),('Beta',2,0.,922.78),('Gamma',3,.04,1002.49),('Delta',5,.035,986.07),('Epsilon',8,.045,1040.71)]

def root(f,lo=-.1,hi=1.,tol=1e-13):
    if f(lo)*f(hi)>0: raise ValueError('Root not bracketed')
    for _ in range(200):
        mid=(lo+hi)/2
        if hi-lo<tol: return mid
        if f(lo)*f(mid)<=0: hi=mid
        else: lo=mid
    return mid

def flows(n,c):
    cf=np.full(n,1000*c); cf[-1]+=1000
    return np.arange(1,n+1,dtype=float),cf

def curve(kind='log_discount'):
    knots=[0.]; vals=[0.] # log discount, with D(0)=1
    for name,n,c,p in BONDS:
        t,cf=flows(n,c)
        def discounts(last):
            xx=np.array(knots+[n]); yy=np.array(vals+[last])
            if kind=='log_discount': return np.exp(np.interp(t,xx,yy))
            zz=-yy[1:]/xx[1:]
            return np.exp(-t*np.interp(t,xx[1:],zz))
        last=root(lambda x:float(cf@discounts(x))-p,-2.,.3)
        knots.append(float(n)); vals.append(last)
    ts=np.arange(1,9,dtype=float)
    if kind=='log_discount': ds=np.exp(np.interp(ts,knots,vals))
    else: ds=np.exp(-ts*np.interp(ts,knots[1:],-np.array(vals[1:])/np.array(knots[1:])))
    return ts,ds

def build(cfg,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    t,d=curve();_,d_alt=curve('linear_zero')
    curve_df=pd.DataFrame({'year':t,'discount_factor':d,'continuous_spot':-np.log(d)/t,
                          'annual_effective_spot':d**(-1/t)-1,'alternative_linear_zero_discount':d_alt})
    curve_df.to_csv(out/'bond_curve.csv',index=False)
    metrics=[];stress=[]
    for name,n,c,p in BONDS:
        tt,cf=flows(n,c); dd=d[:n];y=root(lambda y:float(cf/(1+y)**tt @ np.ones(n))-p)
        pv=cf/(1+y)**tt
        mac=float(tt@pv/p); mod=mac/(1+y); conv=float((tt*(tt+1))@pv/(p*(1+y)**2))
        dc=float(tt@(cf*dd)/p);cc=float(tt**2@(cf*dd)/p)
        metrics.append(dict(bond=name,maturity=n,coupon=c,price=p,ytm=y,macaulay_duration=mac,modified_duration=mod,
                            yield_convexity=conv,curve_parallel_duration=dc,curve_parallel_convexity=cc,calibration_error=float(cf@dd-p)))
        for label,shock in [('Parallel +100bp',np.full(n,.01)),('Parallel -100bp',np.full(n,-.01)),
                             ('Steepener -100 to +100bp',np.interp(tt,[1,8],[-.01,.01])),
                             ('Parallel +200bp',np.full(n,.02))]:
            exact=float(cf@(dd*np.exp(-tt*shock)))
            approx=float(p-np.sum(cf*dd*tt*shock)+.5*np.sum(cf*dd*tt**2*shock**2))
            stress.append(dict(bond=name,scenario=label,base_price=p,exact_price=exact,approx_price=approx,
                               exact_return=exact/p-1,approx_return=approx/p-1,approx_error_dollars=approx-exact))
    pd.DataFrame(metrics).to_csv(out/'bond_metrics.csv',index=False)
    pd.DataFrame(stress).to_csv(out/'bond_stress.csv',index=False)
    # Ring-fence Beta principal and Delta final coupon + principal.
    beta_face=cfg['payment_year_2'];delta_face=cfg['payment_year_5']/1.035
    beta_cost=beta_face*.92278;delta_cost=delta_face*.98607
    bond_cost=beta_cost+delta_cost;fees=bond_cost*cfg['bond_cost_per_dollar_traded']
    equity=(cfg['initial_wealth']-bond_cost-fees)/(1+cfg['equity_cost_per_dollar_traded'])
    equity_fees=equity*cfg['equity_cost_per_dollar_traded']
    coupon=delta_face*.035
    cash=0;rows=[]
    for year in range(1,9):
        beta=beta_face if year==2 else 0
        delta=coupon if year<=5 else 0
        principal=delta_face if year==5 else 0
        pay=cfg['payment_year_2'] if year==2 else cfg['payment_year_5'] if year==5 else 0
        cash+=beta+delta+principal-pay
        rows.append(dict(year=year,date=f'{2022+year}-12-31',beta_maturity=beta,delta_coupon=delta,delta_principal=principal,
                         mandatory_payment=pay,net_to_cash=beta+delta+principal-pay,cumulative_cash_zero_reinvestment=cash))
    pd.DataFrame(rows).to_csv(out/'funding_cashflows.csv',index=False)
    # Feasible alternative: retain early coupons to partly fund the 2024 payment, at zero interest.
    alt_beta_face=cfg['payment_year_2']-2*coupon
    alt_bond=alt_beta_face*.92278+delta_cost
    alt_eq=(cfg['initial_wealth']-alt_bond*(1+cfg['bond_cost_per_dollar_traded']))/(1+cfg['equity_cost_per_dollar_traded'])
    alternatives=pd.DataFrame([
        dict(policy='Separate payment rings',beta_face=beta_face,delta_face=delta_face,bond_cost=bond_cost,equity=equity,surplus_cash_2030=4*coupon),
        dict(policy='Coupons earmarked for year 2',beta_face=alt_beta_face,delta_face=delta_face,bond_cost=alt_bond,equity=alt_eq,surplus_cash_2030=2*coupon)])
    alternatives.to_csv(out/'funding_alternatives.csv',index=False)
    terminal_cash=4*coupon
    goal=cfg['real_goal']*(1+cfg['inflation'])**8
    required=((goal-terminal_cash)/equity)**(1/8)-1
    sensitivity=[]
    for pi in [.02,.025,.03,.04,.05]:
        for reinv in [0,.02,.04]:
            cash_fv=sum(coupon*(1+reinv)**(8-y) for y in range(1,5))
            target=cfg['real_goal']*(1+pi)**8
            sensitivity.append(dict(inflation=pi,cash_reinvestment=reinv,nominal_goal=target,cash_2030=cash_fv,
                required_equity_cagr=((target-cash_fv)/equity)**(1/8)-1))
    pd.DataFrame(sensitivity).to_csv(out/'goal_sensitivity.csv',index=False)
    portfolio_stress=[]
    for label in pd.DataFrame(stress).scenario.unique():
        sub=pd.DataFrame(stress).set_index(['scenario','bond'])
        bv=beta_face/1000*sub.loc[(label,'Beta'),'exact_price']+delta_face/1000*sub.loc[(label,'Delta'),'exact_price']
        for eqshock in [-.2,-.3,-.4]:
            change=bv-bond_cost+equity*eqshock
            portfolio_stress.append(dict(rate_scenario=label,equity_shock=eqshock,bond_value_change=bv-bond_cost,
                 total_value_change=change,loss_fraction_initial_wealth=-change/cfg['initial_wealth'],
                 payment_cashflows_unchanged=True))
    pd.DataFrame(portfolio_stress).to_csv(out/'whole_fund_stress.csv',index=False)
    summary=dict(beta_face=beta_face,delta_face=delta_face,beta_cost=beta_cost,delta_cost=delta_cost,bond_cost=bond_cost,
                 bond_fees=fees,equity_investment=equity,equity_fees=equity_fees,total_fees=fees+equity_fees,
                 annual_delta_coupon=coupon,terminal_cash=terminal_cash,nominal_goal=goal,required_equity_cagr=required,
                 initial_equity_weight=equity/cfg['initial_wealth'],alternative_coupon_earmarked_equity=alt_eq)
    (out/'funding_summary.json').write_text(json.dumps(summary,indent=2))
    assert abs(beta_cost+delta_cost+equity+fees+equity_fees-cfg['initial_wealth'])<1e-6
    assert max(abs(r['calibration_error']) for r in metrics)<1e-7
    assert min(r['cumulative_cash_zero_reinvestment'] for r in rows)>=0
    return summary
