<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD033 MD041-->
<div align="center"><img src="assets/banner.svg" alt="Flatpak Automatic CLI
Banner" width="450"></div>
<!-- prettier-ignore-end -->

# Changelog

This is the changelog for **Flatpak Automatic**. All notable changes to this
project will be documented in this file.

The used format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.37] - 2026-05-05

### 🐛 Bug Fixes

- _(rpm)_ Use compatible package names for OpenSUSE and AlmaLinux

## [1.5.36] - 2026-05-05

### 🐛 Bug Fixes

- _(rpm)_ Mark example config as configuration file to satisfy rpmlint
- _(rpm)_ Mark example config as noreplace to satisfy rpmlint

### ⚙️ Miscellaneous Tasks

- _(release)_ Bump version to 1.5.36

## [1.5.35] - 2026-05-05

### 🐛 Bug Fixes

- _(ci)_ Resolve OpenSUSE and AlmaLinux installation issues and improve spec
  portability

## [1.5.34] - 2026-05-05

### ⚙️ Miscellaneous Tasks

- Expand distro testing coverage with AlmaLinux, Arch, and OpenSUSE
- Fix Arch Linux package name for bats and expand distro matrix

## [1.5.33] - 2026-05-05

### 🐛 Bug Fixes

- Resolve memory leak in test_config and improve coverage enforcement

## [1.5.32] - 2026-05-04

### 🚀 Features

- Standardize date formatting and mark excluded apps in status view

## [1.5.31] - 2026-05-04

### 🚀 Features

- Expand notification status with desktop and webhook availability checks

## [1.5.30] - 2026-05-04

### 🚀 Features

- Implement Python bytecode cache clearing for installation and reloads

## [1.5.29] - 2026-05-04

### 🚀 Features

- Polish status view, fix CLI formatting, and harden packaging for reliable
  updates

## [1.5.28] - 2026-05-04

### 🐛 Bug Fixes

- Improve updater parsing and update tests to match remote-ls output

## [1.5.27] - 2026-05-04

### 🐛 Bug Fixes

- Resolve update detection by switching to remote-ls and enhance status view
  with timer state

## [1.5.26] - 2026-05-04

### 🚀 Features

- Ensure UPDATE_LIST and LOG_OUTPUT placeholders are correctly replaced in all
  templates

## [1.5.25] - 2026-05-04

### 🚀 Features

- Improve mailx header compatibility and content-type detection

## [1.5.24] - 2026-05-04

### 🐛 Bug Fixes

- Improved mailx parameter usage

## [1.5.23] - 2026-05-04

### 🐛 Bug Fixes

- Improve mail client compatibility for debian/ubuntu (bsd-mailx support)
- Use shutil.which for reliable mail client detection

## [1.5.22] - 2026-05-04

### 🐛 Bug Fixes

- Improve --reload handling by checking service status before signaling

## [1.5.21] - 2026-05-04

### 🐛 Bug Fixes

- Add missing debian dependencies for desktop notifications and parity with rpm

## [1.5.20] - 2026-05-04

### 🐛 Bug Fixes

- Resolve unsigned debian repository and improve metadata generation

### 📚 Documentation

- Comprehensive audit and update of troubleshooting guides and technical
  manifests

### ⚙️ Miscellaneous Tasks

- _(release)_ Bump version to 1.5.19

## [1.5.19] - 2026-05-04

### 📚 Documentation

- Comprehensive audit and update of troubleshooting guides and technical
  manifests

## [1.5.18] - 2026-05-04

### 🚀 Features

- Improve desktop notification filtering and rootless safety

## [1.5.17] - 2026-05-03

### 📚 Documentation

- Link to license in contributing guide
- Simplify resources section in generated index.md via prepare-docs.sh
- Replace prepare-docs.sh with Python script and translate index.md links
- Fix SameFileError in prepare_docs.py and finalize link translations
- Separate generated documentation from source docs folder using build_docs
- Update resource link transformations in prepare_docs.py

### ⚙️ Miscellaneous Tasks

- Commit remaining manual refinements and script updates
- _(release)_ Bump version to 1.5.17-rc4

## [1.5.17-rc4] - 2026-05-03

### 📚 Documentation

- Link to license in contributing guide
- Simplify resources section in generated index.md via prepare-docs.sh

### ⚙️ Miscellaneous Tasks

- Commit remaining manual refinements and script updates

## [1.5.17-rc3] - 2026-05-03

### 📚 Documentation

- Fix banner image paths for sub-pages and refine repo link

## [1.5.17-rc2] - 2026-05-03

### 📚 Documentation

- Refine mkdocs setup and repository page

## [1.5.17-rc1] - 2026-05-03

### 🚀 Features

- _(package)_ Add pyproject.toml following PEP 621 standards
- Unify documentation with MkDocs Material theme and integrate DNF index

### 🐛 Bug Fixes

- _(core)_ Ensure f-string compatibility with Python < 3.12

## [1.5.16-rc2] - 2026-05-03

### 🚀 Features

- _(update)_ Add exclusion list and dual-default configuration for non-root
  users

### 🚜 Refactor

- _(config)_ Implement dual-default loading and XDG skeleton mechanism

## [1.5.16-rc1] - 2026-05-03

### 🚀 Features

- Add --desktop-mode and update desktop file to avoid bash wrapper
- Add CLI parameters for systemd timer management and update documentation

### 🐛 Bug Fixes

- Resolve import errors in tests and satisfy linter
- Restore version tracking and update tbump.toml for modular structure
- Resolve tbump version tracking and linter issues in wrapper
- _(desktop)_ Fix icon flag in notify-send

### 🚜 Refactor

- Split monolithic script into structured Python package

### ⚙️ Miscellaneous Tasks

- _(release)_ Bump version to 1.5.15

## [1.5.15] - 2026-05-02

### 🚀 Features

- Improve branding, asset discovery, and notification logic
- Make documentation package opt-in for RPM and DEB

### 🎨 Styling

- Replace logo with modern software-update icon

## [1.5.15-rc1] - 2026-05-02

### 🚜 Refactor

- Rename icon.svg to logo.svg and improve notification icon discovery

## [1.5.14-rc3] - 2026-05-01

### 🐛 Bug Fixes

- Ci gh-pages checkout and banner.svg

### 📚 Documentation

- Cleared changelog

### 🎨 Styling

- Prevent version string from shifting banner content
- Fix banner centering by using separate text chunks
- Fix banner.svg, save against auto format

### ⚙️ Miscellaneous Tasks

- _(release)_ Bump version to 1.5.14-rc3
- Update gh-pages deployment to use Pull Requests for protected branch

## [1.5.14-rc2] - 2026-05-01

### 🎨 Styling

- Prevent version string from shifting banner content

### 🐛 Bug Fixes

- Resolve RPM build failure and prevent duplicate debian changelogs
- Use standard SemVer hyphen in CHANGELOG.md while preserving tilde for packages

### 📚 Documentation

- Update documentation and tbump configuration for pre-releases

### ⚙️ Miscellaneous Tasks

- Update gh-pages deployment to use Pull Requests for protected branch
- _(release)_ Bump version to 1.5.14-rc1

## [1.5.14-rc1] - 2026-05-01

### 📚 Documentation

- Update documentation and tbump configuration for pre-releases

## [1.5.13] - 2026-05-01

### 🚀 Features

- Integrate git-cliff for automated changelogs and update release workflow

### 🐛 Bug Fixes

- Resolve invisible icons in desktop notifications

### 📚 Documentation

- Update technical manifest and improve desktop launcher UX

### ⚙️ Miscellaneous Tasks

- Bump version to v1.5.13 and cleanup templates
- Manual reversioning after tbump git-cliff changelog switch
- Refine release documentation and metadata script logic

## [1.5.12] - 2026-05-01

### Added

- **UX**: Added "Run as Administrator (Root)" action to
  `flatpak-automatic.desktop` using `pkexec`.

### Changed

- **Docs**: Updated project descriptions across `README.md`, `AGENTS.md`,
  `docs/flatpak-automatic.1`, `rpm/flatpak-automatic.spec.in`, and
  `debian/control` for consistency and accuracy.
- **Core**: Updated the CLI description in `src/flatpak-automatic.py` to align
  with the new project description.
- **Docs**: Major overhaul of `README.md` for better clarity on features,
  non-root execution, and configuration.
- **Docs**: Updated `flatpak-automatic.1` man page to reflect current CLI
  options (`--check-config`, `--reload`), updated configuration paths, and
  non-root execution details.
- **Docs**: Consolidated Technical Manifest in `AGENTS.md` and cleaned up
  redundant documentation in `docs/development.md` and
  `docs/templates/index.html.j2`.
- **Docs**: Major update to the technical manifest in `AGENTS.md`, adding DEB
  support details, multi-channel notification specifics, and updated CI/CD
  requirements.
- **UX**: Improved `.desktop` launcher with a persistent terminal window after
  execution.
- **Fix**: Resolved invisible icons in desktop notifications by using `file://`
  URIs and `image-path` hints for absolute icon paths.
- **SecOps**: Implemented GitHub Private Vulnerability Reporting in
  `.github/SECURITY.md`.

## [1.5.11] - 2026-05-01

### Added

- Automatic detection of Flatpak scope (user vs system) based on user ID.
- User-level state file support in `~/.cache/flatpak-automatic/state.json`.

### Changed

- Improved systemd integration for user-level services by renaming unit files.
- Removed mandatory root privilege check to allow rootless operation.
- Updated `systemctl` commands to respect user/system scope.
- Updated `flatpak-automatic.desktop` and user service to rely on auto-detection
  instead of `--user` flag.
- **CI/CD**: Added `--retry-wait-time` to lychee link checker job and increased
  wait time from 5 to 30 seconds during retries for better chance of retry
  success.

### Fixed

- Fixed bug where `save_state` was called with incorrect arguments.
- Fixed path expansion for user state file.

## [1.5.10] - 2026-04-30

### Changed

- **Security/UX:** Removed `pkexec` from the `.desktop` launcher; GUI execution
  now defaults to non-root `--user` mode for a seamless desktop experience.

### Added

- **Feature:** Added `--user` CLI flag to support non-root user-level Flatpak
  updates.

### Fixed

- **CI/Build:** Replaced the Snap-dependent `chromium-browser` package with the
  official Google Chrome `.deb` binary in the CI pipeline to permanently resolve
  `snapd` execution hangs within containerized runners.

## [1.5.9] - 2026-04-30

### Added

- **UI/UX:** Added XDG `.desktop` entry for GUI application menu integration and
  CLI launch routing.
- **Security/UX:** Wrapped GUI application launcher execution with `pkexec` to
  trigger standard graphical authentication (Polkit) for required privileges.

## [1.5.8] - 2026-04-30

### Changed

- refactor(assets): rename `logo.svg` to `banner.svg` to clarify brand
  architecture
- fix(packaging): update Makefile, RPM spec, and Debian install files to package
  `icon.svg` alongside `banner.svg`
- use source `banner.svg` in image tag of `index.html`

### Added

- feat(assets): introduce 1:1 `icon.svg` for desktop notifications and compact
  elements
- feat(templates): embed 1:1 icon into HTML email template headers for unified
  brand identity
- feat(notifications): wire DBus desktop notifications to utilize the new 1:1
  `icon.svg`

### Fixed

- fix: respect global notification policy

## [1.5.7] - 2026-04-30

### Changed

- **Design/UI:** Inlined `logo.svg` directly into the Jinja2 HTML template for
  zero-dependency standalone output.
- **Branding**: Updated the SVG logo with enhanced colors and integrated version
  string to align with the CLI banner.
- **CLI**: Improved terminal output with new colors (`OKPINK`) and refined
  banner layout.
- **Documentation**: Updated the repository index template to use the enhanced
  SVG logo instead of the manual ASCII implementation.
- **CI/CD**: Added `assets/logo.svg` to version tracking in `tbump.toml`.

## [1.5.6] - 2026-04-29

### Changed (Enterprise Standards Hardening)

- **Configuration**: Enforced strict enterprise YAML schema templates for
  `config.default.yaml` and `config.example.yaml` (Type, Description, Default).
- **Documentation**: Updated `docs/development.md` to explicitly outline the
  Shift-Left testing matrix (DBus & Notifications).
- **Documentation**: Synchronized `README.md` to reference the comprehensive QA
  workflow.
- **Core**: Adjusted `flatpak-automatic.py` and tests to work with new
  configuration. Added constructor policy chack to notification classes.
- **Core**: Improved cli banner creation.

### Added

- **Features**: Added mail success and failure html templates.
- **Core**: Added `notification_policy` to yaml configuration files.

### Fixed

- **Style**: Improved cli output and cli banner typo.

## [1.5.5] - 2026-04-29

### Added

- Added `--check-config` and `--reload` CLI directives for configuration
  validation and dynamic hot-reloading via `SIGHUP`.

- Added `--check-config` and `--reload` CLI directives for configuration
  validation and dynamic hot-reloading via `SIGHUP`.

### Changed

- Synchronized `README.md` and `docs/flatpak-automatic.1` man pages with the new
  `--check-config` and `--reload` CLI arguments.

- Refactored mail and notification templates to strictly adhere to Markdown
  standards by moving `Subject` metadata into `config.default.yaml`.

### Fixed

- Resolved desktop UI notification bottleneck on Wayland/GNOME by dynamically
  targeting `DBUS_SESSION_BUS_ADDRESS` via `/run/user/<UID>/bus`.

- Resolved desktop UI notification bottleneck on Wayland/GNOME by dynamically
  targeting `DBUS_SESSION_BUS_ADDRESS` via `/run/user/<UID>/bus`.

## [1.5.4] - 2026-04-29

### Added

- Introduced `config/config.default.yaml` with sane default values to serve as
  the initial configuration.
- Added `config/config.example.yaml` (renamed from `config.yaml.example`) as a
  comprehensive reference for all settings.

### Changed

- Standardized configuration file naming to use `.yaml` extension consistently.

### Fixed

- Improved `Makefile` linting targets (`lint-shell`, `lint-md`) for better
  robustness.
- Enhanced YAML configuration output in the CLI with preserved key ordering and
  better indentation.

## [1.5.3] - 2026-04-28

### Added

- **Config**: Introduced Universal State-Resolution (success vs failure) for all
  hierarchical notification fields (`title` and `body_template`), natively
  parsing flat strings or dictionaries.

- **Config**: Introduced hierarchical resolution for `title` and `body_template`
  fields in `notification_groups`. Allows for distinct subjects and templates
  per notification target (Mail, Webhook, Apprise).
- **Config**: Added a Minimal example configuration block to
  `config.yaml.example`.

### Changed

- **Core**: Overhauled `NotificationRouter.dispatch_all` to support cascading
  templates and titles from specific targets up to the group level.

## [1.5.2] - 2026-04-28

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- **Config**: Full schema migration to `config.yaml`. Nesting support added for
  `timer`, `snapshots`, and advanced `notification_groups`.
- **Config**: Deprecated flat variables in `/etc/sysconfig/flatpak-automatic` in
  favor of grouped YAML keys.

## [1.5.1] - 2026-04-27

### Added

- Restored direct Mail and Webhook integrations supporting legacy
  `mailx`/`s-nail` and pure HTTP POST webhooks with HMAC-SHA256 signatures.
- Updated YAML configuration to support global and group-specific `mail` and
  `webhooks` blocks.
- Native YAML configuration routing supporting notification groups and
  Markdown/Text template bodies.
- Added customizable default and minimal notification templates.
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.
- Improved documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- Deprecated `/etc/sysconfig/flatpak-automatic` in favor of
  `/etc/flatpak-automatic/config.yaml`.
- Renamed configuration key `FLATPAK_AUTO_UPDATE` to `AUTO_UPDATE`.

### Removed

- Interactive `--setup` wizard functionality (replaced by default template
  distribution).

## [1.5.0] - 2026-04-27

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **Core**: Implemented `os.geteuid() == 0` guard to gracefully enforce `sudo`
  execution.
- **Core**: Added `MINIMUM_DELAY_HOURS` configuration parameter to prevent
  update spamming, tracking executions in
  `/var/lib/flatpak-automatic/.last_run`.

### Fixed

- **CI/CD**: Fixed HTML index generation bug where semantic versions (e.g.,
  `1.4.23`) were incorrectly sorted alphabetically below older versions (e.g.,
  `1.4.9`).

## [1.4.23] - 2026-04-27

### Fixed

- **CLI**: Fixed an `AttributeError` during execution by properly registering
  the `--apply-schedule` argument with `argparse`, bypassing formatting-induced
  injection failures.

## [1.4.22] - 2026-04-27

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **CLI**: Introduced the `--apply-schedule` command to dynamically generate
  systemd timer overrides (`TIMER_SCHEDULE`, `TIMER_DELAY`) directly from
  sysconfig.
- **UX/Logging**: Implemented context-aware logging detection. The CLI now
  renders human-readable ANSI outputs in TTY environments and strictly preserves
  JSON structured logging when executed by systemd in the background.

## [1.4.21] - 2026-04-27

### Fixed

- **QA**: Updated `TestMainIntegration` to correctly assert the execution of
  both pre and post Snapper snapshots (`flatpak-automatic-pre` and
  `flatpak-automatic-post`) introduced in the monitoring update.

## [1.4.20] - 2026-04-27

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **CLI**: Introduced `--status` for system monitoring overviews and `--history`
  for tailored journalctl execution history routing.
- **Core**: Added `FLATPAK_EXCLUDES` configuration option to mask specific App
  IDs from being updated automatically.
- **Notifications**: Implemented `DesktopNotifier` DBus class to traverse
  session boundaries and send native OS UI notifications to the active user's
  graphical session.

## [1.4.19] - 2026-04-27

### Fixed

- **QA**: Patched `sys.argv` in integration tests to prevent `argparse` from
  consuming `pytest` arguments and throwing an `unrecognized arguments`
  SystemExit.

## [1.4.18] - 2026-04-27

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **CLI**: Implemented the robust `argparse` router, introducing `--dry-run`,
  `--test-notify`, `--force`, and `--help` flags.
- **Documentation**: Updated `README.md` to detail new CLI interaction modes.

## [1.4.17] - 2026-04-26

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **Architecture**: Migrated application core to `src/`, consolidated
  environment templates to `config/`, and segregated CI/CD utilities into
  `scripts/build/` and `scripts/maintainer/`.

### Fixed

- **UX/UI**: Resolved WCAG 2.1 AA contrast violations in the web repository
  index and CLI banner by adopting darker, accessible gradient stops.
- **Style**: Fixed svg logo intention mismatch.

## [1.4.16] - 2026-04-26

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **Refactor**: Reorganized repository structure by moving documentation to
  `docs/` and repository management scripts to `scripts/`.
- **Refactor**: Consolidated `generate-index.py` and its template into
  `scripts/` and `docs/templates/` respectively.
- **Documentation**: Updated all internal links and SVG logo paths to reflect
  the new repository structure.
- **Packaging**: Updated RPM spec file to include new documentation paths and
  correct file locations.

## [1.4.15] - 2026-04-26

### Fixed

- **UX/UI**: Fixed a Markdown rendering bug where invisible ANSI escape
  characters (`\x1b`) stranded by previous string replacements caused the SVG
  header HTML block to render as plain text in `README.md`.

## [1.4.14] - 2026-04-26

### Fixed

- **UX/UI**: Replaced GitHub-incompatible Markdown ANSI escape sequences with a
  universally rendering SVG gradient banner (`assets/logo.svg`) to ensure
  cross-platform brand integrity.

## [1.4.13] - 2026-04-26

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **UX/UI**: Replaced traditional SVG logos and plain text headers in
  `README.md` and repository web index with the CLI-native ASCII gradient banner
  for strict brand consistency.

## [1.4.12] - 2026-04-26

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **UX/UI**: Refactored CLI execution banner to use a compact, multicolored ANSI
  gradient.
- **UX/UI**: Redesigned SVG logo for strict inline typography alignment.
- **UX/UI**: Updated web index and README.md layouts to use mobile-friendly
  inline responsive styling.

## [1.4.11] - 2026-04-26

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **UX/UI**: Introduced project branding with a new vector logo for the
  repository and an ASCII banner for interactive CLI executions.

## [1.4.10] - 2026-04-26

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **Documentation**: Created `MAINTAINERS.md` to consolidate release checklists
  and `tbump` versioning instructions, extracting maintainer processes from
  `DEVELOPMENT.md`.

## [1.4.9] - 2026-04-26

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **Notifications**: Integrated the `apprise` library to support universal
  notifications (Slack, Discord, Telegram, Matrix, etc.) via the
  `FLATPAK_APPRISE_URLS` configuration variable.

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **Core**: Refactored `load_sysconfig()` to use Python's native `shlex` module
  for robust, quote-safe environment variable parsing.

## [1.4.8] - 2026-04-25

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **CI/CD**: Expanded GitOps branch prefixes to include `style`, `test`,
  `revert`, `perf`, `build`, `format`, `deps`, and `sec`.
- **CI/CD**: Hardened CI pipeline by integrating `Bandit` for automated Python
  security linting in pre-commit hooks.
- **Tests**: Expanded core integration tests to verify graceful error
  degradation during D-Bus communication failures.
- **CI/CD**: Integrated `Bandit` SAST scanning into the pipeline to continuously
  monitor for insecure subprocess execution and Python vulnerabilities.
- **Tests**: Expanded Pytest coverage to include the core execution "Happy Path"
  using mocked `dbus` and `subprocess` interfaces.

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **Core**: Migrated standard text logging to structured JSON output using a
  native `JSONFormatter` for improved SIEM observability.
- **CI/QA**: Resolved `mypy` strict type hinting violations in custom logging
  formatter.
- **Documentation**: Refactored `README.md` into a streamlined Quick Start
  Guide.
- **UI/UX**: Delegated DNF/APT repository configuration logic to the hosted
  index page.
- **UI/UX**: Injected mobile-responsive CSS breakpoints to decrease index
  template padding on smaller viewports.
- **CI/CD**: Tuned SAST thresholds to filter expected Low-severity subprocess
  warnings inherent to the wrapper script.
- **QA**: Renamed metadata tests to ensure 1:1 parity with the
  `update-package-metadata.py` script.
- **QA**: Resolved strict `mypy` typing violations in the expanded test suite. -

### Fixed

- **Tests**: Resolved intermittent assertion failures in D-Bus integration tests
  by implementing explicit `dbusmock` process teardown.

## [1.4.7] - 2026-04-25

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **Core**: Migrated daemon to use strict Python type hinting (`mypy`
  compliant).
- **Core**: Transitioned standard output prints to the native `logging` module
  for better `journalctl` integration.
- **CI/CD**: Added integration tests using `dbusmock` to simulate system-bus
  message passing.

## [1.4.6] - 2026-04-24

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **Versioning**: Integrated `tbump` configuration for centralized,
  single-source-of-truth version bumping.

## [1.4.5] - 2026-04-24

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **Systemd**: Standardized service configuration paths by adding dual
  `EnvironmentFile` directives (`/etc/sysconfig` and `/etc/default`) to natively
  support both RPM and Debian-based systems.

## [1.4.4] - 2026-04-24

### Fixed

- **CI/CD**: Added missing `hostname` and `util-linux`/`bsdutils` dependencies
  to the containerized matrix tests to fix `Code 127` script execution failures.

## [1.4.3] - 2026-04-24

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **CI/CD**: Expanded `unit-tests` job in the pipeline to run across a
  containerized matrix (`fedora:latest`, `debian:latest`) to validate core shell
  logic on multiple OS families.

## [1.4.2] - 2026-04-24

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **Repository**: Overhauled Debian APT repository layout to use
  enterprise-standard `pool/` and `dists/` hierarchies via `apt-ftparchive`.
- **Documentation**: Updated `README.md` and repository web index configuration
  to reflect proper `dists/` routing for Debian-based installs.

## [1.4.1] - 2026-04-24

### Refactored

- **Build System**: Decoupled package building and signing logic from `Makefile`
  into dedicated shell scripts (`build-rpm-local.sh`, `sign-rpm.sh`,
  `build-deb-local.sh`) to improve maintainability.

## [1.4.0] - 2026-04-24

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **Core**: Added distro-agnostic mail client detection (`s-nail`, `mailutils`,
  `mailx`) to natively support Debian/Ubuntu email formats.

## [1.3.6] - 2026-04-24

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

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

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **Packaging**: Unified metadata generation for DEB and RPM packaging.
- **Packaging**: Automated `debian/changelog` generation logic.

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **Build System**: Updated `Makefile` DEB target to use native
  `dpkg-buildpackage`.

## [1.3.0] - 2026-04-24

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **Debian Support**: Adapted config path resolution to check
  `/etc/default/flatpak-automatic`.

## [1.2.14] - 2026-04-24

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **Linting**: Integrated `prettier` into pre-commit hooks for native Markdown
  auto-formatting to ensure 1:1 parity with VSCode.

## [1.2.13] - 2026-04-23

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **Documentation**: Added Troubleshooting & Runbook section to `README.md`.
- **Documentation**: Added Mermaid.js execution flow diagram to `AGENTS.md`.

## [1.2.12] - 2026-04-23

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **Testing**: Added BATS testing framework for shell script logic validation.
- **Testing**: Integrated `pytest` to validate Python parsing scripts.
- **CI/CD**: Added `make test` target and integrated it into `pipeline.yml`.

## [1.2.11] - 2026-04-23

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **CI/CD**: Added Ruff (Python) and shfmt (Bash) linting to
  `.pre-commit-config.yaml` and pipeline.
- **CI/CD**: Enforced artifact retention policies (5 days) in `pipeline.yml` to
  prevent storage bloat.
- **Documentation**: Formally documented strict branch protection requirements
  in `AGENTS.md`.

## [1.2.10] - 2026-04-23

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

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

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **CI/CD**: Integrated `pa11y` into the repository site build process to
  enforce WCAG accessibility standards on the generated index page.

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

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

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **Documentation**: Updated CI/CD status badges in `README.md` to reflect the
  new unified `pipeline.yml`.

## [1.2.6] - 2026-04-23

### Fixed

- **CI/CD**: Added missing `python3-pip` dependency to the `build-html-artifact`
  job in the unified pipeline.

## [1.2.5] - 2026-04-23

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **CI/CD**: Unified `ci.yml` and `release.yml` into a single `pipeline.yml` to
  enforce strict artifact promotion. The HTML index is now built once, uploaded
  as an artifact, and downloaded for deployment.

## [1.2.4] - 2026-04-23

### Removed

- **Cleanup**: Permanently removed the obsolete `generate-index.sh` legacy
  script.

## [1.2.3] - 2026-04-23

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **CI/CD**: Switched `release.yml` to use `generate-index.py` with injected
  build metadata and added a pre-deployment `htmlhint` check.

## [1.2.2] - 2026-04-23

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **CI/CD**: Integrated `htmlhint` into GitHub Actions (`ci.yml`) to validate
  the generated `index.html` during pull requests.

## [1.2.1] - 2026-04-23

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **CI/CD**: Added dynamic footer to repository index with build metadata (SHA,
  Run ID, Timestamp).

## [1.2.0] - 2026-04-23

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **Architecture**: Migrated repository index generation from a Bash script to a
  Python/Jinja2 template system for improved separation of concerns and
  maintainability.

## [1.1.9] - 2026-04-23

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **UI/UX**: Constrained RPM package lists within channel `<details>` blocks to
  a max height with an `overflow-y` scrollbar to improve repository index
  scalability.

## [1.1.8] - 2026-04-23

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **UI/UX**: Refactored `generate-index.sh` to dynamically tag the newest
  version folder and patch RPMs as 'LATEST'.
- **UI/UX**: Removed dead directory links for empty channels and replaced them
  with inline indicators.
- **Documentation**: Updated index.html installation instructions to include the
  testing channel.

## [1.1.7] - 2026-04-23

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **UI/UX**: Added native dark mode support (`prefers-color-scheme`) to the
  repository index page.
- **UI/UX**: Enhanced repository index to display collapsible lists of actual
  RPM files using HTML5 `<details>` and `<summary>` tags.

## [1.1.6] - 2026-04-23

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **CI/CD**: Dynamic directory discovery in `generate-index.sh` to track and
  list available versions/channels.

## [1.1.5] - 2026-04-22

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **Bugfix**: Resolved bash heredoc collision in `generate-index.sh` to fix CI
  deployment failure.

- **CI/CD**: Added Lychee automated link checker workflow to validate
  documentation.

- **CI/CD**: Expanded `renovate.json` to enable automerging for minor and patch
  updates on GitHub Actions.

## [1.1.4] - 2026-04-22

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **Bugfix**: Resolved bash heredoc collision in `generate-index.sh` to fix CI
  deployment failure.

- **CI/CD**: Added Lychee automated link checker workflow to validate
  documentation.

- **Documentation**: Synchronized `README.md` and `DEVELOPMENT.md` with the new
  GitHub Pages root URL architecture.

## [1.1.3] - 2026-04-22

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

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

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

- **Bugfix**: Resolved bash heredoc collision in `generate-index.sh` to fix CI
  deployment failure.

- **CI/CD**: Added Lychee automated link checker workflow to validate
  documentation.

- **Consistency**: Replaced legacy `flatpak-auto-update` references with
  `flatpak-automatic` across sysconfig and automation scripts.

## [1.1.1] - 2026-04-22

### Changed

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

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

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

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

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

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

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

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

- **Docs**: Updated `README.md` configuration examples and installation
  instructions to reflect the new nested YAML schema.

- **Core**: Refactored `NotificationRouter` to dynamically parse multi-tenant
  array groupings, nested webhook/mail settings, and local desktop
  notifications.

- Added ANSI color formatting for improved CLI visual hierarchy.
- Implemented execution state caching (`last_try` and `last_success` dates) in
  status view.
- Standardized list indentation across all CLI outputs.
- Enforced trailing empty lines for cleaner terminal UX.

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

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- **Dynamic Subjects:** Email subjects now include the count of updated packages
  using regex parsing.
- **Optimization:** Added a zero-impact dry-run check to prevent unnecessary
  disk writes/snapshots.

### Fixed

- **RPM Build:** Corrected macro path resolution for `LICENSE` and `README.md`
  within the buildroot.

## [1.0.0] - 2026-03-12

### Added

- Added customizable default and minimal notification templates.\n- Improved
  documentation wording replacing generic terms with Ubuntu/Debian and
  Fedora/RHEL.\n
- Added `python3-yaml` (PyYAML) dependency to CI workflows, RPM specs, and
  Debian control files to resolve test failures.

- **Docs**: Authored standard `troff` man pages (`flatpak-automatic.1`),
  configured `Makefile`, `rpm`, and `debian` packaging rules to install it, and
  updated `README.md` with new features.

- **Security**: Resolved CodeQL `py/clear-text-storage-sensitive-data`
  vulnerability by removing secret collection from the `--setup` wizard and
  explicitly enforcing `0600` file permissions on config generation.

- **CLI & UX**: Subclassed `ArgumentParser` to inject persistent, colorized
  gradient branding across all interactive `--help` screens.
- **CLI & UX**: Introduced the `--setup` interactive configuration wizard,
  allowing users to rapidly generate `/etc/sysconfig/flatpak-automatic` without
  manual text editing.

- **Telemetry**: Introduced `WebhookNotifier` allowing pure HTTP POST webhook
  integration with HMAC-SHA256 signature verification (for Datadog, Splunk,
  etc).
- **Notifications**: Hardened `DesktopNotifier` by reading the target user's
  systemd environment to dynamically detect and support pure `WAYLAND_DISPLAY`
  or `DISPLAY` graphical sessions, preventing notification dispatches to
  headless TTY users.

- Initial release with Snapper pre/post snapshot integration.
- Systemd timer and service for daily automation.
- Email reporting via `s-nail/mailx`.
