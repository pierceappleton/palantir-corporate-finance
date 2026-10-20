# Palantir corporate finance - FIN439
Project 1 for Pierce Appleton (Purdue, Finance and Accounting), built with AI assistance under Pierce's direction. AI use is disclosed in `docs/ai-use-record.md` and `submission/Validation-and-AI-Use.pdf`. The first submission was received through Brightspace at 12:00 AM October 20, 2026; post-deadline revisions are identified separately.

**Pierce's adopted committee action: do not initiate at the October 5 close of $189.40.** DCF range about $17-$66 per diluted share (base $30.12). The range is judgment-dependent, not a statistical confidence interval; see the assumptions and limitations before relying on it.

**First submission.** Brightspace received three videos, Edition A and the original Edition B. The official Edition A PDF is preserved unchanged at `submission/Edition A.pdf`; the original Edition B remains at `submission/Edition B.pdf`. The revised `submission/Research-Evolution.pdf` combines Edition A, a dated correction, revised Edition B and an A-to-B evidence map. A repository Markdown copy of Pierce's Edition A draft (`data/reference/FIN439-Labs/labs/lab-03/Project1_EditionA_Palantir.md`) was read after the October 6 independent freeze for comparison.

**Repository visibility.** This repository was observed public on October 20. The project plan had called for a private repository; grader access if visibility changes must be checked.

## Visible results
[Decision memo](submission/Decision-Memo.pdf), [validation and AI-use record](submission/Validation-and-AI-Use.pdf), [static review page](outputs/review.html), [results and checks](outputs/results.json), [valuation bridge](docs/valuation-bridge-2026-10-20.md), [terminal conventions](outputs/terminal_conventions.csv), [base five-year statements](outputs/base_three_statements.csv), [WACC-growth sensitivity](outputs/wacc_growth.csv), [peer multiples](outputs/peer_multiples.csv), [named stresses](outputs/named_stresses.csv).

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
Read PROJECT_GUIDE.md, docs/STATUS.md, docs/HANDOFF.md, docs/requirements-matrix.csv, docs/normalization.md, docs/assumption-challenges.csv, docs/source_manifest.json and validation/STATUS.md. The financial engine is in `src/`; the interface is in `app/`. The separate human locked-run instructions are in `submission/separate-human-run.md`. The Lab 11 partner feedback supplied by Pierce is credited.

## Open items
- Validation Gate D was not completed by the original deadline. A separate 2029 government-growth run was recorded after submission in prediction commit `28f3017` and result commit `80546d1`; Pierce's post-run explanation is in `validation/locked/20261020T044925989222Z/human-review.md`. The original conflicting direction field remains unchanged. The earlier AI-controlled capex sensitivity remains separate.
- Beta is an analyst assumption without a saved provider or regression source, and the peer set is narrow.
- Treasury yield and equity risk premium evidence has limits, listed in `docs/source-verification-2026-10-20.md`.
- Replacement videos under 3/5/5 minutes and corrected transcripts are pending.

The official checklist and video/memo limits are preserved under `data/reference/official-course` (see docs/submission-compliance.md).
