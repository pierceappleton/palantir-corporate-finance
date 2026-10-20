# AI-controlled capex sensitivity precommit

**Classification:** AI-generated controlled software/model sensitivity. This is not the course's human-authored, AI-off locked changed-input record and does not satisfy Validation Gate D.

- Prediction recorded: 2026-10-20T00:43:57Z (2026-10-19 8:43:57 PM America/Indianapolis)
- Base repository commit: `293ffd1f174195e61829ab1051c7f386583c63b3`
- Base `config/assumptions.json` SHA-256: `800C5C9441EF331812A2FB1B2862662F6E7587F4CA960804F52372F79225BE3A`
- Base `src/model.py` SHA-256: `7EE5F5CF0E346007CD3E7593CC2A40BF05C5713224B63D0882F34D672433C49C`
- Base `src/dcf.py` SHA-256: `03D1C3134A9923657BDAABF763621527A9BD4DD12482D257454C8F6D3D3757F3`

## Controlled change

Change annual capex / revenue from 1.2% to 2.0%, holding revenue, operating margins, tax, WACC, working capital, and terminal assumptions fixed. Compare the base case at the same valuation date and share basis. Do not change the committed base assumption.

## AI prediction, before execution

Per-share intrinsic value should decrease. The model deducts capex in FCFF in each forecast year; the higher ratio adds reinvestment without changing forecast revenue, operating margins, D&A, or terminal assumptions. The first forecast year's capex is adjusted for reported first-half capex, so the increase applies to the forecast portion after the reported amount. The higher capex should also reduce cash flow and increase ending PP&E while preserving the balance-sheet and cash-flow checks. The recommendation should remain do-not-initiate at the unchanged $189.40 reference price because the base value is far below that price; the exact value effect must be measured.

## Execution state

Not executed at this precommit. The result will be stored separately and labeled AI-generated. No claim of a human prediction or AI-closed execution will be made.
