#!/usr/bin/env bash
# SIH 2026 Smart Road Monitoring Platform — Complete Project Verification Script

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
echo "SIH 2026 SYSTEM AUTOMATED INTEGRITY & TEST AUDIT"
echo "=================================================="

# 1. Model Checksums
echo "[1/6] Auditing Protected AI Model Checksums..."
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
    print(f'  ✓ PASS: {path} SHA256 matches verified baseline')
"

# 2. Database Record Audit
echo "[2/6] Auditing SQLite Database Record Integrity..."
"$PYTHON_BIN" -c "
import sqlite3, sys
conn = sqlite3.connect('data/events.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM events')
total = c.fetchone()[0]
if total != 7964:
    print(f'❌ Event count altered: {total} (expected 7,964)')
    sys.exit(1)

c.execute('SELECT COUNT(*) FROM events WHERE latitude IS NULL')
gps_null = c.fetchone()[0]
if gps_null != 7964:
    print(f'❌ Fake GPS detected! Null count: {gps_null} (expected 7,964)')
    sys.exit(1)

print(f'  ✓ PASS: Database Integrity Verified (7,964 Real Records, 100% Honest GPS-Null State)')
"

# 3. Backend Unit, Incident & Analytics Tests
echo "[3/6] Running Backend, Incident & Analytics Unit Tests..."
"$PYTHON_BIN" tests/test_backend.py
"$PYTHON_BIN" tests/test_phase6_incidents.py
"$PYTHON_BIN" tests/test_phase7_analytics.py
"$PYTHON_BIN" tests/test_phase8_pedestrian.py

# 4. Dashboard & GIS Tests
echo "[4/6] Running Dashboard & Integration Tests..."
"$PYTHON_BIN" tests/test_dashboard.py

# 5. API Health Check
echo "[5/6] Checking API Endpoint Responsiveness..."
"$PYTHON_BIN" -c "
import urllib.request, json
req = urllib.request.urlopen('http://127.0.0.1:8000/health')
data = json.loads(req.read().decode())
if data.get('status') == 'ok':
    print('  ✓ PASS: FastAPI Backend Health Endpoint Responding 200 OK')
else:
    print('❌ Health endpoint returned unexpected response')
    sys.exit(1)
"

# 6. Zero Fabrication Code Audit
echo "[6/6] Auditing Codebase for Unsafe Data Fabrication..."
"$PYTHON_BIN" -c "
import os, sys
banned = ['generateRandomGps', 'fakeGps', 'syntheticCoordinates']
found = False
for root, dirs, files in os.walk('src'):
    for f in files:
        if f.endswith(('.py', '.js', '.html')):
            path = os.path.join(root, f)
            content = open(path, 'r', encoding='utf-8', errors='ignore').read()
            for b in banned:
                if b in content:
                    print(f'❌ Banned term \"{b}\" found in {path}')
                    found = True
if found:
    sys.exit(1)
print('  ✓ PASS: Zero-Fabrication Audit Clean (No synthetic GPS functions found)')
"

echo "=================================================="
echo "✅ ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!"
echo "=================================================="
