# Flatpak Automatic

[![CI](https://github.com/fedoraBee/flatpak-automatic/actions/workflows/ci.yml/badge.svg)](https://github.com/fedoraBee/flatpak-automatic/actions/workflows/ci.yml)
[![Release](https://github.com/fedoraBee/flatpak-automatic/actions/workflows/release.yml/badge.svg)](https://github.com/fedoraBee/flatpak-automatic/actions/workflows/release.yml)

Flatpak Automatic provides a secure, configurable, and systemd-native automation
wrapper for Flatpak updates.

It integrates with Snapper to provide atomic-like pre/post update snapshots and
uses systemd timers for reliable, scheduled execution on Fedora and other
RPM-based distributions.

## ✨ Features

- **Automated Updates** – Keeps your Flatpak applications up to date
- **Atomic-like Rollbacks** – Integrates with Snapper/Btrfs for pre/post snapshots
- **Smart Execution** – Dry-run checks prevent unnecessary snapshots and logs
- **Notifications** – Sends update reports via local mail (`s-nail`/`mailx`)
- **Systemd Integration** – Managed via standard oneshot services and timers
- **Configurable** – Easily tune email, snapshot, and scheduling behavior via `/etc/sysconfig/flatpak-automatic`

## 📦 Installation via DNF (Recommended)

Packages are distributed via a dedicated DNF repository hosted on GitHub Pages:

👉 <https://fedorabee.github.io/flatpak-automatic/rpms/>

### 1. Add the Repository

```bash
sudo tee /etc/yum.repos.d/flatpak-automatic.repo <<'EOF'
[flatpak-automatic]
name=Flatpak Automatic - Stable
baseurl=https://fedorabee.github.io/flatpak-automatic/rpms/latest/stable/
enabled=1
gpgcheck=1
gpgkey=https://fedorabee.github.io/flatpak-automatic/rpms/gpg.key

[flatpak-automatic-testing]
name=Flatpak Automatic - Testing
baseurl=https://fedorabee.github.io/flatpak-automatic/rpms/latest/testing/
enabled=0
gpgcheck=1
gpgkey=https://fedorabee.github.io/flatpak-automatic/rpms/gpg.key
EOF
```

### 2. Update Cache & Install

```bash
sudo dnf makecache
sudo dnf install flatpak-automatic
```

### 3. Enable the Timer

```bash
sudo systemctl enable --now flatpak-automatic.timer
```

## 🔐 GPG Key

The GPG key is available at
<https://fedorabee.github.io/flatpak-automatic/rpms/gpg.key>.

Fingerprint:

```text
8D12 D614 9E1E 5E83 29DD E6FD 9B99 A03F 6577 BF59
```

## ⚙️ Configuration

The main configuration file is located at:

```text
/etc/sysconfig/flatpak-automatic
```

Key options include:

- `ENABLE_EMAIL`: Set to `yes` to enable mail notifications.
- `EMAIL_TO`: Recipient for update reports.
- `ENABLE_SNAPSHOTS`: Enable Snapper integration.
- `SNAPPER_CONFIG`: The Snapper configuration to use (default: `root`).

## 💾 Manual Execution

To trigger an update manually:

```bash
sudo flatpak-automatic
```

To monitor the logs of the automated service:

```bash
sudo journalctl -u flatpak-automatic.service -f
```

## 📁 Repository Contents

The package repository contains:

- RPM packages: `flatpak-automatic`
- Repository metadata (`repodata/`)
- GPG signing key

## GitOps PR CLI Tool

The project includes a `scripts/gitops-pr-cli-tool.sh` to automate and enforce
the Pull Request workflow. It ensures version synchronization across the
Makefile, RPM spec, and CHANGELOG.

## 🔗 Resources

- 🌐 DNF Repository: <https://fedorabee.github.io/flatpak-automatic/rpms/>
- 💻 Development: <https://github.com/fedoraBee/flatpak-automatic>

## ⚠️ Disclaimer

This is an independent project and not affiliated with Fedora or the Flatpak project.
Use at your own discretion.
