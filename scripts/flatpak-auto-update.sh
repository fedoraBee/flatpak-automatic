#!/bin/bash
################################################################################
# Flatpak Auto Update (Linux Professional Edition)
# Version: 1.0.0
# Author: fedoraBee
# Source: https://github.com/fedoraBee/flatpak-auto-update
#
# Description:
#   An automation wrapper for Flatpak updates on Fedora Linux,
#   integrating Snapper for atomic-like rollbacks and systemd for scheduling.
#
# License:
#   Copyright (C) 2026 fedoraBee
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
################################################################################
set -euo pipefail
CONFIG_FILE="/etc/flatpak-auto-update/env.conf"
[ -f "$CONFIG_FILE" ] && source "$CONFIG_FILE"

# Defaults
ENABLE_EMAIL="${ENABLE_EMAIL:-yes}"
ENABLE_SNAPSHOTS="${ENABLE_SNAPSHOTS:-yes}"

# Mail Defaults
EMAIL_FROM_DISPLAY="${EMAIL_FROM_DISPLAY:-Fedora Bot}"
EMAIL_SUBJECT_SUCCESS="${EMAIL_SUBJECT_SUCCESS:-Flatpak Update: Success ($(hostname))}"
EMAIL_SUBJECT_FAILURE="${EMAIL_SUBJECT_FAILURE:-SERIOUS: Flatpak Update Failed ($(hostname))}"
MAIL_CMD="${MAIL_CMD:-mailx -S sendwait -r \"\$EMAIL_FROM_DISPLAY <\$email_from>\" -s \"\$1\" \"\$2\"}"
EMAIL_BODY_SUCCESS="${EMAIL_BODY_SUCCESS:-\$UPDATE_OUT}"
EMAIL_BODY_FAILURE="${EMAIL_BODY_FAILURE:-\$UPDATE_OUT}"

# Snapper Defaults
SNAPPER_CONFIG="${SNAPPER_CONFIG:-root}"
SNAPPER_DESC_PRE="${SNAPPER_DESC_PRE:-flatpak-auto-update-pre}"
SNAPPER_DESC_POST="${SNAPPER_DESC_POST:-flatpak-auto-update-post}"
SNAPPER_PRE_CMD="${SNAPPER_PRE_CMD:-snapper -c \"\$SNAPPER_CONFIG\" create --type pre --description \"\$SNAPPER_DESC_PRE\" --cleanup-algorithm number --print-number}"
SNAPPER_POST_CMD="${SNAPPER_POST_CMD:-snapper -c \"\$SNAPPER_CONFIG\" create --type post --pre-number \"\$PRE_NUM\" --description \"\$SNAPPER_DESC_POST\"}"
SNAPPER_DELETE_CMD="${SNAPPER_DELETE_CMD:-snapper -c \"\$SNAPPER_CONFIG\" delete \"\$PRE_NUM\"}"

# Validation for email if enabled
if [[ "$ENABLE_EMAIL" == "yes" ]]; then
    : "${email_to:? 'Set email_to in $CONFIG_FILE or disable ENABLE_EMAIL'}"
    : "${email_from:? 'Set email_from in $CONFIG_FILE or disable ENABLE_EMAIL'}"
fi

# Helper to send notifications
send_notification() {
    local subject="$1"
    local recipient="$2"
    local body_template="$3"
    local body
    body=$(eval "echo \"$body_template\"")
    (
        set -- "$subject" "$recipient"
        printf "%s\n" "$body" | eval "$MAIL_CMD"
    )
}

# 0. Dry run check (optional)
# Avoids creating a snapshot if there are no updates to apply.
if [[ "$ENABLE_SNAPSHOTS" == "yes" ]]; then
    DRY_RUN_OUT=$(flatpak update --dry-run --noninteractive 2>&1) || true
    if [[ "$DRY_RUN_OUT" =~ "Nothing to do" ]] || [[ "$DRY_RUN_OUT" =~ "No updates" ]]; then
        exit 0
    fi
fi

# 1. Pre-update snapshot (optional)
PRE_NUM=""
if [[ "$ENABLE_SNAPSHOTS" == "yes" ]]; then
    PRE_NUM=$(eval "$SNAPPER_PRE_CMD")
fi

# 2. Perform the update
EXIT_CODE=0
UPDATE_OUT=$(flatpak update -y --noninteractive 2>&1) || EXIT_CODE=$?

UPDATED=false
# Flatpak exit code 0 usually means success; check output to see if anything happened
[[ "$EXIT_CODE" -eq 0 ]] && [[ ! "$UPDATE_OUT" =~ "Nothing to do" ]] && [[ ! "$UPDATE_OUT" =~ "No updates" ]] && UPDATED=true

# 3. Post-processing
if [ "$UPDATED" = true ]; then
    # Create post-snapshot (optional)
    if [[ "$ENABLE_SNAPSHOTS" == "yes" && -n "$PRE_NUM" ]]; then
        eval "$SNAPPER_POST_CMD"
    fi
    # Send success email (optional)
    if [[ "$ENABLE_EMAIL" == "yes" ]]; then
        send_notification "$EMAIL_SUBJECT_SUCCESS" "$email_to" "$EMAIL_BODY_SUCCESS"
    fi
elif [ "$EXIT_CODE" -ne 0 ]; then
    # Send failure email (optional)
    if [[ "$ENABLE_EMAIL" == "yes" ]]; then
        send_notification "$EMAIL_SUBJECT_FAILURE" "$email_to" "$EMAIL_BODY_FAILURE"
    fi
    # Cleanup orphan pre-snapshot (optional)
    if [[ "$ENABLE_SNAPSHOTS" == "yes" && -n "$PRE_NUM" ]]; then
        eval "$SNAPPER_DELETE_CMD" >/dev/null 2>&1 || true
    fi
    exit "$EXIT_CODE"
else
    # Success but nothing updated - Cleanup pre-snapshot (optional)
    if [[ "$ENABLE_SNAPSHOTS" == "yes" && -n "$PRE_NUM" ]]; then
        eval "$SNAPPER_DELETE_CMD" >/dev/null 2>&1 || true
    fi
fi
