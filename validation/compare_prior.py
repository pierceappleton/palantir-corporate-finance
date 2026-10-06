import importlib.util,json,copy
from pathlib import Path
from src.dcf import dcf,Bridge
from src.model import load,bridge,forecast,value,dump_csv
p=Path('data/reference/FIN439-Labs/labs/lab-10/pltr_proforma.py')
spec=importlib.util.spec_from_file_location('prior_lab10_readonly',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
prior=m.build_model();m.check_model(prior);v=m.value_equity(prior)
assert abs(v['Value Per Share']-34.53)<.01
rows=list(prior.values());cashflows=[x['Valuation FCFE'] for x in rows]
b=Bridge(7177.043,0,0,100.743,2565.197);data,c=load();w=.11;g=.03;periods=[1,2,3,4,5];terminal=cashflows[-1]*(1+g);results=[]
def add(label):
 val=dcf(cashflows,periods,w,g,terminal,b)['per_share'];prev=results[-1]['per_share'] if results else val;results.append(dict(step=label,per_share=val,change_from_previous=val-prev));return val
add('Prior Lab10 rebuilt through FCFF engine: debt zero, cash interest removed')
w=c['cases']['base']['wacc'];add('Change discount rate11% to10.56%; all cash flows fixed')
b=bridge(data,c);add('Change reported liquidity/claims and share/award bridge')
periods=[c['remaining_days']/365+i for i in range(5)];cashflows[0]*=c['remaining_days']/365;add('Change yearend timing to Oct5 stub; approximate prorated first annual cash flow')
ind=forecast(c['cases']['base'],data,c);cashflows=[x['valued_fcff'] for x in ind];terminal=cashflows[-1]*(1+g);add('Replace operating forecast: segment growth, margins, tax and WC/reinvestment')
terminal=value(ind,c['cases']['base'],data,c)['terminal_fcff'];endpoint=add('Replace terminal shortcut with mature margin and growth/ROIC reinvestment')
assert abs(endpoint-value(ind,c['cases']['base'],data,c)['per_share'])<1e-8
# Retain negative cash-flow failure evidence without editing saved original code.
negative=copy.deepcopy(prior);negative[2026]['Valuation FCFE']=-100
clipped=m.value_equity(negative)['Value Per Share'];correct=(sum(negative[y]['Valuation FCFE']/1.11**i for i,y in enumerate(m.YEARS,1))+v['PV Terminal Value']+7177.043-100.743)/2565.197
packet=dict(prior_reproduced=v,steps=results,negative_cashflow_check=dict(prior_clipped_price=clipped,correct_signed_price=correct,overstatement=clipped-correct,status='Prior code clips negative explicit cash flow tozero; reject this behavior prospectively'),note='Sequential attribution is order-dependent; no claim of additive independent sensitivities. Original model/source files unchanged.')
Path('outputs/prior-work-comparison.json').write_text(json.dumps(packet,indent=2));dump_csv('outputs/prior-work-attribution.csv',results);print(json.dumps(packet,indent=2))