"""Streamlit inspection interface and bounded driver workbench for the Palantir model."""
import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.model import load  # noqa: E402
from src.workbench import calculate  # noqa: E402

BASE_DRIVERS = {"growth_shift": 0.0, "margin_shift": 0.0, "wacc": 10.56, "terminal_growth": 3.0, "terminal_roic": 25.0}
INCOME_COLUMNS = [
    "year", "revenue", "cost_of_revenue", "gross_profit", "sales_marketing", "research_development",
    "general_administrative", "ebit_before_old_award_adjustment", "existing_award_service_adjustment", "ebit",
    "annual_interest", "annual_tax", "annual_net_income",
]
BALANCE_COLUMNS = [
    "year", "cash", "investments", "ar", "prepaid", "ppe", "rou", "other_assets", "assets", "ap_accrued",
    "contract_current", "contract_noncurrent", "lease_noncurrent", "other_liabilities", "liabilities", "equity",
    "nci", "balance_residual",
]
CASH_COLUMNS = ["year", "period_net_income", "da", "delta_nwc", "cfo", "capex", "cfi", "cff", "cash", "fcff", "valued_fcff", "cash_residual"]


def reset_drivers():
    """Restore every slider to the base case."""
    for key, base_value in BASE_DRIVERS.items():
        st.session_state[key] = base_value


st.set_page_config(page_title="Palantir independent finance review", layout="wide")
st.title("Palantir - finance review and driver workbench")
st.caption("Valuation date: October 5, 2026. USD; currency and shares in millions. Course and human validation gates remain pending.")
r = json.loads((ROOT / "outputs/results.json").read_text(encoding="utf8"))
st.warning(r["status"])
history, config = load()

with st.sidebar:
    st.header("Operating driver workbench")
    st.button("Reset to base", on_click=reset_drivers)
    growth_shift = st.slider("Revenue growth shift, 2027-2030 (percentage points)", -15.0, 15.0, 0.0, 0.5, key="growth_shift") / 100
    margin_shift = st.slider("Operating margin shift (percentage points)", -5.0, 5.0, 0.0, 0.5, key="margin_shift") / 100
    wacc = st.slider("WACC (%)", 8.0, 13.0, 10.56, 0.01, key="wacc") / 100
    terminal_growth = st.slider("Terminal growth (%)", 2.0, 4.0, 3.0, 0.1, key="terminal_growth") / 100
    terminal_roic = st.slider("Mature return on invested capital (%)", 2.0, 30.0, 25.0, 0.5, key="terminal_roic") / 100
    st.caption(
        "Bounds are analyst stress limits, not probability estimates. Growth shifts bracket deceleration; margin shifts "
        "bracket compensation/compute costs. ROIC includes a weak-return failure case. Terminal margin stays fixed when "
        "explicit margins move. Capex is held at base pending the human locked test."
    )

live_rows = None
try:
    live_rows, live_value = calculate(history, config, growth_shift, margin_shift, wacc, terminal_growth, terminal_roic)
    st.success("Live checks PASS: statements balance, cash ties, WACC exceeds growth, terminal reinvestment is feasible.")
    st.metric("Live base-model value per diluted share", f"${live_value['per_share']:.2f}")
    st.caption("Restored-base value $29.76. Live results recalculate from the same operating forecast; saved independent cases below are unchanged.")
except ValueError as error:
    st.error("Live checks FAILED: " + str(error))
    st.info(
        "Recover using Reset to base. For the demonstration, set mature ROIC below terminal growth; funding the assumed "
        "perpetual growth requires more than all terminal operating profit."
    )

for column, (name, v) in zip(st.columns(3), r["cases"].items()):
    column.metric(name.capitalize() + " value / diluted share", f"${v['per_share']:.0f}")
    column.caption(f"Terminal dependence {v['terminal_share']:.0%}; {v['action'].replace('_', ' ')}")
st.write("Model range is a conditional estimate. Review assumption evidence and forecast maturity before accepting an investment action.")

case = st.selectbox("Inspect case", ["base", "low", "high"])
if case == "base" and live_rows is not None:
    f = pd.DataFrame(live_rows)
else:
    f = pd.read_csv(ROOT / f"outputs/{case}_three_statements.csv")
if case == "base" and live_rows is None:
    st.warning("Input combination failed. Table below is the saved base, not a live result.")

tabs = st.tabs(["Income statement", "Balance sheet", "Cash flow and FCFF", "Sensitivity", "Comparables", "Reverse DCF", "Validation"])
with tabs[0]:
    st.dataframe(f[INCOME_COLUMNS].set_index("year").T)
with tabs[1]:
    st.dataframe(f[BALANCE_COLUMNS].set_index("year").T)
with tabs[2]:
    st.info("2026 cash flows cover H2; valuation uses the post-October 5 fraction. Later years are full annual flows.")
    st.dataframe(f[CASH_COLUMNS].set_index("year").T)
with tabs[3]:
    grid = pd.read_csv(ROOT / "outputs/wacc_growth.csv")
    st.dataframe(grid.pivot(index="wacc", columns="growth", values="per_share"))
    st.write("One-at-a-time changes; all other assumptions reset to base")
    st.dataframe(pd.read_csv(ROOT / "outputs/one_at_a_time.csv"))
    st.write("Equal proportional perturbations: 90%, 100%, 110% of base input rates/levels")
    st.dataframe(pd.read_csv(ROOT / "outputs/equal_proportional_sensitivity.csv"))
with tabs[4]:
    st.dataframe(pd.read_csv(ROOT / "outputs/peer_multiples.csv"))
    st.dataframe(pd.read_csv(ROOT / "outputs/relative_valuation.csv"))
    st.caption(
        "Latest reported TTM periods differ by one month; share/balance dates precede prices. P/E is affected by "
        "investment gains and tax benefits. Basic-share relative values differ from diluted DCF values."
    )
with tabs[5]:
    st.json(r["reverse_dcf"])
with tabs[6]:
    st.json(r["historical_checks"])
    st.markdown((ROOT / "validation/STATUS.md").read_text(encoding="utf8"))

st.subheader("Assumptions and limitations")
st.json(json.loads((ROOT / "config/assumptions.json").read_text(encoding="utf8")))
for caveat in r["caveats"]:
    st.write("â€¢ " + caveat)
