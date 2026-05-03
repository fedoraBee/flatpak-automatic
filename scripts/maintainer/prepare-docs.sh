#!/bin/bash
set -euo pipefail

# Usage: prepare-docs.sh [SOURCE_DIR]
# Defaults to current directory if SOURCE_DIR is not provided.
SRC_DIR="${1:-.}"
DOCS_DIR="docs"

echo "Preparing documentation in ${DOCS_DIR} using sources from ${SRC_DIR}..."

mkdir -p "${DOCS_DIR}"

# Copy root markdown files
for f in README.md CHANGELOG.md MAINTAINERS.md AGENTS.md SECURITY.md LICENSE; do
    if [ -f "${SRC_DIR}/${f}" ]; then
        dest_name="${f,,}" # lowercase
        if [ "${f}" == "README.md" ]; then dest_name="index.md"; fi
        cp "${SRC_DIR}/${f}" "${DOCS_DIR}/${dest_name}"
    fi
done

# Copy files already in docs/
if [ -d "${SRC_DIR}/docs" ]; then
    find "${SRC_DIR}/docs" -maxdepth 1 \( -name "*.md" -o -name "*.css" -o -name "*.js" \) -exec cp {} "${DOCS_DIR}/" \;
fi

# Ensure assets are available
mkdir -p "${DOCS_DIR}/assets"
if [ -d "${SRC_DIR}/assets" ]; then
    cp "${SRC_DIR}/assets/"*.svg "${DOCS_DIR}/assets/" 2>/dev/null || true
fi

echo "Documentation files prepared in ${DOCS_DIR}/"
