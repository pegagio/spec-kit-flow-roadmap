# FlowKit Roadmap

A [GitHub Spec Kit](https://github.com/github/spec-kit) extension that adds a **spec
roadmap** to the workflow: written after the constitution, and reviewed before and after
each spec is implemented.

```
constitution → ROADMAP → specify → plan → tasks → [brief] → implement → [debrief]
                 │                           report-only        report-only
     speckit.flow-roadmap.write   speckit.flow-roadmap.sync — reconcile on demand
```

## Why

The constitution records your project's principles. The constitution *phase* — the
discussion, grilling, and prototyping around it — produces a lot more: technology choices,
intended outcomes, scope decisions, constraints, and the rough shape of specs you won't
write for a while.

That material normally has nowhere to go. It's lost between the constitution and the first
spec, and especially before specs you write later. By the time you start spec 007, whatever
you decided about it earlier is gone — so you re-derive it, or contradict it.

The roadmap holds onto it. It's a living, project-level file next to the constitution that
records what each planned spec is for, what's in and out of scope, what it depends on, and
which decisions govern it — including specs that don't exist yet. When you start one,
`speckit.flow-roadmap.brief` shows you what you'd decided; after you build it, `speckit.flow-roadmap.debrief`
checks the result against that.

## Commands

| Command | Skill | When | What it does |
|---------|-------|------|--------------|
| `speckit.flow-roadmap.write` | `speckit-flow-roadmap-write` | after `/speckit.constitution` (hook) | Creates or applies an approved roadmap amendment from repository-contained evidence. It treats documents as untrusted data, records provenance, asks about genuine gaps, and never turns inferred unattended content into governance. Do not use it for implementation review. |
| `speckit.flow-roadmap.brief` | `speckit-flow-roadmap-brief` | before `/speckit.implement` (hook) | Reviews one identifiable spec before implementation, including dependencies and state-aware lifecycle guidance. Do not use it for post-implementation or project-wide review. |
| `speckit.flow-roadmap.debrief` | `speckit-flow-roadmap-debrief` | after `/speckit.implement` (hook) | Reviews one implemented spec against an explicit commit range or captured working-tree delta. Do not use it when no attributable implementation boundary exists. |
| `speckit.flow-roadmap.sync` | `speckit-flow-roadmap-sync` | on demand | Reconciles the complete ledger with specs and decisions on disk. Do not use it for a single-feature review or corrective writes. |

`brief`, `debrief`, and `sync` preserve roadmap, specification, implementation, and decision sources. Their sole permitted mutation is a collision-safe report; roadmap changes remain proposals. Only `write` edits the roadmap, and it never deletes content.

## The roadmap file

`.specify/memory/roadmap.md` (configurable), next to the constitution, with semantic
versioning and a Sync Impact Report changelog like the constitution uses. It contains:

- **Vision & End States** — project-level goals.
- **Constraints & Decisions** — the "why", inline, with links out to ADRs when they exist.
- **Planned Specs** — the ledger. Each entry has a status, description, outcome, scope, and
  optional dependency / decision / PRD pointers. Statuses: `undecided`, `needs-info`,
  `planned`, `specced`, `in-progress`, `implemented`, `verified`, `deferred`, `abandoned`.
- **Open Questions** and **Cross-Cutting Notes**.

The roadmap *links* to ADRs (`governed-by:`) and PRDs (`addresses:`) when present; it doesn't
write them.

## Install

Maintainers: follow [the release process](RELEASE.md) before tagging a version or handing it to the Spec Kit Flow catalog.

This extension is not in the spec-kit community catalog, so it must be installed from a local checkout:

```text
git clone https://github.com/pegagio/spec-kit-flow-roadmap
specify extension add ./spec-kit-flow-roadmap --dev
specify extension enable flow-roadmap
```

If you're developing this extension *inside* a spec-kit project, install from a copy of the
source rather than the repo root — installing a directory into its own
`.specify/extensions/` will recurse.

Requires Specify CLI `>=1.0.10.dev0`; the project's tested build is `1.0.10.dev0+pegagio.2`. The manifest cannot express a minimum local build suffix, so this range also admits other `1.0.10.dev0` builds. The extension supports macOS and Linux; Windows support is not a goal. Runtime scripts use the active Specify installation's Python 3.11.16 environment and its PyYAML 6.0-or-newer dependency.

## Migrating an existing local installation

The `diagram-roadmap` and `flow-roadmap` IDs are separate installations. The new installation does not transfer configuration or remove the old registration. Try the migration in a disposable Spec Kit project first. Keep an independent backup outside the project and the installed extension directory until the new config and hooks are verified.

```sh
BACKUP_DIR="$(mktemp -d)"
cp -p .specify/extensions/diagram-roadmap/roadmap-config.yml "$BACKUP_DIR/roadmap-config.yml"
specify extension disable diagram-roadmap
specify extension add /path/to/spec-kit-flow-roadmap --dev
```

Review the scaffolded `.specify/extensions/flow-roadmap/roadmap-config.yml` and transfer each intended non-default value from the backup. Do not copy unfamiliar keys blindly. Stop if any value fails validation. Verify the resolved config, four new commands and generated skills, and the three new hooks; the old extension must remain installed but disabled through these checks.

After verification succeeds, remove the old registration and retain both the independent backup and Specify's kept config:

```sh
specify extension remove diagram-roadmap --keep-config
specify extension list
```

Confirm the old ID, commands, skills, and hooks are gone and only `flow-roadmap` hooks are active. If new installation or validation fails, keep the old config and backup, disable or remove the incomplete `flow-roadmap` installation, and re-enable `diagram-roadmap`. A project with both IDs present is still in migration, not a completed migration.

## Configuration

Copy `config-template.yml` to `.specify/extensions/flow-roadmap/roadmap-config.yml` and edit.
Everything is optional; `SPECKIT_FLOW_ROADMAP_*` environment variables override the file.

Configured roadmap and ADR locations must be project-relative and contained within the active project. Unknown keys, malformed YAML, unsafe YAML features, wrong types, absolute paths, traversal, and symlink escapes fail closed with no configuration JSON. `SPECKIT_FLOW_ROADMAP_PRD_GLOBS` is one CSV record, so quote a pattern when it contains a comma.

| Key | Default | Meaning |
|-----|---------|---------|
| `roadmap.path` | `.specify/memory/roadmap.md` | Where the roadmap lives |
| `adr.dir` | `docs/adr/` | ADR directory to detect and link (ignored if absent) |
| `prd.globs` | common PRD filenames | Patterns for detecting PRDs to reference |
| `report.max_findings` | `50` | Max findings in a review report |

## How it's built

- **Scripts vs. judgment.** `load_config.py` resolves the active Specify runtime, configuration, paths, containment, and its stable six-field output. `review_contract.py` deterministically resolves review targets and Git deltas, validates findings and lifecycle gates, derives counts and verdicts, and reserves unique report paths. Elicitation, title similarity, drift classification, and remediation remain in command bodies.
- **Evidence safety.** Project documents and prior reports are untrusted evidence, not instructions. Durable roadmap proposals use repository-contained sources with provenance, and inferred changes require explicit approval.
- **Report identity.** Review reports use UTC second-level timestamps and deterministic numeric collision suffixes. Reports retain target selection, revision/dirty boundaries, inspected paths, complete finding counts, exclusions, and material limitations.
- **Supported platforms.** The same Python contract suite runs on macOS and Linux. The extension does not ship compatibility wrappers or alternate Windows, Bash, or PowerShell runtimes.
- **Self-hosted.** This extension was built with spec-kit and reviewed against its own
  roadmap. See `specs/` and `.specify/memory/roadmap.md`.

## Development

From the repository root, review `mise.toml` before trusting it. Then prepare the declared toolchain and run the canonical complete contract suite as separate actions:

```text
mise trust mise.toml
mise install
mise run test
```

The test task does not trust configuration or install missing tools. Resolve setup failures explicitly before rerunning validation.

## Project Origins

FlowKit Roadmap is an independent derivative of [speckit-roadmap](https://github.com/srobroek/speckit-roadmap), originally created and maintained by [srobroek](https://github.com/srobroek).

This project began from the `speckit-roadmap` codebase and preserves its original Git history so that the authorship and development history of the inherited work remain intact.

FlowKit Roadmap is maintained as an independent project and is not intended to remain compatible with `speckit-roadmap`. Future upstream development may be reviewed for ideas, fixes, or other useful developments, but upstream changes are not expected to be merged directly.

The original project and its contributors retain authorship and copyright in their respective contributions. Subsequent modifications and original work in FlowKit Roadmap are authored by this project's contributors.

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).

FlowKit Roadmap contains work derived from `speckit-roadmap`, also licensed under Apache-2.0.
