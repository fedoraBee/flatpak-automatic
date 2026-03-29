# Flatpak Auto Update (Universal RPM Edition)

**Flatpak Auto Update** is a robust system utility for Fedora and RPM-based Linux distributions that orchestrates Flatpak package updates with atomic-like safety using Snapper snapshots and provides intelligent, dynamic email reporting.

---

## 📖 Project Architecture & Vision

This framework is designed to solve the "update-and-forget" challenge for Flatpak-heavy environments by bridging the gap between containerized application management and system-level recovery.

### The "Safety-First" Engineering Pillars:
* **Intelligent State Detection:** Implements **Universal Compatibility** via real-time probe of the host filesystem. If Snapper or Btrfs is unavailable, the engine self-reconfigures into a "Safe-Update" mode to ensure 100% uptime regardless of hardware abstraction.
* **Zero-Waste Logic:** To preserve SSD endurance, the tool executes a `dry-run` analysis. If no updates are pending, the script terminates before a single disk write or snapshot is generated.
* **Dynamic Notification Engine:** The engine parses the transaction buffer to provide high-signal subject lines (e.g., `[hostname] 5 new upgrades installed`), allowing for rapid fleet monitoring.

---

## 🚀 Overview

This utility ensures your Flatpak environment remains current without manual overhead. By leveraging Btrfs snapshots, it creates a reliable "time machine" for your applications. 

### Key Features
* **Atomic-like Safety:** Automatically pairs Snapper `pre` and `post` snapshots for every update session.
* **Universal Logic:** Gracefully degrades on non-Btrfs systems (XFS, EXT4, LVM).
* **Smart Notifications:** Dynamic subject lines based on actual package modification counts.
* **Developer Tooling:** Includes `build-rpm.sh` for rapid RPM generation and testing.

---

## 🛠 Technical Logic Flow (v1.0.3)

1.  **Safety Check:** Verifies Snapper configuration. Disables snapshots if requirements aren't met.
2.  **Zero-Impact Check:** Executes `flatpak update --dry-run`.
3.  **Pre-Update State:** Generates a Snapper `pre` snapshot (if supported).
4.  **Automated Execution:** Applies updates in non-interactive mode (`-y`).
5.  **Change Analysis:** Calculates exactly how many packages were modified.
6.  **Conditional Finalization:** Links `post` snapshot on success or purges orphans on failure.

---

## 📥 Installation

### For Users
Install the latest stable RPM package:
```bash
sudo dnf install flatpak-auto-update-1.0.3-1.*.noarch.rpm
```

### For Developers (Build from Source)
Use the build helper in the project root:
```bash
chmod +x build-rpm.sh
./build-rpm.sh --install --clean
```

---

## ⚙️ Usage

### Check the Schedule
```bash
systemctl list-timers flatpak-auto-update.timer
```

### Manual Trigger
```bash
sudo systemctl start flatpak-auto-update.service
```

---

## 🔧 Configuration

Settings are managed in `/etc/flatpak-auto-update/env.conf`.

```bash
# --- Core Identification ---
EMAIL_FROM="bot@$(hostname)"
EMAIL_TO="admin@example.com"

# --- Feature Toggles ---
ENABLE_EMAIL=yes
ENABLE_SNAPSHOTS=yes  # Set to "no" to force-disable snapshots

# --- Notification Customization ---
EMAIL_FROM_DISPLAY="Fedora Bot"
EMAIL_SUBJECT_SUCCESS="[$(hostname)] flatpak-auto-update: \$UPDATE_COUNT new upgrades have been installed."

# --- Advanced Provider Settings ---
SNAPPER_CONFIG="root"
```

---

## 📋 Dependencies & Compatibility

* **flatpak**: Application management.
* **snapper**: Snapshot orchestration (Optional).
* **mailx/s-nail**: SMTP delivery.
* **systemd**: Scheduling and logging.

*Compatible with Fedora, RHEL, and modern RPM-based distributions.*

---
*License: GPL-3.0-or-later* *Maintained by fedoraBee - 2026*
