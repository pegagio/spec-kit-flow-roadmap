# Feature Specification: Adopt mise Tooling

**Feature Branch**: `develop`

**Created**: 2026-09-01

**Status**: Complete

**Input**: User description: "Specify the next roadmap feature, entry 010 mise migration."

## Clarifications

### Session 2026-09-01

- Q: How should a first-time contributor prepare the project before running its canonical test task? → A: Document reviewing and trusting `mise.toml`, running `mise install`, then running `mise run test`; the test task does not bootstrap tools.
- Q: From which working directories must `mise run test` be supported? → A: Support invocation from the repository root only and document that requirement.

### Session 2026-09-02

- Q: How should a clean host satisfy the installer required by mise's `pipx:` backend? → A: Pin `uv` as a project tool and make the Specify CLI declaration depend on both Python and `uv`, so `mise install` is self-contained and ordered rather than relying on undeclared global state.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run the canonical project validation (Priority: P1)

As a contributor, I can use the project's declared tool environment and one documented task to run the complete contract suite, so I do not need to know which interpreter or lower-level command the repository expects.

**Why this priority**: The complete contract suite is the only functional workflow worth preserving from the current task-runner configuration. A reliable canonical entrypoint is the minimum useful outcome of the migration.

**Independent Test**: From a supported development host with the declared tools installed, run the documented canonical test task and verify that it discovers and executes the complete contract suite with an unambiguous pass or fail result.

**Acceptance Scenarios**:

1. **Given** a first-time contributor has reviewed and trusted `mise.toml` and run `mise install`, **When** the contributor runs `mise run test` from the repository root, **Then** the complete Python contract suite executes in the project-declared environment.
2. **Given** any contract test fails, **When** the contributor runs the canonical test task, **Then** the task returns a failing result rather than reporting false success.
3. **Given** the repository is used on macOS or Linux, **When** the canonical test task is run, **Then** it exposes the same test workflow and completion semantics on both supported operating systems.

### User Story 2 - Discover one trustworthy task surface (Priority: P2)

As a contributor, I can inspect the project task list and see only workflows that perform real work, so placeholder commands cannot be mistaken for supported build, development, cleanup, or lint capabilities.

**Why this priority**: A canonical task runner is useful only when its task inventory is trustworthy. False-success placeholders make automation and contributor expectations less reliable.

**Independent Test**: List the project tasks and verify that every advertised task has a repository-owned workflow and that no Just-based or placeholder task surface remains.

**Acceptance Scenarios**:

1. **Given** the migration is complete, **When** a contributor lists project tasks, **Then** every listed task performs a real, validated project workflow.
2. **Given** the former `build`, `dev`, and `clean` recipes only printed placeholder messages, **When** the canonical task surface is inspected, **Then** equivalent false-success tasks are absent.
3. **Given** the repository has no owned lint configuration, **When** the canonical task surface is inspected, **Then** it does not advertise a lint task that cannot run successfully from repository state alone.

### User Story 3 - Follow current guidance without rewriting history (Priority: P3)

As a maintainer, I can keep current contributor guidance and current-surface validation aligned on mise while preserving accepted specifications, dated reports, and released history as evidence of the commands used when earlier work was completed.

**Why this priority**: The project requires later changes to flow forward. Current guidance must be accurate without retroactively changing the meaning of merged feature records.

**Independent Test**: Scan maintained current surfaces and accepted historical surfaces separately; current surfaces identify mise as canonical, while merged feature artifacts and dated reports remain unchanged.

**Acceptance Scenarios**:

1. **Given** a contributor reads current development or test documentation, **When** the contributor looks for the supported validation command, **Then** the documentation consistently directs them to `mise run test` and does not offer `just test` as a current alternative.
2. **Given** repository contract tests inspect current project guidance, **When** those tests run, **Then** they validate the mise task surface rather than require a `justfile`.
3. **Given** a merged specification or dated report records `just test`, **When** the migration updates current surfaces, **Then** that historical reference remains unchanged.

### Edge Cases

- The canonical task is invoked before the declared tools are installed or before the project configuration is trusted; the failure remains visible and directs the contributor back to the separate documented setup sequence.
- The task is invoked from a nested repository directory rather than the repository root; nested-directory invocation is outside the supported contract, and current documentation identifies the repository root as the required working directory.
- A declared development tool has no current task, test, packaging, or contributor workflow that uses it.
- A clean host has mise but does not already have `uv` or `pipx`; the declared install graph must install Python and `uv` before the Specify CLI rather than depend on ambient global tooling.
- A globally installed Just or pre-commit executable is available even though the repository no longer owns the corresponding project configuration.
- Historical specifications and dated reports still contain `just`, `justfile`, or the former direct test command.
- A future contributor adds a task that exits successfully while performing no project work.
- The number of discovered contract tests changes after this feature; the canonical task must continue to run the complete discovered suite rather than encode a fixed count.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The project MUST designate mise as the sole canonical declaration of development tool versions and project task entrypoints.
- **FR-002**: Contributors MUST be able to run the complete discovered Python contract suite through `mise run test` after installing the project-declared tools.
- **FR-003**: The canonical test task MUST execute within the project-declared environment and MUST preserve the test discovery path, filename pattern, pass/fail behavior, and exit semantics of the existing complete-suite workflow.
- **FR-004**: The maintained repository MUST remove the `justfile` and MUST NOT require Just for any current contributor or validation workflow.
- **FR-005**: Current development documentation, test documentation, and current-surface contract checks MUST identify `mise run test` as the canonical complete-suite command.
- **FR-006**: Current documentation MUST NOT present a duplicate lower-level test invocation as an equivalent supported workflow.
- **FR-007**: The canonical task inventory MUST NOT preserve or recreate placeholder `build`, `dev`, or `clean` tasks that report success without performing project work.
- **FR-008**: The canonical task inventory MUST NOT include a lint task unless the repository contains and validates the configuration required to execute that task.
- **FR-009**: Every development tool declaration MUST have a current, documented project purpose; declarations without a current task, test, packaging, or contributor workflow MUST be removed.
- **FR-010**: Repository contract tests MUST validate the canonical mise configuration and MUST fail if current documentation or task configuration reintroduces Just as a supported surface.
- **FR-011**: The migration MUST preserve merged feature directories, dated generated reports, and released changelog history without rewriting their historical task-runner references.
- **FR-012**: The migration MUST NOT change extension runtime behavior, supported operating systems, command semantics, configuration contracts, or installed extension payload contents.
- **FR-013**: Project task validation and the canonical test task MUST produce an unambiguous non-zero result when their configuration or executed workflow fails.
- **FR-014**: The migration MUST NOT introduce another task runner, framework, build system, compatibility wrapper, or dependency unrelated to the declared tooling setup and validation workflow.
- **FR-015**: The canonical test task MUST be validated on macOS and Linux, the project's complete supported operating-system set.
- **FR-016**: The migration MUST flow forward in this feature and MUST reference the verified Python migration as its dependency rather than editing that merged feature to describe the new outcome.
- **FR-017**: Current contributor documentation MUST present first-time setup as three separate actions: review and trust `mise.toml`, run `mise install`, and then run `mise run test`. The test task MUST NOT install tools, trust configuration, or otherwise bootstrap its own environment.
- **FR-018**: The canonical test task MUST be supported from the repository root. Current documentation MUST identify that working-directory requirement; invocation from nested or unrelated directories is not a supported workflow.
- **FR-019**: The project MUST pin `uv` as the installer required by mise's `pipx:` backend, and the Specify CLI declaration MUST depend on the pinned Python and `uv` declarations so a clean `mise install` does not rely on undeclared global tooling.

### Key Entities

- **Development Tool Declaration**: A project-owned declaration of a tool and version needed by a current task, test, tool-installation edge, packaging operation, or contributor workflow.
- **Project Task**: A named contributor entrypoint that performs a real repository workflow and returns a truthful success or failure result.
- **Current Surface**: Maintained task configuration, contributor documentation, and contract validation that describe how the project works now.
- **Historical Artifact**: A merged feature file, dated generated report, or released changelog record that preserves the workflow accepted at that time.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A contributor can run the complete discovered contract suite through one documented project task with no knowledge of its lower-level test command.
- **SC-002**: On macOS and Linux, 100% of the existing contract suite runs through the canonical task and yields the same pass/fail outcome as the complete-suite workflow it replaces.
- **SC-003**: A current-surface scan finds exactly one documented canonical complete-suite entrypoint and zero current references that require Just or `just test`.
- **SC-004**: The project task inventory contains zero placeholder tasks and zero tasks that depend on repository-absent configuration.
- **SC-005**: Every retained development tool declaration maps to at least one current project purpose, and zero unused declarations remain.
- **SC-006**: Repository contract tests fail when a current Just requirement, duplicate test workflow, or false-success placeholder task is introduced.
- **SC-007**: Relative to a deterministic protected-surface baseline recorded before implementation begins, the migration changes zero merged feature files, dated generated reports, released changelog sections, extension runtime files, packaging rules, generated skills, or installed payload files.
- **SC-008**: A contributor following only the current README and test documentation can locate and successfully start the complete validation workflow on the first attempt.
- **SC-009**: A first-time contributor can distinguish setup from validation, complete the documented setup sequence once, and rerun validation without repeating installation or trust actions.
- **SC-010**: Every maintained example of the canonical test task identifies or demonstrates the repository root as the required working directory, and acceptance validation succeeds from that location on both supported operating systems.
- **SC-011**: On a clean supported host with only mise available, `mise install` installs the complete project toolchain without requiring an undeclared global `uv` or `pipx` executable.

## Assumptions

- Contributors install mise itself outside this repository; project documentation begins with review and explicit trust of `mise.toml`, followed by `mise install`, before any project task is run.
- The complete Python contract suite established by the verified Python migration remains the only current project workflow that the former `justfile` usefully exposes.
- The existing `build`, `dev`, and `clean` recipes are placeholders rather than supported capabilities, and the existing lint recipe has no repository-owned pre-commit configuration to execute.
- Roadmap entry 009 and `specs/006-python-script-migration/` are complete and verified dependencies whose historical contents must not be revised.
- Roadmap entry 010 maps to this independently numbered `specs/007-adopt-mise-tooling/` directory; roadmap and feature directory identifiers are not required to match.
- Tool installation and project configuration trust failures should remain visible to contributors rather than being hidden by fallback execution paths.
