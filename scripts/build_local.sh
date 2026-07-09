#!/usr/bin/env bash
# Build the whole showcase locally into _site/ (mirrors CI).
set -euo pipefail
cd "$(dirname "$0")/.."
BIN="$PWD/.venv/bin"
for dir in galleries/*/; do
  echo "Building $dir"
  ( cd "$dir" && "$BIN/simpleGals" build --force )
done
"$BIN/python" build_index.py --out _site
echo "Done: _site/index.html"
