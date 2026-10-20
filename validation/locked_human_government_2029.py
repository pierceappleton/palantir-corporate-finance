"""Human-only locked changed-input run; launch after closing every AI tool.

The form records Pierce's own prediction in a one-file Git commit before this
program evaluates either model case. It makes no network or AI calls.
"""
import copy
import hashlib
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.model import forecast, load, value  # noqa: E402
from validation.locked_human_runner import commit_only, git  # noqa: E402

OLD_GROWTH = 0.22
NEW_GROWTH = 0.12
YEAR_INDEX = 3  # 2026, 2027, 2028, 2029, 2030


def run_experiment(answer):
    """Commit the human prediction, then compute and commit the actual result."""
    data, config = load()
    base_case = copy.deepcopy(config["cases"]["base"])
    old = base_case["government_growth"][YEAR_INDEX]
    if abs(old - OLD_GROWTH) > 1e-12:
        raise ValueError("The 2029 base government growth input changed. Stop; do not silently change the designated test.")

    now = datetime.now(timezone.utc)
    run_id = now.strftime("%Y%m%dT%H%M%S%fZ")
    folder = ROOT / "validation" / "locked" / run_id
    folder.mkdir(parents=True)
    prediction = folder / "prediction.json"
    prediction.write_text(json.dumps({
        "human_answer": answer,
        "human_attests_ai_closed": True,
        "recorded_utc": now.isoformat(),
        "input": "base-case 2029 government revenue growth",
        "input_path": "config/assumptions.json:cases.base.government_growth[3]",
        "old_value": old,
        "new_value": NEW_GROWTH,
        "units": "fraction of prior-year government revenue; 22% to 12%",
        "held_fixed": "All other growth inputs, operating margins, tax, WACC, working capital, capex, terminal convention, valuation date, share basis and reference price",
        "base_repository_commit": git("rev-parse", "HEAD"),
        "config_sha256": hashlib.sha256((ROOT / "config/assumptions.json").read_bytes()).hexdigest(),
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "output_status": "not executed at prediction precommit",
    }, indent=2), encoding="utf8")
    prediction_commit = commit_only(prediction, f"Precommit human AI-off 2029 government growth prediction {run_id}")

    before = value(forecast(base_case, data, config), base_case, data, config)
    changed_case = copy.deepcopy(base_case)
    changed_case["government_growth"][YEAR_INDEX] = NEW_GROWTH
    after = value(forecast(changed_case, data, config), changed_case, data, config)
    difference = after["per_share"] - before["per_share"]
    direction = "decrease" if difference < 0 else ("increase" if difference > 0 else "unchanged")
    result = folder / "results.json"
    result.write_text(json.dumps({
        "prediction_precommit": prediction_commit,
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "input": "base-case 2029 government revenue growth",
        "old_value": old,
        "new_value": NEW_GROWTH,
        "units": "fraction of prior-year government revenue",
        "before": before,
        "after": after,
        "per_share_change": difference,
        "actual_direction": direction,
        "decision_effect": f"{before['action']} -> {after['action']}",
        "human_comparison_status": "Pierce must compare his precommitted prediction with this result after the run",
    }, indent=2), encoding="utf8")
    result_commit = commit_only(result, f"Record AI-closed 2029 government growth result {run_id}")
    return folder, prediction_commit, result_commit, direction, difference


def main():
    import tkinter as tk
    from tkinter import messagebox, ttk

    app = tk.Tk()
    app.title("FIN439 - separate human locked input")
    app.geometry("790x670")
    frame = ttk.Frame(app, padding=20)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="Close Codex, ChatGPT, Claude and other AI tools before writing or running.", wraplength=740, font=("Segoe UI", 12, "bold")).pack(anchor="w")
    ttk.Label(frame, text="Designated change: base-case 2029 government revenue growth, 22% to 12%. All other assumptions remain fixed. No predicted result is supplied.", wraplength=740).pack(anchor="w", pady=12)
    fields = {}
    for key, label, height in [
        ("name", "Your name", 1),
        ("direction", "Your predicted direction for intrinsic value per diluted share", 2),
        ("reasoning", "Your financial reasoning before the run", 5),
        ("decision", "Your predicted effect on the investment action at $189.40, and why", 4),
    ]:
        ttk.Label(frame, text=label).pack(anchor="w")
        box = tk.Text(frame, height=height, width=84, wrap="word")
        box.pack(fill="x", pady=4)
        fields[key] = box
    attest = tk.BooleanVar(value=False)
    ttk.Checkbutton(frame, text="I wrote this prediction myself and will run with AI tools closed.", variable=attest).pack(anchor="w", pady=10)
    status = ttk.Label(frame, text="Not run. Prediction will be committed before either case is calculated.", wraplength=740)
    status.pack(anchor="w", pady=5)

    def execute():
        answer = {key: box.get("1.0", "end").strip() for key, box in fields.items()}
        if not all(answer.values()) or not attest.get():
            messagebox.showerror("Incomplete record", "Complete every field and the AI-closed attestation.")
            return
        button.config(state="disabled")
        try:
            folder, pred_commit, result_commit, direction, difference = run_experiment(answer)
            status.config(text=f"Prediction {pred_commit[:12]}; result {result_commit[:12]}; files in {folder.relative_to(ROOT)}. Actual value direction: {direction}; change: ${difference:+.4f}/share.")
            messagebox.showinfo("Records saved", "The prediction and result are in separate Git commits. Compare them in your own words, then reopen this chat and share the folder path.")
        except Exception as error:
            (ROOT / "validation" / "locked-run-error.txt").write_text(traceback.format_exc(), encoding="utf8")
            button.config(state="normal")
            messagebox.showerror("Run stopped", str(error) + "\nAn error log was saved; no successful completion is claimed.")

    button = ttk.Button(frame, text="Commit my prediction, then run", command=execute)
    button.pack(anchor="w", pady=12)
    app.mainloop()


if __name__ == "__main__":
    main()
