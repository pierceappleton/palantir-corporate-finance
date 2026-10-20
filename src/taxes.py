"""Bounded net-operating-loss (NOL) utilization sensitivity. Not in the base case.

The base forecast charges a normalized 25% tax from day one. The 2025 10-K reports about
$9.0B federal and $4.8B state NOLs, but face value alone does not prove zero cash taxes:
- post-2017 federal NOLs ($8.3B, indefinite) can offset at most 80% of taxable income a year;
- an ownership change (Internal Revenue Code section 382) can impose a further annual limit;
- state NOLs depend on apportionment and some expire from 2026;
- the NOLs arose mostly from excess stock-compensation deductions, which the cash-replacement
  convention removes from the forecast, so no further NOL build-up is modeled.
The schedule therefore reports a range of availability (share of the NOL pools usable) and
values the tax saved as a separate bridge item, leaving operating FCFF at the normalized rate.
Research-credit carryforwards ($578M federal) are not modeled.
"""
import copy

from src.model import bridge, dump_csv, forecast, load


def nol_schedule(rows, config, availability):
    """Year-by-year NOL use and tax saved when `availability` of each pool can be used."""
    nol = config["nol"]
    definite = nol["federal_definite"] * availability
    indefinite = nol["federal_indefinite"] * availability
    state = nol["state_nol"] * availability
    schedule = []
    for row in rows:
        taxable = max(row["period_pretax_income"], 0)
        use_definite = min(definite, taxable)
        use_indefinite = min(indefinite, nol["indefinite_limit"] * (taxable - use_definite))
        use_state = min(state, nol["state_limit"] * taxable)
        definite -= use_definite
        indefinite -= use_indefinite
        state -= use_state
        saved = (use_definite + use_indefinite) * nol["federal_rate"] + use_state * nol["state_rate"]
        schedule.append(
            dict(
                year=row["year"],
                availability=availability,
                taxable_income=taxable,
                federal_nol_used=use_definite + use_indefinite,
                state_nol_used=use_state,
                tax_saved=saved,
                federal_nol_remaining=definite + indefinite,
                state_nol_remaining=state,
            )
        )
    return schedule


def nol_value(rows, case, data, config, availability):
    """Present value of tax saved, in USD millions and per diluted share."""
    schedule = nol_schedule(rows, config, availability)
    periods = [config["remaining_days"] / config["days_in_year"] + i for i in range(len(rows))]
    present = sum(x["tax_saved"] / (1 + case["wacc"]) ** t for x, t in zip(schedule, periods))
    shares = bridge(data, config, rows).shares
    left = schedule[-1]["federal_nol_remaining"] + schedule[-1]["state_nol_remaining"]
    return dict(availability=availability, pv_tax_saved=present, per_share=present / shares, nol_left_after_2030=left), schedule


def run():
    """Write outputs/nol_sensitivity.csv (per case and availability) and the base schedule."""
    data, c = load()
    summary = []
    base_schedule = []
    for name, case in c["cases"].items():
        rows = forecast(case, data, c)
        for availability in c["nol"]["availability_scenarios"]:
            result, schedule = nol_value(rows, case, data, c, availability)
            summary.append(dict(case=name, **result))
            if name == "base":
                base_schedule.extend(schedule)
    dump_csv("outputs/nol_sensitivity.csv", summary)
    dump_csv("outputs/nol_schedule_base.csv", base_schedule)
    return summary


if __name__ == "__main__":
    for line in run():
        print(line)
