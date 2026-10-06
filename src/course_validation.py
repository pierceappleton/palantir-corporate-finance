import json
from pathlib import Path
from src.dcf import dcf,Bridge

def run():
 starting=100;rates=[.08,.06,.05,.04,.03];fcffs=[]
 for rate in rates:starting*=1+rate;fcffs.append(starting)
 v=dcf(fcffs,[1,2,3,4,5],.10,.03,fcffs[-1]*1.03,Bridge(50,0,300,0,50))
 actual={**{f'FCFF Year {i+1}':f for i,f in enumerate(fcffs)},'PV explicit':v['explicit_pv'],'Terminal value':fcffs[-1]*1.03/(.10-.03),'PV terminal':v['terminal_pv'],'EV':v['enterprise_value'],'Equity':v['equity_value'],'Per share':v['per_share'],'Terminal share':v['terminal_share']}
 expected=dict(zip(actual,[108,114.48,120.204,125.0122,128.7625,448.4408,1894.6486,1176.4277,1624.8685,1374.8685,27.4974,.7240]))
 rows=[]
 for label,val in actual.items():
  diff=val-expected[label];passed=abs(diff)<.0001
  rows.append(dict(label=label,published=expected[label],calculated=val,difference=diff,tolerance=.0001,passed=passed))
 if not all(x['passed'] for x in rows):raise ValueError('Published training case mismatch')
 source='https://github.com/CinderZhang/FIN43900-Fall2026/blob/69eac1e8cbd63b35e801d48d990c4b594bfdbbc8/lessons/week-03/lab-05-dcf-build.md'
 packet=dict(source=source,local_source='data/reference/official-course/lessons/week-03/lab-05-dcf-build.md',status='PASS: all twelve published outputs; not an AI-invented synthetic answer',checks=rows)
 Path('validation/published-training-reconciliation.json').write_text(json.dumps(packet,indent=2));print(packet['status']);return packet
if __name__=='__main__':run()