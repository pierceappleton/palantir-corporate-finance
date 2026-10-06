from pathlib import Path
import csv,json,hashlib,subprocess
from datetime import datetime,timezone
cold=json.loads(Path('validation/postcomparison-cold-run.json').read_text(encoding='utf8'));assert len(cold)==5 and all(x['returncode']==0 for x in cold)
end=cold[-1]['completed_utc']
p=Path('docs/STATUS.md');s=p.read_text(encoding='utf8').replace('Revisedfresh-environmentcoldrun inprogress; originalcoldrunpreserved.',f'Revised fresh-environment cold run passed all five commands, ending {end}; original cold run preserved.');p.write_text(s,encoding='utf8')
p=Path('validation/STATUS.md');s=p.read_text(encoding='utf8')+f'\nPostcomparison fresh-environment run: PASS; validation/postcomparison-cold-run.json; completed {end}. 15 tests,32 source checks,12 official outputs and liveworkbench change/failure/reset all pass.\n';p.write_text(s,encoding='utf8')
Path('data/reference/AGENTS.md').write_text('All files beneath data/reference are read-only reference snapshots. Do not edit, rename or delete their content. Preserve source commits/hashes. Store refreshed sources in a new dated/commit-specific directory. Original FIN439-Labs remote remains unchanged.\n',encoding='utf8')
# Remove one-time patch generators; maintained code and resulting records remain.
for name in ['validation/patch_workbench.py','validation/fix_utf8.py','validation/update_postcomparison_status.py','validation/document_comparison.py']:
 p=Path(name)
 if p.exists():p.unlink()
fields=['item','required','location_or_url','title','duration_or_as_of','timestamp_index','access_checked','frozen_or_commit_id','notes']
records=[]
for item,path,note in [('Research-Evolution.pdf','PENDING','Needs unchanged submitted EditionA PDF and adoptedEditionB'),('Repository','https://github.com/pierceappleton/palantir-corporate-finance','Private; graderaccesspending'),('Visible executed output','outputs/review.html','Materialinputs/datedcases/comparisons/sensitivities'),('Decision memo or deck','submission/Decision-Memo.pdf','Two-page draft; finalhumanstrategylabelpending'),('Validation-and-AI-Use.pdf','submission/Validation-and-AI-Use.pdf','Two-page draft; humanlockedgatepending')]:
 records.append(dict(item=item,required='yes',location_or_url=path,title=item,duration_or_as_of='October5,2026 valuation; October6,2026 preparation',timestamp_index='',access_checked='localverified; graderpending',frozen_or_commit_id='postcomparison commit pending; independent890b973 preserved',notes=note))
for i,limit in [(1,'3:00'),(2,'5:00'),(3,'5:00')]:
 records.append(dict(item=f'Video {i}',required='yes',location_or_url='PENDING actualrecordingURL',title=f'Palantir - Video{i}',duration_or_as_of='maximum '+limit,timestamp_index='PENDING actualrecordingindex',access_checked='PENDING',frozen_or_commit_id='PENDING',notes='Video3 requires liveworkbench opening' if i==3 else 'No fictionalvideo'))
 records.append(dict(item=f'Transcript Video {i}',required='yes',location_or_url=f'transcript-video-{i}.txt - PENDING',title=f'Transcript Video{i}',duration_or_as_of='',timestamp_index='',access_checked='PENDING',frozen_or_commit_id='PENDING',notes='Must correct against actualrecording; not generatedbeforehand'))
records.append(dict(item='Optional deployed output',required='no',location_or_url='Not deployed',title='',duration_or_as_of='',timestamp_index='',access_checked='',frozen_or_commit_id='',notes='Localworkbench meetsproductfloor'))
with Path('submission/project-submission-manifest.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(records)
Path('docs/HANDOFF.md').write_text(f'''# Postcomparison handoff - October6,2026
Independent snapshot890b973 and originalfreeze/memo preserved. User supplied FIN439-Labs; snapshot2e861768,29 text/codefiles preserved. Course snapshot69eac1e8,18 files preserved. Originalremote notchanged; DOCXnotinspected.

Actual actions: ghAPIinventory and commit/blobretrieval; UTF8response correction; auditedstandardlibrary Lab10 imported read-only; modelchecks reproduce34.5344; sequentialattribution ends29.7560; negativeFCFFclippingaudited. SourceNOLnote distinguishes9Bfederalloss/4.8Bstateloss from2.618BNOLtaxasset. SuppliedEthanrangechallengecredited; Lab10/12unfilledsectionsleftunfilled. SingleLab11commitdoesnotestablishseparatepre-runcommit.

Officialknown-answer check: all12outputswithin0.0001. Revisedworkbench has boundedcontrols/base-reset/redfailure. OAT/equalproportionaltests quantify output-dependent rankings.15softwaretests and32 sourcechecks pass. Newfreshenvironmentcoldrun passed fivecommands, completed{end}; all real logs preserved. Standalonelockedrunnercompiled only, notlaunched: capexdesignatedrunremainsunexecuted.

Created2page Decision-Memo.pdf and2page Validation-and-AI-Use.pdf usingbundledReportLab; renderedPopplerpages and visuallycheckedallfour. Originalindependentmemo restoredbyte-for-byte; currentreportseparate. EditionB workingdraft andofficialsubmissionmanifest includependinghumanstates. Video3run-sheetnowopenswithliveproductdemo.

Remaining: Pierce chooseswatch/defer vsdo-not-initiatelabel/materialassumptions; unchangedofficialEditionA PDFforResearch-Evolutionassembly; AI-offprediction/AI-closedlockedrun; finalpartnerreview; realvideos/correctedtranscripts/access; Brightspaceheaderdeadline andreferencedrubric404. No receipts,personalreflections,precommit chronology or recordingsfabricated. Exactnextsteps: preservepostcomparisoncommit+manifest; reviewactualhumanrecordwhenprovided; quantifyacceptedrevisionswithnewcommits; assembleandverifyfinalbundleafterexternalgates.
''',encoding='utf8')
# Check read-only reference hashes still agree with the retrieved source versions.
for filename,root in [('docs/prior-work-source-manifest.json',Path('data/reference/FIN439-Labs')),('docs/course-source-manifest.json',Path('data/reference/official-course'))]:
 m=json.loads(Path(filename).read_text(encoding='utf8'))
 for x in m['files']:assert hashlib.sha256((root/x['path']).read_bytes()).hexdigest()==x['sha256'],x['path']
print('Cold run, reference integrity and pending submission manifest verified')