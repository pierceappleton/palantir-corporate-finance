# Decision log
2026-10-06: user instruction accepted as project execution authorization; official Edition A receipt confirmation preserved.
2026-10-06: no prior Palantir analysis inspected. Empty workspace except Git metadata verified.
2026-10-06: direct sandbox failed; approved external execution verified without changing controls. SEC/peer bulk HTTP downloads returned403; issuer Palantir mirrors succeeded, peer primary pages remain available through browser research and reproducible URLs.
2026-10-06: valuation/information cutoff chosen October5 regular close; latest filing balances June30, explicit staleness disclosure. Do not use October6 prices.
2026-10-06: peer policy precommitted before name selection; NOW and CRM chosen as workflow/application platforms. SNOW considered but omitted from P/E screen because loss-making economics require separate treatment; no cherry-picked negative multiple.
2026-10-06: future SBC cash replacement plus separately diluted old awards; remove old prospective service cost to avoid duplicate charging. SAR upper-bound dilution is conservative approximation.
2026-10-06: no forced transactions; acquisitions have control/synergy/integration differences.
2026-10-06: recommendation thresholds are policy assumptions: initiate candidate below80% of case value, do-not-initiate above120%, watch between; human strategy ownership preserved.

## Post-comparison revision, Claude Code, 2026-10-20
Not part of the October 6 independent freeze. Commits 890b973, d248dc4 and 7c190eb and their manifests are unchanged.
- Code correction: equity bridge cash rolled from June 30 to October 5 by the cash retained in the 97-day stub (FCFF + after-tax interest + financing). Base +$0.33.
- Code correction: existing-award runoff is now an explicit straight-line schedule capped at each unrecognized balance; RSUs run to June 2029; options use the filed 4y10m21d period. Base +$0.03.
- Code correction: income-statement identity checks; operating, book and cash tax shown separately.
- Engine: terminal fade moved into src/dcf.py/src/model.py; base_years = 0 (unchanged convention) pending Pierce.
- Not adopted (options awaiting Pierce): 5- or 10-year fade, flat 2026 margin, NOL shield, alternative beta, wider peer list. See docs/valuation-bridge-2026-10-20.md.
- Peer policy: dated revision docs/peer-policy-revised-2026-10-20.md; original preserved.
- Locked runner: commits restricted to the record file. The designated test was not run.
- Repository visibility: GitHub reports the repo as public; left unchanged for Pierce's decision.
