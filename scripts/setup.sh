#!/usr/bin/env bash
# SIH 2026 Smart Road Monitoring Platform — Environment Setup Script

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

echo "=================================================="
echo "SIH 2026 Platform Setup & Environment Initializer"
echo "=================================================="

echo "✓ Using Python: $("$PYTHON_BIN" --version) ($PYTHON_BIN)"

if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    "$PYTHON_BIN" -m pip install -q -r requirements.txt
fi

echo "🗄️ Initializing SQLite database schema..."
"$PYTHON_BIN" -c "from src.backend.database import init_db; init_db(); print('✓ Database initialized successfully!')"

echo "=================================================="
echo "✓ Setup Complete! Run './scripts/run_demo.sh' to launch."
echo "=================================================="
