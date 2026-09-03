# Contract: `review_contract.py`

`scripts/python/review_contract.py` is the deterministic runtime entrypoint for brief, debrief, and sync. It reuses `load_config.py` runtime, repository-root, configuration, and containment primitives. It does not interpret prose, decide semantic similarity, classify drift, assign finding severity/category, or write roadmap/specification content.

## Process Contract

- Python requirement: exactly 3.11.16, matching the existing loader contract.
- Working directory: any path inside the Git repository.
- Standard output on success: exactly one compact JSON object followed by a newline.
- Standard error on expected failure: exactly one `Error: ...` line with no traceback.
- Exit status: zero on success and one on expected contract failure.
- Filesystem mutation: none except `allocate-report`, which atomically creates one empty contained report file.
- Network access: prohibited.
- Git invocation: argument arrays with `--` path boundaries where paths are accepted; no shell interpolation.

Invoking the script with no operation loads the validated extension configuration and emits the six fields required by the review commands. This preserves the one-Python-entry frontmatter shape without changing the verified no-argument behavior of `load_config.py`.

```json
{"roadmap_path":".specify/memory/roadmap.md","roadmap_exists":true,"adr_dir":"docs/adr","adr_present":false,"prd_globs":["**/prd*.md"],"max_findings":50}
```

Paths in examples are repository-relative for readability. The implementation emits canonical absolute paths only where the existing loader contract requires them and never persists machine-specific absolute paths in reports.

## `validate-path`

```text
review_contract.py validate-path --kind roadmap-read|roadmap-write|adr|prd --path PATH
```

This operation delegates to the loader's access-time containment contract and returns the canonical repository-relative path. It exists so review commands retain one declared Python entrypoint while reusing, rather than reproducing, loader validation.

## `resolve-target`

```text
review_contract.py resolve-target \
  --command brief|debrief \
  --roadmap-path PATH \
  [--spec-target TARGET] \
  [--roadmap-entry ENTRY] \
  [--ambient-feature PATH] \
  [--selected-entry ENTRY_ID]
```

Rules:

- At least one explicit target or an ambient feature must be available.
- Explicit target fields outrank ambient state and must converge when both are present.
- Exact specification-directory match is selected immediately.
- If exact matching fails, the helper emits ordered candidates for command-owned title-similarity judgment.
- The command may rerun with `--selected-entry`; the helper accepts it only when it belongs to the emitted candidate set and all explicit constraints still converge.
- Number-only matching is considered only after no exact directory or accepted title match exists.
- Missing, conflicting, or ambiguous resolution never silently falls back to a different feature.

Exact-selection output:

```json
{"state":"selected","selection_source":"explicit-spec","match_method":"exact-spec-dir","entry":{"id":"011","title":"Harden command contracts and review evidence","status":"specced","spec_dir":"specs/008-command-contract-hardening","spec_file":"specs/008-command-contract-hardening/spec.md"},"conflicts":[]}
```

Judgment-required output:

```json
{"state":"needs-judgment","selection_source":"explicit-entry","candidates":[{"id":"011","title":"Harden command contracts and review evidence","spec_dir":"specs/008-command-contract-hardening"}],"conflicts":[]}
```

## `resolve-delta`

```text
review_contract.py resolve-delta [--baseline REF --target REF|WORKTREE]
```

The operation resolves refs with `git rev-parse --verify <ref>^{commit}` and verifies explicit commit ancestry with `git merge-base --is-ancestor`. It captures HEAD, index, worktree, untracked, rename, deletion, type-change, unmerged, and gitlink observations. It returns artifacts in stable path/status order and merges duplicate observations without hiding their sources.

An explicit commit range excludes ambient dirty state from the manifest but reports its presence in `exclusions`. `TARGET=WORKTREE` includes the baseline-to-HEAD range and every dirty source. No explicit range uses `head-to-worktree` only when dirty state exists. A clean tree with no range produces `mode=unavailable`, `trustworthy=false`, and a material limitation.

```json
{"mode":"baseline-to-worktree","baseline_input":"develop","baseline_oid":"0123456789abcdef0123456789abcdef01234567","target_input":"WORKTREE","target_oid":null,"head_oid":"89abcdef0123456789abcdef0123456789abcdef","ancestry_valid":true,"dirty_state":{"staged":1,"unstaged":1,"untracked":1,"deleted":0,"renamed":0,"gitlinks":0},"artifacts":[{"status":"modified","old_path":null,"new_path":"commands/speckit.diagram-roadmap.debrief.md","sources":["worktree"]}],"exclusions":[],"limitations":[],"snapshot_digest":"sha256:...","trustworthy":true}
```

`snapshot_digest` covers the resolved revision identities and normalized dirty-state observations. The command invokes the operation again after evidence collection with the captured digest; one mismatch triggers one complete retry, and a repeated mismatch must be reported as untrustworthy.

## `evaluate-findings`

```text
review_contract.py evaluate-findings --kind brief|debrief|sync --max-findings NON_NEGATIVE_INTEGER
```

The operation reads one JSON array from standard input. Each item contains `severity`, `category`, `text`, `suggestion`, `evidence`, and `blocking`. Input order is retained within a severity.

Validation rules:

- Severity is exactly `Must-Address`, `Recommendation`, or `Question`.
- Category belongs to the selected review kind's taxonomy.
- Text and suggestion are non-empty.
- Evidence is a non-empty array of repository-relative paths, revision identifiers, or explicit limitation markers.
- `blocking=true` is valid only with `Must-Address`.
- The maximum is a non-negative integer; zero is summary-only.

The operation orders findings by severity, assigns `F1` and later IDs, computes totals before truncation, and derives the verdict from all findings.

```json
{"findings":[],"summary":{"max_findings":0,"total":3,"displayed":0,"omitted":3,"by_severity":{"Must-Address":{"total":1,"displayed":0,"omitted":1},"Recommendation":{"total":2,"displayed":0,"omitted":2},"Question":{"total":0,"displayed":0,"omitted":0}},"by_category":{"scope-creep":{"total":3,"displayed":0,"omitted":3}},"verdict":"RETHINK"}}
```

Canonical categories are defined by `contracts/command-workflows.md` and must be represented as constants in the helper rather than repeated ad hoc in each command.

## `evaluate-lifecycle`

```text
review_contract.py evaluate-lifecycle \
  --phase brief|debrief \
  --status STATUS \
  [--spec-complete true|false] \
  [--dependency-status STATUS ...] \
  [--outcome-met true|false] \
  [--delta-trustworthy true|false] \
  [--must-address-count NON_NEGATIVE_INTEGER]
```

For brief, every dependency must be `verified`; `implemented` is represented separately as awaiting verification and all other states block. Planned may propose specced only with a complete specification. Specced may propose in-progress only with ready dependencies. Deferred and abandoned require explicit reactivation approval.

For debrief, only in-progress and implemented are eligible to propose verified, and only when outcome met and delta trustworthy are true and Must-Address count is zero. The operation never performs a transition.

```json
{"current_status":"implemented","proposed_status":"verified","gate_results":{"eligible_source_status":true,"outcome_met":true,"delta_trustworthy":true,"must_address_clear":true},"approval_required":false,"reason":"All verification recommendation gates passed."}
```

Unknown statuses, phase-inapplicable flags, and internally inconsistent values are rejected.

## `allocate-report`

```text
review_contract.py allocate-report \
  --kind brief|debrief|sync \
  [--feature-dir PATH] \
  [--timestamp-utc YYYYMMDDTHHMMSSZ]
```

Brief and debrief require a validated feature directory and allocate beneath its `roadmap-reviews/` directory. Sync allocates beneath `.specify/memory/roadmap-reviews/` and rejects `--feature-dir`. Production invocations derive current UTC time internally; the timestamp option exists for deterministic testing and must pass exact format validation.

The helper tries `<kind>-<timestamp>.md`, then `<kind>-<timestamp>-2.md`, `<kind>-<timestamp>-3.md`, and later names. It uses exclusive creation, never truncates an existing path, validates containment before each attempt, and emits the reserved path only after creation succeeds.

```json
{"state":"reserved","kind":"debrief","timestamp_utc":"20260903T210500Z","collision_index":2,"path":"specs/008-command-contract-hardening/roadmap-reviews/debrief-20260903T210500Z-2.md"}
```

The operation must run after target and delta evidence collection so the new report reservation cannot contaminate the implementation delta.

## Integration Surfaces

- `speckit.diagram-roadmap.write.md` continues to declare `scripts/python/load_config.py`.
- Brief, debrief, and sync declare `scripts/python/review_contract.py`; no-argument execution supplies their validated configuration.
- `extension.yml` declares both Python scripts.
- `.extensionignore` allows the new helper and no unrelated payload.
- The installed dogfood mirror contains an exact helper copy.
- Generated brief, debrief, and sync skills express the same normalized inputs, safety boundary, taxonomies, and failure rules as their source commands.

## Verification Contract

Automated tests use temporary repositories and cover every operation, failure shape, platform-neutral path handling, ref names beginning with punctuation, rename/delete/untracked/gitlink cases, clean-tree unavailability, dirty exclusions, snapshot changes, cap zero, hidden blockers, invalid taxonomies, lifecycle matrices, timestamp collisions, containment, manifest membership, installation parity, and generated-skill semantics.
