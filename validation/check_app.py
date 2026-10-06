from streamlit.testing.v1 import AppTest
from pathlib import Path
at=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app/main.py')).run(timeout=30)
assert not at.exception,at.exception
assert len(at.metric)==3
print('Streamlit application executes without exceptions; three case metrics rendered')
for case in ['low','high']:
 at.selectbox[0].select(case).run(timeout=30)
 assert not at.exception,at.exception
print('All case selections passed')