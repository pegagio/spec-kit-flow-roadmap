"""Merge-bounded history guards for accepted Diagram Roadmap artifacts."""

from __future__ import annotations

import subprocess
import unittest

from support import REPOSITORY_ROOT


class ProtectedHistoryTest(unittest.TestCase):
    """Keep accepted feature and released-history surfaces semantically unchanged."""

    def git_show(self, relative: str) -> str:
        result = subprocess.run(["git", "show", f"HEAD:{relative}"], cwd=REPOSITORY_ROOT, text=True, capture_output=True, check=True)
        return result.stdout

    def test_merged_feature_directories_and_reports_are_unchanged(self) -> None:
        protected = [f"specs/{number:03d}-" for number in range(1, 8)]
        result = subprocess.run(["git", "diff", "--name-only", "HEAD", "--", "specs"], cwd=REPOSITORY_ROOT, text=True, capture_output=True, check=True)
        changed = result.stdout.splitlines()
        self.assertFalse(any(any(path.startswith(prefix) for prefix in protected) for path in changed), changed)

    def test_released_changelog_is_unchanged(self) -> None:
        current = (REPOSITORY_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        baseline = self.git_show("CHANGELOG.md")
        self.assertEqual(baseline.split("## 0.1.0", 1)[1], current.split("## 0.1.0", 1)[1])

    def test_accepted_roadmap_entries_are_unchanged(self) -> None:
        current = (REPOSITORY_ROOT / ".specify" / "memory" / "roadmap.md").read_text(encoding="utf-8")
        baseline = self.git_show(".specify/memory/roadmap.md")
        current_entries = current.split("### 001", 1)[1].split("### 011", 1)[0]
        baseline_entries = baseline.split("### 001", 1)[1].split("## Open Questions", 1)[0]
        self.assertEqual(baseline_entries.rstrip(), current_entries.rstrip())


if __name__ == "__main__":
    unittest.main()
