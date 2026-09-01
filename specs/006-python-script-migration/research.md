# Research: Python Script Migration

This research resolves the runtime, configuration, containment, packaging, and validation decisions needed to migrate the extension to one Python implementation on macOS and Linux.

## Specify integration and runtime identity

**Decision**: Require Specify CLI 1.0.1 exactly in the extension manifest, use `scripts.py` frontmatter for all four commands, and provide a self-contained `scripts/python/load_config.py`. The entrypoint first uses only the Python standard library to resolve the active `specify` executable, accept only a verifiable POSIX console-script entrypoint with an absolute interpreter, and re-execute itself once through that exact shebang path in isolated mode. It verifies both the canonical interpreter binary and, when the shebang belongs to a virtual environment, the active environment prefix. It then requires Python 3.11.16 exactly and PyYAML 6.0 or newer. Missing executables, unsupported wrappers, unresolvable interpreters, loops, version or environment mismatches, missing PyYAML, or an older PyYAML version fail with no configuration output.

**Rationale**: Specify CLI 1.0.1 is the only Specify version covered by this feature's integration and cross-platform validation, so advertising a broader range would create an unverified compatibility promise. Version 1.0.1 supports `py:` command frontmatter, but its generated command resolver prefers a project `.venv`, then `python3` or `python` on `PATH`, before `sys.executable`. In this repository the selected project Python is 3.11.16 but lacks PyYAML, while Specify's Python 3.11.16 virtual environment supplies PyYAML 6.0.3. The virtual-environment interpreter is a symlink to a shared Python binary, so executing only its canonical target would lose the environment and its dependencies. The bootstrap therefore verifies canonical identity but executes the original absolute shebang path and verifies `sys.prefix`. `py:` alone does not satisfy the accepted runtime and dependency contract. A bounded bootstrap makes the active Specify installation authoritative without accepting an arbitrary fallback. Isolated mode prevents project-local modules, `PYTHONPATH`, and user-site packages from shadowing the reviewed dependency.

**Alternatives considered**: Trusting Specify's initial `py:` selection was rejected because it can use the wrong environment. Installing PyYAML into the project interpreter was rejected because the active Specify runtime is the accepted dependency owner. Vendoring or writing a YAML parser was rejected by FR-024. Reading arbitrary wrappers or searching multiple Python installations was rejected as brittle and unsafe. The preferred long-term alternative is an upstream Specify runner that invokes extension scripts directly with its own `sys.executable -I`; no released 1.0.1 capability provides that contract.

## Configuration parsing and resolution

**Decision**: Parse `roadmap-config.yml` and `extension.yml` with a local `yaml.SafeLoader` subclass after runtime verification. Reject duplicate keys, aliases, merge keys, unsafe tags, multiple documents, oversized inputs, malformed YAML, wrong types, and unknown documented-configuration keys. Resolve each leaf independently in this order: non-empty environment override, non-empty or non-null installed configuration value, installed manifest default, then built-in default. Lists replace rather than merge; an explicit empty PRD glob list is valid.

**Rationale**: Safe structured parsing preserves the existing precedence and special-character behavior while eliminating line-oriented ambiguity. Manual schema validation is required because PyYAML does not enforce the documented key and type model. Per-leaf resolution preserves null fallthrough and independent overrides.

**Alternatives considered**: `safe_load` without duplicate or schema checks was rejected because it silently accepts misspellings and last-wins duplicates. Line parsing was rejected because it cannot implement YAML correctly. JSON-only configuration was rejected because it would change the public configuration format.

## Project discovery and trusted inputs

**Decision**: Derive the active project and payload roots only from the canonical resolved script location, recognizing the repository source layout and `.specify/extensions/diagram-roadmap/` installed layout. Read only the fixed project configuration and payload manifest paths, require both to be bounded regular files rather than symlinks, and never use the caller's working directory or import project code.

**Rationale**: Script-location discovery makes behavior independent of the working directory and removes the current Bash loader's dependency on project-controlled `.specify/scripts/bash/common.sh`. Fixed, bounded reads keep configuration loading inside the reviewed extension trust boundary.

**Alternatives considered**: Falling back to `PWD` was rejected because an alien working directory can bind the loader to another project. Reusing project Spec Kit helpers was rejected because project-controlled code would execute before configuration is validated.

## Path and glob containment

**Decision**: Reject empty, NUL-containing, home-expanded, POSIX absolute, Windows drive or UNC, and `..`-bearing roadmap paths, ADR paths, and PRD patterns. Resolve roadmap and ADR candidates against the canonical project root with existing symlink ancestors resolved, require containment, and emit canonical project-relative POSIX paths. For globs, validate the literal prefix without scanning and preserve ordered patterns. Command bodies must canonically revalidate every concrete roadmap, ADR, and PRD path immediately before each content access. Roadmap reads require a regular file; roadmap writes may target a nonexistent contained path only when its existing parent chain remains contained and any existing target is a regular file.

**Rationale**: Lexical checks alone do not stop symlink escapes, while canonical containment alone would accept absolute in-project input that the user explicitly rejected. Initial resolution cannot protect against a path or symlink that changes before later access, so consumers must revalidate immediately before reading or writing. PRD patterns remain a two-stage contract: the loader validates the pattern and literal prefix; the consumer validates every eventual match.

**Alternatives considered**: Resolving only lexical paths was rejected because existing symlink ancestors can escape. Scanning globs in the loader was rejected by FR-010 and the determinism split. Accepting absolute paths that happen to resolve inside the root was rejected by clarification.

## Output and error contract

**Decision**: Default mode emits exactly one compact UTF-8 JSON object plus newline containing the six existing fields. A separate `--validate-path` mode validates one concrete project-relative candidate as `roadmap-read`, `roadmap-write`, `adr`, or `prd` and returns a canonical relative path. Every expected failure exits 1, writes no stdout, and emits one sanitized single-line diagnostic without traceback or source content.

**Rationale**: The default contract remains backward-compatible for command bodies, while the validation mode closes the wildcard-match containment gap without adding another installed script. Building the complete result before writing prevents valid-looking partial output.

**Alternatives considered**: Adding error JSON was rejected because the accepted contract separates configuration output from diagnostics. Having each command improvise containment was rejected because deterministic mechanics belong in the shared script. Returning matched PRD files was rejected because the loader must not scan.

## Tests and platform evidence

**Decision**: Replace Bats, Pester, and cross-language parity suites with Python `unittest` contract tests and fixtures. Exercise parsing, precedence, runtime transfer, isolation, output, errors, project discovery, containment, installed parity, generated skills, hooks, and command prerequisite paths on both macOS and Linux. Local macOS evidence cannot by itself close Linux success criteria.

**Rationale**: `unittest` adds no project dependency and runs under the same supported runtime. The migration is complete only when identical behavior is demonstrated on both supported operating systems, including installations where project Python lacks PyYAML.

**Alternatives considered**: Retaining Bats or Pester for migration checks was rejected because they would remain maintained shell dependencies. Treating Darwin results as a proxy for Linux was rejected because the constitution explicitly requires both platforms.

## Packaging and historical boundary

**Decision**: Ship one Python script and an exact 11-file runtime payload. Refresh the ignored dogfood installation from a distinct source copy after preserving its project configuration, then regenerate all four command skills. Compare every source-owned installed file byte-for-byte with its source counterpart; validate a disposable configuration scaffold against the current template separately; and validate the preserved dogfood `roadmap-config.yml` semantically rather than including it in byte parity. Update current README, test guidance, task runner, template comments, manifest, allowlist, and Unreleased changelog while preserving released changelog entries, merged specs 001–005, dated reports, and superseded roadmap history.

**Rationale**: The allowlist is the reviewed distribution boundary. A distinct source copy prevents `--dev --force` from confusing source and destination, and generated skills must be refreshed because they embed command metadata. Historical references describe accepted earlier behavior rather than current support.

**Alternatives considered**: Editing the ignored installed snapshot by hand was rejected because it would bypass installer behavior. Blind repository-wide replacement was rejected because it would falsify merged history. Deleting Specify-owned `.specify/scripts/bash/` was rejected because those files belong to the host project rather than this extension.

## Core prerequisite migration

**Decision**: Brief and debrief replace their current core Bash prerequisite reference with the existing Spec Kit Python prerequisite script. Write and sync retain their existing judgment logic and use only the shared Python configuration contract.

**Rationale**: Removing the extension's own shell files is insufficient if current command instructions still require a core Bash path. The Python counterpart already exists in the supported Spec Kit installation and preserves the deterministic feature-resolution boundary.

**Alternatives considered**: Reimplementing core feature discovery in the extension was rejected as duplication and a canonical-conformance risk. Leaving the Bash reference was rejected because the command would still require Bash at runtime.
