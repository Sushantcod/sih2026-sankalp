# ANPR OCR Phase File Manifest

**Document Timestamp**: 2026-09-13T23:38:25Z  

---

## 1. Documentation Suite (`anpr/documentation/`)

- [`OCR_DATA_AUDIT.md`](file:///Users/sushant/Documents/SIH2026/anpr/documentation/OCR_DATA_AUDIT.md): Complete audit of 1,651 ground-truth OCR images & labels.
- [`OCR_BENCHMARK_REPORT.md`](file:///Users/sushant/Documents/SIH2026/anpr/documentation/OCR_BENCHMARK_REPORT.md): EasyOCR evaluation metrics (7.51% Exact Acc, 79.86% CER, error confusion matrix).
- [`OCR_INTEGRATION_REPORT.md`](file:///Users/sushant/Documents/SIH2026/anpr/documentation/OCR_INTEGRATION_REPORT.md): Integrated YOLOv8n + EasyOCR pipeline design & sample image results.
- [`OCR_REAL_VIDEO_REPORT.md`](file:///Users/sushant/Documents/SIH2026/anpr/documentation/OCR_REAL_VIDEO_REPORT.md): Evaluation on `data/sample_videos/anpr.mp4` (17.49 FPS, 5,256 detections).
- [`OCR_LIMITATIONS.md`](file:///Users/sushant/Documents/SIH2026/anpr/documentation/OCR_LIMITATIONS.md): Systemic limitations and preprocessing/custom OCR model recommendations.
- [`OCR_REPRODUCIBILITY.md`](file:///Users/sushant/Documents/SIH2026/anpr/documentation/OCR_REPRODUCIBILITY.md): Environment details and command line replication steps.
- [`OCR_INTEGRITY_CHECK.md`](file:///Users/sushant/Documents/SIH2026/anpr/documentation/OCR_INTEGRITY_CHECK.md): SHA-256 checksums and Phase 1/2 isolation proof.
- [`FILE_MANIFEST.md`](file:///Users/sushant/Documents/SIH2026/anpr/documentation/FILE_MANIFEST.md): Inventory of all generated scripts and output files.

---

## 2. Output Artifacts (`anpr/outputs/anpr_ocr_v1/`)

- [`real_images/`](file:///Users/sushant/Documents/SIH2026/anpr/outputs/anpr_ocr_v1/real_images/): Directory containing annotated test sample images with bounding boxes & OCR overlays.
- [`anpr_ocr_video_annotated.mp4`](file:///Users/sushant/Documents/SIH2026/anpr/outputs/anpr_ocr_v1/anpr_ocr_video_annotated.mp4): Annotated 1,800-frame video output file with detection bounding boxes and OCR text overlays.

---

## 3. Automation Scripts (`scratch/`)

- [`scratch/ocr_data_audit.py`](file:///Users/sushant/Documents/SIH2026/scratch/ocr_data_audit.py): Audits images, labels, character frequencies, and usability.
- [`scratch/benchmark_ocr.py`](file:///Users/sushant/Documents/SIH2026/scratch/benchmark_ocr.py): Evaluates EasyOCR across 1,651 ground-truth samples, computing CER and confusion matrices.
- [`scratch/integrated_ocr_test.py`](file:///Users/sushant/Documents/SIH2026/scratch/integrated_ocr_test.py): Executes detector + EasyOCR on real test images and sample video.
- [`scratch/run_integrity_check.py`](file:///Users/sushant/Documents/SIH2026/scratch/run_integrity_check.py): Verifies SHA-256 checksums and model isolation.