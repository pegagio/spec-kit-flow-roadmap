# Diagram Roadmap

A [GitHub Spec Kit](https://github.com/github/spec-kit) extension that adds a **spec
roadmap** to the workflow: written after the constitution, and reviewed before and after
each spec is implemented.

```
constitution → ROADMAP → specify → plan → tasks → [brief] → implement → [debrief]
                 │                           report-only        report-only
     speckit.diagram-roadmap.write   speckit.diagram-roadmap.sync — reconcile on demand
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
`speckit.diagram-roadmap.brief` shows you what you'd decided; after you build it, `speckit.diagram-roadmap.debrief`
checks the result against that.

## Commands

| Command | When | What it does |
|---------|------|--------------|
| `speckit.diagram-roadmap.write` | after `/speckit.constitution` (hook) | Creates or applies an approved roadmap amendment from repository-contained evidence. It treats documents as untrusted data, records provenance, asks about genuine gaps, and never turns inferred unattended content into governance. Do not use it for implementation review. |
| `speckit.diagram-roadmap.brief` | before `/speckit.implement` (hook) | Reviews one identifiable spec before implementation, including dependencies and state-aware lifecycle guidance. Do not use it for post-implementation or project-wide review. |
| `speckit.diagram-roadmap.debrief` | after `/speckit.implement` (hook) | Reviews one implemented spec against an explicit commit range or captured working-tree delta. Do not use it when no attributable implementation boundary exists. |
| `speckit.diagram-roadmap.sync` | on demand | Reconciles the complete ledger with specs and decisions on disk. Do not use it for a single-feature review or corrective writes. |

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

This extension is not in the spec-kit community catalog, so it must be installed from a local checkout:

```text
git clone https://github.com/pegagio/spec-kit-diagram-roadmap
specify extension add ./spec-kit-diagram-roadmap --dev
specify extension enable diagram-roadmap
```

If you're developing this extension *inside* a spec-kit project, install from a copy of the
source rather than the repo root — installing a directory into its own
`.specify/extensions/` will recurse.

Requires Specify CLI 1.0.1 exactly. The extension supports macOS and Linux; Windows support is not a goal. Runtime scripts use the active Specify installation's Python 3.11.16 environment and its PyYAML 6.0-or-newer dependency.

## Migrating an existing local installation

The `diagram-roadmap` identity is a clean break from the former `roadmap` extension. Preserve the existing configuration, remove the old extension, install the renamed source, compare the preserved values with the new scaffold, and enable the new identity:

```text
specify extension remove roadmap --keep-config
specify extension add /path/to/spec-kit-diagram-roadmap --dev
diff -u .specify/extensions/diagram-roadmap/roadmap-config.yml .specify/extensions/roadmap/roadmap-config.yml
cp .specify/extensions/roadmap/roadmap-config.yml .specify/extensions/diagram-roadmap/roadmap-config.yml
specify extension enable diagram-roadmap
```

Run the `cp` step only after reviewing the diff. Once the renamed commands and configuration are verified, the preserved `.specify/extensions/roadmap/` directory can be removed deliberately.

## Configuration

Copy `config-template.yml` to `.specify/extensions/diagram-roadmap/roadmap-config.yml` and edit.
Everything is optional; `SPECKIT_DIAGRAM_ROADMAP_*` environment variables override the file.

Configured roadmap and ADR locations must be project-relative and contained within the active project. Unknown keys, malformed YAML, unsafe YAML features, wrong types, absolute paths, traversal, and symlink escapes fail closed with no configuration JSON. `SPECKIT_DIAGRAM_ROADMAP_PRD_GLOBS` is one CSV record, so quote a pattern when it contains a comma.

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

Diagram Roadmap is an independent derivative of [speckit-roadmap](https://github.com/srobroek/speckit-roadmap), originally created and maintained by [srobroek](https://github.com/srobroek).

This project began from the `speckit-roadmap` codebase and preserves its original Git history so that the authorship and development history of the inherited work remain intact.

Diagram Roadmap is maintained as an independent project and is not intended to remain compatible with `speckit-roadmap`. Future upstream development may be reviewed for ideas, fixes, or other useful developments, but upstream changes are not expected to be merged directly.

The original project and its contributors retain authorship and copyright in their respective contributions. Subsequent modifications and original work in Diagram Roadmap are authored by this project's contributors.

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).

Diagram Roadmap contains work derived from `speckit-roadmap`, also licensed under Apache-2.0.
