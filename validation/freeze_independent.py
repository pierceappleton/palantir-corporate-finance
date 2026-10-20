"""Historical one-time script (October 6, 2026) that wrote the independent freeze manifest. Do not rerun."""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PENDING = [
    "Published training-case reconciliation",
    "Human capex prediction/precommit/designated execution",
    "Authentic partner challenges",
    "Human material-assumption/strategy review",
    "Official rubric checklist filenames deadline and limits",
    "Original-work comparison after this freeze",
    "Real recordings and corrected transcripts",
]

if __name__ == "__main__":
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    files = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", commit], text=True).splitlines()
    records = []
    for name in files:
        committed = subprocess.check_output(["git", "show", f"{commit}:{name}"])
        path = Path(name)
        records.append(
            dict(
                path=name,
                committed_sha256=hashlib.sha256(committed).hexdigest(),
                committed_bytes=len(committed),
                worktree_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                worktree_bytes=path.stat().st_size,
            )
        )
    freeze = dict(
        frozen_utc=datetime.now(timezone.utc).isoformat(),
        analysis_commit=commit,
        repository="https://github.com/pierceappleton/palantir-corporate-finance",
        visibility="private",
        scope="Independent postcheckpoint analysis snapshot; not official EditionA and not final course submission",
        provisional_action="Do not initiate at October5,2026 regular close under recorded assumptions",
        pending=PENDING,
        files=records,
        hash_convention=(
            "SHA256 of exact committed Git blob and physical worktree separately; CRLF normalization can differ. "
            "Record itself generated after the snapshot commit; not self-hashed."
        ),
    )
    Path("validation/independent-freeze.json").write_text(json.dumps(freeze, indent=2), encoding="utf8")
    artifacts = [x for x in records if x["path"].startswith(("outputs/", "submission/", "validation/"))]
    manifest = dict(
        analysis_commit=commit,
        record_created_utc=freeze["frozen_utc"],
        status="Independent working bundle; official seven-part filenames pending",
        artifacts=artifacts,
    )
    Path("docs/final-output-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf8")
    status = Path("docs/STATUS.md")
    text = status.read_text().replace("Independent analysis ready to freeze", "Independent analysis frozen").replace(
        "Independent freeze will record commit/timestamp/hash manifest.",
        f"Independent freeze: analysis commit {commit}; UTC {freeze['frozen_utc']}; validation/independent-freeze.json and docs/final-output-manifest.json.",
    )
    status.write_text(text, encoding="utf8")
    print(json.dumps({k: v for k, v in freeze.items() if k != "files"}, indent=2))
    print("Manifest files:", len(records))
