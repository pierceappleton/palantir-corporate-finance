import json,sys
from pathlib import Path
import streamlit as st
import pandas as pd
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
st.set_page_config(page_title='Palantir independent finance review',layout='wide')
st.title('Palantir — independent finance review')
st.caption('Valuation date: October 5, 2026. USD; currency and shares in millions. Course and human validation gates remain pending.')
r=json.loads((root/'outputs/results.json').read_text())
st.warning(r['status'])
cols=st.columns(3)
for col,(name,v) in zip(cols,r['cases'].items()):
 col.metric(name.capitalize()+' value / diluted share',f"${v['per_share']:.0f}")
 col.caption(f"Terminal dependence {v['terminal_share']:.0%}; {v['action'].replace('_',' ')}")
st.write('Model range is a conditional estimate. Review assumption evidence and forecast maturity before accepting an investment action.')
case=st.selectbox('Inspect case',['base','low','high'])
f=pd.read_csv(root/f'outputs/{case}_three_statements.csv')
tabs=st.tabs(['Income statement','Balance sheet','Cash flow and FCFF','Sensitivity','Comparables','Reverse DCF','Validation'])
with tabs[0]:st.dataframe(f[['year','revenue','cost_of_revenue','gross_profit','sales_marketing','research_development','general_administrative','ebit_before_old_award_adjustment','existing_award_service_adjustment','ebit','annual_interest','annual_tax','annual_net_income']].set_index('year').T)
with tabs[1]:st.dataframe(f[['year','cash','investments','ar','prepaid','ppe','rou','other_assets','assets','ap_accrued','contract_current','contract_noncurrent','lease_noncurrent','other_liabilities','liabilities','equity','nci','balance_residual']].set_index('year').T)
with tabs[2]:
 st.info('2026 cash flows cover H2; valuation uses the post-October 5 fraction. Later years are full annual flows.')
 st.dataframe(f[['year','period_net_income','da','delta_nwc','cfo','capex','cfi','cff','cash','fcff','valued_fcff','cash_residual']].set_index('year').T)
with tabs[3]:
 s=pd.read_csv(root/'outputs/wacc_growth.csv');st.dataframe(s.pivot(index='wacc',columns='growth',values='per_share'))
with tabs[4]:
 st.dataframe(pd.read_csv(root/'outputs/peer_multiples.csv'));st.dataframe(pd.read_csv(root/'outputs/relative_valuation.csv'))
 st.caption('Latest reported TTM periods differ by one month; share/balance dates precede prices. P/E is affected by investment gains and tax benefits. Basic-share relative values differ from diluted DCF values.')
with tabs[5]:st.json(r['reverse_dcf'])
with tabs[6]:
 st.json(r['historical_checks']);st.markdown((root/'validation/STATUS.md').read_text())
st.subheader('Assumptions and limitations')
st.json(json.loads((root/'config/assumptions.json').read_text()))
for x in r['caveats']:st.write('• '+x)