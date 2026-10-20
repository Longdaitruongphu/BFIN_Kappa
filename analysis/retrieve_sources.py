"""Save authoritative supporting documents and a reproducible source manifest."""
from pathlib import Path
import sys,json,datetime,hashlib,time
ROOT=Path(__file__).resolve().parents[1]
if (ROOT.parent/'.analysis_packages').exists():sys.path.insert(0,str(ROOT.parent/'.analysis_packages'))
import requests
SOURCES=[
('AAPL','2022-10-28','Information Technology','Devices and services','https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/aapl-20220924.htm'),
('MSFT','2022-07-28','Information Technology','Enterprise software and cloud','https://www.sec.gov/Archives/edgar/data/789019/000156459022026876/msft-10k_20220630.htm'),
('JPM','2022-02-22','Financials','Banking and credit cycle','https://www.sec.gov/Archives/edgar/data/19617/000001961722000272/jpm-20211231.htm'),
('JNJ','2022-02-17','Health Care','Defensive health care demand','https://www.sec.gov/Archives/edgar/data/200406/000020040622000022/jnj-20220102.htm'),
('PG','2022-08-05','Consumer Staples','Consumer staples pricing power','https://www.sec.gov/Archives/edgar/data/80424/000008042422000064/pg-20220630.htm'),
('XOM','2022-02-23','Energy','Oil price and inflation exposure','https://www.sec.gov/Archives/edgar/data/34088/000003408822000011/xom-20211231.htm'),
('CAT','2022-02-16','Industrials','Capital spending cycle','https://www.sec.gov/Archives/edgar/data/18230/000001823022000050/cat-20211231.htm'),
('NEE','2022-02-18','Utilities','Regulated utility and rate sensitivity','https://www.sec.gov/Archives/edgar/data/753308/000075330822000014/nee-20211231.htm'),
('VTI','2020-04-28','US equity ETF','Broad US market comparator','https://www.sec.gov/Archives/edgar/data/36405/000168386320005993/f4654d1.htm'),
('USMV','2022-07-28','US equity ETF','Minimum volatility mandate; contemporary SEC-filed third-party description','https://www.sec.gov/Archives/edgar/data/886982/000156459022026948/gs-424b2.htm'),
('FOMC_SEP','2022-12-14','Assumptions','Contemporaneous inflation and interest-rate outlook','https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20221214.htm'),
('French_library','Current documentation','Data methodology','Revised historical data and FIZ to CIZ change; not a forecast input','https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html'),
('French_definition','Current documentation','Data methodology','Market, SMB, HML and RF definitions','https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html'),
('yfinance_documentation','Current documentation','Data methodology','Explicit retrieval settings','https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html')]

def main():
    dest=ROOT/'data/raw/supporting';dest.mkdir(parents=True,exist_ok=True)
    records=[]
    for ident,date,sector,role,url in SOURCES:
        path=dest/(ident+'.html')
        rec=dict(identifier=ident,document_date=date,sector=sector,role=role,url=url,
                 retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),filename=str(path.relative_to(ROOT)))
        try:
            if path.exists(): rec['status']='reused'
            else:
                r=requests.get(url,headers={'User-Agent':'BFIN academic case research Python requests'},timeout=60)
                r.raise_for_status();path.write_bytes(r.content);rec['status']='downloaded'
            rec['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
            print(ident,rec['status'],path.stat().st_size,flush=True)
        except Exception as exc:
            rec['status']='failed';rec['error']=repr(exc);print(ident,repr(exc),flush=True)
        records.append(rec);time.sleep(.25)
    (dest/'source_register.json').write_text(json.dumps(records,indent=2))

if __name__=='__main__':main()
