"""Current-versus-historical surface tests for the Python-only migration."""

from __future__ import annotations

from pathlib import Path
import unittest

from support import REPOSITORY_ROOT


class CurrentSurfaceTest(unittest.TestCase):
    """Keep unsupported runtime references out of maintained current surfaces."""

    def test_extension_owns_only_the_python_runtime_script(self) -> None:
        scripts = sorted(
            path.relative_to(REPOSITORY_ROOT).as_posix()
            for path in (REPOSITORY_ROOT / "scripts").rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix != ".pyc"
        )
        self.assertEqual(["scripts/python/load_config.py"], scripts)

    def test_command_and_manifest_surfaces_have_no_legacy_runtime_paths(self) -> None:
        files = [REPOSITORY_ROOT / "extension.yml", REPOSITORY_ROOT / ".extensionignore", *(REPOSITORY_ROOT / "commands").glob("*.md")]
        for path in files:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("scripts/bash", text)
                self.assertNotIn("scripts/powershell", text)
                self.assertNotIn("load-config.sh", text)
                self.assertNotIn("load-config.ps1", text)

    def test_current_documentation_describes_python_on_macos_and_linux(self) -> None:
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        tests_readme = (REPOSITORY_ROOT / "tests" / "README.md").read_text(encoding="utf-8")
        justfile = (REPOSITORY_ROOT / "justfile").read_text(encoding="utf-8")
        combined = "\n".join((readme, tests_readme, justfile))
        self.assertIn("macOS", readme)
        self.assertIn("Linux", readme)
        self.assertIn("Python", combined)
        for stale in ("Bats", "Pester", "bash + PowerShell", "test-bash", "test-powershell", "test-parity"):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, combined)

    def test_unreleased_changelog_records_migration_without_rewriting_release(self) -> None:
        changelog = (REPOSITORY_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        unreleased, released = changelog.split("## 0.1.0", 1)
        self.assertIn("Python", unreleased)
        self.assertIn("macOS", unreleased)
        self.assertIn("Linux", unreleased)
        self.assertIn("Windows", unreleased)
        self.assertIn("bash + PowerShell", released)

    def test_generated_skills_have_no_legacy_runtime_paths(self) -> None:
        skills = sorted((REPOSITORY_ROOT / ".agents" / "skills").glob("speckit-diagram-roadmap-*/SKILL.md"))
        self.assertEqual(4, len(skills))
        for skill in skills:
            with self.subTest(skill=skill.parent.name):
                text = skill.read_text(encoding="utf-8")
                self.assertIn("scripts/python/load_config.py", text)
                self.assertNotIn("scripts/bash", text)
                self.assertNotIn("scripts/powershell", text)


if __name__ == "__main__":
    unittest.main()
