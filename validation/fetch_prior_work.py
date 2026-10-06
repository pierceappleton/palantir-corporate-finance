import subprocess,json,base64,hashlib
from pathlib import Path
from datetime import datetime,timezone
repo='pierceappleton/FIN439-Labs'
meta=json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/commits/main'],text=True));commit=meta['sha']
tree=json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/git/trees/{commit}?recursive=1'],text=True))
root=Path('data/reference/FIN439-Labs');root.mkdir(parents=True,exist_ok=True);manifest=[]
for entry in tree['tree']:
 if entry['type']!='blob' or not entry['path'].endswith(('.md','.py')):continue
 blob=json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/git/blobs/{entry["sha"]}'],text=True));content=base64.b64decode(blob['content']);p=root/entry['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
 manifest.append({'path':entry['path'],'blob':entry['sha'],'sha256':hashlib.sha256(content).hexdigest()})
Path('docs/prior-work-source-manifest.json').write_text(json.dumps({'repository':repo,'commit':commit,'snapshot_utc':datetime.now(timezone.utc).isoformat(),'files':manifest,'preservation':'Read-only reference snapshot; source repository unchanged. DOCX files not inspected.'},indent=2))
print('Snapshot',commit,'files',len(manifest))