#!/bin/zsh

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_ACTIVATE="/Users/claudia/Github/.env_base/bin/activate"

cd "$PROJECT_DIR"
source "$ENV_ACTIVATE"
python -m process.create_sample