"""Peer EV/revenue and GAAP P/E multiples on a consistent trailing-twelve-month basis."""
import json
from pathlib import Path

from src.model import dump_csv, load

QUALIFICATION = (
    "Book/face debt approximation; operating leases excluded with lease expense retained; "
    "strategic equity holdings receive zero separate credit, contaminate GAAP earnings. "
    "Latest balance/share dates differ from price date."
)


def multiples(p):
    """Compute TTM revenue, TTM GAAP common income, EV and the two multiples for one company."""
    revenue = p["annual_revenue"] + p["current_h1_revenue"] - p["prior_h1_revenue"]
    net_income = p["annual_ni"] + p["current_h1_ni"] - p["prior_h1_ni"]
    market_cap = p["price"] * p["shares"]
    ev = market_cap + p["debt"] + p.get("nci", 0) - p["cash"] - p["investments"]
    if revenue <= 0:
        raise ValueError("Revenue denominator invalid")
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
        pe=market_cap / net_income if net_income > 0 else None,
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


def run():
    """Write peer multiples and the basic-share PLTR values they imply."""
    peers = json.loads(Path("data/processed/peer_inputs.json").read_text(encoding="utf8"))
    rows = [multiples(p) for p in peers]
    data, c = load()
    h = data["interim_2026h1"]
    rows.append(multiples(palantir_inputs(data, c)))
    dump_csv("outputs/peer_multiples.csv", rows)

    pltr = rows[-1]
    relative = []
    for row in rows[:-1]:
        equity_from_ev = row["ev_revenue"] * pltr["ttm_revenue"] + h["cash"] + h["investments"] - h["nci"]
        equity_from_pe = row["pe"] * pltr["ttm_gaap_common_income"]
        relative.append(
            dict(
                peer=row["ticker"],
                ev_revenue_implied_basic_price=equity_from_ev / h["basic_shares"],
                pe_implied_basic_price=equity_from_pe / h["basic_shares"],
            )
        )
    dump_csv("outputs/relative_valuation.csv", relative)
    print(json.dumps(rows, indent=2))
    return rows


if __name__ == "__main__":
    run()
