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


def forecast(case, data, config):
    """Build five integrated annual statements (2026 H2 flows, then 2027-2030 full years)."""
    h = data["interim_2026h1"]
    prev = copy.deepcopy(h)
    rows = []
    commercial = config["base_2026_revenue"] * h["commercial"] / h["revenue"]
    government = config["base_2026_revenue"] - commercial
    working_capital = config["working_capital"]
    presentation = config["presentation"]
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
        option_amort = h["unrecognized_option_comp"] / h["option_service_years"]
        sar_amort = h["unrecognized_sar_comp"] / h["sar_service_years"]
        rsu_amort = h["unrecognized_rsu_comp"] / h["rsu_service_years"] if i < h["rsu_service_years"] else 0
        old_award_amort = (option_amort + sar_amort + rsu_amort) * (184 / 365 if i == 0 else 1)
        ebit = raw_ebit + old_award_amort

        da = revenue * config["da_ratio"]
        capex = revenue * config["capex_ratio"]
        period_fraction = 184 / 365 if i == 0 else 1
        # H2 normalized operations derived from full-year forecast less reported H1.
        ebit_period = ebit - h["ebit"] if i == 0 else ebit
        da_period = da - h["da"] if i == 0 else da
        capex_period = capex - h["capex"] if i == 0 else capex
        if capex_period < 0 or da_period < 0:
            raise ValueError("Forecast full-year reinvestment below realized H1")

        tax_operating = max(ebit_period, 0) * config["tax"]
        interest = (prev["cash"] + prev["investments"]) * config["interest_yield"] * period_fraction
        period_net = ebit_period + interest - max(ebit_period + interest, 0) * config["tax"]

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
        valued_fcff = fcff * config["remaining_days"] / 184 if i == 0 else fcff

        cost_of_revenue = revenue * presentation["cost_of_revenue_ratio"]
        operating_cost = revenue - cost_of_revenue - raw_ebit
        annual_interest = interest + (h["interest_income"] if i == 0 else 0)
        annual_tax = max(ebit_period + interest, 0) * config["tax"] + (h["tax"] if i == 0 else 0)
        annual_net = period_net + (h["net_income"] if i == 0 else 0)
        row = dict(
            cost_of_revenue=cost_of_revenue,
            gross_profit=revenue - cost_of_revenue,
            sales_marketing=operating_cost * presentation["sales_share_opex"],
            research_development=operating_cost * presentation["rd_share_opex"],
            general_administrative=operating_cost * presentation["ga_share_opex"],
            annual_interest=annual_interest,
            annual_other_income=h["other_income"] if i == 0 else 0,
            annual_tax=annual_tax,
            annual_net_income=annual_net,
            year=year,
            commercial_revenue=commercial,
            government_revenue=government,
            revenue=revenue,
            ebit_before_old_award_adjustment=raw_ebit,
            existing_award_service_adjustment=old_award_amort,
            ebit=ebit,
            period_ebit=ebit_period,
            period_interest=interest,
            period_tax=max(ebit_period + interest, 0) * config["tax"],
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


def bridge(data, config):
    """Enterprise-to-equity bridge from the latest reported balance sheet and award counts."""
    h = data["interim_2026h1"]
    diluted_shares = h["basic_shares"] + h["options"] + h["rsus"] + h["prsus"] + h["sars"]
    return Bridge(
        max(0, h["cash"] - config["cash_reserve"]),
        h["investments"] + h["options"] * h["option_strike"],
        0,
        h["nci"],
        diluted_shares,
    )


def action_for(price, per_share):
    """Map price versus value to the recorded committee action thresholds."""
    if price < per_share * 0.8:
        return "initiate_candidate"
    if price > per_share * 1.2:
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
    periods = [config["remaining_days"] / 365 + i for i in range(5)]
    fcffs = [r["valued_fcff"] for r in rows]
    v = dcf(fcffs, periods, case["wacc"], case["growth"], terminal_fcff, bridge(data, config))
    v.update(
        terminal_revenue=terminal_revenue,
        terminal_nopat=nopat,
        terminal_fcff=terminal_fcff,
        action=action_for(config["price"], v["per_share"]),
    )
    return v


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

    lo, hi = 0.0, 6.0
    if implied(hi) < config["price"]:
        return {"status": "unbracketed", "max_multiplier": hi, "value": implied(hi)}
    for _ in range(80):
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
    for wacc in [0.08, 0.09, 0.105, 0.12, 0.13]:
        for growth in [0.02, 0.03, 0.04]:
            case = {**c["cases"]["base"], "wacc": wacc, "growth": growth}
            v = value(forecasts["base"], case, data, c)
            sensitivity.append(
                dict(wacc=wacc, growth=growth, per_share=v["per_share"], terminal_share=v["terminal_share"])
            )
    dump_csv("outputs/wacc_growth.csv", sensitivity)

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
