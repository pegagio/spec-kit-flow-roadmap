"""Output and diagnostic contract tests for the FlowKit Roadmap Python loader."""

from __future__ import annotations

import json

from support import LoaderTestCase, REPOSITORY_ROOT


class OutputContractTest(LoaderTestCase):
    """Verify stable compact UTF-8 output and bounded failures."""

    def test_default_output_is_compact_and_ordered(self) -> None:
        result = self.layout().run()
        output = self.assert_success(result)
        expected = json.dumps(output, ensure_ascii=False, separators=(",", ":")) + "\n"
        self.assertEqual(expected, result.stdout)

    def test_unicode_quotes_backslashes_tabs_and_lines_round_trip(self) -> None:
        layout = self.layout()
        value = 'docs/雪/"quoted"\\tab\tline\nroadmap.md'
        result = layout.run(environment={"SPECKIT_FLOW_ROADMAP_PATH": value})
        output = self.assert_success(result)
        self.assertEqual(value, output["roadmap_path"])
        self.assertIn("\\t", result.stdout)
        self.assertIn("\\n", result.stdout)

    def test_repeated_results_are_byte_identical(self) -> None:
        layout = self.layout()
        first = layout.run()
        second = layout.run()
        self.assert_success(first)
        self.assert_success(second)
        self.assertEqual(first.stdout, second.stdout)

    def test_failures_have_empty_stdout_and_one_sanitized_line(self) -> None:
        layout = self.layout(installed=True)
        layout.write_config('"bad\\nkey": true\n')
        result = layout.run()
        self.assert_failure(result)
        self.assertNotIn("\nkey", result.stderr)

    def test_unexpected_argument_has_no_traceback(self) -> None:
        self.assert_failure(self.layout().run("unexpected"))

    def test_validate_path_result_is_exact(self) -> None:
        layout = self.layout()
        (layout.root / "document.md").write_text("document", encoding="utf-8")
        result = layout.run("--validate-path", "prd", "document.md")
        self.assert_success(result)
        self.assertEqual('{"path":"document.md"}\n', result.stdout)

    def test_shared_report_template_has_complete_provenance_and_counts(self) -> None:
        text = (REPOSITORY_ROOT / "templates" / "review-report-template.md").read_text(encoding="utf-8")
        for expected in ("Selection source", "Match method", "Reviewed paths", "Baseline input / OID", "Dirty-state boundary", "Snapshot identity", "Configured cap", "Total / displayed / omitted", "Material limitations", "Lifecycle Recommendation", "sole permitted write"):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)


if __name__ == "__main__":
    __import__("unittest").main()
