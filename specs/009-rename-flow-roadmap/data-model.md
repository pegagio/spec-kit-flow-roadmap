# Data Model: FlowKit Roadmap Identity

This feature changes file-backed identities and installation state. It adds no database or new persistent schema.

## Identity record

| Field | Value | Source or relationship |
| --- | --- | --- |
| Display name | `FlowKit Roadmap` | `extension.yml` and current project guidance |
| Project/repository ID | `spec-kit-flow-roadmap` | Repository name, checkout name, and current metadata |
| Extension ID | `flow-roadmap` | `extension.yml`; key for Specify installation and registry |
| Purposes | `write`, `brief`, `debrief`, `sync` | Exactly four command definitions |
| Command IDs | `speckit.flow-roadmap.<purpose>` | Manifest and `commands/` front matter |
| Generated skills | `speckit-flow-roadmap-<purpose>` | Specify 1.0.1 skill generation from command IDs |
| Override namespace | `SPECKIT_FLOW_ROADMAP_*` | Python configuration loader and current guidance |
| Active config | `.specify/extensions/flow-roadmap/roadmap-config.yml` | Installed project configuration |

Validation requires a one-to-one mapping from every purpose to its command file and generated skill. The three existing lifecycle events map to the appropriate renamed commands. There are no old-identity aliases or fifth purpose.

## Installation record

Specify owns the installed extension registry, command registration, hook registration, generated skills, and installed payload. The root repository payload is the reviewed source. A `--dev` installation is a copy and may use a `.specify-dev` cache for generated skill links; it is not a live source mount.

| State | Old `diagram-roadmap` | New `flow-roadmap` | Required evidence |
| --- | --- | --- | --- |
| Initial | Installed and enabled | Absent | Existing config and effective values captured |
| Protected transition | Installed but disabled | Absent | Independent old-config backup readable; old hooks inactive |
| Validation | Installed but disabled | Installed and enabled | New config values reviewed; four commands/skills and three new hooks verified |
| Completed | Removed | Installed and enabled | Old registry/commands/skills/hooks absent; old config backup retained |
| Failed validation | Installed and recoverable | Disabled or removed | Old config intact; old extension can be re-enabled without data loss |

The old installation is removed only after the validation state succeeds. Merely having both identities installed is not a completed migration. `remove --keep-config` preserves supported old config files, but an explicit external backup also protects unusual local files and recovery from mistakes.

## Configuration transfer

The old and new `roadmap-config.yml` files are separate records keyed by extension ID. A maintainer reviews every existing non-default value and maps it into the new config. Unknown keys and invalid values stop transition until resolved. Environment overrides are separate transient inputs; only the new prefix participates in the new loader. A validation failure must not modify or remove the old configuration.

## Historical records and acceptance

The current constitution, README, metadata, and unreleased changelog are current-facing identity records. Merged feature directories, dated reports, earlier roadmap entries, and released changelog entries are historical records whose meaning remains frozen. GitHub repository identity, local checkout/worktree names, and remote URLs are external acceptance evidence; tracked source text cannot prove those operations occurred.
