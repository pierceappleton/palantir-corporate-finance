# Claude Code revision summary (post-comparison revision, Claude Code, 2026-10-20)

Branch `claude/post-comparison-revisions`, starting from `7c190eb`. These revisions are **not** part of the October 6 independent freeze. Commits 890b973, d248dc4 and 7c190eb and their manifests are unchanged; nothing under `data/reference/` was touched. The designated locked capex test was **not** run.

## Result in one paragraph
Only code corrections were adopted. They raise the frozen values slightly: low $16.45 → $16.66, base $29.76 → $30.12, high $65.48 → $65.91. **The recommendation is unchanged: do not initiate at $189.40.** No case comes close to the price, including every assumption option shown. The largest is the high case with a 10-year fade at $139.49, still below the price by more than the 20% threshold. The call does not change, and the range does not overlap the price.

## Changes, labelled
| # | Change | Type | Per-share effect (base) |
|---|---|---|---|
| 1 | Readability reformat of src/, app/, tests/, validation/*.py | Formatting | none (proved: no numeric difference vs 7c190eb) |
| 2 | Hardcoded day counts, stress paths, $20 conditional price, 0.35 fade margin, thresholds moved to config | Refactor | none (proved) |
| 3 | Locked runner commits only its own record file; refuses if anything else is staged | Code correction (process) | none |
| 4 | Cutoff cash: June 30 cash rolled to Oct 5 by stub retained cash ($856M = FCFF $799M + after-tax interest $56M + financing $0) | **Code correction** | +$0.33 |
| 5 | Existing-award runoff: capped straight-line schedule; RSUs to June 2029; options use filed 4y10m21d | **Code correction** | +$0.03 |
| 6 | Income-statement identity checks; operating/book/cash tax lines; award adjustment shown as its own line with an explanation | Code correction (checks/presentation) | none |
| 7 | Shared fade engine (0/5/10 years reported; base stays 0); duplicate math in report.py removed | Engine | none at base_years 0 |
| 8 | Margin history from filings; NOL sensitivity; readable reverse DCF; PLTR normalized P/E | Evidence/diagnostics | none (not adopted) |
| 9 | Revised peer rule (dated copy; original preserved), "not meaningful" P/E marking, growth diagnostic | Policy (data pending) | none |
| 10 | Generators fixed (UTF-8, Edition A wording, Mac/Linux commands, visibility note), data-driven PDFs, .gitattributes, stale claims fixed | Presentation | none |

## Old-to-new bridge (USD per diluted share)
| Case | Frozen Oct 6 | + cutoff cash | + award runoff | Corrected | Option: 5-yr fade | Option: 10-yr fade |
|---|---:|---:|---:|---:|---:|---:|
| Low | 16.45 | 16.63 | 16.66 | **16.66** | 18.17 | 19.61 |
| Base | 29.76 | 30.09 | 30.12 | **30.12** | 35.67 | 42.04 |
| High | 65.48 | 65.88 | 65.91 | **65.91** | 94.96 | 139.49 |

Other options (base, each alone, not adopted): flat 2026 margin $30.55; NOL 50%/100% usable $30.49/$30.83; hypothetical beta 1.00/1.50/2.00 gives $34.26/$26.98/$22.54. Full tables: `docs/valuation-bridge-2026-10-20.md`.

## Commands actually run (Linux cloud container, Python 3.13.16)
- Baseline: fresh venv, `pip install -r requirements.txt`, `pytest -q` (15 passed), `python -m src.reproduce`. Outputs matched except timestamps and line endings (`validation/claude-code-baseline-2026-10-19.txt`).
- After each refactor: `python -m src.reproduce` + `python validation/compare_outputs.py 7c190eb` → no numeric differences.
- Final: `pytest -q` → 34 passed; `src.reproduce` → 38 source-cell checks and 12 training outputs pass; `validation/check_app.py` → PASS; `src.build_submission_pdfs` → both PDFs 2 pages; memo page 1 checked visually.
- Cold run: fresh `git clone` of the branch plus a fresh venv, `python validation/fresh_cold_run.py`: all 7 commands exit 0, 2026-10-20 00:18:52 to 00:19:59 UTC (`validation/cold-run-2026-10-20.json`). Its outputs show no numeric difference from the committed outputs.
- Not run: the readiness checker (the ChatGPT Oct 15 bundle was not supplied), the locked test, any push (see below).

## Verification status
Verified from saved filings: GAAP margins (Q2 2026 47.1%), cash instrument mix (realized yield ~3.5% vs 3.0% assumption), share bridge (June 30 count; the July 27 cover differs by 0.161M shares), NOL facts, and that the low tax rate is not a one-time item. **Pending** because the session's network blocked the hosts: Treasury 10-year on Oct 5, the Damodaran ERP date, a sourced beta, and wider peer data. Details and refresh steps: `docs/source-verification-2026-10-20.md`.

Update after this summary: Pierce subsequently reported checking the Oct 5 10-year yield and Oct 1 Damodaran ERP; the report and remaining evidence qualifications are recorded in `docs/source-verification-2026-10-20.md` and commit `6380cd6`.

## Remaining human items
Repository visibility; base fade length and margin path; beta; final peer list; NOL adoption; final label (do not initiate vs. watch/defer); deadline and possible Q3 refresh; AI-off locked prediction and AI-closed run; final partner review; three recordings and transcripts; unchanged Edition A PDF; rubric and grader access. Not submission-ready.

## Push status
The post-comparison branch was pushed to `pierceappleton/palantir-corporate-finance` at commit `6380cd6` and merged to `main` by PR #1. Later AI capex sensitivity follow-up commits are recorded on `main` separately.
