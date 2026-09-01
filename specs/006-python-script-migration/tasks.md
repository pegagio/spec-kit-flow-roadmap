---
description: "Implementation tasks for the Diagram Roadmap Python script migration"
---

# Tasks: Python Script Migration

**Input**: Design documents from `specs/006-python-script-migration/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [loader contract](contracts/loader-contract.md), [configuration schema](contracts/roadmap-config.schema.json), [output schema](contracts/load-config.schema.json), [quickstart.md](quickstart.md)

**Tests**: Mandatory for the deterministic Python runtime, configuration, containment, packaging, and command-prerequisite contracts on macOS and Linux. Judgment-bearing command behavior is validated by dogfood scenarios rather than unit tests.

**Organization**: Tasks are grouped by user story after a shared Python runtime foundation. Every user story has an independent acceptance path, and current historical records remain outside the migration-edit boundary.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: The task can run in parallel because it targets a different file group and has no incomplete dependency.
- **[Story]**: The user story served by the task: `[US1]`, `[US2]`, or `[US3]`.
- Every task names the repository-relative file or directory it changes or validates.

## Phase 1: Setup

This phase establishes the Python test layout and reusable fixtures without changing runtime behavior.

- [X] T001 Move the reusable YAML fixtures from `tests/bash/fixtures/` to `tests/fixtures/`, replace the invalid unquoted glob scalar in `tests/fixtures/valid.yml` with valid quoted YAML, and preserve the defaults, environment, and invalid-value cases
- [X] T002 [P] Create the subprocess, temporary source-layout, temporary installed-layout, environment-isolation, and stdout/stderr assertion helpers in `tests/python/support.py`

**Checkpoint**: Shared fixtures and test infrastructure exist without introducing a new test dependency.

## Phase 2: Foundational Python Runtime

This phase is blocking. It creates the trusted interpreter boundary and a minimally complete six-field loader contract that every user story uses.

- [X] T003 Add failing tests for active-`specify` interpreter discovery, canonical binary and virtual-environment identity, exact Python 3.11.16 enforcement, isolated re-execution, unsupported wrappers, missing executables, hostile `PYTHONPATH`, project-local `yaml.py`, source/installed root discovery, and alien working directories in `tests/python/test_runtime.py`
- [X] T004 Implement the standard-library-only Specify console-script bootstrap, canonical binary and virtual-environment comparison, one-time `-I` re-execution through the original shebang path, exact Python version check, isolated PyYAML import with rejection below version 6.0, source/installed root discovery, fixed bounded non-symlink regular-file reads, and single-line failure boundary in `scripts/python/load_config.py`
- [X] T005 Add failing smoke tests for built-in defaults, installed configuration loading, the exact six-field JSON object, empty stdout on failure, and `--validate-path` success/failure shapes for `roadmap-read`, `roadmap-write`, `adr`, and `prd` in `tests/python/test_load_config.py`
- [X] T006 Implement strict SafeLoader construction, the documented four-section configuration model, built-in defaults, per-leaf source selection, basic project containment, existence checks, compact UTF-8 JSON serialization, and four-kind `--validate-path` dispatch in `scripts/python/load_config.py`
- [X] T007 Mark `scripts/python/load_config.py` executable and verify its source mode and installed mode both satisfy `specs/006-python-script-migration/contracts/loader-contract.md`

**Checkpoint**: The shared Python entrypoint runs under the verified Specify interpreter and provides the minimum complete contract required by all commands.

## Phase 3: User Story 1 - Run commands on supported platforms (Priority: P1) 🎯 MVP

**Goal**: Install Diagram Roadmap on macOS and Linux and run all four commands' deterministic prerequisite paths without Bash or PowerShell.

**Independent Test**: Install a distinct reviewed source copy into disposable projects on macOS and Linux, enable `diagram-roadmap`, verify all four generated skills and three hooks, and execute every command prerequisite path through the installed Python loader.

### Tests for User Story 1

These tests are written before command and packaging metadata changes.

- [X] T008 [P] [US1] Add failing assertions for one `scripts.py` frontmatter entry per command, Python core prerequisite references in brief/debrief, immediate `roadmap-read`, `roadmap-write`, `adr`, and `prd` validation before each corresponding content access, and absence of `sh`, `ps`, or platform-specific loader prose in `tests/python/test_commands.py`
- [X] T009 [P] [US1] Add failing disposable-install assertions for the exact Specify CLI 1.0.1 manifest requirement, exact 11-file payload, executable Python loader, four generated skills, three registered hooks, byte parity for every source-owned installed file, semantic validation of the newly scaffolded `roadmap-config.yml`, and absence of repository metadata or development files in `tests/python/test_installation.py`

### Implementation for User Story 1

These tasks migrate the user-facing command and installation contract.

- [X] T010 [P] [US1] Replace paired script frontmatter and platform-specific loader instructions with the single Python loader, switch brief/debrief to `.specify/scripts/python/check_prerequisites.py`, and require immediate kind-specific loader validation for every roadmap read or write, ADR directory access, and concrete PRD match in `commands/speckit.diagram-roadmap.write.md`, `commands/speckit.diagram-roadmap.brief.md`, `commands/speckit.diagram-roadmap.debrief.md`, and `commands/speckit.diagram-roadmap.sync.md`
- [X] T011 [P] [US1] Set `requires.speckit_version` to `==1.0.1`, replace the paired script declarations with `load-config-python` in `extension.yml`, and narrow the script allowlist to `scripts/python/load_config.py` in `.extensionignore`
- [X] T012 [P] [US1] Run the User Story 1 command, installation, payload, generated-skill, and hook checks on macOS using `tests/python/test_commands.py`, `tests/python/test_installation.py`, and `specs/006-python-script-migration/quickstart.md`
- [X] T013 [P] [US1] Run the same User Story 1 command, installation, payload, generated-skill, and hook checks on a real Linux host, container, or separately approved CI job using `tests/python/test_commands.py`, `tests/python/test_installation.py`, and `specs/006-python-script-migration/quickstart.md`

**Checkpoint**: User Story 1 is complete when the same four installed command prerequisites work on macOS and Linux with no Bash or PowerShell runtime dependency.

## Phase 4: User Story 2 - Preserve deterministic configuration behavior (Priority: P2)

**Goal**: Preserve the established configuration fields and precedence while enforcing strict YAML, exact runtime, stable error, and project-containment contracts.

**Independent Test**: Run the Python contract suite over defaults, every precedence source, null and empty fallthrough, special characters, malformed and unknown-key YAML, invalid types, path and symlink escapes, working-directory changes, and concrete-path validation; every valid case emits the expected structure and every invalid case emits no stdout.

### Tests for User Story 2

These contract tests must fail against any missing behavior before the corresponding loader task is completed.

- [X] T014 [P] [US2] Add defaults, independent per-leaf precedence, manifest fallback, null and empty fallthrough, explicit empty glob list, strict CSV environment override, zero findings, and no-filesystem-scan cases in `tests/python/test_config_resolution.py`
- [X] T015 [P] [US2] Add malformed, comments-only, multi-document, unsafe-tag, alias, merge-key, duplicate-key, unknown top-level/nested/deprecated key, oversized-input, wrong-root, wrong-section, wrong-list, boolean, float, negative, non-numeric, symlinked configuration/manifest, directory, FIFO or other non-regular input, internally resolving symlink, and externally resolving symlink cases in `tests/python/test_yaml_validation.py`
- [X] T016 [P] [US2] Add POSIX absolute, Windows drive/UNC, traversal, NUL, home syntax, internal and escaping symlink, dangling escape, nonexistent in-root, glob literal-prefix, wildcard-match revalidation, time-of-check revalidation, and all four `roadmap-read`, `roadmap-write`, `adr`, and `prd` kind/existence cases in `tests/python/test_path_containment.py`
- [X] T017 [P] [US2] Add exact field/type/order, compact UTF-8 output, Unicode, quotes, backslashes, tabs, line breaks, deterministic repetition, empty failure stdout, single sanitized stderr line, no traceback, and `--validate-path` result cases in `tests/python/test_output_contract.py`
- [X] T018 [P] [US2] Extend runtime tests with matching and mismatching Specify versions, missing PyYAML, PyYAML below 6.0, supported PyYAML 6.0 or newer, a project Python that lacks PyYAML, a fake project-local `yaml.py`, hostile `PYTHONPATH`, canonical interpreter aliases, and re-execution loop prevention in `tests/python/test_runtime.py`

### Implementation for User Story 2

These tasks complete the loader behind the already-stable public interface.

- [X] T019 [US2] Complete independent environment → project configuration → manifest default → built-in resolution, strict one-record CSV parsing, null/empty fallthrough, list replacement, and the five ordered default PRD patterns in `scripts/python/load_config.py`
- [X] T020 [US2] Complete the bounded PyYAML SafeLoader subclass and exact structural validation for `roadmap-config.yml` and `extension.yml.defaults`, including duplicate, alias, merge, multi-document, unknown-key, exact-type, and sanitized YAML-error handling in `scripts/python/load_config.py`
- [X] T021 [US2] Complete lexical and canonical containment plus immediate access-time validation for roadmap, ADR, PRD patterns, and concrete matches, including existing symlink ancestors, canonical relative POSIX output, `roadmap-read`, `roadmap-write`, `adr`, and `prd` kind/existence rules, contained nonexistent roadmap creation targets, and no PRD scanning in `scripts/python/load_config.py`
- [X] T022 [US2] Complete atomic six-field serialization, stable types, special-character round trips, one-line diagnostics, traceback suppression, and exact default-mode and `--validate-path` exit/output behavior in `scripts/python/load_config.py`

**Checkpoint**: User Story 2 is complete when every valid fixture satisfies `contracts/load-config.schema.json` and every invalid fixture fails according to `contracts/loader-contract.md` on either supported operating system.

## Phase 5: User Story 3 - Maintain one current scripting surface (Priority: P3)

**Goal**: Leave contributors with one Python implementation, one Python validation workflow, current macOS/Linux documentation, and a refreshed reviewed dogfood installation while preserving accepted history.

**Independent Test**: Scan current source, documentation, task-runner configuration, installed payload, and generated skills for legacy scripting references; verify the exact Python payload and confirm that remaining Bash, PowerShell, or Windows references are confined to explicit non-goal or migration text, merged specs 001–005, dated reports, released changelog entries, superseded roadmap history, or Specify-owned core files.

### Tests for User Story 3

These tests establish the current-versus-historical boundary before legacy files are removed.

- [X] T023 [P] [US3] Add a scoped current-surface scan covering extension source, current documentation, task-runner configuration, and generated skills while explicitly excluding merged specs, dated reports, released changelog sections, superseded roadmap history, and Specify-owned `.specify/scripts/bash/` files in `tests/python/test_current_surface.py`
- [X] T024 [P] [US3] Add dogfood assertions for byte parity of every source-owned installed file, semantic validity and preservation of the project-owned `roadmap-config.yml` outside byte comparison, the exact installed file set, regenerated skill content, hook registration, no symlinks, and no nested `.git` in `tests/python/test_dogfood.py`

### Implementation for User Story 3

These tasks remove obsolete maintained surfaces only after the Python replacement and its tests exist.

- [X] T025 [US3] Remove `scripts/bash/load-config.sh`, `scripts/powershell/load-config.ps1`, `tests/bash/load-config.bats`, `tests/parity/parity.bats`, and `tests/powershell/load-config.Tests.ps1`, then remove their empty extension-owned directories without deleting Specify-owned `.specify/scripts/bash/`
- [X] T026 [US3] Replace the Bash, PowerShell, Bats, Pester, and parity development workflow with the direct Python `unittest` workflow in `justfile` and `tests/README.md`
- [X] T027 [P] [US3] Update current platform, runtime, installation, architecture, and development guidance for Python on macOS and Linux in `README.md`
- [X] T028 [P] [US3] Add the Python migration under `Unreleased` without editing version `0.1.0` history in `CHANGELOG.md`, and update strict configuration and environment-override guidance in `config-template.yml`
- [X] T029 [US3] Refresh `.specify/extensions/diagram-roadmap/` from a distinct reviewed source copy with `specify extension add --dev --force`, preserve, reapply, and semantically validate its project-owned `roadmap-config.yml`, enable the extension, and regenerate `.agents/skills/speckit-diagram-roadmap-write/SKILL.md`, `.agents/skills/speckit-diagram-roadmap-brief/SKILL.md`, `.agents/skills/speckit-diagram-roadmap-debrief/SKILL.md`, and `.agents/skills/speckit-diagram-roadmap-sync/SKILL.md`
- [X] T030 [US3] Run the scoped source, history-boundary, exact installed-payload, generated-skill, hook, symlink, nested-Git, source-owned byte-parity, disposable-scaffold, and preserved dogfood-configuration checks in `tests/python/test_current_surface.py` and `tests/python/test_dogfood.py`

**Checkpoint**: User Story 3 is complete when every maintained and installed surface is Python-only and macOS/Linux-current while accepted historical evidence remains unchanged.

## Phase 6: Polish & Cross-Cutting Validation

This phase closes the complete platform, behavior, dogfood, formatting, privacy, and convergence gates.

- [X] T031 [P] Run the complete `just test` workflow on macOS and verify every suite under `tests/python/` passes with Specify 1.0.1, Python 3.11.16, and Specify-supplied PyYAML 6.0 or newer
- [X] T032 [P] Run the complete `just test` workflow on Linux and verify every suite under `tests/python/` passes with Specify 1.0.1, Python 3.11.16, and Specify-supplied PyYAML 6.0 or newer
- [X] T033 Run `git diff --check` plus scoped privacy, unsupported-runtime, executable-mode, and generated-artifact scans over `scripts/python/`, `commands/`, `tests/python/`, `README.md`, `CHANGELOG.md`, `config-template.yml`, `extension.yml`, `.extensionignore`, `justfile`, and `.specify/extensions/diagram-roadmap/`
- [X] T034 Dogfood roadmap creation and amendment with `speckit.diagram-roadmap.write`, pre-implementation context and drift with `speckit.diagram-roadmap.brief`, implementation drift classification and unapplied status proposal with `speckit.diagram-roadmap.debrief`, and bounded ledger reconciliation with `speckit.diagram-roadmap.sync` using the refreshed `.agents/skills/speckit-diagram-roadmap-*/SKILL.md` files; verify every expected outcome in `specs/006-python-script-migration/quickstart.md`, versioned non-destructive writes, and read-only review behavior
- [X] T035 Run the Spec Kit converge workflow against `specs/006-python-script-migration/` and complete any appended tasks until `spec.md`, `plan.md`, `tasks.md`, implementation, and validation evidence have no known gaps

## Dependencies & Execution Order

The verified Python runtime foundation is the root dependency for every user-facing and maintenance increment.

### Phase Dependencies

The phases execute in this order unless the parallel story opportunities below are used.

- **Setup (Phase 1)**: Starts immediately.
- **Foundational (Phase 2)**: Depends on Setup and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on the foundational loader. It is the MVP installation and command-integration increment.
- **User Story 2 (Phase 4)**: Depends on the foundational loader, but its tests can proceed alongside User Story 1 after Phase 2. Its implementation tasks are sequential because they modify the same Python entrypoint.
- **User Story 3 (Phase 5)**: Depends on User Stories 1 and 2 because legacy runtimes must not be removed until the Python command and configuration contracts pass.
- **Polish (Phase 6)**: Depends on all three user stories.

### User Story Dependencies

Each story has a distinct acceptance boundary even where delivery order is constrained.

- **User Story 1 (P1)**: Starts after T007 and has no dependency on User Story 2 or User Story 3.
- **User Story 2 (P2)**: Starts after T007 and has no dependency on User Story 1; T019–T022 complete sequentially after T014–T018 establish the expected failures.
- **User Story 3 (P3)**: Starts after User Stories 1 and 2 because it removes their replaced files and refreshes their installed outputs.

### Within Each User Story

The implementation order preserves test-first evidence for deterministic behavior.

- Write the story's contract tests and confirm relevant cases fail before changing the associated implementation or metadata.
- Complete shared runtime work before command integration or exhaustive configuration behavior.
- Complete source and metadata changes before refreshing installed snapshots or generated skills.
- Complete macOS and Linux checks before marking a platform-dependent story done.

## Parallel Opportunities

The following tasks target independent files or environments and may proceed concurrently once their stated prerequisites are met.

- **Setup**: T002 can proceed while fixtures are moved in T001.
- **User Story 1**: T008 and T009 can be authored in parallel; after they fail as expected, T010 and T011 can proceed in parallel; T012 and T013 can run in parallel on separate operating systems.
- **User Story 2**: T014–T018 can be authored in parallel in separate test modules; T019–T022 then execute sequentially in `scripts/python/load_config.py`.
- **User Story 3**: T023 and T024 can be authored in parallel; T027 and T028 can proceed in parallel after the current contract is settled.
- **Polish**: T031 and T032 can run in parallel on macOS and Linux.

## Parallel Examples

The examples name complete independent work packets rather than shell orchestration.

### User Story 1

```text
T008: command metadata and prerequisite contract tests
T009: disposable installation and payload tests
T010: four command definitions
T011: manifest and install allowlist
```

### User Story 2

```text
T014: precedence and defaults tests
T015: strict YAML tests
T016: containment tests
T017: output and error tests
T018: runtime isolation tests
```

### User Story 3

```text
T023: scoped current-reference tests
T024: dogfood parity tests
T027: README
T028: changelog and configuration template
```

## Implementation Strategy

The implementation proceeds as a small runnable migration rather than a repository-wide replacement in one step.

### MVP First

Complete Setup and the foundational Python runtime, then deliver User Story 1. Stop and validate disposable installations on both supported operating systems before treating the command integration as usable.

### Incremental Delivery

After the MVP, complete User Story 2 to close strict parsing, containment, and deterministic behavior. Only then complete User Story 3 by deleting replaced files, updating current documentation, and refreshing the installed and generated copies. Finish with full cross-platform and dogfood validation.

### Review Gates

Run `$speckit-analyze` after this task list is accepted and before implementation begins. After implementation, T035 invokes `$speckit-converge`; any work it appends remains part of this mutable feature change set and must be completed before merge.

## Notes

- `[P]` tasks modify independent file groups or run in independent operating-system environments.
- The implementation must not add Bash or PowerShell wrappers, compatibility aliases, vendored YAML, another Python dependency, CI infrastructure, or an alternate runtime fallback.
- Direct single-executable documentation commands are allowed; scripting logic belongs in Python.
- Preserve `specs/001-*` through `specs/005-*`, dated roadmap reports, released changelog entries, superseded roadmap history, and Specify-owned `.specify/scripts/bash/` files.
- Do not stage, commit, push, publish, or delete project-owned configuration as part of these tasks unless separately authorized.

## Phase 7: Convergence

This phase closes the remaining validation gap found after implementation.

- [X] T036 Remove transient Python bytecode from `scripts/python/`, make `tests/python/test_current_surface.py` distinguish maintained runtime source from ignored `__pycache__/` and `*.pyc` artifacts, and rerun the complete documented validation workflow per SC-003 and SC-007 (partial)
