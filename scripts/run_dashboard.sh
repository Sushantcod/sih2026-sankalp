#!/usr/bin/env bash
# SIH 2026 Smart Road Monitoring Platform — Dashboard UI Launcher

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

if [ -f "/Users/sushant/Desktop/sih/SIH2026 v1/.venv/bin/python" ]; then
    PYTHON_BIN="/Users/sushant/Desktop/sih/SIH2026 v1/.venv/bin/python"
elif command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
else
    PYTHON_BIN="python"
fi

echo "🌐 Serving GIS Operations Command Center Dashboard on 127.0.0.1:3000..."
exec "$PYTHON_BIN" -m http.server 3000 --directory src/dashboard
