#!/bin/bash
set -euo pipefail
NAME="${1}"
EPOCH="${2}"
VERSION="${3}"
REL_NUM="${4}"
TOPDIR="${5}"

echo "Building RPM for ${NAME} ${EPOCH}:${VERSION}-${REL_NUM}..."
tar -czf "${TOPDIR}/SOURCES/${NAME}-${VERSION}.tar.gz" --exclude='.git' --exclude='.rpmbuild' .
rpmbuild --define "_topdir ${TOPDIR}" -ba "${TOPDIR}/SPECS/${NAME}.spec"
echo "RPM build complete. Output located in ${TOPDIR}/RPMS/noarch/"
