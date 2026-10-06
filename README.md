# Palantir corporate finance â€” FIN439
Private independent project for Pierce Appleton. Official EditionA is unchanged and uninspected. This is an AI-generated postcheckpoint analysis with pending course/human gates.

## Visible results
[Two-page committee memo](submission/Decision-Memo.pdf), [static review](outputs/review.html), [case and reverse DCF results](outputs/results.json), [base five-year statements](outputs/base_three_statements.csv), [sensitivity](outputs/wacc_growth.csv), [peer multiples](outputs/peer_multiples.csv), [named stresses](outputs/named_stresses.csv). DCF range approximately$16â€“$66; conditional do-not-initiate at October5 close$189.40. See assumptions and limitations before accepting this provisional decision.

## Setup and reproduction
Python3.14.7 was used. From repository root:
```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m src.reproduce
.venv\Scripts\python.exe -m streamlit run app/main.py
```
The reproduction command uses saved historical evidence/inputs; it does not require live prices or blocked SEC downloads. Raw retrieval scripts record actual403 failures; Palantir issuer mirrors are saved with hashes. Peer and market inputs include primary/retrieval URLs and as-of dates. No credentials are committed.

## Navigation and validation
Read PROJECT_GUIDE.md, docs/STATUS.md, docs/requirements-matrix.csv, docs/normalization.md, docs/assumption-challenges.csv, docs/source_manifest.json and validation/STATUS.md. Financial engine is in src; interface is in app. The official twelve-output training reconciliation passes. Designated locked capex change remains unexecuted: close AI tools and use validation/Run-Locked-Test-With-AI-Closed.cmd for the genuine human record; no code editing required. Supplied Lab11 partner feedback is attributed; incomplete Lab10/12 reviews and real recordings remain pending.

Official checklist and video/memo limits are now preserved under data/reference/official-course. See docs/submission-compliance.md. The 300-point rubric and Brightspace header remain unavailable. Both PDFs are working drafts; human gates and Research-Evolution.pdf are incomplete.
