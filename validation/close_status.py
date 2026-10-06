from pathlib import Path
import json
from datetime import datetime,timezone
for name in ['validation/cleanup_scaffolding.py','validation/finalize_inputs.py','validation/record_provenance.py','validation/refactor_peers.py']:
 p=Path(name)
 if p.exists():p.unlink()
p=Path('validation/STATUS.md');s=p.read_text().replace('10 tests pass','12 tests pass').replace('I Clean fresh environment run: PENDING actual cold-run log.','I Clean fresh environment run: PASS. validation/cold-run.json records five successful commands in a freshly created isolated environment, completed2026-10-06T22:51:14.041047+00:00. Includes32 raw-cell checks,12 tests, model/peer/report reproduction and all interface cases. First failed dependency-pin attempt is preserved separately.');p.write_text(s)
p=Path('docs/HANDOFF.md');s=p.read_text().replace('Ten software tests pass. Raw-cell historical checks extended from28 to32.','Twelve software tests pass. Raw-cell historical checks extended from28 to32.').replace('Second fresh-environment cold run is in progress until status is explicitly updated.','Second fresh-environment cold run passed all five recorded commands, including interface verification; completed2026-10-06T22:51:14.041047+00:00.').replace('Next gates: finish cold run; preserve independent snapshot commit/timestamp/hash manifest with disclosed pending gates. Only then request Pierce\'s existing work.','Next gates: preserve independent snapshot commit/timestamp/hash manifest with disclosed pending gates, then request Pierce\'s existing work.');p.write_text(s)
p=Path('README.md');s=p.read_text().replace('$16–$66','$16–$65');p.write_text(s)
p=Path('src/report.py');s=p.read_text().replace('approximately$16–$66','approximately$16–$65');p.write_text(s)
Path('docs/STATUS.md').write_text('''# Actual status — 2026-10-06
Independent analysis ready to freeze; no prior Palantir work inspected. Private repository: https://github.com/pierceappleton/palantir-corporate-finance.

Implemented and executed: primary-source historical inputs and normalization, five-year integrated cash-replacement pro-forma, shared-forecast FCFF DCF, enterprise/equity/diluted-share bridge, causal cases, WACC-growth sensitivity, reverse DCF, peer EV/revenue and GAAP P/E, named downside and terminal-maturity challenge, static review, committee memo, Streamlit interface and reproduction command. Case DCF approximately$16–$65; conditional do-not-initiate at October5 close$189.40. Material approximations are explicitly qualified; this is not a fully course-validated investment conclusion.

32 source-row checks and12 software tests pass. Fresh isolated-environment end-to-end run and all app cases pass. First failed cold-run evidence is retained. Pending: published training-case answers, genuine human capex prediction/precommit/test, authentic partner challenges, material assumption review, actual recordings/transcripts and official checklist/rubric/deadline/limits. Recommendation-changing downside currently demonstrates a conditional future$20 entry; it does not reverse today's already-negative initiation action.

Independent freeze will record commit/timestamp/hash manifest. After freeze, request prior work and preserve it alongside official EditionA, then compare evidence/assumptions/results. No official submission-compliance claim or fabricated human contribution.
''',encoding='utf8')
# Additional narration is a draft script, never a claimed actual recording.
Path('submission/video-scripts.md').write_text('''# Proposed recording scripts — adapt to verified course limits
These are AI-written drafts, not statements Pierce has recorded or necessarily accepted. Final narration must reflect his actual judgment and experience.

## Video1 — research evolution
Screen: independent starting view, source manifest, normalization, challenge register.
Draft: The official EditionA was submitted before this AI analysis and remains unchanged. This separate view was created after the checkpoint. The initial research question asked how long growth could persist, what margins survive coherent compensation treatment, and what success the market price embeds. Source work distinguished guidance from realized revenue and cancellable deal metrics from RPO. Restricted cash required an explicit reconciliation. The model keeps recurring compensation costs and exposes growth duration and terminal maturity for challenge. Insert your actual reflections and attributed partner feedback after they exist.

## Video2 — code and validation
Screen: README commands, source-cell check results, statement tables, tests and cold-run JSON.
Draft: This repository separates the Python financial engine from the Streamlit inspection interface. One reproduction command checks source rows, runs12 tests and regenerates outputs. The first cold run caught an incomplete dependency freeze; its error is preserved. The repaired clean environment passed all five commands and every interface case. Statement balances and cash roll-forwards fail loudly; tests reject restricted-cash and thousand-unit contamination and invalid DCF boundaries. These are software checks, not proof of investment judgment. Show the genuine human precommit and designated changed-input result only after the prediction has been received and the test run. The published course-case reconciliation remains pending the actual case and answers.

## Video3 — committee defense
Screen: memo, case range, terminal dependence, sensitivity, reverse DCF, comparisons and named stresses.
Draft: The conditional recommendation is not to initiate at the October5,2026 price under this model. The approximate diluted DCF range is16–65 dollars, with material growth, capital-cost and maturity assumptions. Terminal value dominates; a delayed-maturity case challenges that convention. Revenue-based peers imply lower values while GAAP earnings multiples vary because taxes and investment gains affect denominators. I would not average those methods. To reverse the decision I need evidence of a longer profitable runway or a sufficiently lower entry price, then an updated model and committee judgment. Insert your actual strategy, partner responses and accepted assumption changes; do not claim these draft views are your original EditionA.

Demonstration: from repository root run .venv\\Scripts\\python.exe -m src.reproduce; then .venv\\Scripts\\python.exe -m streamlit run app/main.py. Show artifacts directly in GitHub for visible results. Record actual audio/video; correct transcripts against those recordings. Official durations/formats/filenames are pending supplied checklist.
''',encoding='utf8')