"""Configuration precedence tests for the Diagram Roadmap Python loader."""

from __future__ import annotations

from support import DEFAULT_MANIFEST, LoaderTestCase


class ConfigurationResolutionTest(LoaderTestCase):
    """Verify independent per-leaf precedence and strict environment parsing."""

    def test_defaults_are_stable_and_ordered(self) -> None:
        output = self.assert_success(self.layout().run())
        self.assertEqual(".specify/memory/roadmap.md", output["roadmap_path"])
        self.assertEqual("docs/adr", output["adr_dir"])
        self.assertEqual(
            ["**/prd*.md", "**/PRD*.md", "**/prd-intake.yaml", "**/product-spec.md", "docs/product/**/*.md"],
            output["prd_globs"],
        )
        self.assertEqual(50, output["max_findings"])

    def test_each_environment_leaf_overrides_configuration(self) -> None:
        layout = self.layout(installed=True)
        layout.write_config("roadmap:\n  path: file-roadmap.md\nadr:\n  dir: file-adrs\nprd:\n  globs: [file-prd.md]\nreport:\n  max_findings: 3\n")
        output = self.assert_success(layout.run(environment={
            "SPECKIT_DIAGRAM_ROADMAP_PATH": "environment-roadmap.md",
            "SPECKIT_DIAGRAM_ROADMAP_ADR_DIR": "environment-adrs",
            "SPECKIT_DIAGRAM_ROADMAP_PRD_GLOBS": "environment-one.md,environment-two.md",
            "SPECKIT_DIAGRAM_ROADMAP_MAX_FINDINGS": "9",
        }))
        self.assertEqual("environment-roadmap.md", output["roadmap_path"])
        self.assertEqual("environment-adrs", output["adr_dir"])
        self.assertEqual(["environment-one.md", "environment-two.md"], output["prd_globs"])
        self.assertEqual(9, output["max_findings"])

    def test_configuration_leaves_override_manifest_independently(self) -> None:
        layout = self.layout(installed=True)
        layout.manifest.write_text(DEFAULT_MANIFEST.replace("max_findings: 50", "max_findings: 31"), encoding="utf-8")
        layout.write_config("roadmap:\n  path: configured.md\n")
        output = self.assert_success(layout.run())
        self.assertEqual("configured.md", output["roadmap_path"])
        self.assertEqual(31, output["max_findings"])

    def test_null_and_empty_scalars_fall_through(self) -> None:
        layout = self.layout(installed=True)
        layout.write_config("roadmap:\n  path: null\nadr:\n  dir: ''\nreport:\n  max_findings: null\n")
        output = self.assert_success(layout.run())
        self.assertEqual(".specify/memory/roadmap.md", output["roadmap_path"])
        self.assertEqual("docs/adr", output["adr_dir"])
        self.assertEqual(50, output["max_findings"])

    def test_explicit_empty_glob_list_replaces_defaults(self) -> None:
        layout = self.layout(installed=True)
        layout.write_config("prd:\n  globs: []\n")
        self.assertEqual([], self.assert_success(layout.run())["prd_globs"])

    def test_csv_quotes_preserve_comma(self) -> None:
        output = self.assert_success(self.layout().run(environment={"SPECKIT_DIAGRAM_ROADMAP_PRD_GLOBS": '"docs/a,b.md",docs/c.md'}))
        self.assertEqual(["docs/a,b.md", "docs/c.md"], output["prd_globs"])

    def test_empty_csv_member_is_rejected(self) -> None:
        self.assert_failure(self.layout().run(environment={"SPECKIT_DIAGRAM_ROADMAP_PRD_GLOBS": "one.md,,two.md"}))

    def test_multiple_csv_records_are_rejected(self) -> None:
        self.assert_failure(self.layout().run(environment={"SPECKIT_DIAGRAM_ROADMAP_PRD_GLOBS": "one.md\ntwo.md"}))

    def test_zero_findings_is_valid(self) -> None:
        output = self.assert_success(self.layout().run(environment={"SPECKIT_DIAGRAM_ROADMAP_MAX_FINDINGS": "0"}))
        self.assertEqual(0, output["max_findings"])

    def test_glob_resolution_does_not_scan(self) -> None:
        layout = self.layout()
        (layout.root / "docs").mkdir()
        (layout.root / "docs" / "prd-secret.md").write_text("secret", encoding="utf-8")
        output = self.assert_success(layout.run(environment={"SPECKIT_DIAGRAM_ROADMAP_PRD_GLOBS": "docs/prd*.md"}))
        self.assertEqual(["docs/prd*.md"], output["prd_globs"])
        self.assertNotIn("prd-secret.md", str(output))


if __name__ == "__main__":
    __import__("unittest").main()
