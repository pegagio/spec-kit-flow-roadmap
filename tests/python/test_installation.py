"""Disposable installation tests for the reviewed extension payload."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest

from support import REPOSITORY_ROOT


SOURCE_FILES = [
    "extension.yml",
    "LICENSE",
    "config-template.yml",
    "commands/speckit.diagram-roadmap.write.md",
    "commands/speckit.diagram-roadmap.brief.md",
    "commands/speckit.diagram-roadmap.debrief.md",
    "commands/speckit.diagram-roadmap.sync.md",
    "scripts/python/load_config.py",
    "scripts/python/review_contract.py",
    "templates/roadmap-template.md",
    "templates/review-report-template.md",
]


class DisposableInstallationTest(unittest.TestCase):
    """Install a distinct reviewed copy and verify its complete runtime surface."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_directory = tempfile.TemporaryDirectory()
        temporary_root = Path(cls.temporary_directory.name)
        cls.source = temporary_root / "source"
        cls.project = temporary_root / "project"
        cls.source.mkdir()
        cls.project.mkdir()
        for relative in [*SOURCE_FILES, ".extensionignore"]:
            source = REPOSITORY_ROOT / relative
            destination = cls.source / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        specify_directory = cls.project / ".specify"
        specify_directory.mkdir()
        shutil.copy2(REPOSITORY_ROOT / ".specify" / "integration.json", specify_directory)
        shutil.copy2(REPOSITORY_ROOT / ".specify" / "init-options.json", specify_directory)
        cls.install = subprocess.run(
            ["specify", "extension", "add", "--dev", "--force", str(cls.source)],
            cwd=cls.project,
            text=True,
            capture_output=True,
            check=False,
        )
        cls.enable = subprocess.run(
            ["specify", "extension", "enable", "diagram-roadmap"],
            cwd=cls.project,
            text=True,
            capture_output=True,
            check=False,
        )
        cls.payload = specify_directory / "extensions" / "diagram-roadmap"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary_directory.cleanup()

    def assert_install_succeeded(self) -> None:
        self.assertEqual(0, self.install.returncode, self.install.stderr or self.install.stdout)
        self.assertEqual(0, self.enable.returncode, self.enable.stderr or self.enable.stdout)

    def test_manifest_requires_exact_specify_version(self) -> None:
        self.assertIn("speckit_version: '==1.0.1'", (self.source / "extension.yml").read_text())

    def test_payload_has_exact_twelve_files(self) -> None:
        self.assert_install_succeeded()
        files = sorted(path.relative_to(self.payload).as_posix() for path in self.payload.rglob("*") if path.is_file())
        self.assertEqual(sorted([*SOURCE_FILES, "roadmap-config.yml"]), files)

    def test_source_owned_files_match_byte_for_byte(self) -> None:
        self.assert_install_succeeded()
        for relative in SOURCE_FILES:
            with self.subTest(path=relative):
                self.assertEqual((self.source / relative).read_bytes(), (self.payload / relative).read_bytes())

    def test_scaffold_matches_configuration_template(self) -> None:
        self.assert_install_succeeded()
        self.assertEqual(
            (self.source / "config-template.yml").read_bytes(),
            (self.payload / "roadmap-config.yml").read_bytes(),
        )

    def test_python_scripts_are_executable(self) -> None:
        self.assert_install_succeeded()
        for name in ("load_config.py", "review_contract.py"):
            with self.subTest(name=name):
                mode = (self.payload / "scripts" / "python" / name).stat().st_mode
                self.assertTrue(mode & stat.S_IXUSR)

    def test_four_generated_skills_use_python_contract(self) -> None:
        self.assert_install_succeeded()
        skills = sorted((self.project / ".agents" / "skills").glob("speckit-diagram-roadmap-*/SKILL.md"))
        self.assertEqual(4, len(skills))
        for skill in skills:
            with self.subTest(skill=skill.parent.name):
                text = skill.read_text(encoding="utf-8")
                if skill.parent.name.endswith("-write"):
                    self.assertIn("scripts/python/load_config.py", text)
                else:
                    self.assertIn("scripts/python/review_contract.py", text)
                self.assertNotIn("scripts/bash/load-config.sh", text)
                self.assertNotIn("scripts/powershell/load-config.ps1", text)

    def test_three_hooks_are_registered(self) -> None:
        self.assert_install_succeeded()
        registry = (self.project / ".specify" / "extensions.yml").read_text(encoding="utf-8")
        self.assertEqual(1, registry.count("after_constitution:"))
        self.assertEqual(1, registry.count("before_implement:"))
        self.assertEqual(1, registry.count("after_implement:"))

    def test_payload_contains_no_repository_or_development_files(self) -> None:
        self.assert_install_succeeded()
        self.assertFalse((self.payload / ".git").exists())
        self.assertFalse((self.payload / "tests").exists())
        self.assertFalse((self.payload / "specs").exists())


if __name__ == "__main__":
    unittest.main()
