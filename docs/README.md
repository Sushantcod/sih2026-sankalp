# Urban Intelligence Platform — Solo Build (1-2 Weeks, Laptop/CPU)

## Status right now
✅ Project scaffolding created
✅ `src/detect_potholes.py` — working detection pipeline, tested end-to-end
✅ Generates structured JSON events (matches the central-platform schema)
✅ Runs on CPU (no GPU needed — slower, but fine for a demo)
⏳ Currently using COCO-pretrained weights (detects bus/person/car etc, NOT potholes yet)
👉 **Next action for you: get a real pothole-trained model (Step 2 below)**

---

## Step 0 — Setup on your laptop

```bash
# 1. Clone/copy this project folder to your laptop
# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Step 1 — Confirm the pipeline works (using COCO model, no download needed)

```bash
python src/detect_potholes.py --source path/to/any/road_photo.jpg
```

This proves your environment works before touching the pothole-specific model.
It will detect generic COCO classes (car, bus, person, truck) — not potholes yet.

## Step 2 — Get a real pothole detection model (do this on your laptop, needs internet)

Pick ONE of these (easiest first):

**Option A — Hugging Face (fastest, no training needed)**
```bash
pip install huggingface_hub
python -c "
from huggingface_hub import hf_hub_download
path = hf_hub_download(repo_id='vinothvikas1987/pothole-detection-yolov8', filename='best.pt')
print(path)
"
# Copy the downloaded file into: models/pothole.pt
```
If the exact filename differs, check the repo's "Files" tab on huggingface.co and
copy the correct `.pt` filename.

**Option B — GitHub pretrained repo**
Clone one of these and grab the `.pt` file from it:
- https://github.com/arpy8/Pothole_Detection_YOLOv8
- https://github.com/FarzadNekouee/YOLOv8_Pothole_Segmentation_Road_Damage_Assessment (gives segmentation/severity too)

**Option C — Train it yourself (best for your report, ~30-60 min on free Colab GPU)**
1. Go to Roboflow Universe → search "pothole detection yolov8" → pick a dataset (e.g., masseydigital's) → export in "YOLOv8" format.
2. In Google Colab (free GPU):
```python
!pip install ultralytics
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
model.train(data='path/to/data.yaml', epochs=50, imgsz=640)
```
3. Download `runs/detect/train/weights/best.pt` → put it in `models/pothole.pt`

**Recommendation given your 1-2 week timeline:** Do Option A or B today (5 minutes) to keep moving, then do Option C later in the week if you have spare time — training your own model is a strong talking point ("we fine-tuned our own model on an Indian road dataset") even if you also keep a pretrained fallback.

## Step 3 — Run detection with the real pothole model

```bash
python src/detect_potholes.py --source path/to/road_video.mp4 --weights models/pothole.pt --save-video
```

Get test videos: search YouTube for "India dashcam road drive" and download a short clip
(e.g. with `yt-dlp`), or use your phone to film a short drive.

---

## Day-by-Day Plan (1-2 weeks, solo, laptop/CPU)

### Days 1-2 — Pothole detection (you are here)
- [x] Pipeline scaffolding done
- [ ] Get real pothole weights (Step 2 above)
- [ ] Test on 2-3 sample road videos, tune `CONF_THRESHOLD` in the script
- [ ] Add a second class if your model supports it (waterlogging/cracks) — check `model.names`

### Days 3-4 — Vehicle detection & density
- [ ] Reuse `detect_potholes.py` logic (it's generic) with plain `yolov8n.pt` — COCO already has car/bus/truck/motorcycle
- [ ] Add a simple density calculation: count vehicles per N frames → "vehicles per minute" score
- [ ] Add congestion threshold logic (e.g., >15 vehicles/frame window = "congested")

### Days 5-6 — ANPR (number plate recognition)
- [ ] `pip install easyocr`
- [ ] Find/download a plate-detection YOLO model (Roboflow has Indian plate datasets) OR just OCR the full frame region near detected vehicles as a simpler v1
- [ ] Add confidence score output to the same event JSON schema

### Days 7-8 — Backend (ingestion API)
- [ ] `pip install fastapi uvicorn`
- [ ] Build a `/events` POST endpoint that accepts the JSON schema you're already producing
- [ ] Store in SQLite first (simplest — upgrade to PostgreSQL+PostGIS only if time permits)
- [ ] Modify `detect_potholes.py` to POST events to this API instead of (or in addition to) the local file

### Days 9-10 — Dashboard (GIS map)
- [ ] Simple React + Leaflet page, OR even simpler: a single HTML file with Leaflet.js (no build step needed) that fetches from your FastAPI `/events` endpoint and plots pins
- [ ] Add a heatmap layer (`leaflet.heat`)
- [ ] Add basic filter by event type

### Days 11-12 — Integration + polish
- [ ] Connect all 3 detection modules to write to the same backend
- [ ] Add the deduplication logic (GPS-proximity based confirmation count) — this is a strong differentiator, don't skip it
- [ ] Basic analytics: counts by category, simple bar chart

### Days 13-14 — Pitch prep
- [ ] Record a demo video (screen recording of dashboard + detection running on a road video)
- [ ] Prepare architecture diagram + "what's new" slide (we already scripted this)
- [ ] Mock up the features you didn't fully build (school-crossing, hit-and-run tracking) as roadmap slides — be upfront these are "architecture-ready, next phase"

---

## Hardware note (for later)
You mentioned adding real hardware after the software works — good approach. When you do:
- A **Jetson Nano/Orin Nano** is the standard choice for running YOLO models onboard a vehicle (low power, decent inference speed).
- The exact same `detect_potholes.py` script (or its ONNX-exported version, `model.export(format='onnx')`) runs on Jetson with minimal changes — that's the benefit of building it generically now.

## File structure
```
urban-intel-project/
├── requirements.txt
├── README.md
├── models/              <- put pothole.pt here
├── data/
│   ├── sample_videos/
│   └── sample_images/
├── src/
│   └── detect_potholes.py
└── outputs/
    ├── events.jsonl      <- generated event log
    └── annotated_output.mp4/jpg
```
