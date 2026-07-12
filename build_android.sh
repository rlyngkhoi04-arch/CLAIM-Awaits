#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_MODE="${1:-debug}"

cd "$ROOT_DIR"

python3 prepare_android_build.py
buildozer android "$BUILD_MODE"
