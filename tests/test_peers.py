import unittest,json,copy
from pathlib import Path
from src.peers import multiples
class PeerTests(unittest.TestCase):
 def test_nonpositive_gaap_earnings_are_not_a_pe(self):
  p=json.loads(Path('data/processed/peer_inputs.json').read_text())[0];p=copy.deepcopy(p)
  p['annual_ni']=0;p['current_h1_ni']=0;p['prior_h1_ni']=1
  self.assertIsNone(multiples(p)['pe'])
 def test_negative_revenue_denominator_rejected(self):
  p=json.loads(Path('data/processed/peer_inputs.json').read_text())[0];p=copy.deepcopy(p)
  p['prior_h1_revenue']=p['annual_revenue']+p['current_h1_revenue']+1
  with self.assertRaises(ValueError):multiples(p)
if __name__=='__main__':unittest.main()