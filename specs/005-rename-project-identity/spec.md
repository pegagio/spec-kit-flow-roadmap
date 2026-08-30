# Feature Specification: Rename Project Identity

**Feature Branch**: `naming`

**Created**: 2026-08-30

**Status**: Complete

**Input**: User description: "Rename the project holistically around the diagram-roadmap identity, drop the Kit suffix, and use spec-kit-diagram-roadmap as the repository and local checkout identity. The user will perform the external GitHub and filesystem rename operations directly."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Install the consistently named extension (Priority: P1)

As a local dogfooding user, I can install Diagram Roadmap and receive commands, configuration, and runtime files whose names consistently use the `diagram-roadmap` extension identity.

**Why this priority**: Installation and command registration are the extension's primary user-facing behavior; inconsistent identifiers prevent installation or leave broken runtime references.

**Independent Test**: Install the extension into a disposable Spec Kit project and verify its registered identity, four commands, generated skills, configuration scaffold, and installed runtime paths.

**Acceptance Scenarios**:

1. **Given** a fresh Spec Kit project, **When** the extension is installed from the local checkout, **Then** it is registered as `diagram-roadmap` at version `0.2.0`.
2. **Given** the installed extension, **When** its provided commands and hooks are inspected, **Then** all four canonical commands use the `speckit.diagram-roadmap.*` namespace and resolve their runtime files under `.specify/extensions/diagram-roadmap/`.

---

### User Story 2 - Understand the renamed project (Priority: P2)

As a maintainer or contributor, I see Diagram Roadmap presented consistently and receive accurate instructions for the intended `spec-kit-diagram-roadmap` repository and local installation workflow.

**Why this priority**: Clear identity and migration instructions prevent contributors from recreating the obsolete project, extension, or command names.

**Independent Test**: Review current-facing metadata and documentation and verify that they use the new identity while historical accepted records retain their original terminology.

**Acceptance Scenarios**:

1. **Given** the current project documentation, **When** a contributor follows the installation instructions after the repository rename, **Then** the documented checkout, extension ID, installed directory, and commands agree.
2. **Given** released changelog entries and merged feature records, **When** the rename is applied, **Then** those historical records are not retroactively rewritten.

### Edge Cases

- An existing installation registered as `roadmap` is a separate extension identity and is not silently migrated or overwritten.
- Installing the renamed extension alongside the old extension must not be presented as a supported migration path because their lifecycle hooks serve the same purpose.
- The tracked implementation does not perform GitHub repository or local filesystem rename operations; the user completed those external operations directly before this feature change set closed.
- Historical references in released changelog entries, merged feature directories, and dated generated reports remain discoverable and are not treated as active naming defects.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The current project display name MUST be `Diagram Roadmap` and MUST NOT retain the `Kit` suffix.
- **FR-002**: The extension manifest MUST identify the extension as `diagram-roadmap` at version `0.2.0`.
- **FR-003**: The extension MUST provide exactly `speckit.diagram-roadmap.write`, `speckit.diagram-roadmap.brief`, `speckit.diagram-roadmap.debrief`, and `speckit.diagram-roadmap.sync` as its canonical commands.
- **FR-004**: Command files, hook references, templates, scripts, tests, configuration guidance, environment overrides, and installed runtime references MUST consistently use the new command namespace, `SPECKIT_DIAGRAM_ROADMAP_*` environment prefix, and `.specify/extensions/diagram-roadmap/` installation directory.
- **FR-005**: Current repository metadata and documentation MUST use the intended repository name and URL `pegagio/spec-kit-diagram-roadmap`.
- **FR-006**: The source repository MUST retain a narrow reviewed installation payload that excludes repository metadata, local tooling, specifications, tests, and other development-only files.
- **FR-007**: The rename MUST preserve the historical terminology in the released `0.1.0` changelog entry, merged feature directories, and dated generated reports.
- **FR-008**: The current changelog MUST record the identity migration under `Unreleased`.
- **FR-009**: The extension MUST NOT retain the former `speckit.roadmap.*` commands as aliases.
- **FR-010**: The tracked implementation MUST NOT perform the GitHub repository or local checkout rename operations; the user owns those external operations, and the completed feature state MUST use `pegagio/spec-kit-diagram-roadmap` and `spec-kit-diagram-roadmap` respectively.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A disposable local installation completes successfully and registers one `diagram-roadmap` extension with all four expected commands and hooks.
- **SC-002**: All four generated command skills reference only the `.specify/extensions/diagram-roadmap/` runtime directory.
- **SC-003**: The installed payload contains exactly the reviewed runtime source files plus the generated configuration scaffold, with no `.git`, local agent tooling, IDE configuration, specifications, tests, README, or changelog content.
- **SC-004**: A repository-wide identity scan reports no obsolete command, installation, environment-variable, project, repository, or checkout names in current-facing project files; any remaining matches are confined to explicitly preserved historical records or migration guidance.
- **SC-005**: The Bash loader executes from the installed payload and emits valid configuration output after the rename.

## Assumptions

- The intended repository name is `spec-kit-diagram-roadmap`, while `speckit` remains the required command prefix.
- Existing local dogfood configuration will be migrated deliberately after the code change rather than automatically by the extension installer.
- The unreleased `0.2.0` version is the correct release boundary for this breaking pre-1.0 identity change.
- The user completed the GitHub repository and local checkout renames directly during this feature change set; those external operations are accepted final-state context rather than implementation work performed by the extension change.
