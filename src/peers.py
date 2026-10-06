import json
from pathlib import Path
from src.model import dump_csv,load

def multiples(p):
 rev=p['annual_revenue']+p['current_h1_revenue']-p['prior_h1_revenue']
 ni=p['annual_ni']+p['current_h1_ni']-p['prior_h1_ni']
 cap=p['price']*p['shares'];ev=cap+p['debt']+p.get('nci',0)-p['cash']-p['investments']
 if rev<=0:raise ValueError('Revenue denominator invalid')
 return dict(ticker=p['ticker'],price=p['price'],price_asof='2026-10-05',shares=p['shares'],shares_asof=p['shares_asof'],ttm_end=p['ttm_end'],ttm_revenue=rev,ttm_gaap_common_income=ni,market_cap=cap,ev=ev,ev_revenue=ev/rev,pe=cap/ni if ni>0 else None,private_portfolio_excluded_from_ev_bridge=p['private_portfolio'],qualification='Book/face debt approximation; operating leases excluded with lease expense retained; strategic equity holdings receive zero separate credit, contaminate GAAP earnings. Latest balance/share dates differ from price date.')

def run():
 peers=json.loads(Path('data/processed/peer_inputs.json').read_text())
 rows=[multiples(p) for p in peers]
 data,c=load();h=data['interim_2026h1'];b=data['annual_2025'];prior=data['prior_2025h1']
 pltr=dict(ticker='PLTR',price=c['price'],shares=h['basic_shares'],shares_asof='2026-06-30',ttm_end='2026-06-30',cash=h['cash'],investments=h['investments'],debt=0,nci=h['nci'],private_portfolio=167,annual_revenue=b['revenue'],current_h1_revenue=h['revenue'],prior_h1_revenue=prior['revenue'],annual_ni=b['common_net_income'],current_h1_ni=h['common_net_income'],prior_h1_ni=prior['common_net_income'])
 rows.append(multiples(pltr));dump_csv('outputs/peer_multiples.csv',rows)
 relative=[]
 for row in rows[:-1]:
  equity_ev=row['ev_revenue']*rows[-1]['ttm_revenue']+h['cash']+h['investments']-h['nci']
  equity_pe=row['pe']*rows[-1]['ttm_gaap_common_income']
  relative.append(dict(peer=row['ticker'],ev_revenue_implied_basic_price=equity_ev/h['basic_shares'],pe_implied_basic_price=equity_pe/h['basic_shares']))
 dump_csv('outputs/relative_valuation.csv',relative)
 print(json.dumps(rows,indent=2))
 return rows
if __name__=='__main__':run()
