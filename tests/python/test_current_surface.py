"""Current-versus-historical surface tests for the Python-only migration."""

from __future__ import annotations

from pathlib import Path
import tomllib
import unittest

from support import REPOSITORY_ROOT

CURRENT_DOCUMENTATION_PATHS = ("README.md", "tests/README.md")


def read_root_text(*parts: str) -> str:
    """Read UTF-8 text from a repository-root-relative path."""
    return REPOSITORY_ROOT.joinpath(*parts).read_text(encoding="utf-8")


def load_mise_config() -> dict[str, object]:
    """Load the repository's canonical mise configuration."""
    with (REPOSITORY_ROOT / "mise.toml").open("rb") as config_file:
        return tomllib.load(config_file)


class CurrentSurfaceTest(unittest.TestCase):
    """Keep unsupported runtime references out of maintained current surfaces."""

    def test_mise_test_task_uses_the_declared_python_without_bootstrap(self) -> None:
        config = load_mise_config()
        tools = config.get("tools", {})
        settings = config.get("settings", {})
        tasks = config.get("tasks", {})

        self.assertIsInstance(tools, dict)
        self.assertIsInstance(settings, dict)
        self.assertIsInstance(tasks, dict)
        self.assertEqual("3.11.16", tools.get("python"))
        self.assertEqual(False, settings.get("task", {}).get("run_auto_install"))

        test_task = tasks.get("test", {})
        self.assertEqual("Run the complete Python contract suite", test_task.get("description"))
        self.assertEqual("python -m unittest discover -s tests/python -p 'test_*.py'", test_task.get("run"))
        for forbidden in ("mise exec", "mise install", "mise trust"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, test_task.get("run", ""))

    def test_mise_owns_the_exact_current_tool_and_task_inventory(self) -> None:
        config = load_mise_config()

        self.assertEqual(
            {
                "python": "3.11.16",
                "uv": "0.12.5",
                "pipx:specify-cli": {
                    "version": "1.0.1",
                    "depends": ["python", "uv"],
                },
            },
            config.get("tools"),
        )
        self.assertEqual({"test"}, set(config.get("tasks", {})))
        self.assertEqual(False, config.get("settings", {}).get("task", {}).get("run_auto_install"))
        self.assertFalse((REPOSITORY_ROOT / "justfile").exists())
        for unsupported in ("default", "lint", "build", "dev", "clean"):
            with self.subTest(unsupported=unsupported):
                self.assertNotIn(unsupported, config.get("tasks", {}))

    def test_extension_owns_only_the_two_python_runtime_scripts(self) -> None:
        scripts = sorted(
            path.relative_to(REPOSITORY_ROOT).as_posix()
            for path in (REPOSITORY_ROOT / "scripts").rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix != ".pyc"
        )
        self.assertEqual(["scripts/python/load_config.py", "scripts/python/review_contract.py"], scripts)

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
        readme = read_root_text("README.md")
        tests_readme = read_root_text("tests", "README.md")
        combined = "\n".join((readme, tests_readme))
        self.assertIn("macOS", readme)
        self.assertIn("Linux", readme)
        self.assertIn("Python", combined)
        for stale in ("Bats", "Pester", "bash + PowerShell", "test-bash", "test-powershell", "test-parity"):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, combined)

    def test_current_documentation_uses_only_the_root_mise_workflow(self) -> None:
        documents = {
            path: read_root_text(*path.split("/"))
            for path in CURRENT_DOCUMENTATION_PATHS
        }
        self.assertEqual({"README.md", "tests/README.md"}, set(documents))

        for path, text in documents.items():
            with self.subTest(path=path):
                self.assertIn("repository root", text)
                trust_position = text.index("mise trust mise.toml")
                install_position = text.index("mise install")
                test_position = text.index("mise run test")
                self.assertLess(trust_position, install_position)
                self.assertLess(install_position, test_position)
                self.assertEqual(1, text.count("mise run test"))
                self.assertNotIn("just test", text)
                self.assertNotIn("mise exec -- python -m unittest", text)

    def test_unreleased_changelog_records_migration_without_rewriting_release(self) -> None:
        changelog = read_root_text("CHANGELOG.md")
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
                if skill.parent.name.endswith("-write"):
                    self.assertIn("scripts/python/load_config.py", text)
                else:
                    self.assertIn("scripts/python/review_contract.py", text)
                self.assertNotIn("scripts/bash", text)
                self.assertNotIn("scripts/powershell", text)


if __name__ == "__main__":
    unittest.main()
