<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD033 MD041-->
<div align="center"><img src="../assets/banner.svg" alt="Flatpak Automatic CLI
Banner" width="450"></div>
<!-- prettier-ignore-end -->

## 🎉 Contributing

Thank you for contributing to **Flatpak Automatic**! This project aims to
provide a secure, configurable, and systemd-native automation wrapper for
Flatpak updates with Snapper integration.

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
npm install -g markdownlint-cli # or markdownlint-cli2
npm install git-cliff
```

### 3. Initialize Pre-Commit Hooks

To catch linting errors before pushing to GitHub, install the pre-commit hooks:

```bash
pre-commit install
# (Optional) Run against all files immediately
pre-commit run --all-files
```

### 4. Project Structure & Standards

- **Core Script**: The main automation logic is in `src/flatpak-automatic.py`.
- **Systemd**: Units are located in `config/systemd/`.
- **Configuration**: Default environment variables are in
  `config/sysconfig/flatpak-automatic`.
- **Packaging**: The RPM spec template and linting configurations are in `rpm/`.
  Debian configs are in `debian/`.

### 5. Testing Your Changes

Before submitting a pull request, you should verify your changes using the
provided `make` targets:

1. **Run All Lints**:

   ```bash
   make lint
   ```

   This includes `shellcheck` for scripts, `rpmlint` for the spec file,
   `markdownlint` for documentation, and Python linting via pre-commit.

2. **Build and Verify RPMs**:

   ```bash
   make lint-rpm
   ```

3. **Local Install Test**:

   ```bash
   # Test local installation to a temporary directory
   make install DESTDIR=./test-install
   ```

### 6. Version Management & Changelog

- **Do NOT Manually Edit Versions or Changelogs**: Version numbers in the
  `Makefile`, RPM specs, and `CHANGELOG.md` are exclusively managed by
  automation (`tbump`).
- **Conventional Commits**: Because the changelog is generated automatically
  during a release, you **must** use
  [Conventional Commits](https://www.conventionalcommits.org/) (e.g.,
  `feat: add email support`, `fix: resolve dbus timeout`). This ensures your
  changes are properly categorized in the final release notes.

## 📬 Submitting a Pull Request

This project enforces a specific workflow for all contributions to ensure
consistency and automated release management.

### 1. Branch Naming Convention

All changes must be developed in a new branch. Branch names MUST follow this
format:

`<type>/v<version>-<short-description>`

Where:

- `<type>`: `feat` | `fix` | `chore` | `refactor` | `docs` | `ci` | `style` |
  `test` | `revert` | `perf` | `build` | `format` | `deps` | `sec`
- `<version>`: Target release version milestone (e.g., `v2.0.0`)
- `<short-description>`: Kebab-case description (e.g., `update-docs`)

Example: `docs/v2.0.0-update-contributing-guide`

### 2. Commit Guidelines

- Use descriptive commit messages following **Conventional Commits**.
- Ensure commits are atomic and address a single concern.
- Commits must not mix refactoring with functional changes.

### 3. Creating a Pull Request (Mandatory GitOps Tool)

Contributors **MUST** use the provided GitOps PR CLI tool for PR creation. This
tool validates branch names, enforces Conventional Commits history, and formats
the PR body.

```bash
# Basic usage
./scripts/maintainer/gitops-pr-cli-tool.sh -b main -t <your-branch-name>

# Example
./scripts/maintainer/gitops-pr-cli-tool.sh -b main -t docs/v2.0.0-update-contributing-guide
```

Manual PR creation via the GitHub UI or `gh pr create` is discouraged as it
bypasses critical project validations.

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the
**GPL-3.0-or-later** license, as specified in the `LICENSE` file.
