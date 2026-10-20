"""Reconcile the shared DCF engine to the official Lab 05 published training-case answers."""
import json
from pathlib import Path

from src.dcf import Bridge, dcf

SOURCE = (
    "https://github.com/CinderZhang/FIN43900-Fall2026/blob/"
    "69eac1e8cbd63b35e801d48d990c4b594bfdbbc8/lessons/week-03/lab-05-dcf-build.md"
)
PUBLISHED = [108, 114.48, 120.204, 125.0122, 128.7625, 448.4408, 1894.6486, 1176.4277, 1624.8685, 1374.8685, 27.4974, 0.7240]


def run():
    """Compute the twelve published outputs and fail if any differs by more than 0.0001."""
    starting = 100
    rates = [0.08, 0.06, 0.05, 0.04, 0.03]
    fcffs = []
    for rate in rates:
        starting *= 1 + rate
        fcffs.append(starting)
    v = dcf(fcffs, [1, 2, 3, 4, 5], 0.10, 0.03, fcffs[-1] * 1.03, Bridge(50, 0, 300, 0, 50))
    actual = {
        **{f"FCFF Year {i + 1}": f for i, f in enumerate(fcffs)},
        "PV explicit": v["explicit_pv"],
        "Terminal value": fcffs[-1] * 1.03 / (0.10 - 0.03),
        "PV terminal": v["terminal_pv"],
        "EV": v["enterprise_value"],
        "Equity": v["equity_value"],
        "Per share": v["per_share"],
        "Terminal share": v["terminal_share"],
    }
    expected = dict(zip(actual, PUBLISHED))
    rows = []
    for label, calculated in actual.items():
        difference = calculated - expected[label]
        rows.append(
            dict(
                label=label,
                published=expected[label],
                calculated=calculated,
                difference=difference,
                tolerance=0.0001,
                passed=abs(difference) < 0.0001,
            )
        )
    if not all(x["passed"] for x in rows):
        raise ValueError("Published training case mismatch")
    packet = dict(
        source=SOURCE,
        local_source="data/reference/official-course/lessons/week-03/lab-05-dcf-build.md",
        status="PASS: all twelve published outputs; not an AI-invented synthetic answer",
        checks=rows,
    )
    Path("validation/published-training-reconciliation.json").write_text(json.dumps(packet, indent=2))
    print(packet["status"])
    return packet


if __name__ == "__main__":
    run()
