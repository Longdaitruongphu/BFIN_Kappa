"""Create a recoverable archive, preserving raw files and the first prepared snapshot."""
from pathlib import Path
import csv,hashlib,json,shutil,zipfile,datetime
ROOT=Path(__file__).resolve().parents[1]
SNAP=ROOT/'initial_submission'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def make_initial():
    if (SNAP/'snapshot_manifest.json').exists():return
    for rel in ['analysis/analyze.py','analysis/bonds.py','analysis/config.json','analysis/retrieve_data.py','requirements-analysis.txt','policy/frozen_policy.json','policy/frozen_policy.sha256','deliverables/Kappa_Initial_Decision_Record.pdf','deliverables/Kappa_Initial_Decision_Record_Editable.md']:
        dest=SNAP/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dest)
    for source in (ROOT/'data/raw/train').iterdir():
        dest=SNAP/'data/raw/train'/source.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
    records=[json.loads(line) for line in (ROOT/'data/raw/retrieval_manifest.jsonl').read_text().splitlines()]
    (SNAP/'data/raw/retrieval_manifest.jsonl').write_text('\n'.join(json.dumps(r) for r in records if r.get('phase')=='train')+'\n')
    (SNAP/'README.md').write_text('''# Prepared initial decision snapshot

Prepared on 15 October 2026 for the 22 October initial submission. No claim of actual submission is made. The original policy was frozen before evaluation retrieval. Preserve the eventual actual submission separately if the group changes this prepared version.

The two-page record is in deliverables/. Working training-analysis code and saved raw training data are included. The raw French ZIP is a current complete vendor file; the parser explicitly restricts estimation to January 2015-December 2022. No evaluation equity downloads are included here.

From this folder, install requirements-analysis.txt into a Python 3.12 environment, then run `python analysis/analyze.py --stage train`. This reproduces training calculations from saved files without downloading data. Do not use --freeze: the policy is already preserved. The complete original-mandate package outside this snapshot also contains evaluation results and supporting sources.
''',encoding='utf8')
    entries={str(p.relative_to(SNAP)).replace('\\','/'):sha(p) for p in SNAP.rglob('*') if p.is_file()}
    (SNAP/'snapshot_manifest.json').write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'prepared_not_submitted','files':entries},indent=2))
def selected():
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if not p.is_file() or p.is_symlink():continue
        if any(part.startswith('.') or part in ['__pycache__','node_modules','matplotlib'] for part in rel.parts):continue
        if p.suffix in ['.pyc'] or p.name in ['PACKAGE_MANIFEST.csv','slides_build_stderr.txt']:continue
        yield p
def main():
    make_initial()
    files=list(selected())
    with (ROOT/'PACKAGE_MANIFEST.csv').open('w',newline='',encoding='utf8') as fh:
        writer=csv.writer(fh);writer.writerow(['path','bytes','sha256'])
        writer.writerows([(p.relative_to(ROOT).as_posix(),p.stat().st_size,sha(p)) for p in files])
    target=ROOT.parent/'Kappa_Original_Mandate_Package_2026-10-15.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for p in files+[ROOT/'PACKAGE_MANIFEST.csv']:z.write(p,'BFIN_Kappa/'+p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(target) as z:assert z.testzip() is None
    receipt={'archive':target.name,'bytes':target.stat().st_size,'sha256':sha(target),'files':len(files)+1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    target.with_suffix('.receipt.json').write_text(json.dumps(receipt,indent=2))
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
