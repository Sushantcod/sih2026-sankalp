#!/usr/bin/env bash
# SIH 2026 Smart Road Monitoring Platform — Backend API Launcher

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

echo "🚀 Starting FastAPI Backend Server on 127.0.0.1:8000..."
exec "$PYTHON_BIN" -m uvicorn src.backend.app:app --host 127.0.0.1 --port 8000 --reload
