"""Peer EV/revenue and GAAP P/E multiples on a consistent trailing-twelve-month basis."""
import json
from pathlib import Path

from src.model import dump_csv, load

QUALIFICATION = (
    "Book/face debt approximation; operating leases excluded with lease expense retained; "
    "strategic equity holdings receive zero separate credit, contaminate GAAP earnings. "
    "Latest balance/share dates differ from price date."
)


def pe_status(net_income, revenue, policy):
    """Return (P/E allowed, reason) under the revised peer policy."""
    if net_income <= 0:
        return False, "not meaningful: zero or negative TTM GAAP earnings"
    if net_income / revenue < policy["pe_min_net_margin"]:
        return False, f"not meaningful: GAAP net margin below {policy['pe_min_net_margin']:.0%}"
    return True, "meaningful"


def multiples(p, policy=None):
    """Compute TTM revenue, TTM GAAP common income, EV and the two multiples for one company."""
    policy = policy or {"pe_min_net_margin": 0.0}
    revenue = p["annual_revenue"] + p["current_h1_revenue"] - p["prior_h1_revenue"]
    net_income = p["annual_ni"] + p["current_h1_ni"] - p["prior_h1_ni"]
    market_cap = p["price"] * p["shares"]
    ev = market_cap + p["debt"] + p.get("nci", 0) - p["cash"] - p["investments"]
    if revenue <= 0:
        raise ValueError("Revenue denominator invalid")
    allowed, status = pe_status(net_income, revenue, policy)
    return dict(
        ticker=p["ticker"],
        price=p["price"],
        price_asof="2026-10-05",
        shares=p["shares"],
        shares_asof=p["shares_asof"],
        ttm_end=p["ttm_end"],
        ttm_revenue=revenue,
        ttm_gaap_common_income=net_income,
        market_cap=market_cap,
        ev=ev,
        ev_revenue=ev / revenue,
        pe=market_cap / net_income if allowed else None,
        pe_status=status,
        ytd_revenue_growth=p["current_h1_revenue"] / p["prior_h1_revenue"] - 1,
        private_portfolio_excluded_from_ev_bridge=p["private_portfolio"],
        qualification=QUALIFICATION,
    )


def palantir_inputs(data, config):
    """Assemble Palantir's own multiple inputs on the same basic-share convention as peers."""
    h = data["interim_2026h1"]
    annual = data["annual_2025"]
    prior = data["prior_2025h1"]
    return dict(
        ticker="PLTR",
        price=config["price"],
        shares=h["basic_shares"],
        shares_asof="2026-06-30",
        ttm_end="2026-06-30",
        cash=h["cash"],
        investments=h["investments"],
        debt=0,
        nci=h["nci"],
        private_portfolio=167,
        annual_revenue=annual["revenue"],
        current_h1_revenue=h["revenue"],
        prior_h1_revenue=prior["revenue"],
        annual_ni=annual["common_net_income"],
        current_h1_ni=h["common_net_income"],
        prior_h1_ni=prior["common_net_income"],
    )


def palantir_pe_normalization(data, config, pltr):
    """Palantir P/E on GAAP earnings and on TTM pretax income taxed at the normalized rate."""
    annual = data["annual_2025"]
    h = data["interim_2026h1"]
    prior = data["prior_2025h1"]
    rate = config["peer_policy"]["normalized_tax_rate_for_pltr_pe"]
    pretax = annual["pretax_income"] + h["pretax_income"] - prior["pretax_income"]
    reported_tax = (annual["pretax_income"] - annual["net_income"]) + h["tax"] - prior["tax"]
    nci_share = (annual["net_income"] - annual["common_net_income"]) + (h["net_income"] - h["common_net_income"]) - (
        prior["pretax_income"] - prior["tax"] - prior["common_net_income"]
    )
    normalized = pretax * (1 - rate) - nci_share
    return dict(
        ttm_end="2026-06-30",
        ttm_pretax_income=pretax,
        ttm_reported_tax=reported_tax,
        ttm_effective_tax_rate=reported_tax / pretax,
        ttm_gaap_common_income=pltr["ttm_gaap_common_income"],
        normalized_tax_rate=rate,
        ttm_normalized_common_income=normalized,
        market_cap=pltr["market_cap"],
        pe_gaap=pltr["market_cap"] / pltr["ttm_gaap_common_income"],
        pe_normalized_tax=pltr["market_cap"] / normalized,
        one_time_tax_item_identified="none: low rate reflects excess stock-compensation deductions and a full valuation allowance (2025 10-K tax note); a future allowance release would be a one-time benefit and is not in these figures",
    )


def run():
    """Write peer multiples and the basic-share PLTR values they imply."""
    peers = json.loads(Path("data/processed/peer_inputs.json").read_text(encoding="utf8"))
    data, c = load()
    policy = c["peer_policy"]
    rows = [multiples(p, policy) for p in peers]
    h = data["interim_2026h1"]
    rows.append(multiples(palantir_inputs(data, c), policy))
    dump_csv("outputs/peer_multiples.csv", rows)
    dump_csv("outputs/pltr_pe_normalization.csv", [palantir_pe_normalization(data, c, rows[-1])])

    pltr = rows[-1]
    relative = []
    for row in rows[:-1]:
        equity_from_ev = row["ev_revenue"] * pltr["ttm_revenue"] + h["cash"] + h["investments"] - h["nci"]
        equity_from_pe = row["pe"] * pltr["ttm_gaap_common_income"] if row["pe"] is not None else None
        relative.append(
            dict(
                peer=row["ticker"],
                ev_revenue_implied_basic_price=equity_from_ev / h["basic_shares"],
                pe_implied_basic_price=equity_from_pe / h["basic_shares"] if equity_from_pe is not None else None,
                pe_status=row["pe_status"],
            )
        )
    dump_csv("outputs/relative_valuation.csv", relative)
    print(json.dumps(rows, indent=2))
    return rows


if __name__ == "__main__":
    run()
