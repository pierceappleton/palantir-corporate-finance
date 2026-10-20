"""The locked-test runner may commit only its own record file (the runner itself is never launched here)."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from validation.locked_human_runner import commit_only

ROOT = Path(__file__).resolve().parents[1]


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


class LockedRunnerCommitTests(unittest.TestCase):
    def setUp(self):
        temp_root = ROOT / "tmp"
        temp_root.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="locked-runner-", dir=temp_root)
        self.root = Path(self.temp.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "test@example.invalid")
        git(self.root, "config", "user.name", "Test")
        (self.root / "unrelated.txt").write_text("original\n")
        git(self.root, "add", "unrelated.txt")
        git(self.root, "commit", "-qm", "initial")

    def tearDown(self):
        self.temp.cleanup()

    def test_refuses_when_other_changes_are_staged(self):
        (self.root / "unrelated.txt").write_text("staged edit\n")
        git(self.root, "add", "unrelated.txt")
        record = self.root / "prediction.json"
        record.write_text("{}")
        with self.assertRaises(RuntimeError):
            commit_only(record, "prediction", root=self.root)
        self.assertEqual(git(self.root, "rev-list", "--count", "HEAD"), "1")

    def test_commits_only_the_record_when_other_files_are_modified(self):
        (self.root / "unrelated.txt").write_text("unstaged edit\n")
        record = self.root / "prediction.json"
        record.write_text("{}")
        commit_only(record, "prediction", root=self.root)
        self.assertEqual(git(self.root, "show", "--name-only", "--format=", "HEAD"), "prediction.json")
        self.assertIn("unrelated.txt", git(self.root, "status", "--porcelain"))


if __name__ == "__main__":
    unittest.main()
