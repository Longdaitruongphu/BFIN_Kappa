from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
funding=json.loads((ROOT/'outputs/tables/funding_summary.json').read_text(encoding='utf-8'))
policy=json.loads((ROOT/'policy/frozen_policy.json').read_text(encoding='utf-8'))
initial=float(policy['forecast_assumptions']['initial_wealth'])
growth=float(funding['equity_investment'])
rows=[]
for period,file in [('training_2015_2022','train_monthly_returns.csv'),('evaluation_2023_2025','eval_monthly_returns.csv')]:
    data=pd.read_csv(ROOT/'data/processed'/file,index_col=0,parse_dates=True)
    for ticker in ['USMV','VTI']:
        wealth=(1+data[ticker]).cumprod()
        peak=wealth.cummax().clip(lower=1.0)
        dd=wealth/peak-1.0
        max_i=dd.idxmin()
        for threshold in [0.10,0.15,0.20]:
            crossed=(dd <= -threshold) & (dd.shift(1).fillna(0.0) > -threshold)
            dates=[d.strftime('%Y-%m') for d in dd.index[crossed]]
            rows.append({
                'period':period,'ticker':ticker,'trigger_drawdown_pct':100*threshold,
                'max_month_end_drawdown_pct':100*dd.min(),'max_drawdown_month':max_i.strftime('%Y-%m'),
                'number_of_month_end_crossings':len(dates),'crossing_months':';'.join(dates),
                'dollar_loss_at_trigger_on_initial_growth_sleeve':growth*threshold,
                'dollar_loss_at_trigger_on_initial_total_fund':initial*threshold,
                'measurement':'Monthly total-return wealth index; peak-to-trough, with initial wealth=1; no external flows in ETF series'
            })
out=ROOT/'outputs/tables/stoploss_threshold_history.csv'
pd.DataFrame(rows).to_csv(out,index=False,float_format='%.6f')
print(out)
print(pd.DataFrame(rows).to_string(index=False))
