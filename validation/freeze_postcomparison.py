import subprocess,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
files=subprocess.check_output(['git','ls-tree','-r','--name-only',commit],text=True,encoding='utf8').splitlines();entries=[]
for name in files:
 if name.startswith(('outputs/','submission/','config/','src/','app/','tests/','docs/','validation/')):
  blob=subprocess.check_output(['git','show',f'{commit}:{name}']);entries.append(dict(path=name,sha256=hashlib.sha256(blob).hexdigest(),bytes=len(blob)))
record=dict(created_utc=datetime.now(timezone.utc).isoformat(),postcomparison_analysis_commit=commit,independent_analysis_commit='890b9738c802592abb4e70beb8efc21181fdfcea',prior_work_commit='2e861768f09411764b7859361843389718eb0490',course_commit='69eac1e8cbd63b35e801d48d990c4b594bfdbbc8',status='Working revised bundle; human and inaccessible course gates pending',tests=15,primary_source_row_checks=32,published_known_answer_outputs=12,fresh_environment_run='PASS: validation/postcomparison-cold-run.json',locked_capex_run='NOT EXECUTED; prepared AI-closed human runner',files=entries)
Path('validation/postcomparison-freeze.json').write_text(json.dumps(record,indent=2),encoding='utf8')
print('Postcomparison snapshot',commit,'files',len(entries))