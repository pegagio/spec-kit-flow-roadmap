"""Strict YAML and trusted-input tests for the Diagram Roadmap Python loader."""

from __future__ import annotations

import os
from pathlib import Path

from support import LoaderTestCase


class YamlValidationTest(LoaderTestCase):
    """Reject malformed, ambiguous, unsafe, and structurally invalid YAML."""

    def assert_invalid_config(self, content: str) -> None:
        layout = self.layout(installed=True)
        layout.write_config(content)
        self.assert_failure(layout.run())

    def test_empty_and_comments_only_documents_are_absent(self) -> None:
        for content in ("", "# comment only\n"):
            with self.subTest(content=content):
                layout = self.layout(installed=True)
                layout.write_config(content)
                self.assert_success(layout.run())

    def test_malformed_document_is_rejected(self) -> None:
        self.assert_invalid_config("roadmap: [\n")

    def test_multiple_documents_are_rejected(self) -> None:
        self.assert_invalid_config("roadmap: {}\n---\nreport: {}\n")

    def test_unsafe_tag_is_rejected(self) -> None:
        self.assert_invalid_config("roadmap: !!python/object/apply:os.system ['false']\n")

    def test_alias_is_rejected(self) -> None:
        self.assert_invalid_config("roadmap: &value {path: road.md}\nadr: *value\n")

    def test_merge_key_is_rejected(self) -> None:
        self.assert_invalid_config("base: &base {path: road.md}\nroadmap:\n  <<: *base\n")

    def test_duplicate_key_is_rejected(self) -> None:
        self.assert_invalid_config("report:\n  max_findings: 1\n  max_findings: 2\n")

    def test_unknown_keys_are_rejected(self) -> None:
        for content in ("unknown: true\n", "roadmap:\n  typo: road.md\n", "roadmap:\n  old_path: road.md\n"):
            with self.subTest(content=content):
                self.assert_invalid_config(content)

    def test_oversized_input_is_rejected(self) -> None:
        self.assert_invalid_config("#" * 65_537)

    def test_wrong_root_and_section_types_are_rejected(self) -> None:
        for content in ("[]\n", "roadmap: value\n", "prd:\n  globs: value\n"):
            with self.subTest(content=content):
                self.assert_invalid_config(content)

    def test_exact_scalar_types_are_enforced(self) -> None:
        for content in ("roadmap:\n  path: true\n", "adr:\n  dir: 1.5\n", "report:\n  max_findings: true\n", "report:\n  max_findings: -1\n", "report:\n  max_findings: nope\n", "prd:\n  globs: [valid.md, 2]\n"):
            with self.subTest(content=content):
                self.assert_invalid_config(content)

    def test_configuration_symlinks_are_rejected_inside_and_outside_project(self) -> None:
        for outside in (False, True):
            with self.subTest(outside=outside):
                layout = self.layout(installed=True)
                target = Path(layout._temporary_directory.name) / "outside.yml" if outside else layout.configuration.parent / "inside.yml"
                target.write_text("report:\n  max_findings: 2\n", encoding="utf-8")
                layout.configuration.symlink_to(target)
                self.assert_failure(layout.run())

    def test_manifest_symlink_is_rejected(self) -> None:
        layout = self.layout()
        target = layout.root / "manifest-target.yml"
        layout.manifest.rename(target)
        layout.manifest.symlink_to(target)
        self.assert_failure(layout.run())

    def test_directory_and_fifo_inputs_are_rejected(self) -> None:
        layout = self.layout(installed=True)
        layout.configuration.mkdir()
        self.assert_failure(layout.run())
        layout.configuration.rmdir()
        if hasattr(os, "mkfifo"):
            os.mkfifo(layout.configuration)
            self.assert_failure(layout.run())


if __name__ == "__main__":
    __import__("unittest").main()
