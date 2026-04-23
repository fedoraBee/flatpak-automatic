# Changelog

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
