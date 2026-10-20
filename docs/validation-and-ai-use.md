FIN439 | Pierce Appleton | AI-assisted analysis | Revised Oct 20, 2026
1
 Validation and AI use
Executed evidence and outstanding human gate
Independent snapshot 890b9738c802592abb4e70beb8efc21181fdfcea was frozen Oct 6, 2026 22:53:27 UTC; its manifest is
preserved. FIN439-Labs commit 2e861768 was read only after that freeze. Course snapshot 69eac1e8. Later revisions were
merged to main; they are not part of the independent freeze. User-supplied official Edition A PDF is preserved unchanged at
submission/Edition A.pdf (five pages; SHA-256 24087f84b272baba2eb9c6a3cb83f495c47e5e48f5270e833dd3fe3a2f4ba2b1).
Edition A states a September 1, 2026 valuation date and cites the June 30, 2026 10-Q (published Aug 4, before September 1);
the current model uses an Oct 5 cutoff.
Executed checks and limits
Requirement
Evidence and disposition
Published known answer
PASS: all 12 official Lab 05 DCF outputs within 0.0001, computed by the same engine.
Source integrity
38 saved-filing cell checks pass; balance and cash totals reconcile for 2025 and H1 2026; restricted cash reconciled
through the note.
Articulation and DCF
35 software tests pass: balance/cash ties, income-statement identities, stub cash counted once, award runoff capped,
fade engine timing and zero-fade equivalence, WACC > g, contamination rejection, peer P/E 'not meaningful' rule,
locked-runner commit isolation.
Cold run
Fresh-environment runs recorded Oct 6 (Windows) and Oct 20 (Linux): validation/cold-run-2026-10-20.json.
Economic challenges
Cases, WACC-growth grid, 0/5/10-year fade, readable reverse DCF, NOL sensitivity, named stresses, one-at-a-time and
proportional tests.
Source and date policy
October 5 market data; October 6 prices excluded. June 30 balances rolled to October 5 only by modeled retained cash. Pierce
verified the Oct 5 10-year Treasury yield and the Damodaran ERP outside the revision session; the saved Treasury source row
and exact ERP method evidence are limited. Beta has no saved source and the peer set is narrow. Nothing was entered from
memory.


FIN439 | Pierce Appleton | AI-assisted analysis | Revised Oct 20, 2026
2
Named material AI uses and dispositions
Oct 6, 2026: Codex (ChatGPT; model family exposed as GPT-6, exact build not exposed) wrote and ran the independent build.
Oct 20, 2026: Claude Code (Anthropic) made the post-comparison revisions after a joint Claude/ChatGPT audit; Pierce is not a
coder and did not write code.
Corrected (Claude Code, with evidence): cutoff cash gap (stub FCFF reconciliation); award runoff ended RSU expense early
and used a rounded option period (10-Q XBRL 4y10m21d); duplicate fade math with a hardcoded margin; locked runner could
commit unrelated staged files. Qualified: 47% margin confirmed GAAP from the 10-Q income statement; 1.4% tax rate is
structural (valuation allowance), not one-time. Earlier: adjusted margins rejected as economic profit; negative cash-flow clipping
rejected.
Locked Changed-Input Record (Gate D) - separate human run pending
Field
Current record
Designated new input
Base-case 2029 government revenue growth: 22% to 12% of prior-year government revenue; all other
assumptions fixed.
Human prediction / reasoning
Pending Pierce's separate AI-off pre-run prediction. Do not substitute the earlier jointly discussed capex result.
Timestamp / precommit
Pending. The new runner commits only Pierce's prediction before calculating either case.
Actual result / decision effect
Pending the AI-closed human run and Pierce's comparison. No result is claimed in this revision.
Earlier AI sensitivity
Oct 19 capex 1.2% to 2.0% was AI-authored and AI-run; it remains a separate, disclosed sensitivity, not this
human record.
Authentic contributions and submission gaps
Ethan Heeres is credited only for the supplied Lab 11 exchanges. Pierce adopted do not initiate at $189.40 on Oct 20; this does
not approve every assumption. Brightspace received three videos and Edition A/B at 12:00 AM Oct 20 for an Oct 19 11:59 PM
deadline. The old videos exceeded their respective 3/5/5 minute limits and had no submitted transcripts. Replacement
recordings and corrected transcripts must be based on actual new audio. The separate human locked run and final partner
review remain open; grader repository access is unverified.
Text copy: docs/validation-and-ai-use.md; docs/claude-code-revision-summary.md, validation/ logs and manifests.
