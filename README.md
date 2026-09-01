# Diagram Roadmap

A [GitHub Spec Kit](https://github.com/github/spec-kit) extension that adds a **spec
roadmap** to the workflow: written after the constitution, and reviewed before and after
each spec is implemented.

```
constitution → ROADMAP → specify → plan → tasks → [brief] → implement → [debrief]
                 │                              read-only       read-only
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
| `speckit.diagram-roadmap.write` | after `/speckit.constitution` (hook) | Create or amend the roadmap. Pulls from the constitution, ADRs, PRDs, the current session, and prior notes; asks about gaps; writes a versioned roadmap with a changelog. Detects create vs. amend automatically. |
| `speckit.diagram-roadmap.brief` | before `/speckit.implement` (hook) | Read-only. Surfaces the roadmap's record for the spec you're about to build (outcome, scope, governing decisions, dependencies) and flags anything that has already drifted. |
| `speckit.diagram-roadmap.debrief` | after `/speckit.implement` (hook) | Read-only. Compares what you built against the roadmap entry; classifies any drift; proposes marking the entry `verified`. |
| `speckit.diagram-roadmap.sync` | on demand | Read-only. Reconciles the whole roadmap against the specs on disk: orphans, phantom entries, status drift, broken dependencies. |

`brief`, `debrief`, and `sync` are read-only — they write a report and *propose* changes.
Only `write` edits the roadmap, and it never deletes content (superseded entries are marked,
and every change is recorded in the roadmap's changelog).

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

- **Scripts vs. judgment.** The one shipped Python script resolves the active Specify runtime, configuration, paths, containment, and structured output. Everything that requires judgment—elicitation, drift detection, and review reasoning—lives in the command bodies and is checked through dogfood scenarios.
- **Supported platforms.** The same Python contract suite runs on macOS and Linux. The extension does not ship compatibility wrappers or alternate Windows, Bash, or PowerShell runtimes.
- **Self-hosted.** This extension was built with spec-kit and reviewed against its own
  roadmap. See `specs/` and `.specify/memory/roadmap.md`.

## Development

```text
just test
```

## Project Origins

Diagram Roadmap is an independent derivative of [speckit-roadmap](https://github.com/srobroek/speckit-roadmap), originally created and maintained by [srobroek](https://github.com/srobroek).

This project began from the `speckit-roadmap` codebase and preserves its original Git history so that the authorship and development history of the inherited work remain intact.

Diagram Roadmap is maintained as an independent project and is not intended to remain compatible with `speckit-roadmap`. Future upstream development may be reviewed for ideas, fixes, or other useful developments, but upstream changes are not expected to be merged directly.

The original project and its contributors retain authorship and copyright in their respective contributions. Subsequent modifications and original work in Diagram Roadmap are authored by this project's contributors.

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).

Diagram Roadmap contains work derived from `speckit-roadmap`, also licensed under Apache-2.0.
