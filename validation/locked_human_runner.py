"""Prepared course-required AI-closed runner. Do not execute in an AI session.
The code contains no AI calls. Human writes prediction; Git records it before computation.
"""
import sys,json,copy,hashlib,subprocess,traceback
from pathlib import Path
from datetime import datetime,timezone
import tkinter as tk
from tkinter import ttk,messagebox
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.model import load,forecast,value
app=tk.Tk();app.title('FIN439 - human prediction and AI-closed run');app.geometry('780x690')
frame=ttk.Frame(app,padding=20);frame.pack(fill='both',expand=True)
ttk.Label(frame,text='Close AI tools before writing this prediction and running the experiment.',wraplength=730,font=('Segoe UI',12,'bold')).pack(anchor='w')
ttk.Label(frame,text='Proposed input: annual capex / revenue 1.2% -> 2.0%. Revenue, operating margins, taxes, WACC and the stated terminal convention stay fixed. No expected answer is prefilled.',wraplength=730).pack(anchor='w',pady=12)
fields={}
for key,label,height in [('name','Your name',1),('direction','Your expected value-per-share direction, in your own words',2),('reasoning','Your financial reasoning, written with AI closed',5),('decision','Your expected investment-decision effect and why',3)]:
 ttk.Label(frame,text=label).pack(anchor='w');box=tk.Text(frame,height=height,width=85,wrap='word');box.pack(fill='x',pady=4);fields[key]=box
attest=tk.BooleanVar(value=False)
ttk.Checkbutton(frame,text='I wrote this prediction and am executing this run with AI tools closed.',variable=attest).pack(anchor='w',pady=10)
status=ttk.Label(frame,text='Not run. Prediction must be committed before the model is evaluated.',wraplength=730);status.pack(anchor='w',pady=5)
def execute():
 answer={k:v.get('1.0','end').strip() for k,v in fields.items()}
 if not all(answer.values()) or not attest.get():messagebox.showerror('Incomplete human record','Complete each field and the AI-closed attestation first.');return
 button.config(state='disabled')
 try:
  now=datetime.now(timezone.utc);runid=now.strftime('%Y%m%dT%H%M%S%fZ');folder=ROOT/'validation'/'locked'/runid;folder.mkdir(parents=True)
  data,config=load();old=config['capex_ratio'];new=.020
  if abs(old-.012)>1e-12:raise ValueError('Base capex changed; stop and prepare a new clearly designated experiment.')
  record=dict(human_answer=answer,human_attests_ai_closed=True,recorded_utc=now.isoformat(),input='annual capex / revenue',old_value=old,new_value=new,units='fraction of annual revenue;1.2% to2.0%',base_repository_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),config_sha256=hashlib.sha256((ROOT/'config/assumptions.json').read_bytes()).hexdigest(),runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),output_status='not executed at prediction precommit')
  pred=folder/'prediction.json';pred.write_text(json.dumps(record,indent=2),encoding='utf8')
  subprocess.run(['git','add','--',str(pred.relative_to(ROOT))],cwd=ROOT,check=True,capture_output=True)
  subprocess.run(['git','commit','-m',f'Precommit human AI-off locked prediction {runid}'],cwd=ROOT,check=True,capture_output=True)
  commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();pretime=datetime.now(timezone.utc).isoformat()
  case=config['cases']['base'];before=value(forecast(case,data,config),case,data,config)
  changed=copy.deepcopy(config);changed['capex_ratio']=new;after=value(forecast(case,data,changed),case,data,changed)
  diff=after['per_share']-before['per_share'];direction='decrease' if diff<0 else ('increase' if diff>0 else 'unchanged')
  result=dict(prediction_precommit=commit,precommit_verified_utc=pretime,executed_utc=datetime.now(timezone.utc).isoformat(),before=before,after=after,per_share_change=diff,actual_direction=direction,decision_effect=f"{before['action']} -> {after['action']}",no_change_explanation='Action threshold was not crossed at the recorded market price.' if before['action']==after['action'] else 'The changed value crossed a recorded action threshold.',expected_reconciliation='Human review required; exact expected direction/reasoning preserved verbatim, not automatically rewritten.')
  output=folder/'results.json';output.write_text(json.dumps(result,indent=2),encoding='utf8')
  subprocess.run(['git','add','--',str(output.relative_to(ROOT))],cwd=ROOT,check=True,capture_output=True);subprocess.run(['git','commit','-m',f'Record actual AI-closed locked results {runid}'],cwd=ROOT,check=True,capture_output=True)
  status.config(text=f"Saved genuine prediction at {commit[:12]} and actual results in {folder.relative_to(ROOT)}. Direction: {direction}; value change {diff:+.4f}/share. Local commits made; no remote push or AI call.")
  messagebox.showinfo('Record saved','The prediction and actual output are preserved in separate commits. Reopen the AI session afterward to review the evidence and finish the record.')
 except Exception as error:
  (ROOT/'validation'/'locked-run-error.txt').write_text(traceback.format_exc(),encoding='utf8');messagebox.showerror('Run stopped',str(error)+'\nExact error saved for AI troubleshooting later. No successful completion claimed.');button.config(state='normal')
button=ttk.Button(frame,text='Commit my prediction, then run with AI closed',command=execute);button.pack(anchor='w',pady=12)
app.mainloop()