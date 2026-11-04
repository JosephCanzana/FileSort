#!/bin/bash

set -e
cd "$(dirname "$0")"

# Verify uv to install python
if ! command -v uv > /dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh 
  export PATH="$HOME/.local/bin:$PATH"
fi
# Install python
uv tool install --python 3.12 .
filesort setup