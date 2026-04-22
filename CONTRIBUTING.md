# Contributing to flatpak-automatic

Thank you for contributing! This project aims to provide a secure, configurable,
and systemd-native automation wrapper for Flatpak updates with Snapper
integration.

## 📜 Code of Conduct

By participating in this project, you agree to maintain a professional and
respectful environment. Please report any issues or suggested improvements via
GitHub Issues.

## 🛠 Development Workflow

### 1. Fork and Clone

Fork the repository and clone it to your local machine (Fedora or another
RPM-based distribution is recommended).

### 2. Environment Setup

Ensure you have the necessary development tools installed:

```bash
sudo dnf install make rpm-build flatpak snapper systemd-devel \
  rpmlint shellcheck pre-commit
# Install markdownlint-cli or markdownlint-cli2 globally via npm
sudo npm install -g markdownlint-cli # or markdownlint-cli2
```

### 3. Initialize Pre-Commit Hooks

To catch linting errors before pushing to GitHub, install the pre-commit hooks:

```bash
pre-commit install
# (Optional) Run against all files immediately
pre-commit run --all-files
```

### 3. Project Structure & Standards

- **Scripts**: The main automation logic is in `scripts/flatpak-automatic.sh`.
- **Systemd**: Units are located in `systemd/`.
- **Configuration**: Default environment variables are in `sysconfig/flatpak-automatic`.
- **Packaging**: The RPM spec and linting configurations are in `rpm/`.

### 4. Testing Your Changes

Before submitting a pull request, you should verify your changes using the
provided `make` targets:

1. **Run All Lints**:

   ```bash
   make lint
   ```

   This includes `shellcheck` for scripts, `rpmlint` for the spec file, and
   `markdownlint` for documentation.

1. **Build and Verify RPMs**:

   ```bash
   make lint-rpm
   ```

   This builds the RPMs and runs `rpmlint` against the resulting packages.

1. **Local Install Test**:

   ```bash
   # Test local installation to a temporary directory
   make install DESTDIR=./test-install
   ```

### 5. Version Management & Changelog

- **Version Synchronization**: When bumping the version, ensure the new version
  is updated in:
  - `Makefile` (`VERSION` variable)
  - `rpm/flatpak-automatic.spec` (`Version` field - automatically updated by
    `scripts/update-rpm-metadata.py` from `Makefile`)
  - `CHANGELOG.md` (New version heading)
- **CHANGELOG.md**: Add a brief note under the current version. This file is the
  single source of truth for release notes. The RPM changelog is automatically
  generated from it.

## 📬 Submitting a Pull Request

This project enforces a specific workflow for all contributions to ensure
consistency and automated release management.

### 1. Branch Naming Convention

All changes must be developed in a new branch. Branch names MUST follow this
format:

`<type>/v<version>-<short-description>`

Where:

- `<type>`: `feat` | `fix` | `chore` | `refactor` | `docs` | `ci`
- `<version>`: Target release version (e.g., `v2.0.0`)
- `<short-description>`: Kebab-case description (e.g., `update-docs`)

Example: `docs/v2.0.0-update-contributing-guide`

### 2. Commit Guidelines

- Use descriptive commit messages following
  [Conventional Commits](https://www.conventionalcommits.org/).
- Ensure commits are atomic and address a single concern.
- Commits must not mix refactoring with functional changes.

### 3. Creating a Pull Request (Mandatory GitOps Tool)

Contributors **MUST** use the provided GitOps PR CLI tool for PR creation. This
tool validates branch names, versions, and changelog entries.

```bash
# Basic usage
./scripts/gitops-pr-cli-tool.sh -b main -h <your-branch-name>

# Example
./scripts/gitops-pr-cli-tool.sh -b main -h docs/v2.0.0-update-contributing-guide
```

Manual PR creation via the GitHub UI or `gh pr create` is discouraged as it
bypasses critical project validations.

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the
**GPL-3.0-or-later** license, as specified in the `LICENSE` file.
