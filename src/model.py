"""Transparent provisional integrated cash-replacement pro-forma, USD millions."""
import copy
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from src.dcf import Bridge, dcf

ASSET_KEYS = ["cash", "investments", "ar", "prepaid", "ppe", "rou", "other_assets"]
LIABILITY_KEYS = [
    "ap_accrued",
    "contract_current",
    "lease_current",
    "contract_noncurrent",
    "lease_noncurrent",
    "other_liabilities",
]


def load():
    """Return (historical inputs, assumptions) from the repository data files."""
    data = json.loads(Path("data/processed/historical.json").read_text(encoding="utf8"))
    config = json.loads(Path("config/assumptions.json").read_text(encoding="utf8"))
    return data, config


def check_history(data):
    """Reconcile reported balance sheets and cash roll-forwards; fail loudly on any residual."""
    checks = []
    for key in ["annual_2025", "interim_2026h1"]:
        b = data[key]
        assets = sum(b[k] for k in ASSET_KEYS)
        liabilities = sum(b[k] for k in LIABILITY_KEYS)
        residuals = [
            ("assets", assets - b["assets"]),
            ("liabilities", liabilities - b["liabilities"]),
            ("balance", b["assets"] - b["liabilities"] - b["equity"] - b["nci"]),
            ("cash", b["cash_total_start"] + b["cfo"] + b["cfi"] + b["cff"] + b["fx"] - b["cash_total"]),
        ]
        for name, residual in residuals:
            if abs(residual) > 1e-6:
                raise ValueError(f"{key} {name} reconciliation failed: {residual}")
            checks.append(dict(period=key, check=name, residual=residual))
    return checks


def forecast_periods(config, count):
    """Return (start, end) of each forecast period in years after the June 30, 2026 balance sheet."""
    h2_fraction = config["cashflow_days_h2"] / config["days_in_year"]
    periods = [(0.0, h2_fraction)]
    for i in range(1, count):
        periods.append((h2_fraction + i - 1, h2_fraction + i))
    return periods


AWARD_TYPES = [
    ("options", "unrecognized_option_comp", "option_service_years"),
    ("sars", "unrecognized_sar_comp", "sar_service_years"),
    ("rsus", "unrecognized_rsu_comp", "rsu_service_years"),
]


def existing_award_runoff(data, config, count):
    """Straight-line remaining-service schedule for awards outstanding at June 30, 2026.

    Each award type's unrecognized compensation is spread evenly over its disclosed
    weighted-average remaining service period, starting July 1, 2026, and stops once the
    balance is fully recognized. Returns one dict per period with each type's amortization.
    """
    h = data["interim_2026h1"]
    legacy = not config.get("corrections", {}).get("award_runoff_schedule", True)
    h2_fraction = config["cashflow_days_h2"] / config["days_in_year"]
    rows = []
    for i, (start, end) in enumerate(forecast_periods(config, count)):
        row = {"period_index": i, "start_years": start, "end_years": end}
        for name, balance_key, years_key in AWARD_TYPES:
            balance = h[balance_key]
            if legacy:
                # Frozen October 6 convention, kept only to reproduce the valuation bridge:
                # rounded service periods and RSU expense switched off after the third index.
                years = h.get(years_key + "_text", h[years_key])
                annual = balance / years
                if name == "rsus" and i >= years:
                    annual = 0
                amount = annual * (h2_fraction if i == 0 else 1)
            else:
                years = h[years_key]
                overlap = max(0.0, min(end, years) - max(start, 0.0))
                amount = balance * overlap / years
            row[name] = amount
        row["total"] = sum(row[name] for name, _, _ in AWARD_TYPES)
        rows.append(row)
    return rows


def forecast(case, data, config):
    """Build five integrated annual statements (2026 H2 flows, then 2027-2030 full years)."""
    h = data["interim_2026h1"]
    prev = copy.deepcopy(h)
    rows = []
    commercial = config["base_2026_revenue"] * h["commercial"] / h["revenue"]
    government = config["base_2026_revenue"] - commercial
    working_capital = config["working_capital"]
    presentation = config["presentation"]
    h2_days = config["cashflow_days_h2"]
    h2_fraction = h2_days / config["days_in_year"]
    runoff = existing_award_runoff(data, config, 5)
    # Other assets/ROU, investments, noncurrent leases/contract liabilities and NCI held constant.
    # Cash is calculated from cash flows, never used to fix the balance residual.
    for i, year in enumerate(range(2026, 2031)):
        if i:
            commercial *= 1 + case["commercial_growth"][i]
            government *= 1 + case["government_growth"][i]
        revenue = commercial + government
        raw_ebit = revenue * case["margins"][i]

        # Previously issued awards receive explicit dilution. Remove prospective service
        # expense of those same awards before applying a cash-replacement convention.
        # The input margin is GAAP-like (it includes stock compensation). The old awards are
        # already counted as diluted shares, so their remaining expense is added back once here.
        old_award_amort = runoff[i]["total"]
        ebit = raw_ebit + old_award_amort

        da = revenue * config["da_ratio"]
        capex = revenue * config["capex_ratio"]
        period_fraction = h2_fraction if i == 0 else 1
        # H2 normalized operations derived from full-year forecast less reported H1.
        ebit_period = ebit - h["ebit"] if i == 0 else ebit
        da_period = da - h["da"] if i == 0 else da
        capex_period = capex - h["capex"] if i == 0 else capex
        if capex_period < 0 or da_period < 0:
            raise ValueError("Forecast full-year reinvestment below realized H1")

        # Three tax measures are kept apart. Operating tax: normalized tax on EBIT used in FCFF.
        # Book tax expense: tax on pretax income in the income statement. Cash tax paid: equals
        # book tax here because no deferred tax is modeled (full valuation allowance; see docs).
        tax_operating = max(ebit_period, 0) * config["tax"]
        interest = (prev["cash"] + prev["investments"]) * config["interest_yield"] * period_fraction
        period_pretax = ebit_period + interest
        period_tax = max(period_pretax, 0) * config["tax"]
        period_net = period_pretax - period_tax

        ar = revenue * working_capital["ar_ratio"]
        prepaid = revenue * working_capital["prepaid_ratio"]
        ap = revenue * working_capital["accrual_ratio"]
        contract = revenue * (working_capital["contract_offset_ratio"] - case["nwc_ratio"])
        old_nwc = prev["ar"] + prev["prepaid"] - prev["ap_accrued"] - prev["contract_current"]
        nwc = ar + prepaid - ap - contract
        delta = nwc - old_nwc

        cfo = period_net + da_period - delta
        cfi = -capex_period
        cff = 0.0
        cash = prev["cash"] + cfo + cfi + cff
        if cash < 0:
            raise ValueError("Cash deficit: financing required; no hidden funding plug")
        ppe = prev["ppe"] + capex_period - da_period
        equity = prev["equity"] + period_net
        liabilities = ap + contract + h["contract_noncurrent"] + h["lease_noncurrent"] + h["other_liabilities"]
        assets = cash + h["investments"] + ar + prepaid + ppe + h["rou"] + h["other_assets"]
        residual = assets - liabilities - equity - h["nci"]
        if abs(residual) > 1e-6:
            raise ValueError(f"{year}: statements fail {residual}")

        fcff = ebit_period - tax_operating + da_period - capex_period - delta
        # First explicit FCFF includes only post-Oct5 portion of H2; uniform H2
        # cash timing is an approximation and is exposed for challenge.
        valued_fcff = fcff * config["remaining_days"] / h2_days if i == 0 else fcff

        cost_of_revenue = revenue * presentation["cost_of_revenue_ratio"]
        operating_cost = revenue - cost_of_revenue - raw_ebit
        annual_interest = interest + (h["interest_income"] if i == 0 else 0)
        annual_other_income = h["other_income"] if i == 0 else 0
        annual_tax = period_tax + (h["tax"] if i == 0 else 0)
        annual_net = period_net + (h["net_income"] if i == 0 else 0)
        annual_pretax = ebit + annual_interest + annual_other_income
        sales_marketing = operating_cost * presentation["sales_share_opex"]
        research_development = operating_cost * presentation["rd_share_opex"]
        general_administrative = operating_cost * presentation["ga_share_opex"]
        check_income_statement(
            year,
            revenue=revenue,
            expense_lines=[cost_of_revenue, sales_marketing, research_development, general_administrative],
            award_adjustment=old_award_amort,
            ebit=ebit,
            pretax=annual_pretax,
            tax=annual_tax,
            net_income=annual_net,
        )
        check_income_statement(
            f"{year} modeled period",
            revenue=0,
            expense_lines=[],
            award_adjustment=0,
            ebit=0,
            pretax=period_pretax,
            tax=period_tax,
            net_income=period_net,
        )
        row = dict(
            cost_of_revenue=cost_of_revenue,
            gross_profit=revenue - cost_of_revenue,
            sales_marketing=sales_marketing,
            research_development=research_development,
            general_administrative=general_administrative,
            annual_interest=annual_interest,
            annual_other_income=annual_other_income,
            annual_pretax_income=annual_pretax,
            annual_tax=annual_tax,
            annual_net_income=annual_net,
            year=year,
            commercial_revenue=commercial,
            government_revenue=government,
            revenue=revenue,
            ebit_before_old_award_adjustment=raw_ebit,
            existing_award_service_adjustment=old_award_amort,
            ebit=ebit,
            input_operating_margin=case["margins"][i],
            reported_ebit_margin=ebit / revenue,
            period_ebit=ebit_period,
            period_interest=interest,
            period_pretax_income=period_pretax,
            period_tax=period_tax,
            operating_tax=tax_operating,
            book_tax_expense=period_tax,
            cash_tax_paid=period_tax,
            period_net_income=period_net,
            da=da_period,
            capex=capex_period,
            delta_nwc=delta,
            fcff=fcff,
            valued_fcff=valued_fcff,
            cash=cash,
            investments=h["investments"],
            ar=ar,
            prepaid=prepaid,
            ppe=ppe,
            rou=h["rou"],
            other_assets=h["other_assets"],
            ap_accrued=ap,
            contract_current=contract,
            contract_noncurrent=h["contract_noncurrent"],
            lease_noncurrent=h["lease_noncurrent"],
            other_liabilities=h["other_liabilities"],
            assets=assets,
            liabilities=liabilities,
            equity=equity,
            nci=h["nci"],
            cfo=cfo,
            cfi=cfi,
            cff=cff,
            balance_residual=residual,
            cash_residual=cash - prev["cash"] - cfo - cfi - cff,
            period_label="2026 H2 modeled flows; annual revenue/EBIT" if i == 0 else "full year",
        )
        rows.append(row)
        prev = row
    return rows


def check_income_statement(label, revenue, expense_lines, award_adjustment, ebit, pretax, tax, net_income):
    """Fail loudly unless displayed lines add to EBIT and pretax income less tax equals net income."""
    ebit_residual = revenue - sum(expense_lines) + award_adjustment - ebit
    if abs(ebit_residual) > 1e-6:
        raise ValueError(f"{label}: income statement lines do not add to EBIT ({ebit_residual})")
    net_residual = pretax - tax - net_income
    if abs(net_residual) > 1e-6:
        raise ValueError(f"{label}: pretax income less tax does not equal net income ({net_residual})")


def cutoff_cash(rows, data, config):
    """Roll reported June 30 cash forward to the October 5 valuation date.

    The first forecast row holds modeled July-December flows. The part before the valuation
    date (cashflow_days_h2 - remaining_days days) is not in the valued FCFF, so the cash it
    actually retains is added to the bridge exactly once. Retained cash is reconciled as
    FCFF + after-tax interest + financing flows (zero: no debt, dividends, buybacks or NCI
    distributions are modeled); marketable securities are held constant, so no investment
    purchase or sale moves cash between the two credited balances.
    """
    h = data["interim_2026h1"]
    first = rows[0]
    stub_fraction = (config["cashflow_days_h2"] - config["remaining_days"]) / config["cashflow_days_h2"]
    after_tax_interest = first["period_net_income"] - (first["period_ebit"] - first["operating_tax"])
    stub = dict(
        june_30_cash=h["cash"],
        stub_days=config["cashflow_days_h2"] - config["remaining_days"],
        stub_fraction=stub_fraction,
        stub_fcff=first["fcff"] * stub_fraction,
        stub_after_tax_interest=after_tax_interest * stub_fraction,
        stub_financing=first["cff"] * stub_fraction,
        stub_retained_cash=(first["cfo"] + first["cfi"] + first["cff"]) * stub_fraction,
    )
    reconciled = stub["stub_fcff"] + stub["stub_after_tax_interest"] + stub["stub_financing"]
    if abs(reconciled - stub["stub_retained_cash"]) > 1e-6:
        raise ValueError(f"Stub cash does not reconcile to FCFF, interest and financing ({reconciled - stub['stub_retained_cash']})")
    if not config.get("corrections", {}).get("cutoff_cash_rollforward", True):
        stub["stub_retained_cash_credited"] = 0.0
    else:
        stub["stub_retained_cash_credited"] = stub["stub_retained_cash"]
    stub["valuation_date_cash"] = h["cash"] + stub["stub_retained_cash_credited"]
    return stub


def bridge(data, config, rows=None):
    """Enterprise-to-equity bridge from the latest reported balance sheet and award counts.

    Without forecast rows this is the June 30 bridge; with rows, cash is rolled to the
    valuation date by cutoff_cash.
    """
    h = data["interim_2026h1"]
    diluted_shares = h["basic_shares"] + h["options"] + h["rsus"] + h["prsus"] + h["sars"]
    cash = h["cash"] if rows is None else cutoff_cash(rows, data, config)["valuation_date_cash"]
    return Bridge(
        max(0, cash - config["cash_reserve"]),
        h["investments"] + h["options"] * h["option_strike"],
        0,
        h["nci"],
        diluted_shares,
    )


def action_for(price, per_share, config):
    """Map price versus value to the recorded committee action thresholds."""
    policy = config["recommendation_policy"]
    if price < per_share * policy["initiate_fraction"]:
        return "initiate_candidate"
    if price > per_share * policy["defer_ceiling_fraction"]:
        return "do_not_initiate"
    return "watch_defer"


def value(rows, case, data, config):
    """Value the forecast with a mature Gordon terminal and the shared equity bridge."""
    final = rows[-1]["revenue"]
    terminal_revenue = final * (1 + case["growth"])
    nopat = terminal_revenue * case["terminal_margin"] * (1 - config["tax"])
    terminal_fcff = nopat * (1 - case["growth"] / config["terminal_roic"])
    if terminal_fcff <= 0:
        raise ValueError("Terminal reinvestment incompatible with growth/ROIC")
    periods = [config["remaining_days"] / config["days_in_year"] + i for i in range(5)]
    fcffs = [r["valued_fcff"] for r in rows]
    v = dcf(fcffs, periods, case["wacc"], case["growth"], terminal_fcff, bridge(data, config, rows))
    v.update(
        terminal_revenue=terminal_revenue,
        terminal_nopat=nopat,
        terminal_fcff=terminal_fcff,
        action=action_for(config["price"], v["per_share"], config),
    )
    return v


def award_reconciliation_table(data, config, runoff):
    """Show how existing awards are counted once: as dilution, never again as expense."""
    h = data["interim_2026h1"]
    in_forecast = runoff[:5]
    table = {}
    for name, balance_key, years_key in AWARD_TYPES:
        added_back = sum(row[name] for row in in_forecast)
        table[name] = dict(
            unrecognized_compensation=h[balance_key],
            remaining_service_years=h[years_key],
            added_back_2026h2_to_2030=added_back,
            recognized_after_2030_not_added_back=h[balance_key] - added_back,
        )
    table["dilutive_shares_counted"] = dict(options=h["options"], rsus=h["rsus"], prsus=h["prsus"], sars=h["sars"])
    table["treatment"] = (
        "Existing awards are counted once, as diluted shares in the bridge (options also credit exercise "
        "proceeds). Their remaining GAAP expense is added back to EBIT over the forecast so it is not charged a "
        "second time. Future grants are not added back: their cost stays inside the GAAP-like margin as an "
        "ongoing cash-replacement compensation cost, and no future share issuance is modeled."
    )
    return table


def dump_csv(path, rows):
    """Write a list of dictionaries to CSV with UTF-8 encoding."""
    with Path(path).open("w", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def reverse_dcf(data, config):
    """Find the multiplier on base commercial growth that reproduces the market price."""

    def implied(multiplier):
        case = copy.deepcopy(config["cases"]["base"])
        case["commercial_growth"] = [x * multiplier for x in case["commercial_growth"]]
        return value(forecast(case, data, config), case, data, config)["per_share"]

    settings = config["reverse_dcf"]
    lo, hi = settings["multiplier_lower"], settings["multiplier_upper"]
    if implied(hi) < config["price"]:
        return {"status": "unbracketed", "max_multiplier": hi, "value": implied(hi)}
    for _ in range(settings["bisection_steps"]):
        mid = (lo + hi) / 2
        if implied(mid) < config["price"]:
            lo = mid
        else:
            hi = mid
    multiplier = (lo + hi) / 2
    return {
        "commercial_growth_multiplier": multiplier,
        "annual_growths": [x * multiplier for x in config["cases"]["base"]["commercial_growth"][1:]],
        "price_target": config["price"],
        "other_drivers": "base held fixed; mechanical expectation, not forecast",
    }


def run():
    """Run all cases, the WACC-growth grid and the reverse DCF; write outputs/results.json."""
    data, c = load()
    checks = check_history(data)
    results = {}
    forecasts = {}
    for name, case in c["cases"].items():
        rows = forecast(case, data, c)
        forecasts[name] = rows
        results[name] = value(rows, case, data, c)
        dump_csv(f"outputs/{name}_three_statements.csv", rows)

    sensitivity = []
    for wacc in c["sensitivity_grid"]["wacc"]:
        for growth in c["sensitivity_grid"]["growth"]:
            case = {**c["cases"]["base"], "wacc": wacc, "growth": growth}
            v = value(forecasts["base"], case, data, c)
            sensitivity.append(
                dict(wacc=wacc, growth=growth, per_share=v["per_share"], terminal_share=v["terminal_share"])
            )
    dump_csv("outputs/wacc_growth.csv", sensitivity)

    runoff = existing_award_runoff(data, c, 40)
    dump_csv("outputs/existing_award_runoff.csv", runoff[:10])
    award_reconciliation = award_reconciliation_table(data, c, runoff)

    # Reverse DCF: multiplier on commercial annual growth increments after 2026.
    reverse = reverse_dcf(data, c)
    packet = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        valuation_date=c["valuation_date"],
        status=(
            "Independent provisional analysis: postcomparison version: human locked test, "
            "final partner review and submission requirements pending"
        ),
        cases=results,
        cutoff_cash={name: cutoff_cash(rows, data, c) for name, rows in forecasts.items()},
        existing_awards=award_reconciliation,
        reverse_dcf=reverse,
        historical_checks=checks,
        caveats=[
            "H1 balance sheet used at Oct5; no reported Q3 cash available.",
            "2026 H2 normalized cash flows allocated uniformly after Oct5.",
            "Current lease included within aggregated working capital; noncurrent operating lease and ROU held constant.",
            "Existing awards assumed full vesting/exercise; SAR treated as full-share upper bound.",
            "Future compensation modeled as cash replacement; old award service cost removed to avoid duplication.",
        ],
    )
    Path("outputs/results.json").write_text(json.dumps(packet, indent=2))
    print(json.dumps(packet, indent=2))


if __name__ == "__main__":
    run()
