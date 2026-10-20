"""Surplus growth-sleeve combinations under a provisional capped scenario.

Important: the 10% single-stock / 30% direct-stock caps in analysis/config.json
were analyst-added working assumptions, not rules specified by the assignment or
confirmed by the user. Outputs from this script are capped-scenario sensitivity
only. Use interactive_surplus_portfolio_lab.py for the no-extra-cap baseline.
Primary estimate: CAPM expected returns, 2015-22 sample covariance, long-only.
This script does not mutate the frozen policy.
Run: .venv\\Scripts\\python.exe analysis\\surplus_portfolio_combinations.py
"""
from pathlib import Path
import json, hashlib, os
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'logs'/'matplotlib'))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.optimize import minimize

CFG=json.loads((ROOT/'analysis'/'config.json').read_text(encoding='utf-8'))
TABLE=ROOT/'outputs'/'tables'; FIG=ROOT/'outputs'/'figures'; FIG.mkdir(parents=True,exist_ok=True)
TICKERS=CFG['stocks']+CFG['etfs']; N_STOCKS=len(CFG['stocks'])
RF=float(CFG['forecast_rf']); A=float(CFG['risk_aversion'])
POLICY=ROOT/'policy'/'frozen_policy.json'; POLICY_HASH=hashlib.sha256(POLICY.read_bytes()).hexdigest()
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,
                     'axes.spines.right':False,'savefig.dpi':190})

def load_inputs():
    inp=pd.read_csv(TABLE/'expected_return_inputs.csv').set_index('ticker').loc[TICKERS]
    mu=inp.expected_arithmetic_return.to_numpy(float)
    cov=pd.read_csv(TABLE/'sample_covariance.csv',index_col=0).loc[TICKERS,TICKERS].to_numpy(float)
    icov=pd.read_csv(TABLE/'single_index_covariance.csv',index_col=0).loc[TICKERS,TICKERS].to_numpy(float)
    if len(inp)!=len(TICKERS) or not np.allclose(mu,RF+inp.beta.to_numpy(float)*CFG['forecast_erp'],atol=1e-9):
        raise AssertionError('Forecast returns do not reconcile to the saved CAPM assumptions')
    if not np.allclose(cov,cov.T,atol=1e-10) or np.linalg.eigvalsh(cov).min() < -1e-8:
        raise AssertionError('Sample covariance is not symmetric positive semidefinite')
    return mu,cov,icov

def optimize(mu,cov,kind,A=None):
    n=len(mu); bounds=[(0,CFG['individual_stock_limit'])]*N_STOCKS+[(0,1)]*(n-N_STOCKS)
    cons=[{'type':'eq','fun':lambda w:w.sum()-1},
          {'type':'ineq','fun':lambda w:CFG['aggregate_stock_limit']-w[:N_STOCKS].sum()}]
    def objective(w):
        var=max(float(w@cov@w),1e-15); ret=float(w@mu)
        if kind=='gmv':return var
        if kind=='sharpe':return -(ret-RF)/np.sqrt(var)
        if kind=='utility':return -(ret-.5*A*var)
        if kind=='maxreturn':return -ret
        raise ValueError(kind)
    starts=[np.r_[np.zeros(n-2),.5,.5],np.ones(n)/n]
    best=None
    for start in starts:
        # Make each start feasible by clipping and normalizing, with a simple ETF fallback.
        start=np.asarray(start,float);start[:N_STOCKS]=np.minimum(start[:N_STOCKS],CFG['individual_stock_limit'])
        if start[:N_STOCKS].sum()>CFG['aggregate_stock_limit']:
            start[:N_STOCKS]*=CFG['aggregate_stock_limit']/start[:N_STOCKS].sum()
        stock_total=start[:N_STOCKS].sum()
        if stock_total>=1 or start.sum()<=0:
            start=np.zeros(n);stock_total=0.
        start[N_STOCKS:]=0
        start[N_STOCKS:]=(1-stock_total)/(n-N_STOCKS)
        res=minimize(objective,start,method='SLSQP',bounds=bounds,constraints=cons,
                     options={'ftol':1e-12,'maxiter':3000})
        if res.success and (best is None or res.fun<best.fun):best=res
    if best is None: raise RuntimeError(f'Optimization failed: {kind}')
    w=np.maximum(best.x,0); w[np.abs(w)<1e-10]=0; w/=w.sum()
    return w

def metrics(w,mu,cov):
    risky=np.asarray(w[:len(TICKERS)],float);cash=float(w[len(TICKERS)]) if len(w)>len(TICKERS) else 0.
    ret=float(risky@mu+cash*RF);var=float(risky@cov@risky);vol=float(np.sqrt(var))
    stocks=float(risky[:N_STOCKS].sum())
    return {'expected_return':ret,'variance':var,'standard_deviation':vol,
            'sharpe_ratio':(ret-RF)/vol,'utility_A4':ret-.5*A*var,
            'weight_sum':float(risky.sum()+cash),'risk_free_cash_weight':cash,'direct_stock_weight':stocks,
            'ips_feasible':bool(np.min(w)>=-1e-9 and np.max(w[:N_STOCKS])<=CFG['individual_stock_limit']+1e-9
                                and stocks<=CFG['aggregate_stock_limit']+1e-9)}

def backtest(returns,w,cost=.001):
    """Project-consistent fixed-weight annual rebalance for the 2015-22 dashboard."""
    w=np.asarray(w,float); w=w/w.sum(); v=w.copy(); previous=1.; values=[]
    for month,row in returns.iterrows():
        v*=1+row.to_numpy(float); value=float(v.sum())
        if month.month==12 and month!=returns.index[-1]:
            from scipy.optimize import brentq
            target=brentq(lambda x:x+cost*np.abs(x*w-v).sum()-value,0,value)
            v=target*w; value=target
        values.append(value/previous-1);previous=value
    return np.asarray(values)

def realized_stats(r,rf):
    wealth=np.r_[1,np.cumprod(1+np.asarray(r))]
    dd=wealth/np.maximum.accumulate(wealth)-1
    excess=np.asarray(r)-np.asarray(rf)
    return {'training_cagr':wealth[-1]**(12/len(r))-1,
            'training_volatility':np.std(r,ddof=1)*np.sqrt(12),
            'training_sharpe':excess.mean()/excess.std(ddof=1)*np.sqrt(12),
            'training_max_drawdown':float(dd.min())}

def main():
    mu,cov,icov=load_inputs()
    combos={}
    combos['GMV']=optimize(mu,cov,'gmv')
    combos['Maximum_Sharpe_Tangency']=optimize(mu,cov,'sharpe')
    # Show how the optimizer moves across multiple stated risk-aversion assumptions.
    for aversion in [.5,1.,2.,3.,4.,6.,8.,10.,12.]:
        if aversion==2.:name='Aggressive_A2'
        elif aversion==4.:name='Maximum_Utility_A4'
        elif aversion==6.:name='Balanced_A6'
        elif aversion==8.:name='Conservative_A8'
        else:name=f'Utility_A{aversion:g}'
        combos[name]=optimize(mu,cov,'utility',aversion)
    combos['IPS_Feasible_Equal_Bucket']=np.r_[np.repeat(CFG['aggregate_stock_limit']/N_STOCKS,N_STOCKS),
                                              np.repeat((1-CFG['aggregate_stock_limit'])/len(CFG['etfs']),len(CFG['etfs']))]
    combos['USMV_Frozen_Policy']=np.eye(len(TICKERS))[TICKERS.index('USMV')]
    combos['VTI_Benchmark']=np.eye(len(TICKERS))[TICKERS.index('VTI')]
    for w_vti in [.2,.25,.5,.75,.8]:
        combos[f'ETF_Mix_VTI{int(round(w_vti*100))}_USMV{int(round((1-w_vti)*100))}']=np.eye(len(TICKERS))[TICKERS.index('VTI')]*w_vti+np.eye(len(TICKERS))[TICKERS.index('USMV')]*(1-w_vti)
    combos['Max_Utility_A4_Single_Index_Sensitivity']=optimize(mu,icov,'utility',A)
    eta=pd.read_csv(TABLE/'portfolio_candidates.csv').set_index('strategy').loc['Eta_historical_Sharpe',TICKERS].to_numpy(float)
    combos['Eta_Training_Sharpe_Proxy']=eta
    # Literal 1/N across all ten names is retained as a benchmark but violates the stock budget.
    combos['Equal_Weight_1N_All10_IPS_Violation']=np.repeat(1/len(TICKERS),len(TICKERS))
    # Complete-market Merton allocation, only if a 4% risk-free asset is actually investible.
    tangent=combos['Maximum_Sharpe_Tangency']; tm=metrics(tangent,mu,cov)
    y=(tm['expected_return']-RF)/(A*tm['variance'])
    y=float(np.clip(y,0,1)) # no borrowing; add explicit risk-free cash share
    combos['Maximum_Utility_A4_Conditional_RF']=np.r_[y*tangent,1-y]

    train=pd.read_csv(ROOT/'data'/'processed'/'train_monthly_returns.csv',index_col=0)
    train.index=pd.PeriodIndex(train.index,freq='M')
    rf_train=pd.read_csv(ROOT/'data'/'processed'/'train_factors.csv',index_col=0)['RF'].to_numpy(float)
    if len(train)!=96 or len(rf_train)!=96:raise AssertionError('Expected 96 training months')
    rows=[]
    for number,(name,w) in enumerate(combos.items(),start=1):
        m=metrics(w,mu,cov)
        risky=w[:len(TICKERS)];
        historical=({k:np.nan for k in ['training_cagr','training_volatility','training_sharpe','training_max_drawdown']}
                    if m['risk_free_cash_weight']>0 else realized_stats(backtest(train[TICKERS],risky),rf_train))
        rows.append({'portfolio_id':f'P{number:02d}','portfolio':name,**{t:float(x) for t,x in zip(TICKERS,risky)},**m,**historical,
                     'covariance_basis':'Single-index' if name.endswith('Sensitivity') else 'Sample',
                     'objective_note':('Literal 1/N reference only; direct stock weight breaches 30% IPS cap' if not m['ips_feasible'] else
                                       'Conditional only: assumes the full forecast 4% RF is investible for the horizon' if name.endswith('Conditional_RF') else '')})
    df=pd.DataFrame(rows)
    df.to_csv(TABLE/'surplus_portfolio_combinations.csv',index=False,float_format='%.12g')
    # Full-fund bridge: matched bonds and costs do not change between growth alternatives.
    fund=json.loads((TABLE/'funding_summary.json').read_text(encoding='utf-8'))
    fundrows=[]
    for name,w in combos.items():
        rec={'portfolio':name,'Beta_bond_cost_USD':fund['beta_cost'],'Delta_bond_cost_USD':fund['delta_cost'],
             'growth_sleeve_USD':fund['equity_investment'],'transaction_costs_USD':fund['total_fees']}
        risky=w[:len(TICKERS)];cash=float(w[len(TICKERS)]) if len(w)>len(TICKERS) else 0.
        rec.update({t+'_growth_sleeve_weight':float(x) for t,x in zip(TICKERS,risky)})
        rec.update({t+'_USD':float(x)*fund['equity_investment'] for t,x in zip(TICKERS,risky)})
        rec['Risk_Free_Cash_weight']=cash;rec['Risk_Free_Cash_USD']=cash*fund['equity_investment']
        fundrows.append(rec)
        if abs(fund['beta_cost']+fund['delta_cost']+fund['equity_investment']+fund['total_fees']-CFG['initial_wealth'])>.01:
            raise AssertionError('Full-fund capital bridge failed')
    pd.DataFrame(fundrows).to_csv(TABLE/'surplus_portfolio_full_fund_bridge.csv',index=False,float_format='%.12g')

    # Efficient frontier from mean-variance optimization (sample covariance).
    gmv=combos['GMV']; tangent=combos['Maximum_Sharpe_Tangency'][:len(TICKERS)]
    lo=metrics(gmv,mu,cov)['standard_deviation']; hi=metrics(optimize(mu,cov,'maxreturn'),mu,cov)['standard_deviation']
    targets=np.linspace(lo,hi,70); frontier=[]; prev=gmv.copy()
    bounds=[(0,CFG['individual_stock_limit'])]*N_STOCKS+[(0,1)]*(len(TICKERS)-N_STOCKS)
    consbase=[{'type':'eq','fun':lambda w:w.sum()-1},
              {'type':'ineq','fun':lambda w:CFG['aggregate_stock_limit']-w[:N_STOCKS].sum()}]
    for target in targets:
        cons=consbase+[{'type':'ineq','fun':lambda w,target=target:target**2-float(w@cov@w)}]
        res=minimize(lambda w:-float(w@mu),prev,method='SLSQP',bounds=bounds,constraints=cons,
                     options={'ftol':1e-11,'maxiter':3000})
        if res.success:
            prev=np.maximum(res.x,0);prev/=prev.sum();m=metrics(prev,mu,cov)
            frontier.append({'target_vol':target,**m})
    fdf=pd.DataFrame(frontier)
    fdf.to_csv(TABLE/'surplus_efficient_frontier.csv',index=False,float_format='%.12g')

    # Clear point chart: labels are compact IDs on the dots; a right-hand key gives exact
    # coordinates and comparison metrics for every one of the expanded combinations.
    df['portfolio_id']=df['portfolio_id'].astype(str)
    df.to_csv(TABLE/'surplus_portfolio_combinations.csv',index=False,float_format='%.12g')
    legend=df[['portfolio_id','portfolio','standard_deviation','expected_return','variance','sharpe_ratio',
               'utility_A4','direct_stock_weight','risk_free_cash_weight','ips_feasible','objective_note']].copy()
    legend.to_csv(TABLE/'surplus_portfolio_point_legend.csv',index=False,float_format='%.12g')
    fig=plt.figure(figsize=(17,10));gs=fig.add_gridspec(1,2,width_ratios=[1.45,1.0],wspace=.08)
    ax=fig.add_subplot(gs[0,0]);keyax=fig.add_subplot(gs[0,1]);keyax.axis('off')
    ax.plot(fdf.standard_deviation,fdf.expected_return,color='#176B87',lw=2.6,label='Efficient frontier (sample covariance)')
    tx=metrics(tangent,mu,cov)
    ax.plot([0,tx['standard_deviation']],[RF,tx['expected_return']],color='#C44E52',ls='--',lw=1.6,
            label='CAL from 4% forecast RF to tangency')
    cmap=plt.get_cmap('tab20')
    for i,row in df.iterrows():
        name=row['portfolio'];
        if name.startswith('Utility_A') or name in ['Aggressive_A2','Balanced_A6','Conservative_A8','Maximum_Utility_A4']:
            color=plt.get_cmap('viridis')(min(.95,max(.05,float(name.split('A')[-1])/12)))
        elif name.startswith('ETF_Mix_') or name in ['USMV_Frozen_Policy','VTI_Benchmark']:
            color='#1f77b4' if name!='USMV_Frozen_Policy' else '#164e83'
        elif name=='GMV':color='#2ca02c'
        elif name=='Maximum_Sharpe_Tangency':color='#d62728'
        elif name=='Max_Utility_A4_Single_Index_Sensitivity':color='#8c564b'
        elif name=='Equal_Weight_1N_All10_IPS_Violation':color='#777777'
        elif name=='Maximum_Utility_A4_Conditional_RF':color='#17becf'
        elif name=='IPS_Feasible_Equal_Bucket':color='#9467bd'
        else:color=cmap(i%20)
        marker='X' if not row['ips_feasible'] else ('D' if row['risk_free_cash_weight']>0 else 'o')
        ax.scatter(row['standard_deviation'],row['expected_return'],s=52,marker=marker,color=color,
                   edgecolor='white',linewidth=.6,zorder=4)
        # Put the IDs around the dense utility cluster using a rotating offset schedule.
        offsets={'P01':(14,-20),'P02':(12,16),'P03':(10,12),'P04':(-15,18),'P05':(-15,-8),
                 'P06':(-20,14),'P07':(16,-16),'P08':(-16,22),'P09':(18,-16),'P10':(-18,4),
                 'P11':(14,-22),'P12':(-22,10),'P13':(20,14),'P14':(16,-12),'P15':(-16,10),
                 'P16':(16,12),'P17':(-18,-10),'P18':(-18,14),'P19':(18,16),'P20':(23,8),
                 'P21':(-22,0),'P22':(16,-2),'P23':(12,12)}
        dx,dy=offsets[row['portfolio_id']]
        ax.annotate(row['portfolio_id'],(row['standard_deviation'],row['expected_return']),xytext=(dx,dy),
                    textcoords='offset points',fontsize=6.5,ha='center',va='center',
                    bbox={'boxstyle':'circle,pad=.16','fc':'white','ec':color,'lw':.8,'alpha':.95},
                    arrowprops={'arrowstyle':'-','lw':.35,'color':color})
    ax.scatter([0],[RF],marker='D',s=40,color='black',label='Forecast RF reference (4%)',zorder=5)
    ax.set(xlabel='Annualized standard deviation σp',ylabel='Forecast arithmetic return E(Rp)',
           title='Portfolio points (ID labels match key)\n2015–2022 inputs; decision date 31 Dec 2022')
    ax.set_xlim(-.01,.205);ax.set_ylim(.0375,.095)
    ax.xaxis.set_major_formatter(PercentFormatter(1));ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.grid(alpha=.22);ax.legend(frameon=False,loc='upper left',fontsize=7)
    ax.text(.02,.015,'X = violates direct-stock cap. Diamonds include conditional RF cash.\nCAL is illustrative: 4% is a forecast, not a guaranteed holding-period yield.',
            transform=ax.transAxes,ha='left',va='bottom',fontsize=7,color='#555')
    # Compact key carries names and actual point coordinates; full weights stay in the CSV.
    keyax.set_title('Point key: coordinates and scorecard',loc='left',fontsize=10,pad=8)
    keyax.text(.01,.985,'ID Portfolio | (σ; E[R]) | Var | Sharpe | U(A=4) | direct stock %',
               transform=keyax.transAxes,va='top',fontsize=7.5,fontweight='bold')
    y=.955
    for _,r in df.iterrows():
        status=' X' if not r.ips_feasible else ''
        label=(f"{r.portfolio_id}  {r.portfolio.replace('_',' ')} | "
               f"({r.standard_deviation:.2%}; {r.expected_return:.2%}) | "
               f"{r.variance:.5f} | {r.sharpe_ratio:.3f} | {r.utility_A4:.2%} | {r.direct_stock_weight:.1%}{status}")
        keyax.text(.01,y,label,transform=keyax.transAxes,va='top',fontsize=6.2,
                   color='#9a2222' if not r.ips_feasible else '#202020')
        y-=.034
    fig.suptitle('Surplus growth-sleeve comparison: sample-covariance efficient frontier and CAPM forecasts',y=.99,fontsize=13)
    fig.subplots_adjust(left=.07,right=.98,top=.9,bottom=.08,wspace=.08)
    fig.savefig(FIG/'surplus_efficient_frontier_CAL.png',bbox_inches='tight');plt.close(fig)

    # Radar stays deliberately to a small, named representative set; it is a visual dashboard,
    # not a summed-score ranking. Scaling uses all feasible risky portfolios in this comparison.
    radar_names=['GMV','Maximum_Sharpe_Tangency','Maximum_Utility_A4','Conservative_A8',
                 'Aggressive_A2','USMV_Frozen_Policy','VTI_Benchmark','IPS_Feasible_Equal_Bucket']
    eligible=df[(df.ips_feasible)&(df.risk_free_cash_weight==0)].set_index('portfolio')
    raw=pd.DataFrame({'Forecast return':eligible.expected_return,
                      'CE at A=4':eligible.utility_A4,
                      'Forecast Sharpe':eligible.sharpe_ratio,
                      'Lower forecast volatility':-eligible.standard_deviation,
                      'Shallower 2015–22 drawdown':eligible.training_max_drawdown})
    scores=(raw-raw.min())/(raw.max()-raw.min()).replace(0,1)*100
    rscores=scores.loc[radar_names]
    idmap=df.set_index('portfolio')['portfolio_id'].to_dict()
    rscores.insert(0,'portfolio_id',[idmap[n] for n in radar_names])
    rscores.to_csv(TABLE/'surplus_portfolio_radar_scores.csv',float_format='%.12g')
    scorecols=list(scores.columns)
    angles=np.linspace(0,2*np.pi,len(scorecols),endpoint=False).tolist();angles+=angles[:1]
    fig=plt.figure(figsize=(15,9));gs=fig.add_gridspec(1,2,width_ratios=[1.25,.9],wspace=.06)
    rax=fig.add_subplot(gs[0,0],polar=True);tabax=fig.add_subplot(gs[0,1]);tabax.axis('off')
    palette=plt.cm.tab10(np.linspace(0,1,len(radar_names)))
    for color,name in zip(palette,radar_names):
        vals=scores.loc[name].to_list();vals+=vals[:1]
        rax.plot(angles,vals,label=f"{idmap[name]} {name.replace('_',' ')}",lw=1.8,color=color,marker='o',markersize=3.5)
    rax.set_xticks(angles[:-1]);rax.set_xticklabels(scorecols,fontsize=8)
    rax.set_ylim(0,100);rax.set_yticks([20,40,60,80,100]);rax.set_yticklabels(['20','40','60','80','100'],fontsize=7)
    rax.legend(loc='upper left',bbox_to_anchor=(-.02,-.09),frameon=False,fontsize=7.3,ncol=2)
    tabax.set_title('Exact normalized score by axis',loc='left',fontsize=10,pad=10)
    data=[]
    for name in radar_names:
        data.append([idmap[name],name.replace('_',' '),*[f'{scores.loc[name,c]:.0f}' for c in scorecols]])
    table=tabax.table(cellText=data,colLabels=['ID','Portfolio','Return','CE A4','Sharpe','Low vol','Shallow DD'],
                      cellLoc='center',colLoc='center',loc='upper left',colWidths=[.08,.34,.11,.11,.11,.12,.13])
    table.auto_set_font_size(False);table.set_fontsize(7.5);table.scale(1,1.6)
    tabax.text(.01,.25,'Scores are min–max normalized across all IPS-feasible, fully invested risky candidates in the comparison.\nHigher is better on each plotted axis. These axes overlap; do not add scores or select by polygon area.',
               transform=tabax.transAxes,va='top',fontsize=8,color='#555')
    fig.suptitle('Surplus allocation radar: a visual profile, not an optimization objective',y=.99,fontsize=13)
    fig.text(.5,.02,'Training drawdown uses monthly 2015–2022 data and the project rebalance rule; forecast return, CE, Sharpe and volatility use CAPM/covariance inputs.',ha='center',fontsize=8,color='#555')
    fig.subplots_adjust(left=.04,right=.98,top=.92,bottom=.08,wspace=.04)
    fig.savefig(FIG/'surplus_portfolio_radar.png',bbox_inches='tight');plt.close(fig)

    # Contribution/readability receipt and safeguards.
    for name,w in combos.items():
        if abs(w.sum()-1)>1e-8: raise AssertionError(f'Weights do not sum to 100%: {name}')
        if name!='Equal_Weight_1N_All10_IPS_Violation' and not metrics(w,mu,cov)['ips_feasible']:
            raise AssertionError(f'Portfolio unexpectedly breaches IPS: {name}')
    if hashlib.sha256(POLICY.read_bytes()).hexdigest()!=POLICY_HASH:
        raise AssertionError('Frozen policy changed')
    rec={'cutoff':'2022-12-31','training_months':96,'primary_return_model':'CAPM: forecast RF 4% + beta x ERP 4.5%; alpha 0',
         'primary_covariance':'2015-01 to 2022-12 sample covariance annualized by existing project pipeline',
         'cashflows_funded_by_bonds':['2024 payment: Beta','2027 payment: Delta'],
         'surplus_growth_usd':fund['equity_investment'],'forecast_risk_free_for_Sharpe_and_CAL':RF,
         'risk_aversion_A':A,'policy_hard_constraints':{'long_only':True,'max_single_stock':CFG['individual_stock_limit'],'max_direct_stocks':CFG['aggregate_stock_limit']},
         'literal_equal_weight_feasible':False,'single_index_sensitivity_included':True,
         'conditional_CAL_utility_A4_cash_weight':float(combos['Maximum_Utility_A4_Conditional_RF'][-1]),
         'frozen_policy_sha256':POLICY_HASH,'frozen_policy_preserved':True,
         'portfolio_combinations':len(df),
         'files':['outputs/tables/surplus_portfolio_combinations.csv','outputs/tables/surplus_portfolio_point_legend.csv',
                  'outputs/tables/surplus_portfolio_radar_scores.csv','outputs/tables/surplus_portfolio_full_fund_bridge.csv',
                  'outputs/tables/surplus_efficient_frontier.csv','outputs/figures/surplus_efficient_frontier_CAL.png',
                  'outputs/figures/surplus_portfolio_radar.png']}
    (TABLE/'surplus_portfolio_receipt.json').write_text(json.dumps(rec,indent=2),encoding='utf-8')
    print(df[['portfolio','expected_return','standard_deviation','variance','sharpe_ratio','utility_A4','weight_sum','direct_stock_weight','ips_feasible']].to_string(index=False))
    print(f'Wrote frontier with {len(fdf)} feasible frontier points; frozen policy hash preserved.')

if __name__=='__main__': main()
