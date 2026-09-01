"""Shared test support for the Diagram Roadmap Python loader."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE_LOADER = REPOSITORY_ROOT / "scripts" / "python" / "load_config.py"
DEFAULT_MANIFEST = """\
schema_version: '1.0'
extension:
  id: diagram-roadmap
  name: Diagram Roadmap
  version: 0.2.0
requires:
  speckit_version: '==1.0.1'
provides:
  commands: []
defaults:
  report:
    max_findings: 50
"""


def active_specify_interpreter() -> Path:
    """Return the absolute interpreter recorded by the active Specify entrypoint."""
    executable = shutil.which("specify")
    if executable is None:
        raise unittest.SkipTest("active specify executable is unavailable")
    first_line = Path(executable).resolve().read_text(encoding="utf-8").splitlines()[0]
    if not first_line.startswith("#!/"):
        raise unittest.SkipTest("active specify executable has no absolute shebang")
    return Path(first_line[2:])


class LoaderLayout:
    """A temporary source or installed layout with a controlled Specify entrypoint."""

    def __init__(self, *, installed: bool = False) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary_directory.name) / "project"
        self.root.mkdir()
        self.payload = (
            self.root / ".specify" / "extensions" / "diagram-roadmap"
            if installed
            else self.root
        )
        self.loader = self.payload / "scripts" / "python" / "load_config.py"
        self.loader.parent.mkdir(parents=True)
        if SOURCE_LOADER.exists():
            shutil.copy2(SOURCE_LOADER, self.loader)
        self.manifest = self.payload / "extension.yml"
        self.manifest.write_text(DEFAULT_MANIFEST, encoding="utf-8")
        self.configuration = (
            self.root
            / ".specify"
            / "extensions"
            / "diagram-roadmap"
            / "roadmap-config.yml"
        )
        self.configuration.parent.mkdir(parents=True, exist_ok=True)
        self.bin_directory = Path(self._temporary_directory.name) / "bin"
        self.bin_directory.mkdir()
        self.specify = self.bin_directory / "specify"
        self.write_specify(active_specify_interpreter())

    def cleanup(self) -> None:
        """Remove the temporary layout."""
        self._temporary_directory.cleanup()

    def write_specify(self, interpreter: Path | str, body: str = "pass\n") -> None:
        """Create a minimal POSIX console script with the requested shebang."""
        self.specify.write_text(f"#!{interpreter}\n{body}", encoding="utf-8")
        self.specify.chmod(self.specify.stat().st_mode | stat.S_IXUSR)

    def write_config(self, content: str) -> None:
        """Write the project-owned configuration file."""
        self.configuration.write_text(content, encoding="utf-8")

    def run(
        self,
        *arguments: str,
        environment: dict[str, str] | None = None,
        cwd: Path | None = None,
        interpreter: Path | str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """Run the loader with an isolated, deterministic process environment."""
        command_interpreter = str(interpreter or sys.executable)
        child_environment = os.environ.copy()
        for name in tuple(child_environment):
            if name.startswith("SPECKIT_DIAGRAM_ROADMAP_") or name == "PYTHONPATH":
                child_environment.pop(name)
        child_environment.update(
            {
                "PATH": f"{self.bin_directory}{os.pathsep}{os.environ.get('PATH', '')}",
                "HOME": os.environ.get("HOME", str(self.root)),
                "LANG": "C.UTF-8",
            }
        )
        if environment:
            child_environment.update(environment)
        return subprocess.run(
            [command_interpreter, str(self.loader), *arguments],
            cwd=cwd or self.root,
            env=child_environment,
            text=True,
            capture_output=True,
            check=False,
        )


class LoaderTestCase(unittest.TestCase):
    """Base test case that owns temporary loader layouts."""

    def setUp(self) -> None:
        self.layouts: list[LoaderLayout] = []

    def tearDown(self) -> None:
        for layout in reversed(self.layouts):
            layout.cleanup()

    def layout(self, *, installed: bool = False) -> LoaderLayout:
        """Create and register a temporary loader layout."""
        layout = LoaderLayout(installed=installed)
        self.layouts.append(layout)
        return layout

    def assert_success(self, result: subprocess.CompletedProcess[str]) -> dict[str, object]:
        """Assert success and parse the single JSON output line."""
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        self.assertTrue(result.stdout.endswith("\n"))
        self.assertEqual(1, len(result.stdout.splitlines()))
        return json.loads(result.stdout)

    def assert_failure(self, result: subprocess.CompletedProcess[str]) -> None:
        """Assert the bounded public error contract."""
        self.assertEqual(1, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertTrue(result.stderr.startswith("Error:"), result.stderr)
        self.assertEqual(1, len(result.stderr.splitlines()))
        self.assertNotIn("Traceback", result.stderr)
