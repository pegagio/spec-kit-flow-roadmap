# Quickstart: Validate Canonical mise Tooling

This guide records pre-implementation boundary evidence and validates the contributor workflow after implementation. Run every command from the repository root.

## Record the protected-surface baseline

Before changing any implementation surface, create `specs/007-adopt-mise-tooling/roadmap-reviews/protected-surface-baseline.md`. Record the exact protected paths, their current `git status --short --untracked-files=all` output, their `git diff --binary HEAD` output, and a sorted path-to-`git hash-object` manifest of every existing file, including ignored dogfood payload files. The protected paths are `specs/001-*` through `specs/006-*`, `CHANGELOG.md`, `commands/`, `scripts/`, `templates/`, `extension.yml`, `.extensionignore`, `.specify/extensions/diagram-roadmap/`, and `.agents/skills/speckit-diagram-roadmap-*/`.

This snapshot records pre-existing changes as baseline state rather than attributing them to this feature. Final validation compares the same paths and evidence forms with this snapshot; zero baseline-relative changes are allowed.

## Prerequisites

Use a macOS or Linux host with mise installed independently of this repository. Review `mise.toml` before trusting or installing its declarations.

## Prepare the project

Trust the reviewed project configuration, then install its declared tools as a separate setup step:

```text
mise trust mise.toml
mise settings get task.run_auto_install
mise install
```

The settings command must report `false`. The install graph installs pinned Python and `uv` before the `pipx:`-backed Specify CLI, so clean setup does not require an ambient `uv` or `pipx` executable. Do not combine setup with the test task. A setup failure must remain visible and must be resolved before validation.

## Validate missing-tool behavior safely

Perform the negative test in a disposable copy of the repository with temporary, initially empty `MISE_CONFIG_DIR`, `MISE_DATA_DIR`, `MISE_CACHE_DIR`, and `MISE_STATE_DIR` directories. Trust only the copied `mise.toml`, do not run `mise install`, and invoke `mise run test` from the disposable repository root.

The command must fail non-zero because the declared tools are absent. Confirm that the temporary mise directories contain no newly installed declared tool afterward. Remove only the disposable copy and temporary mise directories; do not alter or inspect the contributor's normal mise-managed tool state for this test.

## Validate the task contract

List and validate the project task inventory:

```text
mise tasks --local --extended
mise tasks validate --errors-only
```

The inventory must contain exactly one local project task, `test`, with a description that identifies the complete Python contract suite. Validation alone is insufficient evidence because an empty task inventory can still be structurally valid; compare the listing and auto-install setting with [the tooling contract](contracts/tooling-contract.md).

## Run the complete suite

Run the one canonical validation entrypoint:

```text
mise run test
```

Every discovered contract test must run. The task returns zero only when the suite passes and non-zero when configuration, discovery, or any test fails. Do not encode an expected test count; discovery is allowed to grow.

## Inspect the current-surface boundary

Confirm that current contributor surfaces use only the canonical workflow:

```text
rg -n 'just test|mise exec -- python -m unittest|TODO: configure' README.md tests/README.md mise.toml
test ! -e justfile
```

The textual scan must return no obsolete contributor workflow or placeholder, and the absence check must succeed. Run `tests/python/test_current_surface.py` as the executable configuration contract; do not include that test source in the textual scan because it necessarily names forbidden strings in negative assertions. Do not apply these scans to merged specs, dated reports, or released changelog history; those paths preserve accepted evidence.

## Confirm packaging remains unchanged

Run the complete suite's existing installation and dogfood checks through the canonical task. They must continue to prove the exact installed payload and source parity without adding `mise.toml`, contributor documentation, tests, specifications, or a task-runner file to the extension payload.

No extension reinstall or dogfood refresh is part of this feature because runtime source and packaging rules do not change.

## Complete the platform matrix

Run the same setup and validation workflow on both supported operating systems and record actual evidence:

| Platform | mise task validation | Complete suite | Tool versions | Result |
|---|---|---|---|---|
| macOS | PASS — mise 2026.8.2 listed exactly `test`; all 1 task validated | PASS — 80 discovered tests; forced failure and missing-tool runs returned non-zero; no implicit installs | Python 3.11.16; `uv` 0.12.5; Specify CLI 1.0.1 | PASS |
| Linux | PASS — mise 2026.9.1 listed exactly `test`; all 1 task validated | PASS — 80 discovered tests; forced failure and missing-tool runs returned non-zero; no implicit installs | Python 3.11.16; `uv` 0.12.5; Specify CLI 1.0.1 | PASS |

A macOS-only result does not satisfy Linux acceptance. Use a real Linux host or separately approved CI job; do not infer Linux success from TOML inspection.

## Final repository checks

```text
git diff --check
```

Review the final diff and confirm it changes only the intended current contributor surfaces plus this feature's mutable artifacts. Recreate the protected-path status, binary diff, and sorted path-to-object manifest using the same path set and procedure recorded in `specs/007-adopt-mise-tooling/roadmap-reviews/protected-surface-baseline.md`; all three must match the baseline exactly. The implementation must not rewrite merged feature directories, dated reports, released history, extension runtime files, packaging rules, generated skills, or the installed dogfood payload.
