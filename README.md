# Palantir corporate finance - FIN439
Project for Pierce Appleton (Purdue, Finance and Accounting). The financial engine, source checks, valuation cases, and static outputs are reproducible. Pierce adopted the do-not-initiate action on October 20, 2026; remaining validation and submission items are disclosed below.

**Edition A.** Pierce supplied the Edition A PDF after the independent freeze; an unchanged copy is preserved at `submission/Edition A.pdf`. A separate repository draft (`data/reference/FIN439-Labs/labs/lab-03/Project1_EditionA_Palantir.md`) was read after the October 6 freeze for comparison.

**Repository visibility.** The project plan called for a private repository, but on 2026-10-20 GitHub reported this repository as public. Pierce decides whether to change that, because it affects grader access. Making it private later does not undo copies already made while it was public.

## Visible results
[Decision memo](submission/Decision-Memo.pdf), [validation and AI-use record](submission/Validation-and-AI-Use.pdf), [static review page](outputs/review.html), [results and checks](outputs/results.json), [valuation bridge](docs/valuation-bridge-2026-10-20.md), [terminal conventions](outputs/terminal_conventions.csv), [base five-year statements](outputs/base_three_statements.csv), [WACC-growth sensitivity](outputs/wacc_growth.csv), [peer multiples](outputs/peer_multiples.csv), [named stresses](outputs/named_stresses.csv). The validation PDF explicitly identifies the human locked gate as unresolved in the available record.

DCF range about $17-$66 per diluted share (base $30.12). Pierce's committee action is **do not initiate at the October 5 reference close of $189.40**. The model assumptions, source limitations, and reversal triggers are in the decision memo. This action was adopted by Pierce on October 20; it does not establish that every assumption or required validation gate is complete.

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
Read PROJECT_GUIDE.md, docs/STATUS.md, docs/HANDOFF.md, docs/requirements-matrix.csv, docs/normalization.md, docs/assumption-challenges.csv, docs/source_manifest.json and validation/STATUS.md. The financial engine is in `src/`; the interface is in `app/`. The earlier capex sensitivity was AI-controlled and is disclosed separately. A new human-only locked test has been prepared for 2029 base government revenue growth (22% to 12%); Pierce will write his prediction and run it with AI closed using `validation/Run-Separate-Human-Test-With-AI-Closed.cmd`. Instructions are in `submission/separate-human-run.md`. Its result is pending. The Lab 11 partner feedback supplied by Pierce is credited; the final partner review and replacement recordings/transcripts remain pending.

The official checklist and video/memo limits are preserved under `data/reference/official-course` (see docs/submission-compliance.md). Brightspace shows the Project 1 due time as October 19, 2026 at 11:59 PM and the analytic rubric as 300 points. The financial application is runnable. `submission/Research-Evolution.pdf` bundles the unchanged official Edition A, a dated correction, revised Edition B and an A-to-B evidence map. The separate human locked test, corrected transcripts and replacement videos remain open as detailed in `docs/STATUS.md`.
