"""Frozen legacy extension interface for manual-migration tests."""

from __future__ import annotations

from pathlib import Path
import shutil
import stat

from support import REPOSITORY_ROOT, active_specify_interpreter


LEGACY_MANIFEST = """\
schema_version: '1.0'
extension:
  id: diagram-roadmap
  name: Diagram Roadmap
  version: 0.2.0
  description: Legacy identity fixture for migration tests
  author: pegagio
  repository: https://github.com/pegagio/spec-kit-diagram-roadmap
  license: Apache-2.0
  homepage: https://github.com/pegagio/spec-kit-diagram-roadmap
requires:
  speckit_version: '>=1.0.10.dev0'
provides:
  commands:
    - name: speckit.diagram-roadmap.write
      file: commands/speckit.diagram-roadmap.write.md
      description: Legacy roadmap write fixture
    - name: speckit.diagram-roadmap.brief
      file: commands/speckit.diagram-roadmap.brief.md
      description: Legacy roadmap brief fixture
    - name: speckit.diagram-roadmap.debrief
      file: commands/speckit.diagram-roadmap.debrief.md
      description: Legacy roadmap debrief fixture
    - name: speckit.diagram-roadmap.sync
      file: commands/speckit.diagram-roadmap.sync.md
      description: Legacy roadmap sync fixture
  scripts:
    - name: load-config-python
      file: scripts/python/load_config.py
      description: Resolve the legacy fixture configuration
      executable: true
  config:
    - name: roadmap-config.yml
      template: config-template.yml
      description: Legacy roadmap configuration
      required: false
hooks:
  after_constitution:
    command: speckit.diagram-roadmap.write
    optional: true
    prompt: Run the legacy roadmap write command?
    description: Legacy roadmap write hook
  before_implement:
    command: speckit.diagram-roadmap.brief
    optional: true
    prompt: Run the legacy roadmap brief command?
    description: Legacy roadmap brief hook
  after_implement:
    command: speckit.diagram-roadmap.debrief
    optional: true
    prompt: Run the legacy roadmap debrief command?
    description: Legacy roadmap debrief hook
tags:
  - roadmap
defaults:
  report:
    max_findings: 50
"""

LEGACY_LOADER = """\
\"\"\"Resolve the single configuration value used by the migration fixture.\"\"\"

import json
from pathlib import Path

import yaml

configuration = Path.cwd() / ".specify/extensions/diagram-roadmap/roadmap-config.yml"
values = yaml.safe_load(configuration.read_text(encoding="utf-8")) or {}
print(json.dumps({"max_findings": values["report"]["max_findings"]}))
"""


def create_legacy_extension(destination: Path) -> None:
    """Write a stable old-ID installation surface without depending on Git HEAD."""
    destination.mkdir()
    (destination / "extension.yml").write_text(LEGACY_MANIFEST, encoding="utf-8")
    (destination / "config-template.yml").write_text("report:\n  max_findings: 50\n", encoding="utf-8")
    shutil.copy2(REPOSITORY_ROOT / "LICENSE", destination / "LICENSE")

    commands = destination / "commands"
    commands.mkdir()
    for purpose in ("write", "brief", "debrief", "sync"):
        (commands / f"speckit.diagram-roadmap.{purpose}.md").write_text(
            f"---\nname: speckit.diagram-roadmap.{purpose}\ndescription: Legacy {purpose} fixture\n"
            "scripts:\n  py: .specify/extensions/diagram-roadmap/scripts/python/load_config.py\n"
            f"---\nLegacy {purpose} command for migration tests.\n",
            encoding="utf-8",
        )

    scripts = destination / "scripts" / "python"
    scripts.mkdir(parents=True)
    loader = scripts / "load_config.py"
    loader.write_text(f"#!{active_specify_interpreter()}\n{LEGACY_LOADER}", encoding="utf-8")
    loader.chmod(loader.stat().st_mode | stat.S_IXUSR)
