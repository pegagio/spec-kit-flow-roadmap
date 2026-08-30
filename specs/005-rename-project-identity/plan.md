# Implementation Plan: Rename Project Identity

**Branch**: `naming` | **Date**: 2026-08-30 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/005-rename-project-identity/spec.md`

## Summary

Rename the active project identity to Diagram Roadmap, prepare current repository references for `pegagio/spec-kit-diagram-roadmap`, change the extension ID to `diagram-roadmap`, and migrate its canonical command namespace, environment overrides, and installed runtime paths to `speckit.diagram-roadmap.*`, `SPECKIT_DIAGRAM_ROADMAP_*`, and `.specify/extensions/diagram-roadmap/`. Preserve released and merged historical records, retain the exact reviewed extension payload, and validate the result through a disposable Spec Kit 1.0.1 installation.

## Technical Context

This feature changes declarative extension metadata, Markdown command contracts, shell path constants, tests, and current project documentation without introducing a new runtime component.

**Language/Version**: YAML 1.2-compatible manifest, Markdown, Bash 3.2+, PowerShell 7+

**Primary Dependencies**: Specify CLI 1.0.1 extension installer and command registrar

**Storage**: Repository files and the installed `.specify/extensions/diagram-roadmap/roadmap-config.yml` configuration scaffold

**Testing**: Disposable `specify extension add --dev` and `extension enable`; Bats and Pester suites when available; shell syntax, JSON-output, payload, and repository reference checks

**Target Platform**: Spec Kit projects on macOS, Linux, and Windows

**Project Type**: Spec Kit extension

**Performance Goals**: Installation and command registration complete in one normal local invocation with no additional runtime overhead

**Constraints**: Preserve version `0.2.0`; no legacy aliases; GitHub repository and local checkout rename operations remain user-owned external actions even though their completed state is part of the accepted feature outcome; no rewriting merged feature records or released changelog history; no expansion of the reviewed install payload

**Scale/Scope**: Four commands, two loaders, one configuration template, one shared report template, three test suites, extension metadata, current governance/project documentation, and one installation allowlist

## Constitution Check

The feature passes all constitutional gates before design and remains compliant after design.

- **I. Canonical Conformance — PASS**: The extension ID and all primary commands satisfy `speckit.{id}.{command}`; the disposable installation is the conformance gate.
- **II. Determinism Split — PASS**: Only deterministic path constants and declarative names change; no judgment moves into scripts.
- **III. Non-Destructive & Idempotent — PASS**: Existing user configuration is not mutated automatically; migration is explicit and preserves the old configuration until verification.
- **IV. Roadmap as Durable Governance — PASS**: The living roadmap is reconciled to the new current identity without rewriting merged feature directories or dated reports.
- **V. Cross-Platform Parity — PASS**: Bash and PowerShell loaders receive equivalent installed-path changes and retain their shared output contract.
- **VI. Elicitation Completeness — PASS**: The rename does not alter roadmap elicitation behavior.
- **VII. Dogfood the Workflow — PASS**: The change has its own feature directory and will be installed into a disposable Spec Kit project before completion.
- **Merge-Bounded Persistence — PASS**: Feature 005 records this later change and explicitly preserves features 001–004 as accepted historical records. Analyze runs after tasking and converge runs after implementation.

## Project Structure

The feature retains the existing extension-at-repository-root structure and changes only identity-bearing active files.

### Documentation (this feature)

```text
specs/005-rename-project-identity/
├── checklists/requirements.md
├── contracts/identity-contract.md
├── data-model.md
├── plan.md
├── quickstart.md
├── research.md
├── spec.md
└── tasks.md
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
├── bash/load-config.sh
└── powershell/load-config.ps1
templates/review-report-template.md
config-template.yml
tests/
├── bash/load-config.bats
├── parity/parity.bats
└── powershell/load-config.Tests.ps1
README.md
ORIGINS.md
CHANGELOG.md
.specify/memory/
├── constitution.md
└── roadmap.md
```

**Structure Decision**: Keep the existing extension layout. Rename command files to match their canonical command IDs, update both platform loaders symmetrically, and leave `specs/001-*` through `specs/004-*`, `.specify/memory/roadmap-sync-2026-06-24.md`, and the released `0.1.0` changelog entry unchanged as historical records.

## Complexity Tracking

No constitutional violations or exceptional complexity are required.
