# Post-run correction to prediction direction field

**Recorded after the October 20, 2026 locked run.** This notice does not amend the human AI-off prediction committed as `28f3017` or claim to have been written before the run.

The original `prediction.json` at precommit `28f3017` has direction `$33.32`. Pierce explained that this number came from a rough stand-in run in a different Lab 10/11 model starting at $34.53 and was entered here by mistake. It is not a prediction to compare against this model's $30.1183 baseline or $29.3238 changed-input result. At Pierce's request, the current working copy's `direction` field now states his intended 3–4% decrease and includes a `post_run_amendment` object. The committed pre-run version remains available in Git history.

The precommitted written reasoning predicted **value down about 3–4%**, with **do not initiate unchanged**. The actual result was **down 2.64%** ($30.1183 to $29.3238 per diluted share), with the action unchanged. Thus the written direction and action matched; the estimated decline was slightly larger than observed. Pierce's verbatim explanation and proposed reason are preserved in `human-review.md`.

This is a post-run correction of a mistaken field, not a replacement pre-run prediction.
