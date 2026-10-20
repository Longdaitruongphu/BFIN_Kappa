"""Offline analysis from saved raw files. No network imports or requests.
Run --stage train --freeze before downloading eval; then --stage all.
"""
from pathlib import Path
import argparse,datetime as dt,hashlib,io,json,sys,zipfile,re,os
ROOT=Path(__file__).resolve().parents[1]
if (ROOT.parent/'.analysis_packages').exists():sys.path.insert(0,str(ROOT.parent/'.analysis_packages'))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'logs/matplotlib'))
import numpy as np
import pandas as pd
import scipy.optimize as opt
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from bonds import build as build_bonds

CFG=json.loads((ROOT/'analysis/config.json').read_text())
TICKERS=CFG['stocks']+CFG['etfs']
TABLE=ROOT/'outputs/tables';PROC=ROOT/'data/processed';FIG=ROOT/'outputs/figures';POL=ROOT/'policy'
for folder in [TABLE,PROC,FIG,POL,ROOT/'logs']:folder.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':170})

def save(df,name,index=False):df.to_csv(TABLE/name,index=index,float_format='%.12g')
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_prices(phase):
    raw=ROOT/'data/raw'/phase; monthly={};closes={};audit=[];actions=[];dates={}
    for ticker in TICKERS:
        p=raw/f'{ticker}_daily.csv'
        df=pd.read_csv(p);df['Date']=pd.to_datetime(df['Date'].astype(str).str[:10])
        if df['Date'].duplicated().any():raise ValueError(f'Duplicate dates: {ticker}')
        df=df.set_index('Date').sort_index()
        if (df['Adj Close'].dropna()<=0).any():raise ValueError(f'Nonpositive prices: {ticker}')
        group=df.groupby(df.index.to_period('M'))
        # iloc[-1] preserves a missing final observation instead of silently moving to an earlier date.
        end=group.tail(1);idx=end.index.to_period('M')
        monthly[ticker]=pd.Series(end['Adj Close'].values,index=idx)
        closes[ticker]=pd.Series(end['Close'].values,index=idx)
        dates[ticker]=pd.Series(end.index.astype(str).values,index=idx)
        for month,g in group:
            audit.append(dict(phase=phase,ticker=ticker,month=str(month),observations=len(g),
                              last_trading_date=str(g.index[-1].date()),missing_adjusted=int(g['Adj Close'].isna().sum())))
        for day,row in df.iterrows():
            if row.get('Dividends',0)!=0 or row.get('Stock Splits',0)!=0:
                actions.append(dict(phase=phase,ticker=ticker,date=str(day.date()),dividend=row.get('Dividends',0),split=row.get('Stock Splits',0)))
    prices=pd.DataFrame(monthly);unadjusted=pd.DataFrame(closes)
    returns=prices.pct_change(fill_method=None)
    a,b=('2015-01','2022-12') if phase=='train' else ('2023-01','2025-12')
    expected=pd.period_range(a,b,freq='M')
    returns=returns.reindex(expected)
    if returns.isna().any().any():raise ValueError('Missing return observations. No fill or silent complete-case deletion allowed.')
    date_matrix=pd.DataFrame(dates).loc[expected]
    if (date_matrix.nunique(axis=1)!=1).any():raise ValueError('Last trading dates differ across the candidate universe')
    returns.index.name='month';prices.index.name='month'
    returns.to_csv(PROC/f'{phase}_monthly_returns.csv',float_format='%.15g')
    prices.to_csv(PROC/f'{phase}_month_end_adjusted_prices.csv',float_format='%.15g')
    unadjusted.to_csv(PROC/f'{phase}_month_end_close_prices.csv',float_format='%.15g')
    date_matrix.to_csv(PROC/f'{phase}_month_end_dates.csv')
    save(pd.DataFrame(audit),f'{phase}_data_quality.csv');save(pd.DataFrame(actions),f'{phase}_corporate_actions.csv')
    return returns,prices

def load_factors(phase,idx):
    p=ROOT/'data/raw'/phase/'F-F_Research_Data_Factors_CSV.zip'
    with zipfile.ZipFile(p) as z:
        contents=z.read(z.namelist()[0]).decode('utf-8-sig')
    lines=contents.splitlines();header=next(x for x in lines if 'Mkt-RF' in x and 'SMB' in x)
    monthly=[x for x in lines if re.match(r'^\s*\d{6},',x)]
    frame=pd.read_csv(io.StringIO(header+'\n'+'\n'.join(monthly)),index_col=0)
    frame.columns=frame.columns.str.strip()
    frame.index=pd.PeriodIndex(frame.index.astype(str),freq='M')
    if frame.index.duplicated().any():raise ValueError('Duplicate factor months')
    frame=frame.astype(float)/100 # Vendor percentages to decimal returns, including RF.
    missing=idx.difference(frame.index)
    if len(missing):raise ValueError('Factor months missing: '+str(missing))
    frame=frame.loc[idx];frame.index.name='month'
    if frame.isna().any().any():raise ValueError('Missing factor observations')
    frame.to_csv(PROC/f'{phase}_factors.csv',float_format='%.15g')
    (ROOT/'logs'/f'{phase}_factor_header.txt').write_text('\n'.join(lines[:5]),encoding='utf-8')
    return frame

def backtest(returns,weights,cost=.001,initial_cost=False):
    w=np.asarray(weights,dtype=float);w=w/w.sum();v=w.copy()
    if initial_cost:v/=1+cost
    previous=1.;rows=[]
    for month,row in returns.iterrows():
        v*=1+row.values
        value=float(v.sum());turnover=0.;fee=0.
        # Annual rebalance after December. There is no sale at evaluation end.
        if month.month==12 and month!=returns.index[-1]:
            # Solve the self-financing post-cost target value.
            target=opt.brentq(lambda x:x+cost*np.abs(x*w-v).sum()-value,0,value)
            turnover=float(np.abs(target*w-v).sum()/value);fee=value-target;v=target*w;value=target
        rows.append(dict(month=str(month),return_net=value/previous-1,wealth=value,turnover=turnover,cost=fee))
        previous=value
    return pd.DataFrame(rows).set_index('month')

def performance(r,rf):
    r=np.asarray(r);rf=np.asarray(rf)
    wealth=np.r_[1,np.cumprod(1+r)];dd=wealth/np.maximum.accumulate(wealth)-1
    excess=r-rf
    rolling=pd.Series(r).rolling(12).apply(lambda x:np.prod(1+x)-1,raw=True).dropna()
    return dict(months=len(r),total_return=wealth[-1]-1,cagr=wealth[-1]**(12/len(r))-1,
                annual_volatility=r.std(ddof=1)*np.sqrt(12),annual_sharpe=excess.mean()/excess.std(ddof=1)*np.sqrt(12),
                max_month_end_drawdown=dd.min(),worst_month=r.min(),worst_rolling_12m=float(rolling.min()))

def optimize(mu,cov,A=4,sharpe=False,sharpe_rf=None):
    n=len(mu);bounds=[(0,CFG['individual_stock_limit'])]*len(CFG['stocks'])+[(0,1)]*2
    cons=[{'type':'eq','fun':lambda w:w.sum()-1},
          {'type':'ineq','fun':lambda w:CFG['aggregate_stock_limit']-w[:len(CFG['stocks'])].sum()}]
    def fun(w):
        if sharpe:return -float((w@mu-(CFG['forecast_rf'] if sharpe_rf is None else sharpe_rf))/np.sqrt(w@cov@w))
        return -float(w@mu-.5*A*w@cov@w)
    initial=np.r_[np.zeros(n-2),.5,.5]
    result=opt.minimize(fun,initial,method='SLSQP',bounds=bounds,constraints=cons,options={'ftol':1e-12,'maxiter':2000})
    if not result.success:raise ValueError(result.message)
    w=np.maximum(result.x,0);w/=w.sum()
    if w[:n-2].sum()>CFG['aggregate_stock_limit']+1e-7:raise ValueError('Stock constraint failed')
    return w

def regress(y,f,cols):
    x=sm.add_constant(f[cols]);res=sm.OLS(y-f['RF'],x).fit(cov_type='HAC',cov_kwds={'maxlags':3})
    ci=res.conf_int()
    rec=dict(n=int(res.nobs),r_squared=float(res.rsquared),adjusted_r_squared=float(res.rsquared_adj),
             alpha_annual=float(res.params['const']*12),alpha_low=float(ci.loc['const',0]*12),alpha_high=float(ci.loc['const',1]*12),
             alpha_pvalue=float(res.pvalues['const']))
    for k in cols:
        rec[k]=float(res.params[k]);rec[k+'_low']=float(ci.loc[k,0]);rec[k+'_high']=float(ci.loc[k,1]);rec[k+'_pvalue']=float(res.pvalues[k])
    return rec,res

def train(funding,freeze):
    r,prices=load_prices('train');f=load_factors('train',r.index)
    assert len(r)==96 and r.index.max()==pd.Period('2022-12')
    excess=r.sub(f['RF'],axis=0)
    cov=r.cov().values*12
    m=f['Mkt-RF'];beta=np.array([np.cov(excess[x],m,ddof=1)[0,1]/m.var(ddof=1) for x in TICKERS])
    residual=excess-excess.mean()-np.outer(m-m.mean(),beta)
    index_cov=np.outer(beta,beta)*m.var(ddof=1)*12+np.diag(residual.var(ddof=1).values*12)
    mu=CFG['forecast_rf']+beta*CFG['forecast_erp']
    save(pd.DataFrame(cov,index=TICKERS,columns=TICKERS),'sample_covariance.csv',True)
    save(pd.DataFrame(index_cov,index=TICKERS,columns=TICKERS),'single_index_covariance.csv',True)
    save(residual.corr(),'single_index_residual_correlation.csv',True)
    inputs=pd.DataFrame({'ticker':TICKERS,'beta':beta,'expected_arithmetic_return':mu,'historical_arithmetic_return':r.mean().values*12,
                         'sample_volatility':np.sqrt(np.diag(cov)),'single_index_volatility':np.sqrt(np.diag(index_cov))})
    save(inputs,'expected_return_inputs.csv')
    weights={};rows=[]
    for name,mat in [('Sample',cov),('Single_index',index_cov)]:
        for A in [1.,2.,4.,6.,8.]:
            w=optimize(mu,mat,A);key=f'{name}_A{A:g}';weights[key]=w
            rows.append(dict(strategy=key,A=A,forecast_return=w@mu,sample_vol=np.sqrt(w@cov@w),index_vol=np.sqrt(w@index_cov@w),
                             model_CE=w@mu-.5*A*w@mat@w,**dict(zip(TICKERS,w))))
    eta=optimize(r.mean().values*12,cov,sharpe=True);weights['Eta_historical_Sharpe']=eta
    rows.append(dict(strategy='Eta_historical_Sharpe',A=np.nan,forecast_return=eta@mu,sample_vol=np.sqrt(eta@cov@eta),
                     index_vol=np.sqrt(eta@index_cov@eta),model_CE=eta@mu-2*eta@cov@eta,**dict(zip(TICKERS,eta))))
    save(pd.DataFrame(rows),'portfolio_candidates.csv')
    pure={ticker:np.eye(len(TICKERS))[TICKERS.index(ticker)] for ticker in CFG['etfs']}
    # The simple policy choice is explicitly confined to two predeclared ETF mandates.
    CE={k:float(w@mu-.5*CFG['risk_aversion']*w@cov@w) for k,w in pure.items()}
    rec=max(CE,key=CE.get);alt=next(x for x in CFG['etfs'] if x!=rec)
    w=pure[rec];v=pure[alt]
    aversion_threshold=2*((v-w)@mu)/(v@cov@v-w@cov@w)
    beta_diff=float((v-w)@beta)
    erp_threshold=(CFG['risk_aversion']*.5*(v@cov@v-w@cov@w))/beta_diff
    preference=[]
    for A in [0,1,2,4,6,8,10]:
        for k,ww in pure.items():
            preference.append(dict(strategy=k,risk_aversion=A,expected_return=ww@mu,annual_variance=ww@cov@ww,
                                   certainty_equivalent=ww@mu-.5*A*ww@cov@ww))
    save(pd.DataFrame(preference),'risk_preference.csv')
    # Annual rule is used consistently for diagnostic historical portfolio histories.
    histories={k:backtest(r,ww,cost=CFG['equity_cost_per_dollar_traded'])['return_net'].set_axis(r.index) for k,ww in {**weights,**pure}.items()}
    stats=[]
    for k,series in histories.items():stats.append(dict(strategy=k,**performance(series,f.RF)))
    save(pd.DataFrame(stats),'training_performance.csv')
    factor_rows=[]
    for name,y in [(rec,histories[rec]),('VTI',r.VTI),('AAPL',r.AAPL),('MSFT',r.MSFT),('JPM',r.JPM)]:
        for model,cols in [('CAPM',['Mkt-RF']),('FF3',['Mkt-RF','SMB','HML'])]:
            d,res=regress(y,f,cols);factor_rows.append(dict(security=name,model=model,**d))
    save(pd.DataFrame(factor_rows).drop_duplicates(['security','model']),'factor_regressions.csv')
    # Subperiod alpha persistence test fixed in advance, without selecting winners.
    alpha=[]
    for a,b in [('2015-01','2018-12'),('2019-01','2022-12')]:
        for ticker in [rec,'AAPL','MSFT']:
            dd,_=regress(r.loc[a:b,ticker],f.loc[a:b],['Mkt-RF','SMB','HML'])
            alpha.append(dict(security=ticker,start=a,end=b,**dd))
    save(pd.DataFrame(alpha),'alpha_stability.csv')
    # Window and expected-return sensitivity, with exactly the same eligible universe.
    sensitivity=[]
    for start in ['2015-01','2018-01']:
        rr=r.loc[start:];ff=f.loc[start:];cc=rr.cov().values*12
        bb=np.array([np.cov(rr[x]-ff.RF,ff['Mkt-RF'],ddof=1)[0,1]/ff['Mkt-RF'].var(ddof=1) for x in TICKERS])
        for erp in [.025,.045,.065]:
            mm=CFG['forecast_rf']+bb*erp
            scores={k:float(ww@mm-2*ww@cc@ww) for k,ww in pure.items()}
            sensitivity.append(dict(start=start,months=len(rr),ERP=erp,preferred=max(scores,key=scores.get),**scores))
    save(pd.DataFrame(sensitivity),'window_and_erp_sensitivity.csv')
    forecast=dict(recommended_ticker=rec,rejected_ticker=alt,forecast_return=float(w@mu),vol=float(np.sqrt(w@cov@w)),
        recommended_CE=CE[rec],alternative_CE=CE[alt],risk_aversion_threshold=float(aversion_threshold),erp_reversal_threshold=float(erp_threshold),
        sample_vs_index_weight_turnover=float(.5*np.abs(weights['Sample_A4']-weights['Single_index_A4']).sum()),
        ETF_residual_correlation=float(residual[['VTI','USMV']].corr().iloc[0,1]),
        recommended_beta=float(w@beta),benchmark_beta=float(pure['VTI']@beta),
        nominal_goal=funding['nominal_goal'])
    policy=dict(case_date=CFG['case_date'],weights=dict(zip(TICKERS,map(float,w))),benchmark={'VTI':1.},
       alternatives={k:dict(zip(TICKERS,map(float,weights[k]))) for k in ['Sample_A4','Single_index_A4','Eta_historical_Sharpe']},
       simple_rejected=alt,rule=CFG['growth_rebalance_rule'],cost=CFG['equity_cost_per_dollar_traded'],
       forecast_assumptions=CFG,funding=funding,forecast=forecast,
       raw_training_hashes={p.name:digest(p) for p in sorted((ROOT/'data/raw/train').glob('*')) if p.suffix in ['.csv','.zip']})
    if freeze:
        if (POL/'frozen_policy.json').exists():raise RuntimeError('Refusing to overwrite the frozen policy')
        policy['frozen_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        policy['limitation']='Retrospective case. Current revised data and discretionary surviving universe do not create a genuinely unseen experiment.'
        (POL/'frozen_policy.json').write_text(json.dumps(policy,indent=2))
        (POL/'frozen_policy.sha256').write_text(digest(POL/'frozen_policy.json')+'  frozen_policy.json\n')
    elif (POL/'frozen_policy.json').exists():
        original=json.loads((POL/'frozen_policy.json').read_text())
        assert original['weights']==policy['weights'],'Offline reproduction changed the frozen weights'
        assert original['raw_training_hashes']==policy['raw_training_hashes'],'Training raw files changed'
        assert original['forecast_assumptions']==CFG,'Configuration changed after freeze; create a separately labelled mandate scenario'
    (TABLE/'decision_summary.json').write_text(json.dumps(forecast,indent=2))
    simulate(r,mu,cov,pure,funding,rec)
    # Executable amounts use the unadjusted last price; adjusted prices are never purchase prices.
    end=pd.read_csv(PROC/'train_month_end_close_prices.csv',index_col=0).loc['2022-12']
    allocation=[dict(instrument='Beta',market_value=funding['beta_cost'],units=funding['beta_face']/1000,unit_description='bonds of USD 1000 face'),
                dict(instrument='Delta',market_value=funding['delta_cost'],units=funding['delta_face']/1000,unit_description='bonds of USD 1000 face'),
                dict(instrument=rec,market_value=funding['equity_investment'],units=funding['equity_investment']/float(end[rec]),unit_description='shares at 2022-12-30 close proxy'),
                dict(instrument='Trading costs',market_value=funding['total_fees'],units=np.nan,unit_description='assumed execution expense')]
    save(pd.DataFrame(allocation),'initial_allocation.csv')
    charts_training(funding,forecast)
    return r,f,forecast

def simulate(r,mu,cov,pure,funding,rec):
    # Joint moving circular block bootstrap. Historical log shocks are centered,
    # then shifted to the stated prospective arithmetic-return approximation.
    npaths=20000;n=96;block=12;rng=np.random.default_rng(CFG['seed'])
    starts=rng.integers(0,len(r),size=(npaths,n//block))
    indices=(starts[:,:,None]+np.arange(block))%len(r);indices=indices.reshape(npaths,n)
    rows=[];scenario=[];terminal={}
    for name,w in pure.items():
        log=np.log1p(r.values@w);var=float(w@cov@w);m=float(w@mu)
        drift=(np.log1p(m)-.5*var)/12
        samples=log[indices]-log.mean()+drift
        wealth=funding['equity_investment']*np.exp(samples.cumsum(axis=1))
        total=wealth[:,-1]+funding['terminal_cash'];real=total/(1+CFG['inflation'])**8
        terminal[name]=real
        success=np.mean(real>=CFG['real_goal'])
        rows.append(dict(strategy=name,paths=npaths,block_months=block,expected_arithmetic_return=m,
           assumed_log_growth_annual=drift*12,volatility=np.sqrt(var),real_p05=np.quantile(real,.05),real_median=np.median(real),real_p95=np.quantile(real,.95),
           probability_goal=float(success),monte_carlo_standard_error=float(np.sqrt(success*(1-success)/npaths)),
           mean_real_shortfall=float(np.maximum(CFG['real_goal']-real,0).mean())))
        for pi in [.02,.025,.04]:
            for erp in [.025,.045,.065]:
                beta=(m-CFG['forecast_rf'])/CFG['forecast_erp'];newmu=CFG['forecast_rf']+beta*erp
                delta=np.log1p(newmu)-np.log1p(m)
                fv=wealth[:,-1]*np.exp(delta*8)+funding['terminal_cash'];rv=fv/(1+pi)**8
                scenario.append(dict(strategy=name,inflation=pi,ERP=erp,probability_goal=np.mean(rv>=CFG['real_goal']),real_median=np.median(rv)))
    save(pd.DataFrame(rows),'mission_simulation.csv');save(pd.DataFrame(scenario),'mission_scenarios.csv')
    # Purely deterministic return scenarios are distinct from probability estimates.
    det=[]
    for name,w in pure.items():
        for g in [0,.02,.04,.06,.08]:
            for pi in [.025,.04]:
                value=funding['equity_investment']*(1+g)**8+funding['terminal_cash']
                det.append(dict(strategy=name,equity_cagr=g,inflation=pi,nominal_2030=value,real_2030=value/(1+pi)**8))
    save(pd.DataFrame(det),'deterministic_terminal_scenarios.csv')
    fig,ax=plt.subplots(figsize=(8.5,3.6))
    for name,values in terminal.items():
        xs=np.sort(values)/1e6;ax.plot(xs,np.arange(1,len(xs)+1)/len(xs),label=name,lw=2)
    ax.axvline(8,color='#a34b36',ls='--',label='USD 8m real goal');ax.set(xlim=(2,22),xlabel='2030 assets in USD millions of December 2022 purchasing power',ylabel='Cumulative probability')
    ax.legend(frameon=False);fig.tight_layout();fig.savefig(FIG/'mission_distribution.png');plt.close(fig)

def evaluate():
    path=POL/'frozen_policy.json';frozen=json.loads(path.read_text());before=digest(path)
    r,p=load_prices('eval');f=load_factors('eval',r.index)
    assert len(r)==36 and r.index.min()==pd.Period('2023-01')
    weights={'Recommended':np.array([frozen['weights'][x] for x in TICKERS]),'Benchmark VTI':np.eye(len(TICKERS))[TICKERS.index('VTI')]}
    for k,ww in frozen['alternatives'].items():weights[k]=np.array([ww[x] for x in TICKERS])
    data={};stats=[];annual=[];turn=[]
    for k,w in weights.items():
        bt=backtest(r,w,cost=frozen['cost'],initial_cost=True)
        save(bt.reset_index(),f'evaluation_{k.replace(" ","_")}_path.csv')
        data[k]=bt['wealth'].values
        stat=performance(bt.return_net,f.RF);stats.append(dict(strategy=k,**stat))
        rr=bt.return_net.set_axis(r.index)
        for year in [2023,2024,2025]:annual.append(dict(strategy=k,year=year,total_return=float(np.prod(1+rr[rr.index.year==year])-1)))
        turn.append(dict(strategy=k,total_one_way_traded_fraction=float(bt.turnover.sum()),rebalance_cost_per_initial_dollar=float(bt.cost.sum())))
    save(pd.DataFrame(stats),'evaluation_performance.csv');save(pd.DataFrame(annual),'evaluation_calendar_years.csv');save(pd.DataFrame(turn),'evaluation_costs.csv')
    wealth=pd.DataFrame(data,index=r.index);wealth.index.name='month';save(wealth,'evaluation_wealth.csv',True)
    diff=wealth['Recommended'].iloc[-1]-wealth['Benchmark VTI'].iloc[-1]
    result=dict(policy_hash_before=before,policy_hash_after=digest(path),recommended_minus_benchmark_terminal_per_dollar=float(diff),
                evaluation_does_not_test_2030_goal=True)
    (TABLE/'evaluation_summary.json').write_text(json.dumps(result,indent=2))
    # Record vendor vintage overlap rather than force identical price levels.
    train_prices=pd.read_csv(PROC/'train_month_end_adjusted_prices.csv',index_col=0)
    eval_prices=pd.read_csv(PROC/'eval_month_end_adjusted_prices.csv',index_col=0)
    overlap=pd.DataFrame({'train_download_2022_12':train_prices.loc['2022-12'],'eval_download_2022_12':eval_prices.loc['2022-12']})
    overlap['difference']=overlap.iloc[:,1]-overlap.iloc[:,0];save(overlap,'download_overlap_comparison.csv',True)
    trainf=load_factors('train',pd.period_range('2015-01','2022-12',freq='M'))
    evalf=load_factors('eval',trainf.index)
    save((evalf-trainf).rename_axis('month'),'factor_vintage_overlap_differences.csv',True)
    load_factors('eval',r.index) # Restore the evaluation processed file after the vintage audit.
    fig,ax=plt.subplots(figsize=(8.5,3.7))
    dates=pd.date_range('2022-12-31',periods=37,freq='ME')
    for k in ['Recommended','Benchmark VTI','Eta_historical_Sharpe']:
        ax.plot(dates,np.r_[1,wealth[k]],label=k.replace('_',' '),lw=2)
    ax.set(ylabel='Growth of USD 1 (net costs)',xlabel='Evaluation period',xlim=(dates[0],dates[-1]));ax.legend(frameon=False);fig.tight_layout();fig.savefig(FIG/'evaluation_growth.png');plt.close(fig)
    assert before==digest(path),'Evaluation changed the frozen decision'
    return result

def charts_training(funding,decision):
    fig,ax=plt.subplots(figsize=(8.5,3.2))
    names=['2024 scholarship','2027 learning centre','Growth allocation','Trading costs']
    vals=[funding['beta_cost'],funding['delta_cost'],funding['equity_investment'],funding['total_fees']]
    ax.barh(names,np.array(vals)/1e6,color=['#38566d','#69899c','#157c80','#b4bbc3'])
    ax.invert_yaxis();ax.set_xlabel('Initial USD millions');fig.tight_layout();fig.savefig(FIG/'initial_allocation.png');plt.close(fig)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['train','all'],default='all');ap.add_argument('--freeze',action='store_true');args=ap.parse_args()
    funding=build_bonds(CFG,TABLE)
    r,f,decision=train(funding,args.freeze)
    result={'training_months':len(r),'tickers':len(TICKERS),'funding':funding,'decision':decision}
    if args.stage=='all':result['evaluation']=evaluate()
    (ROOT/'logs/analysis_run.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
