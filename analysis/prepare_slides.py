from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
if (ROOT.parent/'.analysis_packages').exists():sys.path.insert(0,str(ROOT.parent/'.analysis_packages'))
import pandas as pd
T=ROOT/'outputs/tables'
data={name:json.loads((T/(name+'.json')).read_text()) for name in ['funding_summary','decision_summary','all_bond_summary','risk_limit_sensitivity']}
for name in ['risk_preference','evaluation_wealth','evaluation_performance','factor_regressions','portfolio_candidates','mission_simulation','mission_scenarios','bond_metrics']:
    df=pd.read_csv(T/(name+'.csv'));data[name]=json.loads(df.to_json(orient='records'))
(ROOT/'analysis/slide_data.json').write_text(json.dumps(data,indent=2))
print('Slide evidence prepared')
