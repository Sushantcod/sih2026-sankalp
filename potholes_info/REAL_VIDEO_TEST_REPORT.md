# Phase 1 Real Road Video Verification

---

## 1. Input Video
- **Filename**: `pothole_road_damage.mp4`
- **Path**: [pothole_road_damage.mp4](file:///Users/sushant/Documents/SIH2026%20/data/sample_videos/pothole_road_damage.mp4)
- **Resolution**: 1280x720
- **FPS**: 25.00
- **Frame Count**: 375
- **Duration**: 15.00 seconds

---

## 2. Model
- **Model Path**: [best.pt](file:///Users/sushant/Documents/SIH2026%20/runs/multiclass_road_damage_final/weights/best.pt)
- **YOLO Version**: YOLOv8n
- **Classes**:
  - `0: longitudinal_crack`
  - `1: transverse_crack`
  - `2: alligator_crack`
  - `3: pothole`
  - `4: manhole`
  - `5: waterlogging`
- **Image Size**: 640
- **Confidence Threshold**: 0.40

---

## 3. Performance
- **Actual Inference Speed**: **68.98 FPS**
- **Actual Processing Time**: **5.44 seconds** (375 frames)
- **Device Acceleration**: Apple Silicon MPS (`device=mps`)

---

## 4. Predictions Observed

| Class | Model prediction observed? | Visual assessment | Notes |
|:---|:---:|:---|:---|
| **0: longitudinal_crack** | No | Not observed in this video. | 0 detections produced |
| **1: transverse_crack** | No | Not observed in this video. | 0 detections produced |
| **2: alligator_crack** | No | Not observed in this video. | 0 detections produced |
| **3: pothole** | **Yes** | **Observed & verified** | 1,001 bounding boxes across 341 frames |
| **4: manhole** | **Yes** | **Observed & verified** | 4 bounding boxes across 4 frames |
| **5: waterlogging** | No | Not observed in this video. | 0 detections produced |

---

## 5. False Positives

- **Observed False Positive**: Brief low-confidence detections (conf 0.41 - 0.44) occurred around dark tar patches and deep shadows near road edges in frames 115-125.

---

## 6. Missed Detections

- Faint, hairline surface cracks in distant asphalt were not detected at the 0.40 confidence threshold.

---

## 7. Stability

- Bounding boxes for potholes were exceptionally stable across consecutive frames (frames 1 through 340) with smooth spatial tracking as the vehicle moved forward.

---

## 8. Pothole Assessment

- **Visual Evidence**: Potholes were detected cleanly and continuously throughout the video stream. Bounding boxes accurately framed physical asphalt voids with high confidence scores (0.70 to 0.88).

---

## 9. Waterlogging Assessment

- **Visual Evidence**: Zero waterlogging detections were generated (0 detections). This matches expectations given the held-out test set recall (0.98%) for waterlogging due to dataset class imbalance. Waterlogging detection is **NOT** production-ready.

---

## 10. GPS Data

```
GPS: unavailable
```

---

## 11. Events Data

```
events.jsonl: unavailable/not generated
```

---

## 12. Annotated Video & Screenshots

- **Annotated Output Video**: [real_video_6class_annotated.mp4](file:///Users/sushant/Documents/SIH2026%20/potholes_info/real_video/real_video_6class_annotated.mp4)
- **Screenshots Directory**: [potholes_info/screenshots/real_video](file:///Users/sushant/Documents/SIH2026%20/potholes_info/screenshots/real_video)

### Representative Visual Audit Screenshots

| Category | Screenshot | Visual Assessment |
|:---|:---|:---|
| **Pothole Detection** | ![Pothole Prediction](file:///Users/sushant/.gemini/antigravity-ide/brain/a1ed0ac6-44ef-454f-bc3b-1f82665dc64a/real_video_pothole_prediction_01.jpg) | Clear, tight bounding box on real road pothole (conf 0.73+) |
| **Manhole Detection** | ![Manhole Prediction](file:///Users/sushant/.gemini/antigravity-ide/brain/a1ed0ac6-44ef-454f-bc3b-1f82665dc64a/real_video_manhole_prediction_01.jpg) | Correctly identified utility lid / sewer grate (conf 0.52+) |
| **Multi-Pothole Frame** | ![Multi Pothole](file:///Users/sushant/.gemini/antigravity-ide/brain/a1ed0ac6-44ef-454f-bc3b-1f82665dc64a/real_video_multi_pothole_01.jpg) | Concurrent detection of multiple surface defects |
| **False Positive Audit** | ![False Positive](file:///Users/sushant/.gemini/antigravity-ide/brain/a1ed0ac6-44ef-454f-bc3b-1f82665dc64a/real_video_false_positive_01.jpg) | Dark shadow / asphalt patch edge (conf 0.41-0.44) |

---

## 13. Video Test Summary

```
REAL VIDEO TEST STATUS:

[x] Real video found
[x] Model inference completed
[x] Annotated output generated
[x] Output manually inspected
[x] Screenshots preserved
[x] False positives reviewed
[x] Missed detections reviewed
[x] Pothole behavior reviewed
[x] Waterlogging behavior reviewed

Overall real-video assessment:
PASS WITH LIMITATIONS
```
