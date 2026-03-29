# Development Guide

This document provides instructions for developers who wish to modify, build, and test **Flatpak Auto Update** locally.

## 🛠 Project Standards

- **Idempotency:** The script must handle "No updates available" gracefully by cleaning up its own pre-update snapshots.
- **Atomic Operations:** Every update attempt must be preceded by a Snapper `pre` snapshot and followed by a `post` snapshot only if changes occurred.
- **Reporting:** Dynamic subjects must follow the format `[hostname] flatpak-auto-update: X new upgrades have been installed.`.
- **Packaging:** All components are managed via the RPM spec file.

## 🏗 Architectural Overview

- **`scripts/`**: Core logic (`flatpak-auto-update.sh`) using `set -euo pipefail`.
- **`systemd/`**: Defines the `oneshot` service and the `daily` timer.
- **`config/`**: Holds the environment-based configuration (`env.conf`).
- **`specs/`**: RPM packaging definition for deployment.

## 📦 Local Development & Packaging

### Prerequisites
Install the Fedora packaging tools:
```bash
sudo dnf install fedora-packager rpm-build shellcheck rpmlint
```

### Build & Install Workflow
1. **Sync sources to `rpmbuild`:**
   ```bash
   cp scripts/flatpak-auto-update.sh ~/rpmbuild/SOURCES/
   cp systemd/flatpak-auto-update.service ~/rpmbuild/SOURCES/
   cp systemd/flatpak-auto-update.timer ~/rpmbuild/SOURCES/
   cp config/env.conf ~/rpmbuild/SOURCES/
   cp README.md ~/rpmbuild/SOURCES/
   cp LICENSE ~/rpmbuild/SOURCES/
   cp specs/flatpak-auto-update.spec ~/rpmbuild/SPECS/
   ```

2. **Build the RPM:**
   ```bash
   rpmbuild -bb ~/rpmbuild/SPECS/flatpak-auto-update.spec
   ```

3. **Install/Update the package:**
   ```bash
   sudo dnf reinstall ~/rpmbuild/RPMS/noarch/flatpak-auto-update-1.0.2-1.*.noarch.rpm
   ```

## 🧪 Testing Logic

### Manual Logic Test
To test the script logic immediately (including snapshots and mail):
```bash
sudo /usr/bin/flatpak-auto-update
```

### Configuration Override
To test different email or snapshot settings without modifying the system config, create a local test file and source it before running:
```bash
export CONFIG_FILE="./test-env.conf"
sudo -E /usr/bin/flatpak-auto-update
```

## ✅ Validation & Linting

Before committing changes, run the following checks:

- **Bash Static Analysis:**
  ```bash
  shellcheck scripts/flatpak-auto-update.sh
  ```
- **Script Syntax Check:**
  ```bash
  bash -n scripts/flatpak-auto-update.sh
  ```
- **RPM Spec Lint:**
  ```bash
  rpmlint specs/flatpak-auto-update.spec
  ```

---
*Maintained by fedoraBee - 2026*
