# Current status - October 20, 2026 (after submission)
Project 1 was submitted through Brightspace on October 19-20, 2026. The last on-time commit is `ca1ccb0` (8:49 PM EDT, October 19). Later commits are post-submission documentation cleanup only; they change no model, input or output. The work was built with AI assistance under Pierce's direction; AI use is disclosed in `docs/ai-use-record.md` and `submission/Validation-and-AI-Use.pdf`.

Post-comparison revision, Claude Code, 2026-10-20, merged to `main` by PR #1 (baseline `293ffd1`). The October 6 independent snapshot (890b973), its freeze (d248dc4), the post-comparison snapshot (7c190eb) and all manifests are unchanged.

**Current committee recommendation: do not initiate at the October 5 close of $189.40.** Model: corrected DCF range $16.66-$65.91 per diluted share (base $30.12; frozen base $29.76). Pierce adopted this action on October 20. Code corrections: cutoff cash roll-forward, capped existing-award runoff, income-statement checks. The shared engine supports a fade period; the base keeps immediate maturity.

Checks: 35 tests, 38 filing-cell checks and 12 published training outputs pass; app check passes; fresh-environment cold run on Linux recorded in validation/cold-run-2026-10-20.json. A separate AI-controlled capex sensitivity predicts and confirms a $0.1884/share decline at 2.0% capex. It has its own precommit and result and is not a human prediction.

## Done
- Videos 1-3 submitted via Brightspace (Brightspace shows 12:00 AM October 20 for the assignment due 11:59 PM October 19). Measured durations are 7:57, 5:27 and 3:20; the course limits are 3:00, 5:00 and 5:00.
- Edition A and Edition B PDFs submitted via Brightspace. Edition A is preserved unchanged at `submission/Edition A.pdf` (5 pages; SHA-256 `24087f84b272baba2eb9c6a3cb83f495c47e5e48f5270e833dd3fe3a2f4ba2b1`). Edition A states a September 1, 2026 valuation date and cites the June 30, 2026 Form 10-Q (published August 4, 2026); the current model uses an October 5, 2026 cutoff. Edition B is `submission/Edition B.pdf` (source `docs/research-evolution-edition-b.md`, which carries a dated correction note).
- First submitted Edition B used watch/defer; Pierce's later direct do-not-initiate decision is reflected in the revised package below.
- Repository is public and accessible.

## Supporting records
- `docs/ai-simulated-analyst-decisions.md`: AI-simulated analyst decision options prepared at Pierce's request. They do not alter model assumptions and are not human approval or Gate D. `submission/Analyst-Decision-Guide.pdf` (built by `src/build_analyst_decision_guide.py`) summarizes them.
- `validation/user-supplied-capex-prediction-after-ai-run-2026-10-19.md`: capex reasoning from Pierce A. & Rusheel N., timestamped 10:35 PM EDT, after the AI sensitivity ran at 8:49 PM EDT and its result had been shown. It matches the AI result's direction, approximate size and action. It is kept as a retrospective comparison only and is not a Gate D precommit.

## Open items
- Validation Gate D (human AI-off locked changed-input test, capex 1.2% to 2.0% of revenue): not run by the deadline. `validation/locked_human_runner.py` was not executed.
- Beta 1.25 is an analyst assumption without a saved provider or regression source. The peer set is narrow (only NOW and CRM have data).
- Treasury and ERP evidence: Pierce verified the October 5 10-year yield and the Damodaran ERP, but the primary Treasury source row is not saved and the exact ERP method/date evidence is limited. See `docs/source-verification-2026-10-20.md`.
- Video transcripts were not submitted.

## Resubmission preparation, October 20, 2026
Pierce requested a reworked submission and said he will conduct a separate human locked run. The current committee action is **do not initiate** at the October 5 $189.40 reference price; an earlier watch/defer interpretation in the decision log is superseded. The unchanged five-page Edition A was assembled with a dated correction, revised Edition B and A-to-B evidence map in `submission/Research-Evolution.pdf`. The two-page decision and validation PDFs were regenerated with the correct action and honest pending Gate D status. These are post-deadline revisions; no Brightspace resubmission has occurred yet.

The new human-only input is base-case 2029 government revenue growth 22% to 12%, separate from the already disclosed AI-controlled capex change. `validation/locked_human_government_2029.py` and `validation/Run-Separate-Human-Test-With-AI-Closed.cmd` prepare the precommit-before-computation sequence. **No prediction or result has been executed by the assistant.** Pierce's AI-closed instructions are in `submission/separate-human-run.md` and will be supplied in chat. After he returns the actual record, update the validation PDF and manifest. Replacement videos within 3/5/5 minutes and transcripts corrected from their audio remain outstanding; do not invent them.

## Separate human run received, October 20, 2026 at 12:49 AM EDT
Pierce and Rusheel's form attests AI was closed. The prediction was saved at 04:49:25.989 UTC and committed as `28f3017`; the result followed in commit `80546d1` at 04:49:26.365 UTC. Each commit contains only its own JSON record. The 2029 base government growth input changed from 22% to 12% while other inputs stayed fixed. Value moved $30.1183 to $29.3238 per diluted share (-$0.7944; -2.64%); do not initiate remained unchanged. The prediction's direction field reads "$33.32", but its written reasoning predicts a 3-4% decrease. Preserve that contradiction; Pierce's post-run reconciliation is recorded below and in the dated `FIELD-CORRECTION.md`. This run occurred after the first Brightspace submission.

## Pierce's post-run reconciliation, October 20
Pierce explained in chat that "$33.32" came from a rough run in a different Lab 10/11 model starting at $34.53 and was mistakenly entered in the direction field. His intended prediction was value down about 3-4%, with do-not-initiate unchanged. He attributed the smaller actual 2.64% decline to government being a smaller 2029 revenue share than his rough 50-55% assumption and to his stand-in model's single revenue line. He explicitly said he had not checked the segment figures. A separate assistant read of the saved 2029 statements gives government revenue $8,905.320M / total $19,991.245M = 44.5%, supporting that explanation. Pierce's exact statements are in `validation/locked/20261020T044925989222Z/human-review.md`; the original precommit remains in Git history, while the current `prediction.json` carries a labeled post-run field amendment. This completes the post-run comparison but does not make the run part of the original submission.

## Supplemental Brightspace submission, October 20, 2026 at 1:12 AM EDT

Pierce directed reuse of the original three videos. A supplemental Project 1 submission succeeded as Brightspace ID `23425500`; the submission-history page shows 12 files: the three videos, unchanged Edition A, original Edition B, revised Research-Evolution.pdf, Decision-Memo.pdf, Validation-and-AI-Use.pdf, three audio-derived transcripts, and Submission-Manifest.txt. The original five-file receipt `23424972` remains in history. Brightspace labels the supplemental attempt "1 hour late"; any penalty is an instructor decision. The videos exceed the 3/5/5-minute limits. The transcripts were generated from their audio with technical-term corrections and uncertain passages flagged, but Pierce has not completed a full audio review. The revised PDF identifies the human locked run as occurring after the first submission. Local receipt and screen proof are in `submission/resubmission-2026-10-20/`.
