# Flatpak Auto Update

**Flatpak Auto Update** is a system utility for Fedora Linux that automates Flatpak package updates with atomic-like safety using Snapper snapshots and provides detailed email reporting.

---

## 🚀 Overview

This utility ensures your Flatpak applications stay up-to-date without manual intervention. It leverages Btrfs snapshots to provide a safety net, allowing you to roll back easily if an update causes instability.

### Key Features
- **Atomic-like Safety:** Automatically creates Snapper `pre` and `post` snapshots for every update session.
- **Idempotent Execution:** Performs a dry-run check first; if no updates are available, it exits without creating unnecessary snapshots.
- **Detailed Reporting:** Sends success or failure notifications via local mail (`s-nail`/`mailx`).
- **Fully Configurable:** Easily override snapshot commands, mail settings, and even the backup strategy (e.g., using raw `btrfs` commands) via a central configuration file.

---

## 🛠 How It Works

1. **Dry-Run Check:** The script checks for pending updates. If none are found, it cleans up and exits.
2. **Pre-Update Snapshot:** A Snapper `pre` snapshot is created to capture the system state.
3. **Execution:** Updates are applied non-interactively (`flatpak update -y`).
4. **Conditional Finalization:**
   - **Success:** A `post` snapshot is created and linked to the `pre` snapshot; a success email is sent.
   - **Failure:** The "orphan" `pre` snapshot is deleted to save space, and a failure report is emailed for troubleshooting.

---

## 📥 Installation

Install the utility using the generated RPM package:

```bash
sudo dnf install ./flatpak-auto-update-1.0.0-1.noarch.rpm
```

---

## ⚙️ Usage

The utility is managed by a systemd timer for automated daily updates.

### Check the Schedule
To see when the next update check is scheduled:
```bash
systemctl list-timers flatpak-auto-update.timer
```

### Manual Trigger
To run the update check immediately:
```bash
sudo systemctl start flatpak-auto-update.service
```

### View Logs
Review historical output and troubleshooting information:
```bash
journalctl -u flatpak-auto-update.service
```

---

## 🔄 Rollback Instructions

If an update causes issues, you can revert your system state using Snapper.

### 1. Identify Snapshots
List your snapshots to find the relevant IDs:
```bash
sudo snapper list
```
Look for descriptions: `flatpak-auto-update-pre` and `flatpak-auto-update-post`.

### 2. Review Changes (Optional)
Compare the state between the snapshots (replace `100` and `101` with your IDs):
```bash
sudo snapper status 100..101
```

### 3. Undo Changes
Revert the system state to the point before the update:
```bash
sudo snapper undochange 100..101
```

---

## 🔧 Configuration

Settings are managed in `/etc/flatpak-auto-update/env.conf`.

```bash
# Core Configuration
email_from=bot@your-system.local
email_to=admin@example.com

# Feature Toggles
ENABLE_EMAIL=yes
ENABLE_SNAPSHOTS=yes

# Customization
EMAIL_FROM_DISPLAY="Fedora Bot"
SNAPPER_CONFIG="root"

# Advanced: Command Overrides
# You can replace the default Snapper commands with your own (e.g., btrfs subvolume)
# or customize the mail client behavior.
```

---

## 📋 Dependencies

* **flatpak**: Core update management.
* **snapper**: Default snapshot provider (Btrfs recommended).
* **s-nail**: (or mailx) SMTP notification client.
* **systemd**: Service orchestration and scheduling.

---
*License: GPL-3.0-or-later*
*Built for Fedora Linux*
