# Research: FlowKit Roadmap Identity Migration

## Identity and generated names

**Decision**: Use display name `FlowKit Roadmap`, project/repository ID `spec-kit-flow-roadmap`, extension ID `flow-roadmap`, command IDs `speckit.flow-roadmap.{write,brief,debrief,sync}`, and generated skills `speckit-flow-roadmap-{write,brief,debrief,sync}`.

**Rationale**: Specify 1.0.1 generates skill names from command slugs by replacing dots with hyphens and prefixing `speckit-`. The chosen extension ID produces the requested skill spelling. The distinct display, project, and extension identifiers each have one purpose.

**Alternatives considered**: An extension ID of `spec-kit-flow-roadmap` would produce `speckit-spec-kit-flow-roadmap-*` skills. Keeping `diagram-roadmap` as the ID would not deliver the requested command namespace.

## Compatibility and version

**Decision**: Make a clean identity cutover with no command, skill, or environment-variable aliases. Record the rename in the unreleased changelog; retain the current unreleased extension version `0.2.0` during implementation unless packaging evidence requires a release decision.

**Rationale**: The spec explicitly rejects aliases. `v0.1.0` is the only existing Git tag, while `extension.yml` already declares `0.2.0`; changing its number is a release action outside this identity plan. Existing purpose behavior remains unchanged.

**Alternatives considered**: Alias registration would expand the command/hook surface and blur migration completion. A speculative version bump would mix release policy into an unaccepted feature.

## Safe manual installation migration

**Decision**: Back up the old config outside the installed payload. Disable `diagram-roadmap` before adding `flow-roadmap`; install the new extension from a separate source checkout or copy, transfer reviewed values into the new config, then verify effective configuration, commands, skills, and exactly three active new hooks. Only after success, remove `diagram-roadmap` with `--keep-config`. Retain the external backup and the old config retained by Specify. On failed validation, leave the old installation present, disable/remove the new identity as appropriate, and re-enable the old one.

**Rationale**: In pinned Specify 1.0.1, disable keeps the old installation/config but turns off its hooks. Add enables the new identity and hooks, and does not deduplicate against another extension ID. `remove --keep-config` unregisters old hooks, commands, skills, and registry state while retaining supported old config files. The installer copies a `--dev` payload, so source edits require reinstall or an explicit refresh. It rejects installation from the directory that is also the current installed destination. The old README's remove-first migration sequence would violate the new verification gate.

**Alternatives considered**: Add-first risks duplicate hooks. Remove-first sacrifices rollback. Editing `.specify/extensions/.registry` or generated skills by hand bypasses installer bookkeeping. Relying only on `--keep-config` is insufficient if users have unusual config files or require an independently recoverable backup.

## Configuration namespace

**Decision**: New active config lives at `.specify/extensions/flow-roadmap/roadmap-config.yml` and uses only `SPECKIT_FLOW_ROADMAP_*` environment overrides. Review and transfer each prior non-default value; reject unknown or invalid keys before retiring the old installation. Old override names have no effect on the new extension.

**Rationale**: `scripts/python/load_config.py`, `config-template.yml`, and tests currently encode both the old installed path and override prefix. A one-to-one namespace change makes active configuration inspectable and testable, while explicit review protects user values.

**Alternatives considered**: Reading both old and new override prefixes would be a compatibility alias forbidden by the spec. Automatic config conversion would hide validation and user review.

## Source, package, and dogfood state

**Decision**: Change the authoritative root payload first, including the explicit command allowlist in `.extensionignore`. Validate a clean disposable installation, then migrate the repository's dogfood installation through Specify CLI and inspect its tracked registry and config plus generated skill entries. Compare reviewed source to the installed runtime payload.

**Rationale**: `.extensionignore` names the four old command files; failing to update it can omit renamed commands from the package. `.specify/extensions.yml`, `.specify/extensions/.registry`, and installed `roadmap-config.yml` are tracked project state. Generated skills and much installed payload may be ignored but still affect local execution. Specify owns registry hashes, timestamps, hooks, and generated skills.

**Alternatives considered**: Manually copying files into `.specify/extensions/` or editing registry metadata could leave the CLI and filesystem inconsistent. Assuming `--dev` is a live link would miss snapshot drift.

## Historical and external boundaries

**Decision**: Update current-facing README, metadata, templates, command text, constitution identity, and unreleased changelog. Preserve merged feature records, dated reports, earlier roadmap entries, and released changelog semantics. Treat the GitHub repository rename, configured remote, and extension links as acceptance evidence. Defer local checkout/worktree directory renames until after feature completion so the active Codex task remains attached to its path.

**Rationale**: The constitution's merge-bounded model freezes accepted feature meaning. The current checkout is on `develop`, and another detached worktree exists. Moving the active project path during implementation would disrupt the Codex task, so local directory names are post-feature operational cleanup rather than feature acceptance evidence. The GitHub repository rename and updated URLs remain acceptance gates and are not performed by planning.

**Alternatives considered**: Global substitution would rewrite historical evidence. Treating README links or remote URL text alone as proof of the GitHub rename would overstate acceptance; the maintainer's direct confirmation is recorded in T034.

## Validation scope

**Decision**: Use current Python unit tests, focused identity/installation tests, real disposable Specify installations, and a disposable old-to-new migration with both successful and failed verification paths. Require this feature's validation on macOS; Linux validation is optional, while the extension continues to support both platforms under Constitution V.

**Rationale**: Unit tests alone cannot prove installer-generated command, skill, or hook registration. The migration contract depends on real installer side effects and recoverability. The intended user clarified that Linux execution is not required for this feature's acceptance; that does not change the constitution's Linux support requirement.

**Alternatives considered**: Static string scans alone can miss ignored generated skills and runtime snapshots; a dogfood-only check can pass despite a broken clean install.
