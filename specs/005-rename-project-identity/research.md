# Research: Rename Project Identity

This research resolves the naming and migration decisions needed for a consistent pre-1.0 identity change.

## Repository and command spelling

**Decision**: Use `spec-kit-diagram-roadmap` for the repository and `speckit.diagram-roadmap.*` for commands.

**Rationale**: “Spec Kit” is the product and repository spelling, while Specify requires the literal `speckit` prefix for extension commands. Keeping those conventions distinct avoids the redundant `speckit.speckit-diagram-roadmap.*` namespace.

**Alternatives considered**: `speckit-diagram-roadmap` for every layer was rejected because an extension ID with that value would duplicate the required command prefix. Keeping `diagram-roadmap-kit` was rejected because the user explicitly removed the Kit suffix.

## Extension identity and compatibility

**Decision**: Use `diagram-roadmap` as the extension ID and make `speckit.diagram-roadmap.*` the only canonical command set, without aliases.

**Rationale**: Specify CLI 1.0.1 requires the namespace segment of every primary command to equal the extension ID. A clean break is appropriate before the first `0.2.0` tag and avoids collisions with an installed upstream `roadmap` extension.

**Alternatives considered**: Retaining `speckit.roadmap.*` as aliases was rejected because it preserves obsolete public surface area and can collide with the original extension.

## Installation directory and configuration migration

**Decision**: Move all active runtime references to `.specify/extensions/diagram-roadmap/` and document configuration migration as an explicit user operation.

**Rationale**: Specify derives the installed directory from the extension ID. The installer treats a changed ID as a distinct extension and cannot safely infer whether an old `roadmap-config.yml` should be moved or merged.

**Alternatives considered**: Automatically reading or migrating the former directory was rejected as hidden compatibility behavior and an unnecessary pre-1.0 migration mechanism.

## Environment override namespace

**Decision**: Rename the configuration override prefix from `SPECKIT_ROADMAP_*` to `SPECKIT_DIAGRAM_ROADMAP_*` without compatibility fallback.

**Rationale**: Environment variables are a public configuration interface. Retaining the former namespace would make the identity migration incomplete and create a legacy contract before `0.2.0` has been released.

**Alternatives considered**: Supporting both prefixes was rejected because it adds hidden compatibility behavior and ambiguity over precedence. Leaving the old prefix was rejected as inconsistent with the clean-break command and extension naming decision.

## Historical persistence boundary

**Decision**: Update the living constitution and roadmap, add an `Unreleased` changelog entry, and preserve features 001–004, the dated roadmap-sync report, and the `0.1.0` changelog entry verbatim.

**Rationale**: Current governance and planning documents must describe the project that now exists, while merge-bounded persistence forbids retroactively rewriting accepted feature history.

**Alternatives considered**: Repository-wide blind replacement was rejected because it would falsify historical records. Leaving current governance under the old project name was rejected because it would remain operationally misleading.

## Packaging boundary

**Decision**: Keep the exact reviewed allowlist strategy and change only the four allowed command filenames.

**Rationale**: A catch-all exclusion with explicit runtime inclusions prevents local `--dev` installation from copying `.git`, local tools, specifications, tests, or repository documentation.

**Alternatives considered**: A blocklist was rejected because future development files would be copied unless continuously enumerated.
