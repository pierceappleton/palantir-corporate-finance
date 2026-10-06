import unittest,copy
from src.model import load,check_history,forecast,value
class ModelTests(unittest.TestCase):
 def setUp(self):self.data,self.c=load()
 def test_history_and_restricted_cash(self):
  check_history(self.data)
  broken=copy.deepcopy(self.data);broken['interim_2026h1']['cash']=broken['interim_2026h1']['cash_total']
  with self.assertRaises(ValueError):check_history(broken)
 def test_all_cases_articulate_and_share_forecast(self):
  for case in self.c['cases'].values():
   rows=forecast(case,self.data,self.c)
   self.assertEqual(len(rows),5)
   for row in rows:
    self.assertAlmostEqual(row['balance_residual'],0)
    self.assertAlmostEqual(row['cash_residual'],0)
    self.assertAlmostEqual(row['revenue']-row['cost_of_revenue']-row['sales_marketing']-row['research_development']-row['general_administrative'],row['ebit_before_old_award_adjustment'])
   v=value(rows,case,self.data,self.c)
   self.assertGreater(v['equity_value'],v['enterprise_value'])
 def test_thousand_unit_contamination_rejected(self):
  broken=copy.deepcopy(self.data);broken['annual_2025']['investments']*=1000
  with self.assertRaises(ValueError):check_history(broken)
 def test_terminal_reinvestment_rejects_impossible_growth(self):
  case=copy.deepcopy(self.c['cases']['base']);rows=forecast(case,self.data,self.c);case['growth']=.3;case['wacc']=.4
  with self.assertRaises(ValueError):value(rows,case,self.data,self.c)
 def test_recommendation_changing_downside_at_conditional_entry(self):
  c=copy.deepcopy(self.c);c['price']=20
  base=value(forecast(c['cases']['base'],self.data,c),c['cases']['base'],self.data,c)
  downside=value(forecast(c['cases']['low'],self.data,c),c['cases']['low'],self.data,c)
  self.assertEqual(base['action'],'initiate_candidate');self.assertEqual(downside['action'],'do_not_initiate')
if __name__=='__main__':unittest.main()