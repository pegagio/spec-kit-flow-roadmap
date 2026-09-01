# Tests

This directory contains the standard-library `unittest` suite for the deterministic Python configuration loader, command contracts, disposable installation, and repository dogfood installation. The suite covers runtime transfer, strict YAML, configuration precedence, containment, stable output, packaging, and current-reference boundaries on macOS and Linux. Judgment-bearing command behavior is validated through the dogfood scenarios in `specs/006-python-script-migration/quickstart.md` rather than unit tests.

Run the complete suite from the repository root:

```text
just test
```

The direct command is `mise exec -- python -m unittest discover -s tests/python -p 'test_*.py'`. Shared YAML fixtures live under `tests/fixtures/`. The complete `tests/` tree is development-only and is excluded from installed extension payloads.
