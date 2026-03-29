# Flatpak Auto Update

**Flatpak Auto Update** is a robust system utility for Fedora Linux that orchestrates Flatpak package updates with atomic-like safety using Snapper snapshots and provides intelligent, dynamic email reporting.

---

## 🚀 Overview

This utility ensures your Flatpak environment remains current without manual overhead. By leveraging Btrfs snapshots, it creates a reliable "time machine" for your applications, allowing for granular rollbacks if an update introduces regressions.

### Key Features
- **Atomic-like Safety:** Automatically pairs Snapper `pre` and `post` snapshots for every successful update.
- **Smart Notifications:** Subject lines dynamically include the count of updated packages: `[hostname] flatpak-auto-update: X new upgrades have been installed.`.
- **Optimization-First:** Performs a zero-impact dry-run check. If no updates are found, it exits immediately without touching the disk for snapshots.
- **Enterprise Configurable:** Every aspect—from snapshot cleanup algorithms to mail command strings—can be overridden via a central environment file.

---

## 🛠 Technical Logic Flow (v1.0.2)

1. **Zero-Impact Check:** Executes `flatpak update --dry-run`. If the system is current, the script terminates.
2. **Pre-Update State:** A Snapper `pre` snapshot is generated to secure the current system state.
3. **Automated Execution:** Updates are applied in non-interactive mode (`flatpak update -y`).
4. **Change Analysis:** The script parses the output to calculate exactly how many packages were `Installed`, `Updated`, or `Removed`.
5. **Conditional Finalization:**
   - **On Success:** A `post` snapshot is linked to the `pre` ID. A notification is sent with the dynamic update count.
   - **On Failure:** The "orphan" `pre` snapshot is purged to prevent disk clutter, and a failure report is dispatched.

---

## 📥 Installation

Install the utility using the generated RPM package:

```bash
sudo dnf install ~/rpmbuild/RPMS/noarch/flatpak-auto-update-1.0.2-1.*.noarch.rpm
```

---

## ⚙️ Usage

The utility is managed by a systemd timer for automated daily maintenance.

### Check the Schedule
To see the next scheduled execution:
```bash
systemctl list-timers flatpak-auto-update.timer
```

### Manual Trigger
To initiate an update check and snapshot cycle immediately:
```bash
sudo systemctl start flatpak-auto-update.service
```

### View Logs
Monitor real-time progress or troubleshoot issues:
```bash
journalctl -u flatpak-auto-update.service -f
```

---

## 🔄 Rollback Instructions

If an update causes application instability, revert the changes using Snapper.

### 1. Identify Snapshot Pair
List snapshots to find the specific update window:
```bash
sudo snapper list
```
Identify the IDs for `flatpak-auto-update-pre` and `flatpak-auto-update-post`.

### 2. Undo Changes
Revert the filesystem to the "Pre" state (replace `100` and `101` with your actual IDs):
```bash
sudo snapper undochange 100..101
```

---

## 🔧 Configuration

Settings are managed in `/etc/flatpak-auto-update/env.conf`. This file supports dynamic variable evaluation.

```bash
# --- Core Identification ---
EMAIL_FROM="bot@$(hostname)"
EMAIL_TO="admin@example.com"

# --- Feature Toggles ---
ENABLE_EMAIL=yes
ENABLE_SNAPSHOTS=yes

# --- Notification Customization ---
EMAIL_FROM_DISPLAY="Fedora Bot"
# Subject lines support $UPDATE_COUNT and $(hostname)
EMAIL_SUBJECT_SUCCESS="[$(hostname)] flatpak-auto-update: \$UPDATE_COUNT new upgrades have been installed."

# --- Advanced Provider Settings ---
SNAPPER_CONFIG="root"
SNAPPER_DESC_PRE="flatpak-auto-update-pre"

# --- Command Overrides (Expert Use Only) ---
# MAIL_CMD="mailx -S sendwait ..."
```

---

## 📋 Dependencies

* **flatpak**: Application lifecycle management.
* **snapper**: Btrfs snapshot orchestration.
* **s-nail** (or mailx): SMTP notification delivery.
* **systemd**: Service scheduling and logging.

---
*License: GPL-3.0-or-later* *Maintained by fedoraBee - 2026*
