# Feature Specification: Rename to FlowKit Roadmap

**Feature Branch**: `not-created`

**Created**: 2026-09-23

**Status**: Complete

**Input**: User decision to use FlowKit Roadmap as the human-readable project and extension name under the FlowKit brand, with project identifier `spec-kit-flow-roadmap`, extension ID `flow-roadmap`, and `speckit-flow-roadmap-<purpose>` generated skills; start roadmap entry 012 and document a manual migration that preserves existing configuration.

## Clarifications

### Session 2026-09-23

- Q: Should completing this feature require the GitHub repository and local checkout to be renamed to `spec-kit-flow-roadmap`, or is updating repository content enough? → A: Both the GitHub repository and local checkout must use `spec-kit-flow-roadmap` before the feature is accepted; coordinate the external rename operations separately.
- Sequencing clarification: The maintainer later specified that local checkout and worktree directory renames must happen after feature completion because moving the active project path would disrupt Codex. This supersedes the local-checkout timing in the answer above; local directory names are not a feature-acceptance gate.
- Q: After users migrate to FlowKit Roadmap, should the old `diagram-roadmap` command, skill, and environment variable names continue to work? → A: No; only the new names work after migration.
- Q: Once the new `flow-roadmap` installation and its configuration are verified, should the old `diagram-roadmap` extension be removed or kept installed but disabled? → A: Remove the old extension after verification and retain its configuration backup.
- Q: Is Linux execution of this feature's validation matrix required for acceptance? → A: No. Linux remains a supported runtime platform under Constitution V, but this feature's Linux validation is optional and does not block acceptance.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Install the renamed extension (Priority: P1)

As a Spec Kit user, I can install the renamed extension and invoke each existing roadmap purpose under one consistent FlowKit Roadmap identity.

**Why this priority**: Installation and command dispatch are the primary user experience. A display-name change without a working extension identity would leave the project unusable.

**Independent Test**: Install the extension in a disposable Spec Kit project, inspect its registered identity, four commands, four generated skills, three hooks, configuration, and runtime references, then invoke each command's prerequisite path.

**Acceptance Scenarios**:

1. **Given** a clean supported Spec Kit project, **When** a user installs and enables this extension, **Then** one `flow-roadmap` extension is registered and its four commands are `speckit.flow-roadmap.write`, `speckit.flow-roadmap.brief`, `speckit.flow-roadmap.debrief`, and `speckit.flow-roadmap.sync`.
2. **Given** the enabled extension, **When** a user inspects generated skills, **Then** the four skill names are `speckit-flow-roadmap-write`, `speckit-flow-roadmap-brief`, `speckit-flow-roadmap-debrief`, and `speckit-flow-roadmap-sync`, and each dispatches to the matching installed command.
3. **Given** the renamed extension, **When** constitution, pre-implementation, and post-implementation lifecycle hooks run, **Then** they dispatch to the corresponding `flow-roadmap` commands and preserve their existing behavior.

### User Story 2 - Find one coherent project identity (Priority: P2)

As a maintainer or contributor, I can identify the project as FlowKit Roadmap and follow current setup and development guidance without encountering conflicting active names.

**Why this priority**: Inconsistent repository, command, and configuration names cause installation errors and make the relationship to the FlowKit product group unclear.

**Independent Test**: Inspect current-facing project metadata, documentation, command descriptions, configuration guidance, installation paths, and validation surfaces; verify that their active identifiers agree and a clean installation follows the documented path.

**Acceptance Scenarios**:

1. **Given** current project documentation, **When** a contributor follows its install and configuration guidance, **Then** the project and extension display names are FlowKit Roadmap and the project identifier, extension ID, command names, generated skill names, installed paths, and configuration overrides agree.
2. **Given** a repository-wide identity review, **When** current-facing files are inspected, **Then** the old identity appears only where it is needed to explain migration or preserve accepted history.
3. **Given** merged feature records, dated reports, and released changelog entries, **When** the rename is made, **Then** their historical meaning and verification evidence remain intact.
4. **Given** the content changes are complete, **When** the maintainer evaluates feature acceptance, **Then** the GitHub repository name, configured origin URL, and current extension links use `spec-kit-flow-roadmap`, while local checkout and worktree paths may retain their prior basenames until after feature completion.

### User Story 3 - Migrate an existing installation safely (Priority: P3)

As a user with an existing `diagram-roadmap` installation, I can move to `flow-roadmap` through documented manual steps while preserving my configuration and avoiding duplicate roadmap hooks.

**Why this priority**: Changing the extension ID creates a second installation identity. Existing configuration and hook registration require an explicit transition.

**Independent Test**: Begin with a disposable project that has a configured `diagram-roadmap` installation, follow the documented migration, and compare its effective configuration and registered hooks before and after the transition.

**Acceptance Scenarios**:

1. **Given** an existing configured `diagram-roadmap` installation, **When** the user follows the migration guide, **Then** the old configuration is preserved until its values are reviewed and transferred to the new installation.
2. **Given** the new installation and transferred configuration have been verified, **When** the user completes the migration, **Then** the old `diagram-roadmap` extension is removed, only the intended `flow-roadmap` hooks are active, and a backup of the prior configuration remains recoverable.
3. **Given** a user installs `flow-roadmap` without migrating the old installation, **When** both identities are present, **Then** the documentation does not present that state as a completed migration.
4. **Given** a completed migration, **When** the user invokes an old command or skill name or sets an old environment override, **Then** the new extension does not accept it as an alias or active configuration input.

### Edge Cases

- The old and new extension identities coexist and both register equivalent lifecycle hooks.
- Validation of the new installation or transferred configuration fails before the old extension is removed.
- An existing configuration contains non-default values, unfamiliar keys, or values that fail the new extension's validation.
- A previous generated skill, installed payload path, command reference, or environment override still points to `diagram-roadmap` after the rename.
- The repository's dogfood installation contains local configuration that must survive replacement of the installed payload.
- A current-facing identifier scan encounters old names in historical feature directories, dated reports, released changelog entries, or migration guidance.
- The Spec Kit Flow bundle currently names a separate roadmap prerequisite; this feature does not change that bundle or claim adoption by it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The current project and extension display names MUST be `FlowKit Roadmap`, and the current project and repository identifier MUST be `spec-kit-flow-roadmap`.
- **FR-002**: The installable extension MUST use ID `flow-roadmap` and retain exactly four existing purposes: `write`, `brief`, `debrief`, and `sync`.
- **FR-003**: The canonical command IDs MUST be `speckit.flow-roadmap.write`, `speckit.flow-roadmap.brief`, `speckit.flow-roadmap.debrief`, and `speckit.flow-roadmap.sync`.
- **FR-004**: A supported installation MUST generate `speckit-flow-roadmap-write`, `speckit-flow-roadmap-brief`, `speckit-flow-roadmap-debrief`, and `speckit-flow-roadmap-sync` skills, each bound to the corresponding command.
- **FR-005**: Command definitions, three lifecycle-hook registrations, installed paths, configuration names and environment overrides, templates, and current usage guidance MUST resolve through the `flow-roadmap` identity without stale active `diagram-roadmap` references. The active configuration path MUST be `.specify/extensions/flow-roadmap/roadmap-config.yml`, and environment overrides MUST use the `SPECKIT_FLOW_ROADMAP_*` prefix.
- **FR-006**: The rename MUST preserve the existing behavior, evidence boundaries, report semantics, and supported platforms of all four purposes; it MUST NOT introduce a fifth command, new hook, or new roadmap behavior.
- **FR-007**: The project MUST provide a documented manual migration from `diagram-roadmap` that preserves the existing configuration until the user reviews and transfers its values and verifies the new registration. Only after that verification may the procedure remove the old extension, and it MUST retain a recoverable backup of the old configuration.
- **FR-008**: The migration guidance MUST distinguish the two extension identities and MUST NOT imply that installing `flow-roadmap` automatically converts or removes an existing `diagram-roadmap` installation.
- **FR-009**: Current-facing project metadata and documentation MUST use the new project and extension identities; merged feature directories, dated reports, prior roadmap entries, and released changelog history MUST retain their accepted historical meaning.
- **FR-010**: The renamed extension MUST remain a separately installable component. This feature MUST NOT edit the separate Spec Kit Flow bundle or The Diagram consumer, nor claim either has adopted it.
- **FR-011**: The source and self-installed dogfood copies, generated skills, and the reviewed runtime payload MUST agree on the renamed identity; validation MUST cover installation, command dispatch, hooks, configuration preservation, and current-facing identity consistency.
- **FR-012**: Feature acceptance MUST require the GitHub repository name, configured `origin` URL, and current `extension.yml` repository and homepage links to use `spec-kit-flow-roadmap`. Local checkout and worktree directory basenames are operational paths and MAY retain their prior names through feature completion; the maintainer will rename them afterward to avoid disrupting the active Codex task.
- **FR-013**: The new extension MUST NOT expose compatibility aliases for `speckit.diagram-roadmap.*` commands, `speckit-diagram-roadmap-*` skills, or `SPECKIT_DIAGRAM_ROADMAP_*` environment overrides; only the `flow-roadmap` identity is active after migration.
- **FR-014**: A completed migration MUST leave the old `diagram-roadmap` extension uninstalled, its old hooks inactive, and its preserved configuration backup available for recovery. If new-installation verification fails, the procedure MUST leave the old installation and configuration available rather than removing them.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A clean supported project installs one extension displayed as `FlowKit Roadmap` with ID `flow-roadmap` and exposes all four required commands and all four generated skills with the exact names in FR-003 and FR-004.
- **SC-002**: All three lifecycle events dispatch to the intended renamed command in a disposable project, with no duplicate hook execution after a completed migration.
- **SC-003**: A user following the manual migration retains 100% of reviewed existing configuration values or receives an explicit validation error before replacing the old active configuration.
- **SC-004**: Current-facing identity validation finds zero obsolete active project, extension, command, skill, installed-path, or environment-override names; historical and migration references remain identifiable as such.
- **SC-005**: The four existing command purposes pass the project's relevant contract checks after renaming, and the installed runtime payload matches its reviewed source.
- **SC-006**: A maintainer can identify the FlowKit Roadmap display name, project ID, extension ID, command namespace, skill namespace, and manual migration path from the current README without consulting historical feature records.
- **SC-007**: The existing command contracts and new identity pass the required validation on macOS. Linux remains a supported runtime platform under Constitution V; Linux execution is optional for this feature's acceptance.
- **SC-008**: At acceptance, the GitHub repository name, configured `origin` URL, and current extension repository and homepage links use `spec-kit-flow-roadmap`. Local checkout and worktree directory renames occur after feature completion.
- **SC-009**: A completed migration exposes zero old command or generated-skill aliases, and old environment override names do not affect the new extension's resolved configuration.
- **SC-010**: In a disposable migration, the old extension remains available through any failed new-installation validation; after a successful migration it is absent from the installed registry, its hooks are inactive, and its configuration backup remains readable.

## Assumptions

- The required skill spelling is produced by the supported Specify 1.0.1 mapping from `speckit.flow-roadmap.<purpose>` to `speckit-flow-roadmap-<purpose>`.
- FlowKit is the brand for the spec-kit-flow product group; it does not change the selected project, extension, command, or skill identifiers.
- Roadmap entries 008, 009, and 010 are verified dependencies. Entry 011's deferred Linux verification is a separate gate and is not treated as completed by this rename.
- The GitHub repository rename is coordinated separately and required before feature acceptance. Local checkout and worktree directory renames are post-feature operational follow-up and are not required for acceptance; this specification does not itself perform either operation.
- This is an identity migration within the existing roadmap extension, not a behavioral redesign or automatic replacement of the separate roadmap prerequisite currently named by the Spec Kit Flow bundle.
- Existing installations migrate manually without automatic configuration conversion.
