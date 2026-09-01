# Quickstart: Validate the Python Migration

This quickstart describes the implementation validation workflow. It uses direct executable commands only; any multi-step orchestration belongs in the Python test suite or task runner implementation.

## Prerequisites

Use a macOS or Linux host with the repository toolchain installed through mise. The active Specify installation must be version 1.0.1, use Python 3.11.16, and provide PyYAML 6.0 or newer. The repository pin and extension runtime must report the same exact Python version.

Confirm the selected tools:

```text
mise current
specify version
```

The project Python is allowed to lack PyYAML. The loader must transfer to the verified Specify interpreter before importing that dependency.

## Run the Python contract suite

After implementation, run the maintained validation entrypoint:

```text
just test
```

The direct underlying test command is:

```text
mise exec -- python -m unittest discover -s tests/python -p 'test_*.py'
```

The suite must cover defaults, all precedence sources, null and empty fallthrough, explicit empty globs, strict YAML failures, exact types, Unicode and special characters, working-directory independence, runtime transfer and isolation, missing and below-6.0 PyYAML, project containment, stable output, and empty stdout on every failure.

## Inspect the default contract

Run the source loader directly from any working directory:

```text
mise exec -- python scripts/python/load_config.py
```

Even when mise's Python does not provide PyYAML, the entrypoint must re-execute under the active Specify interpreter and return one six-field JSON object. The default result has this shape:

```json
{"roadmap_path":".specify/memory/roadmap.md","roadmap_exists":true,"adr_dir":"docs/adr","adr_present":false,"prd_globs":["**/prd*.md","**/PRD*.md","**/prd-intake.yaml","**/product-spec.md","docs/product/**/*.md"],"max_findings":50}
```

Actual existence booleans reflect the project filesystem.

## Validate every concrete content path

Command consumers revalidate every roadmap, ADR, and matched PRD path immediately before each content access. Use `roadmap-read` for an existing roadmap, `roadmap-write` before creation or amendment, `adr` for an ADR directory, and `prd` for a matched PRD:

```text
mise exec -- python scripts/python/load_config.py --validate-path prd README.md
mise exec -- python scripts/python/load_config.py --validate-path roadmap-write .specify/memory/roadmap.md
```

The successful result is one canonical project-relative path:

```json
{"path":"README.md"}
```

Absolute paths, traversal, symlink escapes, and wrong-kind targets must fail with exit 1, empty stdout, and one diagnostic line on stderr. `roadmap-read` and `prd` require regular files, `adr` requires a directory, and `roadmap-write` permits a nonexistent contained target only when its existing parent chain remains contained and an existing target is a regular file.

## Validate a disposable installation

Create a temporary Spec Kit project and a distinct copy of the reviewed extension source. From the temporary project, install and enable that source copy:

```text
specify extension add --dev --force <source-copy>
specify extension enable diagram-roadmap
```

Do not use the repository's own installed destination as the `--dev` source. Preserve any project-owned `roadmap-config.yml` across a forced dogfood refresh.

Validate the installed loader and command registration:

```text
mise exec -- python .specify/extensions/diagram-roadmap/scripts/python/load_config.py
specify extension list
```

The enabled installation must contain exactly 11 reviewed runtime files. Every source-owned installed file must match its source counterpart byte-for-byte. Validate a disposable project's newly scaffolded `roadmap-config.yml` against `config-template.yml`; preserve and semantically validate an existing dogfood project's `roadmap-config.yml` rather than including it in source-byte-parity comparison. All four generated Diagram Roadmap skills must reference `scripts/python/load_config.py`; brief and debrief must reference `.specify/scripts/python/check_prerequisites.py`; the three hooks must remain registered.

## Dogfood all four command behaviors

Exercise these bounded scenarios with the refreshed generated skills and verify their established outcomes:

1. **Write — create**: In a disposable project with a constitution and no roadmap, run `speckit.diagram-roadmap.write`; verify it creates a versioned roadmap without fabricating missing context and records genuine gaps explicitly.
2. **Write — amend**: Run `speckit.diagram-roadmap.write` against an existing roadmap with one accepted change; verify existing content is preserved, the change is recorded in the Sync Impact Report, and the version changes according to the documented rules.
3. **Brief**: Run `speckit.diagram-roadmap.brief` for a spec with a matched roadmap entry; verify the report surfaces the entry's outcome, scope, dependencies, governing decisions, and pre-implementation drift without modifying the roadmap or spec.
4. **Debrief**: Run `speckit.diagram-roadmap.debrief` against a bounded implementation; verify it classifies outcome, scope, constraint, or roadmap drift and proposes status without applying the proposal or modifying implementation files.
5. **Sync**: Run `speckit.diagram-roadmap.sync` against a ledger with a known bounded divergence; verify it reports the divergence and proposed correction without modifying the roadmap or spec directories.

The dogfood evidence must record which scenario ran, its generated report or roadmap path, the expected outcome, the observed outcome, and whether the non-destructive/read-only invariant held.

## Validate current-reference boundaries

The Python suite must scan current extension source, current documentation, the installed payload, and regenerated skills for unsupported shell artifacts. Scope exclusions must preserve merged specs 001–005, dated reports, released changelog entries, superseded roadmap history, and Spec Kit-owned `.specify/scripts/bash/` files.

The current surfaces must contain no extension-owned Bash or PowerShell scripts, `sh` or `ps` command frontmatter, shell scripting logic, Bats, Pester, or cross-language parity machinery. Direct single-executable examples remain valid.

## Complete the platform matrix

Run the same documented validation workflow on both macOS and Linux. Record operating system, Specify version, Specify interpreter path and Python version, PyYAML version, test result, disposable payload result, generated-skill result, and hook result. A macOS-only run does not satisfy the Linux acceptance criteria; use a real Linux host, container, or separately approved CI job.
