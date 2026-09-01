# Implementation Plan: Python Script Migration

**Branch**: `python` | **Date**: 2026-08-31 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/006-python-script-migration/spec.md`

## Summary

Replace the extension-owned Bash and PowerShell configuration loaders with one self-contained Python loader, migrate all four command contracts and current automation to Python, and narrow supported platforms to macOS and Linux. Preserve the six-field JSON contract while adding strict PyYAML validation, project containment, and fail-closed execution under the active Specify installation's exact Python 3.11.16 interpreter. Remove obsolete shell implementations and parity tests, refresh the reviewed installed payload and generated skills, and preserve merged historical artifacts unchanged.

## Technical Context

This feature changes the deterministic runtime boundary, extension packaging, generated command metadata, automated tests, and current project documentation without changing the four commands' judgment-bearing workflows.

**Language/Version**: Python 3.11.16 exactly; YAML, JSON, and Markdown declarative artifacts

**Primary Dependencies**: Specify CLI 1.0.1 command integration and installer; the active Specify runtime's PyYAML dependency (currently 6.0.3, minimum 6.0)

**Storage**: Repository files plus installed extension configuration at `.specify/extensions/diagram-roadmap/roadmap-config.yml`; no database or persistent service

**Testing**: Python standard-library `unittest`; disposable `specify extension add --dev --force` and `extension enable`; payload, generated-skill, hook, contract, containment, and current-reference checks on macOS and Linux

**Target Platform**: macOS and Linux; Windows is a non-goal

**Project Type**: Spec Kit extension

**Performance Goals**: One bounded local configuration parse and fixed existence checks per invocation; no network access, recursive project scan, or persistent process

**Constraints**: Python-only maintained scripting; Specify CLI 1.0.1 exactly; exact active-Specify canonical interpreter and virtual-environment match while re-executing through the original shebang path; isolated PyYAML 6.0-or-newer import; no vendored parser or line-based fallback; no project-controlled imports; project-relative contained paths revalidated immediately before every content access; roadmap creation permits a contained nonexistent target only when its existing parent chain remains contained, while an existing target must be a regular file; stable six-field JSON success output; empty stdout on failure; read-only review commands; no rewrite of merged history

**Scale/Scope**: Four commands, one Python loader with default resolution plus four concrete-path validation kinds, six output fields, four environment overrides, four configuration sections, three hooks, one 11-file installed runtime payload, four generated skills, and a two-operating-system validation matrix

## Constitution Check

The feature passed the pre-research gate and passes again after Phase 1 design.

- **I. Canonical Conformance — PASS**: All four commands use Specify's supported `scripts.py` frontmatter and the manifest ships one Python runtime script. The active Specify interpreter bootstrap compensates for the current generated-command resolver without changing the canonical extension shape.
- **II. Determinism Split — PASS**: Runtime discovery, configuration parsing, validation, containment, existence checks, and JSON serialization remain deterministic Python mechanics. Roadmap synthesis and review judgment remain in command bodies.
- **III. Non-Destructive & Idempotent — PASS**: The loader reads fixed configuration files and emits results without mutating project content. Command bodies revalidate roadmap, ADR, and PRD paths immediately before access; roadmap-write validation protects both existing files and contained creation targets. Brief, debrief, and sync remain read-only; write retains its existing guarded roadmap behavior.
- **IV. Roadmap as Durable Governance — PASS**: The stable roadmap location and precedence contract are preserved. The current roadmap records this migration while merged feature history remains unchanged.
- **V. Supported Platforms and Python Scripting — PASS**: Current extension-owned Bash, PowerShell, Bats, Pester, and parity surfaces are replaced by Python and validated on macOS and Linux. Specify-owned compatibility scripts remain outside this extension's maintained surface and are no longer referenced.
- **VI. Elicitation Completeness — PASS**: The migration does not alter the write command's interaction or no-fabrication rules.
- **VII. Dogfood the Workflow — PASS**: Feature 006 follows specify → clarify → plan and requires a refreshed disposable and repository dogfood installation before completion.
- **Merge-Bounded Persistence — PASS**: Runtime research flowed back into FR-023, SC-008, and the assumptions before design continued. Features 001–005 and dated reports remain historical; analyze is required after tasking and converge after implementation.

The isolated re-execution bootstrap is security-sensitive but not a constitutional exception. It is bounded to the active POSIX `specify` console script, verifies the canonical interpreter binary and virtual-environment prefix, executes the original absolute shebang path so the verified environment remains active, verifies the exact interpreter version, refuses unsupported wrappers, re-executes at most once, and has no arbitrary-runtime fallback. A future Specify runner that directly invokes extension scripts with `sys.executable -I` should replace this compatibility boundary.

## Project Structure

The feature retains the extension-at-repository-root layout while consolidating the maintained runtime and tests.

### Documentation (this feature)

```text
specs/006-python-script-migration/
├── checklists/requirements.md
├── contracts/
│   ├── load-config.schema.json
│   ├── loader-contract.md
│   └── roadmap-config.schema.json
├── data-model.md
├── plan.md
├── quickstart.md
├── research.md
└── spec.md
```

### Source Code (repository root)

```text
extension.yml
.extensionignore
commands/
├── speckit.diagram-roadmap.brief.md
├── speckit.diagram-roadmap.debrief.md
├── speckit.diagram-roadmap.sync.md
└── speckit.diagram-roadmap.write.md
scripts/
└── python/
    └── load_config.py
templates/
├── review-report-template.md
└── roadmap-template.md
config-template.yml
tests/
├── fixtures/
├── python/
│   ├── support.py
│   ├── test_commands.py
│   ├── test_config_resolution.py
│   ├── test_current_surface.py
│   ├── test_dogfood.py
│   ├── test_installation.py
│   ├── test_load_config.py
│   ├── test_output_contract.py
│   ├── test_path_containment.py
│   ├── test_runtime.py
│   └── test_yaml_validation.py
└── README.md
justfile
mise.toml
README.md
CHANGELOG.md
.specify/extensions/diagram-roadmap/       # ignored derived dogfood installation
.agents/skills/speckit-diagram-roadmap-*/ # ignored generated command skills
```

**Structure Decision**: Replace `scripts/bash/` and `scripts/powershell/` with `scripts/python/`, consolidate the three shell-oriented suites under `tests/python/`, and move reusable fixtures to `tests/fixtures/`. Brief and debrief switch their core prerequisite reference to `.specify/scripts/python/check_prerequisites.py`; Specify-owned `.specify/scripts/bash/` files are not extension source and are neither migrated nor deleted. The ignored installed snapshot and generated skills are refreshed from a distinct reviewed source copy after source validation.

## Complexity Tracking

No constitutional violations require justification. The runtime bootstrap exists only because Specify 1.0.1's generated `py:` invocation can select a project or `PATH` interpreter rather than Specify's interpreter; [research.md](research.md) records its limits and preferred future replacement.
