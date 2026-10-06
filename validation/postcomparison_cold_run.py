from pathlib import Path
from datetime import datetime,timezone
import subprocess,sys,os,json
root=Path.cwd();venv=root/'.coldvenv3';log=[]
env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
def execute(args):
 started=datetime.now(timezone.utc).isoformat();print('Running',args,flush=True)
 result=subprocess.run(args,cwd=root,env=env,text=True,capture_output=True)
 log.append(dict(started_utc=started,completed_utc=datetime.now(timezone.utc).isoformat(),command=args,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr))
 Path('validation/postcomparison-cold-run.json').write_text(json.dumps(log,indent=2),encoding='utf8')
 print('Exit',result.returncode,flush=True)
 if result.returncode:raise RuntimeError('Cold run failed; inspect saved real log')
execute([sys.executable,'-m','venv',str(venv)])
python=str(venv/'Scripts/python.exe')
execute([python,'-m','pip','install','-r','requirements.txt'])
execute([python,'-m','pip','freeze'])
execute([python,'-m','src.reproduce'])
execute([python,'validation/check_app.py'])
print('Fresh isolated environment cold run complete',flush=True)