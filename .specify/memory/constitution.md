<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 → 1.1.0
Bump rationale: MINOR — adds a binding governance section defining the
  Merge-Bounded Flow-Back Spec Persistence Model without redefining existing
  principles.

Modified principles: none.

Added sections:
  - Spec Evolution and Merge-Bounded Persistence

Removed sections: none.

Templates requiring review:
  ✅ .specify/memory/constitution.md (this file)
  ✅ Dependent templates and commands read the constitution at runtime; no changes required

Deferred / TODO: none.

Project note: this repository BUILDS a spec-kit extension (`speckit-roadmap`).
The principles below govern how that extension is designed, built, and packaged.
-->

# speckit-roadmap Constitution

`speckit-roadmap` is a GitHub spec-kit extension. It inserts a **roadmap** step
immediately after `/speckit.constitution` — capturing the spec-specific topics,
technology choices, outcomes, constraints, milestones, and scope discussed during
the constitution and grilling phases so they are not lost — and adds a
**pre-implementation** roadmap review (before `/speckit.implement`) and a
**post-implementation** roadmap review (after `/speckit.implement`) that check the
spec and its implementation against the roadmap.

## Core Principles

### I. Canonical Conformance

The extension MUST match real spec-kit extension conventions exactly. Ground truth,
in priority order: (1) the spec-kit documentation, (2) real bundled extensions
(e.g. `critique`, `verify`). The extension MUST ship a valid `extension.yml`
(`schema_version`, `extension`, `requires`, `provides`, `hooks`, `tags`),
command files under `commands/` whose `name:` is the full `speckit.{id}.{cmd}`
slug, paired `scripts/bash/` + `scripts/powershell/` scripts where scripts are
used, a `templates/` directory for generated-artifact skeletons, a
`config-template.yml`, and `README.md` + `CHANGELOG.md` + `LICENSE`.
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

### V. Cross-Platform Parity

Every shipped script MUST exist as a bash (`.sh`) and PowerShell (`.ps1`) pair with
equivalent behavior and identical output contracts. Commands MUST function on macOS,
Linux, and Windows. The `scripts.sh` / `scripts.ps1` frontmatter pair MUST reference
both.
*Rationale:* spec-kit users run all three platforms; a bash-only extension silently
breaks for Windows users and fails canonical conformance.

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
- **Scripts:** POSIX-compatible bash and PowerShell 7+, emitting JSON on a `--json`
  flag, reusing core `.specify/scripts/bash/common.sh` helpers where appropriate.
- **Hooks:** `after_constitution` (create roadmap), `before_implement`
  (pre-implementation review), `after_implement` (post-implementation review).
- **License:** Apache-2.0.

If a constraint here ever conflicts with a Core Principle, the principle wins.

## Development Workflow & Quality Gates

- **Spec-driven.** Material work proceeds through the spec-kit workflow; the roadmap
  is written after the constitution and consulted before/after each spec.
- **Constitution check.** Every plan MUST include a constitution check verifying the
  seven principles hold for the work proposed.
- **Script/command tests.** Deterministic scripts MUST have parity tests (bash and
  PowerShell produce the same JSON contract). Review commands MUST be demonstrated
  read-only.
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

**Version**: 1.1.0 | **Ratified**: 2026-06-24 | **Last Amended**: 2026-08-30
