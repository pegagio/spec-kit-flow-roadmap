# Quickstart: Implement and Validate Command Contract Hardening

This guide defines the implementation sequence and acceptance evidence for roadmap entry 011. It is intended for a disposable development checkout with the feature specification, plan, research, data model, and contracts available.

## Prerequisites

Use the repository-managed toolchain and inspect the checkout before editing:

```bash
git status --short --branch
mise trust
mise install
mise run test
```

The baseline suite should pass before implementation. Record the current commit and protect merged feature directories 001 through 007, dated roadmap reports, released changelog history, roadmap entries 001 through 010, and their accepted verification evidence from semantic edits.

## Implementation Sequence

Implement in small reviewable increments:

1. Refactor only the reusable runtime, root-discovery, and containment primitives from `scripts/python/load_config.py`, preserving its no-argument six-field output and failure contract.
2. Add `scripts/python/review_contract.py` with the interfaces in [review-contract.md](contracts/review-contract.md).
3. Add focused helper tests for target resolution, delta capture, finding aggregation, lifecycle gates, and report allocation.
4. Update the four source commands and shared report template to the workflow contract in [command-workflows.md](contracts/command-workflows.md).
5. Update `extension.yml`, `.extensionignore`, source documentation, and test guidance.
6. Refresh the installed dogfood mirror and generated skills from their canonical source commands.
7. Run automated validation, disposable-project dogfood, and protected-history checks.

Do not allocate a debrief report until target and implementation-delta evidence have been collected; otherwise the report itself can appear in the delta.

## Deterministic Helper Checks

After implementation, verify that no-argument review configuration remains compact JSON and that the original loader output has not changed:

```bash
python3 scripts/python/load_config.py
python3 scripts/python/review_contract.py
```

Resolve an exact feature target and confirm that explicit input outranks ambient state:

```bash
python3 scripts/python/review_contract.py resolve-target --command brief --roadmap-path .specify/memory/roadmap.md --spec-target specs/008-command-contract-hardening --ambient-feature specs/007-resolve-ambiguous-entry-selection
```

Exercise summary-only finding aggregation and confirm that an omitted Must-Address finding still yields `RETHINK`:

```bash
printf '%s\n' '[{"severity":"Must-Address","category":"scope-creep","text":"Unexpected runtime surface","suggestion":"Remove or authorize the surface","evidence":["unexpected.txt"],"blocking":true}]' | python3 scripts/python/review_contract.py evaluate-findings --kind debrief --max-findings 0
```

Use disposable Git repositories in tests for delta cases. Do not create artificial commits or working-tree mutations in the project checkout merely to exercise the helper.

## Automated Validation

Run the repository's sole validation entrypoint and whitespace checks:

```bash
mise run test
git diff --check
```

The automated suite must demonstrate:

- The original loader contract and containment failures remain unchanged.
- Explicit target convergence, conflicts, missing targets, candidate handoff, and ambient fallback are deterministic.
- Commit ranges, baseline-to-worktree, head-to-worktree, clean-tree unavailable state, exclusions, renames, deletes, untracked files, gitlinks, and snapshot changes are complete.
- Finding validation, stable ordering and IDs, uncapped totals, cap zero, hidden blockers, and verdict derivation are exact.
- Dependency and lifecycle matrices reject invalid recommendations.
- Report reservations use UTC names, deterministic collision suffixes, exclusive creation, and permitted directories only.
- Source, installed mirror, generated skills, manifest, and allowlist remain consistent.

## Disposable Dogfood Matrix

Run each judgment-bearing scenario in a disposable initialized project and retain concise observations:

| Scenario | Command | Expected result |
|---|---|---|
| Exact authorized delta | Write | Roadmap changes without redundant confirmation |
| Inferred interactive amendment | Write | Proposal shown and explicit confirmation required |
| Inferred non-interactive amendment | Write | No roadmap mutation; proposal or open question returned |
| Named file containing embedded instructions | Write | Content treated only as evidence; instructions ignored |
| Explicit target conflicts with ambient feature | Brief | Explicit target selected |
| Two explicit target forms disagree | Brief | Command stops with conflict |
| Dependency is implemented but not verified | Brief | Must-Address and no in-progress recommendation |
| Explicit clean commit range plus dirty tree | Debrief | Dirty state excluded and disclosed |
| Dirty tree without explicit range | Debrief | HEAD-to-WORKTREE manifest reviewed |
| Clean tree without explicit range | Debrief | Delta unavailable; no absence claim or verified recommendation |
| Unexpected changed file outside anticipated scope | Debrief | Scope finding supported by complete manifest |
| Ledger/spec mismatch plus process entry | Sync | Mismatch classified; process entry informational |
| More findings than configured cap | Any review | Totals and omitted counts remain complete; verdict uses all findings |
| Same-second report collision | Any review | Existing report preserved and lowest numeric suffix allocated |
| Roadmap creation or approved amendment prompt | Write | Host selects write |
| Implementation-planning prompt | Write negative | Host does not select write |
| Pre-implementation single-spec review prompt | Brief | Host selects brief |
| Project-wide reconciliation prompt | Brief negative | Host does not select brief |
| Post-implementation bounded-delta review prompt | Debrief | Host selects debrief |
| Planning-only review prompt | Debrief negative | Host does not select debrief |
| Project-wide roadmap/spec reconciliation prompt | Sync | Host selects sync |
| Single-feature review prompt | Sync negative | Host does not select sync |

For each scenario, record inputs, selected target, reviewed evidence, observed report path, findings totals, verdict, lifecycle recommendation, and whether the source tree remained unchanged apart from the permitted output.

Exercise the repository-owned dogfood installation in an isolated clone or worktree of this repository. Trigger the registered `after_constitution`, `before_implement`, and `after_implement` hooks and record the source revision, installed payload identity, observed command dispatch, and generated artifacts. A different generic Spec Kit project does not satisfy this repository's constitutional dogfood gate.

## Packaging and Generated-Surface Validation

Verify that installation adds exactly the intended helper payload and that no unrelated file becomes installable. Compare source and installed copies of both Python scripts and the shared template, then verify that generated skills preserve the source command's invocation boundaries, inputs, taxonomy, mutation rule, and failure behavior.

The expected installed payload increases by one source-owned helper file. Any larger unexplained increase is a failure.

## Acceptance Record

Create `validation-evidence.md` during implementation only after automated and dogfood checks complete. It should record:

- Commit or working-tree identity tested.
- Exact validation commands and results.
- Automated test count.
- Dogfood scenario results and report paths.
- Host-agent command-selection results for every maintained positive and adjacent-negative prompt.
- Real-project execution evidence for all three registered extension hooks.
- Protected-history comparison result.
- Source/install/generated parity result.
- Known limitations and residual risks.
- Explicit intended-user disposition when requested by the feature tasks.

Passing automation is evidence, not intended-user acceptance. Leave acceptance tasks open until the designated user records the disposition.
