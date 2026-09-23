"""Git delta tests for the FlowKit Roadmap review helper."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

from support import REPOSITORY_ROOT, SOURCE_LOADER, SOURCE_REVIEW_CONTRACT, active_specify_interpreter


class ReviewDeltaTest(unittest.TestCase):
    """Verify explicit and working-tree implementation boundaries."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.root, check=True)
        scripts = self.root / "scripts" / "python"
        scripts.mkdir(parents=True)
        shutil.copy2(SOURCE_LOADER, scripts / "load_config.py")
        shutil.copy2(SOURCE_REVIEW_CONTRACT, scripts / "review_contract.py")
        (self.root / "extension.yml").write_text("schema_version: '1.0'\nextension:\n  id: flow-roadmap\ndefaults:\n  report:\n    max_findings: 50\n", encoding="utf-8")
        self.write("tracked.txt", "one\n")
        self.commit("initial")
        self.baseline = self.git("rev-parse", "HEAD").stdout.strip()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", *arguments], cwd=self.root, text=True, capture_output=True, check=True)

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit(self, message: str) -> None:
        self.git("add", "--all")
        self.git("commit", "-q", "-m", message)

    def run_helper(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        bin_directory = Path(self.temporary.name) / "bin"
        bin_directory.mkdir(exist_ok=True)
        specify = bin_directory / "specify"
        specify.write_text(f"#!{active_specify_interpreter()}\npass\n", encoding="utf-8")
        specify.chmod(specify.stat().st_mode | stat.S_IXUSR)
        environment = {**__import__("os").environ, "PATH": f"{bin_directory}:{__import__('os').environ.get('PATH', '')}"}
        return subprocess.run([sys.executable, str(self.root / "scripts" / "python" / "review_contract.py"), *arguments], cwd=self.root, env=environment, text=True, capture_output=True, check=False)

    def output(self, result: subprocess.CompletedProcess[str]) -> dict[str, object]:
        self.assertEqual(0, result.returncode, result.stderr)
        return json.loads(result.stdout)

    def test_clean_tree_without_range_is_unavailable(self) -> None:
        output = self.output(self.run_helper("resolve-delta"))
        self.assertEqual("unavailable", output["mode"])
        self.assertFalse(output["trustworthy"])

    def test_dirty_tree_includes_tracked_and_untracked_files(self) -> None:
        self.write("tracked.txt", "two\n")
        self.write("new.txt", "new\n")
        output = self.output(self.run_helper("resolve-delta"))
        self.assertEqual("head-to-worktree", output["mode"])
        self.assertEqual(["new.txt", "tracked.txt"], [item["new_path"] for item in output["artifacts"]])

    def test_explicit_range_excludes_ambient_dirty_state(self) -> None:
        self.write("tracked.txt", "two\n")
        self.commit("feature")
        target = self.git("rev-parse", "HEAD").stdout.strip()
        self.write("ambient.txt", "dirty\n")
        output = self.output(self.run_helper("resolve-delta", "--baseline", self.baseline, "--target", target))
        self.assertEqual("explicit-commit-range", output["mode"])
        self.assertTrue(output["exclusions"])
        self.assertNotIn("ambient.txt", [item["new_path"] for item in output["artifacts"]])

    def test_baseline_to_worktree_includes_commit_and_dirty_state(self) -> None:
        self.write("tracked.txt", "two\n")
        self.commit("feature")
        self.write("untracked.txt", "dirty\n")
        output = self.output(self.run_helper("resolve-delta", "--baseline", self.baseline, "--target", "WORKTREE"))
        self.assertEqual("baseline-to-worktree", output["mode"])
        self.assertEqual(["tracked.txt", "untracked.txt"], [item["new_path"] for item in output["artifacts"]])

    def test_option_shaped_ref_is_rejected(self) -> None:
        result = self.run_helper("resolve-delta", "--baseline=-bad", "--target", "HEAD")
        self.assertEqual(1, result.returncode)
        self.assertEqual("", result.stdout)

    def test_rename_and_delete_are_classified(self) -> None:
        self.write("delete.txt", "delete\n")
        self.write("rename-old.txt", "rename\n")
        self.commit("fixtures")
        self.git("mv", "rename-old.txt", "rename-new.txt")
        (self.root / "delete.txt").unlink()
        output = self.output(self.run_helper("resolve-delta"))
        statuses = {(item["status"], item["new_path"]) for item in output["artifacts"]}
        self.assertIn(("deleted", "delete.txt"), statuses)
        self.assertIn(("renamed", "rename-new.txt"), statuses)

    def test_snapshot_digest_changes_when_content_changes(self) -> None:
        self.write("tracked.txt", "two\n")
        first = self.output(self.run_helper("resolve-delta"))
        self.write("tracked.txt", "three\n")
        second = self.output(self.run_helper("resolve-delta"))
        self.assertNotEqual(first["snapshot_digest"], second["snapshot_digest"])

    def test_changed_gitlink_is_classified(self) -> None:
        self.git("update-index", "--add", "--cacheinfo", f"160000,{self.baseline},vendor/module")
        self.git("commit", "-q", "-m", "add gitlink")
        current = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("update-index", "--cacheinfo", f"160000,{current},vendor/module")
        output = self.output(self.run_helper("resolve-delta"))
        gitlink = next(item for item in output["artifacts"] if item["new_path"] == "vendor/module")
        self.assertEqual("gitlink", gitlink["status"])
        self.assertEqual(1, output["dirty_state"]["gitlinks"])


if __name__ == "__main__":
    unittest.main()
