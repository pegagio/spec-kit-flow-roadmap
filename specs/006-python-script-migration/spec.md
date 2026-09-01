# Feature Specification: Python Script Migration

**Feature Branch**: `python`

**Created**: 2026-08-31

**Status**: Complete

**Input**: User description: "Migrate the current scripts to Python, target macOS and Linux, and drop Windows, Bash, and PowerShell support, using roadmap entry 009 as context."

## Clarifications

### Session 2026-08-31

- Q: What Python version contract should the installed extension require? → A: Use the active Specify installation's Python runtime and require the repository pin to match it; the current required version is exactly 3.11.16.
- Q: How should the migrated script parse `roadmap-config.yml`? → A: Use the PyYAML dependency supplied by the active Specify runtime and validate the documented configuration structure.
- Q: How should the extension handle an absolute configured roadmap or ADR path that still resolves inside the active project? → A: Reject every absolute path and require project-relative paths.
- Q: What should happen when `roadmap-config.yml` contains an unrecognized key? → A: Reject unknown keys with a clear error.
- Q: Does the Python-only policy allow simple shell command examples and direct task-runner commands that contain no scripting logic? → A: Allow direct commands, but require all scripting logic to be Python.

## User Scenarios & Testing *(mandatory)*

This feature lets Diagram Roadmap users and maintainers rely on one deterministic scripting contract across the supported operating systems while preserving the behavior of all four extension commands.

### User Story 1 - Run commands on supported platforms (Priority: P1)

As a Diagram Roadmap user on macOS or Linux, I can install the extension and run each command without Bash or PowerShell being part of the extension's runtime contract.

**Why this priority**: The extension's four commands are its user-facing product. The migration succeeds only if they remain installable and usable on both supported operating systems.

**Independent Test**: Install the extension into disposable Spec Kit projects on macOS and Linux, invoke each provided command's deterministic prerequisite path, and verify that all commands receive valid configuration without invoking Bash or PowerShell.

**Acceptance Scenarios**:

1. **Given** a supported Spec Kit project on macOS, **When** Diagram Roadmap is installed and each of its four commands is invoked, **Then** every command resolves its prerequisites through the single supported scripting contract and retains its documented behavior.
2. **Given** a supported Spec Kit project on Linux, **When** Diagram Roadmap is installed and each of its four commands is invoked, **Then** every command resolves its prerequisites through the same contract used on macOS.
3. **Given** an environment where Bash or PowerShell is absent or unavailable, **When** a Diagram Roadmap command runs on macOS or Linux, **Then** the command does not fail because either shell is missing.

### User Story 2 - Preserve deterministic configuration behavior (Priority: P2)

As a maintainer or command author, I receive the same validated configuration contract for identical project state and inputs after the migration, so the judgment-bearing command bodies do not need to reinterpret configuration.

**Why this priority**: Configuration resolution is shared by all commands. Contract drift could silently redirect roadmap reads or writes, change review limits, or make supported installations behave differently.

**Independent Test**: Exercise defaults, file overrides, environment overrides, null values, special characters, invalid values, path boundaries, missing files, and non-root working directories and compare each result with the specified contract.

**Acceptance Scenarios**:

1. **Given** identical project files and environment values, **When** configuration is resolved repeatedly on either supported operating system, **Then** the structured fields, types, values, exit status, and error behavior are equivalent.
2. **Given** configuration from more than one supported source, **When** the configuration is resolved, **Then** the documented precedence selects one deterministic value for every field.
3. **Given** an invalid value or a configured path outside the active project, **When** configuration is resolved, **Then** resolution fails clearly without emitting a valid-looking configuration object.

### User Story 3 - Maintain one current scripting surface (Priority: P3)

As a contributor, I see one current scripting implementation, one supported-platform test strategy, and documentation that clearly distinguishes the supported contract from preserved project history.

**Why this priority**: Removing parallel implementations reduces drift only if source files, installed payload metadata, tests, task runners, and current documentation all agree on the new boundary.

**Independent Test**: Inspect the source repository and a disposable installed payload and verify that current runtime surfaces reference only the supported scripting implementation while historical feature records remain unchanged.

**Acceptance Scenarios**:

1. **Given** the maintained source tree and extension manifest, **When** a contributor inventories current runtime scripts and command references, **Then** no Bash or PowerShell implementation, wrapper, or paired-script metadata remains.
2. **Given** current project documentation and validation instructions, **When** a contributor follows them, **Then** they describe Python on macOS and Linux and do not advertise Windows support.
3. **Given** merged feature directories, dated reports, and released changelog entries, **When** current-reference checks run, **Then** those historical records remain preserved and are not treated as active support commitments.

### Edge Cases

- The configured roadmap or ADR path is absolute, contains traversal, or resolves through a symbolic link outside the active project, or a configured PRD pattern can match outside the active project.
- The command runs from a working directory outside the project while its installed script remains inside the project.
- The project has no configuration file, an empty configuration file, or explicit YAML null sentinels.
- The project configuration or installed manifest path is a symlink, directory, FIFO, or another non-regular filesystem object, including a symlink that resolves inside the project.
- The configuration file contains a misspelled, deprecated, or otherwise unrecognized key.
- Environment overrides contain commas, quotes, backslashes, Unicode, tabs, or line breaks that must remain valid structured output.
- The findings limit is zero, negative, non-numeric, empty, or larger than typical review output.
- The roadmap or ADR directory changes between configuration resolution and later command use.
- A local dogfood installation is stale after the source payload changes.
- Bash or PowerShell happens to be installed on a supported host; its presence must not change execution or validation results.
- A documentation example or task-runner recipe invokes one executable directly, while another uses shell control flow, a pipeline, redirection, variable manipulation, data transformation, or multi-command orchestration.
- Specify-generated command metadata initially selects a project or `PATH` Python rather than the active Specify installation's interpreter.
- The active `specify` executable is missing, is an unsupported wrapper, or resolves to an interpreter whose version does not match the repository pin.
- A project-local `yaml.py`, user-site package, or `PYTHONPATH` entry attempts to shadow the PyYAML dependency supplied by Specify.
- Historical specifications and reports still mention Windows, Bash, or PowerShell as accepted behavior at the time they were merged.

## Requirements *(mandatory)*

The requirements define the supported user-visible contract and the compatibility boundary for the migration. Python is a governing product constraint supplied by the constitution and roadmap, not an implementation choice left open by this specification.

### Functional Requirements

- **FR-001**: The extension MUST support macOS and Linux as its complete operating-system target set and MUST identify Windows support as a non-goal.
- **FR-002**: Every extension-owned runtime script and maintained automation script MUST use Python as its scripting language.
- **FR-003**: The maintained extension MUST NOT ship, invoke, or require Bash or PowerShell scripts, wrappers, paired implementations, platform-specific script metadata, or cross-language parity machinery.
- **FR-004**: All four canonical commands MUST obtain deterministic configuration and prerequisite information through the same supported scripting contract on macOS and Linux.
- **FR-005**: Deterministic scripts MUST limit their responsibility to project discovery, configuration resolution, validation, existence checks, and structured output; roadmap synthesis and review judgment MUST remain in command bodies.
- **FR-006**: Configuration resolution MUST emit exactly these fields with stable types: `roadmap_path` as a non-empty string, `roadmap_exists` as a boolean, `adr_dir` as a non-empty string, `adr_present` as a boolean, `prd_globs` as an ordered list of non-empty strings, and `max_findings` as a non-negative integer.
- **FR-007**: Each configuration value MUST resolve in this precedence order: `SPECKIT_DIAGRAM_ROADMAP_*` environment override, installed `roadmap-config.yml`, installed extension defaults, then built-in defaults.
- **FR-008**: In the absence of overrides, the resolved contract MUST use `.specify/memory/roadmap.md`, `docs/adr/`, the five established PRD detection patterns, and a findings limit of 50.
- **FR-009**: Empty and explicit YAML null values MUST fall through to the next available precedence source rather than becoming configured values.
- **FR-010**: PRD glob resolution MUST return patterns only and MUST NOT scan the filesystem for matching product documents.
- **FR-011**: Project discovery and configuration results MUST be independent of the caller's current working directory for both source-checkout and installed-extension execution.
- **FR-012**: Configured roadmap and ADR paths MUST be project-relative and resolve canonically within the active project, and configured PRD patterns MUST be bounded to that project. Every absolute path, including one that resolves inside the project, plus traversal, symbolic-link escapes, out-of-project glob patterns, and other values that can resolve or match outside the project MUST be rejected. Every concrete roadmap, ADR, or PRD path MUST be canonically revalidated immediately before each content read or write, including after initial configuration resolution. Validation for roadmap creation MUST permit a nonexistent contained target while validating its existing parent chain and rejecting an existing non-regular target.
- **FR-013**: Invalid configuration MUST produce a non-zero result, a clear diagnostic on the error channel, and no structured configuration on the output channel. A findings limit of zero MUST remain valid.
- **FR-014**: Special characters and Unicode in supported configuration values MUST round-trip through the structured output without corruption or injection.
- **FR-015**: The installed extension payload and command metadata MUST reference only the supported runtime script and MUST remain free of repository metadata and development-only files.
- **FR-016**: Automated validation MUST cover the shared configuration contract and command prerequisite paths on macOS and Linux without retaining Bash, PowerShell, Bats, Pester, or cross-language parity as maintained test dependencies.
- **FR-017**: Current README, changelog guidance, development commands, task-runner configuration, manifest descriptions, command metadata, and test documentation MUST consistently describe the macOS/Linux and Python-only contract.
- **FR-018**: The repository's dogfood installation MUST be refreshed from the reviewed source payload. Every source-owned installed command, script, template, manifest, license, and configuration template MUST match its source counterpart byte-for-byte. The project-owned `roadmap-config.yml` MUST be preserved across refresh and validated semantically against the current configuration contract; it is excluded from source-byte-parity comparison.
- **FR-019**: The migration MUST preserve the existing behavior of roadmap creation/amendment, briefing, debriefing, synchronization, configuration precedence, output fields, error separation, and non-destructive command semantics except where this specification explicitly changes platform, scripting, path-containment, or validation behavior.
- **FR-020**: The migration MUST NOT add compatibility aliases or fallback execution paths for Windows, Bash, or PowerShell.
- **FR-021**: Merged feature directories, dated generated reports, released changelog entries, and other accepted historical records MUST NOT be rewritten solely to replace their historical Windows, Bash, or PowerShell references.
- **FR-022**: Deterministic configuration resolution MUST be self-contained within the reviewed installed extension payload and standard runtime. It MUST NOT source, execute, or import project-controlled helper scripts or code as part of loading configuration.
- **FR-023**: Extension scripts MUST ultimately run with the Python interpreter used by the active Specify installation. Because Specify-generated commands can initially select a project or `PATH` interpreter, the entrypoint MAY use standard-library-only bootstrap logic to locate the active `specify` console-script interpreter and re-execute itself once in isolated mode. The repository's required Python pin MUST match the resulting runtime exactly; the current required version is 3.11.16. Resolution MUST fail when the active Specify interpreter is missing, cannot be verified, uses an unsupported wrapper, or does not match the required version, and MUST NOT fall back to an arbitrary runtime.
- **FR-024**: Configuration files MUST be parsed with the PyYAML dependency supplied by the active Specify runtime and validated against the documented mapping, list, scalar, and value-type structure. The extension MUST NOT vendor a YAML parser or retain a line-based parsing fallback.
- **FR-025**: Every configuration key MUST belong to the documented configuration structure. An unknown, misspelled, or deprecated key MUST cause configuration resolution to fail with a clear diagnostic and no structured configuration output.
- **FR-026**: Documentation and task runners MAY directly invoke one executable with literal arguments. Control flow, variable manipulation, pipelines, redirection, data transformation, and multi-command orchestration are scripting logic and MUST be implemented in Python rather than shell syntax.

### Key Entities

- **Resolved Configuration**: The deterministic command input containing roadmap location and existence, ADR location and existence, PRD detection patterns, and the review finding limit.
- **Active Project**: The Spec Kit project root that bounds configuration discovery and all permitted roadmap, ADR, and PRD paths.
- **Runtime Payload**: The reviewed files installed for Diagram Roadmap, including command definitions, templates, configuration defaults, license, and the single supported scripting implementation.
- **Historical Record**: A merged feature artifact, dated generated report, or released changelog entry whose earlier platform and scripting statements remain evidence rather than current guidance.

## Scope Boundaries

This feature is a runtime and maintenance migration. It preserves the extension's judgment-bearing workflows while changing their deterministic execution boundary.

- **In scope**: Current extension-owned scripts; command runtime and prerequisite references; extension metadata and install allowlists; supported-platform automated tests; fixtures; task-runner scripting logic; current README and changelog guidance; current test documentation; and the repository's installed dogfood snapshot.
- **Out of scope**: Windows compatibility; Bash or PowerShell wrappers; multiple scripting implementations; removal of simple direct CLI invocations from documentation or task runners; behavioral redesign of roadmap write, brief, debrief, or sync judgment; compatibility aliases; retroactive edits to merged specifications or dated reports; external publication; and release automation.

## Success Criteria *(mandatory)*

The migration is successful when users and maintainers can verify one coherent supported contract without knowing how the replacement is internally structured.

### Measurable Outcomes

- **SC-001**: All four canonical commands complete their deterministic prerequisite path successfully in disposable projects on both supported operating systems, covering 8 command-and-platform combinations with no Bash or PowerShell runtime requirement.
- **SC-002**: 100% of the defined configuration acceptance cases pass on macOS and Linux, including defaults, source precedence, null fallthrough, special characters, zero and invalid limits, non-root working directories, missing paths, and project-containment failures.
- **SC-003**: A current-runtime repository and installed-payload scan reports zero Bash scripts, PowerShell scripts, shell-specific command frontmatter entries, compatibility wrappers, or maintained cross-language parity tests.
- **SC-004**: The replacement configuration output satisfies all six required fields and their types for 100% of valid fixtures and emits no structured output for 100% of invalid fixtures.
- **SC-005**: A disposable installation contains exactly the reviewed runtime payload, its newly scaffolded `roadmap-config.yml` represents the current configuration template, all four generated command skills resolve the supported runtime path, and every source-owned installed file matches its source counterpart byte-for-byte.
- **SC-006**: A current-documentation scan reports zero statements that advertise Windows support or Bash/PowerShell execution, excluding explicit non-goal statements, migration notes, and preserved historical records.
- **SC-007**: A maintainer can run one documented validation workflow on either supported operating system and receive an unambiguous pass or fail result for the complete supported-platform contract.
- **SC-008**: Runtime validation reports one exact Python version for both Specify and extension scripts, currently 3.11.16; transfers execution from an initially selected project or `PATH` interpreter to the verified active Specify interpreter; and rejects 100% of tested missing, unresolvable, unsupported-wrapper, and version-mismatch cases.
- **SC-009**: 100% of valid documented YAML fixtures resolve to the expected configuration, and 100% of malformed, structurally invalid, or unknown-key YAML fixtures fail with a clear diagnostic and no structured configuration output.
- **SC-010**: The documented dogfood scenarios for roadmap creation, roadmap amendment, briefing, debriefing, and synchronization produce their established outcomes: create writes a versioned roadmap without fabrication; amend preserves existing content and records its change; brief surfaces the matched entry and pre-implementation drift; debrief classifies implementation drift and proposes status without applying it; and sync reports ledger divergence without modifying the roadmap.

## Assumptions

- Roadmap entry 009 maps to this independently numbered `specs/006-python-script-migration/` directory; roadmap and feature directory numbers are not required to match.
- The extension's manifest compatibility requirement is narrowed to Specify CLI `==1.0.1`, the version covered by this feature's integration and cross-platform validation. Supporting another Specify version requires separately accepted compatibility evidence and a corresponding manifest change.
- Extension scripts use the active Specify installation's Python runtime. Specify CLI 1.0.1 does not guarantee that its generated `py:` command invocation initially selects that interpreter, so the Python entrypoint performs a bounded, standard-library-only bootstrap and isolated re-execution before importing PyYAML. The repository currently requires and pins Python 3.11.16 to match Specify; a future Specify runtime change requires the repository pin and compatibility validation to change together.
- The active Specify runtime supplies PyYAML as a runtime dependency. Specify CLI 1.0.1 requires PyYAML 6.0 or newer and the current installation provides 6.0.3; the extension does not declare or vendor a separate YAML dependency.
- A direct command invocation is not treated as Bash or PowerShell support when it contains no shell-specific scripting logic; such invocations remain permitted in documentation and task runners.
- The active project's existing configuration values and `SPECKIT_DIAGRAM_ROADMAP_*` environment variable names remain compatible.
- Project-relative path containment is part of the intended migration contract; configurations that currently rely on any absolute path or on an escaping relative path are unsupported and must be corrected.
- The repository-root source payload remains authoritative, and `.specify/extensions/diagram-roadmap/` remains a derived dogfood installation that must be refreshed during implementation.
- Roadmap entry 008 and `specs/005-rename-project-identity/` are complete dependencies; this feature does not revisit the accepted identity migration.
