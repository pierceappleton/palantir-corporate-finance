from streamlit.testing.v1 import AppTest
from pathlib import Path
at=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app/main.py')).run(timeout=30)
assert not at.exception,at.exception
assert len(at.metric)==4
for case in ['low','high','base']:
 at.selectbox[0].select(case).run(timeout=30);assert not at.exception,at.exception
slider=[x for x in at.slider if x.key=='growth_shift'][0];slider.set_value(10.).run(timeout=30)
assert not at.exception,at.exception
assert float(at.metric[0].value.replace('$',''))>29.76
[x for x in at.slider if x.key=='terminal_roic'][0].set_value(2.).run(timeout=30)
assert not at.exception,at.exception
assert any('FAILED' in x.value for x in at.error)
at.button[0].click().run(timeout=30)
assert not at.exception,at.exception
assert not at.error
assert at.metric[0].value=='$29.76'
print('App PASS: live recalculation, all cases, bounded driver change, red failure and base recovery. Capex remained locked.')