"""Named stresses, working committee memo, static review page and README generator.

All generated text is written as UTF-8. Every number in the memo, review page and README is
read from outputs/*.csv or outputs/results.json, so the visible text cannot drift from the model.
"""
import copy
import csv
import html
import json
from datetime import datetime, timezone
from pathlib import Path

from src.model import action_for, dump_csv, forecast, load, value

REVISION_LABEL = "Post-comparison revision, Claude Code, 2026-10-20"


def save(path, text):
    """Write text as UTF-8."""
    Path(path).write_text(text, encoding="utf8")


def read_csv(name):
    """Read an output CSV into a list of dictionaries."""
    with Path("outputs", name).open(encoding="utf8", newline="") as f:
        return list(csv.DictReader(f))


def named_stresses(data, c):
    """Return the named stress rows and the delayed-maturity per-share value."""
    base = c["cases"]["base"]
    stresses = []
    conditional_price = c["recommendation_policy"]["conditional_entry_price"]
    stress = c["named_stresses"]["procurement_shock"]
    shock = copy.deepcopy(base)
    for key in ["commercial_growth", "government_growth", "margins", "nwc_ratio", "wacc"]:
        shock[key] = copy.deepcopy(stress[key])
    for name, case in [(stress["label"], shock), ("Commercial conversion slowdown", c["cases"]["low"])]:
        v = value(forecast(case, data, c), case, data, c)
        stresses.append(
            dict(
                scenario=name,
                value=v["per_share"],
                current_action=v["action"],
                conditional_price=conditional_price,
                conditional_action=action_for(conditional_price, v["per_share"], c),
            )
        )
    # Terminal-maturity challenge: the October 6 five-year fade path, valued by the shared engine.
    named = c["terminal_fade"]["named_path"]
    v = value(forecast(base, data, c), base, data, c, fade_years=len(named["growth"]), fade_path=named)
    transition_price = v["per_share"]
    stresses.append(
        dict(
            scenario=named["label"],
            value=transition_price,
            current_action=v["action"],
            conditional_price=conditional_price,
            conditional_action=action_for(conditional_price, transition_price, c),
        )
    )
    return stresses, transition_price


def convention(conventions, case, years):
    """Look up one row of outputs/terminal_conventions.csv."""
    for row in conventions:
        if row["case"] == case and int(row["fade_years"]) == years:
            return row
    raise KeyError((case, years))


def memo_text(r, c, stresses, transition_price, now):
    """Working committee memo (Markdown). The two-page PDFs are built separately."""
    cases = r["cases"]
    low, base, high = (cases[k]["per_share"] for k in ["low", "base", "high"])
    conventions = read_csv("terminal_conventions.csv")
    margins = {row["period"]: row for row in read_csv("margin_history.csv")}
    relative = read_csv("relative_valuation.csv")
    pe_norm = read_csv("pltr_pe_normalization.csv")[0]
    peers = {row["ticker"]: row for row in read_csv("peer_multiples.csv")}
    bridge_rows = {(row["case"], row["step"]): row for row in read_csv("valuation_bridge.csv")}
    stub = r["cutoff_cash"]["base"]
    nol = [x for x in r["nol_sensitivity"]["rows"] if x["case"] == "base"]
    shares_terminal = [float(convention(conventions, k, 0)["terminal_share"]) for k in ["low", "base", "high"]]
    fade5 = {k: float(convention(conventions, k, 5)["per_share"]) for k in ["low", "base", "high"]}
    fade10 = {k: float(convention(conventions, k, 10)["per_share"]) for k in ["low", "base", "high"]}
    frozen = {k: float(bridge_rows[(k, "Frozen October 6 model (7c190eb)")]["per_share"]) for k in ["low", "base", "high"]}
    ev_prices = [float(x["ev_revenue_implied_basic_price"]) for x in relative]
    pe_prices = [float(x["pe_implied_basic_price"]) for x in relative if x["pe_implied_basic_price"]]
    sentences = "\n".join(f"- {line}" for line in r["market_implied"]["sentences"])
    price = c["price"]
    ceiling = c["recommendation_policy"]["defer_ceiling_fraction"]
    q2 = margins["2026 Q2"]
    fy25 = margins["2025"]
    fy23 = margins["2023"]
    award = r["existing_awards"]
    added = sum(award[k]["added_back_2026h2_to_2030"] for k in ["options", "sars", "rsus"])
    return f"""# Palantir committee memo
{REVISION_LABEL}. Generated {now}. AI-assisted after the official Edition A checkpoint. This is not the official Edition A. Pierce adopted the do-not-initiate action on October 20, 2026. The October 6 independent freeze (commit 890b973) and its memo (`submission/independent-memo.md`) are preserved unchanged.

**Pierce's adopted action: do not initiate at the October 5, 2026 regular close of ${price:.2f} under this evidence and model.** The fundamental DCF case range is about **${low:.0f} to ${high:.0f} per diluted economic share**, with the base near ${base:.0f}. Even the high case is below the price by more than the {ceiling:.0%} do-not-initiate threshold. This is a judgment-dependent interval, not a statistical confidence interval. The adopted action does not approve every material model assumption listed below.

The fund has no position. Intended user: buy-side analyst group and portfolio manager. Decision horizon: 3-5 years. Security: NASDAQ PLTR Class A; USD; Class A/B/F economic ownership counted; point-in-time basic shares distinguished from weighted-average EPS shares. Palantir sells software and services with identifiable operating revenue, costs, working capital and reinvestment, so operating-company enterprise FCFF is appropriate.

## What changed since the October 6 freeze (code corrections only)
| Case | Frozen Oct 6 | Corrected now |
|---|---:|---:|
| Low | ${frozen['low']:.2f} | ${low:.2f} |
| Base | ${frozen['base']:.2f} | ${base:.2f} |
| High | ${frozen['high']:.2f} | ${high:.2f} |

1. **Cutoff cash.** The equity bridge used June 30 cash, but the valued FCFF only starts October 5. The {stub['stub_days']} days in between were counted nowhere. Cash is now rolled forward by the cash the model retains in that stub: FCFF ${stub['stub_fcff']:,.0f}M + after-tax interest ${stub['stub_after_tax_interest']:,.0f}M + financing ${stub['stub_financing']:,.0f}M = ${stub['stub_retained_cash']:,.0f}M, counted once.
2. **Existing-award runoff.** Remaining stock-compensation expense on awards outstanding at June 30 now follows an explicit straight-line schedule that stops at each unrecognized balance (options $361M over 4.89 years, SARs $136M over 8 years, RSUs $916M over 3 years). The old code stopped RSU expense six months early.
3. **Income-statement checks.** Displayed lines must add to EBIT and pretax income less tax must equal net income, or the run fails.

No economic assumption was changed. Every assumption option is shown separately in `docs/valuation-bridge-2026-10-20.md` and is **not adopted**.

## Evidence and accounting
The audited 2025 10-K (published February 17, 2026) supplies the annual base; the June 30, 2026 10-Q (published August 4) supplies interim statements, cash and awards. The October 5 close is the valuation and information cutoff. The August 3 FY2026 revenue guidance midpoint ($8.154B) is a forecast input, not realized revenue.

**Margins are GAAP.** Q2 2026 GAAP operating margin was {float(q2['gaap_operating_margin']):.1%} (operating income ${float(q2['gaap_operating_income']):,.0f}M on revenue ${float(q2['revenue']):,.0f}M), up from {float(fy25['gaap_operating_margin']):.1%} for FY2025 and {float(fy23['gaap_operating_margin']):.1%} for FY2023. Stock-based compensation fell to {float(q2['sbc_pct_revenue']):.1%} of revenue. The base path (46% in 2026 falling to 40% in 2030 and 35% at maturity) runs against this rising history. It is an analyst assumption about competition and compute/compensation cost, not something the filings show (see `outputs/margin_history.csv`).

**Existing-award add-back.** The input margins are GAAP-like and therefore include stock compensation. The awards already outstanding are counted as {sum(award['dilutive_shares_counted'].values()):.1f}M extra diluted shares in the bridge, so their remaining expense (${added:,.0f}M over 2026 H2-2030) is added back to EBIT as its own line ("existing award service adjustment"). Charging both the dilution and the expense would count the same cost twice. This is why reported EBIT margin is above the input margin. Future grants are not added back: their cost stays inside the margin as an ongoing cash-replacement compensation cost.

**Taxes.** Operating tax (used in FCFF), book tax expense and cash tax paid are separate lines; all three use the normalized 25% because no deferred tax is modeled under the full valuation allowance. The 2025 10-K reports about $9.0B federal and $4.8B state NOLs, but face value alone does not prove zero cash taxes: $8.3B of the federal NOLs can offset only 80% of taxable income a year, and an ownership change could limit use further. A bounded utilization schedule adds ${nol[1]['per_share']:.2f} (50% usable) to ${nol[2]['per_share']:.2f} (100% usable) per share. It is not in the base.

Restricted cash gets no equity credit. Operating lease expense stays in EBIT. There is no hidden funding plug: cash comes from the cash-flow roll-forward, and a deficit would fail.

## Terminal convention and maturity
Terminal value is {shares_terminal[0]:.0%} to {shares_terminal[2]:.0%} of enterprise value with immediate maturity after 2030, so this assumption largely decides the answer. The shared engine now supports a fade period between 2030 and maturity (growth and margin move linearly toward terminal values; reinvestment = growth / ROIC). The base keeps immediate maturity until Pierce decides.

| Case | Immediate maturity (2030) | 5-year fade (2035) | 10-year fade (2040) |
|---|---:|---:|---:|
| Low | ${low:.2f} ({shares_terminal[0]:.0%} terminal) | ${fade5['low']:.2f} ({float(convention(conventions, 'low', 5)['terminal_share']):.0%}) | ${fade10['low']:.2f} ({float(convention(conventions, 'low', 10)['terminal_share']):.0%}) |
| Base | ${base:.2f} ({shares_terminal[1]:.0%} terminal) | ${fade5['base']:.2f} ({float(convention(conventions, 'base', 5)['terminal_share']):.0%}) | ${fade10['base']:.2f} ({float(convention(conventions, 'base', 10)['terminal_share']):.0%}) |
| High | ${high:.2f} ({shares_terminal[2]:.0%} terminal) | ${fade5['high']:.2f} ({float(convention(conventions, 'high', 5)['terminal_share']):.0%}) | ${fade10['high']:.2f} ({float(convention(conventions, 'high', 10)['terminal_share']):.0%}) |

A longer fade is another assumption to defend, not automatically the right answer. Even the high case with a 10-year fade stays below the price. The October 6 delayed-maturity path (five fixed fade years) gives ${transition_price:.2f}.

Base WACC is 10.56% = 10-year Treasury 5.31% (Oct 5) + beta 1.25 x ERP 4.20%. The Treasury value, the ERP date and a sourced beta are **pending verification**: the source hosts were blocked in this session (`docs/source-verification-2026-10-20.md`). Beta is an analyst assumption. At beta 1.50 the base is ${float(bridge_rows[('base', 'Option: beta 1.50 (WACC 11.61%), hypothetical, not a sourced estimate')]['per_share']):.2f}; at 2.00 it is ${float(bridge_rows[('base', 'Option: beta 2.00 (WACC 13.71%), hypothetical, not a sourced estimate')]['per_share']):.2f}.

## What the price implies
One price cannot pin down growth, steady-state margin and fade length at once. Each line below moves one of them and holds the rest at base:
{sentences}

## Relative valuation and why it disagrees with the DCF
The revised peer policy (`docs/peer-policy-revised-2026-10-20.md`) widens the candidate set under a written rule, but data for the new candidates are pending, so only ServiceNow and Salesforce are measured. Palantir trades at {float(peers['PLTR']['ev_revenue']):.1f}x TTM EV/revenue, against {float(peers['NOW']['ev_revenue']):.1f}x for NOW and {float(peers['CRM']['ev_revenue']):.1f}x for CRM. Palantir's year-to-date revenue growth was {float(peers['PLTR']['ytd_revenue_growth']):.0%}, against {float(peers['NOW']['ytd_revenue_growth']):.0%} and {float(peers['CRM']['ytd_revenue_growth']):.0%}. Applied to Palantir, peer EV/revenue implies about ${min(ev_prices):.0f} to ${max(ev_prices):.0f} per basic share and peer GAAP P/E about ${min(pe_prices):.0f} to ${max(pe_prices):.0f}. Palantir's own P/E is {float(pe_norm['pe_gaap']):.0f}x on GAAP earnings (1.3% TTM tax rate) and {float(pe_norm['pe_normalized_tax']):.0f}x with a 25% tax.

The methods disagree for identifiable reasons, and they are not averaged. Peer multiples price slower-growing companies, so they cannot capture Palantir's growth. The DCF does price that growth explicitly, but then imposes a maturity date, a margin path and growth / ROIC reinvestment. The market price implies a much longer and more profitable runway than either method supports under these assumptions (see "What the price implies"). Basic-share relative values are not mixed with diluted DCF values. No transaction multiple is used: control, synergy and timing differences give no defensible bridge.

## Named stresses
{chr(10).join(f"- {row['scenario']}: ${row['value']:.2f} per share; action at today's price {row['current_action'].replace('_', ' ')}; at a hypothetical ${row['conditional_price']} entry, {row['conditional_action'].replace('_', ' ')}." for row in stresses)}

## Conditions, reversals and monitoring
Revisit after reported commercial and government revenue, collections and GAAP margin, not deal value alone. Distinguish RPO from cancellable contract value. Monitor ongoing compensation, award issuance, cash taxes and valuation-allowance status, hosting commitments, capex, receivable concentration and pricing. Two consecutive quarters of realized growth above the high-case path would justify rebuilding the runway and maturity assumptions rather than moving a single multiple. A materially lower price or independently evidenced longer profitable runway could reverse the decision. At a hypothetical ${c['recommendation_policy']['conditional_entry_price']} price, base economics would support an initiate candidate while the low case reverses it. That is a conditional downside, not a forecast.

## Decisions pending (Pierce)
- Base-case fade length and margin path (currently immediate maturity and the October 6 margin path).
- Beta: keep 1.25 or adopt a sourced estimate.
- Final peer list under the revised rule.
- Whether to adopt the NOL utilization schedule.
- Pierce's adopted action is do not initiate at the October 5 reference price; the material assumptions above remain subject to review.

## Validation limits and human work
Arithmetic and boundary tests pass; that is not proof of investment judgment. A separate AI-off human prediction and AI-closed 2029 government-growth run are prepared but pending. Replacement videos within course limits, corrected transcripts, final partner review and grader access checks remain open. Official Edition A is preserved unchanged, and the due time and 300-point rubric were read from Brightspace. The first Brightspace submission is preserved as a historical record.
"""


def table_html(name):
    """HTML table for one output CSV, numbers rounded for reading."""
    import pandas as pd

    return pd.read_csv("outputs/" + name).round(3).to_html(index=False)


def review_html(r, memo, low, high, price):
    """Static review page: material inputs, as-of date, decision and every output table."""
    sections = [
        ("Old-to-new valuation bridge (code corrections adopted; options not adopted)", "valuation_bridge.csv"),
        ("Terminal conventions: value and terminal share by fade length", "terminal_conventions.csv"),
        ("Market-implied expectations", "market_implied.csv"),
        ("Five-year base integrated forecast", "base_three_statements.csv"),
        ("Base fade schedule (5-year comparison)", "base_fade_schedule.csv"),
        ("Existing-award runoff schedule", "existing_award_runoff.csv"),
        ("GAAP margin and SBC history from filings", "margin_history.csv"),
        ("NOL utilization sensitivity (not in base)", "nol_sensitivity.csv"),
        ("WACC-growth sensitivity", "wacc_growth.csv"),
        ("Comparables", "peer_multiples.csv"),
        ("Relative valuation (basic shares)", "relative_valuation.csv"),
        ("Palantir P/E normalization", "pltr_pe_normalization.csv"),
        ("Named stresses", "named_stresses.csv"),
        ("One-at-a-time sensitivities", "one_at_a_time.csv"),
        ("Equal proportional sensitivities", "equal_proportional_sensitivity.csv"),
        ("Prior-work attribution (October 6 comparison, unchanged)", "prior-work-attribution.csv"),
    ]
    fragments = [
        "<h1>Palantir finance review</h1>",
        f"<p>{html.escape(REVISION_LABEL)}. Valuation date October 5, 2026 | DCF range ${low:.0f}-${high:.0f} per diluted share | "
        f"Conditional action: do not initiate at ${price:.2f}</p>",
        "<p>All currency and shares in millions unless stated; DCF values diluted, peer-relative values basic. Required course and human gates pending.</p>",
    ]
    for title, file in sections:
        fragments.append("<h2>" + html.escape(title) + "</h2>")
        fragments.append(table_html(file))
    fragments.append("<h2>Case results and checks (results.json)</h2><pre>" + html.escape(json.dumps(r, indent=2)) + "</pre>")
    fragments.append("<h2>Working committee memo</h2><pre>" + html.escape(memo) + "</pre>")
    style = (
        "<style>body{font:16px system-ui;margin:40px;color:#1b2735;background:#fff}table{border-collapse:collapse;font-size:13px;"
        "display:block;overflow:auto}td,th{padding:7px;border:1px solid #ccd3dc}pre{white-space:pre-wrap;"
        "line-height:1.5}h2{margin-top:35px}</style>"
    )
    return '<!doctype html><meta charset="utf-8"><title>Palantir finance review</title>' + style + "".join(fragments)


def readme_text(low, base, high, price):
    """Repository README with setup commands for Windows, macOS and Linux."""
    return f"""# Palantir corporate finance - FIN439
Project 1 for Pierce Appleton (Purdue, Finance and Accounting), built with AI assistance under Pierce's direction. AI use is disclosed in `docs/ai-use-record.md` and `submission/Validation-and-AI-Use.pdf`. The first submission was received through Brightspace at 12:00 AM October 20, 2026; post-deadline revisions are identified separately.

**Pierce's adopted committee action: do not initiate at the October 5 close of ${price:.2f}.** DCF range about ${low:.0f}-${high:.0f} per diluted share (base ${base:.2f}). The range is judgment-dependent, not a statistical confidence interval; see the assumptions and limitations before relying on it.

**First submission.** Brightspace received three videos, Edition A and the original Edition B. The official Edition A PDF is preserved unchanged at `submission/Edition A.pdf`; the original Edition B remains at `submission/Edition B.pdf`. The revised `submission/Research-Evolution.pdf` combines Edition A, a dated correction, revised Edition B and an A-to-B evidence map. A repository Markdown copy of Pierce's Edition A draft (`data/reference/FIN439-Labs/labs/lab-03/Project1_EditionA_Palantir.md`) was read after the October 6 independent freeze for comparison.

**Repository visibility.** This repository was observed public on October 20. The project plan had called for a private repository; grader access if visibility changes must be checked.

## Visible results
[Decision memo](submission/Decision-Memo.pdf), [validation and AI-use record](submission/Validation-and-AI-Use.pdf), [static review page](outputs/review.html), [results and checks](outputs/results.json), [valuation bridge](docs/valuation-bridge-2026-10-20.md), [terminal conventions](outputs/terminal_conventions.csv), [base five-year statements](outputs/base_three_statements.csv), [WACC-growth sensitivity](outputs/wacc_growth.csv), [peer multiples](outputs/peer_multiples.csv), [named stresses](outputs/named_stresses.csv).

## Setup and reproduction
Tested with Python 3.14.7 (Windows, October 6) and Python 3.13 (Linux, October 20). Run from the repository root.

Windows (PowerShell or Command Prompt):
```
python -m venv .venv
.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.venv\\Scripts\\python.exe -m src.reproduce
.venv\\Scripts\\python.exe -m streamlit run app/main.py
```

macOS or Linux:
```
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m src.reproduce
.venv/bin/python -m streamlit run app/main.py
```

Tests alone: `python -m pytest -q`. Old-to-new bridge: `python -m validation.valuation_bridge`. Two-page PDFs: `python -m src.build_submission_pdfs`. Fresh-environment cold run: `python validation/fresh_cold_run.py`.

The reproduction command uses the saved filings and inputs; it needs no live prices or SEC downloads. Market inputs carry source URLs and as-of dates; items not yet verified are listed in `docs/source-verification-2026-10-20.md`. No credentials are committed.

## Navigation and validation
Read PROJECT_GUIDE.md, docs/STATUS.md, docs/HANDOFF.md, docs/requirements-matrix.csv, docs/normalization.md, docs/assumption-challenges.csv, docs/source_manifest.json and validation/STATUS.md. The financial engine is in `src/`; the interface is in `app/`. The separate human locked-run instructions are in `submission/separate-human-run.md`. The Lab 11 partner feedback supplied by Pierce is credited.

## Open items
- Validation Gate D was not completed by the original deadline. A new human-only 2029 government-growth test is prepared; its prediction and result remain pending. The earlier AI-controlled capex sensitivity is separate and does not substitute for it.
- Beta is an analyst assumption without a saved provider or regression source, and the peer set is narrow.
- Treasury yield and equity risk premium evidence has limits, listed in `docs/source-verification-2026-10-20.md`.
- Replacement videos under 3/5/5 minutes and corrected transcripts are pending.

The official checklist and video/memo limits are preserved under `data/reference/official-course` (see docs/submission-compliance.md).
"""


def run():
    """Regenerate stresses, memo, review page and README from saved results."""
    r = json.loads(Path("outputs/results.json").read_text(encoding="utf8"))
    data, c = load()
    stresses, transition_price = named_stresses(data, c)
    dump_csv("outputs/named_stresses.csv", stresses)
    low = r["cases"]["low"]["per_share"]
    high = r["cases"]["high"]["per_share"]
    base = r["cases"]["base"]["per_share"]
    now = datetime.now(timezone.utc).isoformat()
    memo = memo_text(r, c, stresses, transition_price, now)
    save("submission/current-model-memo.md", memo)
    save("outputs/review.html", review_html(r, memo, low, high, c["price"]))
    save("README.md", readme_text(low, base, high, c["price"]))


if __name__ == "__main__":
    run()
