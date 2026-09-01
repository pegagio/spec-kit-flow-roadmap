"""Contract tests for Diagram Roadmap command definitions."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

from support import REPOSITORY_ROOT


COMMANDS = {
    "write": REPOSITORY_ROOT / "commands" / "speckit.diagram-roadmap.write.md",
    "brief": REPOSITORY_ROOT / "commands" / "speckit.diagram-roadmap.brief.md",
    "debrief": REPOSITORY_ROOT / "commands" / "speckit.diagram-roadmap.debrief.md",
    "sync": REPOSITORY_ROOT / "commands" / "speckit.diagram-roadmap.sync.md",
}


class CommandContractTest(unittest.TestCase):
    """Verify current command metadata and access-time validation instructions."""

    def test_each_command_declares_one_python_script(self) -> None:
        for name, path in COMMANDS.items():
            with self.subTest(command=name):
                text = path.read_text(encoding="utf-8")
                frontmatter = text.split("---", 2)[1]
                self.assertEqual(
                    1,
                    frontmatter.count(
                        "py: .specify/extensions/diagram-roadmap/scripts/python/load_config.py"
                    ),
                )
                self.assertNotRegex(frontmatter, r"(?m)^\s+(?:sh|ps):")

    def test_commands_use_no_shell_runtime_instructions(self) -> None:
        for name, path in COMMANDS.items():
            with self.subTest(command=name):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("scripts/bash", text)
                self.assertNotIn("scripts/powershell", text)
                self.assertNotIn("platform-specific", text)

    def test_brief_and_debrief_use_python_core_prerequisites(self) -> None:
        expected = ".specify/scripts/python/check_prerequisites.py --json --paths-only"
        for name in ("brief", "debrief"):
            with self.subTest(command=name):
                self.assertIn(expected, COMMANDS[name].read_text(encoding="utf-8"))

    def test_write_requires_all_access_validation_kinds(self) -> None:
        text = COMMANDS["write"].read_text(encoding="utf-8")
        for kind in ("roadmap-read", "roadmap-write", "adr", "prd"):
            with self.subTest(kind=kind):
                self.assertIn(f"--validate-path {kind}", text)
        self.assertIn("immediately before", text)

    def test_review_commands_validate_roadmap_before_reading(self) -> None:
        for name in ("brief", "debrief", "sync"):
            with self.subTest(command=name):
                text = COMMANDS[name].read_text(encoding="utf-8")
                self.assertIn("--validate-path roadmap-read", text)
                self.assertIn("immediately before", text)

    def test_commands_that_read_adrs_validate_the_directory(self) -> None:
        for name in ("write", "brief", "debrief", "sync"):
            with self.subTest(command=name):
                text = COMMANDS[name].read_text(encoding="utf-8")
                self.assertIn("--validate-path adr", text)


if __name__ == "__main__":
    unittest.main()
