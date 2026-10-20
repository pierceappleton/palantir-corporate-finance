# Palantir committee memo (working draft)
Post-comparison revision, Claude Code, 2026-10-20. Generated 2026-10-20T03:30:58.497300+00:00. AI-generated after the official Edition A checkpoint. This is not the official Edition A and not Pierce's original judgment. The October 6 independent freeze (commit 890b973) and its memo (`submission/independent-memo.md`) are preserved unchanged.

**Pierce's adopted action: do not initiate at the October 5, 2026 regular close of $189.40 under this evidence and model.** The fundamental DCF case range is about **$17 to $66 per diluted economic share**, with the base near $30. Even the high case is below the price by more than the 120% do-not-initiate threshold. This is a judgment-dependent interval, not a statistical confidence interval. Pierce's action does not imply approval of every material model assumption listed under "Decisions pending."

The fund has no position. Intended user: buy-side analyst group and portfolio manager. Decision horizon: 3-5 years. Security: NASDAQ PLTR Class A; USD; Class A/B/F economic ownership counted; point-in-time basic shares distinguished from weighted-average EPS shares. Palantir sells software and services with identifiable operating revenue, costs, working capital and reinvestment, so operating-company enterprise FCFF is appropriate.

## What changed since the October 6 freeze (code corrections only)
| Case | Frozen Oct 6 | Corrected now |
|---|---:|---:|
| Low | $16.45 | $16.66 |
| Base | $29.76 | $30.12 |
| High | $65.48 | $65.91 |

1. **Cutoff cash.** The equity bridge used June 30 cash, but the valued FCFF only starts October 5. The 97 days in between were counted nowhere. Cash is now rolled forward by the cash the model retains in that stub: FCFF $799M + after-tax interest $56M + financing $0M = $856M, counted once.
2. **Existing-award runoff.** Remaining stock-compensation expense on awards outstanding at June 30 now follows an explicit straight-line schedule that stops at each unrecognized balance (options $361M over 4.89 years, SARs $136M over 8 years, RSUs $916M over 3 years). The old code stopped RSU expense six months early.
3. **Income-statement checks.** Displayed lines must add to EBIT and pretax income less tax must equal net income, or the run fails.

No economic assumption was changed. Every assumption option is shown separately in `docs/valuation-bridge-2026-10-20.md` and is **not adopted**.

## Evidence and accounting
The audited 2025 10-K (published February 17, 2026) supplies the annual base; the June 30, 2026 10-Q (published August 4) supplies interim statements, cash and awards. The October 5 close is the valuation and information cutoff. The August 3 FY2026 revenue guidance midpoint ($8.154B) is a forecast input, not realized revenue.

**Margins are GAAP.** Q2 2026 GAAP operating margin was 47.1% (operating income $912M on revenue $1,935M), up from 31.6% for FY2025 and 5.4% for FY2023. Stock-based compensation fell to 13.7% of revenue. The base path (46% in 2026 falling to 40% in 2030 and 35% at maturity) runs against this rising history. It is an analyst assumption about competition and compute/compensation cost, not something the filings show (see `outputs/margin_history.csv`).

**Existing-award add-back.** The input margins are GAAP-like and therefore include stock compensation. The awards already outstanding are counted as 196.7M extra diluted shares in the bridge, so their remaining expense ($1,325M over 2026 H2-2030) is added back to EBIT as its own line ("existing award service adjustment"). Charging both the dilution and the expense would count the same cost twice. This is why reported EBIT margin is above the input margin. Future grants are not added back: their cost stays inside the margin as an ongoing cash-replacement compensation cost.

**Taxes.** Operating tax (used in FCFF), book tax expense and cash tax paid are separate lines; all three use the normalized 25% because no deferred tax is modeled under the full valuation allowance. The 2025 10-K reports about $9.0B federal and $4.8B state NOLs, but face value alone does not prove zero cash taxes: $8.3B of the federal NOLs can offset only 80% of taxable income a year, and an ownership change could limit use further. A bounded utilization schedule adds $0.37 (50% usable) to $0.71 (100% usable) per share. It is not in the base.

Restricted cash gets no equity credit. Operating lease expense stays in EBIT. There is no hidden funding plug: cash comes from the cash-flow roll-forward, and a deficit would fail.

## Terminal convention and maturity
Terminal value is 66% to 83% of enterprise value with immediate maturity after 2030, so this assumption largely decides the answer. The shared engine now supports a fade period between 2030 and maturity (growth and margin move linearly toward terminal values; reinvestment = growth / ROIC). The base keeps immediate maturity until Pierce decides.

| Case | Immediate maturity (2030) | 5-year fade (2035) | 10-year fade (2040) |
|---|---:|---:|---:|
| Low | $16.66 (66% terminal) | $18.17 (49%) | $19.61 (36%) |
| Base | $30.12 (73% terminal) | $35.67 (62%) | $42.04 (54%) |
| High | $65.91 (83% terminal) | $94.96 (81%) | $139.49 (78%) |

A longer fade is another assumption to defend, not automatically the right answer. Even the high case with a 10-year fade stays below the price. The October 6 delayed-maturity path (five fixed fade years) gives $35.60.

Base WACC is 10.56% = 10-year Treasury 5.31% (Oct 5) + beta 1.25 x ERP 4.20%. The Treasury value, the ERP date and a sourced beta are **pending verification**: the source hosts were blocked in this session (`docs/source-verification-2026-10-20.md`). Beta is an analyst assumption. At beta 1.50 the base is $26.98; at 2.00 it is $22.54.

## What the price implies
One price cannot pin down growth, steady-state margin and fade length at once. Each line below moves one of them and holds the rest at base:
- At $189.40, with base margins, discount rate and immediate maturity after 2030 held fixed, the market implies revenue compounding about 122% a year from 2026 to 2030, versus 31% in the base case.
- At $189.40, with base growth held fixed, no steady-state operating margin up to 100% of revenue is enough (even 100% gives $65); the price cannot be explained by maturity-year profitability alone.
- At $189.40, with base growth and margins held fixed, the market implies about 60 years of linear fade before maturity.
- Diagnostic only: scaling base commercial growth alone requires 4.58x the base path (252%, 183%, 137%, 101% for 2027-2030).

## Relative valuation and why it disagrees with the DCF
The revised peer policy (`docs/peer-policy-revised-2026-10-20.md`) widens the candidate set under a written rule, but data for the new candidates are pending, so only ServiceNow and Salesforce are measured. Palantir trades at 72.4x TTM EV/revenue, against 9.6x for NOW and 4.9x for CRM. Palantir's year-to-date revenue growth was 89%, against 23% and 12%. Applied to Palantir, peer EV/revenue implies about $17 to $28 per basic share and peer GAAP P/E about $25 to $106. Palantir's own P/E is 151x on GAAP earnings (1.3% TTM tax rate) and 199x with a 25% tax.

The methods disagree for identifiable reasons, and they are not averaged. Peer multiples price slower-growing companies, so they cannot capture Palantir's growth. The DCF does price that growth explicitly, but then imposes a maturity date, a margin path and growth / ROIC reinvestment. The market price implies a much longer and more profitable runway than either method supports under these assumptions (see "What the price implies"). Basic-share relative values are not mixed with diluted DCF values. No transaction multiple is used: control, synergy and timing differences give no defensible bridge.

## Named stresses
- Procurement delay and AI deployment failure: $14.33 per share; action at today's price do not initiate; at a hypothetical $20 entry, do not initiate.
- Commercial conversion slowdown: $16.66 per share; action at today's price do not initiate; at a hypothetical $20 entry, do not initiate.
- Maturity deferred to2035 with five-year fade: $35.60 per share; action at today's price do not initiate; at a hypothetical $20 entry, initiate candidate.

## Conditions, reversals and monitoring
Revisit after reported commercial and government revenue, collections and GAAP margin, not deal value alone. Distinguish RPO from cancellable contract value. Monitor ongoing compensation, award issuance, cash taxes and valuation-allowance status, hosting commitments, capex, receivable concentration and pricing. Two consecutive quarters of realized growth above the high-case path would justify rebuilding the runway and maturity assumptions rather than moving a single multiple. A materially lower price or independently evidenced longer profitable runway could reverse the decision. At a hypothetical $20 price, base economics would support an initiate candidate while the low case reverses it. That is a conditional downside, not a forecast.

## Decisions pending (Pierce)
- Base-case fade length and margin path (currently immediate maturity and the October 6 margin path).
- Beta: keep 1.25 or adopt a sourced estimate.
- Final peer list under the revised rule.
- Whether to adopt the NOL utilization schedule.
- Final action label was adopted by Pierce on October 20: do not initiate at $189.40. The material assumptions above still require review.

## Validation limits and human work
Arithmetic and boundary tests pass; that is not proof of investment judgment. Still pending: Pierce's AI-off locked prediction and AI-closed locked run, the final partner review, the three recordings and corrected transcripts, the unchanged official Edition A PDF, the Brightspace deadline/header, the 300-point rubric and grader access. No complete course submission is claimed.
