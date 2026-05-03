<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD033 MD041-->
<div align="center"><img src="assets/banner.svg" alt="Flatpak Automatic CLI
Banner" width="450"></div>
<!-- prettier-ignore-end -->

# [![Pipeline](https://github.com/fedoraBee/flatpak-automatic/actions/workflows/pipeline.yml/badge.svg)](https://github.com/fedoraBee/flatpak-automatic/actions/workflows/pipeline.yml)

**Flatpak Automatic** is a secure, systemd-native automation wrapper for Flatpak
updates. It features Snapper-integrated atomic rollbacks, multi-channel alerting
(Apprise, Mail, Webhooks, Desktop), and supports both system-wide and rootless
user-level execution. Designed for reliability and ease of use, it ensures your
Flatpak environment remains current and resilient.

## ✨ Features

- **Automated Flatpak Updates:** Keep your flatpak applications up-to-date
  seamlessly in the background.
- **Atomic-like Rollbacks:** Integrates with Snapper/Btrfs for pre/post
  snapshots
- **Flexible Notifications:** Multiple delivery methods and formats supported,
  adapting to varying infrastructure needs.
- **Exclusion List:** Prevent specific Flatpaks from updating automatically.
- **Systemd Integration:** Managed via standard oneshot services and timers
- **Smart Execution:** Dry-run checks prevent unnecessary snapshots and logs
- **Dual-Default Configuration:** Separate system and user-level default
  profiles with XDG-compliant overrides and auto-scaffolding.
- **Atomic-like Rollbacks:** Integrates with Snapper/Btrfs for pre/post
  snapshots.
- **Non-Root Execution:** Secure, user-level systemd integration.
- **Desktop Integration:** Native XDG `.desktop` entry included for seamless
  launching from GUI application menus (GNOME, KDE, etc.) with automated
  terminal routing.

## 🚀 Quick Start Guide

Flatpak Automatic is distributed via a dedicated repository hosted on GitHub
Pages for both RPM (Fedora/RHEL) and DEB (Ubuntu/Debian) distributions:

👉 <https://fedorabee.github.io/flatpak-automatic/repository/>

### 1. Add the Repository

**Fedora/RHEL:**

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

**Ubuntu/Debian:**

```bash
KEY="https://fedorabee.github.io/flatpak-automatic/gpg.key"
REPO="https://fedorabee.github.io/flatpak-automatic/debs"
RING="/usr/share/keyrings/flatpak-automatic-archive-keyring.gpg"

curl -fsSL $KEY | sudo gpg --dearmor -o $RING
echo "deb [signed-by=$RING] $REPO stable main" | \
sudo tee /etc/apt/sources.list.d/flatpak-automatic.list
```

### 2. Update Cache & Install

**Fedora/RHEL:**

```bash
sudo dnf makecache && sudo dnf install -y flatpak-automatic
```

**Ubuntu/Debian:**

```bash
sudo apt update && sudo apt install -y flatpak-automatic
```

**Local Development (pip):**

For local development or testing without RPM/DEB packaging, you can install the
package in editable mode:

```bash
pip install -e ".[test,apprise]"
```

### 3. Enable the Timer

To enable and start the automatic update timer:

```bash
sudo flatpak-automatic --enable-timer
```

To disable and stop the timer:

```bash
sudo flatpak-automatic --disable-timer
```

To run `flatpak-automatic` securely without root privileges, utilize the same
commands without `sudo`:

```bash
flatpak-automatic --enable-timer
```

This ensures updates are handled within the user session, adhering to strict
least-privilege security models.

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
/etc/flatpak-automatic/config.yaml
```

Key options include:

- `auto_update`: Automatically install available updates.
- `exclusions`: List of Flatpak App IDs to exclude from automatic updates.
- `auto_notify`: Notification policy: `always`, `on-change`, `on-failure`, or
  `never`.
- `timer.schedule`: The systemd timer execution schedule (e.g., `daily`,
  weekly`).
- `timer.delay`: Maximum randomized delay for the timer.
- `timer.minimum_delay`: Minimum randomized delay for the timer.
- `snapshots.enabled`: Globally enable or disable Snapper snapshot creation.
- `snapshots.snapper_config`: The Snapper configuration to use (default:
  `root`).
- `snapshots.snapper_descriptions.pre`: Description for pre-update snapshots.
- `snapshots.snapper_descriptions.post`: Description for post-update snapshots.
- `notification_policy.desktop`: Enable/disable desktop notifications.
- `notification_policy.mails`: Enable/disable mail notifications.
- `notification_policy.webhooks`: Enable/disable webhook notifications.
- `notification_policy.apprise`: Enable/disable Apprise notifications.
- `notification_groups`: Defines multiple notification groups with various
  methods (desktop, mail, webhooks, apprise) and their respective settings
  (title, body_template, recipient, URLs, etc.).

For non-root users, local configuration overrides can be placed at:

```text
~/.config/flatpak-automatic/config.yaml
```

(This file is automatically generated from the user default template on the
first run).

## 💾 Manual Execution & CLI

To trigger an update manually or use the advanced CLI:

```text

usage: flatpak-automatic [-h] [-d] [-t] [-f] [-s] [-l] [-a] [-c] [-r]
                         [--desktop-mode] [-e] [-x]

Flatpak Automatic - Advanced Update Automation

options:
  -h, --help            show this help message and exit
  -d, --dry-run         Simulate the update process without applying changes.
  -t, --test-notify     Send a test notification to configured endpoints and exit.
  -f, --force           Force the update process, ignoring safeguards.
  -s, --status          Display system monitoring overview and exit.
  -l, --history         Display recent update history from journalctl and exit.
  -a, --apply-schedule  Apply systemd timer overrides based on config settings.
  -c, --check-config    Validate and print the current configuration, then exit.
  -r, --reload          Send SIGHUP to a running instance to reload its config.
  --desktop-mode        Run in interactive desktop mode (keeps terminal open).
  -e, --enable-timer    Enable and start the systemd timer (auto-scope).
  -x, --disable-timer   Disable and stop the systemd timer (auto-scope).
```

### Architecture & Deployment

`flatpak-automatic` is designed with a dual-architecture model, supporting
simultaneous parallel execution for maximum security and flexibility:

- **System-Wide (Root):** Updates global system flatpaks. Ideal for multi-user
  or enterprise fleet deployments.
- **User-Level (Rootless):** Updates user-specific flatpaks. Recommended as the
  primary, secure default for single-user desktop environments.

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
flatpak-automatic --history
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

## 🔗 Resources

- 📝 [Project Documentation](https://fedorabee.github.io/flatpak-automatic/)
- 🌐 [Repository](https://fedorabee.github.io/flatpak-automatic/repository/)
- 📖 [Technical Manifest](AGENTS.md)
- 🛠 [Development Guide](docs/development.md)
- 🤝 [Contribution Guidelines](.github/CONTRIBUTING.md)
- 📜 [Changelog](CHANGELOG.md)
- 🧑‍💻 [Maintainer's Guide](MAINTAINERS.md)
- 🔒 [Security Policy](.github/SECURITY.md)

## ⚠️ Disclaimer

This is an independent project and not affiliated with Fedora or the Flatpak
project. Use at your own discretion.
