# Loader Contract

This contract defines the deterministic interface shared by all four Diagram Roadmap commands. It supersedes the active Bash and PowerShell loader contract without rewriting the historical feature-001 schema.

## Command integration

Each command declares exactly one script entry:

```yaml
scripts:
  py: .specify/extensions/diagram-roadmap/scripts/python/load_config.py
```

`{SCRIPT}` invokes the Python entrypoint in default mode. Command instructions must not describe it as platform-specific and must not retain `sh` or `ps` alternatives.

Brief and debrief invoke the Spec Kit-owned Python prerequisite script at `.specify/scripts/python/check_prerequisites.py --json --paths-only`. They do not reference the core Bash counterpart. Every command must invoke the loader's kind-specific path validation immediately before each roadmap, ADR, or PRD content read or write.

## Runtime bootstrap

Before importing PyYAML or project-adjacent modules, `load_config.py` performs these standard-library-only checks:

1. Resolve the `specify` executable selected by normal `PATH` command resolution and resolve any executable symlink.
2. Require a regular POSIX console-script file whose first line contains one absolute interpreter path and no wrapper arguments. `/usr/bin/env`, shell wrappers, binaries, relative interpreters, and ambiguous shebangs are unsupported and fail closed.
3. Resolve the interpreter canonically and require an executable regular file, while retaining the original absolute shebang path. If that path belongs to a virtual environment, record its environment prefix.
4. If the canonical interpreter differs from the current `sys.executable`, the virtual-environment prefix differs from `sys.prefix`, or the process is not isolated, replace the process once with `[original-shebang-interpreter, "-I", script, *arguments]`. Executing the original path preserves the active Specify virtual environment even when its interpreter is a symlink to a shared Python binary. No alternative Python search or fallback is permitted.
5. In the resulting process, repeat resolution, require canonical interpreter and environment identity, and require `sys.version_info[:3] == (3, 11, 16)` before importing `yaml`.
6. Import PyYAML from the isolated Specify environment and require version 6.0 or newer. Project-local modules, `PYTHONPATH`, and user-site packages must not influence the import.

Failure at any step follows the error contract. A future Specify release that exposes a direct `sys.executable -I` extension-script runner should replace this bootstrap after a separately accepted contract change.

## Default mode

Invocation without mode arguments resolves configuration:

```text
python load_config.py
```

On success it exits 0 and writes exactly one compact UTF-8 JSON object plus newline. The object validates against [load-config.schema.json](load-config.schema.json), has exactly six fields, and is built completely before stdout is written.

Configuration leaves resolve independently in this precedence order:

1. Non-empty `SPECKIT_DIAGRAM_ROADMAP_*` environment override
2. Non-empty or non-null leaf in the project's installed `roadmap-config.yml`
3. Non-empty or non-null leaf under the payload manifest's `defaults`
4. Built-in default

Environment PRD globs are one strict CSV record. Quoting may preserve commas and special characters; empty members, additional records, and malformed CSV are invalid. An explicit YAML `[]` remains a valid value and replaces lower-precedence lists.

## Configuration input

The project configuration validates against [roadmap-config.schema.json](roadmap-config.schema.json). The loader applies these additional YAML rules before schema validation:

- The UTF-8 file is at most 65,536 bytes.
- Only one YAML document is accepted.
- Duplicate keys, aliases, merge keys, unsafe tags, unknown keys, and coercion are rejected.
- An empty or comments-only document is treated as absent configuration.
- `type(max_findings) is int`; booleans are not integers for this contract.

The manifest is separately parsed as extension metadata. Only `defaults` participates in configuration resolution. Duplicate keys are rejected throughout the manifest, and unknown sections or leaves beneath `defaults` are rejected; recognized manifest domains outside `defaults` are not project configuration keys.

## Root discovery and fixed reads

The loader resolves `__file__` strictly and accepts only these layouts:

```text
<project>/scripts/python/load_config.py
<project>/.specify/extensions/diagram-roadmap/scripts/python/load_config.py
```

The first layout derives both project and payload root as `<project>`. The second derives project root as `<project>` and payload root as `<project>/.specify/extensions/diagram-roadmap`. Any other layout fails.

Only these fixed YAML files may be read:

```text
<project>/.specify/extensions/diagram-roadmap/roadmap-config.yml
<payload-root>/extension.yml
```

Each existing input must be opened without following the final symlink and verified as a non-symlink regular file within its expected root before parsing. A symlink is rejected even when it resolves inside the project. Directories, FIFOs, devices, sockets, and other non-regular inputs are rejected. The loader never falls back to the current working directory, invokes a subprocess or shell, scans PRDs, accesses the network, or imports code from the project.

## Containment validation

Roadmap paths, ADR paths, PRD patterns, and concrete PRD matches reject NUL, `~` expansion, POSIX absolute forms, Windows drive or UNC forms, and any literal `..` component. No environment-variable or shell expansion occurs.

Roadmap and ADR values are joined to the canonical project root, resolved with existing symlink ancestors, and required to remain at or below that root. Successful values are emitted as canonical project-relative POSIX paths. Existence flags are computed only after containment. Initial configuration resolution does not replace access-time validation.

PRD patterns remain ordered patterns and are not expanded. The loader canonically validates the literal prefix before the first glob metacharacter. Every command that expands a PRD pattern must anchor matching at the project root. Every concrete roadmap, ADR, or PRD candidate must be passed through the appropriate validation kind immediately before each content access.

## Concrete-path validation mode

Command consumers validate one eventual path with:

```text
python load_config.py --validate-path <roadmap-read|roadmap-write|adr|prd> <project-relative-path>
```

The mode uses the same project discovery and containment rules. On success it exits 0 and emits exactly `{"path":"<canonical-project-relative-posix-path>"}` plus newline. `roadmap-read` and `prd` require a regular file. `adr` requires a directory. `roadmap-write` permits a nonexistent contained target only when its existing parent chain remains within the project; if the target exists, it must be a regular file. The mode does not create, modify, or delete the candidate.

## Error behavior

Every expected runtime, parse, validation, or filesystem failure:

- exits 1;
- writes no stdout;
- writes exactly one single-line UTF-8 diagnostic plus newline to stderr;
- starts with `Error:` and names the relevant field or runtime condition;
- JSON-escapes untrusted key or value fragments so control characters cannot add lines;
- summarizes YAML location without echoing source content; and
- exposes no traceback.

Unexpected internal exceptions are converted to the same bounded external shape while tests retain enough internal structure to identify the failed unit.

## Packaging contract

The manifest exposes one script named `load-config-python` at `scripts/python/load_config.py`. The allowlist admits only that script subtree. A disposable enabled installation contains exactly 11 files: manifest, license, configuration template, installer-created project configuration, four commands, the Python loader, and two templates. Every source-owned installed file must match its source counterpart byte-for-byte. A disposable project's newly scaffolded `roadmap-config.yml` is validated against the current configuration template, while an existing dogfood project's `roadmap-config.yml` is project-owned, preserved, validated semantically, and excluded from source-byte-parity comparison. The payload contains no Bash, PowerShell, Bats, Pester, parity, repository metadata, tests, or specifications.
