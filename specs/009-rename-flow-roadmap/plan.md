# Implementation Plan: Rename to FlowKit Roadmap

**Checkout branch**: `develop` | **Active feature**: `009-rename-flow-roadmap` | **Date**: 2026-09-23 | **Spec**: [spec.md](spec.md)

## Summary

Rename this separately installable roadmap extension to the FlowKit Roadmap identity: repository ID `spec-kit-flow-roadmap`, extension ID `flow-roadmap`, four `speckit.flow-roadmap.*` commands, four `speckit-flow-roadmap-*` generated skills, and `SPECKIT_FLOW_ROADMAP_*` configuration overrides. Preserve the four existing behaviors and three lifecycle hooks. Migrate existing installations manually by backing up configuration, disabling the old extension before installing the new identity, validating the new configuration and hooks, and only then removing the old installation. The GitHub repository rename, configured remote, and extension links are acceptance gates; local checkout and worktree directory renames are deferred until after feature completion to avoid disrupting Codex.

## Technical Context

**Language/Version**: Python 3.11.16 for runtime and tests; Markdown and YAML for commands, metadata, templates, and governance.

**Primary Dependencies**: Specify CLI 1.0.1, pinned by `mise.toml`; its existing YAML support. No new dependency or build tool.

**Storage**: Files in the repository and Spec Kit project: extension manifest, commands, config template, installed extension payload, `.specify/extensions.yml` registry and hooks, `.specify/extensions/<id>/roadmap-config.yml`, and generated skills.

**Testing**: Existing standard-library `unittest` suite through `mise run test`; disposable Specify project installation and migration checks; current-surface identity scan; required contract validation on macOS. Linux execution is optional for this feature's acceptance.

**Target Platform**: macOS and Linux. Windows remains outside the supported contract.

**Project Type**: Standalone Spec Kit extension with a Python deterministic runtime and Markdown agent commands.

**Performance Goals**: Existing command/runtime behavior and practical execution time remain unchanged; the rename adds no runtime work.

**Constraints**: Exactly four purposes and three hooks; no old-name aliases; no automatic migration; preserve reviewed configuration and accepted historical records; source and installed payload must agree; do not edit the separate Spec Kit Flow bundle or The Diagram consumer.

**Scale/Scope**: One extension source, its self-installed dogfood copy and generated skills, active documentation/governance, current identity tests, and a separately coordinated GitHub repository rename. Local checkout/worktree directory renames are post-feature operational follow-up.

## Constitution Check

The pre-research gate passes. The post-design check also passes; the identity and migration contracts below preserve the same boundaries.

| Principle | Plan and design check |
| --- | --- |
| I. Canonical Conformance | Retain Specify 1.0.1 manifest shape, command files, Python scripts, templates, and installable payload; validate actual generated skills and hooks. |
| II. Determinism Split | Keep config/path resolution and validation in Python; retain command judgment in command bodies. The rename adds no behavioral logic. |
| III. Non-Destructive & Idempotent | Back up and review old configuration before transfer; make failed new-install validation recoverable; preserve historical roadmap and report evidence. |
| IV. Roadmap as Durable Governance | Keep the project roadmap beside the constitution and preserve its versioned history; amend only current-facing identity with a Sync Impact Report when implementation requires it. |
| V. Supported Platforms and Python Scripting | Keep runtime scripts Python-only and support both macOS and Linux; this feature requires validation on macOS, while Linux execution is optional for acceptance. |
| VI. Elicitation Completeness | Preserve the existing write-command elicitation contract; introduce no synthetic roadmap content. |
| VII. Dogfood the Workflow | Keep entry 012 in progress through Specify planning/tasking, then exercise the renamed installed extension on this project before acceptance. |
| Merge-Bounded Flow-Back | Reconcile discoveries in this unmerged feature's spec, plan, and later tasks; leave merged feature directories, dated reports, and released changelog entries semantically intact. |

No constitution violation needs a complexity exception. Renaming the current constitution title and project note is an implementation artifact change under its amendment rules, not a change to its seven principles.

## Project Structure

### Documentation for this feature

```text
specs/009-rename-flow-roadmap/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/
│   ├── identity-contract.md
│   └── migration-contract.md
└── quickstart.md
```

`tasks.md` belongs to the later `$speckit-tasks` phase.

### Repository surfaces in scope

```text
extension.yml                    # extension identity, commands, hooks
.extensionignore                 # packaged command allowlist
commands/                        # four command definitions
scripts/python/                  # config and review contract resolution
templates/                       # current report template
config-template.yml              # installed config template
README.md, ORIGINS.md            # current user/contributor guidance
CHANGELOG.md                     # unreleased rename record only
tests/python/                    # identity, installation, behavior contracts
.specify/memory/constitution.md  # current-facing identity, versioned amendment
.specify/memory/roadmap.md       # entry 012 and versioned governance
.specify/extensions.yml          # dogfood registration and hooks
.specify/extensions/.registry    # installer-managed installed registry
.specify/extensions/<id>/        # dogfood payload and retained config
.agents/skills/                  # generated skill entries
```

**Structure decision**: Keep the existing root extension structure. The root is authoritative source. Use Specify's installer for the dogfood transition; its registry and generated skills are derived installation state. Preserve merged `specs/001-*` through `specs/008-*`, dated reports, prior roadmap entries, and released changelog content as historical evidence.

## Delivery Sequence

1. Update root metadata, command filenames/front matter and references, Python config resolution, templates, current docs, unreleased changelog, and current constitution identity. Keep the existing purpose contracts and exact hook count.
2. Update identity and config tests, including stale-name rejection and protected-history boundaries. Validate packaged payload allowlist before installing.
3. Prove a clean install and manual migration in disposable projects, including non-default configuration, failure rollback, generated skills, command dispatch, hook uniqueness, and source/installed payload parity.
4. Migrate this repository's dogfood installation with an explicit old-config backup and Specify CLI operations. Inspect tracked `.specify/extensions.yml`, registry, installed config, and generated skills as one change set.
5. Run the existing tests and required acceptance checks on macOS. Linux execution is optional for this feature and does not change the Constitution V runtime support contract. Verify the renamed GitHub repository, configured `origin`, and extension links before feature acceptance. Defer local checkout/worktree directory renames until afterward so the active Codex task remains attached to its current path.

## Complexity Tracking

No constitution violations or new architectural components are planned.
