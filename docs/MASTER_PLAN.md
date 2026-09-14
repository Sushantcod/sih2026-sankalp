# MASTER PLAN — Full Project Detail, Phase-by-Phase + Project Structure

This document gives you, for **every phase**: the objective, exactly what to build, which repo/model/dataset to use, what to learn, the deliverable, time estimate, AND the exact folder/file structure that phase adds to your project. At the very end is the **full combined project structure** once all phases are done.

---

## HOW TO READ THIS DOCUMENT
Each phase below has 6 parts:
1. **Objective** — what this phase achieves
2. **Problem-statement features covered** — mapped back to the original BEL problem statement
3. **Build steps** — detailed, in order
4. **Resources** — existing repo/model/dataset + YouTube to learn from
5. **Deliverable** — what "done" looks like, testable
6. **Folder structure added** — exact files this phase creates

---

# PHASE 0 — Environment & Foundations
**Time: 2-3 days (parallel with Phase 1)**

### 1. Objective
Get your machine ready, learn just enough of each core tool to be dangerous, and confirm the base pipeline runs (already done in your zip).

### 2. Features covered
Foundational — no specific feature, enables everything else.

### 3. Build steps
1. Install Python 3.10+, create a virtual environment.
2. `pip install -r requirements.txt` (ultralytics, opencv-python-headless).
3. Run the existing `detect_potholes.py` on a sample image to confirm setup (already verified working).
4. Watch first 30-45 min of the YOLOv8 beginner video and the Python/OpenCV video (don't finish them — learn-by-doing from here).
5. Set up a GitHub repo for your project (private is fine) — commit early and often; judges sometimes ask to see commit history as proof of solo work over time.

### 4. Resources
| Type | Link |
|---|---|
| Python/CV basics | https://www.youtube.com/watch?v=N3adGK66myE |
| YOLOv8 basics | https://www.youtube.com/watch?v=OSwsMVkMpNU |

### 5. Deliverable
- Working Python environment
- `detect_potholes.py` runs successfully on a test image (already confirmed)
- GitHub repo initialized

### 6. Folder structure added
```
urban-intel-project/
├── requirements.txt
├── README.md
├── .gitignore
├── venv/                      (local only, not committed)
```

---

# PHASE 1 — Pothole / Road Defect Detection
**Time: 1-2 days | Status: mostly done**

### 1. Objective
Real-time detection of potholes/road damage from bus camera footage, converted into structured events.

### 2. Features covered
- Potholes / damaged road surfaces (core)
- Other general road hazards (folded in as extra classes if available)

### 3. Build steps
1. Download pretrained pothole weights (Hugging Face `vinothvikas1987/pothole-detection-yolov8`, or clone `arpy8/Pothole_Detection_YOLOv8`).
2. Place weights at `models/pothole.pt`.
3. Run `src/detect_potholes.py --source <video> --weights models/pothole.pt --save-video`.
4. Tune `CONF_THRESHOLD` in the script until false positives are acceptable.
5. (Optional, if time allows) Fine-tune your own model using the Roboflow pothole dataset in Google Colab for a stronger "we trained our own model" pitch point.

### 4. Resources
| Type | Link |
|---|---|
| Pretrained model | https://huggingface.co/vinothvikas1987/pothole-detection-yolov8 |
| Alt repo | https://github.com/arpy8/Pothole_Detection_YOLOv8 |
| Segmentation (severity) | https://github.com/FarzadNekouee/YOLOv8_Pothole_Segmentation_Road_Damage_Assessment |
| Dataset (to train yourself) | https://universe.roboflow.com/masseydigital/pothole-detection-yolov8-ncbid |
| Custom training tutorial | https://www.youtube.com/watch?v=m9fH9OWn8YM |

### 5. Deliverable
- `models/pothole.pt` present
- Running the script on a real road video produces bounding boxes on potholes + `outputs/events.jsonl` with `event_type: "pothole"` entries

### 6. Folder structure added
```
urban-intel-project/
├── models/
│   └── pothole.pt                    <- NEW
├── data/
│   └── sample_videos/
│       └── road_test_1.mp4           <- NEW (your test clips)
├── src/
│   └── detect_potholes.py            (already exists)
└── outputs/
    ├── events.jsonl
    └── annotated_output.mp4
```

---

# PHASE 2 — Vehicle Density & Counting
**Time: 1 day**

### 1. Objective
Detect, classify, and count vehicles per time window to estimate traffic density and flag congestion.

### 2. Features covered
- Vehicle density estimation (detection, classification, counting)
- Traffic bottleneck/congestion identification

### 3. Build steps
1. Copy `detect_potholes.py` → `detect_vehicles.py` as a starting point (same event-JSON pattern).
2. Use plain `yolov8n.pt`/`yolov8s.pt` (COCO) — filter detections to classes `car, bus, truck, motorcycle`.
3. Add a rolling counter: count vehicles per 10-second window.
4. Add a simple threshold rule: if count > N (tune N by testing) → emit a `congestion` event type in addition to individual vehicle counts.
5. Test on a busy-road sample video vs a quiet-road sample video to confirm the threshold behaves sensibly.

### 4. Resources
| Type | Link |
|---|---|
| Ready repo | https://github.com/VuBacktracking/yolo-bytetrack-vehicle-tracking |
| Repo with line-counter + TensorRT export | https://github.com/arief25ramadhan/vehicle-tracking-counting |
| Tutorial | https://www.classcentral.com/course/youtube-track-count-objects-using-yolov8-bytetrack-supervision-126793 |

### 5. Deliverable
- `src/detect_vehicles.py` runs on a video, outputs vehicle counts per class per time window
- `outputs/events.jsonl` gains `event_type: "vehicle_count"` and `event_type: "congestion"` entries

### 6. Folder structure added
```
urban-intel-project/
├── src/
│   ├── detect_potholes.py
│   └── detect_vehicles.py            <- NEW
├── data/
│   └── sample_videos/
│       └── traffic_test_1.mp4        <- NEW
```

---

# PHASE 3 — ANPR (Automatic Number Plate Recognition)
**Time: 2 days**

### 1. Objective
Detect vehicle number plates and extract the registration text with a confidence score.

### 2. Features covered
- ANPR with confidence score (part of incident handling)

### 3. Build steps
1. Clone the reference repo directly (it matches its own video tutorial exactly, easiest to follow):
   `git clone https://github.com/computervisioneng/automatic-number-plate-recognition-python-yolov8`
2. Study its structure: vehicle detector → plate detector → OCR (EasyOCR).
3. Adapt the OCR + confidence-score output into your own event JSON schema (`event_type: "plate_detected"`, `plate_number`, `plate_confidence`).
4. If running on CPU is too slow, install `parkocr` (`pip install parkocr[lite]`) as a lighter alternative (~90MB, CPU-optimized).
5. Test against Indian plates specifically — accuracy will be lower than the demo video (Western plates); note this honestly, consider the `samay-jain` Indian-plate-focused repo as an upgrade if time allows.

### 4. Resources
| Type | Link |
|---|---|
| Main repo (matches tutorial) | https://github.com/computervisioneng/automatic-number-plate-recognition-python-yolov8 |
| Matching video | https://www.youtube.com/watch?v=fyJB1t0o0ms |
| Indian-plate-focused alt | https://github.com/samay-jain/Advanced-Automatic-Number-Plate-Recognition-System-ANPR- |
| Lightweight CPU package | `pip install parkocr[lite]` (PyPI) |

### 5. Deliverable
- `src/detect_plates.py` takes a video, outputs plate text + confidence for each detected vehicle
- `outputs/events.jsonl` gains `event_type: "plate_detected"` entries

### 6. Folder structure added
```
urban-intel-project/
├── src/
│   ├── detect_potholes.py
│   ├── detect_vehicles.py
│   └── detect_plates.py              <- NEW
├── models/
│   ├── pothole.pt
│   └── plate_detector.pt             <- NEW (from cloned repo or parkocr)
```

---

# PHASE 4 — Backend Ingestion API
**Time: 1-2 days**

### 1. Objective
A central server that receives JSON events from all "buses" (your scripts), stores them, and serves them to the dashboard.

### 2. Features covered
- Secure transmission to central command system
- Centralized platform data aggregation (foundation)

### 3. Build steps
1. `pip install fastapi uvicorn sqlalchemy`
2. Design the events table schema (mirrors your JSON: event_id, bus_id, event_type, confidence, lat, lon, timestamp, extra fields as JSON blob).
3. Build `POST /events` endpoint — accepts one event, validates with Pydantic, stores in SQLite.
4. Build `GET /events` endpoint — returns all events, with optional query params (`event_type`, `since`, `bbox` for map bounds).
5. Modify your Phase 1-3 scripts: instead of (or in addition to) writing to `events.jsonl`, POST each event to `http://localhost:8000/events`.
6. Test with `curl` or the FastAPI auto-generated Swagger UI (`/docs`).

### 4. Resources
| Type | Link |
|---|---|
| FastAPI beginner course | https://www.youtube.com/watch?v=tLKKmouUams |
| FastAPI crash course (Traversy) | https://www.youtube.com/watch?v=8TMQcRcBnW8 |

### 5. Deliverable
- `uvicorn main:app --reload` runs a live server
- Running any detection script now sends events to the API in real time
- `/docs` shows working Swagger UI with `GET`/`POST /events`

### 6. Folder structure added
```
urban-intel-project/
├── backend/
│   ├── main.py                       <- NEW (FastAPI app)
│   ├── models.py                     <- NEW (SQLAlchemy models)
│   ├── schemas.py                    <- NEW (Pydantic schemas)
│   ├── database.py                   <- NEW (DB connection/session)
│   └── events.db                     <- NEW (SQLite file, auto-created)
├── src/
│   ├── detect_potholes.py            (modified: now POSTs to API)
│   ├── detect_vehicles.py            (modified: now POSTs to API)
│   └── detect_plates.py              (modified: now POSTs to API)
```

---

# PHASE 5 — GIS Dashboard + Congestion Heatmap
**Time: 2 days**

### 1. Objective
A web dashboard showing all events on a map, with a heatmap layer for congestion/defect density.

### 2. Features covered
- GIS map visualization of all events
- Congestion heat maps

### 3. Build steps
1. Create a single `dashboard/index.html` — no build tooling needed, plain HTML + Leaflet via CDN (fastest for solo/hackathon).
2. Add Leaflet base map (OpenStreetMap tiles, free, no key).
3. Fetch `GET /events` from your FastAPI backend (enable CORS on the backend for local dev).
4. Plot each event as a marker, color-coded by `event_type` (red = pothole, orange = congestion, blue = incident, etc).
5. Add `Leaflet.heat` layer for congestion/defect density.
6. Add a simple sidebar/legend + event-type filter checkboxes.
7. Add click-on-marker popup showing event details (confidence, timestamp, plate number if applicable).

### 4. Resources
| Type | Link |
|---|---|
| Leaflet.heat plugin | https://github.com/Leaflet/Leaflet.heat |
| Tutorial | https://www.youtube.com/watch?v=mbRz6MTvDHk |

### 5. Deliverable
- Opening `dashboard/index.html` in a browser (served via a simple local HTTP server) shows a live map with pins from your backend, plus a working heatmap toggle

### 6. Folder structure added
```
urban-intel-project/
├── dashboard/
│   ├── index.html                    <- NEW
│   ├── style.css                     <- NEW
│   └── app.js                        <- NEW (fetch + Leaflet logic)
```

---

# PHASE 6 — Incident Tracking (Hit-and-Run / Rash Driving)
**Time: 2 days**

### 1. Objective
Track a specific offending vehicle across frames and flag rash-driving/hit-and-run behavior.

### 2. Features covered
- Detect and track offending vehicle
- Rash driving / hit-and-run flagging

### 3. Build steps
1. Use Ultralytics' built-in tracker: `model.track(source=video, tracker="bytetrack.yaml", persist=True)`.
2. For each tracked vehicle, store its bounding-box center position per frame.
3. Compute frame-to-frame displacement (pixels/frame) — large sudden displacement or erratic zig-zag pattern = "rash driving" heuristic flag.
4. On flag, capture the last N frames as a short evidence clip (`cv2.VideoWriter`, buffered).
5. Trigger your Phase 3 ANPR module specifically on the flagged/tracked vehicle's bounding box (crop + OCR) instead of scanning the whole frame — faster and more targeted.
6. Send a high-priority event (`event_type: "incident"`, `incident_type: "rash_driving"`) with the plate number, confidence, GPS, timestamp, and evidence clip reference to the backend.

### 4. Resources
| Type | Link |
|---|---|
| Tracking repo | https://github.com/MuhammadMoinFaisal/YOLOv8-DeepSORT-Object-Tracking |
| Tutorial | https://www.youtube.com/watch?v=Z3uquMElyzI |

### 5. Deliverable
- `src/track_incidents.py` — given a video, tracks vehicles, flags erratic ones, saves a short evidence clip, and sends an incident event with plate number to the backend

### 6. Folder structure added
```
urban-intel-project/
├── src/
│   └── track_incidents.py            <- NEW
├── outputs/
│   └── evidence_clips/               <- NEW (short flagged clips)
│       └── incident_<id>.mp4
```

---

# PHASE 7 — Infrastructure Deficiency View + O-D Analysis + Route Delay
**Time: 2-3 days (mostly backend/analytics, no new AI)**

### 1. Objective
Turn raw stored events into city-level insights: where infrastructure is lacking, how traffic flows between points, and how delayed routes are.

### 2. Features covered
- Infrastructure deficiency identification
- Origin–destination traffic pattern analysis
- Route delay estimation

### 3. Build steps
1. Add an `/analytics/deficiency` endpoint: `GROUP BY zone, event_type` on your events table → ranked list of worst zones.
2. Define a small fixed list of "route checkpoints" (e.g., 5 GPS points along your test route) with an "expected time" for each, in a JSON config file.
3. Add an `/analytics/route-delay` endpoint: for each simulated bus trip, compare actual timestamp-at-checkpoint (from your GPS-simulated events) vs expected → compute delay in minutes.
4. Add an `/analytics/od-pattern` endpoint: aggregate travel time between consecutive checkpoints across multiple simulated "trips" → identify the slowest segment.
5. Add a simple analytics panel to your dashboard (Phase 5) — a table or bar chart (Chart.js, CDN, no build step) showing these three outputs.

### 4. Resources
No new external repo needed — this is standard backend aggregation using SQL/pandas. If you want a refresher on SQL grouping/aggregation, any basic SQL tutorial works; not project-specific.

### 5. Deliverable
- Three working analytics endpoints
- Dashboard shows a "Worst Roads" table, a "Route Delay" chart, and a simple O-D segment summary

### 6. Folder structure added
```
urban-intel-project/
├── backend/
│   ├── analytics.py                  <- NEW (aggregation queries)
│   └── routes_config.json            <- NEW (checkpoint definitions)
├── dashboard/
│   └── analytics.js                  <- NEW (charts for the 3 endpoints)
```

---

# PHASE 8 — Pedestrian Safety (School Children Crossing)
**Time: 1 day**

### 1. Objective
Flag vulnerable pedestrian situations near school zones using detection + geofencing rules.

### 2. Features covered
- Detecting vulnerable pedestrian situations (school children crossing)

### 3. Build steps
1. Reuse plain YOLOv8 `person` class detection (no new model needed).
2. Create `data/school_zones.json` — a manually curated list of school GPS coordinates + radius (e.g., 5 schools, 100m radius each) for your demo city/route.
3. Add rule logic: if person-cluster (2+ detections close together) AND current simulated GPS falls within a school zone radius → emit `event_type: "vulnerable_pedestrian"`.
4. Be explicit in your pitch that this is rule-based context reasoning on top of generic detection, not true age/child classification — that's the honest and defensible framing.

### 4. Resources
Same YOLOv8 beginner tutorial as Phase 0 — no new model/repo needed.

### 5. Deliverable
- `src/detect_pedestrian_risk.py` flags events only when both conditions (person cluster + school zone) are met, tested against a school-zone sample video and a non-school-zone sample video to confirm it doesn't over-trigger

### 6. Folder structure added
```
urban-intel-project/
├── src/
│   └── detect_pedestrian_risk.py     <- NEW
├── data/
│   └── school_zones.json             <- NEW
```

---

# PHASE 9 — Remaining Road Infrastructure Checks
**Time: 2-3 days — pick 1 to build fully, mock the rest**

### 1. Objective
Cover zebra crossings, road dividers, signboards, and waterlogging — pick your strongest one to build for real.

### 2. Features covered
- Missing/faded zebra crossings
- Missing road dividers/medians
- Damaged/missing traffic signboards
- Waterlogging

### 3. Build steps (choose ONE to build fully; recommend signboards — best dataset availability)
1. Search Roboflow Universe for a relevant pretrained/labeled dataset (e.g., "traffic sign detection", GTSDB-based).
2. Fine-tune a YOLOv8 model the same way as Phase 1 (reuse that training recipe).
3. For "missing" logic specifically: create `data/expected_infrastructure.json` (GPS points where a zebra crossing/divider/sign SHOULD exist) and compare against detections at that location — no detection found there = flag "missing."
4. For the other 2-3 features you don't fully build: create a short architecture note + a mocked example event in `outputs/events.jsonl` (clearly labeled `"status": "simulated"`) so your dashboard can still visually demo the concept without a fully trained model.

### 4. Resources
| Type | Link |
|---|---|
| Search pattern | Roboflow Universe → search "traffic sign detection", "zebra crossing detection", "lane detection", "waterlogging detection" |
| Training recipe | Same as Phase 1 — https://www.youtube.com/watch?v=m9fH9OWn8YM |

### 5. Deliverable
- One fully working detector among {signboards, zebra crossing, dividers, waterlogging}
- A clear "Phase 2 roadmap" slide/section for the remaining ones (this is fine — be upfront in your pitch)

### 6. Folder structure added
```
urban-intel-project/
├── models/
│   └── signboard_detector.pt         <- NEW (or whichever you picked)
├── src/
│   └── detect_infrastructure.py      <- NEW
├── data/
│   └── expected_infrastructure.json  <- NEW
```

---

# PHASE 10 — Reports, Deployment & Pitch Prep
**Time: 2 days**

### 1. Objective
Package everything into a presentable, deployed, demoable product.

### 2. Features covered
- Actionable insights/reports for transport authorities
- Overall "Expected Solution" packaging

### 3. Build steps
1. Add a `/reports/export` endpoint using `reportlab` (PDF) or `pandas.to_csv()` (CSV) — export filtered event data.
2. Deploy backend (Render/Railway free tier) so your dashboard has a live URL, not just localhost.
3. Deploy dashboard as a static site (Netlify/Vercel free tier, or same host as backend).
4. Record a 2-3 min demo video: run a detection script live on a road video → show it appear on the dashboard in near-real-time → show the heatmap/analytics.
5. Build your pitch deck: Problem → Architecture diagram (from our earlier workflow doc) → What's New (from our earlier discussion) → Live demo → Roadmap (Phase 9 gaps, closed-loop verification, real hardware) → Impact.

### 4. Resources
No new technical resource — this phase is presentation, not code.

### 5. Deliverable
- Live deployed dashboard URL
- Exportable PDF/CSV report
- Recorded demo video
- Pitch deck ready

### 6. Folder structure added
```
urban-intel-project/
├── backend/
│   └── reports.py                    <- NEW
├── docs/
│   ├── architecture_diagram.png      <- NEW
│   ├── pitch_deck.pptx               <- NEW
│   └── demo_video.mp4                <- NEW
```

---

# FULL COMBINED PROJECT STRUCTURE (end state, after all 10 phases)

```
urban-intel-project/
├── README.md
├── ROADMAP.md
├── MASTER_PLAN.md                          (this document)
├── requirements.txt
├── .gitignore
│
├── models/
│   ├── pothole.pt                          [Phase 1]
│   ├── plate_detector.pt                   [Phase 3]
│   └── signboard_detector.pt               [Phase 9]
│
├── data/
│   ├── sample_videos/
│   │   ├── road_test_1.mp4                 [Phase 1]
│   │   └── traffic_test_1.mp4              [Phase 2]
│   ├── sample_images/
│   ├── school_zones.json                   [Phase 8]
│   └── expected_infrastructure.json        [Phase 9]
│
├── src/
│   ├── detect_potholes.py                  [Phase 1]
│   ├── detect_vehicles.py                  [Phase 2]
│   ├── detect_plates.py                    [Phase 3]
│   ├── track_incidents.py                  [Phase 6]
│   ├── detect_pedestrian_risk.py           [Phase 8]
│   └── detect_infrastructure.py            [Phase 9]
│
├── backend/
│   ├── main.py                             [Phase 4]
│   ├── models.py                           [Phase 4]
│   ├── schemas.py                          [Phase 4]
│   ├── database.py                         [Phase 4]
│   ├── analytics.py                        [Phase 7]
│   ├── routes_config.json                  [Phase 7]
│   ├── reports.py                          [Phase 10]
│   └── events.db
│
├── dashboard/
│   ├── index.html                          [Phase 5]
│   ├── style.css                           [Phase 5]
│   ├── app.js                              [Phase 5]
│   └── analytics.js                        [Phase 7]
│
├── docs/
│   ├── architecture_diagram.png            [Phase 10]
│   ├── pitch_deck.pptx                     [Phase 10]
│   └── demo_video.mp4                      [Phase 10]
│
└── outputs/
    ├── events.jsonl
    ├── annotated_output.mp4
    └── evidence_clips/
        └── incident_<id>.mp4               [Phase 6]
```

---

# QUICK REFERENCE — Time Budget Summary

| Phase | Feature area | Time |
|---|---|---|
| 0 | Setup & learning | 2-3 days (parallel) |
| 1 | Pothole detection | 1-2 days |
| 2 | Vehicle density/counting | 1 day |
| 3 | ANPR | 2 days |
| 4 | Backend API | 1-2 days |
| 5 | GIS dashboard + heatmap | 2 days |
| 6 | Incident tracking | 2 days |
| 7 | Deficiency + O-D + delay analytics | 2-3 days |
| 8 | Pedestrian/school-zone safety | 1 day |
| 9 | Remaining infra checks (1 real + mocks) | 2-3 days |
| 10 | Reports + deployment + pitch | 2 days |
| **Total** | | **~18-23 days solo, full scope** |

**If your hard limit is 1-2 weeks:** do Phases 0-5 only (core AI + backend + dashboard, ~9-11 days) and present Phases 6-10 as a documented roadmap with mocked example data — which is exactly what this document gives you the credibility to do.
