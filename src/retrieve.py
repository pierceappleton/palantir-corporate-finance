import json, urllib.request, hashlib
from pathlib import Path
from datetime import datetime, timezone
root=Path('.')
manifest=[]
urls={
 'pltr_2025_10k.html':'https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm',
 'pltr_2026q2_release.html':'https://www.sec.gov/Archives/edgar/data/1321655/000132165526000039/a2026q2ex991pressrelease.htm',
 'pltr_submissions.json':'https://data.sec.gov/submissions/CIK0001321655.json',
 'pltr_companyfacts.json':'https://data.sec.gov/api/xbrl/companyfacts/CIK0001321655.json'
}
for filename,url in urls.items():
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Pierce Appleton academic finance research contact via github.com/pierceappleton','Accept-Encoding':'identity'})
  content=urllib.request.urlopen(req,timeout=45).read()
  (root/'data/raw'/filename).write_bytes(content)
  manifest.append(dict(file=filename,url=url,retrieved_utc=datetime.now(timezone.utc).isoformat(),sha256=hashlib.sha256(content).hexdigest(),bytes=len(content)))
  print(filename,len(content))
 except Exception as e:
  print(filename,type(e).__name__,str(e)); manifest.append(dict(file=filename,url=url,error=str(e)))
(root/'docs/source_manifest.json').write_text(json.dumps(manifest,indent=2))