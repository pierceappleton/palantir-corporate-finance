"""Cross-platform fresh-environment cold run: new venv, install, tests, reproduce, app check, PDFs.

Writes the real command log to validation/cold-run-<UTC date>.json. Usage: python validation/fresh_cold_run.py
"""
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    log = []
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = ROOT / "validation" / f"cold-run-{stamp}.json"
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    venv = Path(tempfile.mkdtemp(prefix="coldvenv-"))
    python = str(venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python"))
    commands = [
        [sys.executable, "-m", "venv", str(venv)],
        [python, "-m", "pip", "install", "-r", "requirements.txt"],
        [python, "-m", "pip", "freeze"],
        [python, "-m", "pytest", "-q"],
        [python, "-m", "src.reproduce"],
        [python, "validation/check_app.py"],
        [python, "-m", "src.build_submission_pdfs"],
    ]
    for args in commands:
        started = datetime.now(timezone.utc).isoformat()
        print("Running", args, flush=True)
        result = subprocess.run(args, cwd=ROOT, env=env, text=True, capture_output=True)
        log.append(dict(started_utc=started, completed_utc=datetime.now(timezone.utc).isoformat(), command=args, returncode=result.returncode, stdout=result.stdout[-20000:], stderr=result.stderr[-20000:]))
        out.write_text(json.dumps(dict(python=sys.version, platform=sys.platform, environment=str(venv), commands=log), indent=2), encoding="utf8")
        print("Exit", result.returncode, flush=True)
        if result.returncode:
            raise SystemExit("Cold run failed; inspect " + str(out))
    print("Fresh environment cold run complete:", out)


if __name__ == "__main__":
    main()
