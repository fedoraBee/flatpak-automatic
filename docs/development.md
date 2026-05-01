<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD033 MD041-->
<div align="center"><img src="../assets/banner.svg" alt="Flatpak Automatic CLI
Banner" width="450"></div>
<!-- prettier-ignore-end -->

# Development Notes

This document outlines the development and deployment workflows for the
**Flatpak Automatic** project.

## Building the RPM

To build the RPM package:

```bash
make rpm
```

## Customizing at Build Time

You can override variables during the RPM build:

```bash
rpmbuild -ba rpm/flatpak-automatic.spec --define "OPEN_WEBUI_PORT 8080"
```

## GitOps PR CLI Tool

The project includes a `scripts/gitops-pr-cli-tool.sh` to automate and enforce
the Pull Request workflow. It performs the following checks:

- Branch naming validation.
- Version extraction from branch name.
- Verification that `CHANGELOG.md` contains the version.
- Verification that the RPM spec file's `Version` field is automatically updated
  by `scripts/update-package-metadata.py` from the `Makefile`'s `VERSION`
  variable, and this value is validated.
- Ensure the `Makefile` version is synchronized with the RPM spec and
  `CHANGELOG.md`.
- Automatic PR body generation from commit messages.

### Prerequisites

- **GitHub CLI (`gh`)**: The tool requires the GitHub CLI to be installed and
  authenticated.

Usage:

```bash
./scripts/gitops-pr-cli-tool.sh --target <branch-name> \
  [--base main] \
  [--title "PR Title"] \
  [--message "PR Body"] \
  [--reviewers user1,user2] \
  [--remote origin] \
  [--dry-run]
```

## Git Clean & Switch Tool

A `scripts/git-clean-switch-tool.sh` is provided to safely reset the current Git
branch to a remote source, clean the worktree, and prepare a development branch.
This is useful for quickly synchronizing a development environment to a known
good state.

Usage:

```bash
./scripts/git-clean-switch-tool.sh \
  [--base main] \
  [--target dev] \
  [--backup backup-main-timestamp] \
  [--remote origin] \
  [--dry-run]
```

### Testing Matrix

This project enforces a Shift-Left testing approach.

- **Integration Tests:** Execute `tests/integration_test_dbus.py` for DBus
  validation.
- **Notification Tests:** Execute `tests/test_notifications.py` for UI/UX
  alerting validation.
- **Automation:** The GitOps patcher logic ensures test coverage is maintained
  on all PRs.

## Architectural Standards & Feature Parity

- **Non-Root Execution:** All new features MUST maintain strict compatibility
  with user-level systemd units (`flatpak-automatic-user.service`). Privilege
  escalation is explicitly forbidden unless structurally required by the
  underlying Flatpak API.
- **Notification Routing:** Outputs and alerts must utilize the defined Jinja2
  templates (Desktop, HTML Mail, Markdown, Minimal) to maintain delivery
  flexibility. Do not hardcode notification structures.
