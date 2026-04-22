# Changelog

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2026-04-22

### Changed

- **Build System**: Modernized the RPM build process using a `.spec.in` template
  and a centralized `.rpmbuild` directory.
- **Metadata Automation**: Enhanced `update-rpm-metadata.py` to handle epoch,
  release numbers, and Makefile-integrated versioning.

## [1.1.0] - 2026-04-22

### Changed

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

- **Variable Refactoring:** Standardized environment variables to **UPPERCASE**
  (`EMAIL_TO`, `EMAIL_FROM`, etc.).
- **Metadata Sync:** Optimized the `.spec` file to include all new documentation
  in the `%%doc` payload.

## [1.0.2] - 2026-03-29

### Changed

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
