"""Network-disabled rebuild from saved raw data. Run from any directory."""
from pathlib import Path
import sys,runpy,socket,hashlib,json,datetime
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
if (ROOT.parent/'.analysis_packages').exists():sys.path.insert(0,str(ROOT.parent/'.analysis_packages'))
def denied(*args,**kwargs):raise RuntimeError('Network disabled during the offline rebuild')
socket.socket.connect=denied
socket.create_connection=denied
before=hashlib.sha256((ROOT/'policy/frozen_policy.json').read_bytes()).hexdigest()
for script,args in [('analyze.py',['--stage','all']),('supplement.py',[]),('build_reports.py',[]),('build_guide.py',[])]:
    print('Running',script,flush=True)
    sys.argv=[script]+args
    runpy.run_path(str(ROOT/'analysis'/script),run_name='__main__')
after=hashlib.sha256((ROOT/'policy/frozen_policy.json').read_bytes()).hexdigest()
assert before==after
record=dict(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),network_connections_disabled=True,
            policy_sha256_before=before,policy_sha256_after=after,status='passed')
(ROOT/'logs/offline_rebuild_receipt.json').write_text(json.dumps(record,indent=2))
print('Offline rebuild complete. Frozen policy preserved.')
