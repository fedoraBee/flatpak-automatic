#!/bin/bash
# Script to update the DNF repository metadata with versioned channels
#
# This script organizes RPMs into a versioned structure (e.g., v1.1/stable)
# and maintains a 'latest' pointer for each channel.

set -e

# --- Configuration ---
RPM_SOURCE_DIR=${1:-".rpmbuild/RPMS/noarch"}
DEB_SOURCE_DIR=${2:-"debs"}
VERSION=${3:-"1.1.0"}
CHANNEL=${4:-"stable"}
GPG_KEY_ID=${5}
REPO_ROOT=${6:-"repo"} # Defaults to creating a 'repo' folder in current directory

# --- Functions ---
usage() {
    echo "Usage: $0 [rpm_source_dir] [deb_source_dir] [version] [channel] [gpg_key_id] [repo_root]"
    echo "Example: $0 .rpmbuild/RPMS/noarch debs 1.1.0 stable 9B99A03F6577BF59 ./repo"
}

check_dependencies() {
    local deps=("createrepo_c" "gpg" "rpm" "dpkg-scanpackages" "apt-ftparchive")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            echo "Error: Required command '$dep' not found. Please install it."
            exit 1
        fi
    done
}

# --- Execution ---
check_dependencies

# Attempt to discover GPG_KEY_ID from RPM macros if not provided as argument
if [ -z "$GPG_KEY_ID" ]; then
    GPG_KEY_ID=$(rpm --eval '%{?_gpg_name}' 2>/dev/null || true)
    # RPM returns the literal macro string if undefined; clean it up
    if [[ "$GPG_KEY_ID" == "%{?_gpg_name}" ]]; then
        GPG_KEY_ID=""
    fi
fi

# Calculate versioned directory name (vMAJOR.MINOR)
MAJOR_MINOR=$(echo "$VERSION" | cut -d. -f1,2)

# --- RPM Repository Update ---
RPM_VERSION_DIR="$REPO_ROOT/rpms/v$MAJOR_MINOR/$CHANNEL"
RPM_LATEST_DIR="$REPO_ROOT/rpms/latest/$CHANNEL"

echo "Updating RPM repository..."
echo "  Source RPMs: $RPM_SOURCE_DIR"
echo "  Version:     $VERSION (v$MAJOR_MINOR)"
echo "  Channel:     $CHANNEL"
echo "  Repo Root:   $REPO_ROOT/rpms"

mkdir -p "$RPM_VERSION_DIR"
mkdir -p "$RPM_LATEST_DIR"

shopt -s nullglob
RPMS=("$RPM_SOURCE_DIR"/*.rpm)
shopt -u nullglob

if [ ${#RPMS[@]} -gt 0 ]; then
    echo "Copying RPMs to $RPM_VERSION_DIR..."
    cp "${RPMS[@]}" "$RPM_VERSION_DIR/"

    echo "Updating RPM metadata in $RPM_VERSION_DIR..."
    createrepo_c --update "$RPM_VERSION_DIR"

    if [ -n "$GPG_KEY_ID" ]; then
        echo "Signing RPM metadata in $RPM_VERSION_DIR..."
        rm -f "$RPM_VERSION_DIR/repodata/repomd.xml.asc"
        gpg --detach-sign --armor --batch --yes --pinentry-mode loopback --local-user "$GPG_KEY_ID" "$RPM_VERSION_DIR/repodata/repomd.xml"
    fi

    echo "Syncing RPM $RPM_VERSION_DIR to $RPM_LATEST_DIR..."
    if command -v rsync >/dev/null 2>&1; then
        rsync -av --delete "$RPM_VERSION_DIR/" "$RPM_LATEST_DIR/"
    else
        rm -rf "${RPM_LATEST_DIR:?}"/*
        cp -r "$RPM_VERSION_DIR/"* "$RPM_LATEST_DIR/"
    fi
else
    echo "Warning: No RPMs found in $RPM_SOURCE_DIR. Skipping RPM repo update."
fi

# --- DEB Repository Update ---
DEB_VERSION_DIR="$REPO_ROOT/debs/v$MAJOR_MINOR/$CHANNEL"
DEB_LATEST_DIR="$REPO_ROOT/debs/latest/$CHANNEL"

echo "Updating DEB repository..."
echo "  Source DEBs: $DEB_SOURCE_DIR"
echo "  Version:     $VERSION (v$MAJOR_MINOR)"
echo "  Channel:     $CHANNEL"
echo "  Repo Root:   $REPO_ROOT/debs"

mkdir -p "$DEB_VERSION_DIR"
mkdir -p "$DEB_LATEST_DIR"

shopt -s nullglob
DEBS=("$DEB_SOURCE_DIR"/*.deb)
shopt -u nullglob

if [ ${#DEBS[@]} -gt 0 ]; then
    echo "Copying DEBs to $DEB_VERSION_DIR..."
    cp "${DEBS[@]}" "$DEB_VERSION_DIR/"

    echo "Updating APT metadata in $DEB_VERSION_DIR..."
    (cd "$DEB_VERSION_DIR" && dpkg-scanpackages . /dev/null >Packages && gzip -9c Packages >Packages.gz && apt-ftparchive release . >Release)

    if [ -n "$GPG_KEY_ID" ]; then
        echo "Signing APT metadata in $DEB_VERSION_DIR..."
        rm -f "$DEB_VERSION_DIR/Release.gpg" "$DEB_VERSION_DIR/InRelease"
        gpg --detach-sign --armor --batch --yes --pinentry-mode loopback --local-user "$GPG_KEY_ID" -o "$DEB_VERSION_DIR/Release.gpg" "$DEB_VERSION_DIR/Release"
        gpg --clearsign --batch --yes --pinentry-mode loopback --local-user "$GPG_KEY_ID" -o "$DEB_VERSION_DIR/InRelease" "$DEB_VERSION_DIR/Release"
    fi

    echo "Syncing DEB $DEB_VERSION_DIR to $DEB_LATEST_DIR..."
    if command -v rsync >/dev/null 2>&1; then
        rsync -av --delete "$DEB_VERSION_DIR/" "$DEB_LATEST_DIR/"
    else
        rm -rf "${DEB_LATEST_DIR:?}"/*
        cp -r "$DEB_VERSION_DIR/"* "$DEB_LATEST_DIR/"
    fi
else
    echo "Warning: No DEBs found in $DEB_SOURCE_DIR. Skipping DEB repo update."
fi

# --- GPG Key Export ---
if [ -n "$GPG_KEY_ID" ]; then
    echo "Exporting public key to $REPO_ROOT/gpt.key..."
    gpg --armor --export "$GPG_KEY_ID" >"$REPO_ROOT/gpt.key"
    # Also keep gpg.key for compatibility if needed, but user asked for gpt.key
    cp "$REPO_ROOT/gpt.key" "$REPO_ROOT/gpg.key"
else
    if [ -f "gpg.key" ]; then
        echo "Copying existing gpg.key to $REPO_ROOT/gpt.key..."
        cp "gpg.key" "$REPO_ROOT/gpt.key"
        cp "gpg.key" "$REPO_ROOT/gpg.key"
    fi
fi

echo "Repository update complete in $REPO_ROOT"
