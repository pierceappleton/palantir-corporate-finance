# Proposed recording scripts (drafts)
Post-comparison revision, Claude Code, 2026-10-20. These are AI-written drafts, not statements Pierce has recorded or accepted. Final narration must reflect his own judgment. Limits: Video 1 ≤ 3:00, Video 2 ≤ 5:00, Video 3 ≤ 5:00 (official checklist).

## Video 1 — research evolution (≤ 3:00)
Screen: Edition A (the unchanged official PDF once supplied), Edition B working draft, `docs/valuation-bridge-2026-10-20.md`, `docs/source-verification-2026-10-20.md`.
Draft: Edition A was submitted before any AI work and is unchanged. Name the consequential change and its driver (course instruction, own analysis, peer challenge, AI, or a mix). Show one AI output and the check on it. Example: the audit found that 97 days of cash between June 30 and October 5 were counted nowhere; the fix was verified by reconciling stub cash to FCFF plus after-tax interest. Another: the 47% margin was confirmed as GAAP from the 10-Q income statement. Insert your own reflections and attributed partner feedback only after they exist.

## Video 2 — code and validation (≤ 5:00)
Screen: README commands, `src/model.py` (statements, cutoff cash, award runoff), `src/dcf.py` (staged engine), the test run, the cold-run log.
Draft: One command (`python -m src.reproduce`) checks 38 filing cells and the 12 published training outputs, runs the test suite (34 tests on 2026-10-20), and regenerates every output. The Oct 20 fresh-environment cold run log is in `validation/`. The training-case reconciliation passes. Checks fail loudly: balance sheet, cash tie, income-statement identities, stub cash counted once, award expense capped, WACC above growth. These are software checks, not proof of judgment. Show the locked test's precommit and result only after you have run it with AI closed.

## Video 3 — committee defense (≤ 5:00; opens with the live demo)
Opening demo (first minute): in the Streamlit workbench, move one bounded driver, read the value, reset to base, then set mature ROIC below growth to show the red failure and recover with Reset.
Draft: The conditional recommendation is not to initiate at $189.40 under this model. Read the current range from `outputs/results.json` (about $17 to $66, base about $30). Terminal value is most of enterprise value; show the 0/5/10-year fade table. Even the high case with a 10-year fade stays below the price. Read the "what the price implies" sentences. Peers and the DCF disagree for stated reasons and are not averaged. State what would reverse the call. Insert your actual decisions on fade length, beta, peers and the final label.
