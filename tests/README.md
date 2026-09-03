# Tests

This directory contains the standard-library `unittest` suite for the deterministic Python configuration and review helpers, command contracts, protected history, disposable installation, and repository dogfood installation. The suite covers runtime transfer, strict YAML, containment, target resolution, Git deltas, findings, lifecycle gates, report allocation, packaging, and current-reference boundaries on macOS and Linux. Judgment-bearing behavior is validated through `specs/008-command-contract-hardening/quickstart.md`.

From the repository root, review `mise.toml`, trust the reviewed configuration, install its declared tools, and then run the canonical complete suite:

```text
mise trust mise.toml
mise install
mise run test
```

The test task does not perform trust or installation. Shared YAML and command-selection fixtures live under `tests/fixtures/`. The complete `tests/` tree is development-only and is excluded from installed extension payloads.

After automated checks, run the quickstart's disposable scenarios for adversarial write evidence, explicit and ambiguous targets, implementation ranges and working-tree deltas, lifecycle states, overflow, collisions, and source-preserving report behavior. Exercise every maintained positive and adjacent-negative selection prompt through a host agent.

Before acceptance, exercise this repository's installed extension and its `after_constitution`, `before_implement`, and `after_implement` hooks in an isolated clone or worktree of this repository. Run the complete automated and judgment-focused acceptance set on both macOS and Linux, tie evidence to the exact revision, compare protected historical surfaces, and record intended-user disposition separately from automated success.
