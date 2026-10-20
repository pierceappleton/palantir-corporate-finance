# Peer policy — revised 2026-10-20 (post-comparison revision, Claude Code)

This file is a dated revision. The original policy, recorded before name selection on 2026-10-06, is preserved unchanged in `docs/peer-policy.md`. Its text is repeated here first so the change is visible.

## Original policy (2026-10-06, unchanged)
Use listed operating enterprise-software companies with recurring enterprise deployment economics, auditable filings and accessible common-date price/share data. Separate infrastructure/platform and application cohorts; discuss government exposure and growth differences. Exclude banks, insurers, REITs, private companies and acquired securities without common-date prices. Compute EV/revenue and market-cap/GAAP common net income using consistent TTM periods and economic EV definitions. Negative net income means P/E is not meaningful; do not replace silently with adjusted earnings. No forced transaction set. Selection and measurements remain pending.

## Why it was revised
Only ServiceNow (NOW) and Salesforce (CRM) were applied under the original policy. Two names are too thin a reference set against Palantir's roughly 72x trailing EV/revenue, and both grow more slowly than Palantir. The revision widens the candidate set under a written rule. It does not add names because they make the answer look better, and it never averages multiples with the DCF.

## Revised written rule (applied the same way to every candidate)
A candidate is **included** only if it passes all of tests 1 to 5:
1. **Business model:** a U.S.-listed operating company whose revenue is mainly recurring subscription or usage software sold to enterprises or governments (data/analytics platforms, AI/workflow platforms, observability/security infrastructure, mission or public-sector software). IT services, consulting and hardware companies fail.
2. **Scale:** trailing-twelve-month (TTM) revenue of at least $1.0B, so the revenue denominator is not dominated by a few contracts.
3. **Evidence:** latest 10-Q/10-K balance sheet and share count, and an October 5, 2026 regular-session close, each with a source URL and as-of date.
4. **Comparable definitions:** TTM revenue built the same way as for Palantir (latest fiscal year + current year-to-date − prior year-to-date); EV = market capitalization + debt + noncontrolling interest − cash − marketable securities; operating leases stay in operating cost for every company.
5. **Independence:** listed with its own common-date price (no pending acquisition at a fixed deal price).

Measurement rules for included names:
- **EV/revenue** is reported for every included name.
- **GAAP P/E** is reported only when TTM GAAP common net income is positive and the GAAP net margin is at least 5%. Otherwise the cell reads **"not meaningful"** with the reason (negative or tiny earnings). The name stays in the table. It is never silently dropped, and no adjusted earnings are substituted.
- **Forward EV/revenue** is added only if every included name has a dated consensus revenue estimate from the same provider on the same fiscal-year definition. Until then it is not reported.
- **Growth diagnostic:** EV/revenue is shown against year-to-date revenue growth (the same window used in the TTM build). This is a diagnostic, not a regression that produces a "fair" multiple for Palantir.
- **Cohorts:** platform/infrastructure, application, and government/public-sector software. Results are shown by cohort, not as one blended average.
- **Palantir P/E:** reported on GAAP earnings and, separately, on pretax income taxed at the normalized 25%. Palantir's 2025 effective tax rate was 1.4%, because of excess stock-compensation deductions and a full valuation allowance. That is a structural, recurring effect while the allowance stands, not a one-time item, but it is not a steady-state tax rate either.

## Candidate set to screen
| Ticker | Company | Proposed cohort | Test 1 (business model) | Tests 2–5 |
|---|---|---|---|---|
| NOW | ServiceNow | application/workflow | pass | data on file (2026-10-05 price, 2026-06-30 balances) |
| CRM | Salesforce | application | pass | data on file (2026-10-05 price, 2026-07-31 balances) |
| SNOW | Snowflake | data platform | pass | pending data |
| DDOG | Datadog | observability infrastructure | pass | pending data |
| CRWD | CrowdStrike | security infrastructure | pass | pending data |
| NET | Cloudflare | network/security infrastructure | pass | pending data |
| MDB | MongoDB | data platform | pass | pending data |
| ADBE | Adobe | application | pass | pending data |
| TYL | Tyler Technologies | government/public-sector software | pass | pending data |
| AI | C3.ai | AI applications | pass | pending data; check test 2 (scale) against the filing |
| BAH, CACI, LDOS | Booz Allen, CACI, Leidos | government IT services | fail (services) | not measured |

"Pending data" means the October 5, 2026 price, latest balance sheet, share count and TTM revenue/income have not been retrieved. In the 2026-10-20 session the session's network policy blocked the SEC, Treasury and market-data hosts, so nothing was entered from memory or from secondary summaries. `data/processed/peer_candidates.json` lists the exact fields and sources needed for each name.

## Status
The final peer list needs Pierce's approval. Until the pending data are retrieved and the list is approved, the model's peer outputs keep only NOW and CRM, now with an explicit P/E status and the growth diagnostic.
