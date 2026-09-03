"""Contract tests for deterministic Diagram Roadmap review mechanics."""

from __future__ import annotations

import json

from support import LoaderTestCase


ROADMAP = """\
# Roadmap

### 010 — Previous feature  [status: verified]

- **Spec dir:** specs/007-previous/

### 011 — Harden command contracts  [status: specced]

- **Spec dir:** specs/008-command-contract-hardening/
"""


class ReviewContractTest(LoaderTestCase):
    """Verify target, finding, lifecycle, and report operations."""

    def review_layout(self):
        layout = self.layout()
        (layout.root / ".specify" / "memory").mkdir(parents=True, exist_ok=True)
        (layout.root / ".specify" / "memory" / "roadmap.md").write_text(ROADMAP, encoding="utf-8")
        (layout.root / "specs" / "008-command-contract-hardening").mkdir(parents=True)
        return layout

    def test_default_preserves_six_field_configuration(self) -> None:
        output = self.assert_success(self.review_layout().run_review())
        self.assertEqual(["roadmap_path", "roadmap_exists", "adr_dir", "adr_present", "prd_globs", "max_findings"], list(output))

    def test_exact_target_overrides_ambient_feature(self) -> None:
        layout = self.review_layout()
        output = self.assert_success(layout.run_review("resolve-target", "--command", "brief", "--roadmap-path", ".specify/memory/roadmap.md", "--spec-target", "specs/008-command-contract-hardening/spec.md", "--ambient-feature", "specs/007-previous"))
        self.assertEqual("selected", output["state"])
        self.assertEqual("011", output["entry"]["id"])
        self.assertEqual("exact-spec-dir", output["match_method"])

    def test_conflicting_explicit_targets_stop(self) -> None:
        layout = self.review_layout()
        output = self.assert_success(layout.run_review("resolve-target", "--command", "debrief", "--roadmap-path", ".specify/memory/roadmap.md", "--spec-target", "specs/008-command-contract-hardening", "--roadmap-entry", "010"))
        self.assertEqual("conflict", output["state"])

    def test_missing_match_returns_candidates_for_judgment(self) -> None:
        layout = self.review_layout()
        output = self.assert_success(layout.run_review("resolve-target", "--command", "brief", "--roadmap-path", ".specify/memory/roadmap.md", "--roadmap-entry", "similar title"))
        self.assertEqual("needs-judgment", output["state"])
        self.assertEqual(["010", "011"], [item["id"] for item in output["candidates"]])

    def test_findings_are_ordered_capped_and_verdict_uses_totals(self) -> None:
        layout = self.review_layout()
        findings = [
            {"severity": "Question", "category": "scope-creep", "text": "Question", "suggestion": "Decide", "evidence": ["spec.md"], "blocking": False},
            {"severity": "Must-Address", "category": "outcome-miss", "text": "Blocker", "suggestion": "Fix", "evidence": ["implementation:delta"], "blocking": True},
        ]
        output = self.assert_success(layout.run_review("evaluate-findings", "--kind", "debrief", "--max-findings", "0", input_text=json.dumps(findings)))
        self.assertEqual([], output["findings"])
        self.assertEqual(2, output["summary"]["total"])
        self.assertEqual(2, output["summary"]["omitted"])
        self.assertEqual("RETHINK", output["summary"]["verdict"])

    def test_invalid_blocking_finding_fails_closed(self) -> None:
        finding = [{"severity": "Question", "category": "scope-creep", "text": "Question", "suggestion": "Decide", "evidence": ["spec.md"], "blocking": True}]
        self.assert_failure(self.review_layout().run_review("evaluate-findings", "--kind", "debrief", "--max-findings", "1", input_text=json.dumps(finding)))

    def test_brief_and_debrief_lifecycle_gates(self) -> None:
        layout = self.review_layout()
        brief = self.assert_success(layout.run_review("evaluate-lifecycle", "--phase", "brief", "--status", "specced", "--dependency-status", "verified"))
        self.assertEqual("in-progress", brief["proposed_status"])
        blocked = self.assert_success(layout.run_review("evaluate-lifecycle", "--phase", "brief", "--status", "specced", "--dependency-status", "implemented"))
        self.assertIsNone(blocked["proposed_status"])
        debrief = self.assert_success(layout.run_review("evaluate-lifecycle", "--phase", "debrief", "--status", "implemented", "--outcome-met", "true", "--delta-trustworthy", "true", "--must-address-count", "0"))
        self.assertEqual("verified", debrief["proposed_status"])

    def test_report_allocation_is_collision_safe(self) -> None:
        layout = self.review_layout()
        arguments = ("allocate-report", "--kind", "brief", "--feature-dir", "specs/008-command-contract-hardening", "--timestamp-utc", "20260903T210500Z")
        first = self.assert_success(layout.run_review(*arguments))
        second = self.assert_success(layout.run_review(*arguments))
        self.assertEqual(1, first["collision_index"])
        self.assertEqual(2, second["collision_index"])
        self.assertNotEqual(first["path"], second["path"])


if __name__ == "__main__":
    __import__("unittest").main()
