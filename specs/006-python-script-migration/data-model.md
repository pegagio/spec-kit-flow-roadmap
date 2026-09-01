# Data Model: Python Script Migration

This feature has no database model. Its data model is the deterministic runtime state that turns reviewed extension configuration into bounded command input.

## Runtime Context

The runtime context establishes which interpreter and payload are trusted before configuration parsing begins.

| Field | Type | Validation |
|---|---|---|
| Initial interpreter | Absolute path | Informational only; it is not trusted to supply dependencies |
| Active Specify executable | Absolute path | Resolved from `PATH`; must be a supported regular POSIX console-script entrypoint |
| Active Specify interpreter | Absolute invocation path plus canonical identity | Parsed from the console-script shebang; must exist and be executable. The original path is retained for virtual-environment execution, the canonical binary must equal the eventual `sys.executable` after resolution, and the eventual `sys.prefix` must identify the shebang's virtual environment when applicable |
| Required Python version | Version tuple | Exactly `3.11.16`, matching the repository pin |
| Required PyYAML version | Version tuple | At least `6.0`, supplied by the isolated active Specify runtime |
| Isolation state | Boolean | PyYAML and configuration parsing run only after isolated re-execution under the active Specify interpreter |
| Script layout | Enum | `source` or `installed`; any other resolved script location is invalid |
| Project root | Canonical path | Derived from script location, never the caller's working directory |
| Payload root | Canonical path | Repository root for source mode or installed extension directory for installed mode |

## Configuration Sources

Each resolved leaf selects the first valid non-empty value from the same ordered source chain.

| Priority | Source | Fields |
|---:|---|---|
| 1 | Environment | `SPECKIT_DIAGRAM_ROADMAP_PATH`, `SPECKIT_DIAGRAM_ROADMAP_ADR_DIR`, `SPECKIT_DIAGRAM_ROADMAP_PRD_GLOBS`, `SPECKIT_DIAGRAM_ROADMAP_MAX_FINDINGS` |
| 2 | Installed `roadmap-config.yml` | `roadmap.path`, `adr.dir`, `prd.globs`, `report.max_findings` |
| 3 | Payload `extension.yml` defaults | Currently `report.max_findings` |
| 4 | Built-ins | Roadmap path, ADR directory, five ordered PRD patterns, and findings limit 50 |

Null and empty scalar values fall through. Lists replace lower-precedence lists rather than merging; an explicit empty list is a valid configured PRD pattern set.

## Configuration Document

The project configuration is a strict optional mapping with four optional sections.

| Section | Leaf | Type | Validation |
|---|---|---|---|
| `roadmap` | `path` | String or null | Empty/null falls through; configured value must be a bounded project-relative file path |
| `adr` | `dir` | String or null | Empty/null falls through; configured value must be a bounded project-relative directory path |
| `prd` | `globs` | Ordered list of strings or null | Every configured item is non-empty and project-bounded; `[]` is valid |
| `report` | `max_findings` | Integer or null | `type(value) is int` and value is at least zero; booleans are invalid |

Unknown top-level and nested keys, duplicate keys, aliases, merge keys, unsafe tags, multiple documents, wrong types, malformed input, and oversized input are invalid states.

## Project-Bounded Path

A project-bounded path carries both the supplied lexical value and its canonical target.

| Field | Type | Validation |
|---|---|---|
| Supplied value | String | Non-empty; no NUL, home expansion, absolute/rooted form, Windows drive or UNC form, or `..` component |
| Canonical target | Path | Joined to the canonical project root and resolved through existing symlink ancestors |
| Relative output | POSIX string | Canonical target expressed relative to the project root |
| Kind | Enum | `roadmap-read`, `roadmap-write`, `adr`, or `prd` |
| Exists | Boolean | Roadmap-read and PRD require a regular file; ADR requires a directory; roadmap-write may be absent but requires a contained existing parent chain and rejects an existing non-regular target |

PRD patterns are bounded descriptions, not scanned matches. Their literal prefix is checked by the loader. Every later concrete roadmap, ADR, or PRD target becomes a new Project-Bounded Path immediately before each content access.

## Resolved Configuration

The successful default-mode output contains exactly six fields.

| Field | Type | Invariant |
|---|---|---|
| `roadmap_path` | Non-empty string | Canonical project-relative POSIX path |
| `roadmap_exists` | Boolean | True only for a regular file at the canonical roadmap target |
| `adr_dir` | Non-empty string | Canonical project-relative POSIX path |
| `adr_present` | Boolean | True only for a directory at the canonical ADR target |
| `prd_globs` | Ordered list of non-empty strings | Validated bounded patterns; filesystem is not scanned |
| `max_findings` | Non-negative integer | Zero is valid |

## Runtime Payload

The installed payload is the reviewed set of 11 runtime files.

| Category | Count | Contents |
|---|---:|---|
| Manifest and configuration | 2 | `extension.yml`, `config-template.yml` |
| License | 1 | `LICENSE` |
| Commands | 4 | Write, brief, debrief, and sync Markdown definitions |
| Script | 1 | `scripts/python/load_config.py` |
| Templates | 2 | Roadmap and review-report templates |
| Project configuration | 1 | Installer-created `roadmap-config.yml` |

Repository metadata, tests, specifications, task-runner files, and Bash or PowerShell artifacts are invalid payload members.

## State Transitions

The loader follows one fail-closed transition sequence.

```text
unverified initial process
  -> resolve active Specify console script
  -> re-execute under its interpreter with isolation when needed
  -> verify Python 3.11.16 and PyYAML 6.0 or newer
  -> derive source or installed roots
  -> parse and validate fixed configuration inputs
  -> resolve each leaf by precedence
  -> validate containment and existence
  -> emit one complete result
```

Command consumers repeat the kind-specific containment transition immediately before every content read or write. Any invalid transition terminates with exit 1, empty stdout, and one sanitized diagnostic line on stderr.
