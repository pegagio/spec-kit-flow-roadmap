# Protected-Surface Baseline

**Recorded**: 2026-09-02T03:11:37Z
**Git HEAD**: `68f08e8133d8eb5e5bf99628d30a7d41afb1da49`

This baseline predates Feature 007 implementation changes. Final validation must reproduce the same protected path set, status command, binary diff command, and complete file manifest. Any difference is a Feature 007 boundary violation unless it was already captured below.

## Protected Paths

- `specs/001-roadmap-write/`
- `specs/002-roadmap-brief/`
- `specs/003-roadmap-debrief/`
- `specs/004-roadmap-sync/`
- `specs/005-rename-project-identity/`
- `specs/006-python-script-migration/`
- `CHANGELOG.md`
- `commands/`
- `scripts/`
- `templates/`
- `extension.yml`
- `.extensionignore`
- `.specify/extensions/diagram-roadmap/`
- `.agents/skills/speckit-diagram-roadmap-brief/`
- `.agents/skills/speckit-diagram-roadmap-debrief/`
- `.agents/skills/speckit-diagram-roadmap-sync/`
- `.agents/skills/speckit-diagram-roadmap-write/`

## Protected-Path Status

```text
A  specs/006-python-script-migration/roadmap-reviews/brief-20260901T145849Z.md
```

## Protected-Path Binary Diff from HEAD

```diff
diff --git a/specs/006-python-script-migration/roadmap-reviews/brief-20260901T145849Z.md b/specs/006-python-script-migration/roadmap-reviews/brief-20260901T145849Z.md
new file mode 100644
index 0000000..9200f31
--- /dev/null
+++ b/specs/006-python-script-migration/roadmap-reviews/brief-20260901T145849Z.md
@@ -0,0 +1,48 @@
+# Pre-Implementation Brief Report: Python Script Migration
+
+**Date**: 2026-09-01
+**Feature**: [Python Script Migration](../spec.md)
+**Roadmap**: [Diagram Roadmap entry 009](../../../.specify/memory/roadmap.md#009--migrate-scripts-to-python-status-verified)
+**Verdict**: 🛑 RETHINK
+
+## Summary
+
+The active-feature resolver selected the completed Python Script Migration and matched it unambiguously to roadmap entry 009 through its `Spec dir` pointer. The specification remains aligned with entry 009's recorded outcome, scope, dependency, and governing decisions, but entry 009 is already verified and the feature specification is complete. The requested next work concerns planned entry 010, which does not yet have an active feature specification. Implementation must not reopen or repurpose this merged historical feature.
+
+## Surfaced Context
+
+- **Entry**: 009 — Migrate scripts to Python · **Status**: verified
+- **Description**: Replace the extension's Bash and PowerShell automation with Python, support macOS and Linux, and remove Windows support.
+- **Outcome (expected)**: All four commands install and execute on macOS and Linux through Python while preserving the deterministic configuration contract and eliminating Bash and PowerShell runtime dependencies. The roadmap records this outcome as achieved and verified.
+- **Scope (in / out)**: In scope were the Python runtime contract, loader migration, command frontmatter and prerequisite migration, manifest and dogfood updates, current tests and documentation, removal of obsolete runtime sources, and macOS/Linux validation. Out of scope were Windows compatibility, compatibility wrappers, changes to roadmap judgment, and retroactive edits to merged historical artifacts.
+- **Depends on**: 008 — Rename project identity (**verified**)
+- **Governed by**: C-01 — Canonical conformance; C-02 — Determinism split; C-03 — Non-destructive and idempotent; C-05 — Supported platforms and Python scripting; C-07 — Packaging and distribution. No ADR directory is configured, and these roadmap decisions resolve directly without external ADR links.
+- **Addresses**: No PRD pointer is recorded.
+- **Related open questions / cross-cutting notes**: The roadmap has no open questions. Relevant notes preserve merged feature directories and dated reports as historical evidence, establish the repository root as the source of truth, and establish mise as the canonical current development-tool surface under the later entry 010.
+
+## Findings
+
+| ID | Severity | Category | Finding | Suggestion |
+|----|----------|----------|---------|------------|
+| F1 | 🎯 Must-Address | status-drift | The resolver selected a feature whose specification is complete and whose roadmap entry is verified. There is no pre-implementation work remaining under entry 009. | Do not reopen or repurpose `specs/006-python-script-migration/`; create or select the new feature specification for roadmap entry 010. |
+| F2 | 🎯 Must-Address | scope-creep | Migrating the remaining Just workflow to canonical mise is a later, independently accepted change recorded by entry 010, not unfinished scope in the Python migration. Adding it to feature 006 would rewrite the accepted historical boundary. | Run the specification workflow for entry 010, ensure the new feature points back to entry 009 as its dependency, then rerun this briefing against that active feature. |
+
+## Findings Summary
+
+| Severity | Count |
+|----------|-------|
+| 🎯 Must-Address | 2 |
+| 💡 Recommendation | 0 |
+| 🤔 Question | 0 |
+
+## Recommended Actions *(proposed only — never auto-applied)*
+
+1. **F1**: Create and select a new feature specification for roadmap entry 010 rather than changing the completed feature 006.
+2. **F2**: Carry entry 010's outcome, in/out scope, dependency on entry 009, and governing decisions C-01, C-02, C-05, and C-08 into the new specification, then rerun `/speckit.diagram-roadmap.brief`.
+3. After the new specification is aligned and implementation is ready to begin, change entry 010 from `planned` to `in-progress` via `/speckit.diagram-roadmap.write`; do not change entry 009's `verified` status.
+
+---
+
+**Severity Legend**: 🎯 Must-Address (blocks proceeding) · 💡 Recommendation (strongly suggested) · 🤔 Question (needs a decision). **This report is read-only**; apply any roadmap changes via `/speckit.diagram-roadmap.write`.
+
+*Generated by `/speckit.diagram-roadmap.brief`.*
```

## Complete File Manifest

The object IDs below use Git blob hashing and include tracked, untracked, and ignored files under the protected paths.

```text
c049586f33fa64d7dfa2674ea0faec20e79ffacf  .agents/skills/speckit-diagram-roadmap-brief/SKILL.md
8fa090363f2ae28f287258e9b4ce15e16ae4a783  .agents/skills/speckit-diagram-roadmap-debrief/SKILL.md
e7ae93b03b23256eb1ce791cbd2d737443c0a5c0  .agents/skills/speckit-diagram-roadmap-sync/SKILL.md
3b5f70627edcd755e883ca3036a50dcaac2da473  .agents/skills/speckit-diagram-roadmap-write/SKILL.md
30844f3e0a65c62d8ec85aa9a425dbc70d072da2  .extensionignore
0a3847ca4bb367f41a8b2a8050ad27361cc5bb53  .specify/extensions/diagram-roadmap/LICENSE
c585399f3165b8594412070ad1c4b885808ceb67  .specify/extensions/diagram-roadmap/commands/speckit.diagram-roadmap.brief.md
af0c5b4bb37bd6dbd6144184cccb02a9e7e58946  .specify/extensions/diagram-roadmap/commands/speckit.diagram-roadmap.debrief.md
95130dab8773044748d68394fb0d3a82343f69d8  .specify/extensions/diagram-roadmap/commands/speckit.diagram-roadmap.sync.md
c7e70dfdf5e7a72a98678710afb69c55af8f5c78  .specify/extensions/diagram-roadmap/commands/speckit.diagram-roadmap.write.md
52dd637e104d7387bb4da1144152ce7a835d0ded  .specify/extensions/diagram-roadmap/config-template.yml
6b3bf7ff286fb31fda327c55482c68b9ca8b3cb8  .specify/extensions/diagram-roadmap/extension.yml
7e1d2f8570b578ff266ec34120513ebdcf2f7332  .specify/extensions/diagram-roadmap/roadmap-config.yml
7f3de94643c07ff8fb1db9da4d818af474b30985  .specify/extensions/diagram-roadmap/scripts/python/load_config.py
8e7c6b9cf6a1c941093203939113dda02d60b1cb  .specify/extensions/diagram-roadmap/templates/review-report-template.md
ef98438d85b13694601c89571384d7d02e7b78ad  .specify/extensions/diagram-roadmap/templates/roadmap-template.md
30a2a9451b1a75d1426fbecf16e41f2b0490128c  CHANGELOG.md
c585399f3165b8594412070ad1c4b885808ceb67  commands/speckit.diagram-roadmap.brief.md
af0c5b4bb37bd6dbd6144184cccb02a9e7e58946  commands/speckit.diagram-roadmap.debrief.md
95130dab8773044748d68394fb0d3a82343f69d8  commands/speckit.diagram-roadmap.sync.md
c7e70dfdf5e7a72a98678710afb69c55af8f5c78  commands/speckit.diagram-roadmap.write.md
6b3bf7ff286fb31fda327c55482c68b9ca8b3cb8  extension.yml
7f3de94643c07ff8fb1db9da4d818af474b30985  scripts/python/load_config.py
b46d474f8b27d24b8c748f9155cd58cc9f29ef9b  specs/001-roadmap-write/checklists/requirements.md
1dec2a0bda05e824324fa979cd6fb27c0d1dda2f  specs/001-roadmap-write/contracts/load-config.schema.json
a80021f6968d82b6e9d3acedc95dc828638f4a1d  specs/001-roadmap-write/critiques/critique-2026-06-24.md
11f27bdf87de9af7bd5d7791236a73be21372d63  specs/001-roadmap-write/data-model.md
69a384945785bc8edd983549200e62c6a66c869d  specs/001-roadmap-write/plan.md
477c56596674e8812b8b5351636d3ac40030dbcc  specs/001-roadmap-write/quickstart.md
adaa8861d29f48feaa8c0cb0ee8f8b1fb9953187  specs/001-roadmap-write/research.md
06083ad2d97d7f944cc9b6bb5f776000db4b391e  specs/001-roadmap-write/spec.md
b96554824a538ea98391d4b617685cfb0a481e7a  specs/001-roadmap-write/tasks.md
c3e010cf8221ad831bd8c7f6901b2fd2c185ef27  specs/002-roadmap-brief/checklists/requirements.md
4d6c967b3232b0558ad0c064909515184e2d4b1e  specs/002-roadmap-brief/critiques/critique-2026-06-24.md
55c1fed8468d6f875a687ce569f15300a38655dc  specs/002-roadmap-brief/plan.md
7beac043bc570ebd02ba01e7bdc90391de92bf95  specs/002-roadmap-brief/quickstart.md
59ea783ed08ad12ddc8ee452bec0aa268bad06ee  specs/002-roadmap-brief/research.md
abfd53be33faca3ce2e47e5370b448c35c4efec4  specs/002-roadmap-brief/roadmap-reviews/brief-2026-06-24.md
eb021c9a2c126f7a2ad944c650c241bdbee3045b  specs/002-roadmap-brief/roadmap-reviews/brief-2026-06-24T19.md
dda447e301ec20e0aaf176c90a0843d5f434f05d  specs/002-roadmap-brief/roadmap-reviews/debrief-2026-06-24.md
294e72bd637f5bfff256f0f45829124ed144206e  specs/002-roadmap-brief/spec.md
120e5a7aa7b0572f6b0b3711f3b3e97ad7495ced  specs/002-roadmap-brief/tasks.md
65b8a1c0b665c0ab1bf0698c3f414a79d2b9fdcd  specs/003-roadmap-debrief/checklists/requirements.md
ac31f4d28e4ecfd461069df50eb281e21f5f416e  specs/003-roadmap-debrief/critiques/critique-2026-06-24.md
8b438e210b597334e76c5e52593b63767682466f  specs/003-roadmap-debrief/plan.md
4f67f6097a5978e701b21312c59080dd55946fb5  specs/003-roadmap-debrief/quickstart.md
c80259634957c2771f311fa0c0df950b93853ae7  specs/003-roadmap-debrief/research.md
257e3461e9003efdaaab4e60d19b338524b1dcdf  specs/003-roadmap-debrief/roadmap-reviews/brief-2026-06-24.md
07e5035b4e43e02ae0a423c5f7906383b6a70452  specs/003-roadmap-debrief/roadmap-reviews/debrief-2026-06-24.md
48532db88632ea9614b9a46bdd22a92a135b81d3  specs/003-roadmap-debrief/spec.md
cd75c7108f60446c12ce1e09914a37ba71caf4b5  specs/003-roadmap-debrief/tasks.md
b2ca32b78e8d832ca7a1c95c28dd59dfe4786338  specs/004-roadmap-sync/checklists/requirements.md
d602e362f290428ae17a7946398665852e1de2cc  specs/004-roadmap-sync/critiques/critique-2026-06-24.md
40e36563e3fa35da62e0242e6011d58fa75e9e24  specs/004-roadmap-sync/plan.md
5d184be0c3ae8c7ce478cd0fe1b4f58ab80e71e0  specs/004-roadmap-sync/quickstart.md
60826a17f924532f9d2f625fe62d2fd5e2402794  specs/004-roadmap-sync/research.md
590d24331dcdca8ea2dd7ae2534ed50958401cf6  specs/004-roadmap-sync/roadmap-reviews/brief-2026-06-24.md
ee81e6b1572b4741d1837d97db8ef6a5017cd5be  specs/004-roadmap-sync/roadmap-reviews/debrief-2026-06-24.md
48ffbf733226f4ab26d833af04a141a6ed43542c  specs/004-roadmap-sync/spec.md
7ea6dd68d6a2a70daa02a0ff2c73270455c98a9e  specs/004-roadmap-sync/tasks.md
728c3a94598a5594f1c42b52a759af1bbdd2ac69  specs/005-rename-project-identity/checklists/requirements.md
4ac9a5d3137d3839939d63bb133c53a149d63bd6  specs/005-rename-project-identity/contracts/identity-contract.md
13bb2cbad0a6b29b548d3644228160ccccd6fbc8  specs/005-rename-project-identity/data-model.md
780c458ef86786d67c7c804ae18dadcaa270b0f5  specs/005-rename-project-identity/plan.md
eeb0ea67d584110bba810445d817b926c375580d  specs/005-rename-project-identity/quickstart.md
f9379cdfa75f35ac167795bd75ddf8514ce27bbd  specs/005-rename-project-identity/research.md
92e01523e770eafb7240b5a8382fbeab86cf0c39  specs/005-rename-project-identity/spec.md
12e23b71f6d83628ed75a994e23f61e67b384d4b  specs/005-rename-project-identity/tasks.md
28f318ab0b6dfaa69f611ec4c7a76ef136c1c35c  specs/006-python-script-migration/checklists/requirements.md
ccbef98140255dc308d35d589233869655f4f511  specs/006-python-script-migration/contracts/load-config.schema.json
bd84c775c9b8574f14872fed1df5c3b7fd2aa9ce  specs/006-python-script-migration/contracts/loader-contract.md
e34bfda3218071af8f262dff8f813fd79c4ae707  specs/006-python-script-migration/contracts/roadmap-config.schema.json
b34adf5e3f44d761cfa673ab2e04668b8ef2786a  specs/006-python-script-migration/data-model.md
4037e0f234b6b44d244615dc8bacc3ee2ba51b23  specs/006-python-script-migration/plan.md
47291ded01640c802393efdbd1f81c0baa994643  specs/006-python-script-migration/quickstart.md
8e91e21d032bf76e301eabf34d98c270cffdad86  specs/006-python-script-migration/research.md
658e3b277d590776e5e5afc8405cf3177d51710c  specs/006-python-script-migration/roadmap-reviews/brief-20260831T171500Z.md
9200f318b931ec9191dc2ef5dd05951e081e38ef  specs/006-python-script-migration/roadmap-reviews/brief-20260901T145849Z.md
08105b2e0ffe478c9e8fa31695b5d1c57bb57c14  specs/006-python-script-migration/roadmap-reviews/debrief-20260831T171600Z.md
38909f204b73676b71b32550fdc5a33233337247  specs/006-python-script-migration/roadmap-reviews/debrief-20260901T143917Z.md
259b32a93e75a548ad417a70429cfcbaabe36e36  specs/006-python-script-migration/spec.md
75e296a3926f65e320fecb5df6425968a1448e07  specs/006-python-script-migration/tasks.md
20e1687cbc6dbbd3db60714ee7038014630afc6d  specs/006-python-script-migration/validation-evidence.md
8e7c6b9cf6a1c941093203939113dda02d60b1cb  templates/review-report-template.md
ef98438d85b13694601c89571384d7d02e7b78ad  templates/roadmap-template.md
```
