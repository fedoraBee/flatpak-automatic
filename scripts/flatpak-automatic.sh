#!/bin/bash
################################################################################
# Flatpak Auto Update (Linux Professional Edition)
# Version: 1.0.3
# Author: fedoraBee
# Source: https://github.com/fedoraBee/flatpak-automatic
#
# Description:
#   An automation wrapper for Flatpak updates on Fedora and RPM-based systems,
#   integrating Snapper for atomic-like rollbacks and systemd for scheduling.
#   Includes dynamic package count and universal Btrfs/Snapper detection.
#
# License: GPL-3.0-or-later
################################################################################
set -euo pipefail

CONFIG_FILE="/etc/sysconfig/flatpak-automatic"
if [ -f "$CONFIG_FILE" ]; then
    # shellcheck disable=SC1090
    source "$CONFIG_FILE"
fi

# Defaults
ENABLE_EMAIL="${ENABLE_EMAIL:-yes}"
ENABLE_SNAPSHOTS="${ENABLE_SNAPSHOTS:-yes}"

# Mail Defaults
EMAIL_FROM_DISPLAY="${EMAIL_FROM_DISPLAY:-Fedora Bot}"
EMAIL_SUBJECT_SUCCESS="${EMAIL_SUBJECT_SUCCESS:-[$(hostname)] flatpak-automatic: \$UPDATE_COUNT new upgrades have been installed.}"
EMAIL_SUBJECT_FAILURE="${EMAIL_SUBJECT_FAILURE:-[$(hostname)] flatpak-automatic: FAILED}"
MAIL_CMD="${MAIL_CMD:-mailx -S sendwait -r \"\$EMAIL_FROM_DISPLAY <\$EMAIL_FROM>\" -s \"\$1\" \"\$2\"}"
EMAIL_BODY_SUCCESS="${EMAIL_BODY_SUCCESS:-\$UPDATE_OUT}"
EMAIL_BODY_FAILURE="${EMAIL_BODY_FAILURE:-\$UPDATE_OUT}"

# Snapper Defaults
SNAPPER_CONFIG="${SNAPPER_CONFIG:-root}"
SNAPPER_DESC_PRE="${SNAPPER_DESC_PRE:-flatpak-automatic-pre}"
SNAPPER_DESC_POST="${SNAPPER_DESC_POST:-flatpak-automatic-post}"
SNAPPER_PRE_CMD="${SNAPPER_PRE_CMD:-snapper -c \"\$SNAPPER_CONFIG\" create --type pre --description \"\$SNAPPER_DESC_PRE\" --cleanup-algorithm number --print-number}"
SNAPPER_POST_CMD="${SNAPPER_POST_CMD:-snapper -c \"\$SNAPPER_CONFIG\" create --type post --pre-number \"\$PRE_NUM\" --description \"\$SNAPPER_DESC_POST\"}"
SNAPPER_DELETE_CMD="${SNAPPER_DELETE_CMD:-snapper -c \"\$SNAPPER_CONFIG\" delete \"\$PRE_NUM\"}"

# Validation for email if enabled
if [[ "$ENABLE_EMAIL" == "yes" ]]; then
    : "${EMAIL_TO:? "Set EMAIL_TO in $CONFIG_FILE or disable ENABLE_EMAIL"}"
    : "${EMAIL_FROM:? "Set EMAIL_FROM in $CONFIG_FILE or disable ENABLE_EMAIL"}"
fi

# Helper to send notifications
send_notification() {
    local subject_template="$1"
    local recipient="$2"
    local body_template="$3"
    
    # Evaluate templates to resolve variables like $UPDATE_COUNT and $UPDATE_OUT
    local subject
    local body
    subject=$(eval "echo \"$subject_template\"")
    body=$(eval "echo \"$body_template\"")
    
    (
        set -- "$subject" "$recipient"
        printf "%s\n" "$body" | eval "$MAIL_CMD"
    )
}

# Safety Check: Disable snapshots if Snapper config is invalid or Btrfs is missing
if [[ "$ENABLE_SNAPSHOTS" == "yes" ]]; then
    if ! snapper -c "$SNAPPER_CONFIG" get-config >/dev/null 2>&1; then
        echo "WARNING: Snapper config '$SNAPPER_CONFIG' invalid or missing. Disabling snapshots." >&2
        ENABLE_SNAPSHOTS="no"
    fi
fi

# 0. Dry run check
# Optimization: Check if updates exist before doing anything with Snapper
DRY_RUN_OUT=$(flatpak update --dry-run --noninteractive 2>&1) || true
if [[ "$DRY_RUN_OUT" =~ "Nothing to do" ]] || [[ "$DRY_RUN_OUT" =~ "No updates" ]]; then
    exit 0
fi

# 1. Pre-update snapshot
PRE_NUM=""
if [[ "$ENABLE_SNAPSHOTS" == "yes" ]]; then
    PRE_NUM=$(eval "$SNAPPER_PRE_CMD")
fi

# 2. Perform the update
EXIT_CODE=0
UPDATE_OUT=$(flatpak update -y --noninteractive 2>&1) || EXIT_CODE=$?

# 3. Calculate Update Count
# Counts lines starting with Installing, Updating, or Removing
UPDATE_COUNT=$(echo "$UPDATE_OUT" | grep -E -c "^(Installing|Updating|Removing)")

UPDATED=false
[[ "$EXIT_CODE" -eq 0 ]] && [[ "$UPDATE_COUNT" -gt 0 ]] && UPDATED=true

# 4. Post-processing
if [ "$UPDATED" = true ]; then
    # Create post-snapshot
    if [[ "$ENABLE_SNAPSHOTS" == "yes" && -n "$PRE_NUM" ]]; then
        eval "$SNAPPER_POST_CMD"
    fi
    # Send success email
    if [[ "$ENABLE_EMAIL" == "yes" ]]; then
        send_notification "$EMAIL_SUBJECT_SUCCESS" "$EMAIL_TO" "$EMAIL_BODY_SUCCESS"
    fi
elif [ "$EXIT_CODE" -ne 0 ]; then
    # Send failure email
    if [[ "$ENABLE_EMAIL" == "yes" ]]; then
        send_notification "$EMAIL_SUBJECT_FAILURE" "$EMAIL_TO" "$EMAIL_BODY_FAILURE"
    fi
    # Cleanup orphan pre-snapshot
    if [[ "$ENABLE_SNAPSHOTS" == "yes" && -n "$PRE_NUM" ]]; then
        eval "$SNAPPER_DELETE_CMD" >/dev/null 2>&1 || true
    fi
    exit "$EXIT_CODE"
else
    # Success but nothing actually changed (rare due to dry-run check)
    if [[ "$ENABLE_SNAPSHOTS" == "yes" && -n "$PRE_NUM" ]]; then
        eval "$SNAPPER_DELETE_CMD" >/dev/null 2>&1 || true
    fi
fi