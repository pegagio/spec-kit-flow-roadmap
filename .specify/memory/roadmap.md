<!--
SYNC IMPACT REPORT
==================
Version change: 2.4.3 → 2.4.4
Bump rationale: PATCH — records verification of existing entry 012 without changing its scope or outcome.

Changes this revision (2.4.4, amended 2026-09-23):
  - Advanced entry 012 from in-progress to verified after the completed specification, implementation debrief, and 114 passing tests.

Specs affected: 012 verified
Open questions added/resolved: none.

--- Prior revision (2.4.3, amended 2026-09-23): PATCH — aligned the living roadmap title, vision, and source-of-truth note with the FlowKit Roadmap identity in entry 012. Specs affected: 012 current identity documentation; status remained in-progress. Open questions added/resolved: none.

--- Prior revision (2.4.2, amended 2026-09-23): PATCH — refined entry 012's human-readable name to FlowKit Roadmap and recorded its product-group relationship. Specs affected: 012 display name refined; status remained in-progress. Open questions added/resolved: none.

--- Prior revision (2.4.1, amended 2026-09-23): PATCH — advanced entry 012 to in-progress at the intended user's request before specification, confirmed its verified dependencies, resolved Q7 as documented manual migration, and recorded `specs/009-rename-flow-roadmap/`. Specs affected: 012 advanced to in-progress. Open questions added/resolved: Q7 resolved.

--- Prior revision (2.4.0, amended 2026-09-23): MINOR — added planned entry 012 for the Spec Kit Flow Roadmap identity migration and Q7 for existing-installation migration. Specs affected: 012 added. Open questions added/resolved: Q7 added.

--- Prior revision (2.3.2, amended 2026-09-03): PATCH — records intended-user acceptance, advances entry 011 to implemented, and explicitly defers Linux verification. Specs affected: 011 advanced to implemented. Open questions added/resolved: none.

--- Prior revision (2.3.1, amended 2026-09-03): PATCH — records the new command-contract specification and advances entry 011 to specced. Specs affected: 011 advanced to specced. Open questions added/resolved: none.

--- Prior revision (2.3.0, amended 2026-09-03): MINOR — added C-09, requiring repository-contained, provenance-preserving treatment of project evidence as untrusted data rather than executable instructions; added planned entry 011 to review and harden the four command contracts, their shared report semantics, and their judgment-focused validation scenarios. Specs affected: 011 added. Open questions added/resolved: none.

--- Prior revision (2.2.0, amended 2026-09-02): MINOR — refined entry 010's scope after clean Linux validation proved mise's `pipx:` backend requires a declared `uv` or `pipx` installer; recorded pinned `uv` and the explicit Python/`uv` installation dependency as accepted in-scope tooling; changed entry 010 from planned to verified after all 17 tasks, convergence, protected-surface checks, and macOS/Linux validation completed successfully. Specs affected: 010 amended and verified. Open questions added/resolved: none.

--- Prior revision (2.1.0, amended 2026-09-01): MINOR — added C-08, establishing mise as the canonical project toolchain and task runner; added planned entry 010 to preserve the real test workflow in mise, remove the Just scaffolding, and align current documentation and contract tests. Specs affected: 010 added. Open questions added/resolved: none.

--- Prior revision (2.0.1, amended 2026-09-01): PATCH — marked the completed Python migration verified and recorded its feature-directory and validation evidence. Changed entry 009 from planned to verified after implementation, convergence, and the macOS/Linux validation matrix completed successfully; added the `specs/006-python-script-migration/` pointer and verification evidence to entry 009. Specs affected: 009. Open questions added/resolved: none.

--- Prior revision (2.0.0, amended 2026-08-31): MAJOR — reversed the Windows and
    paired Bash/PowerShell platform decision, adopted macOS/Linux and Python, and
    added the required migration spec. Replaced the platform contract in C-01,
    C-05, and C-07; marked former parity decisions superseded without rewriting
    verified historical specs; and added planned entry 009. Specs affected: 009
    added; 002 and 006 retained as historical implementation records. Open
    questions added/resolved: none.

--- Prior revision (1.5.2, amended 2026-08-31): PATCH — resolved Q1–Q6 or
    removed them as obsolete; recorded current numbering, command-spec,
    compatibility, loader-path, and process-entry behavior.

--- Prior revision (1.5.1, amended 2026-08-31): PATCH — changed entry 007 from
    planned to abandoned; preserved its intended outcome and scope as history;
    retired its dependency edge without changing C-01 or C-07.

--- Prior revision (1.5.0, amended 2026-08-30): MINOR — added entry 008 for the
    flow-forward rename to Diagram Roadmap/diagram-roadmap; updated current command,
    installation, project, and repository naming; verified the installed identity;
    preserved accepted historical terminology.

--- Prior revision (1.4.0, amended 2026-06-24): MINOR — after spec 004 verified.
    005 roadmap.sync → verified; scope-in gained the divergence taxonomy,
    status pivot, empty-dir definition, and process-entry exception; Q6 added.

--- Prior revision (1.3.0, amended 2026-06-24): MINOR — after spec 003 verified.
    004 roadmap.debrief → verified; scope-in gained the drift taxonomy + verified-gate +
    bounded reading; spec dir + C-01 added.

--- Prior revision (1.2.0, amended 2026-06-24): MINOR — after spec 002 verified.
    003 roadmap.brief → verified; scope-in gained the shared review template + the
    ambiguous-match tie-break; spec dir + C-01 added.

--- Prior revision (1.1.0, amended 2026-06-24): MINOR — after spec 001 verified.
    002 → verified (folded in PowerShell parity + test suite from former 006); 006
    → abandoned (absorbed into 002, struck through not deleted); Q4 resolved.

--- Prior revision (1.0.0, ratified 2026-06-24): MAJOR — first ratified roadmap;
    replaced the template skeleton with vision, decisions C-01..C-07, the 001–007
    spec ledger, and Open Questions Q1..Q5. Drafted by harvesting the constitution,
    extension.yml, config-template.yml, and the task list; gaps parked as Open
    Questions rather than fabricated.
-->

# FlowKit Roadmap — Spec Roadmap

Living, non-binding map of the specs planned for **FlowKit Roadmap**. It is **not a
commitment to order or scope** — it captures the spec-specific discussion,
decisions, technology choices, outcomes, and constraints surfaced during the
constitution and grilling phases so they are not lost before the spec that needs
them is written. Specs are scoped and clarified when they are actually started.
Foundations: the project [constitution](constitution.md). No PRD detected.

Status legend (lifecycle): **undecided** · **needs-info** · **planned** ·
**specced** · **in-progress** · **implemented** · **verified** · **deferred** ·
**abandoned**.

---

## Vision & End States

<!-- Harvested from the constitution; the WHY of the project. -->

- A spec-kit extension (`flow-roadmap`) that **installs and registers cleanly**
  via `specify extension add` / `enable` and whose three lifecycle hooks
  (`after_constitution`, `before_implement`, `after_implement`) fire correctly in a
  real spec-kit project.
- A **durable, versioned roadmap artifact** lives beside the constitution
  (`.specify/memory/roadmap.md`) that captures the WHY — decisions, technology
  choices, intended outcomes, constraints — plus a cross-spec ledger (planned specs,
  dependencies, lifecycle status), surviving across features.
- **No loss of constitution-phase / grilling context**: spec-specific intent for
  specs not written for weeks or months is recorded once and checked later.
- **Pre- and post-implementation reviews** that read the roadmap and check the spec
  about to be / just built against its recorded outcome and scope — strictly
  read-only, proposing changes rather than applying them.
- The extension is **dogfooded on its own repository** (built through constitution → roadmap → specify → plan → tasks → implement) before release and ships with Apache-2.0 licensing. The former cross-platform Bash/PowerShell parity end state was superseded on 2026-08-31.
- The extension supports **macOS and Linux**, uses **Python as its only maintained scripting language**, and does not target Windows or retain Bash/PowerShell runtime compatibility.

## Constraints & Decisions

<!-- Durable "why", harvested from the constitution and extension.yml. No ADRs
     present, so none of these link out yet. Stable ids let spec entries reference
     them. -->

- **C-01 — Canonical conformance (Constitution I):** the extension MUST match real spec-kit extension shape within its supported platform contract (valid `extension.yml`; `commands/` whose `name:` is the full `speckit.{id}.{cmd}` slug; Python scripts where scripts are used; `templates/`; `config-template.yml`; README + CHANGELOG + LICENSE). Ground truth is spec-kit docs then real bundled extensions (`critique`, `verify`). The current manifest requires Spec Kit `>=1.0.0`. **Superseded 2026-08-31:** this decision formerly required paired Bash + PowerShell scripts.
- **C-02 — Determinism split (Constitution II):** deterministic mechanics
  (path/feature resolution, prereq checks, JSON output contracts, version/changelog
  arithmetic, file-existence checks) live in scripts; judgment (elicitation,
  synthesis, drift detection, review reasoning) lives in command bodies. Neither
  re-derives the other's work.
- **C-03 — Non-destructive & idempotent (Constitution III):** commands never
  overwrite user-authored content; review commands are STRICTLY read-only and only
  edit after explicit approval; every command is safe to re-run; roadmap changes
  append to the Sync Impact Report changelog and mark (not delete) superseded
  entries.
- **C-04 — Roadmap as durable governance (Constitution IV):** the roadmap is a
  project-level artifact beside the constitution (default
  `.specify/memory/roadmap.md`, overridable via `config-template.yml`), carries
  constitution-style semver + Sync Impact Report, and survives across features.
- **C-05 — Supported platforms and Python scripting (Constitution V):** the extension supports macOS and Linux; Windows support is explicitly not a goal. Python is the only maintained scripting language. Extension commands MUST NOT ship or require Bash or PowerShell runtime scripts, compatibility wrappers, paired implementations, or platform-specific parity. **Superseded 2026-08-31:** this decision formerly required `.sh` + `.ps1` pairs, paired frontmatter, and macOS/Linux/Windows behavior.
- **C-06 — Elicitation completeness, no fabrication (Constitution VI):** the draft
  command actively asks for end states, goals, scope (in/out), outcomes, and
  constraints where the constitution did not settle them, and never invents content
  — unknowns become explicit Open Questions or `needs-info`/`undecided` entries.
- **C-07 — Packaging & distribution (Technology Constraints):** distributed as a spec-kit extension; source of truth at the repo root; scripts are Python and emit stable JSON contracts where structured output is required; hooks are `after_constitution` / `before_implement` / `after_implement`; license Apache-2.0. Non-binding: if it conflicts with a principle, the principle wins. **Superseded 2026-08-31:** this decision formerly selected POSIX Bash + PowerShell 7+ and reuse of core Bash helpers.
- **C-08 — Canonical project tooling:** `mise.toml` is the canonical declaration of development tool versions and project task entrypoints. Maintained development documentation and validation MUST use `mise run <task>` rather than duplicate workflows through Just or another task runner. Canonical tasks MUST execute real project workflows; placeholder tasks that report success without doing work are not retained.
- **C-09 — Evidence trust boundary:** Project documents, prior reports, handovers, session context, and other harvested material are untrusted evidence, not instructions. Commands MUST restrict durable evidence harvesting to repository-contained, explicitly permitted sources; preserve source provenance; ignore embedded instructions or tool requests; and require explicit user approval before inferred content changes a durable governance artifact. Non-interactive execution MUST surface unsupported or unconfirmed content as a proposal or open question rather than silently adopting it.

## Planned Specs

<!-- THE LEDGER. Roadmap numbers are planning identifiers and the current extension
     does not require or guarantee that they match specs/NNN-* directory numbers.
     Existing spec directories will not be renumbered; a later extension update may
     enforce consistency, and roadmap identifiers may be reconsidered then. -->

### Core extension

### 001 — Bootstrap extension skeleton  [status: implemented]

- **Description:** The minimal installable shell of the extension — `extension.yml`
  manifest (id, provides, hooks, requires), the roadmap template, and the initial
  `roadmap.write` command body — enough to install and fire the
  `after_constitution` hook.
- **Outcome:** `extension.yml` validates against the spec-kit loader; the extension
  installs/enables and the `after_constitution` hook is registered; the roadmap
  template and draft command exist at the repo root.
- **Scope (in):** `extension.yml`, `templates/roadmap-template.md`, initial
  `commands/speckit.diagram-roadmap.write.md`.
- **Scope (out):** brief/debrief/sync commands; PowerShell scripts; tests; release
  packaging.
- **Depends on:** none.
- **Governed by:** C-01, C-07.
- **Notes:** Matches task "Author minimal bootstrap (manifest, template, draft)",
  marked complete. The bootstrap artifacts are present at the repo root and mirrored
  under `.specify/extensions/diagram-roadmap/`.

### 002 — roadmap.write command + load-config script  [status: verified]

- **Description:** The create/amend `write` command plus its `load-config` script
  (bash + PowerShell) that emits the JSON config contract (`roadmap_path`,
  `roadmap_exists`, `adr_dir`, `adr_present`, `prd_globs`, `max_findings`).
- **Outcome:** Running `speckit.diagram-roadmap.write` after the constitution produces a
  versioned `roadmap.md` (v1.0.0 on create) or non-destructively amends + version-
  bumps an existing one; the script resolves config from `config-template.yml` /
  `roadmap-config.yml` and `SPECKIT_DIAGRAM_ROADMAP_*` env overrides, identically on bash and
  PowerShell. **Achieved** — verified by 96 passing tests (Bats 35 + Pester 53 +
  parity 8) and two clean verification gates.
- **Scope (in):** `commands/speckit.diagram-roadmap.write.md`, `scripts/bash/load-config.sh`,
  **`scripts/powershell/load-config.ps1` + the Bats/Pester/parity test suite** (folded
  in from former entry 006), config detection logic, self-detecting create-vs-amend,
  semver bump rules, malformed-roadmap guard.
- **Scope (out):** brief/debrief/sync (entries 003–005); release packaging (007).
- **Depends on:** 001.
- **Governed by:** C-02, C-03, C-04, C-05, C-06.
- **Spec dir:** specs/001-roadmap-write/
- **Notes:** Built via the full SDD cycle (specify → plan → critique → tasks →
  implement → verify → debrief). The debrief surfaced that PowerShell parity landed
  here rather than in a separate spec; entry 006 is absorbed into this one (see v1.1.0
  Sync Impact Report). Resolves former Q4: the installed Bash script path is
  `.specify/extensions/diagram-roadmap/scripts/bash/load-config.sh`, and the
  Spec Kit-compliant filename present on disk is authoritative.

### 003 — roadmap.brief (pre-implementation review)  [status: verified]

- **Description:** Read-only briefing fired by the `before_implement` hook that
  surfaces what the roadmap expects for the spec about to be implemented — outcome,
  scope, governing decisions, dependencies.
- **Outcome:** Before `/speckit.implement`, the implementer sees the roadmap entry's
  recorded outcome, in/out scope, governing C-/ADR ids, and dependency specs, with
  no file mutation. **Achieved** — built via the full SDD cycle and dogfood-verified
  read-only (roadmap unchanged across runs).
- **Scope (in):** `commands/speckit.diagram-roadmap.brief.md`; matching the active spec to its
  ledger entry (spec-dir → title → number, with an **ambiguous-match tie-break: list
  candidates and ask**); rendering a briefing report; **the shared
  `templates/review-report-template.md`** (also reused by debrief/sync).
- **Scope (out):** any roadmap or spec mutation; status transitions.
- **Depends on:** 002 (verified).
- **Governed by:** C-01, C-03.
- **Spec dir:** specs/002-roadmap-brief/
- **Notes:** Built via specify → plan → critique → tasks → brief → implement → debrief.
  No new scripts/tests (judgment, Principle II — validated by dogfood). Critique added
  the ambiguous-match tie-break; debrief proposed this verified status + scope update.

### 004 — roadmap.debrief (post-implementation review)  [status: verified]

- **Description:** Read-only review fired by the `after_implement` hook that checks
  the implemented spec against its roadmap entry's outcome and scope, classifies drift,
  and proposes a status transition.
- **Outcome:** After `/speckit.implement`, a report compares the built spec to its
  recorded outcome/scope and PROPOSES (does not apply) a ledger status update.
  **Achieved** — built via the full SDD cycle and dogfood-verified read-only.
- **Scope (in):** `commands/speckit.diagram-roadmap.debrief.md`; outcome/scope comparison; the
  **drift taxonomy** (outcome-miss / scope-creep / constraint-violation / roadmap-stale);
  the **verified-gate** (propose verified only when outcome met AND zero must-address);
  bounded reading of spec-referenced artifacts; uses the shared review-report template.
- **Scope (out):** applying edits without approval; authoring spec or ADR files.
- **Depends on:** 002 (verified), 003-brief (verified).
- **Governed by:** C-01, C-03.
- **Spec dir:** specs/003-roadmap-debrief/
- **Notes:** Built via specify → plan → critique → tasks → brief → implement → debrief
  (the debrief reviewed its own implementation). No new scripts/tests (judgment,
  Principle II). Critique added the verified-gate + bounded reading.

### 005 — roadmap.sync (drift reconciliation)  [status: verified]

- **Description:** Read-only reconciliation that detects drift between the roadmap
  ledger and specs on disk — orphans, phantom entries, status drift, dependency
  contradictions, superseded ADRs.
- **Outcome:** A findings report (capped at `max_findings`) listing roadmap/spec
  drift, proposing reconciling edits without applying them. **Achieved** — built via
  the full SDD cycle and dogfooded against this repo's own roadmap (correctly flagged
  the then-in-progress sync spec as status-lagging).
- **Scope (in):** `commands/speckit.diagram-roadmap.sync.md`; whole-ledger-vs-`specs/`
  comparison; the **STATUS-as-pivot** disk-existence rule; the divergence taxonomy
  (orphan-spec / phantom-entry / status-lagging / dependency-contradiction /
  superseded-ADR); the **empty-dir** definition (spec.md missing or still template);
  the **process-entry exception** (entries with no `spec dir:` pointer are not phantoms);
  uses the shared review-report template; roadmap-level report.
- **Scope (out):** auto-applying reconciliation; mutating specs.
- **Depends on:** 002 (verified).
- **Governed by:** C-01, C-03.
- **Spec dir:** specs/004-roadmap-sync/
- **Notes:** Manual command, no lifecycle hook. Built via specify → plan → critique →
  tasks → brief → implement → debrief. No new scripts/tests (judgment, Principle II;
  `specs/` enumerated in-model). The real dogfood surfaced the process-entry exception
  (now in scope) — see Open Question Q6.

### Cross-cutting

### 006 — Cross-platform script parity + tests  [status: abandoned]

- **Description:** ~~PowerShell counterparts for every bash script with identical JSON
  output contracts, plus parity tests proving bash and PowerShell agree.~~
  **ABSORBED into entry 002** (debrief 2026-06-24): cross-platform parity is
  foundational, not a separable follow-on — PowerShell `load-config.ps1` and the
  Bats/Pester/parity suite were delivered as part of spec 001. Future scripts added by
  003–005 carry the C-05 parity obligation within their own specs.
- **Outcome:** _superseded — see entry 002._
- **Scope (in):** _superseded — see entry 002._
- **Depends on:** 002.
- **Governed by:** C-05, C-02.
- **Notes:** Not a separate spec. Kept here (struck through, not deleted) to preserve
  the decision history per the Non-Destructive principle.
  `tests/` is currently a `.gitkeep` placeholder.

### 007 — Release packaging  [status: abandoned]

- **Description:** Release-readiness artifacts: README, CHANGELOG, LICENSE
  (Apache-2.0), and release-please automation; final conformance check that the
  extension installs and hooks fire in a real spec-kit project.
- **Outcome:** ~~The extension is publishable — docs present, changelog automated,
  Apache-2.0 license shipped, and dogfooded install/hook-fire verified.~~ _Forgone —
  release packaging will not be pursued._
- **Scope (in):** ~~README.md, CHANGELOG.md, LICENSE, release-please config, final
  conformance/dogfood gate.~~ _No active scope; entry abandoned._
- **Scope (out):** feature behavior of the four commands.
- **Depends on:** ~~002, 003, 004, 005, 006.~~ _None — dependency edge retired with
  this abandoned entry._
- **Governed by:** C-01, C-07.
- **Notes:** Maps to task "Add release-please + README/CHANGELOG/LICENSE". LICENSE
  exists at the repo root already; README/CHANGELOG for the extension were still
  pending when this entry was planned. **Abandoned 2026-08-31:** the project decided
  not to pursue release packaging. This status change does not amend C-01 or C-07;
  any future release requires new roadmap work or an explicit governance amendment.

### 008 — Rename project identity  [status: verified]

- **Description:** Rename the active project identity to Diagram Roadmap, the extension ID to `diagram-roadmap`, the intended repository to `spec-kit-diagram-roadmap`, and the canonical commands to `speckit.diagram-roadmap.*`.
- **Outcome:** A disposable Spec Kit project installs and enables Diagram Roadmap version `0.2.0`; all four commands, generated skills, hooks, configuration, runtime paths, and current project documentation agree on the new identity.
- **Scope (in):** `extension.yml`, `.extensionignore`, `commands/`, `scripts/`, `templates/review-report-template.md`, platform tests, current project documentation, constitution identity text, and this living roadmap.
- **Scope (out):** Renaming the GitHub repository or local checkout; compatibility aliases; automatic migration of existing installed configuration; rewriting merged feature directories, dated reports, or released changelog history.
- **Depends on:** 001, 002, 003, 004, 005.
- **Governed by:** C-01, C-03, C-05, C-07.
- **Spec dir:** specs/005-rename-project-identity/
- **Notes:** This entry flows the later identity change forward while preserving the accepted terminology of earlier features. Verified by a disposable Spec Kit 1.0.1 installation, exact payload and generated-skill checks, hook registration checks, and installed Bash loader execution; Bats and PowerShell were unavailable locally.

### 009 — Migrate scripts to Python  [status: verified]

- **Description:** Flow the new platform and scripting policy forward by replacing the extension's current Bash and PowerShell automation with Python and removing Windows support.
- **Outcome:** On macOS and Linux, all four commands install and execute with equivalent deterministic configuration and prerequisite behavior through Python, the established JSON configuration contract remains stable, and the shipped extension has no Bash or PowerShell runtime dependency.
- **Scope (in):** Select and document the supported Python runtime contract; replace `scripts/bash/load-config.sh` and `scripts/powershell/load-config.ps1` with a Python loader; migrate command script frontmatter and any Bash prerequisite resolution; update `extension.yml`, the installed dogfood snapshot, current tests and fixtures, task-runner configuration, README, and other current documentation; remove obsolete Bash/PowerShell source and tests; validate on macOS and Linux.
- **Scope (out):** Windows compatibility; Bash or PowerShell wrappers; parallel implementations or parity tests; behavior changes to roadmap synthesis or review judgment; retroactive edits to merged feature directories, dated reports, or historical changelog entries.
- **Depends on:** 008.
- **Governed by:** C-01, C-02, C-03, C-05, C-07.
- **Spec dir:** specs/006-python-script-migration/
- **Notes:** The exact supported Python version and invocation details are selected during specification and planning against the active Spec Kit contract. The migration MUST preserve current configuration precedence, validation, path containment, output fields, exit behavior, and non-destructive command semantics unless the new spec explicitly changes them. **Verified 2026-09-01:** all 36 tasks completed; 77 tests passed on macOS and Linux with Specify CLI 1.0.1, Python 3.11.16, and PyYAML 6.0.3; the exact installed payload, generated skills, hooks, and bounded dogfood scenarios passed. See `specs/006-python-script-migration/validation-evidence.md` and `specs/006-python-script-migration/roadmap-reviews/debrief-20260901T143917Z.md`.

### 010 — Make mise the canonical project tool  [status: verified]

- **Description:** Consolidate development tool versions and executable project workflows under mise, replacing the remaining Just-based task-runner surface.
- **Outcome:** Contributors install the declared toolchain with mise and run the complete Python contract suite through `mise run test`; current documentation, task configuration, and repository contract tests agree that mise is the sole canonical project task runner.
- **Scope (in):** Add a real `test` task to `mise.toml` using the existing Python contract-suite command; remove the `justfile`; replace current `just test` guidance with `mise run test`; update current-surface tests so they validate `mise.toml`; review the existing mise tool declarations and retain only declarations with a current project purpose; pin `uv` as the installer required by mise's `pipx:` backend and make the Specify CLI declaration depend on the pinned Python and `uv` tools; validate clean installation, mise task configuration, the complete test suite, and repository whitespace.
- **Scope (out):** Rewriting merged feature directories, dated reports, or released changelog history; changing extension runtime behavior or supported platforms; introducing another task runner, framework, or build system; ~~introducing any dependency~~ (**superseded 2026-09-02:** required clean-install tooling is in scope); introducing a dependency unrelated to declared tooling setup and validation; preserving placeholder `build`, `dev`, or `clean` tasks; creating a lint task without a repository-owned lint configuration.
- **Depends on:** 009.
- **Governed by:** C-01, C-02, C-05, C-08.
- **Spec dir:** specs/007-adopt-mise-tooling/
- **Notes:** Preserve the functional behavior of the existing `just test` recipe, not the Just wrapper. A mise task runs inside the mise-managed environment and should invoke `python` directly rather than nesting `mise exec`. Historical evidence that records `just test` remains unchanged under the merge-bounded persistence policy. **Verified 2026-09-02:** all 17 tasks completed; convergence found no gaps; the exact one-task inventory, disabled task auto-install, clean setup, failure propagation, missing-tool non-bootstrap behavior, and all 80 tests passed on macOS and Linux with Python 3.11.16, `uv` 0.12.5, and Specify CLI 1.0.1; protected history, runtime, packaging, generated skills, and dogfood payload matched their pre-implementation baseline. See `specs/007-adopt-mise-tooling/quickstart.md` and `specs/007-adopt-mise-tooling/roadmap-reviews/debrief-20260902T144140Z.md`.

### 011 — Harden command contracts and review evidence  [status: implemented]

- **Description:** Review and refine the four Diagram Roadmap command bodies so their inputs, evidence boundaries, lifecycle recommendations, and generated reports are explicit, safe, and consistent across interactive, hook-driven, and non-interactive use.
- **Outcome:** `write`, `brief`, `debrief`, and `sync` operate from explicit target and evidence contracts; untrusted context cannot silently direct durable changes; debrief conclusions are tied to an identifiable implementation delta; review commands share one findings cap, drift taxonomy, verdict policy, status-transition policy, and report provenance contract; ambiguous or insufficient evidence produces a clear limitation or question rather than an unsupported conclusion.
- **Scope (in):** Add repository-contained evidence and provenance rules to `write`; reconcile interactive confirmation with non-interactive behavior; define argument precedence and target resolution; bind `debrief` to a bounded implementation baseline and record the reviewed revision/dirty state; consume `max_findings` consistently; standardize drift categories and verdict derivation; make dependency readiness and status recommendations state-aware; clarify that review commands preserve source artifacts while writing reports; define collision-safe report identity; tighten skill descriptions with positive and negative invocation boundaries; update the shared report template, installed extension mirror, current documentation, and judgment-focused scenario tests or fixtures needed to validate these behaviors.
- **Scope (out):** Replacing the Python loader or reimplementing path containment delivered by entry 009; changing the roadmap file format or lifecycle vocabulary; adding new commands or hooks; Windows, Bash, or PowerShell support; rewriting merged feature directories, dated reports, or released changelog history; implementing unrelated product features.
- **Depends on:** 009, 010.
- **Governed by:** C-01, C-02, C-03, C-04, C-05, C-06, C-07, C-08, C-09.
- **Spec dir:** specs/008-command-contract-hardening/
- **Notes:** This entry flows forward from the 2026-09-03 review of the current command Markdown. Existing Python path validation remains authoritative. The feature should preserve the determinism split: scripts may expose exact repository state and validation inputs, while command bodies retain synthesis and drift judgment. **Specced 2026-09-03:** the feature specification and quality checklist define the accepted command-contract changes with no unresolved clarification markers. **Implemented 2026-09-03:** all implementation and macOS dogfood tasks passed, and the intended user accepted the command selection, evidence boundaries, debrief provenance, report semantics, and lifecycle guidance. Linux validation is explicitly deferred, so this entry remains implemented rather than verified. See `specs/008-command-contract-hardening/validation-evidence.md`.

### 012 — Rename to FlowKit Roadmap  [status: verified]

- **Description:** Rename this project to **FlowKit Roadmap**, the human-readable name under the FlowKit brand for the spec-kit-flow product group, with project identifier `spec-kit-flow-roadmap`; rename its Spec Kit extension ID from `diagram-roadmap` to `flow-roadmap`.
- **Outcome:** Current project and extension display names use FlowKit Roadmap; the project identifier uses `spec-kit-flow-roadmap`; the installed extension uses `flow-roadmap`; the four canonical commands use `speckit.flow-roadmap.<purpose>`; and generated skills use `speckit-flow-roadmap-<purpose>`, with each purpose retaining its existing behavior.
- **Scope (in):** Align current-facing project metadata, extension manifest and installation identity, command IDs and files, generated skills, hooks, configuration names and environment overrides, runtime paths, packaging rules, tests, and documentation with the new identities. Validate installation and command dispatch in a disposable Spec Kit project.
- **Scope (out):** New roadmap behavior or commands; changes to the separate Spec Kit Flow bundle or The Diagram; rewriting merged feature directories, dated reports, released changelog history, or earlier roadmap entries.
- **Depends on:** 008 (verified prior identity), 009 (verified Python runtime), 010 (verified project tooling).
- **Governed by:** C-01, C-03, C-05, C-07, C-08.
- **Spec dir:** specs/009-rename-flow-roadmap/
- **Notes:** The project and extension identifiers were explicitly distinguished by the intended user on 2026-09-23. The intended user subsequently selected FlowKit Roadmap as the human-readable name without changing those identifiers. Specify 1.0.1 derives a generated skill name by replacing dots in a canonical `speckit.<extension-id>.<purpose>` command with hyphens, so extension ID `flow-roadmap` produces the requested `speckit-flow-roadmap-<purpose>` skills. The prior `diagram-roadmap` identity remains accepted history in entry 008. Entry 011's deferred Linux verification remains a separate gate. **In progress 2026-09-23:** the intended user explicitly started this feature before specification; the `specced` state was skipped by that requested sequence. The intended user selected documented manual migration that preserves existing configuration. **Verified 2026-09-23:** the specification is Complete, all 36 tasks are checked, the fresh debrief found no roadmap gaps and recommended verification, and all 114 tests passed on macOS. The GitHub repository was renamed by the maintainer; local checkout and worktree directory renames are intentionally deferred until after feature completion. See `specs/009-rename-flow-roadmap/roadmap-reviews/debrief-20260923T154819Z.md`.

## Open Questions

Q1–Q6 were resolved or removed on 2026-08-31; their durable conclusions are recorded in the ledger, Constraints & Decisions, and Cross-Cutting Notes. Q7 was resolved on 2026-09-23: existing `diagram-roadmap` installations require a documented manual migration to `flow-roadmap` that preserves configuration.

## Cross-Cutting Notes

<!-- Architecture-level notes spanning multiple specs. -->

- **Determinism split is the recurring shape.** Every command (002–005) pairs deterministic automation (path resolution, prerequisite and existence checks, JSON contracts, version/changelog arithmetic) with a judgment-bearing command body. Entry 009 migrates that automation to Python under C-05.
- **Read-only is the default for reviews.** brief/debrief/sync (003/004/005) must
  emit reports and PROPOSE edits only; only `write` (002) writes, and only the roadmap
  artifact, non-destructively.
- **Source of truth is the repo root**, mirrored into `.specify/extensions/flow-roadmap/`
  for the installed/dogfooded copy. Keep both in sync when editing commands/scripts.
- **Roadmap and spec numbering are independent in the current version.** Existing
  spec directories will not be renumbered. Matching uses explicit `Spec dir`
  pointers and titles; a later extension update should remedy the lack of enforced
  numbering consistency, potentially by renumbering roadmap identifiers.
- **Command features may use separate specs.** Entries 002–005 were intentionally
  implemented in separate feature directories rather than one combined spec.
- **Process entries are explicit by omission.** A lifecycle entry with no `Spec dir`
  pointer, such as bootstrap entry 001, is informational process work and is exempt
  from phantom-entry detection.
- **Platform boundary is intentional.** macOS and Linux are the supported operating systems. Windows, Bash, and PowerShell compatibility are non-goals; merged specs and dated reports retain earlier references only as historical evidence.
- **Development tooling has one canonical surface.** mise owns project tool versions and task entrypoints; current contributor documentation uses `mise run`, while accepted historical artifacts retain the commands that were current when their work was verified.

---

**Version**: 2.4.4 | **Ratified**: 2026-06-24 | **Last Amended**: 2026-09-23
