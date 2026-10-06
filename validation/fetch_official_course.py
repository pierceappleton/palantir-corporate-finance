import subprocess,json,base64,hashlib
from pathlib import Path
from datetime import datetime,timezone
repo='CinderZhang/FIN43900-Fall2026';meta=json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/commits/HEAD'],text=True,encoding='utf8'));sha=meta['sha'];tree=json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/git/trees/{sha}?recursive=1'],text=True,encoding='utf8'))
files=[x for x in tree['tree'] if x['type']=='blob' and (x['path'].startswith('projects/') and x['path'].endswith(('.md','.csv','.txt')) or x['path'] in ['PROJECT-SUBMISSION-ARCHITECTURE.md','lessons/week-03/lab-05-dcf-build.md','lessons/week-03/teach-dcf-worked-example.md','lessons/week-05/lab-10-proforma-your-company.md','lessons/week-06/lab-11-proforma-what-if.md','lessons/week-06/lab-12-proforma-present.md'] or 'rubric' in x['path'].lower())]
root=Path('data/reference/official-course');manifest=[]
for f in files:
 blob=json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/git/blobs/{f["sha"]}'],text=True,encoding='utf8'));b=base64.b64decode(blob['content']);p=root/f['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);manifest.append({'path':f['path'],'blob':f['sha'],'sha256':hashlib.sha256(b).hexdigest()})
Path('docs/course-source-manifest.json').write_text(json.dumps({'repo':repo,'commit':sha,'retrieved_utc':datetime.now(timezone.utc).isoformat(),'files':manifest},indent=2));print('Official snapshot',sha,len(manifest))
