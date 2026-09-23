"""Merge-bounded history guards for accepted FlowKit Roadmap artifacts."""

from __future__ import annotations

import subprocess
import unittest

from support import REPOSITORY_ROOT


def accepted_roadmap_entries(document: str) -> str:
    """Select the pre-feature entries whether or not HEAD contains entry 012."""
    entries = document.split("### 001", 1)[1]
    return entries.split("### 012", 1)[0].split("## Open Questions", 1)[0].rstrip()


class ProtectedHistoryTest(unittest.TestCase):
    """Keep accepted feature and released-history surfaces semantically unchanged."""

    def git_show(self, relative: str) -> str:
        result = subprocess.run(["git", "show", f"HEAD:{relative}"], cwd=REPOSITORY_ROOT, text=True, capture_output=True, check=True)
        return result.stdout

    def test_merged_feature_directories_and_reports_are_unchanged(self) -> None:
        protected = [f"specs/{number:03d}-" for number in range(1, 9)]
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
        self.assertEqual(accepted_roadmap_entries(baseline), accepted_roadmap_entries(current))

    def test_accepted_roadmap_boundary_survives_entry_012_in_head(self) -> None:
        earlier = "# Roadmap\n### 001\naccepted\n### 011\naccepted\n## Open Questions\n"
        with_entry_012 = earlier.replace("## Open Questions", "### 012\ncurrent feature\n## Open Questions")
        modified_history = with_entry_012.replace("### 011\naccepted", "### 011\nchanged")
        self.assertEqual(accepted_roadmap_entries(earlier), accepted_roadmap_entries(with_entry_012))
        self.assertNotEqual(accepted_roadmap_entries(earlier), accepted_roadmap_entries(modified_history))


if __name__ == "__main__":
    unittest.main()
