#!/bin/bash
set -euo pipefail
TOPDIR="${1}"
GPG_KEY_ID="${2}"

echo "Signing RPM packages..."
shopt -s nullglob
for f in "${TOPDIR}"/RPMS/noarch/*.rpm; do
    if [ -f "$f" ]; then
        echo "Signing $f..."
        if [ -n "$GPG_KEY_ID" ]; then
            rpmsign --addsign "$f" --define "_gpg_name ${GPG_KEY_ID}" || {
                echo "Conflict detected, removing old signature and re-signing..."
                rpmsign --delsign "$f"
                rpmsign --addsign "$f" --define "_gpg_name ${GPG_KEY_ID}"
            }
        elif [ "$(rpm --eval '%{?_gpg_name}')" != "%{?_gpg_name}" ]; then
            rpmsign --addsign "$f" || {
                echo "Conflict detected, removing old signature and re-signing..."
                rpmsign --delsign "$f"
                rpmsign --addsign "$f"
            }
        else
            echo "Error: GPG_KEY_ID is not set and %_gpg_name macro is not defined."
            echo "Use: make rpm-sign GPG_KEY_ID=<your-key-id> or configure ~/.rpmmacros"
            exit 1
        fi
    fi
done
