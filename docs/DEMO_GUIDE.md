# SIH 2026 — 5-to-10 Minute Judge Demonstration Walkthrough

This guide provides a structured, step-by-step demonstration script for presenting the **SIH 2026 Smart Road Monitoring & Traffic Management Platform** to hackathon judges.

---

## 1. Pre-Demo Diagnostic Execution (30 Seconds)

Open your terminal and run:
```bash
./scripts/run_demo.sh
```
Verify that the output displays:
- `✓ models/pothole.pt: SHA256 Verified`
- `✓ models/anpr/best.pt: SHA256 Verified`
- `✓ Database Verified: 7,964 Stored Telemetry Events`
- `GIS Operations Dashboard UI : http://127.0.0.1:3000`

---

## 2. Opening Elevator Pitch (30 Seconds)

> **Judge Pitch**: *"Good morning judges. We are addressing **SIH Problem Statement 26124** by **Bharat Electronics Limited (BEL)**: 'AI-Powered Mobile Urban Intelligence Platform Using Public Transport Fleet'. Today, cities spend millions installing static CCTVs that only monitor isolated junctions. We convert existing public bus fleets into mobile urban sensing units. By running Edge-AI computer vision directly on the bus, we process road damage, vehicle density, and ANPR locally—sending only lightweight JSON telemetry alerts to our Central Command Platform. This eliminates the cellular bandwidth cost of raw video while covering 100% of municipal transit routes daily."*

---

## 3. Step-by-Step Demonstration Script (5-10 Minutes)

### Step 1: Open Operations Command Center UI
1. Navigate to `http://127.0.0.1:3000` in Google Chrome or Safari.
2. Point out the top header: **SIH 2026 Operations Command Center** with real-time API and DB status chips (`API Online`, `DB Connected`).
3. Point out the Overview KPI Cards:
   - Total Ingested Events: **7,964**
   - Road Damage Detections: **2,708**
   - ANPR Plate Events: **5,256**
   - Active Incidents: **0**

### Step 2: Explain Zero Fabrication & Honest GPS State
1. Show the GIS Map section with the warning banner:
   `"⚠️ GPS Telemetry Unavailable — 7,964 events in database contain latitude: null, longitude: null."`
2. **Key Judge Talking Point**: *"Our system enforces a strict zero-fabrication policy. Because test video streams were recorded without attached NMEA hardware GPS sensors, we represent GPS telemetry honestly as unavailable (Mode B) rather than generating fake map points."*

### Step 3: Demonstrate Real Telemetry Event Stream & Inspection
1. Scroll down to the **Ingested Telemetry Events Table**.
2. Filter events by `event_type = pothole` or `source = BUS-101`.
3. Click **"Details"** on any row to open the Event Detail Modal.
4. Show the verbatim original JSON payload received from the edge inference script.
5. Click **"🚨 Dispatch Incident From This Event"** button.

### Step 4: Dispatch & Manage a Real Incident
1. You will be redirected to the **Incident Management** tab with the real `event_id` auto-filled.
2. Select Severity: `HIGH`.
3. Enter Title: `Pothole Repair Request — Sector 4`.
4. Enter Assigned Operator: `Officer_Rao`.
5. Enter Initial Note: `Maintenance crew dispatched to site`.
6. Click **"Create Incident"**.
7. In the Incidents Table, locate the newly created incident (`inc_...`).
8. Click **"Manage"** to open the Incident Status Modal.
9. Change Status from `OPEN` -> `IN_PROGRESS`, add note `"Crews arrived on site"`, and click **"Save Changes"**.
10. Re-open **"Manage"** to show the complete audit history log tracking state transitions.

### Step 5: Explore Subsystem Tabs & Technical Specs
1. Click **Road Damage Tab**: Show breakdown of 1,747 alligator cracks, 527 potholes, 273 longitudinal cracks, 135 transverse cracks, 24 manholes, 2 waterloggings.
2. Click **ANPR & OCR Tab**: Explain plate localization strength (98.04% mAP50) while transparently noting OCR limitations (20.14% character accuracy).
3. Click **System Health Tab**: Show live status checks for backend, database, model weights, and hardware sensors.
4. Click **Reports Tab**: Click **"📄 Export Events CSV"** to download the official dataset export.

---

## 3. Wrap-Up Summary Statement
> *"In summary, the SIH 2026 Smart Road Monitoring Platform connects edge computer vision detectors to a high-performance FastAPI ingestion engine, SQLite event store, incident management subsystem, and dark-theme GIS Command Center. Every single number and metric presented is derived strictly from real database records."*
