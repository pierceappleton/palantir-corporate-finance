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
- 2026-10-20: Pierce supplied `Edition A.pdf` from Downloads. Copied unchanged to `submission/Edition A.pdf`, five pages, SHA-256 `24087f84b272baba2eb9c6a3cb83f495c47e5e48f5270e833dd3fe3a2f4ba2b1`. It records a September 1 valuation date while citing a June 30 10-Q filed August 4; discrepancy disclosed, not silently corrected. The independent freeze predates this document.
- 2026-10-20: Created `docs/ai-simulated-analyst-decisions.md` at Pierce's request. It proposes provisional choices but does not alter config/model inputs, does not claim human approval, and is not Validation Gate D. Created `submission/human-gate-inputs.md` with the human prediction/run order and copy/paste templates.

## Pierce's committee action, 2026-10-20
In this conversation, Pierce explicitly answered, "I adopt do not initiate," for PLTR at the model's October 5 reference price of $189.40. This is Pierce's adoption of the committee action on October 20, not a claim that he authored the model, approved every assumption, or completed the required AI-off locked changed-input record. The existing source and valuation limitations remain disclosed.

## Post-submission corrections and cleanup, 2026-10-20
- 2026-10-20: correction. The 2026-10-20 Edition A entry above, the Edition B PDF and several status files said Edition A's September 1, 2026 valuation date predates its cited 10-Q. That was backwards: the June 30, 2026 Form 10-Q was published August 4, 2026, before September 1, so Edition A's date and source are consistent. The current model uses an October 5, 2026 cutoff. Corrected in docs/research-evolution-edition-b.md, docs/STATUS.md, docs/submission-compliance.md, docs/ai-use-record.md (appended note) and the Validation-and-AI-Use.pdf generator. `submission/Edition B.pdf` is preserved unchanged as submitted.
- 2026-10-20: post-submission documentation cleanup; no model, input, or output changes; last on-time commit ca1ccb0.
- 2026-10-20: final committee label, as stated by Pierce for the post-submission record: watch/defer with no initial position at the October 5 close of $189.40, matching the adopted Edition B. This is consistent with the "I adopt do not initiate" entry above: the model's price action is not to initiate at $189.40, and the portfolio keeps the name on watch. No position is taken either way.

## Superseding decision and resubmission preparation, 2026-10-20
The preceding watch/defer interpretation is superseded. Pierce's direct answer was "I adopt do not initiate" at $189.40. The revised memo and Edition B use **do not initiate** as the committee action. Monitoring reversal evidence does not change the action label. This is a post-submission revision and was not in the first Brightspace submission. A separate 2029 government-growth changed-input run is prepared for Pierce with AI closed; its prediction and result are not yet recorded.

2026-10-20 post-run Gate D comparison: Pierce supplied in chat that the "$33.32" prediction field was a mistaken value from the separate Lab 10/11 model (base $34.53). His intended pre-run narrative was a 3-4% decline and unchanged do-not-initiate action. He attributed the smaller actual 2.64% decline to government being less than the assumed 50-55% of 2029 revenue and to using a single-line stand-in model. Saved 2029 statements show 44.5% government share. Exact human wording is preserved in `validation/locked/20261020T044925989222Z/human-review.md`; the original precommit is unchanged and its conflicting field remains disclosed.
