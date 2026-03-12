# Project: Flatpak Auto Update
**Role:** System Utility for Fedora Linux
**Context:** Automates Flatpak updates with Snapper snapshots and email reporting.

## 1. Technical Logic Flow (AI-Context)
- **Dry-Run Check:** Script performs a `flatpak update --dry-run` check first. If no updates are found, it exits immediately, saving system resources and keeping the snapshot timeline clean.
- **Pre-Snapshot:** If updates are pending, script initiates a pre-update snapshot command (default: Snapper `pre`) and captures the ID.
- **Execution:** Runs `flatpak update -y --noninteractive`.
- **Conditionality:**
   - **Success (Updates applied):** Executes the post-update snapshot command (default: Snapper `post`) linked to the `pre` ID; sends an email with the update log.
   - **Failure (Error):** Sends a failure report via email; executes the delete snapshot command to clean up the orphan `pre` snapshot.
- **Extensibility:** All major commands (Mail, Snapper/Snapshot) and email bodies are fully configurable via `env.conf`.

## 2. Installation
Install the utility using the generated RPM package:
```bash
sudo dnf install ./flatpak-auto-update-1.0.0-1.noarch.rpm
```

## 3. Usage
The service is automated via a systemd timer.

### Check the Schedule
To see when the next automatic update check is scheduled:
```bash
systemctl list-timers flatpak-auto-update.timer
```

### Manual Trigger
To force an update check immediately:
```bash
sudo systemctl start flatpak-auto-update.service
```

### View Logs
To review the historical output of the updater:
```bash
journalctl -u flatpak-auto-update.service
```

## 4. Rollback Instructions
If a Flatpak update causes application instability, use your snapshot tool (default: Snapper) to revert the changes.

### Step 1: Identify Snapshots (Snapper Default)
List your snapshots to find the `pre` and `post` IDs:
```bash
sudo snapper list
```
Look for descriptions: `flatpak-auto-update-pre` and `flatpak-auto-update-post`.

### Step 2: Review Changes (Optional)
To see exactly which files were modified (replace `100` and `101` with your actual IDs):
```bash
sudo snapper status 100..101
```

### Step 3: Undo Changes
Revert the system state to the point before the update occurred:
```bash
sudo snapper undochange 100..101
```

## 5. Configuration
Configuration settings are stored in the environment configuration file.

**File:** `/etc/flatpak-auto-update/env.conf`

```bash
# Configuration for flatpak-auto-update
email_from=bot@your-system.local
email_to=admin@example.com

# Optional features (yes/no)
ENABLE_EMAIL=yes
ENABLE_SNAPSHOTS=yes

# Mail settings
EMAIL_FROM_DISPLAY="Fedora Bot"
EMAIL_SUBJECT_SUCCESS="Flatpak Update: Success ($(hostname))"
EMAIL_SUBJECT_FAILURE="SERIOUS: Flatpak Update Failed ($(hostname))"

# Snapper settings
SNAPPER_CONFIG="root"
SNAPPER_DESC_PRE="flatpak-auto-update-pre"
SNAPPER_DESC_POST="flatpak-auto-update-post"

# Advanced Command Overrides (Inclusive parameters)
# The mail command should accept the subject as $1 and recipient as $2. Body via stdin.
MAIL_CMD='mailx -S sendwait -r "$EMAIL_FROM_DISPLAY <$email_from>" -s "$1" "$2"'

# Snapper command overrides
SNAPPER_PRE_CMD='snapper -c "$SNAPPER_CONFIG" create --type pre --description "$SNAPPER_DESC_PRE" --cleanup-algorithm number --print-number'
SNAPPER_POST_CMD='snapper -c "$SNAPPER_CONFIG" create --type post --pre-number "$PRE_NUM" --description "$SNAPPER_DESC_POST"'
SNAPPER_DELETE_CMD='snapper -c "$SNAPPER_CONFIG" delete "$PRE_NUM"'

# Example: Using btrfs instead of snapper
# SNAPPER_PRE_CMD='btrfs subvolume snapshot / /.snapshots/pre-update'
# SNAPPER_POST_CMD='btrfs subvolume snapshot / /.snapshots/post-update'
# SNAPPER_DELETE_CMD='btrfs subvolume delete /.snapshots/pre-update'

# Mail Body Templates (Available variables: $UPDATE_OUT, $hostname, $EXIT_CODE)
EMAIL_BODY_SUCCESS='$UPDATE_OUT'
EMAIL_BODY_FAILURE='$UPDATE_OUT'
```

## 6. Dependencies
* **flatpak**: Managed application updates.
* **snapper**: Btrfs snapshot management (Default, overrideable).
* **s-nail**: (or mailx) SMTP notification client (Default, overrideable).
* **systemd**: Service orchestration and scheduling.

---
*License: GPL-3.0-or-later*
*Generated for Fedora Linux - 2026*
