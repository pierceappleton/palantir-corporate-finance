"""Prepared course-required AI-closed runner. Do not execute in an AI session.

The code contains no AI calls. The human writes the prediction; Git records it before computation.
Each commit is restricted to the single record file it writes, so unrelated staged or
modified files can never ride along with the prediction or results commit.
"""
import copy
import hashlib
import json
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.model import forecast, load, value  # noqa: E402

DESIGNATED_OLD_CAPEX = 0.012
DESIGNATED_NEW_CAPEX = 0.020


def git(*args, root=None):
    """Run a Git command in the repository and return its standard output."""
    return subprocess.check_output(["git", *args], cwd=root or ROOT, text=True).strip()


def commit_only(path, message, root=None):
    """Commit exactly one file. Refuse if anything else is already staged."""
    root = Path(root or ROOT)
    relative = Path(path).resolve().relative_to(root.resolve()).as_posix()
    staged = [name for name in git("diff", "--cached", "--name-only", root=root).splitlines() if name]
    if staged:
        raise RuntimeError(
            "Other changes are already staged (" + ", ".join(staged) + "). Unstage them first; "
            "the locked record commit must contain only its own file."
        )
    git("add", "--", relative, root=root)
    # The pathspec limits the commit to this one file.
    git("commit", "-m", message, "--only", "--", relative, root=root)
    committed = [name for name in git("show", "--name-only", "--format=", "HEAD", root=root).splitlines() if name]
    if committed != [relative]:
        raise RuntimeError(f"Commit contained {committed}, expected only {relative}")
    return git("rev-parse", "HEAD", root=root)


def run_experiment(answer):
    """Precommit the prediction, then evaluate the designated change and commit the results."""
    now = datetime.now(timezone.utc)
    run_id = now.strftime("%Y%m%dT%H%M%S%fZ")
    folder = ROOT / "validation" / "locked" / run_id
    folder.mkdir(parents=True)
    data, config = load()
    old = config["capex_ratio"]
    if abs(old - DESIGNATED_OLD_CAPEX) > 1e-12:
        raise ValueError("Base capex changed; stop and prepare a new clearly designated experiment.")
    record = dict(
        human_answer=answer,
        human_attests_ai_closed=True,
        recorded_utc=now.isoformat(),
        input="annual capex / revenue",
        old_value=old,
        new_value=DESIGNATED_NEW_CAPEX,
        units="fraction of annual revenue;1.2% to2.0%",
        base_repository_commit=git("rev-parse", "HEAD"),
        config_sha256=hashlib.sha256((ROOT / "config/assumptions.json").read_bytes()).hexdigest(),
        runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        output_status="not executed at prediction precommit",
    )
    prediction = folder / "prediction.json"
    prediction.write_text(json.dumps(record, indent=2), encoding="utf8")
    commit = commit_only(prediction, f"Precommit human AI-off locked prediction {run_id}")
    precommit_time = datetime.now(timezone.utc).isoformat()

    case = config["cases"]["base"]
    before = value(forecast(case, data, config), case, data, config)
    changed = copy.deepcopy(config)
    changed["capex_ratio"] = DESIGNATED_NEW_CAPEX
    after = value(forecast(case, data, changed), case, data, changed)
    difference = after["per_share"] - before["per_share"]
    direction = "decrease" if difference < 0 else ("increase" if difference > 0 else "unchanged")
    result = dict(
        prediction_precommit=commit,
        precommit_verified_utc=precommit_time,
        executed_utc=datetime.now(timezone.utc).isoformat(),
        before=before,
        after=after,
        per_share_change=difference,
        actual_direction=direction,
        decision_effect=f"{before['action']} -> {after['action']}",
        no_change_explanation=(
            "Action threshold was not crossed at the recorded market price."
            if before["action"] == after["action"]
            else "The changed value crossed a recorded action threshold."
        ),
        expected_reconciliation="Human review required; exact expected direction/reasoning preserved verbatim, not automatically rewritten.",
    )
    output = folder / "results.json"
    output.write_text(json.dumps(result, indent=2), encoding="utf8")
    commit_only(output, f"Record actual AI-closed locked results {run_id}")
    return commit, folder, direction, difference


def main():
    """Open the prediction form; nothing is computed until the prediction is committed."""
    import tkinter as tk
    from tkinter import messagebox, ttk

    app = tk.Tk()
    app.title("FIN439 - human prediction and AI-closed run")
    app.geometry("780x690")
    frame = ttk.Frame(app, padding=20)
    frame.pack(fill="both", expand=True)
    ttk.Label(
        frame,
        text="Close AI tools before writing this prediction and running the experiment.",
        wraplength=730,
        font=("Segoe UI", 12, "bold"),
    ).pack(anchor="w")
    ttk.Label(
        frame,
        text=(
            "Proposed input: annual capex / revenue 1.2% -> 2.0%. Revenue, operating margins, taxes, WACC and the "
            "stated terminal convention stay fixed. No expected answer is prefilled."
        ),
        wraplength=730,
    ).pack(anchor="w", pady=12)
    fields = {}
    prompts = [
        ("name", "Your name", 1),
        ("direction", "Your expected value-per-share direction, in your own words", 2),
        ("reasoning", "Your financial reasoning, written with AI closed", 5),
        ("decision", "Your expected investment-decision effect and why", 3),
    ]
    for key, label, height in prompts:
        ttk.Label(frame, text=label).pack(anchor="w")
        box = tk.Text(frame, height=height, width=85, wrap="word")
        box.pack(fill="x", pady=4)
        fields[key] = box
    attest = tk.BooleanVar(value=False)
    ttk.Checkbutton(frame, text="I wrote this prediction and am executing this run with AI tools closed.", variable=attest).pack(anchor="w", pady=10)
    status = ttk.Label(frame, text="Not run. Prediction must be committed before the model is evaluated.", wraplength=730)
    status.pack(anchor="w", pady=5)

    def execute():
        answer = {key: box.get("1.0", "end").strip() for key, box in fields.items()}
        if not all(answer.values()) or not attest.get():
            messagebox.showerror("Incomplete human record", "Complete each field and the AI-closed attestation first.")
            return
        button.config(state="disabled")
        try:
            commit, folder, direction, difference = run_experiment(answer)
            status.config(
                text=(
                    f"Saved genuine prediction at {commit[:12]} and actual results in {folder.relative_to(ROOT)}. "
                    f"Direction: {direction}; value change {difference:+.4f}/share. Local commits made; no remote push or AI call."
                )
            )
            messagebox.showinfo(
                "Record saved",
                "The prediction and actual output are preserved in separate commits. Reopen the AI session afterward "
                "to review the evidence and finish the record.",
            )
        except Exception as error:
            (ROOT / "validation" / "locked-run-error.txt").write_text(traceback.format_exc(), encoding="utf8")
            messagebox.showerror("Run stopped", str(error) + "\nExact error saved for AI troubleshooting later. No successful completion claimed.")
            button.config(state="normal")

    button = ttk.Button(frame, text="Commit my prediction, then run with AI closed", command=execute)
    button.pack(anchor="w", pady=12)
    app.mainloop()


if __name__ == "__main__":
    main()
