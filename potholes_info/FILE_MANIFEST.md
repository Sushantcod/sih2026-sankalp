# Phase 1 Project File & Asset Preservation Manifest

---

## 1. Master Directory Structure

```
potholes_info/
├── README.md                          # Master Phase 1 Overview
├── DATASET_PROOF.md                   # Real Dataset Provenance & Pair Audit
├── TRAINING_REPORT.md                 # YOLOv8n Training Execution & Curves
├── VALIDATION_REPORT.md               # Validation Split Metrics (2,605 images)
├── TEST_REPORT.md                     # Held-Out Test Metrics (2,627 images)
├── REAL_VIDEO_TEST_REPORT.md          # Real Video Verification & Smoke Test
├── MODEL_REPLACEMENT_REPORT.md        # SHA-256 Checksum & Replacement Log
├── REPRODUCIBILITY_REPORT.md          # Environment & Commands
├── LIMITATIONS_REPORT.md              # Limitations & Failure Modes
├── FILE_MANIFEST.md                   # Asset Preservation Manifest
├── CLEANUP_REPORT.md                  # Intermediate Cleanup Log
├── INTEGRITY_CHECK.md                 # 12-Point Automated Integrity Matrix
├── JUDGE_PROOF_CHECKLIST.md           # Audit Compliance Checklist
├── real_video/                        # Video outputs
│   └── real_video_6class_annotated.mp4
└── screenshots/                       # Visual proof images
    ├── ground_truth/
    └── real_video/
```

---

## 2. Preserved System Weight Files
- `models/pothole.pt` (Active SHA256: `947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b`)
- `models/pothole_previous.pt` (Backup SHA256: `8ae3f0fa1d72ce45e74e5f60a48f6aa1da44354971f945f77495c7f157d03420`)
- `runs/multiclass_road_damage_final/weights/best.pt`
- `runs/multiclass_road_damage_final/weights/last.pt`

---

## 3. Preserved Master Dataset
- `potholes/train/images` (20,930 images)
- `potholes/train/labels` (20,930 labels)
- `potholes/valid/images` (2,605 images)
- `potholes/valid/labels` (2,605 labels)
- `potholes/test/images` (2,627 images)
- `potholes/test/labels` (2,627 labels)
- `potholes/data.yaml`
