# Implementation Plan: Harden Command Contracts and Review Evidence

**Branch**: `008-command-contract-hardening` | **Date**: 2026-09-03 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/008-command-contract-hardening/spec.md`

**Note**: This plan covers roadmap entry 011. The active checkout is a detached Codex worktree based on the current `develop` commit; the feature identifier above is resolved from `.specify/feature.json`.

## Summary

Harden the four Diagram Roadmap commands by making their input, evidence, lifecycle, report, and failure contracts explicit. Preserve `load_config.py` as the verified configuration and containment authority, add one focused Python `review_contract.py` helper for deterministic review mechanics, and keep synthesis and drift judgment in the command bodies. Update the shared report template, source and installed command surfaces, generated skills, current documentation, packaging metadata, and the standard-library contract suite. Validate judgment-bearing behavior through bounded disposable-project dogfood scenarios and preserve merged historical artifacts unchanged.

## Technical Context

**Language/Version**: Python 3.11.16 for extension-owned deterministic mechanics; Markdown and YAML for command, template, manifest, and documentation contracts

**Primary Dependencies**: Python standard library, existing `load_config.py` runtime and containment behavior, Specify CLI 1.0.1, and PyYAML 6.0 or newer supplied by the active Specify environment; no new third-party dependency

**Storage**: Repository-owned Markdown roadmap/spec/report artifacts, JSON subprocess contracts, YAML extension configuration, and Git repository state; no database

**Testing**: Standard-library `unittest` discovery through `mise run test`, disposable Git repositories, installation and dogfood parity tests, command-contract assertions, manual judgment scenarios, `git diff --check`, and protected-surface comparison

**Target Platform**: macOS and Linux; Windows, Bash, and PowerShell remain out of scope

**Project Type**: GitHub Spec Kit extension containing four agent command workflows, two Python deterministic entrypoints after this feature, shared templates, and generated Codex skills

**Performance Goals**: Deterministic helpers enumerate the complete bounded target or delta without silent truncation and return one compact result per invocation; correctness, containment, and reproducibility take priority over latency

**Constraints**: Preserve the no-argument six-field `load_config.py` contract and existing path-validation behavior; no network access; no machine-global evidence; no unsupported baseline inference; no report overwrite; no mutation outside the roadmap write or allocated report path; no semantic edits to merged feature directories, dated reports, released changelog history, or verified evidence for entries 001 through 010

**Scale/Scope**: Four command files, one existing loader, one new review helper, one shared report template, one manifest/allowlist pair, four generated skills, the installed dogfood mirror, current README/test guidance, and focused additions to the existing 80-test Python suite plus manual acceptance scenarios

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

- **I. Canonical Conformance — PASS**: The design keeps the valid extension layout, declares the new Python helper in `extension.yml`, updates `.extensionignore`, refreshes the installed snapshot and generated skills, and retains exact Specify CLI 1.0.1 compatibility.
- **II. Determinism Split — PASS**: `review_contract.py` owns exact path and target candidates, Git revision validation, delta manifests, timestamps, collision handling, counts, verdicts, and lifecycle gates. Command bodies continue to own source interpretation, title similarity, drift judgment, severity/category selection, explanations, and remediation.
- **III. Non-Destructive & Idempotent — PASS**: Write authorization is explicit; review commands preserve roadmap, spec, and implementation sources and write only one atomically reserved report. The constitution's phrase “STRICTLY READ-ONLY” is interpreted operationally as source/governance read-only with the documented report as the sole permitted write, matching the same principle's existing statement that reviews emit reports.
- **IV. Roadmap as Durable Governance — PASS**: The design protects roadmap provenance, requires confirmation for inferred durable changes, and does not change the roadmap format or lifecycle vocabulary.
- **V. Supported Platforms and Python Scripting — PASS**: The only new runtime automation is Python and uses the existing project toolchain on macOS and Linux. No shell or Windows compatibility layer is introduced.
- **VI. Elicitation Completeness — PASS**: Interactive inferred changes require confirmation; genuine gaps remain proposals or open questions; unattended execution cannot fabricate consent.
- **VII. Dogfood the Workflow — PASS**: Feature 008 is specified and planned through Spec Kit, and the design requires disposable-project and repository dogfood evidence before acceptance.
- **Spec Evolution and Merge-Bounded Persistence — PASS**: The work flows forward from verified entries 009 and 010. Specs 001 through 007, dated reports, released history, and earlier validation evidence are protected from semantic change.

### Post-Design Re-evaluation

All gates remain passed after Phase 1. The two-contract split keeps the new helper's deterministic interface explicit without broadening the verified configuration loader into Git and reporting responsibilities. The data model assigns every judgment-bearing decision to the command layer and every reproducible state transition or count to the helper. No constitutional exception or complexity waiver is required.

## Project Structure

### Documentation (this feature)

```text
specs/008-command-contract-hardening/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── command-workflows.md
│   └── review-contract.md
├── checklists/
│   └── requirements.md
├── validation-evidence.md        # implementation-phase acceptance record
└── tasks.md                      # generated later by $speckit-tasks
```

### Source Code (repository root)

```text
commands/
├── speckit.diagram-roadmap.write.md
├── speckit.diagram-roadmap.brief.md
├── speckit.diagram-roadmap.debrief.md
└── speckit.diagram-roadmap.sync.md

scripts/python/
├── load_config.py               # retained configuration and containment authority
└── review_contract.py           # new deterministic review mechanics

templates/
└── review-report-template.md

extension.yml
.extensionignore
README.md
tests/README.md

tests/python/
├── support.py
├── test_commands.py
├── test_command_selection.py    # positive/negative host-selection fixtures
├── test_current_surface.py
├── test_dogfood.py
├── test_installation.py
├── test_protected_history.py    # merge-bounded historical guard
├── test_review_contract.py      # target, lifecycle, findings, and report allocation
└── test_review_delta.py         # Git revision and working-tree delta cases

tests/fixtures/
└── command-selection.json       # maintained positive and adjacent-negative prompts

.specify/extensions/diagram-roadmap/
├── commands/                    # source-command mirrors
├── scripts/python/              # loader and review helper mirrors
├── templates/                   # report-template mirror
└── extension.yml                # manifest mirror

.agents/skills/
└── speckit-diagram-roadmap-*/SKILL.md
```

**Structure Decision**: Keep the repository-root extension layout and its installed dogfood mirror. Preserve `load_config.py` as the focused configuration and path-validation entrypoint. Add one sibling `review_contract.py` entrypoint for mechanics shared by brief, debrief, and sync; it reuses loader runtime, project-root, and containment primitives rather than duplicating them. Write remains on `load_config.py`; the three review command frontmatter entries point to `review_contract.py`, whose default operation returns the same configuration fields those commands require. The manifest and installation allowlist declare both scripts, increasing the installed payload by one source-owned file.
