"""Project-containment tests for the FlowKit Roadmap Python loader."""

from __future__ import annotations

from pathlib import Path

from support import LoaderTestCase


class PathContainmentTest(LoaderTestCase):
    """Verify lexical, canonical, kind, and access-time path boundaries."""

    def assert_roadmap_value_fails(self, value: str) -> None:
        layout = self.layout(installed=True)
        layout.write_config(f"roadmap:\n  path: {value!r}\n")
        self.assert_failure(layout.run())

    def test_absolute_rooted_and_traversal_forms_are_rejected(self) -> None:
        for value in ("/tmp/roadmap.md", "C:\\temp\\roadmap.md", "\\\\server\\share\\roadmap.md", "../roadmap.md", "docs/../roadmap.md", "~/roadmap.md"):
            with self.subTest(value=value):
                self.assert_roadmap_value_fails(value)

    def test_nul_is_rejected(self) -> None:
        layout = self.layout(installed=True)
        layout.write_config('roadmap:\n  path: "bad\\0path.md"\n')
        self.assert_failure(layout.run())

    def test_internal_symlink_is_canonicalized(self) -> None:
        layout = self.layout()
        (layout.root / "real").mkdir()
        (layout.root / "real" / "roadmap.md").write_text("roadmap", encoding="utf-8")
        (layout.root / "link").symlink_to(layout.root / "real", target_is_directory=True)
        output = self.assert_success(layout.run("--validate-path", "roadmap-read", "link/roadmap.md"))
        self.assertEqual("real/roadmap.md", output["path"])

    def test_escaping_and_dangling_symlinks_are_rejected(self) -> None:
        for dangling in (False, True):
            with self.subTest(dangling=dangling):
                layout = self.layout()
                outside = Path(layout._temporary_directory.name) / "outside"
                if not dangling:
                    outside.mkdir()
                (layout.root / "escape").symlink_to(outside, target_is_directory=True)
                self.assert_failure(layout.run("--validate-path", "roadmap-write", "escape/roadmap.md"))

    def test_nonexistent_in_root_roadmap_target_is_allowed(self) -> None:
        layout = self.layout()
        output = self.assert_success(layout.run("--validate-path", "roadmap-write", "future/path/roadmap.md"))
        self.assertEqual("future/path/roadmap.md", output["path"])

    def test_glob_literal_prefix_escape_is_rejected_without_scanning(self) -> None:
        layout = self.layout(installed=True)
        outside = Path(layout._temporary_directory.name) / "outside"
        outside.mkdir()
        (layout.root / "escape").symlink_to(outside, target_is_directory=True)
        layout.write_config("prd:\n  globs: ['escape/**/*.md']\n")
        self.assert_failure(layout.run())

    def test_concrete_wildcard_match_is_revalidated(self) -> None:
        layout = self.layout()
        outside = Path(layout._temporary_directory.name) / "outside"
        outside.mkdir()
        (outside / "prd.md").write_text("prd", encoding="utf-8")
        (layout.root / "escape").symlink_to(outside, target_is_directory=True)
        self.assert_failure(layout.run("--validate-path", "prd", "escape/prd.md"))

    def test_access_time_revalidation_detects_changed_symlink(self) -> None:
        layout = self.layout(installed=True)
        inside = layout.root / "inside"
        inside.mkdir()
        (inside / "roadmap.md").write_text("roadmap", encoding="utf-8")
        link = layout.root / "current"
        link.symlink_to(inside, target_is_directory=True)
        layout.write_config("roadmap:\n  path: current/roadmap.md\n")
        self.assert_success(layout.run())
        link.unlink()
        outside = Path(layout._temporary_directory.name) / "outside"
        outside.mkdir()
        (outside / "roadmap.md").write_text("roadmap", encoding="utf-8")
        link.symlink_to(outside, target_is_directory=True)
        self.assert_failure(layout.run("--validate-path", "roadmap-read", "current/roadmap.md"))

    def test_kind_and_existence_rules(self) -> None:
        layout = self.layout()
        (layout.root / "directory").mkdir()
        (layout.root / "file.md").write_text("file", encoding="utf-8")
        successes = (("roadmap-read", "file.md"), ("roadmap-write", "file.md"), ("roadmap-write", "new.md"), ("adr", "directory"), ("prd", "file.md"))
        failures = (("roadmap-read", "missing.md"), ("roadmap-read", "directory"), ("roadmap-write", "directory"), ("adr", "file.md"), ("prd", "missing.md"))
        for kind, value in successes:
            with self.subTest(kind=kind, value=value, expected="success"):
                self.assert_success(layout.run("--validate-path", kind, value))
        for kind, value in failures:
            with self.subTest(kind=kind, value=value, expected="failure"):
                self.assert_failure(layout.run("--validate-path", kind, value))


if __name__ == "__main__":
    __import__("unittest").main()
