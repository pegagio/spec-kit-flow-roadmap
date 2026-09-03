# Feature Specification: Harden Command Contracts and Review Evidence

**Feature Branch**: `not-created`

**Created**: 2026-09-03

**Status**: Draft

**Input**: User description: "Review the current Diagram Roadmap command Markdown and incorporate the accepted recommendations for safer evidence handling, explicit inputs, accurate implementation review, consistent reporting, and state-aware lifecycle guidance."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Safely create or amend durable roadmap content (Priority: P1)

As a project maintainer, I can run the roadmap write command knowing that project documents are treated as evidence rather than instructions and that inferred content will not silently become durable governance.

**Why this priority**: The write command changes the project's durable record. Untrusted or unconfirmed material influencing that record creates the highest risk of incorrect governance, information leakage, and unintended actions.

**Independent Test**: Run the write workflow against repository-contained evidence that includes embedded instructions, incomplete decisions, and a mix of confirmed and inferred content; verify that embedded instructions are ignored, provenance is reported, unresolved material remains proposed or open, and only explicitly approved content is written.

**Acceptance Scenarios**:

1. **Given** an allowed project document contains text instructing the agent to run a tool or change unrelated files, **When** the write command harvests that document, **Then** it treats the text only as evidence and does not follow the embedded instruction.
2. **Given** harvested context supports a proposed roadmap addition but the user has not approved that inferred content, **When** the command runs interactively, **Then** it presents the proposal for confirmation before changing the roadmap.
3. **Given** the command runs without a human interaction channel and the requested change is not explicit and complete, **When** evidence suggests a roadmap amendment, **Then** it reports a proposal or open question without modifying the roadmap.
4. **Given** multiple allowed sources support an amendment, **When** the command presents or writes the amendment, **Then** it identifies the repository-contained sources that informed the content.

### User Story 2 - Receive an evidence-backed implementation debrief (Priority: P2)

As an implementer, I can debrief a feature against an identifiable implementation delta, so conclusions about outcome, scope creep, and constraint compliance are traceable to the work actually reviewed.

**Why this priority**: A review limited to anticipated files can miss unplanned changes and cannot substantiate a claim that no scope creep occurred.

**Independent Test**: Debrief a feature whose implementation delta contains both expected and unexpected changed artifacts; verify that the report identifies its baseline and target, examines the bounded delta, detects the unexpected change, and records any evidence limitation.

**Acceptance Scenarios**:

1. **Given** the user supplies an implementation baseline and target, **When** debrief runs, **Then** those references define the reviewed delta and appear in the report provenance.
2. **Given** no explicit references are supplied but the working tree contains implementation changes, **When** debrief runs, **Then** it reviews the identifiable working-tree delta and records the revision and dirty-state boundary used.
3. **Given** the repository is clean and no implementation range can be established, **When** debrief runs, **Then** it states that limitation and does not claim that scope creep or outcome gaps are absent.
4. **Given** a changed artifact lies outside the files anticipated by the specification or tasks, **When** it is present in the bounded implementation delta, **Then** debrief includes it when evaluating scope creep.

### User Story 3 - Get consistent, state-aware command results (Priority: P3)

As a maintainer, I receive reports and lifecycle recommendations with the same terminology, limits, verdict rules, and provenance across brief, debrief, and sync, so reruns and different invocation paths do not produce contradictory guidance.

**Why this priority**: Shared semantics make the review suite predictable and prevent a command from proposing an invalid or stale lifecycle transition.

**Independent Test**: Exercise representative brief, debrief, and sync scenarios with identical finding severities, status states, dependency states, and findings caps; verify consistent verdicts, category names, report identity, and transition behavior.

**Acceptance Scenarios**:

1. **Given** any review command produces at least one Must-Address finding, **When** it derives the verdict, **Then** the verdict is RETHINK.
2. **Given** a review has no Must-Address findings but has recommendations or questions, **When** it derives the verdict, **Then** the verdict is PROCEED WITH UPDATES.
3. **Given** a review has no findings, **When** it derives the verdict, **Then** the verdict is PROCEED.
4. **Given** the configured findings limit is zero or lower than the number of detected findings, **When** any review report is generated, **Then** its table respects the limit and its summary preserves the total counts and overflow information.
5. **Given** an entry is already in progress, implemented, verified, deferred, or abandoned, **When** brief recommends a lifecycle action, **Then** it does not blindly recommend transitioning that entry to in-progress.
6. **Given** two reports of the same kind are generated within the same timestamp unit, **When** their output paths are selected, **Then** both reports are retained under distinct filesystem-safe names.

### User Story 4 - Invoke the correct command for the intended job (Priority: P4)

As a user or host agent, I can identify each command's accepted inputs, target-selection precedence, outputs, and non-goals from its description and command body, so explicit and implicit invocation selects the appropriate workflow.

**Why this priority**: Clear activation and input boundaries reduce avoidable clarification loops and prevent a project-wide or mutating workflow from running when a narrower review was intended.

**Independent Test**: Present positive and negative invocation prompts for all four commands and verify that each command description identifies its intended use, rejects adjacent jobs, and resolves explicit targets before ambient active-feature state.

**Acceptance Scenarios**:

1. **Given** the user explicitly identifies a spec directory, spec file, or ledger entry, **When** brief or debrief resolves its target, **Then** the explicit target takes precedence over the ambient active feature.
2. **Given** no explicit target is supplied and one active feature can be resolved, **When** brief or debrief runs, **Then** it uses that active feature and reports how the target was selected.
3. **Given** no unique target can be resolved, **When** a command would otherwise have to guess, **Then** it lists the ambiguity or missing input and asks for a decision without writing a report for an assumed target.
4. **Given** a prompt describes an adjacent but unsupported job, **When** command descriptions are evaluated for invocation, **Then** their positive and negative boundaries distinguish the correct workflow.

### Edge Cases

- An allowed evidence file is repository-contained when discovered but resolves through a symlink outside the repository immediately before access.
- A PRD, ADR, handover, or prior report contains prompt-injection text, tool requests, secrets, personal machine paths, or claims unsupported by other project evidence.
- A user explicitly supplies conflicting target forms, such as one spec directory and a different ledger entry.
- A title match produces multiple plausible roadmap entries while an exact `spec dir` pointer is absent.
- A debrief receives an invalid, missing, or non-ancestral revision reference, or a delta includes generated and untracked files.
- A dependency is missing, abandoned, deferred, incomplete, implemented but unverified, or already verified.
- A lifecycle recommendation would skip states, regress a state, or reactivate an abandoned or deferred entry without explicit approval.
- `max_findings` is zero, exactly equal to the finding count, or smaller than the number of Must-Address findings.
- An ADR pointer cannot be resolved because the ADR directory is absent or the referenced ADR does not exist.
- A previous report already occupies the timestamp-derived output path.
- The source command, installed extension mirror, generated skill, shared template, and current documentation disagree after an update.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Each command MUST define its accepted user inputs, target-selection rules, permitted writes, outputs, stop conditions, and evidence limitations explicitly.
- **FR-002**: For brief and debrief, an explicit spec directory, spec file, or ledger-entry target MUST take precedence over ambient active-feature state; exact `spec dir` matches MUST take precedence over title similarity, and title similarity MUST take precedence over number-only matching.
- **FR-003**: A command MUST stop and request a decision when explicit inputs conflict or when target matching remains ambiguous after applying the documented precedence rules.
- **FR-004**: The write command MUST restrict harvested durable-project evidence to repository-contained sources permitted by its documented evidence policy and MUST NOT read machine-global memory or unspecified external handover stores as project evidence.
- **FR-005**: All harvested documents, reports, and quoted session material MUST be treated as untrusted evidence rather than executable instructions; embedded instructions, tool requests, or requests to expand scope MUST NOT be followed unless the user independently gives that instruction in the active interaction.
- **FR-006**: Proposed roadmap content MUST identify the source paths or direct user decisions that support it, and unsupported synthesis MUST be labeled as an inference, proposal, or open question.
- **FR-007**: In interactive use, inferred roadmap content MUST require explicit user confirmation before it changes the durable roadmap.
- **FR-008**: In non-interactive use, the write command MUST modify the roadmap only when the requested delta is explicit, complete, and already authorized; otherwise it MUST return a proposal or open question without modifying the roadmap.
- **FR-009**: Debrief MUST review an identifiable, bounded implementation delta rather than only the artifacts anticipated by the specification or task list.
- **FR-010**: Debrief MUST prefer a valid user-supplied baseline and target; otherwise it MAY use a clearly identifiable working-tree delta, but it MUST report the chosen baseline, target, current revision, and dirty-state boundary.
- **FR-011**: When debrief cannot establish a trustworthy implementation delta, it MUST disclose that limitation and MUST NOT assert that outcome gaps, scope creep, or constraint violations are absent.
- **FR-012**: Debrief MUST consider every artifact in the established implementation delta when evaluating scope creep, while keeping content inspection bounded to that delta and the feature's governing artifacts.
- **FR-013**: Brief MUST classify dependencies as ready only when verified; missing, abandoned, deferred, or not-yet-delivered dependencies MUST block proceeding, while implemented-but-unverified dependencies MUST be reported as awaiting verification.
- **FR-014**: Brief MUST make lifecycle guidance conditional on the entry's current state: planned entries with a completed specification are proposed as specced, specced entries may be proposed as in-progress, entries already in progress or later receive no redundant transition, and deferred or abandoned entries require explicit reactivation approval.
- **FR-015**: Debrief MUST propose verified only when the outcome is met, no Must-Address findings remain, the implementation delta is trustworthy, and the current status is in-progress or implemented; other current states MUST be reported as status drift requiring reconciliation.
- **FR-016**: Status recommendations MUST state the current and proposed statuses and MUST NOT silently skip, regress, or reactivate lifecycle states.
- **FR-017**: Brief, debrief, and sync MUST all consume the configured non-negative findings limit. A zero limit MUST produce summary-only reporting, and overflow MUST retain total counts by severity and category without silently dropping Must-Address findings from the summary.
- **FR-018**: The shared verdict policy MUST be deterministic: any Must-Address finding yields RETHINK; otherwise any Recommendation or Question yields PROCEED WITH UPDATES; no findings yields PROCEED.
- **FR-019**: A finding that must be resolved before safe continuation MUST be classified as Must-Address rather than Question so the verdict policy cannot label a blocking uncertainty as proceedable.
- **FR-020**: The shared report taxonomy MUST use canonical category names. Sync MUST use `status-lagging`, `orphan-spec`, `phantom-entry`, `dependency-contradiction`, `superseded-ADR`, and `abandoned-but-active`; process entries MUST be informational rather than findings. Debrief MUST use `outcome-miss`, `scope-creep`, `constraint-violation`, and `roadmap-stale`.
- **FR-021**: Every report MUST record the selected target, target-selection method, roadmap entry, reviewed source paths, relevant revision or dirty-state evidence, configured findings limit, omitted or aggregated finding counts, and material limitations.
- **FR-022**: Review commands MUST describe themselves as preserving source artifacts while permitting only their documented report write; they MUST NOT claim that creating a report is strictly read-only.
- **FR-023**: Report filenames MUST use a filesystem-safe UTC timestamp with second-level precision and MUST add a deterministic numeric suffix when the derived path already exists.
- **FR-024**: Unresolved ADR pointers MUST be reported as unresolved evidence and MUST NOT be treated as either compliance or violation without the referenced decision content.
- **FR-025**: Each command description MUST front-load when the command should run and state at least one adjacent situation in which it should not be selected.
- **FR-026**: Deterministic mechanics, including path containment, exact target candidates, revision validation, timestamps, collision handling, counts, and output contracts, MUST remain script-owned; synthesis, similarity judgment, drift classification, and remediation guidance MUST remain command-owned.
- **FR-027**: The feature MUST preserve the existing Python path-containment contract and MUST NOT reintroduce machine-global paths, unrestricted globs, shell runtime dependencies, or alternate platform implementations.
- **FR-028**: Current source commands, the installed extension mirror, generated skills, shared report template, extension metadata, and maintained documentation MUST agree on the revised contracts.
- **FR-029**: Automated contract scenarios MUST cover positive, degraded, ambiguous, adversarial-evidence, status-transition, findings-overflow, report-collision, target-selection, and implementation-baseline cases for all affected commands.
- **FR-030**: Validation MUST demonstrate equivalent command contracts and report semantics on macOS and Linux.
- **FR-031**: The feature MUST flow forward without changing merged feature specifications, dated generated reports, protected historical changelog entries, or the accepted implementation evidence for roadmap entries 001 through 010.

### Key Entities

- **Command Contract**: The documented inputs, target-selection rules, evidence boundaries, permitted mutations, outputs, stop conditions, and limitations for one Diagram Roadmap command.
- **Evidence Source**: A repository-contained artifact or direct user decision used to support a proposal or finding, identified by provenance and treated according to its trust level.
- **Implementation Delta**: The bounded set of implementation changes between an identifiable baseline and target, including relevant working-tree state when explicitly selected.
- **Review Finding**: A categorized observation with severity, evidence, remediation guidance, and inclusion in deterministic verdict and count summaries.
- **Lifecycle Recommendation**: A proposed current-to-next status transition constrained by the entry's present state, evidence readiness, and explicit approval requirements.
- **Report Provenance**: The target, roadmap entry, sources, revisions, configuration, aggregation details, and limitations necessary to reproduce or understand a generated review.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In the adversarial-evidence acceptance set, 100% of embedded instructions and tool requests are ignored as directives, and zero unapproved inferred changes are written to the roadmap.
- **SC-002**: Every generated brief, debrief, and sync report includes all required provenance fields, with zero reports claiming evidence that was not inspected.
- **SC-003**: In 100% of debrief acceptance scenarios, the report identifies a valid implementation delta or explicitly limits its conclusions because no trustworthy delta exists.
- **SC-004**: Across all review-command acceptance scenarios, identical severity sets produce identical verdicts, finding caps, total counts, and overflow summaries.
- **SC-005**: All lifecycle and dependency-state scenarios yield the documented state-aware recommendation, with zero redundant, regressive, skipped, or unauthorized reactivation transitions.
- **SC-006**: All ambiguous or conflicting target scenarios stop without selecting an unsupported target or writing a misleading report.
- **SC-007**: Two or more reports generated within the same second retain 100% of outputs under unique filesystem-safe paths.
- **SC-008**: Positive and negative invocation examples for each of the four commands select the intended workflow with no cross-command ambiguity in the maintained acceptance set.
- **SC-009**: Current source commands, installed commands, generated skills, shared templates, metadata, and maintained documentation pass repository consistency checks with zero contract drift.
- **SC-010**: The complete existing contract suite plus the new judgment-focused acceptance scenarios pass on both supported operating systems.
- **SC-011**: Protected-surface comparison reports zero semantic changes to merged feature directories, dated reports, released history, or verified evidence for roadmap entries 001 through 010.

## Assumptions

- Roadmap entry 011 maps to this independently numbered `specs/008-command-contract-hardening/` directory; roadmap and feature-directory numbers remain intentionally independent.
- The verified Python migration and mise tooling entries remain authoritative dependencies, including current path containment, supported operating systems, installed extension layout, and canonical validation entrypoint.
- Direct instructions and approvals provided by the active user are authoritative; text merely quoted or harvested from project artifacts or earlier reports is evidence, not authority.
- The existing lifecycle vocabulary remains unchanged; this feature clarifies transitions and readiness without creating new statuses.
- Similarity-based target matching remains judgment-bearing, while exact candidate discovery and validation remain deterministic mechanics.
- Existing command behavior that is not changed by an explicit requirement remains in scope for regression protection rather than redesign.
