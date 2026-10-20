"""Reproduce the AI-controlled capex sensitivity; this does not satisfy human Gate D."""
import copy
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.model import forecast, load, value

PRECOMMIT = ROOT / "validation" / "ai-capex-precommit-2026-10-19.md"
OUTPUT = ROOT / "validation" / "ai-capex-sensitivity-2026-10-19.json"
NEW_CAPEX_RATIO = 0.020


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    os.chdir(ROOT)
    if not PRECOMMIT.is_file():
        raise FileNotFoundError(f"Missing AI prediction precommit: {PRECOMMIT}")
    precommit = git("log", "-1", "--format=%H", "--", PRECOMMIT.relative_to(ROOT).as_posix())
    git("merge-base", "--is-ancestor", precommit, "HEAD")

    data, config = load()
    old_ratio = float(config["capex_ratio"])
    if abs(old_ratio - 0.012) > 1e-12:
        raise ValueError(f"Expected 1.2% base capex; found {old_ratio:.4%}; stop and reassess the experiment.")

    case = copy.deepcopy(config["cases"]["base"])
    base_rows = forecast(case, data, config)
    base_value = value(base_rows, case, data, config)

    changed_config = copy.deepcopy(config)
    changed_config["capex_ratio"] = NEW_CAPEX_RATIO
    changed_rows = forecast(case, data, changed_config)
    changed_value = value(changed_rows, case, data, changed_config)

    annual = []
    for base, changed in zip(base_rows, changed_rows):
        annual.append(
            {
                "year": int(base["year"]),
                "base_capex": base["capex"],
                "changed_capex": changed["capex"],
                "base_fcff": base["fcff"],
                "changed_fcff": changed["fcff"],
                "base_balance_check_pass": abs(base["balance_residual"]) < 1e-7,
                "changed_balance_check_pass": abs(changed["balance_residual"]) < 1e-7,
                "base_cash_check_pass": abs(base["cash_residual"]) < 1e-7,
                "changed_cash_check_pass": abs(changed["cash_residual"]) < 1e-7,
            }
        )

    prediction_match = changed_value["per_share"] < base_value["per_share"]
    if not prediction_match:
        raise AssertionError("Observed per-share direction did not match the precommitted AI prediction.")
    if changed_value["action"] != base_value["action"]:
        raise AssertionError("Decision effect differs from the precommitted AI prediction; inspect the result.")
    if not all(row["changed_capex"] > row["base_capex"] and row["changed_fcff"] < row["base_fcff"] for row in annual):
        raise AssertionError("Expected capex to rise and FCFF to fall in every forecast year.")
    if not all(row[key] for row in annual for key in ("base_balance_check_pass", "changed_balance_check_pass", "base_cash_check_pass", "changed_cash_check_pass")):
        raise AssertionError("Balance-sheet or cash-flow articulation failed under the changed input.")

    payload = {
        "classification": "AI-generated controlled sensitivity; not course Validation Gate D",
        "prediction_precommit": {
            "record": PRECOMMIT.relative_to(ROOT).as_posix(),
            "recorded_utc": "2026-10-20T00:43:57Z",
            "commit": precommit,
        },
        "execution": {
            "executed_utc": datetime.now(timezone.utc).isoformat(),
            "repository_commit": git("rev-parse", "HEAD"),
            "command": "python validation/run_ai_capex_sensitivity.py",
        },
        "input": {
            "name": "annual capex / revenue",
            "old_value": old_ratio,
            "new_value": NEW_CAPEX_RATIO,
            "units": "fraction of annual revenue",
            "controls": "Base case; revenue, margins, tax, WACC, working capital, and terminal assumptions held fixed. Base config was not modified.",
        },
        "prediction": {
            "per_share_direction": "decrease",
            "decision_effect": "remain do_not_initiate at the unchanged $189.40 reference price",
            "basis": "Capex is deducted from FCFF; other operating and terminal assumptions are fixed.",
        },
        "result": {
            "base_per_share_usd": base_value["per_share"],
            "changed_per_share_usd": changed_value["per_share"],
            "per_share_change_usd": changed_value["per_share"] - base_value["per_share"],
            "base_equity_value_usd_millions": base_value["equity_value"],
            "changed_equity_value_usd_millions": changed_value["equity_value"],
            "actual_direction": "decrease",
            "prediction_match": prediction_match,
            "base_action": base_value["action"],
            "changed_action": changed_value["action"],
        },
        "annual_results_usd_millions": annual,
        "source_hashes_at_execution": {
            "config_assumptions_sha256": sha256(ROOT / "config" / "assumptions.json"),
            "src_model_sha256": sha256(ROOT / "src" / "model.py"),
        },
        "course_gate_d": "Still pending: a human-authored prediction and AI-closed run are explicitly required. This AI run is not represented as human work.",
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"AI capex sensitivity PASS: ${base_value['per_share']:.4f} -> "
        f"${changed_value['per_share']:.4f} per share "
        f"({changed_value['per_share'] - base_value['per_share']:+.4f}); "
        f"action {base_value['action']} -> {changed_value['action']}"
    )
    print(f"Record: {OUTPUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
