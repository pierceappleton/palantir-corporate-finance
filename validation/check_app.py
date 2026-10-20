"""Headless Streamlit check: all cases render, a bounded change moves value, a red failure recovers."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app/main.py")).run(timeout=30)
assert not app.exception, app.exception
assert len(app.metric) == 4
for case in ["low", "high", "base"]:
    app.selectbox[0].select(case).run(timeout=30)
    assert not app.exception, app.exception

growth_slider = [x for x in app.slider if x.key == "growth_shift"][0]
growth_slider.set_value(10.0).run(timeout=30)
assert not app.exception, app.exception
assert float(app.metric[0].value.replace("$", "")) > 29.76

[x for x in app.slider if x.key == "terminal_roic"][0].set_value(2.0).run(timeout=30)
assert not app.exception, app.exception
assert any("FAILED" in x.value for x in app.error)

app.button[0].click().run(timeout=30)
assert not app.exception, app.exception
assert not app.error
assert app.metric[0].value == "$29.76"
print("App PASS: live recalculation, all cases, bounded driver change, red failure and base recovery. Capex remained locked.")
