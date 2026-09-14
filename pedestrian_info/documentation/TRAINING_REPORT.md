# 🏋️ Phase 8 Training Report

> **Subsystem**: Phase 8 Pedestrian & Crosswalk Safety Analytics  
> **Model Weights**: `models/pedestrian/pedestrian_detector.pt`

---

## 1. Pre-Training Configuration

- **Dataset**: `pedestrian_info/pedestrian` (smart-crossing-version-1)
- **Total Dataset Images**: **7,737 images**
  - Train Split: `5,415 images`
  - Validation Split: `1,547 images`
  - Test Split: `775 images`
- **Base Architecture**: YOLOv8 Transfer Learning (`models/yolov8n.pt`)
- **Hardware Acceleration**: Apple Silicon MPS (Metal Performance Shaders)
- **Hyperparameters**:
  - `epochs`: **8**
  - `imgsz`: **416**
  - `batch`: **64** (106 iterations per epoch)
  - `workers`: **2**
  - `optimizer`: **AdamW** (lr=0.001429)

---

## 2. Training Loss & Convergence Metrics

| Epoch | GPU Memory | Box Loss | Class Loss | DFL Loss | Iterations | Time / Epoch |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 7.30 GB | 1.551 | 2.004 | 1.267 | 106 / 106 | ~1.5 min |
| **2** | 7.29 GB | 1.428 | 1.154 | 1.181 | 106 / 106 | ~1.5 min |
| **3** | 7.29 GB | 1.401 | 1.071 | 1.180 | 106 / 106 | ~1.5 min |
| **4** | 7.30 GB | 1.383 | 1.025 | 1.169 | 106 / 106 | ~1.5 min |
| **5** | 7.29 GB | 1.329 | 0.916 | 1.135 | 106 / 106 | ~1.5 min |
| **6** | 7.29 GB | 1.279 | 0.862 | 1.121 | 106 / 106 | ~1.5 min |
| **7** | 7.29 GB | 1.243 | 0.810 | 1.088 | 106 / 106 | ~1.5 min |
| **8** | 7.30 GB | 1.168 | 0.739 | 1.068 | 106 / 106 | ~1.5 min |

---

## 3. Training Run Artifacts

- **Weights Directory**: [`runs/pedestrian_detection_v1/weights/best.pt`](../runs/pedestrian_detection_v1/weights/best.pt)
- **Model Checksum (SHA256)**: `18d6e7c72fccde6dec294b02ab5c06ee73c89302f319234f857c7915549b1c9d`
- **Plots & Metrics Log**: [`runs/pedestrian_detection_v1/results.csv`](../runs/pedestrian_detection_v1/results.csv)
