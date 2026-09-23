# Tasks: Rename to FlowKit Roadmap

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [identity contract](contracts/identity-contract.md), [migration contract](contracts/migration-contract.md), and [quickstart.md](quickstart.md).

**Tests**: The spec explicitly requires clean-install, migration, command, hook, configuration, and supported-platform validation. Add or update focused tests before changing the corresponding behavior; keep the four existing purpose contracts intact.

**Organization**: Tasks follow the three prioritized user stories. Paths are repository-relative. `[P]` means the task touches different files and can proceed alongside other marked tasks in its phase after shared prerequisites are complete.

## Phase 1: Setup

**Purpose**: Establish the current identity and installation state before changing source or project registration.

- [X] T001 Inspect `extension.yml`, `.extensionignore`, `commands/`, `.specify/extensions.yml`, `.specify/extensions/.registry`, and `.agents/skills/` against `specs/009-rename-flow-roadmap/contracts/identity-contract.md`; record current command, hook, and generated-skill names for comparison.
- [X] T002 Inspect `.specify/extensions/diagram-roadmap/roadmap-config.yml` and `config-template.yml` for non-default or unfamiliar values, and preserve a readable backup outside `.specify/extensions/diagram-roadmap/` before any dogfood installation change.

## Phase 2: Foundational

**Purpose**: Complete the required post-tasking analysis before any implementation edit, then align shared fixtures for all three stories.

- [X] T003 Verify `specs/009-rename-flow-roadmap/spec.md`, `specs/009-rename-flow-roadmap/plan.md`, and `specs/009-rename-flow-roadmap/tasks.md` agree on the three identity namespaces, manual migration order, historical boundary, and external acceptance gate before implementation; run `$speckit-analyze` and reconcile any findings in those same files.
- [X] T004 Update `tests/python/support.py` fixture manifest and installed payload path for `flow-roadmap`; clear both old and new environment prefixes by default while allowing explicit old-prefix inputs for negative migration tests.

**Checkpoint**: The shared test layout and cross-artifact gate are ready; no source identity has been changed yet.

## Phase 3: User Story 1 - Install the renamed extension (Priority: P1) 🎯 MVP

**Goal**: A clean Spec Kit project installs FlowKit Roadmap under `flow-roadmap` with four working commands, four generated skills, three lifecycle hooks, and the renamed config namespace.

**Independent test**: Install a reviewed source copy into a disposable project and verify exact registered names, generated skills, hooks, Python runtime payload, config resolution, and each command's prerequisite path.

### Tests for User Story 1

- [X] T005 [P] [US1] Change `tests/python/test_installation.py` to expect the `flow-roadmap` manifest, renamed command files, exact twelve-file installed payload, four `speckit-flow-roadmap-*` skills, three hooks, and byte parity with source; confirm the identity assertions fail against old source.
- [X] T006 [P] [US1] Change `tests/python/test_commands.py` and `tests/python/test_command_selection.py` to assert the four `speckit.flow-roadmap.*` command IDs and unchanged purpose dispatch; confirm old command names fail the new assertions.
- [X] T007 [P] [US1] Change `tests/python/test_load_config.py`, `tests/python/test_config_resolution.py`, and `tests/python/test_runtime.py` to assert the new installed config path and `SPECKIT_FLOW_ROADMAP_*` overrides while preserving the six-field runtime contract; confirm the new-name assertions fail against old source.

### Implementation for User Story 1

- [X] T008 [P] [US1] Change `extension.yml` to display FlowKit Roadmap, register ID `flow-roadmap`, list exactly four `speckit.flow-roadmap.*` commands and the existing three renamed hook targets, and use the `spec-kit-flow-roadmap` repository URL.
- [X] T009 [P] [US1] Rename all four `commands/speckit.diagram-roadmap.*.md` files to `commands/speckit.flow-roadmap.*.md` and update their front matter and active internal command, skill, config, and script-path references without altering review or write semantics.
- [X] T010 [P] [US1] Update `.extensionignore` to allowlist the four renamed command files while retaining the reviewed twelve-file runtime payload and excluding development files.
- [X] T011 [P] [US1] Update `scripts/python/load_config.py` and `scripts/python/review_contract.py` to resolve the new installed path and override namespace, with no old-name fallback or change to their JSON/report contracts.
- [X] T012 [P] [US1] Update `config-template.yml` and `templates/review-report-template.md` current identity and example paths, preserving existing configuration fields and report semantics; inspect `templates/roadmap-template.md` and change it only if it has an active old-identity reference.
- [X] T013 [US1] Run `tests/python/test_installation.py`, `tests/python/test_commands.py`, `tests/python/test_command_selection.py`, `tests/python/test_load_config.py`, `tests/python/test_config_resolution.py`, and `tests/python/test_runtime.py`; resolve failures caused by the rename without adding a fifth command, new hook, or behavior change.
- [X] T014 [US1] Follow the clean-install scenario in `specs/009-rename-flow-roadmap/quickstart.md` using a disposable Spec Kit project; verify generated command-to-skill bindings, three hook registrations and dispatches, installed config, executable Python scripts, and source/payload parity.

**Checkpoint**: US1 is independently installable and passes its identity and existing-purpose checks. This is the suggested MVP scope.

## Phase 4: User Story 2 - Find one coherent project identity (Priority: P2)

**Goal**: Current project metadata, governance, and contributor guidance consistently identify FlowKit Roadmap while accepted history keeps its original meaning.

**Independent test**: Read the current README and project metadata, follow the installation guidance, and run a current-surface scan that distinguishes active old identifiers from migration and historical references.

### Tests for User Story 2

- [X] T015 [P] [US2] Update `tests/python/test_current_surface.py` to cover current project/display ID, repository links, commands, skills, env names, hooks, and living `README.md`, `.specify/memory/constitution.md`, and `.specify/memory/roadmap.md` sections while allowing explicit migration examples and protected history.
- [X] T016 [P] [US2] Correct and extend `tests/python/test_protected_history.py` so it compares accepted feature records, prior roadmap entries, dated reports, and the released `CHANGELOG.md` section against appropriate committed baselines without blocking entry 012 or current-facing amendments.

### Implementation for User Story 2

- [X] T017 [P] [US2] Update `README.md` current title, installation, usage, configuration, commands, generated skills, project relationship, and repository links to the FlowKit Roadmap identities; leave its migration sequence for US3.
- [X] T018 [P] [US2] Update `ORIGINS.md` and any other current-facing root metadata with the FlowKit Roadmap name and `spec-kit-flow-roadmap` project ID, preserving genuine historical references.
- [X] T019 [P] [US2] Amend `.specify/memory/constitution.md` current title, project note, and identity wording and `.specify/memory/roadmap.md` current title, vision, and source-of-truth note; give each living document its own accurate versioned Sync Impact Report while preserving the seven principles, merge-bounded governance, and accepted roadmap entries.
- [X] T020 [P] [US2] Add the identity migration to the unreleased section of `CHANGELOG.md` without changing the released `0.1.0` section or its historical claims.
- [X] T021 [US2] Run `tests/python/test_current_surface.py` and `tests/python/test_protected_history.py`, then inspect `README.md`, `ORIGINS.md`, `.specify/memory/constitution.md`, `.specify/memory/roadmap.md`, `CHANGELOG.md`, and current root files for stale active identities; classify old-name matches as migration, accepted history, or defects.

**Checkpoint**: US2's current documentation and governance identify one project; protected records retain their accepted meaning. The GitHub repository rename remains an acceptance gate; local directory renames follow feature completion.

## Phase 5: User Story 3 - Migrate an existing installation safely (Priority: P3)

**Goal**: A configured `diagram-roadmap` installation can transition manually to `flow-roadmap` without losing reviewed config, running duplicate hooks, or retaining old aliases.

**Independent test**: In a disposable project, test non-default and invalid old config, the successful disable/install/verify/remove order, failure rollback before removal, readable backup, and absence of old registrations after completion.

### Tests for User Story 3

- [X] T022 [P] [US3] Add `tests/python/test_migration.py` with disposable old/new installation scenarios for non-default config transfer, old-hook disablement, new registration verification, `remove --keep-config`, failed validation rollback, and backup readability.
- [X] T023 [P] [US3] Add old-command, old-skill, and old-override negative assertions to `tests/python/test_installation.py` and `tests/python/test_config_resolution.py` for a completed migration, including proof that old env values do not affect the new loader.

### Implementation for User Story 3

- [X] T024 [US3] Replace the remove-first migration section of `README.md` with the verified manual sequence from `specs/009-rename-flow-roadmap/contracts/migration-contract.md`: independent backup, disable old, install new, review and transfer config, validate, then remove old with `--keep-config`; document rollback and coexistence as incomplete.
- [X] T025 [US3] Execute the success and failed-validation paths in a disposable project per `specs/009-rename-flow-roadmap/quickstart.md`; inspect `.specify/extensions.yml`, `.specify/extensions/.registry`, both installed config paths, and generated skills after each transition, and retain the old installation on failure.
- [X] T026 [US3] Migrate this repository's dogfood installation with Specify CLI only after T025 succeeds: use the T002 backup, disable `diagram-roadmap`, add `flow-roadmap` from separate source, transfer reviewed values, verify new hooks/skills/config, then remove old with `--keep-config`; inspect `.specify/extensions.yml`, `.specify/extensions/.registry`, and `.specify/extensions/flow-roadmap/roadmap-config.yml` without hand-editing installer metadata.
- [X] T027 [US3] Update `tests/python/test_dogfood.py` to assert the new installed path, exact source/payload parity, valid retained config, four generated skills, three active new hooks, and no active old registry, command, skill, or hook names.
- [X] T028 [US3] Run `tests/python/test_migration.py`, `tests/python/test_installation.py`, `tests/python/test_config_resolution.py`, and `tests/python/test_dogfood.py`; reconcile any failed migration or dogfood checks and verify the independent old-config backup remains readable.

**Checkpoint**: US3 has a reversible, documented transition and the repository's dogfood installation uses only the new active identity. The old config backup remains recoverable.

## Phase 6: Polish and cross-cutting validation

**Purpose**: Complete repository-wide consistency and the acceptance evidence that spans all stories.

- [X] T029 Run `mise run test` and `git diff --check` from the repository root; verify all four purpose contracts, Python-only runtime, installed payload parity, and protected-history checks through `tests/python/`.
- [X] T030 Perform a holistic current-surface scan of `extension.yml`, `.extensionignore`, `commands/`, `scripts/python/`, `templates/`, `config-template.yml`, `README.md`, `ORIGINS.md`, `tests/python/`, `.specify/memory/constitution.md`, `.specify/memory/roadmap.md`, `.specify/extensions.yml`, `.specify/extensions/flow-roadmap/`, and `.agents/skills/`; fix stale active names while preserving documented migration and accepted history.
- [X] T031 Run the `specs/009-rename-flow-roadmap/quickstart.md` clean-install and migration validation on macOS. Linux execution is optional for this feature's acceptance; Linux runtime support remains required by Constitution V.
- [X] T032 Exercise the installed `write`, `brief`, `debrief`, and `sync` workflows on this repository through `.agents/skills/speckit-flow-roadmap-*/SKILL.md` and the current feature; retain their reports or proposals, complete the roadmap debrief, and apply no unapproved roadmap edit. Evidence: pre-implementation `brief-20260923T141331Z.md`, current `debrief-20260923T150113Z.md`, and `sync-20260923T145359Z.md`. The brief was not rerun after implementation because its skill is limited to pre-implementation review; installed skill bindings are covered by dogfood tests. The write workflow made no roadmap mutation; entry 012 remains `in-progress`.
- [X] T033 Review `specs/009-rename-flow-roadmap/spec.md`, `specs/009-rename-flow-roadmap/plan.md`, and `specs/009-rename-flow-roadmap/tasks.md` against the implementation and dogfood evidence; run `$speckit-converge` until no gaps remain, reconcile any new tasks, and re-run `$speckit-analyze` after consequential artifact changes before feature acceptance. Convergence found no uncovered implementation work, so no convergence phase was added. Analysis passed with all 24 buildable FR/SC items covered by the task list and no consistency findings.
- [X] T034 Verify the GitHub repository rename, configured `origin` URL, and root and installed `extension.yml` repository/homepage links use `spec-kit-flow-roadmap`. Evidence: the maintainer confirmed the GitHub rename on 2026-09-23; local `origin` was updated and verified, and both manifests contain the renamed URLs. Direct GitHub fetch was unavailable in this environment. Per the maintainer's sequencing direction, local checkout and worktree directory renames are post-feature operational follow-up and are excluded from FR-012/SC-008 acceptance.

## Dependencies and execution order

| Phase | Dependency | Result |
| --- | --- | --- |
| Setup | None | Baseline names and old config backup established. |
| Foundational | Setup | Shared fixture and required cross-artifact analysis ready. |
| US1 | Foundational | Clean installable new identity; MVP. |
| US2 | Foundational; current command names from US1 for final scan | Current documentation and governance; independently reviewable. |
| US3 | US1 clean install; US2 README identity changes before editing its migration section | Safe manual migration and dogfood transition. |
| Polish | All three stories; GitHub rename only after internal checks | Full suite, required macOS validation, dogfood, convergence, and final external acceptance evidence; local directory renames follow feature completion. |

Within each story, write focused tests first and observe the intended failures, then implement, run those tests, and complete its independent check. The old dogfood extension must stay installed until the new registration and config pass validation. The final GitHub rename gate does not authorize a GitHub or filesystem rename by itself. Local checkout/worktree directory renames are deferred until the feature is complete.

## Parallel execution examples

- **US1**: T005, T006, and T007 can update separate test files together. T008, T009, T010, T011, and T012 touch separate source files and can proceed after the test expectations are established. T013 and T014 wait for their source changes.
- **US2**: T015 and T016 can update separate tests together. T017, T018, T019, and T020 touch separate documents. T021 waits for those changes.
- **US3**: T022 and T023 can establish separate migration and alias tests together. T024 and T025 then validate the manual procedure before T026 changes the dogfood installation; T027 and T028 follow that migration.

## Implementation strategy

Complete setup and the `$speckit-analyze` gate before editing implementation files. Deliver US1 as the MVP: one clean installable `flow-roadmap` extension with the existing four purposes and three hooks. Then make current-facing project identity coherent through US2, followed by the configuration-preserving US3 migration. Finish with repository-wide checks, required macOS validation, all four commands exercised on this repository, and separately coordinated GitHub rename evidence. Linux remains supported but its validation is optional for this feature. Local directory renames are post-feature follow-up. Do not mark entry 012 verified until all acceptance gates are met.

## Phase 7: Convergence

- [X] T035 Replace `tests/python/test_migration.py`'s `git show HEAD:<old path>` source construction with a stable repository-owned legacy fixture, and verify the successful and failed migration tests still pass after the rename is committed, per FR-011 and SC-010 (partial).
- [X] T036 Make `tests/python/test_protected_history.py` compare the same accepted-roadmap-entry boundary in the working tree and committed baseline before and after entry 012 is committed, while retaining protection for merged feature records and released changelog content, per FR-009 and Constitution Merge-Bounded Flow-Back (partial).
