"""Assertions for the repository's installed Diagram Roadmap snapshot."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import unittest

from support import REPOSITORY_ROOT
from test_installation import SOURCE_FILES


class DogfoodInstallationTest(unittest.TestCase):
    """Verify parity and project-owned state in the ignored dogfood installation."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = REPOSITORY_ROOT / ".specify" / "extensions" / "diagram-roadmap"

    def test_exact_installed_file_set(self) -> None:
        files = sorted(path.relative_to(self.payload).as_posix() for path in self.payload.rglob("*") if path.is_file())
        self.assertEqual(sorted([*SOURCE_FILES, "roadmap-config.yml"]), files)

    def test_source_owned_files_match_byte_for_byte(self) -> None:
        for relative in SOURCE_FILES:
            with self.subTest(path=relative):
                self.assertEqual((REPOSITORY_ROOT / relative).read_bytes(), (self.payload / relative).read_bytes())

    def test_project_configuration_is_regular_and_semantically_valid(self) -> None:
        configuration = self.payload / "roadmap-config.yml"
        self.assertTrue(configuration.is_file())
        self.assertFalse(configuration.is_symlink())
        result = subprocess.run(
            [str(self.payload / "scripts" / "python" / "load_config.py")],
            cwd=REPOSITORY_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(6, len(json.loads(result.stdout)))

    def test_generated_skills_and_hooks_are_current(self) -> None:
        skills = sorted((REPOSITORY_ROOT / ".agents" / "skills").glob("speckit-diagram-roadmap-*/SKILL.md"))
        self.assertEqual(4, len(skills))
        for skill in skills:
            with self.subTest(skill=skill.parent.name):
                text = skill.read_text(encoding="utf-8")
                if skill.parent.name.endswith("-write"):
                    self.assertIn("scripts/python/load_config.py", text)
                else:
                    self.assertIn("scripts/python/review_contract.py", text)
        registry = (REPOSITORY_ROOT / ".specify" / "extensions.yml").read_text(encoding="utf-8")
        self.assertEqual(1, registry.count("after_constitution:"))
        self.assertEqual(1, registry.count("before_implement:"))
        self.assertEqual(1, registry.count("after_implement:"))

    def test_payload_has_no_symlinks_or_nested_git(self) -> None:
        self.assertFalse(any(path.is_symlink() for path in self.payload.rglob("*")))
        self.assertFalse(any(path.name == ".git" for path in self.payload.rglob(".git")))


if __name__ == "__main__":
    unittest.main()
