"""Transparent provisional integrated cash-replacement pro-forma, USD millions."""
import json, csv, copy
from pathlib import Path
from datetime import date,datetime,timezone
from src.dcf import dcf,Bridge

def load():
 return json.loads(Path('data/processed/historical.json').read_text(encoding='utf8')),json.loads(Path('config/assumptions.json').read_text(encoding='utf8'))

def check_history(data):
 checks=[]
 for key in ['annual_2025','interim_2026h1']:
  b=data[key]
  assets=sum(b[k] for k in ['cash','investments','ar','prepaid','ppe','rou','other_assets'])
  liabilities=sum(b[k] for k in ['ap_accrued','contract_current','lease_current','contract_noncurrent','lease_noncurrent','other_liabilities'])
  for name,residual in [('assets',assets-b['assets']),('liabilities',liabilities-b['liabilities']),('balance',b['assets']-b['liabilities']-b['equity']-b['nci']),('cash',b['cash_total_start']+b['cfo']+b['cfi']+b['cff']+b['fx']-b['cash_total'])]:
   if abs(residual)>1e-6:raise ValueError(f'{key} {name} reconciliation failed: {residual}')
   checks.append(dict(period=key,check=name,residual=residual))
 return checks

def forecast(case, data, config):
 h=data['interim_2026h1'];prev=copy.deepcopy(h); rows=[]
 commercial=config['base_2026_revenue']*h['commercial']/h['revenue']
 government=config['base_2026_revenue']-commercial
 # Other assets/ROU, investments, noncurrent leases/contract liabilities and NCI held constant.
 # Cash is calculated from cash flows, never used to fix the balance residual.
 for i,year in enumerate(range(2026,2031)):
  if i:
   commercial*=1+case['commercial_growth'][i];government*=1+case['government_growth'][i]
  revenue=commercial+government
  raw_ebit=revenue*case['margins'][i]
  # Previously issued awards receive explicit dilution. Remove prospective service
  # expense of those same awards before applying a cash-replacement convention.
  old_award_amort=(h['unrecognized_option_comp']/h['option_service_years']+h['unrecognized_sar_comp']/h['sar_service_years']+(h['unrecognized_rsu_comp']/h['rsu_service_years'] if i<h['rsu_service_years'] else 0))*(184/365 if i==0 else 1)
  ebit=raw_ebit+old_award_amort
  da=revenue*config['da_ratio'];capex=revenue*config['capex_ratio']
  period_fraction=184/365 if i==0 else 1
  # H2 normalized operations derived from full-year forecast less reported H1.
  ebit_period=ebit-h['ebit'] if i==0 else ebit
  da_period=da-h['da'] if i==0 else da
  capex_period=capex-h['capex'] if i==0 else capex
  if capex_period<0 or da_period<0:raise ValueError('Forecast full-year reinvestment below realized H1')
  tax_operating=max(ebit_period,0)*config['tax']
  interest=(prev['cash']+prev['investments'])*config['interest_yield']*period_fraction
  period_net=ebit_period+interest-max(ebit_period+interest,0)*config['tax']
  ar=revenue*config['working_capital']['ar_ratio']; prepaid=revenue*config['working_capital']['prepaid_ratio']
  ap=revenue*config['working_capital']['accrual_ratio'];contract=revenue*(config['working_capital']['contract_offset_ratio']-case['nwc_ratio'])
  old_nwc=prev['ar']+prev['prepaid']-prev['ap_accrued']-prev['contract_current']
  nwc=ar+prepaid-ap-contract; delta=nwc-old_nwc
  cfo=period_net+da_period-delta; cfi=-capex_period;cff=0.
  cash=prev['cash']+cfo+cfi+cff
  if cash<0:raise ValueError('Cash deficit: financing required; no hidden funding plug')
  ppe=prev['ppe']+capex_period-da_period
  equity=prev['equity']+period_net
  liabilities=ap+contract+h['contract_noncurrent']+h['lease_noncurrent']+h['other_liabilities']
  assets=cash+h['investments']+ar+prepaid+ppe+h['rou']+h['other_assets']
  residual=assets-liabilities-equity-h['nci']
  if abs(residual)>1e-6:raise ValueError(f'{year}: statements fail {residual}')
  fcff=ebit_period-tax_operating+da_period-capex_period-delta
  # First explicit FCFF includes only post-Oct5 portion of H2; uniform H2
  # cash timing is an approximation and is exposed for challenge.
  valued_fcff=fcff*config['remaining_days']/184 if i==0 else fcff
  cost_of_revenue=revenue*config['presentation']['cost_of_revenue_ratio']
  operating_cost=revenue-cost_of_revenue-raw_ebit
  annual_interest=interest+(h['interest_income'] if i==0 else 0)
  annual_tax=max(ebit_period+interest,0)*config['tax']+(h['tax'] if i==0 else 0)
  annual_net=period_net+(h['net_income'] if i==0 else 0)
  row=dict(cost_of_revenue=cost_of_revenue,gross_profit=revenue-cost_of_revenue,sales_marketing=operating_cost*config['presentation']['sales_share_opex'],research_development=operating_cost*config['presentation']['rd_share_opex'],general_administrative=operating_cost*config['presentation']['ga_share_opex'],annual_interest=annual_interest,annual_other_income=(h['other_income'] if i==0 else 0),annual_tax=annual_tax,annual_net_income=annual_net,year=year,commercial_revenue=commercial,government_revenue=government,revenue=revenue,
    ebit_before_old_award_adjustment=raw_ebit,existing_award_service_adjustment=old_award_amort,ebit=ebit,
    period_ebit=ebit_period,period_interest=interest,period_tax=max(ebit_period+interest,0)*config['tax'],
    period_net_income=period_net,da=da_period,capex=capex_period,delta_nwc=delta,fcff=fcff,valued_fcff=valued_fcff,
    cash=cash,investments=h['investments'],ar=ar,prepaid=prepaid,ppe=ppe,rou=h['rou'],other_assets=h['other_assets'],
    ap_accrued=ap,contract_current=contract,contract_noncurrent=h['contract_noncurrent'],lease_noncurrent=h['lease_noncurrent'],
    other_liabilities=h['other_liabilities'],assets=assets,liabilities=liabilities,equity=equity,nci=h['nci'],
    cfo=cfo,cfi=cfi,cff=cff,balance_residual=residual,cash_residual=cash-prev['cash']-cfo-cfi-cff,
    period_label='2026 H2 modeled flows; annual revenue/EBIT' if i==0 else 'full year')
  rows.append(row);prev=row
 return rows

def bridge(data,config):
 h=data['interim_2026h1']
 return Bridge(max(0,h['cash']-config['cash_reserve']),h['investments']+h['options']*h['option_strike'],0,h['nci'],
  h['basic_shares']+h['options']+h['rsus']+h['prsus']+h['sars'])

def value(rows,case,data,config):
 final=rows[-1]['revenue']; terminal_revenue=final*(1+case['growth'])
 nopat=terminal_revenue*case['terminal_margin']*(1-config['tax'])
 terminal_fcff=nopat*(1-case['growth']/config['terminal_roic'])
 if terminal_fcff<=0:raise ValueError('Terminal reinvestment incompatible with growth/ROIC')
 periods=[config['remaining_days']/365+i for i in range(5)]
 v=dcf([r['valued_fcff'] for r in rows],periods,case['wacc'],case['growth'],terminal_fcff,bridge(data,config))
 v.update(terminal_revenue=terminal_revenue,terminal_nopat=nopat,terminal_fcff=terminal_fcff,
  action='initiate_candidate' if config['price']<v['per_share']*.8 else ('do_not_initiate' if config['price']>v['per_share']*1.2 else 'watch_defer'))
 return v

def dump_csv(path,rows):
 with Path(path).open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

def run():
 data,c=load();checks=check_history(data); results={};forecasts={}
 for name,case in c['cases'].items():
  rows=forecast(case,data,c);forecasts[name]=rows;results[name]=value(rows,case,data,c);dump_csv(f'outputs/{name}_three_statements.csv',rows)
 sensitivity=[]
 for w in [.08,.09,.105,.12,.13]:
  for g in [.02,.03,.04]:
   case={**c['cases']['base'],'wacc':w,'growth':g};v=value(forecasts['base'],case,data,c);sensitivity.append(dict(wacc=w,growth=g,per_share=v['per_share'],terminal_share=v['terminal_share']))
 dump_csv('outputs/wacc_growth.csv',sensitivity)
 # Reverse DCF: multiplier on commercial annual growth increments after 2026.
 def implied(k):
  case=copy.deepcopy(c['cases']['base']);case['commercial_growth']=[x*k for x in case['commercial_growth']]
  return value(forecast(case,data,c),case,data,c)['per_share']
 lo,hi=0.,6.
 if implied(hi)<c['price']:reverse={'status':'unbracketed','max_multiplier':hi,'value':implied(hi)}
 else:
  for _ in range(80):
   mid=(lo+hi)/2
   if implied(mid)<c['price']:lo=mid
   else:hi=mid
  reverse={'commercial_growth_multiplier':(lo+hi)/2,'annual_growths':[x*(lo+hi)/2 for x in c['cases']['base']['commercial_growth'][1:]],'price_target':c['price'],'other_drivers':'base held fixed; mechanical expectation, not forecast'}
 packet=dict(created_utc=datetime.now(timezone.utc).isoformat(),valuation_date=c['valuation_date'],status='Independent provisional analysis: postcomparison version: human locked test, final partner review and submission requirements pending',cases=results,reverse_dcf=reverse,historical_checks=checks,
  caveats=['H1 balance sheet used at Oct5; no reported Q3 cash available.','2026 H2 normalized cash flows allocated uniformly after Oct5.','Current lease included within aggregated working capital; noncurrent operating lease and ROU held constant.','Existing awards assumed full vesting/exercise; SAR treated as full-share upper bound.','Future compensation modeled as cash replacement; old award service cost removed to avoid duplication.'])
 Path('outputs/results.json').write_text(json.dumps(packet,indent=2));print(json.dumps(packet,indent=2))
if __name__=='__main__':run()