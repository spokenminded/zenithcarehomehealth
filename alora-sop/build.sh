#!/usr/bin/env bash
# Build the Zenith Alora Office Operating Manual (HTML and PDF).
#   ./build.sh
# Needs: python3 with fonttools (pip install fonttools), the Liberation Sans fonts, node with playwright and Chromium.
set -euo pipefail
cd "$(dirname "$0")"
export NODE_PATH="${NODE_PATH:-$(npm root -g)}"
python3 src/build.py zenith-alora-office-sop.html --strict
node src/build_pdf.js "$PWD/zenith-alora-office-sop.html" "$PWD/zenith-alora-office-sop.pdf"
