# Quickstart: Validate FlowKit Roadmap

This guide is for validation after implementation. It does not perform the external GitHub rename or local checkout/worktree directory renames. Use disposable Spec Kit projects for installation and migration checks. The [identity contract](contracts/identity-contract.md) defines exact names; the [migration contract](contracts/migration-contract.md) defines the transition gates.

## Prerequisites

From the extension repository root, use the pinned toolchain (`mise trust` and `mise install` if needed), and run the existing test suite. Use a separate extension source directory when testing migration from an already installed copy. The required acceptance checks run on macOS. Linux remains a supported runtime platform, and running this validation on Linux is optional.

```sh
mise run test
git diff --check
```

## Clean installation

The following creates a disposable project without changing this repository's dogfood installation. Capture the source and CLI paths before leaving the repository so the pinned executable remains explicit.

```sh
EXTENSION_SOURCE="$(pwd -P)"
SPECIFY_BIN="$(mise which specify)"
SANDBOX_PARENT="$(mktemp -d)"
SANDBOX_PROJECT="$SANDBOX_PARENT/flow-roadmap-check"
"$SPECIFY_BIN" init "$SANDBOX_PROJECT" --non-interactive --ignore-agent-tools --integration codex --integration-options="--skills"
cd "$SANDBOX_PROJECT"
"$SPECIFY_BIN" extension add "$EXTENSION_SOURCE" --dev
"$SPECIFY_BIN" extension list
"$SPECIFY_BIN" extension info flow-roadmap
```

Expect one enabled `flow-roadmap` extension displayed as FlowKit Roadmap, the four exact command IDs and generated skill names in the identity contract, three hook registrations, and `.specify/extensions/flow-roadmap/roadmap-config.yml`. Inspect `.specify/extensions.yml`, `.agents/skills/`, and the installed payload as well as the CLI output. Exercise each command's prerequisite path and each lifecycle hook in the disposable project; each event must dispatch to its intended command once. Compare installed runtime files to the reviewed root source, accounting for intentional installation metadata.

## Existing-installation migration

Start with a separate disposable project containing a configured `diagram-roadmap` installation. Set a non-default value in its config and record its resolved value before transition. The old and new sources must be separate from the installed directory. Review the files and backup destination before running these commands.

```sh
cp -p .specify/extensions/diagram-roadmap/roadmap-config.yml ./diagram-roadmap-config.backup.yml
"$SPECIFY_BIN" extension disable diagram-roadmap
"$SPECIFY_BIN" extension add "$EXTENSION_SOURCE" --dev
```

Inspect the new `.specify/extensions/flow-roadmap/roadmap-config.yml` and transfer reviewed values from the backup. Do not copy unknown keys blindly. Validate effective values through the new loader, then inspect registered commands, generated skills, and hooks. Confirm the old hooks are disabled and only the three new hooks are active. Test an invalid transferred value: validation must stop before removal and leave the old installation and backup available.

For the successful path, remove the old extension only after the checks pass:

```sh
"$SPECIFY_BIN" extension remove diagram-roadmap --keep-config --force
"$SPECIFY_BIN" extension list
test -r ./diagram-roadmap-config.backup.yml
```

Expect the old registry entry, commands, generated skills, and hooks to be absent. Check that an old environment override has no effect on the new loader, while its new-prefix counterpart does. On a failed validation before removal, disable or remove the incomplete new installation and re-enable `diagram-roadmap`; keep the old config and independent backup. Do not run the removal command in that path.

## Dogfood and acceptance

After the disposable checks pass, repeat the reviewed migration on this repository's self-installation using Specify CLI. Inspect the tracked `.specify/extensions.yml`, `.specify/extensions/.registry`, and installed config together with the generated skills and copied payload; run `mise run test` again. Search current-facing source and docs for stale active old names while allowing explicit migration references and protected history.

Verify the external acceptance gate separately: the GitHub repository name, configured `origin` URL, and current extension repository and homepage links must correspond to `spec-kit-flow-roadmap`. Record the evidence; source-file changes alone do not satisfy this gate. Local checkout and worktree directory renames are post-feature follow-up so they do not move the project from under the active Codex task. Do not claim platform acceptance until the required macOS checks have passed; Linux execution is optional.
