# 🎬 Phase 8 Multi-Video Real Validation Report

> **Validation Script**: [`src/detection/validate_pedestrian_video.py`](../../src/detection/validate_pedestrian_video.py)  
> **Tested Videos**: `data/sample_videos/crossign.mp4`, `data/sample_videos/pedestrian_ipid.mp4`, `data/sample_videos/traffic_density_bridge.mp4`

---

## 1. Multi-Video Benchmark Summary

| Video Stream File | Resolution | Frames | Speed (FPS) | Pedestrians | Vehicles | Crosswalks | Video Type |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`crossign.mp4`** | `720x480 @ 30 FPS` | 463 | **80.22 FPS** | 0 | 0 | **443** | Crosswalk Infrastructure Stream |
| **`pedestrian_ipid.mp4`** | `1920x1080 @ 30 FPS` | 318 | **59.50 FPS** | **68** | **85** | 0 | IPID Real Pedestrian Stream |
| **`traffic_density_bridge.mp4`** | `1920x1080 @ 24 FPS` | 576 | **60.28 FPS** | 0 | 1 | 0 | Bridge Traffic Stream |

---

## 2. Empirical Detection Breakdown

### A. IPID Real Pedestrian Video Stream (`pedestrian_ipid.mp4`)
- **Video Source**: [`data/sample_videos/pedestrian_ipid.mp4`](../../data/sample_videos/pedestrian_ipid.mp4)
- **Output Video**: [`outputs/pedestrian_ipid_annotated.mp4`](../../outputs/pedestrian_ipid_annotated.mp4)
- **Inference Speed**: **59.50 FPS**
- **Pedestrian Bounding Boxes**: **68 detections**
- **Vehicle Bounding Boxes**: **85 detections**

### B. Crosswalk Video Stream (`crossign.mp4`)
- **Video Source**: [`data/sample_videos/crossign.mp4`](../../data/sample_videos/crossign.mp4)
- **Output Video**: [`outputs/crossign_annotated.mp4`](../../outputs/crossign_annotated.mp4)
- **Inference Speed**: **80.22 FPS**
- **Crosswalk Bounding Boxes**: **443 detections** (**95.68% coverage**)

---

## 3. Honest Telemetry Verification

- **GPS Telemetry**: `UNAVAILABLE (latitude: null, longitude: null)`
- **School-Zone Context**: `UNAVAILABLE`
- **Pedestrian Risk Score**: `UNAVAILABLE`
