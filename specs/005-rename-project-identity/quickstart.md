# Quickstart: Validate the Renamed Identity

This guide validates the completed identity migration from the renamed GitHub repository and local checkout. It verifies their resulting identity but does not perform either external rename operation.

## Prerequisites

Run from the repository root with Specify CLI 1.0.1 available. Bats and PowerShell are optional and should be used when installed.

## Static checks

Verify formatting, manifest names, command files, and active references:

```bash
git diff --check
find commands -maxdepth 1 -type f -print | sort
rg -n 'diagram-roadmap|speckit\.diagram-roadmap|SPECKIT_DIAGRAM_ROADMAP|spec-kit-diagram-roadmap' extension.yml .extensionignore README.md ORIGINS.md CHANGELOG.md config-template.yml commands scripts templates tests .specify/memory/constitution.md .specify/memory/roadmap.md
```

Expected outcome: current-facing files use the identity contract, and old names appear only in the `Unreleased` migration description or explicitly preserved historical records.

## Disposable installation

Create a temporary Spec Kit project, install this checkout with `--dev`, and enable the new extension ID:

```bash
specify init "$TEMP_PROJECT" --non-interactive --integration codex --integration-options=--skills
cd "$TEMP_PROJECT"
specify extension add --dev "$SOURCE_CHECKOUT"
specify extension enable diagram-roadmap
```

Expected outcome: Specify reports Diagram Roadmap version `0.2.0`, registers the four `speckit.diagram-roadmap.*` commands, and generates four corresponding skills.

## Runtime and payload checks

Run the installed Bash loader and inspect the copied payload:

```bash
.specify/extensions/diagram-roadmap/scripts/bash/load-config.sh | python3 -m json.tool
find .specify/extensions/diagram-roadmap -type f -print | sort
```

Expected outcome: the loader emits valid JSON and the installed files match the packaging contract plus the generated `roadmap-config.yml` scaffold.

## Platform suites

Run every locally available suite:

```bash
bats tests/bash/load-config.bats
bats tests/parity/parity.bats
pwsh -NoProfile -Command "Invoke-Pester -Path tests/powershell/load-config.Tests.ps1"
```

If Bats or PowerShell is unavailable, record that limitation and retain the disposable installation and syntax checks as the verified local evidence.
