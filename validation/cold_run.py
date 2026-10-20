"""Historical Windows cold-run script (October 6, 2026). Kept for provenance; it overwrites validation/cold-run.json.

Use validation/fresh_cold_run.py for new cross-platform cold runs.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path.cwd()
venv = root / ".coldvenv2"
log = []
env = dict(os.environ)
env.pop("PYTHONPATH", None)
env.pop("PYTHONHOME", None)


def execute(args):
    """Run one command, append its real output to the log and stop on failure."""
    started = datetime.now(timezone.utc).isoformat()
    print("Running", args, flush=True)
    result = subprocess.run(args, cwd=root, env=env, text=True, capture_output=True)
    log.append(
        dict(
            started_utc=started,
            completed_utc=datetime.now(timezone.utc).isoformat(),
            command=args,
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )
    )
    Path("validation/cold-run.json").write_text(json.dumps(log, indent=2), encoding="utf8")
    print("Exit", result.returncode, flush=True)
    if result.returncode:
        raise RuntimeError("Cold run failed; inspect saved real log")


if __name__ == "__main__":
    execute([sys.executable, "-m", "venv", str(venv)])
    python = str(venv / "Scripts/python.exe")
    execute([python, "-m", "pip", "install", "-r", "requirements.txt"])
    execute([python, "-m", "pip", "freeze"])
    execute([python, "-m", "src.reproduce"])
    execute([python, "validation/check_app.py"])
    print("Fresh isolated environment cold run complete", flush=True)
