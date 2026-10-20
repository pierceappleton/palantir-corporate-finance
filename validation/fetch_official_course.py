"""Historical one-time script: snapshot official course files into data/reference/official-course. Do not rerun."""
import base64
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO = "CinderZhang/FIN43900-Fall2026"
LESSONS = [
    "PROJECT-SUBMISSION-ARCHITECTURE.md",
    "lessons/week-03/lab-05-dcf-build.md",
    "lessons/week-03/teach-dcf-worked-example.md",
    "lessons/week-05/lab-10-proforma-your-company.md",
    "lessons/week-06/lab-11-proforma-what-if.md",
    "lessons/week-06/lab-12-proforma-present.md",
]


def gh(path):
    return json.loads(subprocess.check_output(["gh", "api", path], text=True, encoding="utf8"))


def wanted(entry):
    path = entry["path"]
    project_file = path.startswith("projects/") and path.endswith((".md", ".csv", ".txt"))
    return entry["type"] == "blob" and (project_file or path in LESSONS or "rubric" in path.lower())


if __name__ == "__main__":
    sha = gh(f"repos/{REPO}/commits/HEAD")["sha"]
    tree = gh(f"repos/{REPO}/git/trees/{sha}?recursive=1")
    root = Path("data/reference/official-course")
    manifest = []
    for entry in [x for x in tree["tree"] if wanted(x)]:
        content = base64.b64decode(gh(f"repos/{REPO}/git/blobs/{entry['sha']}")["content"])
        target = root / entry["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        manifest.append({"path": entry["path"], "blob": entry["sha"], "sha256": hashlib.sha256(content).hexdigest()})
    record = {"repo": REPO, "commit": sha, "retrieved_utc": datetime.now(timezone.utc).isoformat(), "files": manifest}
    Path("docs/course-source-manifest.json").write_text(json.dumps(record, indent=2))
    print("Official snapshot", sha, len(manifest))
