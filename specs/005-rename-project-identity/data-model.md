# Data Model: Rename Project Identity

This feature has no persisted application data. Its model is the set of identity values that must remain consistent across extension surfaces.

## Project Identity

The project identity represents the human-facing project and its intended source repository.

| Field | Value | Validation |
|---|---|---|
| Display name | `Diagram Roadmap` | Current-facing project documents and manifest use the exact value |
| Repository name | `spec-kit-diagram-roadmap` | Current repository URLs and clone instructions use this path |
| Repository owner | `pegagio` | Existing allowed owner identity remains unchanged |

## Extension Identity

The extension identity controls installation, command namespace validation, and configuration location.

| Field | Value | Validation |
|---|---|---|
| Extension ID | `diagram-roadmap` | Lowercase alphanumeric and hyphen form accepted by Specify |
| Version | `0.2.0` | Valid plain semantic version supported by the manifest schema |
| Installed directory | `.specify/extensions/diagram-roadmap/` | Derived from the extension ID and used by every runtime reference |
| Configuration file | `.specify/extensions/diagram-roadmap/roadmap-config.yml` | Scaffolded during installation |
| Environment prefix | `SPECKIT_DIAGRAM_ROADMAP_*` | Every supported override uses the exact new prefix |

## Command Identity

Each command consists of the required `speckit` prefix, the exact extension ID, and one operation.

| Operation | Canonical command | Source file |
|---|---|---|
| Write | `speckit.diagram-roadmap.write` | `commands/speckit.diagram-roadmap.write.md` |
| Brief | `speckit.diagram-roadmap.brief` | `commands/speckit.diagram-roadmap.brief.md` |
| Debrief | `speckit.diagram-roadmap.debrief` | `commands/speckit.diagram-roadmap.debrief.md` |
| Sync | `speckit.diagram-roadmap.sync` | `commands/speckit.diagram-roadmap.sync.md` |

## Identity transition

The repository transitions from the former active identity to the new identity before `0.2.0` is tagged.

```text
roadmap + speckit.roadmap.* + SPECKIT_ROADMAP_* + .specify/extensions/roadmap/
  -> diagram-roadmap + speckit.diagram-roadmap.* + SPECKIT_DIAGRAM_ROADMAP_* + .specify/extensions/diagram-roadmap/
```

Existing installed configuration remains under the old identity until the user explicitly migrates it. No compatibility alias or automatic state transition is provided.
