# Flatpak Automatic

![Flatpak Automatic Logo](assets/logo.svg)

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
Pages for both RPM (Fedora/RHEL) and DEB (Ubuntu/Debian) distributions:

👉 <https://fedorabee.github.io/flatpak-automatic/>

### 1. Add the Repository

**RPM-based:**

```bash
sudo tee /etc/yum.repos.d/flatpak-automatic.repo <<'EOF'
[flatpak-automatic]
name=Flatpak Automatic - Stable
baseurl=https://fedorabee.github.io/flatpak-automatic/rpms/latest/stable/
enabled=1
gpgcheck=1
gpgkey=https://fedorabee.github.io/flatpak-automatic/gpg.key
EOF
```

**DEB-based:**

```bash
KEY="https://fedorabee.github.io/flatpak-automatic/gpg.key"
REPO="https://fedorabee.github.io/flatpak-automatic/debs"
RING="/usr/share/keyrings/flatpak-automatic-archive-keyring.gpg"

curl -fsSL $KEY | sudo gpg --dearmor -o $RING
echo "deb [signed-by=$RING] $REPO stable main" | \
sudo tee /etc/apt/sources.list.d/flatpak-automatic.list
```

### 2. Update Cache & Install

**RPM-based:**

```bash
sudo dnf makecache
sudo dnf install -y flatpak-automatic
```

**DEB-based:**

```bash
sudo apt update && sudo apt install -y flatpak-automatic
```

### 3. Enable the Timer

```bash
sudo systemctl enable --now flatpak-automatic.timer
```

## 🔐 GPG Key

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
- `FLATPAK_APPRISE_URLS`: Comma-separated Apprise URLs for Slack, Discord,
  Gotify, Matrix, etc.
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

## ⚠️ Disclaimer

This is an independent project and not affiliated with Fedora or the Flatpak
project. Use at your own discretion.

## 🔗 Resources

- 🌐 Project Repo: <https://fedorabee.github.io/flatpak-automatic/>
