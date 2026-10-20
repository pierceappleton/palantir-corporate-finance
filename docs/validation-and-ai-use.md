FIN439 | Pierce Appleton | AI-assisted analysis | Revised Oct 20, 2026
1
 Validation and AI use
Executed evidence and human locked run
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
Locked Changed-Input Record (Gate D) - executed after first submission
Field
Current record
Input and controls
Base 2029 government revenue growth 22% to 12% of prior-year government revenue; other inputs, cutoff, share
basis and price fixed.
Human precommit
Form names Pierce A. and Rusheel N. and attests AI closed. Prediction saved
2026-10-20T04:49:25.989222+00:00 in commit 28f301791741; result commit 80546d140046 follows it.
Prediction as entered
Direction field: '$33.32'. Written reasoning predicted value would fall by about 3-4%; action would remain do not
initiate. These statements conflict; the original precommit is unchanged.
Actual and decision
$30.1183 to $29.3238 per diluted share; $-0.7944 (-2.64%). Do not initiate before and after.
Pierce's post-run review
He says '$33.32' was mistakenly carried from a separate Lab 10/11 model with a $34.53 starting value. His
intended forecast was down 3-4%, action unchanged. He attributes the smaller 2.64% decline to a lower
government mix and a one-segment effect; saved 2029 government share is 44.5%. Original precommit
unchanged.
Earlier AI sensitivity
The Oct 19 capex 1.2% to 2.0% run was AI-authored and AI-run; it remains separate from this post-deadline
human record.
Authentic contributions and submission gaps
Ethan Heeres is credited only for the supplied Lab 11 exchanges. Pierce adopted do not initiate at $189.40 on Oct 20; this does
not approve every assumption. Brightspace received three videos and Edition A/B at 12:00 AM Oct 20 for an Oct 19 11:59 PM
deadline. The old videos exceeded their respective 3/5/5 minute limits and had no submitted transcripts. Replacement
recordings and corrected transcripts must be based on actual new audio. The human locked run and Pierce's post-run review
occurred after the first submission. Final partner review and grader-access confirmation remain open.
Text copy: docs/validation-and-ai-use.md; docs/claude-code-revision-summary.md, validation/ logs and manifests.
