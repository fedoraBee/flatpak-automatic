#!/bin/bash
set -euo pipefail

# Usage: prepare-docs.sh [SOURCE_DIR]
# Defaults to current directory if SOURCE_DIR is not provided.
SRC_DIR="${1:-.}"
DOCS_DIR="docs"

echo "Preparing documentation in ${DOCS_DIR} using sources from ${SRC_DIR}..."

mkdir -p "${DOCS_DIR}"

# Copy root markdown files
for f in README.md CHANGELOG.md MAINTAINERS.md AGENTS.md; do
    if [ -f "${SRC_DIR}/${f}" ]; then
        dest_name="${f,,}" # lowercase
        if [ "${f}" == "README.md" ]; then dest_name="index.md"; fi
        cp "${SRC_DIR}/${f}" "${DOCS_DIR}/${dest_name}"
    fi
done

# Handle LICENSE (not an .md file)
if [ -f "${SRC_DIR}/LICENSE" ]; then
    {
        echo "# License"
        echo ""
        echo '```text'
        cat "${SRC_DIR}/LICENSE"
        echo '```'
    } >"${DOCS_DIR}/license.md"
fi

# Handle files from .github/
mkdir -p "${DOCS_DIR}/about"
for f in CONTRIBUTING.md SECURITY.md; do
    if [ -f "${SRC_DIR}/.github/${f}" ]; then
        dest_name="${f,,}" # lowercase
        cp "${SRC_DIR}/.github/${f}" "${DOCS_DIR}/about/${dest_name}"
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

# Fix banner paths in index.md (root)
if [ -f "${DOCS_DIR}/index.md" ]; then
    # Use relative path that works for MkDocs (assets/banner.svg is in docs/assets/)
    # In index.md, assets/banner.svg is correct as it's in the same base dir.
    # However, to be safe across sub-pages, some themes prefer absolute-like paths or relative from root.
    # MkDocs usually rewrites paths, but raw HTML <img> tags might need help.
    sed -i 's|src="assets/banner.svg"|src="assets/banner.svg"|g' "${DOCS_DIR}/index.md"
fi

# Fix banner paths
if [ -f "${DOCS_DIR}/agents.md" ]; then
    sed -i 's|src="assets/banner.svg"|src="../assets/banner.svg"|g' "${DOCS_DIR}/agents.md"
fi
if [ -f "${DOCS_DIR}/changelog.md" ]; then
    sed -i 's|src="assets/banner.svg"|src="../assets/banner.svg"|g' "${DOCS_DIR}/changelog.md"
fi

if [ -f "${DOCS_DIR}/about/contributing.md" ]; then
    sed -i 's|src="../assets/banner.svg"|src="../../assets/banner.svg"|g' "${DOCS_DIR}/about/contributing.md"
fi

if [ -f "${DOCS_DIR}/about/security.md" ]; then
    sed -i 's|src="../assets/banner.svg"|src="../../assets/banner.svg"|g' "${DOCS_DIR}/about/security.md"
fi

echo "Documentation files prepared in ${DOCS_DIR}/"
