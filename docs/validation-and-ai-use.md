FIN439 | Pierce Appleton | AI-assisted working draft | Post-comparison revision, Claude Code, 2026-10-20
1
 Validation and AI use
Working record - human gates incomplete
Independent snapshot 890b9738c802592abb4e70beb8efc21181fdfcea was frozen Oct 6, 2026 22:53:27 UTC; its manifest is
preserved. FIN439-Labs commit 2e861768 was read only after that freeze. Course snapshot 69eac1e8. Post-comparison
revisions on Oct 20, 2026 are on branch claude/post-comparison-revisions and are not part of the independent freeze.
Executed checks and limits
 Requirement
Evidence and disposition
Published known answer
PASS: all 12 official Lab 05 DCF outputs within 0.0001, computed by the same engine.
Source integrity
38 saved-filing cell checks pass; balance and cash totals reconcile for 2025 and H1 2026; restricted cash reconciled
through the note.
Articulation and DCF
34 software tests pass: balance/cash ties, income-statement identities, stub cash counted once, award runoff capped,
fade engine timing and zero-fade equivalence, WACC > g, contamination rejection, peer P/E 'not meaningful' rule,
locked-runner commit isolation.
Cold run
Fresh-environment runs recorded Oct 6 (Windows) and Oct 20 (Linux): validation/cold-run-2026-10-20.json.
Economic challenges
Cases, WACC-growth grid, 0/5/10-year fade, readable reverse DCF, NOL sensitivity, named stresses, one-at-a-time and
proportional tests.
Source and date policy
October 5 market data; October 6 prices excluded. June 30 balances rolled to October 5 only by modeled retained cash.
Treasury yield, ERP date, beta estimate and wider peer data are pending: the revision session's network blocked those hosts,
and nothing was entered from memory.


FIN439 | Pierce Appleton | AI-assisted working draft | Post-comparison revision, Claude Code, 2026-10-20
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
Locked Changed-Input Record - NOT EXECUTED
 Field
Current record
Input and units
Annual capex / revenue: old 1.2%, new 2.0%; other drivers, tax, WACC and terminal convention fixed.
Human prediction / reasoning
PENDING Pierce's AI-off prediction. Nothing substituted.
Timestamp / precommit
PENDING. The runner commits only the prediction file before computing.
Actual result / decision effect
PENDING. Not run.
Note
The base value moved from $29.76 to the corrected value after the code corrections; the runner reads the current
model at run time.
Authentic contributions and submission gaps
Ethan Heeres is credited only for the supplied Lab 11 exchanges. Pending: the unchanged official Edition A PDF, final partner
review, three real videos (3/5/5 minutes) with corrected transcripts, grader access (repository currently public; Pierce decides),
the Brightspace deadline/header and the 300-point rubric. No final compliance claim.
Working source: docs/validation-and-ai-use.md, docs/claude-code-revision-summary.md, validation/ logs and manifests.
