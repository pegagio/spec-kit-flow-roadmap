# Validation Evidence: Python Script Migration

This record captures the platform matrix and bounded roadmap-command dogfood required by the feature quickstart. All results are from 2026-08-31 against Specify CLI 1.0.1.

## Platform Matrix

The documented `just test` entrypoint executed the complete Python suite on both supported operating systems.

| Platform | Specify interpreter | Python | PyYAML | Test result | Disposable payload, skills, hooks |
|----------|---------------------|--------|--------|-------------|-----------------------------------|
| macOS 15 arm64 | `~/.local/share/spec-tool-kit/specify-cli/1.0.1/venv/bin/python` | 3.11.16 | 6.0.3 | 77 passed | Passed: exact 11-file payload, four skills, three hooks |
| Ubuntu Linux 26.04 arm64 in Lima | `~/.local/share/mise/installs/pipx-specify-cli/1.0.1/specify-cli/bin/python` | 3.11.16 | 6.0.3 | 77 passed | Passed: exact 11-file payload, four skills, three hooks |

The Linux `mise` run ignored host-level configuration and loaded only this repository's `mise.toml`. The repository Python pin and both active Specify runtimes reported exactly 3.11.16.

## Roadmap Command Dogfood

Each scenario used the refreshed generated skill and ran the installed Python loader's kind-specific validation immediately before roadmap content access.

| Scenario | Generated artifact | Expected outcome | Observed outcome | Mutation boundary |
|----------|--------------------|------------------|------------------|-------------------|
| Write — create | `/tmp/diagram-roadmap-write-dogfood/.specify/memory/roadmap.md`, initial SHA-256 `8f1104245661d23da3d08531576f1498eaa8778926631478d9bc695584d2f1a0` | Create a structurally complete 1.0.0 roadmap from harvested constitution facts and expose genuine gaps | Created 1.0.0 with one planned entry, two governing constraints, and Q1 recorded instead of fabricated | Only the disposable roadmap was created |
| Write — amend | `/tmp/diagram-roadmap-write-dogfood/.specify/memory/roadmap.md`, amended SHA-256 `8a330a8e90ed4f23c680ec007557e25b6003bb754d5ddd6bbff1a16ce1445be1` | Preserve accepted content, record one accepted sequencing decision, update the Sync Impact Report, and bump version | Preserved the entry and description, resolved Q1, transitioned `planned` to `specced`, and bumped 1.0.0 to 1.0.1 with PATCH rationale | Only the disposable roadmap was amended after `roadmap-write` validation |
| Brief | [brief report](roadmap-reviews/brief-20260831T171500Z.md) | Surface entry 009 outcome, scope, dependency, constraints, and pre-implementation drift | Matched by title, resolved dependency 008 as verified, found no drift, and recommended but did not apply `in-progress` | Roadmap and specification unchanged |
| Debrief | [debrief report](roadmap-reviews/debrief-20260831T171600Z.md) | Classify implementation drift and propose status without applying it | Found no outcome, scope, or constraint drift and proposed `verified` after convergence | Roadmap, specification, and implementation unchanged |
| Sync | [sync report](../../.specify/memory/roadmap-sync-20260831T171700Z.md) | Reconcile the complete ledger and propose corrections without applying them | Reported one bounded `status-drift` finding for entry 009 and no orphan, phantom, dependency, or ADR findings | Roadmap and specification directories unchanged apart from the generated report |

The create and amend project was disposable and had no PRD or ADR inputs. Its input constitution explicitly supplied the platform, runtime, and non-destructive governance facts used in the generated roadmap.
