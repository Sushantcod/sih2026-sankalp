# Phase 1 Active Model Replacement & SHA-256 Checksum Log

---

## 1. Overview
This document records the official verification and replacement of the active production model `models/pothole.pt` with the newly trained Phase 1 6-class model (`runs/multiclass_road_damage_final/weights/best.pt`).

---

## 2. SHA-256 Checksum Verification Matrix

| Model Asset | File Path | SHA-256 Checksum | Verification Status |
|:---|:---|:---|:---:|
| **Authoritative Trained Model** | `runs/multiclass_road_damage_final/weights/best.pt` | `947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b` | Source Master |
| **Active System Model** | `models/pothole.pt` | `947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b` | **Identical Copy** |
| **Preserved Previous Backup** | `models/pothole_previous.pt` | `8ae3f0fa1d72ce45e74e5f60a48f6aa1da44354971f945f77495c7f157d03420` | Preserved |

```
Verification Result:
models/pothole.pt === runs/multiclass_road_damage_final/weights/best.pt (EXACT MATCH)
```

---

## 3. Verified Active Model Class Mapping

Loaded directly from `models/pothole.pt`:
- `0`: `longitudinal_crack`
- `1`: `transverse_crack`
- `2`: `alligator_crack`
- `3`: `pothole`
- `4`: `manhole`
- `5`: `waterlogging`

---

## 4. Default Application Model Smoke Test

Executed default application CLI command without extra model flags:
```bash
python3 src/detect_potholes.py --source "data/sample_videos/pothole_road_damage.mp4" --conf 0.40 --clean-events
```

- **Default Model Path Loaded**: `models/pothole.pt`
- **Result**: **PASS**
- **Frames Processed**: 375 frames
- **Processing Time**: 8.11 seconds
- **Inference Speed**: **46.25 FPS**
- **Detections Logged**: 1,005 total (`pothole`: 1,001, `manhole`: 4)
- **Telemetry Event Log**: `outputs/events.jsonl`
- **Annotated Video Written**: `outputs/annotated_output.mp4`

---

## 5. Distinction: Application Smoke Test vs. Dedicated Real-Video Verification

- **Default Application Smoke Test**:
  - Command: `python3 src/detect_potholes.py --source ... --conf 0.40`
  - Purpose: Verify default system integration and telemetry event logging (`outputs/events.jsonl`).
  - Speed: 46.25 FPS (8.11s total time for 375 frames).
- **Dedicated Real-Video Verification Run**:
  - Command: Direct `model.predict()` pipeline run on `pothole_road_damage.mp4`.
  - Purpose: Frame-by-frame visual audit, bounding box spatial tracking, and manual error inspection.
  - Speed: 68.98 FPS (5.44s total time for 375 frames).
  - Findings: 1,001 pothole boxes (across 341 frames), 4 manhole boxes (across 4 frames), minor false positives around dark roadside shadows (frames 115-125), faint background cracks unannotated at 0.40 conf, waterlogging unobserved (0 detections).
