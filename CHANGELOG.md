# Changelog

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.6] - 2026-04-24

### Changed

- **Repository**: Refactored repository structure to use separate `rpms/` and
  `debs/` subdirectories.
- **Repository**: Moved repository GPG key to `gpg.key` at the root for unified
  access.
- **Web**: Enhanced repository index page to display both RPM and Debian
  packages in distinct sections.
- **CI/CD**: Updated pipeline to handle the new disjunct repository structure
  and ensure proper staging for GitHub Pages.
- **Documentation**: Updated `README.md` and `DEVELOPMENT.md` with new
  installation instructions and repository layout details.

## [1.3.5] - 2026-04-24

### Fixed

- **CI/CD**: Made `smoke-test` filesystem and systemd integrity checks
  distro-aware to properly validate `/etc/default` paths on Debian/Ubuntu.

## [1.3.4] - 2026-04-24

### Fixed

- **Debian**: Fixed malformed syntax in `lintian-overrides` file by removing
  brackets and type specifiers.

## [1.3.3] - 2026-04-24

### Fixed

- **Debian**: Removed essential package `bash` from `Depends`.
- **Debian**: Added machine-readable `debian/copyright` file to comply with
  policy.
- **Debian**: Added `lintian-overrides` to safely ignore man page and bug
  tracker warnings.

## [1.3.2] - 2026-04-24

### Fixed

- **Debian**: Fixed Debian Policy violation by moving sysconfig to
  `/etc/default` in `debian/rules`.
- **Debian**: Aligned maintainer email in auto-generated `debian/changelog` with
  `debian/control`.
- **CI/CD**: Containerized `build-deb` job with `debian:latest` and integrated
  `lintian`.

## [1.3.1] - 2026-04-24

### Added

- **Packaging**: Unified metadata generation for DEB and RPM packaging.
- **Packaging**: Automated `debian/changelog` generation logic.

### Changed

- **Build System**: Updated `Makefile` DEB target to use native
  `dpkg-buildpackage`.

## [1.3.0] - 2026-04-24

### Added

- **Debian Support**: Adapted config path resolution to check
  `/etc/default/flatpak-automatic`.

## [1.2.14] - 2026-04-24

### Added

- **Linting**: Integrated `prettier` into pre-commit hooks for native Markdown
  auto-formatting to ensure 1:1 parity with VSCode.

## [1.2.13] - 2026-04-23

### Added

- **Documentation**: Added Troubleshooting & Runbook section to `README.md`.
- **Documentation**: Added Mermaid.js execution flow diagram to `AGENTS.md`.

## [1.2.12] - 2026-04-23

### Added

- **Testing**: Added BATS testing framework for shell script logic validation.
- **Testing**: Integrated `pytest` to validate Python parsing scripts.
- **CI/CD**: Added `make test` target and integrated it into `pipeline.yml`.

## [1.2.11] - 2026-04-23

### Added

- **CI/CD**: Added Ruff (Python) and shfmt (Bash) linting to
  `.pre-commit-config.yaml` and pipeline.
- **CI/CD**: Enforced artifact retention policies (5 days) in `pipeline.yml` to
  prevent storage bloat.
- **Documentation**: Formally documented strict branch protection requirements
  in `AGENTS.md`.

## [1.2.10] - 2026-04-23

### Added

- **CLI**: Implemented the `--check` (`-c`) argument for manual environment
  validation and health checks.
- **Telemetry**: Replaced standard outputs with `logger` to natively integrate
  with the systemd journal for better troubleshooting.

## [1.2.9] - 2026-04-23

### Fixed

- **CI/CD**: Fixed browser launch failure in `pa11y` by explicitly passing a
  configuration file via the `--config` flag and adding
  `--disable-dev-shm-usage`.
- **CI/CD**: Resolved `pa11y` accessibility audit failure by migrating from the
  deprecated `--chrome-launch-config` CLI flag to a localized `.pa11yrc`
  configuration file.
- **UI/UX**: Adjusted repository index colors (links, badges, footers) to meet
  WCAG 2.1 AA contrast requirements.
- **CI/CD**: Resolved `unknown-key` errors in `rpmlint` by importing the public
  GPG key into the RPM database during the build process.
- **CI/CD**: Injected missing GPG import logic into the `build-web-assets` job
  to successfully sign DNF repository metadata during release tags.

### Added

- **CI/CD**: Integrated `pa11y` into the repository site build process to
  enforce WCAG accessibility standards on the generated index page.

### Changed

- **CI/CD**: Refactored the primary pipeline (`pipeline.yml`) with descriptive
  job naming, structural reorganization, and improved internal documentation.
- **CI/CD**: Moved `rpmlint` execution into the primary build job to resolve
  cryptographic isolation errors, bypassing the need for a standalone linting
  job.

## [1.2.8] - 2026-04-23

### Fixed

- **CI/CD**: Conditionally assigned the `gh-pages` environment to build jobs
  during tag pushes to restore access to environment-scoped GPG secrets.

## [1.2.7] - 2026-04-23

### Changed

- **Documentation**: Updated CI/CD status badges in `README.md` to reflect the
  new unified `pipeline.yml`.

## [1.2.6] - 2026-04-23

### Fixed

- **CI/CD**: Added missing `python3-pip` dependency to the `build-html-artifact`
  job in the unified pipeline.

## [1.2.5] - 2026-04-23

### Changed

- **CI/CD**: Unified `ci.yml` and `release.yml` into a single `pipeline.yml` to
  enforce strict artifact promotion. The HTML index is now built once, uploaded
  as an artifact, and downloaded for deployment.

## [1.2.4] - 2026-04-23

### Removed

- **Cleanup**: Permanently removed the obsolete `generate-index.sh` legacy
  script.

## [1.2.3] - 2026-04-23

### Changed

- **CI/CD**: Switched `release.yml` to use `generate-index.py` with injected
  build metadata and added a pre-deployment `htmlhint` check.

## [1.2.2] - 2026-04-23

### Added

- **CI/CD**: Integrated `htmlhint` into GitHub Actions (`ci.yml`) to validate
  the generated `index.html` during pull requests.

## [1.2.1] - 2026-04-23

### Added

- **CI/CD**: Added dynamic footer to repository index with build metadata (SHA,
  Run ID, Timestamp).

## [1.2.0] - 2026-04-23

### Added

- **Architecture**: Migrated repository index generation from a Bash script to a
  Python/Jinja2 template system for improved separation of concerns and
  maintainability.

## [1.1.9] - 2026-04-23

### Changed

- **UI/UX**: Constrained RPM package lists within channel `<details>` blocks to
  a max height with an `overflow-y` scrollbar to improve repository index
  scalability.

## [1.1.8] - 2026-04-23

### Changed

- **UI/UX**: Refactored `generate-index.sh` to dynamically tag the newest
  version folder and patch RPMs as 'LATEST'.
- **UI/UX**: Removed dead directory links for empty channels and replaced them
  with inline indicators.
- **Documentation**: Updated index.html installation instructions to include the
  testing channel.

## [1.1.7] - 2026-04-23

### Added

- **UI/UX**: Added native dark mode support (`prefers-color-scheme`) to the
  repository index page.
- **UI/UX**: Enhanced repository index to display collapsible lists of actual
  RPM files using HTML5 `<details>` and `<summary>` tags.

## [1.1.6] - 2026-04-23

### Added

- **CI/CD**: Dynamic directory discovery in `generate-index.sh` to track and
  list available versions/channels.

## [1.1.5] - 2026-04-22

### Changed

- **Bugfix**: Resolved bash heredoc collision in `generate-index.sh` to fix CI
  deployment failure.

- **CI/CD**: Added Lychee automated link checker workflow to validate
  documentation.

- **CI/CD**: Expanded `renovate.json` to enable automerging for minor and patch
  updates on GitHub Actions.

## [1.1.4] - 2026-04-22

### Changed

- **Bugfix**: Resolved bash heredoc collision in `generate-index.sh` to fix CI
  deployment failure.

- **CI/CD**: Added Lychee automated link checker workflow to validate
  documentation.

- **Documentation**: Synchronized `README.md` and `DEVELOPMENT.md` with the new
  GitHub Pages root URL architecture.

## [1.1.3] - 2026-04-22

### Changed

- **Bugfix**: Resolved bash heredoc collision in `generate-index.sh` to fix CI
  deployment failure.

- **CI/CD**: Added Lychee automated link checker workflow to validate
  documentation.

- **Build System**: Refactored CI/CD deployment architecture to use a `public/`
  staging directory for GitHub Pages.
- **Documentation**: Overhauled the static `index.html` landing page to provide
  a modern, styled installation guide at the repository root.

## [1.1.2] - 2026-04-22

### Changed

- **Bugfix**: Resolved bash heredoc collision in `generate-index.sh` to fix CI
  deployment failure.

- **CI/CD**: Added Lychee automated link checker workflow to validate
  documentation.

- **Consistency**: Replaced legacy `flatpak-auto-update` references with
  `flatpak-automatic` across sysconfig and automation scripts.

## [1.1.1] - 2026-04-22

### Changed

- **Bugfix**: Resolved bash heredoc collision in `generate-index.sh` to fix CI
  deployment failure.

- **CI/CD**: Added Lychee automated link checker workflow to validate
  documentation.

- **Build System**: Modernized the RPM build process using a `.spec.in` template
  and a centralized `.rpmbuild` directory.
- **Metadata Automation**: Enhanced `update-rpm-metadata.py` to handle epoch,
  release numbers, and Makefile-integrated versioning.
- **CI/CD**: Upgraded GitOps PR tool to v3 with template-aware validation and
  automated rebase logic.
- **Linting**: Removed unused filters.

### Fixed

- **CI/CD**: Updated GitHub workflows and scripts to reflect the new `.rpmbuild`
  directory and `repo` path architecture.

## [1.1.0] - 2026-04-22

### Changed

- **Bugfix**: Resolved bash heredoc collision in `generate-index.sh` to fix CI
  deployment failure.

- **CI/CD**: Added Lychee automated link checker workflow to validate
  documentation.

- **Documentation**: Updated `CONTRIBUTING.md` and `bug_report.md` to align with
  project dependencies (Flatpak, Snapper, systemd) and remove legacy references.
- **Versioning**: Bumped minor version to `1.1.0` to reflect stable
  architectural alignment.

### Fixed

- **Packaging**: Expanded 'pre' to 'pre-update' in the spec description to
  resolve rpmlint spelling warnings.
- **Packaging**: Suppressed rpmlint warnings for missing man pages,
  `incoherent-version-in-changelog`, and empty `%%preun` scriptlets.

## [1.0.3] - 2026-03-29

### Added

- **Build Automation:** Introduced `build-rpm.sh`, a dynamic helper script that
  extracts versioning from the SPEC file and automates the full build lifecycle.
- **Universal Compatibility:** Added filesystem safety checks to automatically
  detect Snapper/Btrfs support. The script now gracefully degrades to
  "Update-Only" mode on non-Btrfs systems.
- **Open Source Governance:** Added `CONTRIBUTING.md` and `DEVELOPMENT.md` to
  establish standards and local setup guides.
- **Fail-Fast Logic:** Integrated `set -euo pipefail` and validation checks for
  reliability.

### Changed

- **Bugfix**: Resolved bash heredoc collision in `generate-index.sh` to fix CI
  deployment failure.

- **CI/CD**: Added Lychee automated link checker workflow to validate
  documentation.

- **Variable Refactoring:** Standardized environment variables to **UPPERCASE**
  (`EMAIL_TO`, `EMAIL_FROM`, etc.).
- **Metadata Sync:** Optimized the `.spec` file to include all new documentation
  in the `%%doc` payload.

## [1.0.2] - 2026-03-29

### Changed

- **Bugfix**: Resolved bash heredoc collision in `generate-index.sh` to fix CI
  deployment failure.

- **CI/CD**: Added Lychee automated link checker workflow to validate
  documentation.

- **Internal Refactor:** Improved shell logic consistency and variable
  validation.
- **Reporting:** Optimized notification logic with late-binding variable
  evaluation.

## [1.0.1] - 2026-03-29

### Added

- **Dynamic Subjects:** Email subjects now include the count of updated packages
  using regex parsing.
- **Optimization:** Added a zero-impact dry-run check to prevent unnecessary
  disk writes/snapshots.

### Fixed

- **RPM Build:** Corrected macro path resolution for `LICENSE` and `README.md`
  within the buildroot.

## [1.0.0] - 2026-03-12

### Added

- Initial release with Snapper pre/post snapshot integration.
- Systemd timer and service for daily automation.
- Email reporting via `s-nail/mailx`.
