# Development Notes

## Building the RPM

To build the RPM package:

```bash
make rpm
```

This generates the following packages in `.rpmbuild/RPMS/noarch/`:

- `flatpak-automatic`: Core configuration.
- `flatpak-automatic-user`: Rootless deployment.
- `flatpak-automatic-root`: Rootfull deployment.

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
