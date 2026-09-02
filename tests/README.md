# Tests

This directory contains the standard-library `unittest` suite for the deterministic Python configuration loader, command contracts, disposable installation, and repository dogfood installation. The suite covers runtime transfer, strict YAML, configuration precedence, containment, stable output, packaging, and current-reference boundaries on macOS and Linux. Judgment-bearing command behavior is validated through the dogfood scenarios in `specs/006-python-script-migration/quickstart.md` rather than unit tests.

From the repository root, review `mise.toml`, trust the reviewed configuration, install its declared tools, and then run the canonical complete suite:

```text
mise trust mise.toml
mise install
mise run test
```

The test task does not perform trust or installation. Shared YAML fixtures live under `tests/fixtures/`. The complete `tests/` tree is development-only and is excluded from installed extension payloads.
