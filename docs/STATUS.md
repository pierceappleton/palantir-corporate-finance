# Current status - October 20, 2026
Post-comparison revision, Claude Code, 2026-10-20, on branch `claude/post-comparison-revisions`. Not merged to main. The October 6 independent snapshot (890b973), its freeze (d248dc4), the post-comparison snapshot (7c190eb) and all manifests are unchanged.

Model: corrected DCF range $16.66-$65.91 per diluted share (base $30.12; frozen base $29.76). Action at the $189.40 October 5 close is unchanged: do not initiate. Code corrections: cutoff cash roll-forward, capped existing-award runoff, income-statement checks. The shared engine now supports a fade period; the base keeps immediate maturity until Pierce decides.

Checks: 34 tests, 38 filing-cell checks and 12 published training outputs pass; app check passes; fresh-environment cold run on Linux recorded in validation/cold-run-2026-10-20.json.

Pending verification (hosts blocked in the session): Treasury 10-year on Oct 5, Damodaran ERP date, a sourced beta, wider peer data. Pending Pierce: repository visibility (currently public), fade length and margin path, beta, peer list, NOL adoption, final label, AI-off locked test (not run), final partner review, recordings and transcripts, Edition A PDF, deadline/rubric/grader access. Not submission-ready.
