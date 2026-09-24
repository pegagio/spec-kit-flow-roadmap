# Release Process

This repository releases the `flow-roadmap` extension from an immutable `vX.Y.Z` Git tag. The tag identifies the reviewed source commit; the version in `extension.yml` alone does not constitute a release.

## Release mechanics

Perform these steps in order. Complete the candidate checks in [Release validation](#release-validation) before creating the tag.

1. **Set the version.** Choose a new semantic version. Set `extension.version` in `extension.yml` to `X.Y.Z`. Move the relevant notes from `Unreleased` into a dated `X.Y.Z` entry in `CHANGELOG.md`, including migration or Specify compatibility changes. Keep an `Unreleased` heading for subsequent work. Never reuse a released version for different tagged payload bytes.
2. **Integrate the candidate into `master`.** Review and commit the version and changelog changes with the candidate, then merge the approved changes from `develop` into `master`. From the `master` checkout, record the release commit with `git rev-parse HEAD`. It must include the intended runtime payload, manifest, and changelog.
3. **Validate and approve.** Complete the candidate checks below against that `master` commit. Resolve failures in a new commit, integrate the correction into `master`, and repeat the checks. Have a human review the candidate and its validation evidence.
4. **Create the tag on `master`.** Confirm `git branch --show-current` reports `master`, `git status --porcelain` is empty, and `git tag --list vX.Y.Z` returns nothing. Confirm `git rev-parse HEAD` still equals the reviewed commit, then create an annotated tag with `git tag -a vX.Y.Z HEAD -m "Release vX.Y.Z"`. Confirm `git rev-list -n 1 vX.Y.Z` equals the reviewed commit and `git show vX.Y.Z:extension.yml` declares `X.Y.Z`. Do not move or reuse a release tag; corrections need a new version and tag.
5. **Check the tagged source.** Complete the tagged source check below before handing the tag to the catalog.
6. **Decide publication separately.** Pushing the tag or creating a GitHub Release requires an explicit publication decision. A GitHub Release is optional for the Spec Kit Flow local catalog; the immutable tag is the required source identity.

## Release validation

Record the tested Specify CLI version, candidate commit, checks performed, and results so the reviewer can connect the evidence to the tag. Use a fresh disposable initialized Spec Kit project for each installation check; do not install the extension into its own source checkout.

### Candidate checks, before tagging

1. Run `mise run test` at the candidate commit and resolve failures.
2. Inspect the payload selected by `.extensionignore`. Confirm it contains the intended runtime files and excludes development files, local state, secrets, and host paths.
3. Install the candidate in a disposable project with `specify extension add --dev <candidate-checkout>`. Verify the `flow-roadmap` ID, all four commands and generated skills, three hooks, and scaffolded configuration. Exercise the commands with representative project inputs and review their outputs and write boundaries.

### Tagged source check, after tagging

Create an archive from `vX.Y.Z`, extract it outside the source checkout, and install that extracted source in a fresh disposable project. Repeat the installation and runtime checks against the tagged bytes. If they fail, prepare a corrected version and tag; do not change the existing tag.

Installation and command registration show that the package is usable. Human review of judgment-bearing command output remains a separate acceptance decision.

## Resume development

After the release and any chosen publication, keep the release tag and dated changelog entry unchanged.

1. Return to `develop` with `git switch develop` and merge the released `master` commit into it. Confirm `git merge-base --is-ancestor vX.Y.Z HEAD` succeeds before starting new work.
2. Before changing the runtime payload again, set `extension.version` to a prerelease for the next intended version, such as `0.2.1-dev.0` after `v0.2.0`. Choose the next patch, minor, or major line based on the planned change. Commit this version transition separately so development installs no longer claim the released version.
3. Record new work under `Unreleased` in `CHANGELOG.md`. Move those notes into a dated entry only when preparing the next release candidate.
4. In the development Spec Kit project, refresh the local checkout with `specify extension add --dev <development-checkout> --force` and run the relevant tests as work continues. Keep projects consuming the release tag pinned to that tag.

The prerelease version describes a moving development checkout. Only a reviewed, immutable tag identifies a released payload.
