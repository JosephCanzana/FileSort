#!/usr/bin/env bash
set -euo pipefail                # stop on any error
cd "$(dirname "$0")"             # go to this script's own folder

# Install uv only if missing
if ! command -v uv > /dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

export PATH="$HOME/.local/bin:$PATH"   # now always runs

uv tool install --python 3.12 --force .
echo "Installed! Open a new terminal and run: filesort"