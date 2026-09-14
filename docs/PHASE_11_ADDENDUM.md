# PHASE 11 — Closing the Gaps (Secure Transmission, Dedup, Edge Proof, Real-Time Alerts, Closed-Loop Verification)

**Insert this after Phase 10 (or interleave individual steps into Phases 4/6/9 if you prefer building them alongside those — cross-references given below). Time: 2-3 days.**

This phase exists because five things you already promised in your own pitch/workflow narrative were never actually built in Phases 0-10. Each of these is a specific, cheap-to-implement gap — not a redesign. A judge who has seen a well-structured problem breakdown like yours will ask about these exact five things.

---

### 1. Objective
Turn the four "we said this but didn't build it" claims — secure transmission, deduplication/confirmation-count, edge feasibility, real-time alerting — plus closed-loop resolution verification, into real, demoable code.

### 2. Features covered
- Secure transmission to central command system (explicit line item in the problem statement)
- Fleet-wide aggregation done properly (dedup/confirmation-count — your own stated differentiator)
- Edge-AI onboard processing framework (explicit line item — currently unproven)
- Reliable real-time alerts (explicit line item — currently just a passive DB)
- Closed-loop resolution verification (your own novelty claim, currently absent)

### 3. Build steps

**A. Secure transmission (extends Phase 4)**
1. Run the FastAPI backend behind HTTPS locally using a self-signed cert (`uvicorn main:app --ssl-keyfile key.pem --ssl-certfile cert.pem`) — enough to demo "TLS-encrypted transmission" honestly.
2. Add a simple API-key header check (`X-API-Key`) on the `/events` endpoint — every bus script sends this key; reject requests without it. This is your "authenticated bus" story.
3. Add retry-with-backoff in the bus-side scripts: wrap the `POST` call in a try/except, exponential backoff (1s, 2s, 4s...), and fall back to writing into the local `events.jsonl` queue if all retries fail — this is literally the "local buffer for connectivity gaps" your workflow doc describes.
4. On next successful connection, flush the queued file to the backend.

**B. Deduplication / confirmation-count (extends Phase 4)**
1. Before inserting a new event, query existing events of the same `event_type` within a GPS radius (e.g., 15m — use simple Haversine distance in Python, no PostGIS needed for a hackathon) and within a time window (e.g., 30 days).
2. If a match exists, increment a `confirmation_count` field on the existing row instead of inserting a duplicate row.
3. Add a `status` field: `unconfirmed` (count = 1) → `verified` (count ≥ 3, tune threshold). Only `verified` events show on the public-facing map by default (toggle to show unconfirmed too).
4. This is cheap to build (one SQL query + one Python distance function) and it's one of the strongest "we thought about real deployment" points in your pitch.

**C. Edge feasibility proof (extends Phase 1)**
1. Export your pothole/vehicle YOLOv8 model to ONNX: `model.export(format="onnx")`.
2. Benchmark inference time: PyTorch `.pt` vs exported ONNX vs (if you have access) a Raspberry Pi/Jetson Nano — even a laptop-CPU-only benchmark table is enough to demo "this runs without a GPU."
3. Record FPS and model size before/after export in a short table for your pitch deck — this single artifact answers "is this actually edge-feasible?" without needing real bus hardware.
4. If you have a Raspberry Pi or Jetson available, running the ONNX model on it live during the demo is a strong differentiator; if not, the benchmark table alone is credible.

**D. Real-time alerting (extends Phase 6)**
1. Add a WebSocket endpoint to your FastAPI backend (`@app.websocket("/ws/alerts")`) — FastAPI supports this natively, no extra library needed.
2. When a high-priority event is ingested (e.g., `incident_type: "hit_and_run"` or `plate_confidence > 0.8`), broadcast it to all connected WebSocket clients immediately.
3. On the dashboard (Phase 5), open a WebSocket connection in `app.js` and show a toast/notification the instant an alert arrives, instead of requiring a page refresh.
4. This directly satisfies "reliable alerts" as a live, pushed experience rather than a query-only report.

**E. Closed-loop resolution verification (new, small)**
1. Add an admin action in the dashboard: a "Mark Resolved" button on any event popup → `PATCH /events/{id}` sets `status: "resolved"`.
2. Add a background check (can be a manual "re-check" button for demo purposes, or a cron-style script): if a bus passes within the same GPS radius again and the model does NOT detect the defect anymore, auto-set `status: "auto_confirmed_resolved"`.
3. For the hackathon demo, this can be simulated: re-run your detection script on a version of the test video without the defect, at the "same" GPS point, and show the dashboard status flip automatically.

### 4. Resources
| Type | Link |
|---|---|
| FastAPI WebSockets | https://fastapi.tiangolo.com/advanced/websockets/ |
| YOLOv8 export to ONNX | https://docs.ultralytics.com/modes/export/ |
| Haversine distance (Python, no extra deps needed) | standard formula, ~10 lines, no library required |
| HTTPS with self-signed cert (uvicorn) | https://www.uvicorn.org/deployment/#running-with-https |

### 5. Deliverable
- Backend runs over HTTPS with API-key auth
- Bus scripts retry-and-queue on failure, flush when reconnected
- Duplicate pothole sightings collapse into one event with a rising `confirmation_count`, and only `verified` events are shown by default
- An ONNX-exported model + a benchmark table (FPS, size, before/after) ready for the pitch deck
- Dashboard shows a live toast notification within ~1 second of a high-priority event being ingested, via WebSocket
- At least one defect can be marked "resolved" manually, and one can be shown auto-confirming resolved when the model stops detecting it at the same location

### 6. Folder structure added
```
urban-intel-project/
├── backend/
│   ├── main.py                       (modified: +HTTPS, +API key check, +WebSocket endpoint, +dedup query)
│   ├── security.py                   <- NEW (API key validation)
│   ├── dedup.py                      <- NEW (Haversine distance + confirmation-count logic)
│   ├── alerts_ws.py                  <- NEW (WebSocket broadcast manager)
│   ├── cert.pem / key.pem            <- NEW (self-signed, local dev only, .gitignore this)
├── src/
│   ├── detect_potholes.py            (modified: +retry-with-backoff, +local queue fallback)
│   └── export_onnx.py                <- NEW (model export + benchmark script)
├── dashboard/
│   └── app.js                        (modified: +WebSocket listener, +toast notifications, +"Mark Resolved" button)
├── docs/
│   └── edge_benchmark_table.png      <- NEW (FPS/size comparison for pitch deck)
```

---

## Updated Quick Reference — Time Budget

| Phase | Feature area | Time |
|---|---|---|
| 0-10 | (as before) | ~18-23 days |
| **11** | **Secure transmission + dedup + edge proof + real-time alerts + closed-loop** | **+2-3 days** |
| **Total** | | **~20-26 days solo, full scope** |

**If your hard limit is 1-2 weeks:** Phases 0-5 stay your core. From Phase 11, cherry-pick just **B (dedup)** and **C (ONNX export/benchmark)** — together under half a day of extra work — since those two single-handedly answer the two questions judges ask most: "won't the same pothole get logged 100 times?" and "does this actually run on edge hardware?"
