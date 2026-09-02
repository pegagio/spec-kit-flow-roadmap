# Data Model: Adopt mise Tooling

This feature has no persistent application data. Its model describes the contributor-facing toolchain, task, documentation, and historical-boundary contracts.

## Development Tool Declaration

| Field | Type | Validation |
|---|---|---|
| Name | String | Unique within the project tool table |
| Version | Exact version string | Must be reviewable and reproducible; floating declarations are invalid |
| Purpose | Enum | `task-runtime`, `tool-installer`, or `contract-suite-dependency` |
| Current consumer | Non-empty reference set | Must name at least one current task, test, packaging operation, or contributor workflow |

The valid target state contains Python 3.11.16 as the task runtime, `uv` 0.12.5 as the installer for the `pipx:` backend, and Specify CLI 1.0.1 as a contract-suite dependency. The Specify declaration has explicit installation dependencies on Python and `uv`. A declaration with no current consumer is invalid and is removed rather than retained speculatively.

## Project Task

| Field | Type | Validation |
|---|---|---|
| Name | String | Exactly `test`; unique in the project task inventory |
| Description | Non-empty string | States that the task runs the complete Python contract suite |
| Invocation | Literal executable plus arguments | Runs standard-library unittest discovery for `tests/python/test_*.py`; contains no nested mise activation, setup, shell control flow, or placeholder output |
| Working directory | Enum | Repository root only |
| Environment | Reference | Uses the active project tool declarations |
| Auto-install | Boolean | False; task execution never installs a missing declaration |
| Success state | Exit code | Zero only when the complete discovered suite passes |
| Failure state | Exit code | Non-zero when task configuration, discovery, or any test fails |

## Current Documentation Surface

| Field | Type | Validation |
|---|---|---|
| Path | Repository-relative path | Maintained contributor documentation only |
| Setup sequence | Ordered actions | Review/trust configuration → install declared tools → run canonical test task |
| Canonical command | String | `mise run test` |
| Working-directory statement | String | Explicitly identifies the repository root |
| Disallowed alternatives | Set | No current `just test` or duplicate lower-level test workflow |

The README establishes first-use setup. Test documentation repeats or links to that setup while naming the same canonical task; it does not create a second supported validation path.

## Historical Artifact

| Field | Type | Validation |
|---|---|---|
| Path | Repository-relative path | Merged feature directory, dated generated report, or released changelog section |
| Recorded workflow | Historical text | May retain Just or direct-command references that were valid when accepted |
| Mutation policy | Enum | Semantically immutable for this feature |

Historical references are evidence, not current contributor instructions. Current-surface tests classify paths before evaluating task-runner language so ordinary prose and preserved history do not cause false failures.

## Contributor Environment State

```text
mise available
  -> configuration reviewed and trusted
  -> declared tools installed
  -> canonical task runnable from repository root
  -> complete suite passed or failed visibly
```

Trust and installation occur only through explicit contributor actions. A missing prerequisite terminates visibly and does not trigger task-owned fallback or setup.

## Relationships and Invariants

- The `test` task uses the Python declaration.
- The Specify CLI installation waits for the Python and `uv` declarations; clean setup does not depend on an ambient global installer.
- The discovered suite relies on the Specify CLI declaration for installation and runtime contract scenarios.
- Current documentation names the one canonical task and its ordered setup prerequisites.
- The task inventory contains no name without real behavior and no behavior without truthful exit semantics.
- The project task setting disables mise's default missing-tool auto-install behavior.
- Development tooling remains outside the extension runtime payload.
- Current surfaces may change; historical artifacts remain unchanged.
