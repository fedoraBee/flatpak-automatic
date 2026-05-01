#!/bin/bash
set -euo pipefail
NAME="${1}"
EPOCH="${2}"
VERSION="${3}"
REL_NUM="${4}"
TOPDIR="${5}"

# Standardize RPM version format (RPM doesn't like hyphens in the version string)
# This MUST match the logic in update-package-metadata.py
# Use quotes around '~' to prevent shell expansion to $HOME
SAFE_VERSION="${VERSION//-/'~'}"

echo "Building RPM for ${NAME} ${EPOCH}:${SAFE_VERSION}-${REL_NUM}..."
tar -czf "${TOPDIR}/SOURCES/${NAME}-${SAFE_VERSION}.tar.gz" --exclude='.git' --exclude='.rpmbuild' .
rpmbuild --define "_topdir ${TOPDIR}" -ba "${TOPDIR}/SPECS/${NAME}.spec"
echo "RPM build complete. Output located in ${TOPDIR}/RPMS/noarch/"
