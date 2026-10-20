"""Historical retrieval script for Palantir SEC sources; records failures (e.g. HTTP 403) honestly.

Not part of src.reproduce. Running it overwrites docs/source_manifest.json.
"""
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(".")
URLS = {
    "pltr_2025_10k.html": "https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm",
    "pltr_2026q2_release.html": "https://www.sec.gov/Archives/edgar/data/1321655/000132165526000039/a2026q2ex991pressrelease.htm",
    "pltr_submissions.json": "https://data.sec.gov/submissions/CIK0001321655.json",
    "pltr_companyfacts.json": "https://data.sec.gov/api/xbrl/companyfacts/CIK0001321655.json",
}
USER_AGENT = "Pierce Appleton academic finance research contact via github.com/pierceappleton"


def main():
    """Download each source, saving content hashes or the exact error."""
    manifest = []
    for filename, url in URLS.items():
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"})
            content = urllib.request.urlopen(request, timeout=45).read()
            (ROOT / "data/raw" / filename).write_bytes(content)
            manifest.append(
                dict(
                    file=filename,
                    url=url,
                    retrieved_utc=datetime.now(timezone.utc).isoformat(),
                    sha256=hashlib.sha256(content).hexdigest(),
                    bytes=len(content),
                )
            )
            print(filename, len(content))
        except Exception as error:
            print(filename, type(error).__name__, str(error))
            manifest.append(dict(file=filename, url=url, error=str(error)))
    (ROOT / "docs/source_manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
