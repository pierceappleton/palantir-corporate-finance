import unittest
from src.model import load
from src.workbench import calculate
from src.course_validation import run
class CourseWorkbenchTests(unittest.TestCase):
 def test_published_training_case(self):self.assertTrue(all(x['passed'] for x in run()['checks']))
 def test_live_growth_and_reset(self):
  d,c=load();_,base=calculate(d,c);_,higher=calculate(d,c,growth_shift=.10);_,reset=calculate(d,c)
  self.assertGreater(higher['per_share'],base['per_share']);self.assertEqual(reset['per_share'],base['per_share'])
 def test_bounded_inputs_and_terminal_failure(self):
  d,c=load()
  with self.assertRaises(ValueError):calculate(d,c,growth_shift=.16)
  with self.assertRaises(ValueError):calculate(d,c,terminal_roic=.02)
if __name__=='__main__':unittest.main()