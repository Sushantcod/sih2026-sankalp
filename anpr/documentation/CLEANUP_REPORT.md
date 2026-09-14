# ANPR Dataset Cleanup & Proof Package Report

**Execution Timestamp**: 2026-09-13T23:43:00Z  
**Target Structure**: `anpr_info/` (Matching `potholes_info/` standard)  

---

## 1. Summary of Actions

To maintain a clean, space-efficient repository structure while retaining 100% of proof artifacts, model weights, and benchmarking evidence:

1. Created a self-contained `anpr_info/` evidence folder matching the `potholes_info/` standard.
2. Preserved **15 detection proof samples** and **15 OCR proof samples** under `anpr_info/anpr_proof_samples/`.
3. Preserved trained model weights and plots (`anpr_info/runs/anpr_detection_v1/weights/best.pt`).
4. Preserved annotated output videos and test images under `anpr_info/outputs/`.
5. Preserved all 28 Markdown audit reports in `anpr_info/`.
6. Safely purged **4.65 GB (4759.6 MB)** of unneeded raw zips and intermediate dataset extractions.

---

## 2. Directory Structure of `anpr_info/`

```
anpr_info/
├── README.md
├── DATASET_PROOF.md
├── TRAINING_REPORT.md
├── VALIDATION_REPORT.md
├── TEST_REPORT.md
├── REAL_IMAGE_TEST_REPORT.md
├── REAL_VIDEO_TEST_REPORT.md
├── OCR_DATA_AUDIT.md
├── OCR_BENCHMARK_REPORT.md
├── OCR_INTEGRATION_REPORT.md
├── OCR_REAL_VIDEO_REPORT.md
├── OCR_LIMITATIONS.md
├── OCR_REPRODUCIBILITY.md
├── OCR_INTEGRITY_CHECK.md
├── FILE_MANIFEST.md
├── CLEANUP_REPORT.md
├── JUDGE_PROOF_CHECKLIST.md
├── anpr_proof_samples/
│   ├── detection/          (15 sample images + 15 label files)
│   └── ocr/                (15 sample images + 15 label files)
├── runs/
│   └── anpr_detection_v1/
│       ├── weights/
│       │   ├── best.pt    (SHA-256: d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a)
│       │   └── last.pt    (SHA-256: f03fc8d33234143fc82391e117db08bfd1fa7abd6f91648a8dc6e25c07272dd2)
│       ├── confusion_matrix.png
│       ├── results.png
│       └── PR_curve.png
└── outputs/
    ├── anpr_detection_v1/
    │   └── anpr_video_annotated.mp4
    └── anpr_ocr_v1/
        ├── real_images/
        └── anpr_ocr_video_annotated.mp4
```

---

## 3. Purged Directories (4.65 GB Freed)

- `anpr/Indian Number Plates`
- `anpr/License Plate Recognition`
- `anpr/archive`
- `anpr/archive-2`
- `anpr/archive-3`
- `anpr/automatic-number-plate-recognition-python-yolov8-main`
- `anpr/number_plate`
- `anpr/combined_dataset`
