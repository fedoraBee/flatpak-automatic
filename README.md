# Flatpak Automatic

[![Pipeline](https://github.com/fedoraBee/flatpak-automatic/actions/workflows/pipeline.yml/badge.svg)](https://github.com/fedoraBee/flatpak-automatic/actions/workflows/pipeline.yml)

Flatpak Automatic provides a secure, configurable, and systemd-native automation
wrapper for Flatpak updates.

It integrates with Snapper to provide atomic-like pre/post update snapshots and
uses systemd timers for reliable, scheduled execution on Fedora and other
RPM-based distributions.

## ✨ Features

- **Automated Updates** – Keeps your Flatpak applications up to date
- **Atomic-like Rollbacks** – Integrates with Snapper/Btrfs for pre/post
  snapshots
- **Smart Execution** – Dry-run checks prevent unnecessary snapshots and logs
- **Notifications** – Sends update reports via local mail (`s-nail`/`mailx`)
- **Systemd Integration** – Managed via standard oneshot services and timers
- **Configurable** – Easily tune email, snapshot, and scheduling behavior via
  `/etc/sysconfig/flatpak-automatic`

## 🚀 Quick Start Guide

Flatpak Automatic is distributed via a dedicated repository hosted on GitHub
Pages for both RPM (Fedora/RHEL) and DEB (Ubuntu/Debian) distributions.

👉
**[View Full Installation & Repository Setup Instructions](https://fedorabee.github.io/flatpak-automatic/)**

### General Setup Flow

1. **Configure Repository:** Add the DNF or APT repository using the commands
   provided on the project website.
2. **Install Package:** `sudo dnf install flatpak-automatic` OR
   `sudo apt install flatpak-automatic`
3. **Enable Automation:** Activate the systemd timer:

   ```bash
   sudo systemctl enable --now flatpak-automatic.timer
   ```

## 🔐 Security & GPG

The GPG key is available at
<https://fedorabee.github.io/flatpak-automatic/gpg.key>.

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

- RPM packages: `flatpak-automatic` (in `/rpms`)
- Debian packages: `flatpak-automatic` (in `/debs`)
- Repository metadata
- GPG signing key (`gpg.key`)

## GitOps PR CLI Tool

The project includes a `scripts/gitops-pr-cli-tool.sh` to automate and enforce
the Pull Request workflow. It ensures version synchronization across the
Makefile, RPM spec, and CHANGELOG.

## 🔗 Resources

- 🌐 Project Website & Repo: <https://fedorabee.github.io/flatpak-automatic/>
- 💻 Development: <https://github.com/fedoraBee/flatpak-automatic>

## ⚠️ Disclaimer

This is an independent project and not affiliated with Fedora or the Flatpak
project. Use at your own discretion.

## Troubleshooting & Runbook

If you encounter issues with `flatpak-automatic`, follow these steps to diagnose
and resolve them:

### 1. Viewing Logs

Since the script integrates natively with systemd, the best place to check for
failures or warnings is the system journal:

```bash
journalctl -u flatpak-automatic.service -e
```

### 2. Snapper Config Errors

If the health check reports `FAIL: snapper config 'root' is invalid or missing`,
you need to initialize a Snapper configuration for your root filesystem:

```bash
sudo snapper -c root create-config /
```

### 3. Email/Mailx Authentication Failures

If you have `ENABLE_EMAIL=yes` but are not receiving notifications, check your
`s-nail` configuration. The mail client relies on `/etc/mail.rc`. Ensure your
SMTP server, port, and authentication credentials are set up correctly.

### Debian / Ubuntu (APT)

```bash
KEY="https://fedorabee.github.io/flatpak-automatic/gpg.key"
REPO="https://fedorabee.github.io/flatpak-automatic/debs"
RING="/usr/share/keyrings/flatpak-automatic-archive-keyring.gpg"

curl -fsSL $KEY | sudo gpg --dearmor -o $RING
echo "deb [signed-by=$RING] $REPO stable main" | \
sudo tee /etc/apt/sources.list.d/flatpak-automatic.list
sudo apt update && sudo apt install -y flatpak-automatic
```
