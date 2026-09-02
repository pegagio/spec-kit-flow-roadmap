# Research: Adopt mise Tooling

## Canonical task representation

- **Decision**: Define one inline `[tasks.test]` entry in the root `mise.toml`, with a description and the existing complete-suite discovery command.
- **Rationale**: The preserved workflow is one direct executable invocation with no control flow, data transformation, or reusable script logic. An inline task keeps the public surface visible and matches the roadmap decision that `mise.toml` owns tool versions and task entrypoints.
- **Alternatives considered**: A file task under `.mise/tasks/` adds unnecessary indirection; retaining Just duplicates the canonical surface; a wrapper script creates another maintained automation artifact with no behavior to encapsulate.

## Task environment activation

- **Decision**: Run `python -m unittest discover -s tests/python -p 'test_*.py'` directly inside the mise task.
- **Rationale**: `mise run` activates the tools declared by the loaded project configuration before executing the task. Nesting `mise exec` inside a mise task is redundant and makes the execution boundary harder to reason about.
- **Alternatives considered**: Preserve `mise exec -- python ...` from the Just recipe; invoke a system Python; introduce a Python wrapper. All either duplicate environment activation, weaken the pinned-runtime contract, or add an unnecessary artifact.

## First-use setup and trust

- **Decision**: Document three separate actions from the repository root: review and explicitly trust `mise.toml`, run `mise install`, then run `mise run test`. Set `settings.task.run_auto_install = false`; the test task performs no setup.
- **Rationale**: Trust and installation are visible contributor decisions with different side effects from validation. Installed mise 2026.8.2 defaults task auto-install to true, so omitting install commands from the task body is insufficient: without the project setting, `mise run test` may install missing tools. Disabling auto-install makes precondition failures visible and makes the accepted setup sequence enforceable. The setting also makes the configuration trust-sensitive, so explicit review and trust are operationally meaningful.
- **Alternatives considered**: Assume an already configured environment; rely on mise's default auto-install; put installation or trust inside the test task. The first leaves onboarding incomplete, while the latter two hide mutations inside validation and repeat or bypass the explicit setup contract.

## Supported working directory

- **Decision**: Support and document `mise run test` from the repository root only; do not add directory normalization.
- **Rationale**: This is the clarified acceptance boundary and matches current test documentation. Root-only invocation avoids additional task configuration and nested-directory acceptance cases that provide no required user value.
- **Alternatives considered**: Support every nested directory; support arbitrary directories through an explicit repository path. Both broaden the interface and test matrix without advancing the canonical-workflow outcome.

## Tool declaration inventory

- **Decision**: Pin `python = "3.11.16"` and `uv = "0.12.5"`; declare `pipx:specify-cli` at 1.0.1 with installation dependencies on both tools; remove `jq = "latest"`.
- **Rationale**: Python executes the canonical task. The contract suite invokes Specify and validates its active interpreter. Mise's `pipx:` backend requires `uv` or `pipx`; declaring pinned `uv` and an explicit dependency edge makes clean installation portable and prevents the successful macOS path from depending on an undeclared global installer. Repository-wide current-surface searches find no maintained jq use outside `mise.toml`, and an unpinned unused declaration violates the requirement that every retained tool have a current project purpose.
- **Alternatives considered**: Require contributors to install `uv` or `pipx` globally; retain jq for possible personal use; pin jq without a repository use; remove Specify because it is not in the direct task command. An ambient installer would make the declared setup incomplete, personal or hypothetical use is not a project contract, and the suite's installation/runtime tests require Specify.

## Task inventory and removed recipes

- **Decision**: Expose exactly one task named `test`. Remove the Just `default` and `lint` recipes and the `build`, `dev`, and `clean` placeholders without mise equivalents.
- **Rationale**: `test` is the only recipe that performs a valid project workflow. The default recipe only lists Just tasks, lint depends on a repository-absent pre-commit configuration, and the remaining recipes report false success without doing work.
- **Alternatives considered**: Translate every recipe for command-name continuity; retain empty names as future placeholders. Both would make the canonical inventory misleading.

## Contract validation strategy

- **Decision**: Extend `tests/python/test_current_surface.py` to parse `mise.toml` with `tomllib`, assert the exact tool, task, and `run_auto_install = false` settings contract, assert the task command and absence of `justfile`, and validate current documentation separately from accepted historical artifacts. Validate task syntax with `mise tasks validate --errors-only` and inspect the actual local task inventory in end-to-end validation.
- **Rationale**: Task validation can succeed when zero tasks exist, so syntax validation alone cannot prove the required interface. Exact deterministic assertions prevent Just, unused tools, duplicate lower-level workflows, placeholder tasks, or an empty mise task surface from returning unnoticed.
- **Alternatives considered**: Rely only on `mise tasks validate`; recursively run `mise run test` from inside the suite; scan every repository file for the word `just`. The first misses an empty inventory, the second recurses, and the third confuses normal prose and historical evidence with current task-runner references.

## Current versus historical boundary

- **Decision**: Change only `mise.toml`, `README.md`, `tests/README.md`, `tests/python/test_current_surface.py`, and deletion of `justfile`. Do not edit merged specs 001–006, dated reports, released changelog history, constitution, runtime source, packaging rules, generated skills, or the installed dogfood payload.
- **Rationale**: The constitution requires later behavior to flow forward and freezes merged feature meaning. Development task files are excluded from the installed payload, so no extension refresh or runtime parity work is necessary.
- **Alternatives considered**: Replace historical `just test` references repository-wide; refresh the dogfood extension; update runtime packaging. Each would create unrelated churn or falsify accepted history without changing the contributor workflow.

## Cross-platform acceptance

- **Decision**: Run the same root-level setup and canonical task workflow on macOS and Linux and record actual results for both platforms.
- **Rationale**: These are the project's complete supported development platforms. A macOS result does not establish Linux behavior, and test counts must be observed rather than fixed because discovery can grow.
- **Alternatives considered**: Infer Linux behavior from TOML and macOS results; require Windows validation. Inference is insufficient evidence, while Windows is outside the governing platform contract.
