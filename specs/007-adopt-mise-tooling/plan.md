# Implementation Plan: Adopt mise Tooling

**Branch**: `develop` | **Feature Directory**: `007-adopt-mise-tooling` | **Date**: 2026-09-01 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/007-adopt-mise-tooling/spec.md`

## Summary

Make `mise.toml` the sole current toolchain and task-runner surface, preserving the complete Python contract suite as one truthful `test` task. Pin Python, `uv`, and Specify CLI with an explicit installation dependency graph, remove the unused jq declaration and the Just scaffolding, align current contributor documentation and contract tests, and leave extension runtime, packaging, and merged historical artifacts unchanged.

## Technical Context

**Language/Version**: Python 3.11.16 for the existing contract suite and standard-library TOML inspection; declarative TOML for project tools and tasks

**Primary Dependencies**: mise as an externally installed tool/version manager and task runner; Python 3.11.16, `uv` 0.12.5, and Specify CLI 1.0.1 as mise-managed project tools; Python standard library only for contract-test changes

**Storage**: Repository files only; no database, service, cache, or new generated state

**Testing**: Python standard-library `unittest`, `tomllib` contract inspection, mise task inventory and validation commands, an isolated missing-tool check with disposable mise state, end-to-end `mise run test`, current-surface scans, comparison with a pre-implementation protected-surface baseline, `git diff --check`, and macOS/Linux acceptance evidence

**Target Platform**: macOS and Linux development hosts; Windows remains out of scope

**Project Type**: Spec Kit extension repository with contributor-facing development automation

**Performance Goals**: No new runtime performance target; the canonical task adds no bootstrap work and runs the same complete discovered suite with negligible task-runner overhead

**Constraints**: mise is canonical; setup is the explicit sequence review/trust → install → test; project task auto-install is disabled so validation never installs or trusts; missing-tool behavior is tested only with disposable mise configuration, data, cache, and state directories; repository-root invocation only; exactly one real project task; no Just, placeholder tasks, unconfigured lint task, duplicate lower-level workflow, unrelated dependency, lockfile, or additional task runner; `uv` is retained only as the pinned installer required by the Specify CLI backend; extension runtime, packaging rules, generated skills, and payload remain byte-stable against a baseline recorded before implementation; merged specs, dated reports, and released history remain unchanged against that baseline

**Scale/Scope**: One tool configuration, one task, three exact tool declarations connected by one installation dependency edge, one removed unused declaration, two current documentation files, one current-surface test module, one deleted task-runner file, two supported operating systems, and no extension payload changes

## Constitution Check

The feature passes the pre-research gate and, after Phase 1 design, continues to pass every applicable principle.

- **I. Canonical Conformance — PASS**: The extension manifest, commands, Python runtime, templates, configuration, and installed payload are outside the change set. Contributor automation remains development-only and excluded by the existing packaging allowlist.
- **II. Determinism Split — PASS**: The mise task is one literal executable invocation. Contract assertions and current-surface classification remain deterministic Python tests; no judgment is embedded in scripts or task configuration.
- **III. Non-Destructive & Idempotent — PASS**: Setup and validation do not mutate user-authored extension content. Tool installation remains an explicit contributor action, task auto-install is disabled, and failure remains visible. The pinned `uv` dependency makes clean setup deterministic instead of relying on ambient global state. Historical artifacts are not rewritten.
- **IV. Roadmap as Durable Governance — PASS**: Roadmap entry 010 records the outcome, boundary, dependency, and canonical-tool decision. This feature implements that entry without changing roadmap semantics.
- **V. Supported Platforms and Python Scripting — PASS**: The maintained test suite remains Python-only and the canonical task is validated on macOS and Linux. TOML contains no shell control flow or alternate runtime implementation.
- **VI. Elicitation Completeness — PASS**: The feature does not change roadmap-write elicitation. Its own specification has no unresolved clarification markers.
- **VII. Dogfood the Workflow — PASS**: Feature 007 proceeds through specify → clarify → plan and will run roadmap briefing before implementation, analyze after tasking, converge after implementation, and debrief after completion.
- **Merge-Bounded Persistence — PASS**: The tooling change flows forward from verified feature 006 into a new feature directory. Merged feature directories, dated reports, and released history remain unchanged.

Post-design re-evaluation found no new violations. No complexity exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/007-adopt-mise-tooling/
├── checklists/
│   └── requirements.md
├── contracts/
│   └── tooling-contract.md
├── data-model.md
├── plan.md
├── quickstart.md
├── research.md
└── spec.md
```

### Source Code (repository root)

```text
mise.toml                              # canonical tool declarations and test task
README.md                              # first-use setup and canonical validation
tests/
├── README.md                          # test-focused canonical workflow
└── python/
    └── test_current_surface.py        # exact tooling/docs/history boundary contract
justfile                               # removed by this feature

commands/                              # unchanged extension runtime
scripts/                               # unchanged extension runtime
templates/                             # unchanged extension runtime
extension.yml                          # unchanged extension manifest
.extensionignore                       # unchanged packaging boundary
.specify/extensions/diagram-roadmap/   # unchanged ignored dogfood payload
.agents/skills/speckit-diagram-roadmap-*/ # unchanged generated command skills
specs/001-*/ through specs/006-*/       # unchanged merged history
CHANGELOG.md                            # unchanged released history
```

**Structure Decision**: Keep the change in the repository's existing root-level contributor surfaces. The single short task belongs inline in `mise.toml`; a `.mise/tasks/` script would add indirection without reusable logic. Extend the existing current-surface test module rather than creating a new framework or suite. The contributor-facing command contract is recorded under this feature's `contracts/` directory because the task names and setup sequence are public project interfaces.

## Complexity Tracking

No constitutional violations require justification.
