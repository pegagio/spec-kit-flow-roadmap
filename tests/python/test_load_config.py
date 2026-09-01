"""Smoke tests for the Diagram Roadmap Python loader."""

from __future__ import annotations

from support import LoaderTestCase


class LoadConfigSmokeTest(LoaderTestCase):
    """Verify default and validation-mode public shapes."""

    def test_defaults_emit_exact_six_field_shape(self) -> None:
        layout = self.layout()
        output = self.assert_success(layout.run())
        self.assertEqual(
            [
                "roadmap_path",
                "roadmap_exists",
                "adr_dir",
                "adr_present",
                "prd_globs",
                "max_findings",
            ],
            list(output),
        )
        self.assertEqual(".specify/memory/roadmap.md", output["roadmap_path"])
        self.assertEqual("docs/adr", output["adr_dir"])
        self.assertEqual(5, len(output["prd_globs"]))
        self.assertEqual(50, output["max_findings"])

    def test_installed_configuration_is_loaded(self) -> None:
        layout = self.layout(installed=True)
        layout.write_config("report:\n  max_findings: 7\n")
        output = self.assert_success(layout.run())
        self.assertEqual(7, output["max_findings"])

    def test_validation_kinds_return_canonical_path(self) -> None:
        layout = self.layout()
        (layout.root / "docs").mkdir()
        (layout.root / "docs" / "roadmap.md").write_text("roadmap", encoding="utf-8")
        cases = {
            "roadmap-read": "docs/roadmap.md",
            "roadmap-write": "docs/new-roadmap.md",
            "adr": "docs",
            "prd": "docs/roadmap.md",
        }
        for kind, candidate in cases.items():
            with self.subTest(kind=kind):
                output = self.assert_success(layout.run("--validate-path", kind, candidate))
                self.assertEqual(candidate, output["path"])

    def test_invalid_validation_kind_has_empty_stdout(self) -> None:
        layout = self.layout()
        result = layout.run("--validate-path", "unknown", "README.md")
        self.assert_failure(result)


if __name__ == "__main__":
    __import__("unittest").main()
