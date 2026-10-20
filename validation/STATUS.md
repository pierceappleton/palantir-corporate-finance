# Validation status
A Published training-case reconciliation: PASS. All twelve official Lab05 outputs match within0.0001; publication source and commit preserved.
B Source/definition check: cash versus restricted cash reconciled using balance-sheet and Note5 definitions; issuer rendering compared with SEC main statement. Same underlying filing, not independently audited new data. Oct5 market price cross-check uses separate providers; historical share counts remain stale.
C AI controlled directional tests: precommitted 10194f6 before run; pass.
D Human-assisted locked change: PENDING. Designated capex ratio 1.2% to 2.0% of revenue; prediction and human precommit required before run. The separate AI-controlled sensitivity in `validation/ai-capex-sensitivity-2026-10-19.json` predicted and observed a $0.1884/share decrease; it is not the human Gate D run.
E History and forecast articulation: 15 tests pass; annual and H1 totals reconcile. Checks establish arithmetic, not assumption truth.
F DCF known answer, boundaries, monotonicity and bridge: pass.
G Peer policy recorded before selected names; EV/revenue and GAAP P/E computed. Date and private-investment limitations disclosed; basic-share peer values cannot silently be combined with diluted DCF.
H Highest implementation risk: unit/restricted-cash contamination is injected and rejected. Highest economic risk remains premature terminal maturity, exposed in cases/sensitivity and challenge packet.
I Clean fresh environment run: PASS. validation/cold-run.json records five successful commands in a freshly created isolated environment, completed2026-10-06T22:51:14.041047+00:00. Includes32 raw-cell checks,12 tests, model/peer/report reproduction and all interface cases. First failed dependency-pin attempt is preserved separately.
J AI output corrected/qualified: automatic consumption of issuer-rendered signs rejected against SEC main statement; existing-award adjustment corrected to H2 service horizon. Adjusted operating margins rejected as substitutes for GAAP economic margin using issuer reconciliation.
Supplied Lab11 Ethan feedback is preserved and attributed; completed final review and recordings/transcripts remain pending. Course names/limits now verified; 300-point rubric, Brightspaceheader, officialEditionA PDF and grader access remain pending. Bounded liveworkbench reset/failure and one-at-a-time/equalproportional tests added postfreeze.

Postcomparison fresh-environment run: PASS; validation/postcomparison-cold-run.json; completed 2026-10-06T23:22:29.551572+00:00. 15 tests,32 source checks,12 official outputs and liveworkbench change/failure/reset all pass.

## Post-comparison revision, Claude Code, 2026-10-20
E: income-statement identity checks added (lines to EBIT; pretax - tax = net income). F: fade engine tests (zero-fade equivalence, cross-stage timing, growth/ROIC reinvestment, WACC > g); stub cash counted once; award runoff capped. G: revised peer rule with 'not meaningful' P/E marking; wider data pending. I: fresh-environment Linux cold run recorded in validation/cold-run-2026-10-20.json. D remains PENDING and was not run; the runner now commits only its record file. 35 tests and 38 source-row checks pass after adding the AI capex sensitivity regression test.

## AI-controlled capex sensitivity, 2026-10-20
Precommitted AI prediction at commit `1e3cdb9`, then changed capex/revenue from 1.2% to 2.0% with other inputs fixed. Base value fell from $30.1183 to $29.9299 per share (-$0.1884); FCFF fell in each forecast year, statement checks remained within tolerance, and the action remained do-not-initiate. Regression coverage is in `tests/test_accounting_corrections.py`. This does not complete human Validation Gate D.

Pierce A. & Rusheel N. later supplied a prediction timestamped 10:35 PM EDT on Oct 19, after the AI sensitivity execution at 8:49 PM EDT and after disclosure of its result. Their directional and approximate-size expectations match the already known AI result. It is preserved at `validation/user-supplied-capex-prediction-after-ai-run-2026-10-19.md` as a retrospective comparison only; it is not a precommit and does not satisfy Gate D.

## Separate human Gate D prepared October 20
Pierce agreed to perform a new AI-off prediction and AI-closed run after the original deadline. The designated new input is base-case 2029 government revenue growth 22% to 12%, with all other inputs fixed. The prepared runner is `validation/locked_human_government_2029.py`. It commits Pierce's own prediction before evaluating either case, then commits the actual result separately. The assistant has not run it or computed its expected result. Gate D remains pending until the two commits and Pierce's comparison are inspected. Preserve the real run time; do not characterize it as original-submission evidence.
