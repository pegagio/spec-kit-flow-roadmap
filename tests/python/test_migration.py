"""Specify CLI tests for the manual Diagram Roadmap migration."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from legacy_fixture import create_legacy_extension
from support import REPOSITORY_ROOT


class ManualMigrationTest(unittest.TestCase):
    """Verify the old installation remains recoverable until new validation passes."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.temporary_root = Path(self.temporary_directory.name)
        self.project = self.temporary_root / "project"
        self.project.mkdir()
        self.specify = shutil.which("specify")
        if self.specify is None:
            self.skipTest("Specify CLI is unavailable")

        specify_directory = self.project / ".specify"
        specify_directory.mkdir()
        for filename in ("integration.json", "init-options.json"):
            shutil.copy2(REPOSITORY_ROOT / ".specify" / filename, specify_directory / filename)

        self.old_source = self.temporary_root / "diagram-roadmap-source"
        create_legacy_extension(self.old_source)
        self.install_old = self.run_specify("extension", "add", "--dev", str(self.old_source))
        self.assert_cli_success(self.install_old)
        self.old_payload = specify_directory / "extensions" / "diagram-roadmap"
        self.old_config = self.old_payload / "roadmap-config.yml"
        self.old_config.write_text("report:\n  max_findings: 7\n", encoding="utf-8")
        self.backup = self.temporary_root / "roadmap-config.backup.yml"
        shutil.copy2(self.old_config, self.backup)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_specify(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        """Run the pinned Specify CLI in the disposable project."""
        return subprocess.run(
            [self.specify, *arguments],
            cwd=self.project,
            text=True,
            capture_output=True,
            check=False,
        )

    def assert_cli_success(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(0, result.returncode, result.stderr or result.stdout)

    def registry(self) -> dict[str, object]:
        """Read Specify's JSON registry for the disposable installation."""
        return json.loads((self.project / ".specify" / "extensions" / ".registry").read_text(encoding="utf-8"))

    def resolve_config(self, extension_id: str) -> dict[str, object]:
        """Run an installed loader and parse its public JSON result."""
        loader = self.project / ".specify" / "extensions" / extension_id / "scripts" / "python" / "load_config.py"
        result = subprocess.run(
            [str(loader)],
            cwd=self.project,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        return json.loads(result.stdout)

    def test_successful_migration_transfers_config_and_removes_old_identity(self) -> None:
        self.assertEqual(7, self.resolve_config("diagram-roadmap")["max_findings"])

        self.assert_cli_success(self.run_specify("extension", "disable", "diagram-roadmap"))
        disabled_registry = self.registry()["extensions"]
        self.assertFalse(disabled_registry["diagram-roadmap"]["enabled"])

        self.assert_cli_success(self.run_specify("extension", "add", "--dev", str(REPOSITORY_ROOT)))
        new_payload = self.project / ".specify" / "extensions" / "flow-roadmap"
        new_config = new_payload / "roadmap-config.yml"
        new_config.write_text(self.backup.read_text(encoding="utf-8"), encoding="utf-8")
        self.assertEqual(7, self.resolve_config("flow-roadmap")["max_findings"])

        registry = self.registry()["extensions"]
        self.assertFalse(registry["diagram-roadmap"]["enabled"])
        self.assertTrue(registry["flow-roadmap"]["enabled"])
        skills_directory = self.project / ".agents" / "skills"
        self.assertEqual(4, len(list(skills_directory.glob("speckit-flow-roadmap-*/SKILL.md"))))

        self.assert_cli_success(
            self.run_specify("extension", "remove", "diagram-roadmap", "--keep-config", "--force")
        )
        registry = self.registry()["extensions"]
        self.assertNotIn("diagram-roadmap", registry)
        self.assertIn("flow-roadmap", registry)
        self.assertTrue(self.old_config.is_file())
        self.assertEqual("report:\n  max_findings: 7\n", self.backup.read_text(encoding="utf-8"))
        self.assertEqual([], list(skills_directory.glob("speckit-diagram-roadmap-*/SKILL.md")))

    def test_failed_new_config_validation_keeps_old_installation_and_backup(self) -> None:
        self.assert_cli_success(self.run_specify("extension", "disable", "diagram-roadmap"))
        self.assert_cli_success(self.run_specify("extension", "add", "--dev", str(REPOSITORY_ROOT)))

        new_config = self.project / ".specify" / "extensions" / "flow-roadmap" / "roadmap-config.yml"
        new_config.write_text("unknown:\n  value: true\n", encoding="utf-8")
        loader = self.project / ".specify" / "extensions" / "flow-roadmap" / "scripts" / "python" / "load_config.py"
        validation = subprocess.run(
            [str(loader)],
            cwd=self.project,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(0, validation.returncode)

        registry = self.registry()["extensions"]
        self.assertIn("diagram-roadmap", registry)
        self.assertFalse(registry["diagram-roadmap"]["enabled"])
        self.assertTrue(self.old_config.is_file())
        self.assertEqual(self.backup.read_bytes(), self.old_config.read_bytes())

        self.assert_cli_success(self.run_specify("extension", "disable", "flow-roadmap"))
        self.assert_cli_success(self.run_specify("extension", "enable", "diagram-roadmap"))
        registry = self.registry()["extensions"]
        self.assertTrue(registry["diagram-roadmap"]["enabled"])
        self.assertFalse(registry["flow-roadmap"]["enabled"])


if __name__ == "__main__":
    unittest.main()
