# ANPR OCR Reproducibility & Environment Setup Guide

**Document Timestamp**: 2026-09-13T23:38:00Z  

---

## 1. System & Environment Specifications

- **OS**: macOS Sonoma 14.x / Apple Silicon (M5 Architecture)
- **Python Runtime**: Python v3.14.0
- **Virtualenv Path**: `/Users/sushant/Desktop/sih/SIH2026 v1/.venv`
- **PyTorch Version**: `2.14.0`
- **EasyOCR Version**: `1.7.2`
- **Ultralytics Version**: `8.4.149`
- **OpenCV Version**: `5.0.0`

---

## 2. Reproduction Commands

### Step 1: Run OCR Data Audit
```bash
/Users/sushant/Desktop/sih/"SIH2026 v1"/.venv/bin/python scratch/ocr_data_audit.py
```
*Generates dataset audit summary at `scratch/ocr_audit_summary.json`.*

### Step 2: Run EasyOCR Benchmark
```bash
/Users/sushant/Desktop/sih/"SIH2026 v1"/.venv/bin/python scratch/benchmark_ocr.py
```
*Evaluates all 1,651 ground-truth OCR samples and outputs `scratch/ocr_benchmark_results.json`.*

### Step 3: Run Integrated Detector + OCR Pipeline
```bash
/Users/sushant/Desktop/sih/"SIH2026 v1"/.venv/bin/python scratch/integrated_ocr_test.py
```
*Generates sample image outputs in `anpr/outputs/anpr_ocr_v1/real_images/`, outputs `anpr/outputs/anpr_ocr_v1/anpr_ocr_video_annotated.mp4`, and writes `scratch/ocr_video_metrics.json`.*

---

## 3. SHA-256 Checksums for Scripts & Models

| Artifact / File Path | SHA-256 Checksum |
| :--- | :--- |
| `anpr/runs/anpr_detection_v1/weights/best.pt` | `d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a` |
| `scratch/ocr_data_audit.py` | *(Computed dynamically in integrity check)* |
| `scratch/benchmark_ocr.py` | *(Computed dynamically in integrity check)* |
| `scratch/integrated_ocr_test.py` | *(Computed dynamically in integrity check)* |
| `anpr/outputs/anpr_ocr_v1/anpr_ocr_video_annotated.mp4` | *(Generated output artifact)* |
