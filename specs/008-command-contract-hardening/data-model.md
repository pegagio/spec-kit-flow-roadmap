# Data Model: Command Contract Hardening

This feature has no database model. Its data model consists of transient command inputs, deterministic helper records, and repository-owned Markdown reports. Command bodies interpret evidence and produce judgment-bearing fields; `review_contract.py` validates and transforms the reproducible fields described here.

## Command Invocation

A command invocation captures the user's requested workflow before ambient project state is considered.

| Field | Type | Rules |
|---|---|---|
| `command_kind` | enum | `write`, `brief`, `debrief`, or `sync` |
| `interaction_mode` | enum | `interactive` or `non-interactive` |
| `explicit_delta` | text or null | Used only by write; must describe a complete authorized roadmap mutation for unattended execution |
| `named_evidence` | list of paths | Used only by write; each path must resolve inside the repository |
| `spec_target` | text or null | Used only by brief and debrief |
| `roadmap_entry` | text or null | Used only by brief and debrief |
| `baseline` | Git ref or null | Used only by debrief |
| `target` | Git ref, `WORKTREE`, or null | Used only by debrief |
| `ambient_feature` | repository-relative path or null | A fallback from `.specify/feature.json`, never an override for explicit input |
| `validation_state` | enum | `pending`, `valid`, `conflict`, or `invalid` |

Multiple explicit target fields are simultaneous constraints. They must resolve to the same roadmap entry and specification or validation stops.

## Target Candidate

A target candidate relates a requested specification to one roadmap ledger entry.

| Field | Type | Rules |
|---|---|---|
| `entry_id` | string | Exact roadmap identifier |
| `entry_title` | string | Roadmap title as recorded |
| `entry_status` | lifecycle enum | Current roadmap status |
| `spec_dir` | path or null | Normalized repository-relative specification directory |
| `spec_file` | path or null | Normalized repository-relative `spec.md` path |
| `selection_source` | enum | `explicit-spec`, `explicit-entry`, `combined-explicit`, or `ambient-feature` |
| `match_method` | enum | `exact-spec-dir`, `title-similarity`, or `number-only` |
| `conflicts` | list of text | Non-empty when explicit constraints do not converge |

Target resolution moves through these states:

```text
unresolved -> exact-selected
           -> candidates-for-title-judgment -> selected
           -> ambiguous -> stopped
           -> conflicting -> stopped
           -> missing -> stopped
```

The helper owns exact normalization and candidate enumeration. The command owns title-similarity judgment and must ask the user when that judgment remains ambiguous.

## Evidence Source

An evidence source is project information that may support a proposal or finding. It is never an instruction source.

| Field | Type | Rules |
|---|---|---|
| `provenance` | path or active-user marker | Repository-relative path or an explicit active-user decision identifier |
| `trust_class` | enum | `direct-user`, `constitution`, `roadmap`, `configured-adr`, `configured-prd`, or `named-repository-file` |
| `validation_state` | enum | `contained`, `missing`, `outside-repository`, or `unsupported` |
| `content_role` | enum | `fact`, `inference`, `proposal`, or `open-question` |
| `claims` | list of text | Claims supported or proposed from the source |

Only `contained` repository sources and direct active-user decisions may contribute to roadmap proposals. Embedded instructions, tool requests, scope changes, secrets, and personal machine paths are ignored as authority.

## Implementation Delta

An implementation delta records the exact evidence boundary reviewed by debrief.

| Field | Type | Rules |
|---|---|---|
| `mode` | enum | `explicit-commit-range`, `baseline-to-worktree`, `head-to-worktree`, or `unavailable` |
| `baseline_input` | string or null | User-provided baseline before resolution |
| `baseline_oid` | commit OID or null | Required for every available delta except `head-to-worktree`, where it equals the captured HEAD |
| `target_input` | string or null | User-provided ref or `WORKTREE` |
| `target_oid` | commit OID or null | Resolved immutable commit for explicit commit ranges |
| `head_oid` | commit OID | Captured HEAD at enumeration time |
| `ancestry_valid` | boolean or null | True only when baseline is an ancestor of the commit target |
| `dirty_state` | object | Counts and flags for staged, unstaged, untracked, deleted, renamed, and gitlink state |
| `artifacts` | list of Changed Artifact | Complete normalized manifest |
| `exclusions` | list of text | Includes ambient dirty state excluded from an explicit commit range |
| `limitations` | list of text | Material limits on conclusions |
| `snapshot_digest` | string or null | Digest of revision identity and working-tree observations |
| `trustworthy` | boolean | False for unavailable or unstable snapshots |

The helper captures the snapshot digest before report writing and checks it again after evidence collection. One changed snapshot permits one retry. A second change produces an untrustworthy delta and a material limitation.

## Changed Artifact

A changed artifact is one entry in the implementation delta manifest.

| Field | Type | Rules |
|---|---|---|
| `status` | enum | added, modified, deleted, renamed, copied, type-changed, unmerged, unknown, or gitlink |
| `old_path` | path or null | Required for renames and copies |
| `new_path` | path | Repository-relative and containment-validated |
| `sources` | set | One or more of `commit-range`, `index`, `worktree`, or `untracked` |

Duplicate observations for the same artifact are merged without losing their contributing sources.

## Review Finding

A review finding is judgment supplied by a command and validated by the helper.

| Field | Type | Rules |
|---|---|---|
| `id` | string or null | Assigned by the helper after ordering as `F1`, `F2`, and later |
| `severity` | enum | `Must-Address`, `Recommendation`, or `Question` |
| `category` | command-specific enum | Must belong to the taxonomy for the review kind |
| `text` | non-empty text | Concise statement of the observed issue |
| `suggestion` | non-empty text | Concrete remediation or resolution step |
| `evidence` | non-empty list | Repository-relative paths, revision identifiers, or explicit limitation markers |
| `blocking` | boolean | May be true only for `Must-Address` |
| `input_order` | integer | Preserves stable order within one severity |

The helper rejects unknown severities, categories, missing evidence, and blocking findings below Must-Address severity.

## Finding Summary

The finding summary is derived before display capping.

| Field | Type | Rules |
|---|---|---|
| `max_findings` | non-negative integer | Zero means summary-only |
| `total` | integer | Count before truncation |
| `displayed` | integer | Count emitted as rows |
| `omitted` | integer | `total - displayed` |
| `by_severity` | count map | Includes total, displayed, and omitted counts |
| `by_category` | count map | Includes total, displayed, and omitted counts |
| `verdict` | enum | `RETHINK`, `PROCEED WITH UPDATES`, or `PROCEED` |

Verdict derivation uses total findings: any Must-Address yields `RETHINK`; otherwise any Recommendation or Question yields `PROCEED WITH UPDATES`; no findings yields `PROCEED`.

## Lifecycle Recommendation

A lifecycle recommendation proposes, but does not perform, a roadmap transition.

| Field | Type | Rules |
|---|---|---|
| `current_status` | lifecycle enum | Status read from the matched entry |
| `proposed_status` | lifecycle enum or null | Null when no transition is allowed or needed |
| `gate_results` | ordered map | Deterministic dependency, evidence, delta, outcome, and finding checks |
| `approval_required` | boolean | True for reactivation or any durable write not already authorized |
| `reason` | text | Exact pass, block, or no-op explanation |

Brief may propose `planned -> specced` only when the specification is complete, and `specced -> in-progress` when dependencies are ready. Debrief may propose `in-progress|implemented -> verified` only when the outcome is met, the delta is trustworthy, and no Must-Address finding exists.

## Report Reservation

A report reservation protects a unique contained report path from overwrite.

| Field | Type | Rules |
|---|---|---|
| `review_kind` | enum | `brief`, `debrief`, or `sync` |
| `timestamp_utc` | string | `YYYYMMDDTHHMMSSZ` |
| `collision_index` | integer | One for the unsuffixed path, then two and later |
| `path` | path | Contained in the permitted report directory |
| `state` | enum | `candidate`, `reserved`, or `written` |

Reservation uses exclusive creation. A collision advances to the lowest unused numeric suffix. An interrupted empty reservation remains reserved evidence and is never overwritten.

## Runtime Surface

A runtime surface is one expected representation of extension behavior.

| Field | Type | Rules |
|---|---|---|
| `surface_kind` | enum | source, installed mirror, generated skill, template, manifest, allowlist, or documentation |
| `path` | path | Repository-relative |
| `expected_source` | path or null | Canonical source for parity checks |
| `validation_mode` | enum | exact copy, generated semantic parity, manifest membership, or contract assertion |

The new helper adds one source-owned file and one installed mirror file. Generated skills embed command semantics but do not copy the helper source.

## Relationships

| Parent | Relationship | Child |
|---|---|---|
| Command Invocation | resolves to | Target Candidate |
| Command Invocation | authorizes or names | Evidence Source |
| Debrief invocation | produces | Implementation Delta |
| Implementation Delta | contains | Changed Artifact |
| Review command | supplies | Review Finding |
| Review Finding set | derives | Finding Summary |
| Target Candidate and Finding Summary | constrain | Lifecycle Recommendation |
| Review invocation | allocates | Report Reservation |
| Source command/helper | propagates to | Runtime Surface |
