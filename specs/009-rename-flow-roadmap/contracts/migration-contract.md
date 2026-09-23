# Manual Migration Contract

## Preconditions

A user has an installed `diagram-roadmap` extension with a readable config. The `flow-roadmap` source is available from a separate directory, because Specify 1.0.1 does not install a dev extension from its own installed destination. Capture the old effective values and make a recoverable config backup outside `.specify/extensions/diagram-roadmap/` before changing registration.

## Ordered transition

1. Disable `diagram-roadmap`, retaining its installation and config while turning off its hooks.
2. Install `flow-roadmap` and inspect the new scaffolded config. Transfer every reviewed non-default value; stop on unknown or invalid values.
3. Verify new effective config, four commands and generated skills, three active new hooks, and absence of simultaneous active old hooks. Confirm behavior in a disposable project before changing the repository's dogfood installation.
4. Remove `diagram-roadmap` with `--keep-config` only after verification. Check its registry entry, commands, skills, and hooks are gone and its old config backup remains readable.

An installation with both extension IDs is a transition state, never evidence of completion. The new ID does not automatically consume or remove the old installation.

## Failure and rollback

If installation or validation fails before step 4, retain the old installation and config. Disable or remove the incomplete `flow-roadmap` installation, then re-enable `diagram-roadmap` if the user needs the old workflow. Do not remove the old extension as part of failure handling. If failure occurs after removal, recover the reviewed config from the independent backup and follow the documented installation procedure; the backup must remain available.

## Acceptance checks

The extension migration is complete only when the new identity passes the [identity contract](identity-contract.md), the old registry and active hooks are absent, the old config backup is readable, and source/installed runtime payloads agree. The separate GitHub repository rename, configured remote, and current extension links are project acceptance checks rather than extension installer side effects. Local checkout/worktree directory renames are deferred until after feature completion to avoid disrupting the active Codex task.
