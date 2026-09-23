<!--
SYNC IMPACT REPORT
==================
Version change: 2.0.1 → 2.0.2
Bump rationale: PATCH — updates current project and extension identity wording
  without changing a principle or technology constraint.

Modified principles: none.

Modified sections:
  - Current project note and opening description

Added sections: none.
Removed sections: none.

Templates requiring review:
  ✅ .specify/memory/constitution.md (current identity wording only)
  ✅ Dependent templates and commands; no changes required

Deferred / TODO: none.

Project note: this repository BUILDS FlowKit Roadmap, the separately installable
Spec Kit extension in the spec-kit-flow product group. Its project identifier is
`spec-kit-flow-roadmap`; its extension ID is `flow-roadmap`.
-->

<!--
SYNC IMPACT REPORT
==================
Version change: 2.0.0 → 2.0.1
Bump rationale: PATCH — removes obsolete references to retired scripting
  implementations while preserving the Python-only platform contract.

Modified principles:
  - V. Supported Platforms and Python Scripting (removed stale implementation and migration wording)

Modified sections:
  - Technology Constraints & Packaging
  - Development Workflow & Quality Gates

Added sections: none.

Removed sections: none.

Removed references:
  - Retired scripting implementations and their completed migration work

Templates requiring review:
  ✅ .specify/memory/constitution.md (this file)
  ✅ Dependent templates and commands read the constitution at runtime; no changes required

Deferred / TODO: none.

Project note: this repository BUILDS the Diagram Roadmap spec-kit extension (`diagram-roadmap`).
The principles below govern how that extension is designed, built, and packaged.
-->

# FlowKit Roadmap Constitution

FlowKit Roadmap is a GitHub spec-kit extension. It inserts a **roadmap** step
immediately after `/speckit.constitution` — capturing the spec-specific topics,
technology choices, outcomes, constraints, milestones, and scope discussed during
the constitution and grilling phases so they are not lost — and adds a
**pre-implementation** roadmap review (before `/speckit.implement`) and a
**post-implementation** roadmap review (after `/speckit.implement`) that check the
spec and its implementation against the roadmap.

## Core Principles

### I. Canonical Conformance

The extension MUST match real spec-kit extension conventions exactly within its supported platform contract. Ground truth, in priority order: (1) the spec-kit documentation, (2) real bundled extensions (e.g. `critique`, `verify`). The extension MUST ship a valid `extension.yml` (`schema_version`, `extension`, `requires`, `provides`, `hooks`, `tags`), command files under `commands/` whose `name:` is the full `speckit.{id}.{cmd}` slug, Python scripts where scripts are used, a `templates/` directory for generated-artifact skeletons, a `config-template.yml`, and `README.md` + `CHANGELOG.md` + `LICENSE`.
*Rationale:* an extension that deviates from the loader's expected shape will not
install, register, or hook correctly; conformance is what makes it work at all.

### II. Determinism Split

Deterministic mechanics MUST live in scripts; non-deterministic judgment MUST live
in command/skill bodies. Scripts own: path/feature resolution, prerequisite checks,
JSON output contracts, version/changelog arithmetic, and file-existence checks.
Command bodies own: elicitation, roadmap synthesis, drift detection, and review
reasoning. A command MUST NOT re-derive in prose what a script can compute exactly,
and a script MUST NOT embed judgment that belongs to the model.
*Rationale:* deterministic work must be reproducible and testable; reasoning work
must not be faked by brittle string logic. The split keeps each honest.

### III. Non-Destructive & Idempotent

Commands MUST NOT overwrite user-authored content. Review commands are STRICTLY
READ-ONLY: they emit reports and PROPOSE changes, and only apply edits after
explicit user approval. Every command MUST be safe to re-run. Roadmap updates
MUST append to a versioned changelog (Sync Impact Report) rather than silently
clobber prior content; superseded entries are struck through or marked deprecated,
never deleted.
*Rationale:* the roadmap and constitution are durable records of *why* decisions
were made; destroying that history defeats the extension's entire purpose.

### IV. Roadmap as Durable Governance

The roadmap is a project-level governance artifact, not a per-feature scratch file.
It MUST live beside the constitution (default `.specify/memory/roadmap.md`,
overridable via `config-template.yml`), carry constitution-style semantic
versioning with a Sync Impact Report changelog, and survive across features. It
MUST capture the WHY — decisions, technology choices, intended outcomes, and
constraints — and the cross-spec map (planned specs, dependencies, status), not
merely a task list.
*Rationale:* constitution-phase discussion, grilling, and prototyping insight are
otherwise lost between features; the roadmap is the institutional memory that the
pre/post reviews check against.

### V. Supported Platforms and Python Scripting

The extension MUST support macOS and Linux. Windows support is explicitly not a goal. Every extension-owned runtime script and maintained automation script MUST be written in Python, and extension commands MUST use platform-neutral Python interfaces at runtime.
*Rationale:* one portable scripting language keeps deterministic behavior and tests consistent across the supported platforms without the cost and drift of parallel shell implementations.

### VI. Elicitation Completeness

The create-roadmap command MUST actively ask the user for end states, goals,
milestones, scope (in and out), features, outcomes, and constraints wherever these
are not already settled by the constitution conversation. It MUST NOT fabricate
roadmap content to fill gaps; unknowns are surfaced as explicit questions or marked
as open items.
*Rationale:* a roadmap is only valuable if it records what was actually decided;
guessing produces a confident, wrong record that the reviews then enforce.

### VII. Dogfood the Workflow

The extension MUST be developed through spec-kit's own workflow
(constitution → roadmap → specify → plan → tasks → implement) and reviewed against
its own roadmap. Its own commands are exercised on this repository before release.
*Rationale:* building the roadmap extension *through* a roadmap step is the most
direct proof that the artifact format, scripts, and reviews actually work.

## Technology Constraints & Packaging

The principles above are binding. The specific tooling that realizes them is a
decision owned by specs and the roadmap, and may change without amending this
document, provided the principles still hold:

- **Distribution:** a spec-kit extension installed via `specify extension add` /
  `enable`; source of truth lives at the repository root
  (`extension.yml`, `commands/`, `scripts/`, `templates/`, `config-template.yml`).
- **Supported platforms:** macOS and Linux. Windows compatibility is out of scope.
- **Scripts:** Python, emitting stable JSON contracts where structured output is required.
- **Hooks:** `after_constitution` (create roadmap), `before_implement`
  (pre-implementation review), `after_implement` (post-implementation review).
- **License:** Apache-2.0.

If a constraint here ever conflicts with a Core Principle, the principle wins.

## Development Workflow & Quality Gates

- **Spec-driven.** Material work proceeds through the spec-kit workflow; the roadmap
  is written after the constitution and consulted before/after each spec.
- **Constitution check.** Every plan MUST include a constitution check verifying the
  seven principles hold for the work proposed.
- **Script/command tests.** Deterministic Python scripts MUST have automated tests on macOS and Linux. Review commands MUST be demonstrated read-only. Validation MUST confirm that the shipped extension's runtime scripts are Python.
- **Conformance check.** Before release, the extension MUST install and its hooks
  MUST fire in a real spec-kit project (dogfooded on this repo).

## Spec Evolution and Merge-Bounded Persistence

The project MUST use the Merge-Bounded Flow-Back Spec Persistence Model.

- **One mutable change set**: Before a feature is merged, its `spec.md`, `plan.md`, `tasks.md`, and implementation MUST be treated as one mutable, reviewable unit.
- **Changes flow back**: Accepted discoveries MAY originate in any artifact, but their consequences MUST be applied throughout the artifact set before work proceeds from the changed direction. A change to intended behavior MUST be reflected in `spec.md`; a change to technical approach MUST be reflected in `plan.md`; and a change to the required work MUST be reflected in `tasks.md`. Lower-level artifacts and implementation MUST NOT silently contradict higher-level intent.
- **Scope requires acceptance**: Flow-back MUST NOT be used to introduce material scope without review. Independently valuable behavior, substantial scope expansion, or work requiring separate acceptance MUST be captured as a separate feature.
- **Consistency gates implementation and merge**: After tasking or consequential artifact reconciliation, the agent MUST run `/speckit.analyze` before starting or resuming implementation. After implementation, the agent MUST use `/speckit.converge` until no gaps remain. Known divergence MUST block implementation or merge until it is reconciled or explicitly removed from scope.
- **Merge freezes history**: Acceptance into the project's designated integration branch is the persistence boundary. After that merge, the feature directory MUST be treated as a semantically immutable historical record. Editorial corrections MAY improve presentation only when they do not alter meaning.
- **Later changes flow forward**: A later requirement or behavioral change MUST be expressed in a new feature directory. The new feature MUST reference any earlier feature that it amends, replaces, or depends on when that relationship is material, and MUST NOT rewrite the earlier feature to describe the new outcome retroactively.

**Rationale:** This model permits requirements and implementation knowledge to converge while a feature is being developed, makes the merged feature a coherent unit of review, and preserves an auditable sequence of accepted changes without rewriting project history.

## Governance

This constitution supersedes other practices where they conflict.

- **Amendment.** Principles change only by explicit amendment to this file, with a
  Sync Impact Report recording the change and rationale.
- **Versioning.** Semantic versioning applies: MAJOR for principle removal or
  redefinition or backward-incompatible governance change; MINOR for a new principle
  or materially expanded section; PATCH for clarifications and wording.
- **Compliance review.** Plans and reviews MUST verify compliance; violations are
  fixed or justified in the plan's Complexity Tracking, never silently accepted.
- **Precedence.** Where Technology Constraints and a Core Principle conflict, the
  principle wins.

**Version**: 2.0.2 | **Ratified**: 2026-06-24 | **Last Amended**: 2026-09-23
