# Flatpak Automatic: Technical Manifest

Flatpak Automatic is a secure, configurable, and systemd-native automation
wrapper for Flatpak updates. It integrates Snapper for atomic-like rollbacks and
systemd for reliable scheduling on Fedora and other RPM-based distributions.

## 🏗 Architectural Overview

The project is structured as a single RPM package providing the following
components:

### 1. Automation Script (`/usr/bin/flatpak-automatic`)

- **Update Logic**: Handles the `flatpak update` process with dry-run checks to
  avoid unnecessary operations.
- **Snapshot Integration**: Automatically creates Snapper pre/post snapshots if
  Btrfs and Snapper are detected.
- **Notification System**: Sends update reports via local mail
  (`s-nail`/`mailx`).

### 2. Systemd Integration

- **Timer (`flatpak-automatic.timer`)**: Manages the daily execution schedule
  with randomized delays to prevent server congestion.
- **Service (`flatpak-automatic.service`)**: A `oneshot` service that executes
  the automation script with proper environment configuration.

### 3. Configuration

- **Sysconfig (`/etc/sysconfig/flatpak-automatic`)**: Holds environment-based
  configuration for email alerts, snapshot behavior, and Snapper settings.

## 🛠 Project Standards

- **Idempotency**: The update script handles "No updates available" gracefully
  by cleaning up its own pre-update snapshots.
- **Atomic Operations**: Every update attempt is preceded by a Snapper `pre`
  snapshot and followed by a `post` snapshot only if changes occurred.
- **Configuration Persistence**: The `/etc/sysconfig/flatpak-automatic` file is
  marked as `noreplace` to preserve user overrides during package updates.
- **Automated Changelog**: The RPM changelog is generated from `CHANGELOG.md`
  using `scripts/update-rpm-metadata.py` and included in the spec file via
  `%include %{_topdir}/changelog`.
- **Markdown Linting**: All changes to Markdown files (`.md`) must adhere to the
  project's Markdown linting rules, especially MD013 to prevent line length
  overflows.
- **Language Standard**: Always use English when editing any project files,
  including code, comments, and documentation.

## 🚀 Deployment Workflow

To deploy changes locally for testing:

1. **Build the RPM:** `make rpm`
2. **Generate Repo:** `make rpm-repo CHANNEL=testing`
3. **Update Local Repo:** `cp -r repo/ ../dnf-repos/flatpak-automatic/`
4. **Install/Reinstall:**
   `sudo dnf reinstall -Cy ../dnf-repos/flatpak-automatic/latest/testing/*.rpm`
5. **Start Timer:** `systemctl enable --now flatpak-automatic.timer`

## 🤖 CLI Guidelines

- **Self-Correction**
  After modifying `AGENTS.md`, immediately re-read it to ensure the active
  context reflects the latest project guidelines.

- **Professionalism**
  Maintain high engineering standards. Write clean, idiomatic code, communicate
  clearly, and verify all changes before completion.

- **Branching Strategy (Mandatory)**
  All features, bug fixes, and other changes must be developed in a new branch.
  Never commit directly to `main`. Branch protection rules MUST be configured on
  `main` to require status checks (`lint-code`, `lint-python`, `lint-spec`,
  `build-packages`, `smoke-test`) and mandatory Pull Requests.

  Branch names must follow:

  `<type>/v<version>-<short-description>`

  Where:

  - `<type>`: feat | fix | chore | refactor | docs | ci
  - `<version>`: target release version

- **Pull Request Workflow (Mandatory)**
  Each branch must open a descriptive Pull Request (PR).

  PR creation MUST be performed using the GitOps PR CLI tool provided in this
  repository (located at scripts/gitops-pr-cli-tool.sh).

- **CI Requirements**
  All Pull Requests must pass CI checks before merging. This includes:

  - markdownlint
  - shellcheck
  - lint-python
  - shfmt
  - rpmlint
  - RPM build and smoke tests

- **Atomic Commits**
  Commit frequently with small, logical, atomic changes.

- **Testing**
  Thoroughly test all changes before committing:

  - Build RPMs using `make rpm`
  - Verify systemd integration and timer scheduling
  - Validate scripts and error handling

- **Verification**
  After modifying the RPM spec or Makefile:

  - Verify file paths
  - Validate installation logic
  - Ensure resulting RPM behaves as expected

- **Documentation**
  Keep documentation consistent and up to date:

  - Update `DEVELOPMENT.md` for build steps and prerequisites
  - Update `README.md` for installation and user-facing changes

  **Changelog (Mandatory)**

  For every feature, fix, or release:

  - Update `CHANGELOG.md` using the "Keep a Changelog" format.
  - The `CHANGELOG.md` is the **single source of truth** for release notes.

- **Versioning Discipline**
  Any version bump (including patch releases) must be synchronized across:

  - `Makefile` (`VERSION` variable)
  - `rpm/flatpak-automatic.spec` (`Version` field - automatically updated by
    `scripts/update-rpm-metadata.py` from `Makefile`)
  - `CHANGELOG.md` (New version heading)

- **Script Requirements**
  All scripts must be:

  - Idempotent
  - Safe to re-run
  - Failure-tolerant with proper error handling

## 📦 Reference Docs

- [README.md](README.md): Installation and usage guide.
- [CONTRIBUTING.md](CONTRIBUTING.md): Guidelines for contributors.
- [DEVELOPMENT.md](DEVELOPMENT.md): Build instructions and technical notes.
- [CHANGELOG.md](CHANGELOG.md): Record of notable changes and versions.
- [LICENSE](LICENSE): GPL-3.0-or-later.

**Note:** All changes made to this instruction file must also be reflected in
`AGENTS.md`.
