# Contributor Tooling Contract

This contract defines the public development workflow for contributors to Diagram Roadmap. It does not change the installed extension interface or runtime payload.

## Preconditions

- The host is macOS or Linux.
- The contributor has installed mise independently of this repository.
- Commands are run from the repository root.

## First-Use Setup

The supported setup sequence is ordered and explicit:

```text
review mise.toml
mise trust mise.toml
mise install
mise run test
```

Review and trust are contributor decisions. Installation may change the contributor's mise-managed tool state. The test task MUST NOT perform either action.

The canonical configuration sets:

```toml
[settings.task]
run_auto_install = false
```

This setting is part of the public failure contract. A missing tool causes validation to fail visibly instead of being installed implicitly.

## Tool Declarations

| Tool | Version | Required purpose |
|---|---|---|
| Python | 3.11.16 | Executes the complete contract suite |
| `uv` | 0.12.5 | Provides the pinned installer required by mise's `pipx:` backend |
| Specify CLI | 1.0.1 | Supports installation, command, and active-runtime contract cases within the suite |

The Specify CLI declaration depends on both Python and `uv`, so a clean `mise install` completes the prerequisite tools before installing the CLI. The canonical configuration contains no declaration without a current project consumer. In particular, jq is not part of this contract.

## Task Inventory

The complete public task inventory is exactly:

| Task | Description | Behavior |
|---|---|---|
| `test` | Run the complete Python contract suite | Discover every `test_*.py` module under `tests/python/`, run it through the declared Python environment, and propagate the suite's exit status |

The task body is the single direct invocation:

```text
python -m unittest discover -s tests/python -p 'test_*.py'
```

It contains no nested `mise exec`, trust, installation, control flow, pipeline, redirection, data transformation, or compatibility fallback. Project task auto-install is disabled independently of the task body.

## Failure Contract

- Missing or untrusted project configuration remains visible to the contributor.
- Missing declared tools remains visible and directs the contributor to the setup sequence.
- Invalid task configuration returns non-zero.
- Test discovery or test failure returns non-zero.
- The task MUST NOT report success after skipping setup, discovery, or a failed test.

## Current-Surface Contract

The maintained current surfaces are `mise.toml`, the README development instructions, `tests/README.md`, and current-surface contract tests. Together they MUST:

- identify mise as the sole task runner;
- use `mise run test` as the single canonical complete-suite entrypoint;
- state or demonstrate repository-root invocation;
- keep setup separate from validation;
- contain no current `just test`, duplicate lower-level workflow, placeholder task, or unconfigured lint task;
- assert the exact tool, task, and auto-install settings contract rather than relying only on permissive task validation.

## Historical and Packaging Boundary

Merged specs, dated reports, and released changelog history may retain prior Just commands. They are not current surfaces and MUST NOT be rewritten by this feature.

The root task configuration, contributor documentation, tests, and specifications remain development-only. The extension manifest, source runtime, `.extensionignore`, installed dogfood payload, and generated command skills are unchanged.
