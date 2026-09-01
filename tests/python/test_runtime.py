"""Runtime-boundary tests for the Diagram Roadmap Python loader."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

from support import LoaderTestCase, active_specify_interpreter


class RuntimeBoundaryTest(LoaderTestCase):
    """Verify trusted interpreter discovery and isolated execution."""

    def create_venv(self, parent: Path) -> Path:
        """Create a same-version virtual environment or skip when unavailable."""
        environment = parent / "venv"
        completed = __import__("subprocess").run(
            [sys.executable, "-m", "venv", str(environment)],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            self.skipTest("venv creation is unavailable")
        return environment

    def test_source_layout_runs_from_alien_working_directory(self) -> None:
        layout = self.layout()
        with tempfile.TemporaryDirectory() as alien:
            result = layout.run(cwd=Path(alien))
        self.assert_success(result)

    def test_installed_layout_discovers_project_from_script(self) -> None:
        layout = self.layout(installed=True)
        result = layout.run()
        self.assert_success(result)

    def test_missing_specify_fails_closed(self) -> None:
        layout = self.layout()
        layout.specify.unlink()
        result = layout.run(environment={"PATH": str(layout.bin_directory)})
        self.assert_failure(result)
        self.assertIn("specify", result.stderr)

    def test_env_wrapper_is_rejected(self) -> None:
        layout = self.layout()
        layout.write_specify("/usr/bin/env python3")
        result = layout.run()
        self.assert_failure(result)
        self.assertIn("console-script", result.stderr)

    def test_hostile_pythonpath_and_project_yaml_are_ignored(self) -> None:
        layout = self.layout()
        (layout.root / "yaml.py").write_text("raise RuntimeError('shadowed')\n", encoding="utf-8")
        result = layout.run(environment={"PYTHONPATH": str(layout.root)})
        self.assert_success(result)
        self.assertNotIn("shadowed", result.stderr)

    def test_canonical_interpreter_alias_is_accepted(self) -> None:
        layout = self.layout()
        real_specify = layout.bin_directory / "real-specify"
        layout.specify.rename(real_specify)
        layout.specify.symlink_to(real_specify)
        result = layout.run()
        self.assert_success(result)

    def test_missing_pyyaml_is_rejected(self) -> None:
        layout = self.layout()
        with tempfile.TemporaryDirectory() as temporary:
            environment = self.create_venv(Path(temporary))
            layout.write_specify(environment / "bin" / "python")
            result = layout.run()
        self.assert_failure(result)
        self.assertIn("PyYAML", result.stderr)

    def test_pyyaml_below_six_is_rejected(self) -> None:
        layout = self.layout()
        with tempfile.TemporaryDirectory() as temporary:
            environment = self.create_venv(Path(temporary))
            purelib_result = __import__("subprocess").run(
                [str(environment / "bin" / "python"), "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"],
                capture_output=True,
                text=True,
                check=True,
            )
            yaml_package = Path(purelib_result.stdout.strip()) / "yaml"
            yaml_package.mkdir()
            (yaml_package / "__init__.py").write_text("__version__ = '5.4.1'\n", encoding="utf-8")
            layout.write_specify(environment / "bin" / "python")
            result = layout.run()
        self.assert_failure(result)
        self.assertIn("6.0 or newer", result.stderr)

    def test_reexecution_loop_marker_fails_closed(self) -> None:
        layout = self.layout()
        result = layout.run(environment={"SPECKIT_DIAGRAM_ROADMAP_ISOLATED": "1"})
        self.assert_failure(result)
        self.assertIn("did not converge", result.stderr)

    def test_mismatched_python_version_is_rejected_when_available(self) -> None:
        candidate = Path("/usr/bin/python3")
        if not candidate.exists() or candidate.resolve() == active_specify_interpreter():
            self.skipTest("no alternate system Python is available")
        version = __import__("subprocess").run(
            [str(candidate), "-c", "import sys; print('.'.join(map(str, sys.version_info[:3])))"],
            capture_output=True,
            text=True,
            check=False,
        )
        if version.stdout.strip() == "3.11.16":
            self.skipTest("alternate system Python has the required version")
        layout = self.layout()
        layout.write_specify(candidate)
        result = layout.run()
        self.assert_failure(result)
        self.assertIn("3.11.16", result.stderr)


if __name__ == "__main__":
    unittest.main()
