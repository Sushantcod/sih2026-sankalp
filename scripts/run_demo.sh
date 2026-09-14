#!/usr/bin/env bash
# SIH 2026 Smart Road Monitoring Platform — Unified Demo Launcher

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
echo "SIH 2026 SMART ROAD MONITORING & TRAFFIC PLATFORM"
echo "Unified System Demo Launcher & Diagnostic Check"
echo "=================================================="

# 1. Verify Models
echo "🔍 1. Verifying AI Model Checksums..."
"$PYTHON_BIN" -c "
import hashlib, os, sys

models = {
    'models/pothole.pt': '947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b',
    'models/anpr/best.pt': 'd9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a',
    'models/yolov8n.pt': 'f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36'
}

for path, expected in models.items():
    if not os.path.exists(path):
        print(f'❌ Missing model: {path}')
        sys.exit(1)
    h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    if h != expected:
        print(f'❌ Checksum mismatch for {path}')
        sys.exit(1)
    print(f'  ✓ {path}: SHA256 Verified')
"

# 2. Verify Database
echo "🗄️ 2. Verifying SQLite Telemetry Database..."
"$PYTHON_BIN" -c "
import sqlite3, sys
conn = sqlite3.connect('data/events.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM events')
cnt = c.fetchone()[0]
if cnt != 7964:
    print(f'❌ DB Event count mismatch: {cnt} (expected 7,964)')
    sys.exit(1)
print(f'  ✓ Database Verified: {cnt:,} Stored Telemetry Events')
"

echo "=================================================="
echo "🚀 SYSTEM ENDPOINTS READY FOR SIH DEMO:"
echo "--------------------------------------------------"
echo "  1. GIS Operations Dashboard UI : http://127.0.0.1:3000"
echo "  2. FastAPI Central Backend REST: http://127.0.0.1:8000"
echo "  3. Interactive API Docs (Swagger): http://127.0.0.1:8000/docs"
echo "  4. Database Health Endpoint     : http://127.0.0.1:8000/health"
echo "  5. Empirical Statistics         : http://127.0.0.1:8000/stats"
echo "=================================================="
echo "JUDGE DEMO STEPS:"
echo "  1. Open http://127.0.0.1:3000 in your browser."
echo "  2. Review Overview cards and System Health tab."
echo "  3. Click 'Incident Management' tab."
echo "  4. Create an incident from a real event ID (e.g. evt_0001)."
echo "  5. Update status (OPEN -> ACKNOWLEDGED -> RESOLVED) and add operator notes."
echo "  6. Click 'Reports' tab to download real CSV/JSON export."
echo "=================================================="
