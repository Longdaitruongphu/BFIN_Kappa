"""Read-only analysis of frozen inputs; write advisory outputs only. Python 3.12 stdlib."""
from pathlib import Path
import csv
import hashlib
import json
import math
import statistics as st

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPECTED_HASH = '21b4ec3fb864144e7b56e54c668ebaed9c96d5a1771564b50c892700978c9f5c'

def read(rel):
    with (ROOT / rel).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def write(name, rows):
    with (HERE / name).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

policy_path = ROOT / 'policy/frozen_policy.json'
before = hashlib.sha256(policy_path.read_bytes()).hexdigest()
assert before == EXPECTED_HASH
policy = json.loads(policy_path.read_text(encoding='utf-8-sig'))
factors = {r['month']: r for r in read('data/processed/eval_factors.csv')}
paths = {}
rows = []
for ticker, filename in [('USMV', 'Recommended'), ('VTI', 'Benchmark_VTI')]:
    path = read(f'outputs/tables/evaluation_{filename}_path.csv')
    dates = [r['month'] for r in path]
    assert dates == sorted(factors) and len(dates) == 36
    r = [float(x['return_net']) for x in path]
    rf = [float(factors[d]['RF']) for d in dates]
    excess = [a-b for a, b in zip(r, rf)]
    paths[ticker] = r
    rows.append(dict(ticker=ticker, months=len(r),
        arithmetic_return_annual=12*st.mean(r), rf_arithmetic_annual=12*st.mean(rf),
        excess_return_arithmetic_annual=12*st.mean(excess),
        total_return_vol_annual=math.sqrt(12)*st.stdev(r),
        excess_return_vol_annual=math.sqrt(12)*st.stdev(excess),
        sharpe=math.sqrt(12)*st.mean(excess)/st.stdev(excess),
        cumulative_return=math.prod(1+x for x in r)-1,
        cagr=math.prod(1+x for x in r)**(1/3)-1))
write('sharpe_decomposition.csv', rows)
saved = {r['strategy']:r for r in read('outputs/tables/evaluation_performance.csv')}
for r, label in zip(rows, ['Recommended', 'Benchmark VTI']):
    assert abs(r['sharpe']-float(saved[label]['annual_sharpe'])) < 1e-9
    assert abs(r['cumulative_return']-float(saved[label]['total_return'])) < 1e-9

regime = []
for label, predicate in [('VTI positive month', lambda x:x>0), ('VTI negative month', lambda x:x<0)]:
    ids = [i for i, r in enumerate(paths['VTI']) if predicate(r)]
    u = st.mean(paths['USMV'][i] for i in ids)
    v = st.mean(paths['VTI'][i] for i in ids)
    regime.append(dict(regime=label, months=len(ids), USMV_mean_monthly=u,
        VTI_mean_monthly=v, arithmetic_conditional_capture=u/v,
        definition='Ratio of mean returns in VTI-positive or VTI-negative months; not compounded capture'))
write('conditional_returns.csv', regime)

coeff = {(r['security'],r['model']):r for r in read('outputs/tables/factor_regressions.csv')}
observed_gap = 12*st.mean(u-v for u,v in zip(paths['USMV'],paths['VTI']))
bridge = []
for factor in ['Mkt-RF','SMB','HML']:
    diff = float(coeff['USMV','FF3'][factor])-float(coeff['VTI','FF3'][factor])
    realized = 12*st.mean(float(factors[d][factor]) for d in dates)
    bridge.append(dict(component=factor, contribution_annual_arithmetic=diff*realized,
        meaning='Frozen training FF3 loading difference times evaluation factor mean; descriptive accounting'))
alpha_diff = float(coeff['USMV','FF3']['alpha_annual'])-float(coeff['VTI','FF3']['alpha_annual'])
bridge.append(dict(component='Training intercept difference', contribution_annual_arithmetic=alpha_diff,
    meaning='Fitted training intercept, not forecast alpha; forecast alpha remains zero'))
remainder = observed_gap-sum(r['contribution_annual_arithmetic'] for r in bridge)
bridge.append(dict(component='Out-of-sample remainder including entry cost', contribution_annual_arithmetic=remainder,
    meaning='Realized deviations from frozen training model, not causal or security-level attribution'))
assert abs(sum(r['contribution_annual_arithmetic'] for r in bridge)-observed_gap)<1e-12
write('frozen_factor_gap_bridge.csv', bridge)

funding = policy['funding']
e = funding['equity_investment']
c = funding['terminal_cash']
t = funding['nominal_goal']
fee = policy['cost']
reserves = []
for reserve in [0, 120000, 250000, 500000, 1000000]:
    growth = (e*(1+fee)-reserve)/(1+fee)
    for treatment in ['retained_to_2030_zero_interest','fully_spent_by_2030']:
        terminal_reserve = reserve if treatment.startswith('retained') else 0
        required = ((t-c-terminal_reserve)/growth)**(1/8)-1
        reserves.append(dict(initial_cash_reserve=reserve,treatment=treatment,growth_investment=growth,
            required_growth_cagr=required,terminal_cash=c+terminal_reserve,
            note='Illustration only; bonds unchanged; 10bp equity entry cost; no reserve income; no other costs'))
write('reserve_tradeoffs.csv', reserves)
assert abs(reserves[0]['required_growth_cagr']-funding['required_equity_cagr'])<1e-12

r = funding['required_equity_cagr']
g2027 = e*(1+r)**5
share2027 = g2027/(g2027+c)
summary = dict(date_local='2026-10-16', timezone='Asia/Saigon',
    frozen_policy_sha256=before, inputs_changed=False,
    USMV_minus_VTI_arithmetic_return_annual=observed_gap,
    tracking_error_annual=st.stdev(u-v for u,v in zip(paths['USMV'],paths['VTI']))*math.sqrt(12),
    USMV_excess_return_fraction_of_VTI=rows[0]['excess_return_arithmetic_annual']/rows[1]['excess_return_arithmetic_annual'],
    USMV_excess_vol_fraction_of_VTI=rows[0]['excess_return_vol_annual']/rows[1]['excess_return_vol_annual'],
    illustration_after_2027_payment=dict(constant_growth_cagr=r,growth_dollars=g2027,
        retained_coupon_cash=c,growth_fraction=share2027,
        equity_minus_30pct_wealth_loss=0.3*share2027,
        limitation='Deterministic illustration, not a forecast, realized path, or drawdown backtest'),
    limitations=['36 evaluation months only','Monthly observations miss intramonth drawdowns',
        'Conditional capture and factor bridge are descriptive, not causal',
        'No historical sector holdings or security-level attribution supplied',
        'No live implementation or stop-loss backtest performed'])
assert hashlib.sha256(policy_path.read_bytes()).hexdigest()==before
(HERE/'diagnostic_receipt.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2))
