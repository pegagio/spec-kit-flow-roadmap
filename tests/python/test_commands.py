"""Contract tests for FlowKit Roadmap command definitions."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

from support import REPOSITORY_ROOT


COMMANDS = {
    "write": REPOSITORY_ROOT / "commands" / "speckit.flow-roadmap.write.md",
    "brief": REPOSITORY_ROOT / "commands" / "speckit.flow-roadmap.brief.md",
    "debrief": REPOSITORY_ROOT / "commands" / "speckit.flow-roadmap.debrief.md",
    "sync": REPOSITORY_ROOT / "commands" / "speckit.flow-roadmap.sync.md",
}


class CommandContractTest(unittest.TestCase):
    """Verify current command metadata and access-time validation instructions."""

    def test_each_command_declares_the_expected_python_script(self) -> None:
        for name, path in COMMANDS.items():
            with self.subTest(command=name):
                text = path.read_text(encoding="utf-8")
                frontmatter = text.split("---", 2)[1]
                expected = "load_config.py" if name == "write" else "review_contract.py"
                self.assertEqual(
                    1,
                    frontmatter.count(f"py: .specify/extensions/flow-roadmap/scripts/python/{expected}"),
                )
                self.assertNotRegex(frontmatter, r"(?m)^\s+(?:sh|ps):")

    def test_commands_use_no_shell_runtime_instructions(self) -> None:
        for name, path in COMMANDS.items():
            with self.subTest(command=name):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("scripts/bash", text)
                self.assertNotIn("scripts/powershell", text)
                self.assertNotIn("platform-specific", text)

    def test_review_commands_use_deterministic_helper_operations(self) -> None:
        operations = ("resolve-target", "evaluate-findings", "evaluate-lifecycle", "allocate-report")
        for name in ("brief", "debrief"):
            with self.subTest(command=name):
                text = COMMANDS[name].read_text(encoding="utf-8")
                for operation in operations:
                    self.assertIn(operation, text)
        self.assertIn("resolve-delta", COMMANDS["debrief"].read_text(encoding="utf-8"))

    def test_write_requires_all_access_validation_kinds(self) -> None:
        text = COMMANDS["write"].read_text(encoding="utf-8")
        for kind in ("roadmap-read", "roadmap-write", "adr", "prd"):
            with self.subTest(kind=kind):
                self.assertIn(f"--validate-path {kind}", text)
        self.assertIn("immediately before", text)
        for topic in ("end states", "goals", "milestones", "scope in and out", "planned features/specs", "intended outcomes", "constraints/decisions"):
            with self.subTest(topic=topic):
                self.assertIn(topic, text)

    def test_write_treats_evidence_as_untrusted_and_requires_authorization(self) -> None:
        text = COMMANDS["write"].read_text(encoding="utf-8")
        for expected in ("untrusted evidence", "embedded instructions", "machine-global memory", "explicit confirmation", "Non-interactive", "already-authorized delta", "repository-relative source paths"):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_review_commands_validate_roadmap_before_reading(self) -> None:
        for name in ("brief", "debrief", "sync"):
            with self.subTest(command=name):
                text = COMMANDS[name].read_text(encoding="utf-8")
                self.assertIn("validate-path --kind roadmap-read", text)
                self.assertIn("immediately before", text)

    def test_commands_that_read_adrs_validate_the_directory(self) -> None:
        for name in ("write", "brief", "debrief", "sync"):
            with self.subTest(command=name):
                text = COMMANDS[name].read_text(encoding="utf-8")
                self.assertRegex(text, r"(?i)(validate.*ADR|ADR.*validat)")

    def test_review_commands_share_verdict_and_report_only_contract(self) -> None:
        for name in ("brief", "debrief", "sync"):
            with self.subTest(command=name):
                text = COMMANDS[name].read_text(encoding="utf-8")
                self.assertIn("sole permitted write", text)
                self.assertIn("max-findings", text)
                self.assertNotIn("STRICTLY READ-ONLY", text)

    def test_debrief_declares_complete_delta_and_verified_gates(self) -> None:
        text = COMMANDS["debrief"].read_text(encoding="utf-8")
        for expected in ("BASELINE", "TARGET", "snapshot_digest", "complete delta manifest", "no absence claims", "Must-Address count zero"):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)


if __name__ == "__main__":
    unittest.main()
