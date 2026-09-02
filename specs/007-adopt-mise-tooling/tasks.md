# Tasks: Adopt mise Tooling

**Input**: Design documents from `/specs/007-adopt-mise-tooling/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/tooling-contract.md](contracts/tooling-contract.md), [quickstart.md](quickstart.md)

**Tests**: The feature requires deterministic contract tests for the exact mise tools, settings, task inventory, current documentation, and current-versus-historical boundary. Story test tasks precede the behavior they protect.

**Organization**: Tasks are grouped by prioritized user story so each story has an explicit goal, independent test, and checkpoint.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because the tasks use different files or operating-system environments and do not depend on incomplete work.
- **[Story]**: Maps a task to User Story 1, 2, or 3 from [spec.md](spec.md).
- Every task names the exact repository file or feature artifact it changes, validates, or produces.

## Phase 1: Setup and Roadmap Alignment

This phase establishes the roadmap context that must govern implementation.

- [X] T001 Run `$speckit-diagram-roadmap-brief` for `specs/007-adopt-mise-tooling/spec.md`, verify it matches roadmap entry 010 and dependency 009, save the pre-implementation report under `specs/007-adopt-mise-tooling/roadmap-reviews/`, and record the protected-path status, binary diff, and sorted path-to-object manifest in `specs/007-adopt-mise-tooling/roadmap-reviews/protected-surface-baseline.md` using `specs/007-adopt-mise-tooling/quickstart.md` before changing implementation surfaces

**Checkpoint**: The active feature is matched to roadmap entry 010 with no must-address pre-implementation drift, and pre-existing protected-path state has a deterministic baseline for later comparison.

## Phase 2: Foundational Current-Surface Test Support

This blocking phase prepares the one existing test module shared by all three stories without changing project behavior.

- [X] T002 Add standard-library `tomllib` loading plus reusable root `mise.toml`, `README.md`, and `tests/README.md` access helpers in `tests/python/test_current_surface.py`

**Checkpoint**: Shared deterministic test support exists; user-story contract tests can now be added without introducing another test module or dependency.

## Phase 3: User Story 1 — Run the Canonical Project Validation (Priority: P1) 🎯 MVP

**Goal**: Provide one root-level `mise run test` entrypoint that runs the complete discovered Python contract suite in the declared environment and never bootstraps missing tools.

**Independent Test**: After explicit review/trust and `mise install`, run `mise run test` from the repository root on macOS and Linux; all discovered tests run, failures propagate non-zero, and missing tools are not installed implicitly.

### Tests for User Story 1

- [X] T003 [US1] Add failing assertions for Python 3.11.16, pinned `uv` 0.12.5, Specify CLI 1.0.1 with installation dependencies on Python and `uv`, `settings.task.run_auto_install = false`, the `test` task's description and exact direct unittest-discovery command, and absence of nested setup or `mise exec` in `tests/python/test_current_surface.py`

### Implementation for User Story 1

- [X] T004 [US1] Pin Python 3.11.16 and `uv` 0.12.5, retain Specify CLI 1.0.1 with explicit installation dependencies on Python and `uv`, remove the unused jq declaration, disable task auto-install, and define the single direct `test` task in `mise.toml`
- [X] T005 [P] [US1] From the repository root on macOS, follow the setup sequence and verify task validation, full discovery, and truthful exit propagation; verify missing-tool non-bootstrap behavior only in the disposable repository and isolated mise directories defined by `specs/007-adopt-mise-tooling/quickstart.md`
- [X] T006 [P] [US1] From the repository root on a real Linux host or separately approved CI job, run the same setup, discovery, and exit-propagation checks; repeat the missing-tool check only with the disposable repository and isolated mise directories defined by `specs/007-adopt-mise-tooling/quickstart.md`

**Checkpoint**: User Story 1 is complete when the canonical task runs the entire suite with the same pass/fail semantics on macOS and Linux and performs no implicit setup.

## Phase 4: User Story 2 — Discover One Trustworthy Task Surface (Priority: P2)

**Goal**: Expose exactly one real local task and remove Just, unused declarations, placeholders, and the unconfigured lint recipe from the maintained project surface.

**Independent Test**: Inspect parsed `mise.toml` and `mise tasks ls --local --name-only`; both report exactly `test`, every retained tool has a current consumer, task validation succeeds, and the root `justfile` is absent regardless of globally installed executables.

### Tests for User Story 2

- [X] T007 [US2] Extend `tests/python/test_current_surface.py` with failing exact-inventory assertions for only Python, `uv`, and Specify CLI tools with the required installation edge, only the `test` task, disabled task auto-install, no default/lint/build/dev/clean placeholders, and no root `justfile`

### Implementation for User Story 2

- [X] T008 [US2] Delete the root `justfile` without creating replacement default, lint, build, dev, or clean tasks
- [X] T009 [US2] Validate the exact local task inventory and configuration with `mise tasks ls --local --name-only`, `mise tasks validate --errors-only`, and `tests/python/test_current_surface.py` against `specs/007-adopt-mise-tooling/contracts/tooling-contract.md`

**Checkpoint**: User Story 2 is complete when task discovery is exact and trustworthy, syntax validation passes, and Just or global pre-commit availability cannot restore a removed project workflow.

## Phase 5: User Story 3 — Follow Current Guidance Without Rewriting History (Priority: P3)

**Goal**: Make current README and test guidance consistently describe explicit mise setup and the one root-level test task while preserving accepted historical artifacts and the extension payload.

**Independent Test**: Scan only maintained current surfaces and verify ordered review/trust → install → test guidance, repository-root invocation, one canonical command, no `just test` or duplicate lower-level workflow, and no new implementation delta under merged specs, dated reports, released history, runtime source, packaging rules, generated skills, or the installed payload.

### Tests for User Story 3

- [X] T010 [US3] Extend `tests/python/test_current_surface.py` with failing current-documentation assertions for the ordered setup sequence, repository-root requirement, `mise run test` as the sole canonical entrypoint, absence of `just test` and the duplicate lower-level invocation, and explicit exclusion of historical artifacts from current-surface scanning

### Implementation for User Story 3

- [X] T011 [P] [US3] Replace the README development command with review/trust, `mise install`, and repository-root `mise run test` guidance in `README.md`
- [X] T012 [P] [US3] Replace `just test` and the duplicate direct unittest command with the same canonical root-level mise workflow in `tests/README.md`
- [X] T013 [US3] Run the complete current-surface contract in `tests/python/test_current_surface.py`, recreate the protected-path status, binary diff, and sorted path-to-object manifest using `specs/007-adopt-mise-tooling/quickstart.md`, and compare them with `specs/007-adopt-mise-tooling/roadmap-reviews/protected-surface-baseline.md` to confirm protected history, runtime, packaging, generated-skill, and dogfood-payload paths gained no feature-007 changes

**Checkpoint**: User Story 3 is complete when a first-time contributor can follow current documentation successfully and every older task-runner reference remains confined to accepted history.

## Phase 6: Polish and Cross-Cutting Validation

This phase consolidates platform evidence and closes repository, convergence, and roadmap-review gates.

- [X] T014 Record actual macOS and Linux task validation, complete-suite results, and Python/`uv`/Specify versions from T005 and T006 in the platform matrix in `specs/007-adopt-mise-tooling/quickstart.md`
- [X] T015 Run `git diff --check`, scoped privacy and task-runner scans, exact task/settings/tool assertions, the complete `mise run test` workflow, and an exact protected-path baseline comparison using `specs/007-adopt-mise-tooling/quickstart.md`
- [X] T016 Run `$speckit-converge` against `specs/007-adopt-mise-tooling/` and complete every task it appends to `specs/007-adopt-mise-tooling/tasks.md` until no spec, plan, task, implementation, or validation gap remains
- [X] T017 Run `$speckit-diagram-roadmap-debrief` against the completed feature and save its read-only outcome/scope drift report under `specs/007-adopt-mise-tooling/roadmap-reviews/`

**Checkpoint**: The feature is converged, cross-platform evidence is recorded, the protected boundary is intact, and the roadmap debrief has no must-address implementation drift.

## Dependencies and Execution Order

The work is small but intentionally serialized where tasks modify the shared current-surface test module or establish a contract consumed by a later story.

### Phase Dependencies

- **Phase 1 — Setup**: Starts immediately and must confirm roadmap alignment.
- **Phase 2 — Foundational**: Depends on T001 and blocks all user-story test work.
- **Phase 3 — User Story 1**: Depends on T002; T003 must precede T004, then T005 and T006 may run in parallel.
- **Phase 4 — User Story 2**: Depends on T004 because it validates the canonical task configuration; T007 precedes T008 and T009.
- **Phase 5 — User Story 3**: Its documentation is conceptually independent after T002, but T010 follows T009 to avoid concurrent edits to `tests/python/test_current_surface.py`; T011 and T012 then run in parallel before T013.
- **Phase 6 — Polish**: Depends on all three story checkpoints and both platform runs.

### Dependency Graph

```text
T001 → T002 → T003 → T004
T004 → T005
T004 → T006
T004 → T007 → T008 → T009 → T010
T010 → T011
T010 → T012
T009 + T011 + T012 → T013
T005 + T006 + T013 → T014 → T015 → T016 → T017
```

### User Story Dependencies

- **User Story 1 (P1)**: Starts after T002 and provides the MVP canonical test task.
- **User Story 2 (P2)**: Depends on User Story 1's task configuration but has its own independently testable exact-inventory and Just-removal outcome.
- **User Story 3 (P3)**: Current documentation can be authored independently, but final validation depends on the canonical task and Just removal from User Stories 1 and 2.

### Within Each User Story

- Add the story's deterministic failing contract assertions before the behavior or documentation change they protect.
- Change the smallest current surface that satisfies those assertions.
- Run the story's independent test before proceeding to the next priority.
- Do not stage, commit, refresh the extension installation, or rewrite historical files as part of these tasks.

## Parallel Opportunities

Only work packets with different files or execution environments are marked parallel.

- **User Story 1**: T005 and T006 run the same accepted workflow on separate operating systems.
- **User Story 3**: T011 changes `README.md` while T012 changes `tests/README.md`.
- User-story test tasks are not parallel because they modify the same `tests/python/test_current_surface.py` file.
- User Stories 2 and 3 retain separate acceptance boundaries even though their safest implementation order is sequential.

## Parallel Examples

The examples describe independent work packets rather than shell orchestration.

### User Story 1

```text
T005: macOS canonical-task acceptance using specs/007-adopt-mise-tooling/quickstart.md
T006: Linux canonical-task acceptance using specs/007-adopt-mise-tooling/quickstart.md
```

### User Story 3

```text
T011: current setup and validation guidance in README.md
T012: current test workflow in tests/README.md
```

## Implementation Strategy

The implementation preserves a reviewable MVP and adds stricter discovery and documentation contracts incrementally.

### MVP First

1. Complete T001–T002.
2. Complete User Story 1 through T006.
3. Stop and verify the canonical task independently on macOS and Linux.
4. Do not remove Just until the mise task has passed the MVP checkpoint.

### Incremental Delivery

1. **Foundation**: Confirm roadmap alignment and prepare shared test support.
2. **User Story 1**: Establish the canonical task and cross-platform execution.
3. **User Story 2**: Lock the exact inventory and remove the misleading Just surface.
4. **User Story 3**: Align current guidance and verify the historical/package boundary.
5. **Polish**: Consolidate evidence, run full validation, converge, and debrief.

### Review Gates

Run `$speckit-analyze` after this task list is accepted and before `$speckit-implement`. After implementation, T016 requires convergence until no gaps remain; T017 then performs the roadmap debrief. Explicit user acceptance remains separate from automated completion.

## Notes

- `[P]` tasks are limited to separate operating-system runs or separate documentation files.
- The suite discovers tests dynamically; no task may hardcode the current count.
- `mise tasks validate --errors-only` is necessary but insufficient because an empty task inventory can validate successfully; exact TOML and local task-list assertions are mandatory.
- The task body invokes Python directly because `mise run` already activates declared tools.
- `settings.task.run_auto_install = false` is required so missing tools fail visibly instead of being installed during validation.
- Preserve all pre-existing staged and untracked work outside feature-007 implementation scope.
