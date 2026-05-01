<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD033 MD041-->
<div align="center"><img src="assets/banner.svg" alt="Flatpak Automatic CLI
Banner" width="450"></div>
<!-- prettier-ignore-end -->

# [![Pipeline](https://github.com/fedoraBee/flatpak-automatic/actions/workflows/pipeline.yml/badge.svg)](https://github.com/fedoraBee/flatpak-automatic/actions/workflows/pipeline.yml)

**Flatpak Automatic** provides a secure, configurable, and systemd-native
automation wrapper for Flatpak updates.

It integrates with Snapper to provide atomic-like pre/post update snapshots and
uses systemd timers for reliable, scheduled execution on Fedora and other
Fedora/RHEL distributions.

## ✨ Features

- **Automated Updates** – Keeps your Flatpak applications up to date
- **Atomic-like Rollbacks** – Integrates with Snapper/Btrfs for pre/post
  snapshots
- **Smart Execution** – Dry-run checks prevent unnecessary snapshots and logs
- **Notifications** – Sends update reports via local mail (`s-nail`/`mailx`)
- **Systemd Integration** – Managed via standard oneshot services and timers
- **Configurable** – Easily tune email, snapshot, and scheduling behavior via
  `/etc/flatpak-automatic/config.yaml`

## 🚀 Quick Start Guide

Flatpak Automatic is distributed via a dedicated repository hosted on GitHub
Pages for both RPM (Fedora/RHEL) and DEB (Ubuntu/Debian) distributions:

👉 <https://fedorabee.github.io/flatpak-automatic/>

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
/etc/flatpak-automatic/config.yaml
```

Key options include:

- `ENABLE_EMAIL`: Set to `yes` to enable mail notifications.
- `EMAIL_TO`: Recipient for update reports.
- `FLATPAK_APPRISE_URLS`: Comma-separated Apprise URLs for Slack, Discord,
  Gotify, Matrix, etc.
- `SNAPPER_CONFIG`: The Snapper configuration to use (default: `root`).

## 💾 Manual Execution & CLI

To trigger an update manually or use the advanced CLI:

```bash
# Standard manual run
sudo flatpak-automatic

# Simulate an update (Dry-run) without snapshots or changes
sudo flatpak-automatic --dry-run

# Display system health, configuration, and monitoring overview
sudo flatpak-automatic --status

# View recent execution history
sudo flatpak-automatic --history

# Apply timer schedule configuration to systemd
sudo flatpak-automatic --apply-schedule
* `-c`, `--check-config`: Validate and print the current configuration, then exit.
* `-r`, `--reload`: Send SIGHUP to a running instance to reload its config.

# Test notification endpoints (Email, Apprise, Desktop UI)
sudo flatpak-automatic --test-notify

# Force an update (ignoring FLATPAK_AUTO_UPDATE safeguards)
sudo flatpak-automatic --force

# View all commands
flatpak-automatic --help
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
- 📖 [Technical Manifest](AGENTS.md)
- 🛠 [Development Guide](docs/development.md)
- 🤝 [Contribution Guidelines](.github/CONTRIBUTING.md)
- 📜 [Changelog](CHANGELOG.md)
- 🧑‍💻 [Maintainers' Guide](MAINTAINERS.md)

## Development & QA

See `docs/development.md` for our strict testing matrix (DBus & Notifications)
and GitOps patcher workflows.

### Brand Assets

- **`banner.svg`**: The primary logotype/header used in documentation and CLIs.
- **`icon.svg`**: The 1:1 scalable logomark used for desktop notifications and
  compact contexts.

## GUI / Desktop Integration

**Desktop Integration:** Native XDG `.desktop` entry included for seamless
launching from GUI application menus (GNOME, KDE, etc.) with automated terminal
routing.

## Features

- **Automated Flatpak Updates:** Keep your flatpak applications up-to-date
  seamlessly in the background.
- **Flexible Notifications:** Multiple delivery methods and formats supported,
  adapting to varying infrastructure needs.
- **Non-Root Execution:** Secure, user-level systemd integration via
  `flatpak-automatic-user`.
- **Extensive Templating:** Jinja2 powered output formatting for logs and
  notifications.

## Notifications

The system supports various notification types defined in `config/templates/`:

- **Desktop Notifications:** Native desktop popups
  (`default_desktop_success.txt`, `default_desktop_failure.txt`).
- **Mail Delivery:** Rich HTML (`default_mail_success.html`) or standard
  Markdown (`default_mail_failure.md`, `default_mail_success.md`) emails.
- **Standard Logging:** Formatted Markdown logs (`default_success.md`,
  `default_failure.md`).
- **Minimal Text:** Simple, concise text output (`minimal.txt`).

## Non-Root Mode (User-Level Systemd)

To run `flatpak-automatic` securely without root privileges, utilize the
provided user-level systemd units:

```bash
systemctl --user enable flatpak-automatic-user.timer
systemctl --user start flatpak-automatic-user.timer
```

_This ensures updates are handled within the user session, adhering to strict
least-privilege security models._
