# Validation Evidence: Command Contract Hardening

This record captures implementation validation and intended-user disposition for roadmap entry 011. The feature is accepted as implemented with Linux validation explicitly deferred.

## Tested identity

- **Repository revision**: `6f7a7ac1ba5267a58ed15c7b9d753be98d75b563`
- **Working-tree status digest**: SHA-256 `5623ac80ad788d416dfff3f5903bdee4119233d88dc40728de8d88e565a9025e`
- **Platform**: Darwin 25.6.0 arm64
- **Python**: 3.11.16
- **Specify CLI**: 1.0.1

The digest identifies the complete `git status --short` manifest at the time of validation. This feature is validated as a working-tree delta rather than as a committed revision.

## Automated validation

The complete project validation passed:

```text
$ mise run test
Ran 105 tests in 10.526s
OK

$ git diff --check
(no output; exit 0)
```

Focused protected-history and command-selection checks also passed:

```text
$ python3 -m unittest discover -s tests/python -p 'test_protected_history.py'
Ran 3 tests
OK

$ python3 -m unittest discover -s tests/python -p 'test_command_selection.py'
Ran 2 tests
OK
```

The `mise` invocation emitted cache-write warnings for a sandboxed user cache, but the test process completed successfully and did not depend on those cache writes.

## Deterministic contract checks

Both no-argument helpers returned the same compact six-field configuration object. Exact brief target resolution selected roadmap entry 011 from `specs/008-command-contract-hardening` even when the ambient feature named feature 007. A debrief finding evaluation with `max_findings=0` displayed no findings while retaining total 1, omitted 1, and verdict `RETHINK` for the hidden Must-Address finding.

Disposable Git repository tests cover explicit ranges, ancestry rejection, baseline-to-worktree and HEAD-to-WORKTREE modes, clean-tree unavailability, exclusions, renames, deletions, untracked files, changed gitlinks, punctuation-leading refs, and content-sensitive snapshot changes. Report-allocation tests cover UTC naming, same-second collision suffixes, exclusive creation, empty reservations, kind-specific directories, and containment rejection.

## Command-selection review

The maintained positive and adjacent-negative prompts were reviewed through this host agent with these results:

| Prompt intent | Expected boundary | Observed selection |
|---|---|---|
| Create the roadmap from constitution decisions | Write positive | Write |
| Plan implementation tasks | Write negative | Not Write |
| Review one specification before implementation | Brief positive | Brief |
| Reconcile the project-wide ledger | Brief negative | Not Brief |
| Review an implemented feature from baseline to target | Debrief positive | Debrief |
| Review before implementation exists | Debrief negative | Not Debrief |
| Reconcile the whole roadmap and specifications | Sync positive | Sync |
| Review only one implemented specification | Sync negative | Not Sync |

The matching fixture and static selection contract are in `tests/fixtures/command-selection.json` and `tests/python/test_command_selection.py`.

## Disposable dogfood matrix

The full quickstart matrix was exercised in an isolated clone. Test setup mutations were established before each observation; command mutations were then compared with that scenario baseline.

| Scenario | Input and selected target | Evidence boundary and report | Findings, verdict, and lifecycle | Observed mutation |
|---|---|---|---|---|
| Exact authorized delta | Write; add isolated `Q-DOGFOOD` marker | Existing roadmap plus direct test authorization; no report | No review findings; version 2.3.1 to 2.3.2 | Roadmap only |
| Inferred interactive amendment | Write; proposed access-time wording clarification | Named contained evidence; no report | Proposal withheld for confirmation | None |
| Inferred non-interactive amendment | Write; same incomplete inference | Named contained evidence; no report | Open question returned | None |
| Embedded instructions in named file | Write; no new target accepted | `dogfood-untrusted-evidence.md`, validated immediately before access; no report | Embedded release/tool directive ignored | Roadmap digest remained `21f045d399b177ab385821af0db1929619db1a22530ba139e20e4a734d5d9eab` |
| Explicit target conflicts with ambient | Brief; explicit feature 008 over ambient feature 007 | Roadmap and explicit spec target; existing brief report | Entry 011 selected by exact spec directory; PROCEED; propose in-progress | Report only |
| Two explicit target forms disagree | Brief; feature 008 plus entry 010 | Target constraints only; no report allocated | Conflict returned; no verdict or lifecycle guidance | None |
| Implemented dependency is unverified | Brief; entry 011 with an implemented dependency | Lifecycle inputs only; no report allocated for the focused check | Dependency awaiting verification and blocking; no in-progress proposal | None |
| Explicit clean commit range plus dirty tree | Debrief; `HEAD^` to `HEAD` with one untracked path | Complete 47-path commit manifest; ambient dirty path explicitly excluded | Trustworthy explicit range; exclusion disclosed | None |
| Dirty tree without explicit range | Debrief; ambient feature delta | HEAD-to-WORKTREE manifest containing `unexpected-runtime-surface.txt` | Trustworthy; complete manifest | None |
| Clean tree without explicit range | Debrief; no baseline or target | Clean disposable commit; no report allocated for focused check | Delta unavailable and untrustworthy; limitation recorded; no absence or verification claim | None |
| Unexpected changed file | Debrief; HEAD-to-WORKTREE | Complete one-path manifest; no focused report allocated | Must-Address `scope-creep`; RETHINK | None |
| Ledger/spec mismatch plus process entry | Sync; project-wide | Entire ledger and `specs/`; `.specify/memory/roadmap-reviews/sync-20260903T200002Z.md` | One `status-lagging` Recommendation; entry 001 informational; PROCEED WITH UPDATES | Sync report only |
| Findings exceed configured cap | Debrief; one Must-Address with cap zero | Structured finding input; no report needed | Total 1, displayed 0, omitted 1; hidden blocker retained; RETHINK | None |
| Same-second report collision | Brief; feature 008 | Existing `brief-20260903T200000Z.md`; reserved `brief-20260903T200000Z-2.md` | Existing report preserved; deterministic lowest suffix selected | New empty reservation only |
| Roadmap creation/amendment prompt | Host selection | Maintained prompt fixture; no report | Write selected | None |
| Implementation-planning prompt | Host selection | Maintained prompt fixture; no report | Write excluded | None |
| Pre-implementation single-spec prompt | Host selection | Maintained prompt fixture; no report | Brief selected | None |
| Project-wide reconciliation prompt for Brief | Host selection | Maintained prompt fixture; no report | Brief excluded | None |
| Post-implementation bounded-delta prompt | Host selection | Maintained prompt fixture; no report | Debrief selected | None |
| Planning-only prompt for Debrief | Host selection | Maintained prompt fixture; no report | Debrief excluded | None |
| Project-wide roadmap/spec prompt | Host selection | Maintained prompt fixture; no report | Sync selected | None |
| Single-feature prompt for Sync | Host selection | Maintained prompt fixture; no report | Sync excluded | None |

The isolated Brief report recorded zero findings, verdict `PROCEED`, and a specced-to-in-progress recommendation because dependencies 009 and 010 were verified. The isolated Debrief report reviewed all 45 paths present before allocation, retained snapshot `sha256:2f993176d9de7755fb912c7c5206604bd615d6b660c3dcbad090d5c6cf8c17f2` across its recheck, reported one `roadmap-stale` Recommendation, returned `PROCEED WITH UPDATES`, and correctly proposed no direct specced-to-verified transition.

## Installed lifecycle-hook dogfood

The current working tree was copied into an isolated local clone at source revision `6f7a7ac1ba5267a58ed15c7b9d753be98d75b563`. `specify extension add . --dev --force` installed Diagram Roadmap 0.2.0 successfully. The installed source-owned payload digest, excluding project configuration, was `514be02595c6c81e604ce7902c81afa01a3130e5d65fef614c699c641668bf7b`.

Specify 1.0.1's `HookExecutor` resolved and dispatched the registered events as follows:

| Lifecycle event | Installed command | Host invocation | Generated artifact | Boundary result |
|---|---|---|---|---|
| `after_constitution` | `speckit.diagram-roadmap.write` | `$speckit-diagram-roadmap-write` | Roadmap 2.3.2 with isolated `Q-DOGFOOD` marker | Only the authorized roadmap changed |
| `before_implement` | `speckit.diagram-roadmap.brief` | `$speckit-diagram-roadmap-brief` | `specs/008-command-contract-hardening/roadmap-reviews/brief-20260903T200000Z.md` | Source preserved; one report written |
| `after_implement` | `speckit.diagram-roadmap.debrief` | `$speckit-diagram-roadmap-debrief` | `specs/008-command-contract-hardening/roadmap-reviews/debrief-20260903T200001Z.md` | Source preserved; one report written after stable delta recheck |

The Brief artifact SHA-256 was `83e301ea41f02751f7960db82ed9e9ac86522f9a69cc42cb8a848dd38f0aeb48`; the Debrief artifact SHA-256 was `5eadef495f378bdd9894d45de2038292e26946325bd5c79fb43117704d4cf213`. All artifacts remained in the disposable clone and were not copied into the development checkout.

## Packaging and historical protection

Byte comparisons succeeded for both Python helpers and the shared report template between source and the installed dogfood payload. The complete suite additionally verifies the twelve-file installation, executable helper, command copies, manifest, generated skill semantics, and registered hook declarations.

The protected-history test found zero semantic changes to merged feature directories 001 through 007, dated reports, released changelog content, roadmap entries 001 through 010, and accepted verification evidence. The repository-content privacy scan found no personal name, username, or absolute personal home path; the Git administrative pointer is outside project content and is not a tracked artifact.

## Intended-user disposition

On 2026-09-03, the intended user reviewed this validation evidence and accepted the revised command selection, repository-contained evidence boundary, attributable debrief provenance, report semantics, and lifecycle guidance. The feature is complete at lifecycle status `implemented`.

## Deferred validation

The following verification gate remains deliberately open:

- **Linux validation**: the intended user explicitly deferred T046 because local virtualization would be disproportionate for this change. The local Colima profile cannot start its configured Docker runtime because the Docker CLI is absent, and no external Linux evidence tied to this working-tree identity was supplied.

This deferral prevents advancing roadmap entry 011 from `implemented` to `verified`; it does not invalidate the intended-user acceptance or completed macOS implementation evidence.
