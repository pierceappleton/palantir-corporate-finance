"""Compare regenerated numeric outputs with the copies committed at a Git reference.

Used to prove that a formatting or configuration refactor changed no number.
Usage: python validation/compare_outputs.py <git-ref> [tolerance]
Exits 1 and lists every difference when any numeric cell or JSON value differs.
"""
import csv
import io
import json
import subprocess
import sys
from pathlib import Path

NUMERIC_FILES = [
    "outputs/base_three_statements.csv",
    "outputs/low_three_statements.csv",
    "outputs/high_three_statements.csv",
    "outputs/wacc_growth.csv",
    "outputs/named_stresses.csv",
    "outputs/one_at_a_time.csv",
    "outputs/equal_proportional_sensitivity.csv",
    "outputs/peer_multiples.csv",
    "outputs/relative_valuation.csv",
    "outputs/results.json",
]
IGNORED_KEYS = {"created_utc"}


def committed_text(ref, path):
    """Return a file's text as committed at the reference."""
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True, encoding="utf8")


def as_number(value):
    """Return a float for numeric text, otherwise None."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def compare_values(old, new, location, tolerance, differences):
    """Recursively compare JSON-like values and record differences."""
    if isinstance(old, dict) and isinstance(new, dict):
        for key in sorted(set(old) | set(new)):
            if key in IGNORED_KEYS:
                continue
            if key not in old or key not in new:
                differences.append(f"{location}.{key}: present in only one version")
                continue
            compare_values(old[key], new[key], f"{location}.{key}", tolerance, differences)
        return
    if isinstance(old, list) and isinstance(new, list):
        if len(old) != len(new):
            differences.append(f"{location}: length {len(old)} -> {len(new)}")
            return
        for index, (left, right) in enumerate(zip(old, new)):
            compare_values(left, right, f"{location}[{index}]", tolerance, differences)
        return
    old_number, new_number = as_number(old), as_number(new)
    if old_number is not None and new_number is not None and not isinstance(old, bool):
        if abs(old_number - new_number) > tolerance:
            differences.append(f"{location}: {old} -> {new}")
    elif old != new:
        differences.append(f"{location}: {old!r} -> {new!r}")


def read_csv(text):
    """Parse CSV text into a list of row dictionaries."""
    return list(csv.DictReader(io.StringIO(text)))


def main():
    ref = sys.argv[1]
    tolerance = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-9
    differences = []
    for path in NUMERIC_FILES:
        old_text = committed_text(ref, path)
        new_text = Path(path).read_text(encoding="utf8")
        if path.endswith(".json"):
            compare_values(json.loads(old_text), json.loads(new_text), path, tolerance, differences)
        else:
            compare_values(read_csv(old_text), read_csv(new_text), path, tolerance, differences)
    if differences:
        print(f"{len(differences)} differences against {ref}:")
        print("\n".join(differences))
        sys.exit(1)
    print(f"No numeric differences against {ref} in {len(NUMERIC_FILES)} files (tolerance {tolerance}).")


if __name__ == "__main__":
    main()
