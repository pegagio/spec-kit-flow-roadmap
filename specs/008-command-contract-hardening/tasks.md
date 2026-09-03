---

description: "Dependency-ordered implementation tasks for command contract hardening"
---

# Tasks: Harden Command Contracts and Review Evidence

**Input**: Design documents from `/specs/008-command-contract-hardening/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

**Tests**: Automated contract coverage is required by FR-029 and SC-010. Test tasks precede the corresponding implementation tasks. Judgment-bearing behavior also requires disposable-project dogfood and explicit intended-user disposition.

**Organization**: Tasks are grouped by user story so each story produces an independently testable increment after the deterministic foundation is complete.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it uses different files and has no dependency on an incomplete task.
- **[Story]**: Maps the task to a user story in `spec.md`.
- Every task names the exact file or files it changes or validates.

## Phase 1: Setup and Historical Safeguards

**Purpose**: Prepare reusable test infrastructure and make the forward-only history boundary executable before changing current command surfaces.

- [X] T001 Extend disposable Git repository, executable-script, and JSON subprocess helpers in `tests/python/support.py`
- [X] T002 [P] Add semantic protected-history assertions for merged feature directories 001 through 007, dated reports, released changelog content, roadmap entries 001 through 010, and accepted verification evidence in `tests/python/test_protected_history.py`

**Checkpoint**: Test infrastructure is ready and protected historical surfaces have a reproducible pre-change guard.

---

## Phase 2: Foundational Deterministic Review Contract

**Purpose**: Implement the shared, script-owned mechanics that block every review story while preserving the verified loader contract.

**Critical**: No user-story implementation begins until this phase passes its focused tests.

- [X] T003 Add regression tests for reusable runtime, repository-root, configuration, and containment primitives while preserving the loader's no-argument six-field contract in `tests/python/test_load_config.py` and `tests/python/test_path_containment.py`
- [X] T004 Expose reusable runtime, repository-root, configuration, and containment primitives without changing CLI behavior in `scripts/python/load_config.py`
- [X] T005 Add failing process-contract and no-argument configuration tests for the new helper in `tests/python/test_review_contract.py`
- [X] T006 Create the Python 3.11 entrypoint, stable JSON output, expected-error handling, and loader-backed default operation in `scripts/python/review_contract.py`
- [X] T007 Add failing exact-target, explicit-precedence, convergence, conflict, candidate-handoff, selected-candidate, number-only, and ambient-fallback tests in `tests/python/test_review_contract.py`
- [X] T008 Implement deterministic target normalization and candidate resolution for brief and debrief in `scripts/python/review_contract.py`
- [X] T009 Add failing temporary-repository tests for commit ranges, ancestry failures, baseline-to-worktree, HEAD-to-WORKTREE, clean-tree unavailability, dirty exclusions, renames, deletions, untracked files, gitlinks, punctuation-leading refs, and snapshot changes in `tests/python/test_review_delta.py`
- [X] T010 Implement complete Git delta enumeration, stable artifact merging, exclusions, limitations, and snapshot digests in `scripts/python/review_contract.py`
- [X] T011 Add failing taxonomy, finding validation, stable ordering/IDs, cap-zero, overflow, hidden-blocker, and verdict tests in `tests/python/test_review_contract.py`
- [X] T012 Implement canonical review taxonomies, structured finding validation, uncapped aggregation, display capping, and verdict derivation in `scripts/python/review_contract.py`
- [X] T013 Add failing dependency-readiness and brief/debrief lifecycle matrix tests in `tests/python/test_review_contract.py`
- [X] T014 Implement deterministic dependency and lifecycle recommendation gates without performing transitions in `scripts/python/review_contract.py`
- [X] T015 Add failing UTC timestamp, same-second collision, exclusive-creation, empty-reservation, kind-specific-directory, and containment tests in `tests/python/test_review_contract.py`
- [X] T016 Implement atomic report allocation with deterministic numeric suffixes in `scripts/python/review_contract.py`
- [X] T017 Update the declared Python runtime payload and installation allowlist for the new helper in `extension.yml` and `.extensionignore`
- [X] T018 Update current-runtime inventory and platform-neutral Python assertions for the two-script architecture in `tests/python/test_current_surface.py`

**Checkpoint**: `load_config.py` remains backward-compatible and every deterministic operation in `review-contract.md` passes focused tests.

---

## Phase 3: User Story 1 — Safely Create or Amend Durable Roadmap Content (Priority: P1) MVP

**Goal**: Ensure roadmap writing treats repository material as untrusted evidence, records provenance, and never turns inferred content into durable governance without authorization.

**Independent Test**: Run write against contained evidence with embedded instructions, incomplete decisions, and inferred proposals; verify embedded instructions are ignored, provenance is shown, interactive inference requires confirmation, and unattended inference leaves the roadmap unchanged.

### Tests for User Story 1

- [X] T019 [US1] Add failing command-contract assertions for the evidence allowlist, access-time containment, provenance, untrusted-content handling, interactive confirmation, non-interactive no-write rule, and preservation of required elicitation for end states, goals, milestones, scope, features, outcomes, and constraints in `tests/python/test_commands.py`

### Implementation for User Story 1

- [X] T020 [US1] Rewrite the write command's accepted inputs, evidence policy, provenance rules, authorization gates, stop conditions, and non-goals while actively eliciting any unsettled end states, goals, milestones, scope, features, outcomes, and constraints in `commands/speckit.diagram-roadmap.write.md`
- [X] T021 [US1] Add adversarial-evidence, interactive-inference, and unattended-inference dogfood procedures and expected outcomes in `tests/README.md`

**Checkpoint**: User Story 1 passes its static contract tests and can be dogfooded without relying on any review-command implementation.

---

## Phase 4: User Story 2 — Receive an Evidence-Backed Implementation Debrief (Priority: P2)

**Goal**: Bind debrief conclusions to a complete, attributable implementation delta and prevent unsupported absence or verification claims.

**Independent Test**: Debrief expected and unexpected changed artifacts across explicit commit, baseline-to-worktree, dirty fallback, and unavailable-clean-tree scenarios; verify provenance, scope evaluation, exclusions, limitations, and verification gates.

### Tests for User Story 2

- [X] T022 [US2] Add failing debrief command assertions for explicit baseline/target precedence, complete delta inspection, dirty-state boundaries, snapshot recheck, unavailable-delta limitations, absence-claim prohibition, and verified gates in `tests/python/test_commands.py`
- [X] T023 [P] [US2] Add debrief report provenance assertions for revisions, dirty state, exclusions, reviewed artifacts, snapshot identity, and material limitations in `tests/python/test_output_contract.py`

### Implementation for User Story 2

- [X] T024 [US2] Integrate target and delta resolution, complete artifact review, snapshot retry, canonical debrief findings, limitations, and state-aware verification guidance in `commands/speckit.diagram-roadmap.debrief.md`

**Checkpoint**: User Story 2 produces a traceable debrief for every trustworthy delta mode and narrows its conclusion when delta evidence is unavailable or unstable.

---

## Phase 5: User Story 3 — Get Consistent, State-Aware Command Results (Priority: P3)

**Goal**: Give brief, debrief, and sync one findings model, deterministic verdict policy, complete overflow summaries, honest mutation boundary, lifecycle rules, and collision-safe report identity.

**Independent Test**: Feed equivalent severity sets, caps, dependencies, and lifecycle states through all review contracts; verify canonical categories, identical verdicts and counts, valid status guidance, complete provenance, and unique report paths.

### Tests for User Story 3

- [X] T025 [US3] Add failing cross-command assertions for helper integration, canonical taxonomies, shared severities/verdicts, cap-zero and overflow semantics, source-preserving report-only mutation, unresolved ADR handling, and state-aware lifecycle guidance in `tests/python/test_commands.py`
- [X] T026 [P] [US3] Add failing shared-template assertions for target, selection, roadmap entry, reviewed paths, revision/dirty evidence, findings cap, total/displayed/omitted counts, limitations, verdict, and lifecycle recommendation in `tests/python/test_output_contract.py`

### Implementation for User Story 3

- [X] T027 [US3] Update the shared review template with canonical findings, aggregation, provenance, limitation, verdict, and lifecycle fields in `templates/review-report-template.md`
- [X] T028 [US3] Integrate deterministic target, dependency, finding, lifecycle, and report-allocation contracts in `commands/speckit.diagram-roadmap.brief.md`
- [X] T029 [P] [US3] Integrate project-wide taxonomy, finding aggregation, process-entry treatment, and report allocation in `commands/speckit.diagram-roadmap.sync.md`
- [X] T030 [US3] Align debrief's findings, verdict, cap, provenance, unresolved-evidence, report-allocation, and report-only mutation language in `commands/speckit.diagram-roadmap.debrief.md`

**Checkpoint**: User Story 3 passes the same semantic contract assertions across all three review commands without silently mutating source or governance artifacts.

---

## Phase 6: User Story 4 — Invoke the Correct Command for the Intended Job (Priority: P4)

**Goal**: Make positive use cases, adjacent non-goals, accepted inputs, target precedence, outputs, and stop conditions unambiguous to users and host agents.

**Independent Test**: Evaluate maintained positive and negative invocation examples for all four commands; verify correct selection, explicit-over-ambient precedence, conflict stops, and no report creation for an assumed target.

### Tests for User Story 4

- [X] T031 [US4] Add failing metadata and body assertions for positive activation language, adjacent negative cases, normalized inputs, explicit-over-ambient precedence, ambiguity stops, and declared outputs in `tests/python/test_commands.py`
- [X] T032 [P] [US4] Add maintained positive and negative invocation fixtures for all four commands in `tests/fixtures/command-selection.json` and selection-contract assertions in `tests/python/test_command_selection.py`

### Implementation for User Story 4

- [X] T033 [US4] Front-load the write and brief descriptions with their positive use cases and adjacent non-goals, and align their input/output summaries in `commands/speckit.diagram-roadmap.write.md` and `commands/speckit.diagram-roadmap.brief.md`
- [X] T034 [P] [US4] Front-load the debrief and sync descriptions with their positive use cases and adjacent non-goals, and align their input/output summaries in `commands/speckit.diagram-roadmap.debrief.md` and `commands/speckit.diagram-roadmap.sync.md`

**Checkpoint**: User Story 4's maintained selection set distinguishes all four workflows and stops rather than guessing when targets conflict or remain ambiguous.

---

## Phase 7: Packaging, Dogfood, and Cross-Cutting Validation

**Purpose**: Propagate the accepted contracts to every runtime surface, prove the complete feature end to end, and record platform and human-review evidence.

- [X] T035 Update exact source payload, twelve-file installation, executable-helper, source-copy, generated-skill, and hook assertions in `tests/python/test_installation.py` and `tests/python/test_dogfood.py`
- [X] T036 Copy the source commands, both Python scripts, shared review template, and manifest into `.specify/extensions/diagram-roadmap/commands/`, `.specify/extensions/diagram-roadmap/scripts/python/`, `.specify/extensions/diagram-roadmap/templates/review-report-template.md`, and `.specify/extensions/diagram-roadmap/extension.yml`
- [X] T037 Regenerate the four command skills and verify their source-semantic parity in `.agents/skills/speckit-diagram-roadmap-write/SKILL.md`, `.agents/skills/speckit-diagram-roadmap-brief/SKILL.md`, `.agents/skills/speckit-diagram-roadmap-debrief/SKILL.md`, and `.agents/skills/speckit-diagram-roadmap-sync/SKILL.md`
- [X] T038 [P] Update user-facing command behavior, evidence safety, report semantics, and Python helper documentation in `README.md`
- [X] T039 [P] Update automated, disposable-project, dogfood, protected-history, and macOS/Linux validation instructions in `tests/README.md`
- [X] T040 [P] Record the command-contract hardening under the unreleased section without altering released history in `CHANGELOG.md`
- [X] T041 Run the complete automated suite and whitespace validation from `quickstart.md`, then record exact commands, results, and test count in `specs/008-command-contract-hardening/validation-evidence.md`
- [X] T042 Execute every disposable dogfood scenario from `quickstart.md` and record inputs, selected targets, evidence boundaries, report paths, findings summaries, verdicts, lifecycle guidance, and observed mutations in `specs/008-command-contract-hardening/validation-evidence.md`
- [X] T043 Exercise every maintained positive and adjacent-negative prompt through a host agent, verify the selected command for all four workflows, and record the results in `specs/008-command-contract-hardening/validation-evidence.md`
- [X] T044 Exercise this repository's installed Diagram Roadmap extension and trigger its registered `after_constitution`, `before_implement`, and `after_implement` hooks in an isolated clone or worktree of this repository; record the source revision, installed payload identity, observed command dispatch, and generated artifacts in `specs/008-command-contract-hardening/validation-evidence.md`
- [X] T045 Verify zero semantic changes to every protected historical surface guarded by T002 and record the comparison result in `specs/008-command-contract-hardening/validation-evidence.md`
- [ ] T046 Run the complete automated suite and every judgment-focused disposable acceptance scenario on Linux, or record equivalent external Linux evidence tied to the exact tested revision, in `specs/008-command-contract-hardening/validation-evidence.md` — **Deferred by intended-user decision on 2026-09-03; required before verified status.**
- [X] T047 Obtain and record explicit intended-user disposition for the revised command selection, evidence boundary, debrief provenance, report semantics, and lifecycle guidance in `specs/008-command-contract-hardening/validation-evidence.md`

**Checkpoint**: All current source, installed, generated, metadata, template, test, and documentation surfaces agree; macOS evidence and intended-user disposition are recorded; historical artifacts remain unchanged; Linux verification is explicitly deferred before verified status.

---

## Dependencies and Execution Order

### Phase Dependencies

- **Phase 1 — Setup**: No dependencies and starts immediately.
- **Phase 2 — Foundation**: Depends on Phase 1 and blocks every user story.
- **Phase 3 — User Story 1**: Depends only on Phase 2 and is the MVP.
- **Phase 4 — User Story 2**: Depends only on Phase 2; it can proceed independently of User Story 1.
- **Phase 5 — User Story 3**: Depends on Phase 2 and on T024 for the final debrief alignment in T030; brief and sync work may begin independently.
- **Phase 6 — User Story 4**: Depends on the command bodies from Phases 3 through 5 so selection wording describes their final behavior.
- **Phase 7 — Packaging and Validation**: Depends on all selected user stories and is required before feature acceptance.

### User Story Dependencies

```text
Setup -> Foundation -> US1 (MVP)
                    -> US2 -----------+
                    -> US3 (brief/sync) +-> US4 -> Packaging and Validation
                       US2 -> US3 debrief+
```

- **US1** is independently deliverable after Foundation.
- **US2** is independently deliverable after Foundation because target and delta mechanics are foundational.
- **US3** can implement brief and sync after Foundation; its final debrief alignment follows US2.
- **US4** validates selection against the completed command behaviors and therefore follows US1 through US3.

### Within Each User Story

1. Add the specified failing contract tests.
2. Implement the command or template behavior.
3. Run the focused tests until they pass.
4. Exercise the independent test before moving to packaging.

## Parallel Opportunities

- T002 can run in parallel with T001 because it creates a separate test module.
- After T006, delta work T009–T010 can proceed independently of target work T007–T008 until both modify `review_contract.py`; coordinate integration before merging those edits.
- US1 and US2 can proceed in parallel after Foundation because they primarily change different command files.
- T023 can run in parallel with T022, and T026 can run in parallel with T025.
- T029 can run in parallel with T028; T030 waits for the US2 debrief implementation.
- T032 can run in parallel with T031, and T034 can run in parallel with T033.
- T038, T039, and T040 can run in parallel after command behavior stabilizes.

## Parallel Examples

### User Story 1 and User Story 2

```text
Task A: T019-T021 harden and validate roadmap write evidence and authorization.
Task B: T022-T024 harden and validate implementation debrief provenance and delta handling.
```

### User Story 3

```text
Task A: T025 and T028 implement shared brief semantics.
Task B: T026, T027, and T029 implement shared template and sync semantics.
Task C: T030 aligns debrief after T024 completes.
```

### User Story 4

```text
Task A: T031 and T033 validate and revise write/brief selection boundaries.
Task B: T032 and T034 validate and revise debrief/sync selection boundaries.
```

## Implementation Strategy

### MVP First

1. Complete Setup and Foundation.
2. Complete User Story 1 only.
3. Run its command-contract tests and adversarial-evidence dogfood.
4. Stop for review before changing review-command behavior.

This MVP addresses the highest-risk surface: durable roadmap mutation influenced by untrusted or unapproved material.

### Incremental Delivery

1. Foundation establishes deterministic contracts without changing judgment semantics.
2. US1 secures roadmap writes.
3. US2 makes implementation review attributable.
4. US3 unifies report and lifecycle semantics.
5. US4 makes workflow selection explicit.
6. Packaging and validation propagate and prove the integrated feature.

### Required Gates

- Run `speckit-analyze` after this task list and resolve material cross-artifact inconsistencies before implementation.
- Keep tests failing before their associated implementation task and passing at each story checkpoint.
- Do not treat automated validation as intended-user acceptance.
- Run `speckit-converge` after implementation until no in-scope gaps remain.
- Do not merge while specification, plan, tasks, implementation, or validation evidence materially diverge.
