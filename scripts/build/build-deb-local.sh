#!/bin/bash
set -euo pipefail

echo "Building Debian package..."
dpkg-buildpackage -us -uc -b
mkdir -p debs
mv ../flatpak-automatic_* debs/ || true
