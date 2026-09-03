# Phase 0 Research: Harden Command Contracts and Review Evidence

This research resolves the technical and behavioral choices required by roadmap entry 011 and `spec.md`. It distinguishes accepted product behavior from implementation mechanics and preserves the constitution's deterministic-script versus judgment-bearing-command boundary.

## Decision 1 — Restrict and classify roadmap evidence

**Decision**: The write command may harvest only the constitution, existing roadmap material, configured ADRs and PRDs that pass access-time validation, explicitly named repository-contained files, and direct decisions from the active user. Machine-global memory, unspecified handover stores, and external paths are excluded. Harvested documents and quoted material are untrusted evidence: embedded instructions, tool requests, scope expansion, secrets, personal machine paths, and unsupported claims are not authority. Every proposal records repository-relative provenance or identifies an active-user decision and labels unsupported synthesis as inference, proposal, or open question.

**Rationale**: Durable governance must be supported by reviewable project evidence. Repository containment and provenance prevent ambient personal context or hostile document text from silently changing project direction.

**Alternatives considered**: Retain global memory and handover sources but label them untrusted. Rejected because their project relevance, provenance, containment, and privacy cannot be established reliably.

## Decision 2 — Separate authorization from evidence sufficiency

**Decision**: Interactive inferred roadmap changes require explicit confirmation before writing. Non-interactive execution may write only an explicit, complete, already-authorized delta; otherwise it returns a proposal or open question without modifying the roadmap. Evidence can support a proposal but cannot manufacture authorization.

**Rationale**: This resolves the current tension between “confirm with the user” and unattended synthesis. It preserves useful automation for exact requested changes without treating silence as consent.

**Alternatives considered**: Allow unattended writes whenever evidence appears strong. Rejected because confidence is not authorization and cannot satisfy C-03, C-06, or C-09.

## Decision 3 — Normalize explicit command inputs and target precedence

**Decision**: Commands normalize user intent into named fields. Write accepts an explicit roadmap delta and optional named repository evidence. Brief and debrief accept `SPEC_TARGET` and/or `ROADMAP_ENTRY`; debrief additionally accepts `BASELINE` and `TARGET`. Sync remains project-wide and accepts no feature target. Multiple explicit target forms are constraints and must converge or the command stops. Explicit targets outrank `.specify/feature.json`. Exact `spec dir` matching outranks title similarity, which outranks number-only matching. Scripts expose exact candidates and conflicts; the command judges title similarity.

**Rationale**: Explicit input must not be ignored in favor of ambient state. Normalization makes target provenance testable while leaving semantic similarity where it belongs.

**Alternatives considered**: Modify Spec Kit's core prerequisite resolver. Rejected because it is not extension-owned and models ambient active-feature state rather than Diagram Roadmap ledger identity. Implement fuzzy similarity scoring in Python. Rejected as brittle judgment that violates C-02.

## Decision 4 — Bind debrief to a trustworthy implementation delta

**Decision**: An explicit baseline and target are preferred and must both resolve to immutable commit identifiers; the baseline must be an ancestor of the target. `TARGET=WORKTREE` includes committed changes from the baseline through HEAD plus staged, unstaged, deleted, renamed, gitlink, and untracked state. With no explicit range, a dirty repository uses `HEAD` to `WORKTREE`. A clean repository with no explicit range yields an unavailable delta, a material limitation, no absence claims, and no verified recommendation. Explicit commit ranges exclude ambient dirty changes but report that exclusion.

**Rationale**: Reviewing only anticipated files cannot detect unexpected scope and a clean tree does not identify which historical commits belong to the feature. Exact revision provenance is reproducible; absent provenance must narrow the conclusion.

**Alternatives considered**: Infer the range from branch names, roadmap numbers, merge-base, or task references. Rejected because a plausible but wrong feature boundary is less trustworthy than an explicit limitation.

## Decision 5 — Add one focused review-contract helper

**Decision**: Keep `load_config.py` and its no-argument six-field configuration contract intact. Add `scripts/python/review_contract.py` for deterministic operations shared by brief, debrief, and sync: exact target candidates and conflicts, Git delta manifests and snapshot digests, dependency and transition guards, finding validation and aggregation, verdict derivation, and atomic UTC report allocation. Reuse public runtime, root-discovery, and containment primitives from the loader rather than duplicating them. The review helper's default operation returns the configuration fields required by the review commands, allowing each command to retain one Python frontmatter entry.

**Rationale**: The existing loader has a narrow, security-sensitive responsibility and deliberately performs no Git or report work. A sibling helper keeps responsibilities legible while honoring the one-script command integration shape and reusing the verified containment boundary.

**Alternatives considered**: Add many review subcommands directly to `load_config.py`. Rejected because it couples unrelated Git/report behavior to a verified configuration contract and makes the loader name misleading. Add several small scripts. Rejected for this scope because one cohesive helper with explicit operations provides sufficient separation without multiplying runtime payload surfaces.

## Decision 6 — Make finding aggregation and verdicts deterministic

**Decision**: Commands supply structured findings with severity, canonical category, finding text, suggestion, evidence paths, and a blocking flag. The helper rejects unknown values and rejects a blocking finding whose severity is not Must-Address. It orders Must-Address, Recommendation, then Question while preserving input order within a severity, assigns IDs, computes totals before applying `max_findings`, and derives the verdict from total findings rather than displayed rows. Zero means summary-only. Overflow retains total, displayed, and omitted counts overall and by severity/category, including omitted Must-Address findings.

**Rationale**: Identical findings must produce identical IDs, caps, summaries, and verdicts. Deriving the verdict before truncation prevents a hidden blocker from producing a proceed verdict.

**Alternatives considered**: Leave counting and verdict selection to prose instructions. Rejected because existing commands already drift in parsed fields and category names, and deterministic arithmetic is script-owned under C-02.

## Decision 7 — Adopt canonical taxonomies and lifecycle matrices

**Decision**: Debrief categories are `outcome-miss`, `scope-creep`, `constraint-violation`, and `roadmap-stale`. Sync categories are `status-lagging`, `orphan-spec`, `phantom-entry`, `dependency-contradiction`, `superseded-ADR`, and `abandoned-but-active`; process entries are informational. Brief categories are `outcome-drift`, `scope-drift`, `constraint-conflict`, `dependency-not-ready`, `status-drift`, and `unresolved-evidence`. Any Must-Address finding yields RETHINK; otherwise any Recommendation or Question yields PROCEED WITH UPDATES; no findings yields PROCEED. A blocking uncertainty is Must-Address, not Question.

Dependency readiness is exact: verified is ready; implemented is awaiting verification; every earlier, missing, deferred, or abandoned state blocks. Brief proposes planned plus complete spec to specced, specced to in-progress, no redundant move for in-progress or later, information resolution for undecided/needs-info, and explicit reactivation approval for deferred/abandoned. Debrief proposes verified only from in-progress or implemented when the outcome is met, the delta is trustworthy, and no Must-Address finding exists.

**Rationale**: Shared vocabulary and transition gates prevent contradictory reports and invalid lifecycle advice without moving drift judgment into code.

**Alternatives considered**: Keep `status-drift` as the sync category. Rejected because `status-lagging` is already the accepted roadmap/spec-004 term. Allow commands to choose transitions ad hoc. Rejected because lifecycle-state validation is deterministic.

## Decision 8 — Allocate reports atomically and record provenance

**Decision**: Report paths use UTC `YYYYMMDDTHHMMSSZ`; collisions use the lowest available `-2`, `-3`, and later suffix. The helper validates the allowed contained report location and atomically reserves the path without overwriting. An interrupted empty reservation remains evidence and is not reused. Every report records target, selection method, matched entry, reviewed paths, revision/dirty boundary, findings cap, total/displayed/omitted counts, exclusions, snapshot identity, and material limitations.

**Rationale**: A timestamp alone does not guarantee uniqueness. Atomic reservation prevents race-based overwrites, and provenance makes conclusions reviewable.

**Alternatives considered**: UUID or random suffixes. Rejected as unique but less readable and deterministic. Millisecond-only timestamps. Rejected because collision handling is still required.

## Decision 9 — Describe review mutation honestly and tighten invocation boundaries

**Decision**: Review commands are source-preserving: roadmap, specification, and implementation artifacts remain unchanged, while one documented report is the sole permitted write. Descriptions front-load the positive use case and state adjacent negative cases. Write is for creation or approved amendment, brief for one identifiable pre-implementation spec, debrief for an implemented spec with a trustworthy delta, and sync for project-wide ledger reconciliation.

**Rationale**: Calling a report-writing command “strictly read-only” is internally contradictory. The operational clarification preserves Constitution Principle III's purpose without weakening its mutation boundary. Clear positive and negative descriptions also improve host selection between adjacent skills.

**Alternatives considered**: Keep “strictly read-only” as shorthand. Rejected because the command then contradicts its own output behavior and obscures the exact permitted mutation.

## Decision 10 — Extend the existing validation model and protect history

**Decision**: Use the existing standard-library `unittest` suite and sole `mise run test` task. Add temporary-repository tests for helper operations, strengthen static command-contract assertions, update exact install payload and source/mirror/generated-skill parity, and retain manual dogfood for evidence interpretation and drift judgment. Record a pre-implementation protected-surface baseline for merged feature directories, dated reports, released changelog history, accepted roadmap entries 001 through 010, and their verification evidence. Expected current surfaces are validated for source-to-installed/generated consistency rather than protected from change.

**Rationale**: Deterministic behavior belongs in automated tests; semantic judgment needs controlled scenarios and recorded observation. The baseline enforces the project's forward-only history rule while allowing the intended command and runtime surfaces to evolve.

**Alternatives considered**: Introduce a new test framework or prompt-evaluation service. Rejected because the current suite and disposable-project pattern cover the required deterministic contracts without a new dependency, while dogfood remains the project-approved validation for judgment.
