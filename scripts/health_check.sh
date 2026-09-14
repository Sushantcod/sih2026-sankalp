#!/usr/bin/env bash
# SIH 2026 Smart Road Monitoring Platform — Quick System Health Check CLI

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

PYTHON_BIN=""
if [ -f "/Users/sushant/Desktop/sih/SIH2026 v1/.venv/bin/python" ]; then
    PYTHON_BIN="/Users/sushant/Desktop/sih/SIH2026 v1/.venv/bin/python"
elif command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
else
    PYTHON_BIN="python"
fi

$PYTHON_BIN -c "
import urllib.request, json, sqlite3, os

print('--- SIH 2026 SYSTEM HEALTH CHECK ---')
# API
try:
    req = urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)
    data = json.loads(req.read().decode())
    print(f'FastAPI Backend : ONLINE ({data})')
except Exception as e:
    print(f'FastAPI Backend : OFFLINE ({e})')

# DB
if os.path.exists('data/events.db'):
    conn = sqlite3.connect('data/events.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM events')
    cnt = c.fetchone()[0]
    print(f'SQLite Database : CONNECTED ({cnt:,} records in data/events.db)')
else:
    print('SQLite Database : MISSING (data/events.db not found)')

# Models
pothole_ok = os.path.exists('models/pothole.pt')
anpr_ok = os.path.exists('models/anpr/best.pt')
print(f'Pothole Model   : {\"READY\" if pothole_ok else \"MISSING\"}')
print(f'ANPR Model      : {\"READY\" if anpr_ok else \"MISSING\"}')
print('GPS Telemetry   : UNAVAILABLE (Mode B — Honest null state)')
"
