# Identity Contract

## Public extension interface

The installable manifest identifies one extension and exactly four commands. This excerpt shows the identity fields; the existing manifest's other required fields and three hook events remain present.

```yaml
extension:
  id: flow-roadmap
  name: FlowKit Roadmap
provides:
  commands:
    - name: speckit.flow-roadmap.write
    - name: speckit.flow-roadmap.brief
    - name: speckit.flow-roadmap.debrief
    - name: speckit.flow-roadmap.sync
```

Each `commands/<purpose>.md` equivalent has a front matter `name` matching the manifest. The exact filename may carry the extension namespace, but `.extensionignore` must include all four renamed files in the installable payload. Specify 1.0.1 must generate these skills from the command IDs:

| Purpose | Command | Generated skill |
| --- | --- | --- |
| Write | `speckit.flow-roadmap.write` | `speckit-flow-roadmap-write` |
| Brief | `speckit.flow-roadmap.brief` | `speckit-flow-roadmap-brief` |
| Debrief | `speckit.flow-roadmap.debrief` | `speckit-flow-roadmap-debrief` |
| Sync | `speckit.flow-roadmap.sync` | `speckit-flow-roadmap-sync` |

The existing `after_constitution`, `before_implement`, and `after_implement` hooks each dispatch to their corresponding `flow-roadmap` command once. The reviewed Python runtime payload retains existing JSON and report contracts; this feature changes identity and resolution paths, not purpose semantics.

## Configuration interface

The installed config path is `.specify/extensions/flow-roadmap/roadmap-config.yml`. Existing configuration fields and validation rules remain as defined by `config-template.yml` and `scripts/python/load_config.py`. Environment override names use the `SPECKIT_FLOW_ROADMAP_*` prefix with the same field suffixes as the old implementation. For example, an old `SPECKIT_DIAGRAM_ROADMAP_<FIELD>` input becomes `SPECKIT_FLOW_ROADMAP_<FIELD>` after reviewing that field; the old name does not affect the new loader.

Validation rejects unknown or invalid transferred keys before the old installation is retired. A default-only configuration and a non-default configuration must both resolve correctly from the new path. The loader must not read the old installed path as a fallback.

## Negative contract

A completed migration exposes no `speckit.diagram-roadmap.*` command, no `speckit-diagram-roadmap-*` generated skill, no active old lifecycle hook, and no effect from `SPECKIT_DIAGRAM_ROADMAP_*` variables. Old spellings may remain only as historical records or explicit migration examples.
