"""Historical one-time script: snapshot FIN439-Labs into data/reference/FIN439-Labs. Do not rerun."""
import base64
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO = "pierceappleton/FIN439-Labs"


def gh(path):
    return json.loads(subprocess.check_output(["gh", "api", path], text=True))


if __name__ == "__main__":
    commit = gh(f"repos/{REPO}/commits/main")["sha"]
    tree = gh(f"repos/{REPO}/git/trees/{commit}?recursive=1")
    root = Path("data/reference/FIN439-Labs")
    root.mkdir(parents=True, exist_ok=True)
    manifest = []
    for entry in tree["tree"]:
        if entry["type"] != "blob" or not entry["path"].endswith((".md", ".py")):
            continue
        content = base64.b64decode(gh(f"repos/{REPO}/git/blobs/{entry['sha']}")["content"])
        target = root / entry["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        manifest.append({"path": entry["path"], "blob": entry["sha"], "sha256": hashlib.sha256(content).hexdigest()})
    record = {
        "repository": REPO,
        "commit": commit,
        "snapshot_utc": datetime.now(timezone.utc).isoformat(),
        "files": manifest,
        "preservation": "Read-only reference snapshot; source repository unchanged. DOCX files not inspected.",
    }
    Path("docs/prior-work-source-manifest.json").write_text(json.dumps(record, indent=2))
    print("Snapshot", commit, "files", len(manifest))
