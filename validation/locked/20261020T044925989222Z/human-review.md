# Pierce's post-run comparison

**Provenance:** Pierce supplied the statements below in this chat on October 20, 2026, after the AI-closed model run. This review is a post-run explanation; it was not in the pre-run prediction commit and is not represented as AI-off writing. The original precommit remains in Git history; the current `prediction.json` carries a labeled post-run field amendment.

## Pierce's explanation of the prediction field

> $33.32 came from my rough stand-in run in a different model, the repo’s Lab 10/11 model, which starts at $34.53, not your $30.1183. Putting it in the field was a mistake, and it shouldn’t be compared with your $29.3238. My actual prediction was: value down by about 3–4%, with do-not-initiate unchanged.

## Pierce's explanation of the smaller actual decline

> The decline was probably smaller because government is a smaller share of 2029 revenue in your model than the roughly 50–55% I assumed. Commercial likely grows faster through 2029, so a 10-point cut in government growth moves total revenue, and therefore cash flow and terminal value, less than I expected. My estimate also came from a stand-in model with a single revenue line and its own growth path, which tends to overstate the effect of a change to one segment. This is my best explanation; I haven’t checked it against your model’s segment numbers.

## Result and separate model check

The precommitted narrative predicted a decrease of about 3–4% and an unchanged do-not-initiate action. The actual result was $30.1183 to $29.3238 per diluted share, a $0.7944 (2.64%) decrease, with do-not-initiate unchanged. The direction and action matched; the magnitude was slightly smaller than Pierce's rough range. The direction field itself contained "$33.32", which is inconsistent with the precommitted narrative. At Pierce's request, the current file corrects that field with an explicit post-run amendment; the original entry remains in commit `28f3017`.

After Pierce supplied the explanation, the assistant read the saved `outputs/base_three_statements.csv` row for 2029: government revenue $8,905.320 million / total revenue $19,991.245 million = about 44.5%. This supports Pierce's proposed segment-share explanation; it was not a check Pierce claimed to have performed before or during the run. The separate AI-controlled October 19 capex sensitivity remains a different record.
