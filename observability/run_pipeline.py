from __future__ import annotations
import csv, hashlib, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
LOG_DIR=BASE/'observability'/'logs'; RUNS_FILE=BASE/'observability'/'pipeline_runs.csv'
LOG_DIR.mkdir(parents=True, exist_ok=True)
def utc_now(): return datetime.now(timezone.utc).isoformat()
def sha256_file(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()
def append_run(row):
    cols=['run_id','pipeline_name','start_time_utc','end_time_utc','status','stage','exit_code','error_message']
    new=not RUNS_FILE.exists()
    with RUNS_FILE.open('a', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=cols)
        if new: w.writeheader()
        w.writerow(row)
def main():
    run_id=datetime.now(timezone.utc).strftime('RUN-%Y%m%dT%H%M%SZ')
    stages=[('silver','src/validation/run_silver.py'),('gold','src/transformation/build_gold.py')]
    for stage,script in stages:
        started=time.perf_counter(); start=utc_now()
        p=subprocess.run([sys.executable,str(BASE/script)],capture_output=True,text=True)
        dur=time.perf_counter()-started
        (LOG_DIR/f'{run_id}_{stage}.log').write_text(
            f'START={start}\nDURATION_SECONDS={dur:.3f}\nRETURN_CODE={p.returncode}\n\nSTDOUT\n{p.stdout}\nSTDERR\n{p.stderr}\n',encoding='utf-8')
        append_run({'run_id':run_id,'pipeline_name':'andes_commerce_e2e','start_time_utc':start,'end_time_utc':utc_now(),'status':'SUCCESS' if p.returncode==0 else 'FAILED','stage':stage,'exit_code':p.returncode,'error_message':p.stderr.strip()[:500]})
        if p.returncode!=0: raise SystemExit(p.returncode)
    manifest=[]
    for f in sorted((BASE/'data'/'sample').glob('*.csv')):
        manifest.append({'file':f.name,'bytes':f.stat().st_size,'sha256':sha256_file(f)})
    (BASE/'observability'/'source_manifest.json').write_text(__import__('json').dumps(manifest,indent=2),encoding='utf-8')
    print(f'Pipeline completed successfully: {run_id}')
if __name__=='__main__': main()
