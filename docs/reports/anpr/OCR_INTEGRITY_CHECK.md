# ANPR OCR System Integrity Check Report

**Verification Timestamp**: 2026-09-13T23:38:20Z  
**Verification Auditor**: Antigravity Automated Verification Engine  

---

## 1. Safety & Isolation Verification

| Boundary / Asset | Target File Path | Expected SHA-256 Checksum | Measured SHA-256 Checksum | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1 Pothole Model** | `models/pothole.pt` | `947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b` | `947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b` | **PASS (Untouched)** |
| **ANPR Detector Weights** | `anpr/runs/anpr_detection_v1/weights/best.pt` | `d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a` | `d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a` | **PASS (Untouched)** |
| **Source ANPR Datasets** | `anpr/combined_dataset/ocr/` | N/A (1,651 images & 1,651 labels) | 1,651 images & 1,651 labels | **PASS (Untouched)** |
| **OCR Training Execution** | N/A | No OCR training requested | 0 training runs executed | **PASS (No Training)** |

---

## 2. Execution Artifact Checksums

| Execution Script / Output | File Path | SHA-256 Checksum | Status |
| :--- | :--- | :--- | :--- |
| **Input Test Video** | `data/sample_videos/anpr.mp4` | `83fad1739bacb3c7e00077e11b1da90194fbb10b73c666e0745ba9923efad3d1` | Verified |
| **Output Annotated Video** | `anpr/outputs/anpr_ocr_v1/anpr_ocr_video_annotated.mp4` | `7972dca6a3c8d603e41b30dc35e55c5cfa2e1cf1027c9e189c8cef900096c234` | Verified |
| **OCR Data Audit Script** | `scratch/ocr_data_audit.py` | `a391f0443052ab9583294a766d1e238dc798c3c5c4006691c927347ed424a5d7` | Verified |
| **OCR Benchmark Script** | `scratch/benchmark_ocr.py` | `9b27e86bbeb8d09d03b4caf4f7ffc7b0743f5ea383cc54711b8ae905d78600ae` | Verified |
| **OCR Integration Script** | `scratch/integrated_ocr_test.py` | `3f0ac862d9523e92ec13b13cb8a82cea45163c6fd71c321f077510cea365c0f0` | Verified |

---

## 3. Compliance Verification Checklist

- [x] **No Fabricated Data**: All numbers, accuracies, CERs, and FPS rates are measured empirically.
- [x] **No OCR Model Training**: Zero weights modified or trained during Phase 3 OCR benchmark.
- [x] **Phase 1 Isolation**: `models/pothole.pt` remains 100% untouched with matching SHA-256.
- [x] **Phase 2 Isolation**: Vehicle detection codebase untouched.
- [x] **Output Video Generated**: Annotated MP4 exists and rendered cleanly at `anpr/outputs/anpr_ocr_v1/anpr_ocr_video_annotated.mp4`.
