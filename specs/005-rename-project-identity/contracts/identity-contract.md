# Contract: Diagram Roadmap Extension Identity

This contract defines the public names and installed locations exposed by the renamed extension.

## Manifest contract

The extension manifest exposes these invariant values:

```yaml
extension:
  id: diagram-roadmap
  name: Diagram Roadmap
  version: 0.2.0
  repository: https://github.com/pegagio/spec-kit-diagram-roadmap
  homepage: https://github.com/pegagio/spec-kit-diagram-roadmap
```

## Command contract

The manifest provides exactly four primary commands and no compatibility aliases:

```text
speckit.diagram-roadmap.write
speckit.diagram-roadmap.brief
speckit.diagram-roadmap.debrief
speckit.diagram-roadmap.sync
```

Lifecycle hooks refer only to these canonical commands.

## Installation contract

Specify installs the reviewed payload beneath:

```text
.specify/extensions/diagram-roadmap/
```

Every command frontmatter path, loader configuration path, and template reference resolves within that directory. Installation scaffolds `roadmap-config.yml` there from `config-template.yml`.

## Configuration contract

The supported environment overrides are `SPECKIT_DIAGRAM_ROADMAP_PATH`, `SPECKIT_DIAGRAM_ROADMAP_ADR_DIR`, `SPECKIT_DIAGRAM_ROADMAP_PRD_GLOBS`, and `SPECKIT_DIAGRAM_ROADMAP_MAX_FINDINGS`. The former `SPECKIT_ROADMAP_*` names are not aliases.

## Packaging contract

The source payload consists only of `extension.yml`, `LICENSE`, `config-template.yml`, four canonical command files, two templates, and the Bash and PowerShell loaders. `.extensionignore` itself and all repository-only content are excluded.

## Migration contract

The source change does not mutate an existing `roadmap` installation. A user migrating an installed copy preserves the former configuration, removes the former extension, installs and enables `diagram-roadmap`, and then deliberately reconciles the preserved configuration into the new directory.
