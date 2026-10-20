# Palantir corporate finance - FIN439
Project for Pierce Appleton (Purdue, Finance and Accounting). AI-generated post-checkpoint analysis with pending course and human gates.

**Edition A.** The official Edition A submitted through Brightspace is unchanged and is not in this repository. A repository copy of Pierce's Edition A draft (`data/reference/FIN439-Labs/labs/lab-03/Project1_EditionA_Palantir.md`) was read after the October 6 independent freeze, as part of the prior-work comparison. It is not assumed identical to the submitted PDF.

**Repository visibility.** The project plan called for a private repository, but on 2026-10-20 GitHub reported this repository as public. Pierce decides whether to change that, because it affects grader access. Making it private later does not undo copies already made while it was public.

## Visible results
[Working memo](submission/current-model-memo.md), [static review page](outputs/review.html), [results and checks](outputs/results.json), [valuation bridge](docs/valuation-bridge-2026-10-20.md), [terminal conventions](outputs/terminal_conventions.csv), [base five-year statements](outputs/base_three_statements.csv), [WACC-growth sensitivity](outputs/wacc_growth.csv), [peer multiples](outputs/peer_multiples.csv), [named stresses](outputs/named_stresses.csv), [Claude Code revision summary](docs/claude-code-revision-summary.md). The two-page PDFs in `submission/` are working drafts.

DCF range about $17-$66 per diluted share (base $30.12); conditional do-not-initiate at the October 5 close of $189.40. Read the assumptions, the pending verifications and the limitations before relying on this provisional decision.

## Setup and reproduction
Tested with Python 3.14.7 (Windows, October 6) and Python 3.13 (Linux, October 20). Run from the repository root.

Windows (PowerShell or Command Prompt):
```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m src.reproduce
.venv\Scripts\python.exe -m streamlit run app/main.py
```

macOS or Linux:
```
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m src.reproduce
.venv/bin/python -m streamlit run app/main.py
```

Tests alone: `python -m pytest -q`. Old-to-new bridge: `python -m validation.valuation_bridge`. Two-page PDFs: `python -m src.build_submission_pdfs`. Fresh-environment cold run: `python validation/fresh_cold_run.py`.

The reproduction command uses the saved filings and inputs; it needs no live prices or SEC downloads. Market inputs carry source URLs and as-of dates; items not yet verified are listed in `docs/source-verification-2026-10-20.md`. No credentials are committed.

## Navigation and validation
Read PROJECT_GUIDE.md, docs/STATUS.md, docs/HANDOFF.md, docs/requirements-matrix.csv, docs/normalization.md, docs/assumption-challenges.csv, docs/source_manifest.json and validation/STATUS.md. The financial engine is in `src/`; the interface is in `app/`. The AI-controlled capex sensitivity from 1.2% to 2.0% is recorded in `validation/ai-capex-sensitivity-2026-10-19.json`; it is separate from the designated human locked test, which remains pending. Pierce must write that prediction with AI closed and run `validation/locked_human_runner.py` (on Windows, `validation/Run-Locked-Test-With-AI-Closed.cmd`). The Lab 11 partner feedback supplied by Pierce is credited; the final partner review and the real recordings remain pending.

The official checklist and video/memo limits are preserved under `data/reference/official-course` (see docs/submission-compliance.md). The 300-point rubric and the Brightspace header remain unavailable. The submission is not complete.
