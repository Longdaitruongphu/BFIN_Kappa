"""Online retrieval only. Never invoked by the offline rebuild.
Usage: python analysis/retrieve_data.py --phase train [or eval]
Yahoo responses are saved before any return construction. French ZIP bytes are intact.
"""
from pathlib import Path
import argparse, datetime as dt, hashlib, importlib.metadata as md, json, platform, sys, time, traceback

ROOT = Path(__file__).resolve().parents[1]
local_packages = ROOT.parent / '.analysis_packages'
if local_packages.exists(): sys.path.insert(0, str(local_packages))
import pandas as pd
import requests
import yfinance as yf

CFG = json.loads((ROOT/'analysis/config.json').read_text())
RAW = ROOT/'data/raw'
RAW.mkdir(parents=True, exist_ok=True)
yf.set_tz_cache_location(str(ROOT/'data/.yf_cache'))

def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def record(entry):
    entry['recorded_utc'] = now()
    with (RAW/'retrieval_manifest.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False)+'\n')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--phase', choices=['train','eval'],required=True)
    args=ap.parse_args()
    if args.phase=='eval' and not (ROOT/'policy/frozen_policy.json').exists():
        raise RuntimeError('Freeze a policy from training data before retrieving evaluation data.')
    dest=RAW/args.phase; dest.mkdir(exist_ok=True)
    start,end=('2014-12-01','2023-01-01') if args.phase=='train' else ('2022-12-01','2026-01-01')
    settings=dict(start=start,end=end,interval='1d',auto_adjust=False,back_adjust=False,actions=True,repair=False,keepna=True,rounding=False)
    versions={n:md.version(n) for n in ['yfinance','pandas','numpy','requests','curl_cffi']}
    record(dict(event='run_start',phase=args.phase,python=sys.version,platform=platform.platform(),versions=versions,settings=settings,
                note='December baseline is retained solely to calculate January returns. Estimation starts January 2015.'))
    failures=[]
    for ticker in CFG['stocks']+CFG['etfs']:
        file=dest/f'{ticker}_daily.csv'
        if file.exists():
            record(dict(event='reuse_saved',ticker=ticker,file=str(file.relative_to(ROOT)),sha256=sha(file)))
            continue
        for attempt in range(1,4):
            try:
                frame=yf.Ticker(ticker).history(**settings,raise_errors=True)
                if frame.empty or 'Adj Close' not in frame: raise ValueError('Empty response or missing adjusted close')
                frame.to_csv(file,index=True)
                frame.to_pickle(dest/f'{ticker}_daily.pkl')
                record(dict(event='success',source='Yahoo Finance via yfinance.Ticker.history',source_url=f'https://finance.yahoo.com/quote/{ticker}/history/',
                       endpoint='https://query2.finance.yahoo.com/v8/finance/chart/'+ticker,phase=args.phase,ticker=ticker,
                       settings=settings,attempt=attempt,file=str(file.relative_to(ROOT)),sha256=sha(file),rows=len(frame),
                       first=str(frame.index.min()),last=str(frame.index.max()),columns=list(frame.columns),versions=versions))
                print(ticker, len(frame), str(frame.index.min()), str(frame.index.max()), flush=True)
                break
            except Exception as exc:
                record(dict(event='failed_download',phase=args.phase,ticker=ticker,attempt=attempt,error=repr(exc),settings=settings))
                print('FAILED',ticker,attempt,repr(exc),flush=True)
                if attempt==3: failures.append(ticker)
                else: time.sleep(2*attempt)
    factorfile=dest/'F-F_Research_Data_Factors_CSV.zip'
    url='https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip'
    if not factorfile.exists():
        try:
            response=requests.get(url,timeout=60); response.raise_for_status()
            if not response.content.startswith(b'PK'): raise ValueError('Factor response is not a ZIP archive')
            factorfile.write_bytes(response.content)
            record(dict(event='success',phase=args.phase,source='Kenneth French Data Library',source_url=url,dataset='Fama/French 3 Factors monthly',
                        requested_dates='Full vendor file; analytical slice selected offline',file=str(factorfile.relative_to(ROOT)),sha256=sha(factorfile),
                        status_code=response.status_code,headers=dict(response.headers),versions=versions))
            print('French ZIP',len(response.content),'bytes',flush=True)
        except Exception as exc:
            record(dict(event='failed_download',phase=args.phase,dataset='French FF3',source_url=url,error=repr(exc)))
            failures.append('French')
    # Pin the actually installed environment, excluding unrelated bundled packages.
    (ROOT/'requirements-analysis.txt').write_text('\n'.join(f'{k}=={md.version(k)}' for k in
        ['yfinance','numpy','pandas','scipy','statsmodels','matplotlib','requests','reportlab','python-docx','pypdf'])+'\n')
    record(dict(event='run_complete',phase=args.phase,failures=failures))
    if failures: raise RuntimeError('Unresolved downloads: '+', '.join(failures))

if __name__=='__main__': main()
