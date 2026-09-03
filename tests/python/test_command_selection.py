"""Maintained command-selection contract fixtures."""

from __future__ import annotations

import json
import unittest

from support import REPOSITORY_ROOT


class CommandSelectionTest(unittest.TestCase):
    """Verify each workflow has positive and adjacent-negative fixtures."""

    def test_each_command_has_positive_and_negative_examples(self) -> None:
        fixtures = json.loads((REPOSITORY_ROOT / "tests" / "fixtures" / "command-selection.json").read_text(encoding="utf-8"))
        for command in ("write", "brief", "debrief", "sync"):
            with self.subTest(command=command):
                self.assertTrue(any(item.get("expected") == command for item in fixtures))
                self.assertTrue(any(item.get("excluded") == command for item in fixtures))

    def test_descriptions_front_load_use_and_non_goal(self) -> None:
        for command in ("write", "brief", "debrief", "sync"):
            with self.subTest(command=command):
                path = REPOSITORY_ROOT / "commands" / f"speckit.diagram-roadmap.{command}.md"
                description = path.read_text(encoding="utf-8").splitlines()[1]
                self.assertIn("description:", description)
                self.assertRegex(description, r"(?i)(do not|not for)")


if __name__ == "__main__":
    unittest.main()
