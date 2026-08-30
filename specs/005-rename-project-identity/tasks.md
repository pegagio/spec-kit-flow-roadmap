---

description: "Implementation tasks for the Diagram Roadmap identity migration"
---

# Tasks: Rename Project Identity

**Input**: Design documents from `specs/005-rename-project-identity/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [identity contract](contracts/identity-contract.md), [quickstart.md](quickstart.md)

**Organization**: Tasks are grouped by user story so installation behavior and contributor-facing identity can be validated independently.

## Phase 1: Setup

This phase establishes the canonical manifest identity that all later paths and commands derive from.

- [x] T001 Set the `diagram-roadmap` ID, Diagram Roadmap display name, version `0.2.0`, intended repository URL, canonical commands, and hooks in `extension.yml`

---

## Phase 2: Foundational

This phase aligns the command source filenames and reviewed installation boundary before runtime references change.

- [x] T002 Rename the four command files from `commands/speckit.roadmap.*.md` to `commands/speckit.diagram-roadmap.*.md`
- [x] T003 Update the exact command-file allowlist without expanding the payload in `.extensionignore`

**Checkpoint**: The manifest, command filenames, and package allowlist agree on the new canonical namespace.

---

## Phase 3: User Story 1 - Install the consistently named extension (Priority: P1) 🎯 MVP

**Goal**: Install one `diagram-roadmap` extension whose four commands and all runtime references use the new identity.

**Independent Test**: Install the source into a disposable Spec Kit 1.0.1 project, enable `diagram-roadmap`, verify the exact payload and generated skills, and execute the installed Bash loader.

- [x] T004 [P] [US1] Update command invocations and installed template/script paths in `commands/speckit.diagram-roadmap.write.md`, `commands/speckit.diagram-roadmap.brief.md`, `commands/speckit.diagram-roadmap.debrief.md`, and `commands/speckit.diagram-roadmap.sync.md`
- [x] T005 [P] [US1] Update the installed configuration directory and `SPECKIT_DIAGRAM_ROADMAP_*` override names symmetrically in `scripts/bash/load-config.sh` and `scripts/powershell/load-config.ps1`
- [x] T006 [P] [US1] Update canonical command references in `templates/review-report-template.md`
- [x] T007 [P] [US1] Update renamed installation paths and environment overrides in `config-template.yml`, `tests/README.md`, `tests/bash/fixtures/env.yml`, `tests/bash/load-config.bats`, `tests/parity/parity.bats`, and `tests/powershell/load-config.Tests.ps1`
- [x] T008 [US1] Run the disposable installation, exact payload, generated-skill, hook, executable-mode, and installed Bash loader checks from `specs/005-rename-project-identity/quickstart.md`

**Checkpoint**: User Story 1 is independently complete when Specify installs and runs the renamed extension without obsolete runtime references.

---

## Phase 4: User Story 2 - Understand the renamed project (Priority: P2)

**Goal**: Present the current project and intended repository consistently while preserving accepted historical identity records.

**Independent Test**: Scan current-facing files for the new names and verify that remaining old-name matches are confined to explicit migration text or frozen historical records.

- [x] T009 [P] [US2] Rename the project and update repository, install, command, and configuration guidance in `README.md` and `ORIGINS.md`
- [x] T010 [P] [US2] Add an `Unreleased` identity-migration entry without editing the released `0.1.0` section in `CHANGELOG.md`
- [x] T011 [US2] Reconcile the current project identity and active command/path references in `.specify/memory/constitution.md` and `.specify/memory/roadmap.md`
- [x] T012 [US2] Verify `specs/001-*` through `specs/004-*`, `.specify/memory/roadmap-sync-2026-06-24.md`, and the released `0.1.0` changelog text remain historically unchanged using a scoped repository reference scan

**Checkpoint**: User Story 2 is independently complete when current-facing identity is consistent and frozen records preserve their accepted terminology.

---

## Phase 5: Polish & Cross-Cutting Concerns

This phase closes repository-wide formatting, privacy, syntax, test, and convergence gates.

- [x] T013 Run `git diff --check`, Bash syntax, payload symlink/privacy scans, and every locally available Bats or PowerShell suite documented in `specs/005-rename-project-identity/quickstart.md`
- [x] T014 Run the Spec Kit converge workflow against `specs/005-rename-project-identity/` and append or complete any tasks required to close remaining implementation gaps

---

## Dependencies & Execution Order

The manifest identity is the root dependency for the filename, runtime, and documentation changes.

- **Phase 1**: Starts immediately.
- **Phase 2**: Depends on T001 and blocks installation work.
- **User Story 1**: Depends on Phase 2. T004–T007 can proceed in parallel; T008 depends on all four.
- **User Story 2**: Depends on the identity contract in T001 but can otherwise proceed alongside T004–T007. T012 depends on T009–T011.
- **Polish**: Depends on both user stories.

## Parallel Example

After T001–T003, these independent file groups can be updated together:

```text
T004: command bodies
T005: platform loaders
T006: shared template
T007: platform tests
T009: README and origins
T010: changelog
```

## Implementation Strategy

Complete User Story 1 first as the MVP because a correct installation proves the extension identity contract. Then finish current-facing documentation and governance reconciliation in User Story 2, preserving the explicitly bounded historical records. Close with the full validation and convergence gates.

## Notes

- `[P]` tasks modify independent file groups.
- GitHub repository and local checkout rename operations are not implementation tasks; the user completed them directly before the feature change set closed, and their resulting names are part of the accepted final state.
- Do not add compatibility aliases or automatic migration behavior.
- Do not commit, push, or perform external repository or checkout rename operations as part of these implementation tasks.

## Phase 6: Convergence

This phase closes the two partial documentation/state gaps found by the post-implementation assessment.

- [x] T015 Add the explicit preserve, remove, reinstall, enable, and configuration-reconciliation procedure for existing `roadmap` installations to `README.md` per the plan migration decision (partial)
- [x] T016 Mark identity-migration entry 008 verified in `.specify/memory/roadmap.md` after the installation and historical-boundary checks pass per FR-004 (partial)

---

## Phase 7: Final Flow-Back Reconciliation

This phase reconciles the accepted external repository and checkout rename state across the mutable feature artifacts before the amended commit is reviewed.

- [x] T017 Flow the completed GitHub repository and local checkout identities back through `spec.md`, `plan.md`, `tasks.md`, and `quickstart.md` while preserving user ownership of the external operations per FR-010
- [x] T018 Run the Spec Kit analyze and converge workflows after the consequential reconciliation and close any remaining artifact or implementation gaps
