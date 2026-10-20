"""Reproducible ex-ante portfolio comparison at 2022-12-31 and separate OOS review.

Reads only frozen, local project inputs. It never edits policy/frozen_policy.json.
Run: .venv\\Scripts\\python.exe analysis\\portfolio_choice_visuals.py
"""
from pathlib import Path
import json, hashlib, os
ROOT = Path(__file__).resolve().parents[1]
import numpy as np
import pandas as pd
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'logs'/'matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.optimize import brentq

OUT = ROOT / 'outputs'
TABLE = OUT / 'tables'
FIG = OUT / 'figures'
FIG.mkdir(parents=True, exist_ok=True)
CFG = json.loads((ROOT / 'analysis' / 'config.json').read_text(encoding='utf-8'))
TICKERS = CFG['stocks'] + CFG['etfs']
A = float(CFG['risk_aversion'])
POLICY = ROOT/'policy'/'frozen_policy.json'
POLICY_HASH_BEFORE = hashlib.sha256(POLICY.read_bytes()).hexdigest()

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'savefig.dpi':190})
COLORS = {'USMV':'#176B87','VTI':'#7A5195','50_50_ETF':'#A05195','Sample_A4':'#EF5675',
          'Single_index_A4':'#FFA600','Eta_historical_Sharpe':'#374C80',
          'Sample_A8':'#2F4B7C','Single_index_A8':'#665191'}

def read_weights():
    c = pd.read_csv(TABLE/'portfolio_candidates.csv').set_index('strategy')
    weights = {i: c.loc[i, TICKERS].to_numpy(float) for i in c.index}
    weights['USMV'] = np.eye(len(TICKERS))[TICKERS.index('USMV')]
    weights['VTI'] = np.eye(len(TICKERS))[TICKERS.index('VTI')]
    weights['50_50_ETF'] = .5*weights['USMV'] + .5*weights['VTI']
    return weights

def bt(r, w, cost=.001, initial_cost=False):
    """Same self-financing December rebalance logic as analysis/analyze.py."""
    w = np.asarray(w, float); w = w/w.sum(); v = w.copy()
    if initial_cost: v /= (1+cost)
    previous=1.; out=[]
    for i,(month,row) in enumerate(r.iterrows()):
        v *= (1+row.to_numpy(float)); value=float(v.sum()); fee=0.
        if month.month == 12 and month != r.index[-1]:
            target=brentq(lambda x:x+cost*np.abs(x*w-v).sum()-value,0,value)
            fee=value-target; v=target*w; value=target
        out.append(value/previous-1); previous=value
    return np.asarray(out)

def perf(x, rf):
    x=np.asarray(x); rf=np.asarray(rf); wealth=np.r_[1.,np.cumprod(1+x)]
    dd=wealth/np.maximum.accumulate(wealth)-1
    return {'total_return':wealth[-1]-1,'cagr':wealth[-1]**(12/len(x))-1,
            'annual_volatility':x.std(ddof=1)*np.sqrt(12),
            'annual_sharpe':(x-rf).mean()/(x-rf).std(ddof=1)*np.sqrt(12),
            'max_month_end_drawdown':dd.min()}

def main():
    weights=read_weights()
    mu_df=pd.read_csv(TABLE/'expected_return_inputs.csv').set_index('ticker')
    mu=mu_df.loc[TICKERS,'expected_arithmetic_return'].to_numpy(float)
    cov=pd.read_csv(TABLE/'sample_covariance.csv',index_col=0).loc[TICKERS,TICKERS].to_numpy(float)
    icov=pd.read_csv(TABLE/'single_index_covariance.csv',index_col=0).loc[TICKERS,TICKERS].to_numpy(float)
    train=pd.read_csv(ROOT/'data/processed/train_monthly_returns.csv',index_col=0,parse_dates=False)
    # Period strings are parsed explicitly to keep the same monthly sequence.
    train.index=pd.PeriodIndex(train.index,freq='M')
    evalr=pd.read_csv(ROOT/'data/processed/eval_monthly_returns.csv',index_col=0,parse_dates=False)
    evalr.index=pd.PeriodIndex(evalr.index,freq='M')
    rf_train=pd.read_csv(ROOT/'data/processed/train_factors.csv',index_col=0)['RF'].to_numpy(float)
    rf_eval=pd.read_csv(ROOT/'data/processed/eval_factors.csv',index_col=0)['RF'].to_numpy(float)
    assert len(train)==96 and len(evalr)==36 and len(rf_train)==96 and len(rf_eval)==36

    rows=[]; histories={}; oos={}
    for name,w in weights.items():
        w=np.array(w,float,copy=True)
        w[np.abs(w) < 1e-10] = 0.0
        if abs(w.sum()-1)>1e-8 or (w < -1e-9).any(): raise AssertionError(f'Invalid weights: {name}')
        h=bt(train[TICKERS],w); e=bt(evalr[TICKERS],w,initial_cost=True)
        m=float(mu@w); vs=float(w@cov@w); vi=float(w@icov@w)
        tr=perf(h,rf_train); ev=perf(e,rf_eval)
        rows.append({'strategy':name,'forecast_return':m,'sample_vol':np.sqrt(vs),
                     'single_index_vol':np.sqrt(vi),'CE_A4_sample_cov':m-.5*A*vs,
                     'CE_A4_single_index_cov':m-.5*A*vi,
                     **{'train_'+k:v for k,v in tr.items()},
                     **{'oos_'+k:v for k,v in ev.items()}})
        histories[name]=np.cumprod(1+h)
        oos[name]=np.cumprod(1+e)
    comp=pd.DataFrame(rows).sort_values('CE_A4_sample_cov',ascending=False)
    comp.to_csv(TABLE/'portfolio_comparison_decision_2022.csv',index=False,float_format='%.12g')
    # Independent reconciliation against the project's already-saved headline results.
    old_train=pd.read_csv(TABLE/'training_performance.csv').set_index('strategy')
    old_eval=pd.read_csv(TABLE/'evaluation_performance.csv').set_index('strategy')
    reconcile={'USMV':'Recommended','VTI':'Benchmark VTI','Sample_A4':'Sample_A4',
               'Single_index_A4':'Single_index_A4','Eta_historical_Sharpe':'Eta_historical_Sharpe'}
    for new,old in reconcile.items():
        nr=comp.set_index('strategy').loc[new]
        for metric in ['total_return','cagr','annual_volatility','annual_sharpe','max_month_end_drawdown']:
            if abs(nr['train_'+metric]-old_train.loc[new if new in old_train.index else ('USMV' if new=='USMV' else new),metric])>1e-9:
                raise AssertionError(f'Training reconciliation failed: {new}/{metric}')
            if abs(nr['oos_'+metric]-old_eval.loc[old,metric])>1e-9:
                raise AssertionError(f'Evaluation reconciliation failed: {new}/{metric}')

    # Growth-sleeve weight table and full-fund dollar bridge, holding liability sleeve fixed.
    f=json.loads((TABLE/'funding_summary.json').read_text(encoding='utf-8'))
    full=[]
    for name,w in weights.items():
        rec={'strategy':name,'Beta_bond_USD':f['beta_cost'],'Delta_bond_USD':f['delta_cost'],
             'trading_costs_USD':f['total_fees']}
        rec['equity_sleeve_USD']=f['equity_investment']
        for t,x in zip(TICKERS,w): rec[t+'_growth_weight']=x; rec[t+'_USD']=x*f['equity_investment']
        full.append(rec)
        allocated=f['beta_cost']+f['delta_cost']+f['equity_investment']+f['total_fees']
        if abs(allocated-CFG['initial_wealth']) > .01: raise AssertionError('Full-fund dollar bridge does not sum to initial wealth')
    pd.DataFrame(full).to_csv(TABLE/'portfolio_weights_and_full_fund_bridge.csv',index=False,float_format='%.12g')

    # Ex-ante risk-return map.  Forecast inputs are frozen at the 2022 cutoff.
    fig,ax=plt.subplots(figsize=(10,6.4))
    for name,row in comp.iterrows():
        strategy=row['strategy']; is_key=strategy in ['USMV','VTI','50_50_ETF','Sample_A4','Single_index_A4','Eta_historical_Sharpe']
        ax.scatter(row['sample_vol'],row['forecast_return'],s=80 if is_key else 42,
                   color=COLORS.get(strategy,'#9AA0A6'),alpha=1 if is_key else .48,
                   edgecolor='white',linewidth=.7,zorder=3 if is_key else 2)
        if is_key:
            label={'Single_index_A4':'Index A=4','Eta_historical_Sharpe':'Eta: train Sharpe',
                   '50_50_ETF':'50/50 ETFs','Sample_A4':'Sample A=4'}.get(strategy,strategy)
            ax.annotate(label,(row['sample_vol'],row['forecast_return']),xytext=(6,6),textcoords='offset points',fontsize=8)
    x=np.linspace(max(.08,comp.sample_vol.min()-.01),comp.sample_vol.max()+.01,200)
    for ce,color in [(0.03,'#AAAAAA'),(.04,'#777777')]:
        ax.plot(x,ce+.5*A*x*x,color=color,ls='--',lw=1,label=f'CE = {ce:.0%} at A={A:g} (sample covariance)')
    ax.set(xlabel='Annualized volatility from 2015–2022 sample covariance',ylabel='CAPM forecast arithmetic return',
           title='Growth-sleeve candidates at the 31 Dec 2022 decision date')
    ax.xaxis.set_major_formatter(PercentFormatter(1));ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.grid(alpha=.2);ax.legend(frameon=False,loc='upper left',fontsize=8)
    ax.text(.99,.02,'2015–2022 estimates only; CAPM forecast uses 4% RF + beta × 4.5% ERP, alpha = 0.\nPoints with different covariance estimators have CE evaluated under the common sample covariance here.',transform=ax.transAxes,ha='right',va='bottom',fontsize=7,color='#555')
    fig.tight_layout();fig.savefig(FIG/'portfolio_frontier_decision_2022.png');plt.close(fig)

    # Weight comparison for policy and a small set of contrasting portfolios.
    show=['USMV','VTI','50_50_ETF','Sample_A4','Single_index_A4','Eta_historical_Sharpe']
    wt=pd.DataFrame({k:weights[k] for k in show},index=TICKERS).T
    wt.to_csv(TABLE/'portfolio_weights_selected_growth_sleeve.csv',float_format='%.12g')
    fig,ax=plt.subplots(figsize=(11,5.6));bottom=np.zeros(len(show))
    pal=plt.cm.tab20(np.linspace(0,1,len(TICKERS)))
    for i,t in enumerate(TICKERS):
        vals=wt[t].to_numpy();ax.bar(show,vals,bottom=bottom,label=t,color=pal[i],width=.72);bottom+=vals
    ax.set_ylabel('Share of growth sleeve');ax.set_ylim(0,1);ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.set_title('Candidate weights; fixed liability-matching bonds sit outside this growth sleeve')
    ax.tick_params(axis='x',rotation=20);ax.legend(ncol=5,frameon=False,loc='upper center',bbox_to_anchor=(.5,-.17))
    ax.grid(axis='y',alpha=.18);fig.tight_layout();fig.savefig(FIG/'portfolio_weights_growth_sleeve.png',bbox_inches='tight');plt.close(fig)

    # Radar as a presentation aid only. Axes deliberately are NOT added into a total score.
    radar_names=['USMV','VTI','50_50_ETF','Sample_A4','Single_index_A4','Eta_historical_Sharpe']
    d=comp.set_index('strategy').loc[radar_names]
    raw=pd.DataFrame({'Forecast return':d.forecast_return,
                      'CE (A=4)':d.CE_A4_sample_cov,
                      'Lower volatility':-d.sample_vol,
                      'Training Sharpe':d.train_annual_sharpe,
                      'Shallower drawdown':d.train_max_month_end_drawdown},index=radar_names)
    scores=(raw-raw.min())/(raw.max()-raw.min()).replace(0,1)*100
    scores.to_csv(TABLE/'portfolio_radar_descriptive_scores.csv',float_format='%.12g')
    labels=list(scores.columns); angles=np.linspace(0,2*np.pi,len(labels),endpoint=False).tolist();angles+=angles[:1]
    fig=plt.figure(figsize=(8.5,7));ax=fig.add_subplot(111,polar=True)
    for name in radar_names:
        vals=scores.loc[name].tolist();vals+=vals[:1]
        ax.plot(angles,vals,label=name,color=COLORS.get(name,'#666'),lw=1.8)
        ax.fill(angles,vals,color=COLORS.get(name,'#666'),alpha=.035)
    ax.set_xticks(angles[:-1]);ax.set_xticklabels(labels,fontsize=8);ax.set_ylim(0,100)
    ax.set_yticks([20,40,60,80,100]);ax.set_yticklabels(['20','40','60','80','100'],fontsize=7)
    ax.set_title('Radar is a dashboard, not a validated total-score rule\nMin–max scaled across the six portfolios shown',pad=24)
    ax.legend(loc='upper left',bbox_to_anchor=(1.02,1.08),frameon=False,fontsize=8)
    fig.text(.5,.025,'Axes overlap economically (return, CE, volatility and drawdown are related). Do not sum them or choose the largest radar area. Training-only metrics and forecasts as of 31 Dec 2022.',ha='center',fontsize=8,color='#555')
    fig.tight_layout(rect=[0,.05,.82,1]);fig.savefig(FIG/'portfolio_radar_training_2022.png',bbox_inches='tight');plt.close(fig)

    # Strictly separate held-out evaluation; it does not enter 2022 selection/radar.
    oos_names=['USMV','VTI','50_50_ETF','Sample_A4','Single_index_A4','Eta_historical_Sharpe']
    erows=comp.set_index('strategy').loc[oos_names]
    fig,ax=plt.subplots(figsize=(9,5.5))
    for n,row in erows.iterrows():
        ax.scatter(row.oos_annual_volatility,row.oos_cagr,s=95,color=COLORS.get(n,'#777'),edgecolor='white',linewidth=.8)
        ax.annotate(n,(row.oos_annual_volatility,row.oos_cagr),xytext=(5,5),textcoords='offset points',fontsize=8)
    ax.set(xlabel='Annualized volatility, Jan 2023–Dec 2025',ylabel='Net CAGR, Jan 2023–Dec 2025',
           title='Out-of-sample review (36 months): evidence after the frozen 2022 decision')
    ax.xaxis.set_major_formatter(PercentFormatter(1));ax.yaxis.set_major_formatter(PercentFormatter(1));ax.grid(alpha=.2)
    ax.text(.99,.02,'Separate evaluation only; 2023–2025 data are not used to select the 2022 portfolio.',transform=ax.transAxes,ha='right',fontsize=8,color='#555')
    fig.tight_layout();fig.savefig(FIG/'portfolio_oos_2023_2025.png');plt.close(fig)

    # Preserve exact weights alongside strategy metrics in one convenient file.
    wdf=pd.DataFrame.from_dict(weights,orient='index',columns=TICKERS);wdf.index.name='strategy'
    wdf.reset_index().merge(comp,on='strategy').to_csv(TABLE/'portfolio_comparison_and_weights.csv',index=False,float_format='%.12g')
    POLICY_HASH_AFTER = hashlib.sha256(POLICY.read_bytes()).hexdigest()
    if POLICY_HASH_BEFORE != POLICY_HASH_AFTER: raise AssertionError('Frozen policy was unexpectedly modified')
    frozen_hash=hashlib.sha256(POLICY.read_bytes()).hexdigest()
    expected_hash=(ROOT/'policy'/'frozen_policy.sha256').read_text(encoding='utf-8').split()[0]
    if frozen_hash != expected_hash: raise AssertionError('Frozen-policy file does not match its saved hash receipt')
    receipt={'decision_cutoff':'2022-12-31','training_months':len(train),'evaluation_months':len(evalr),
             'risk_aversion_A':A,'forecast_rf':CFG['forecast_rf'],'forecast_erp':CFG['forecast_erp'],
             'forecast_alpha':CFG['forecast_alpha'],'max_single_stock_weight':CFG['individual_stock_limit'],
             'max_direct_stock_weight':CFG['aggregate_stock_limit'],
             'initial_wealth_bridge_usd':allocated,'frozen_policy_sha256_before':POLICY_HASH_BEFORE,
             'frozen_policy_sha256_after':POLICY_HASH_AFTER,'frozen_policy_preserved':True,
             'best_candidate_by_sample_cov_CE_A4':str(comp.iloc[0].strategy),
             'outputs':['outputs/tables/portfolio_comparison_decision_2022.csv',
                        'outputs/tables/portfolio_comparison_and_weights.csv',
                        'outputs/tables/portfolio_weights_selected_growth_sleeve.csv',
                        'outputs/tables/portfolio_weights_and_full_fund_bridge.csv',
                        'outputs/tables/portfolio_radar_descriptive_scores.csv',
                        'outputs/figures/portfolio_frontier_decision_2022.png',
                        'outputs/figures/portfolio_weights_growth_sleeve.png',
                        'outputs/figures/portfolio_radar_training_2022.png',
                        'outputs/figures/portfolio_oos_2023_2025.png']}
    (TABLE/'portfolio_comparison_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print('Wrote portfolio comparison tables and figures.')
    print(comp[['strategy','forecast_return','sample_vol','CE_A4_sample_cov','CE_A4_single_index_cov','train_annual_sharpe','train_max_month_end_drawdown','oos_cagr','oos_annual_sharpe']].to_string(index=False))

if __name__=='__main__': main()
