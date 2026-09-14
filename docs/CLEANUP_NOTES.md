# Workspace Cleanup Classification & Scratch Audit Notes

**Date**: 2026-09-14  
**Audit Purpose**: Classification of workspace utility scripts, scratch files, and research artifacts.  

---

## 1. Scratch Directory Classification (`scratch/`)

In compliance with the project cleanup instructions, all files in `scratch/` were audited to preserve research provenance and benchmark reproducibility. Zero useful research files were deleted.

| File Name | Category | Functionality & Provenance | Preservation Action |
| :--- | :--- | :--- | :--- |
| `scratch/benchmark_ocr.py` | Benchmark Utility | EasyOCR V1 Baseline Benchmark Script | **KEPT** (Required for OCR V1 baseline reproduction) |
| `scratch/benchmark_ocr_v2.py` | Benchmark Utility | Preprocessing Experiment & OCR V2 Benchmark Script | **KEPT** (Required for OCR V2 evaluation reproduction) |
| `scratch/setup_anpr_dataset_folder.py` | Dataset Utility | Copies and structures 1,651 real ANPR plate crops | **KEPT** (Required for dataset setup reproducibility) |
| `scratch/reorganize_dataset.py` | Provenance Script | Rearranges multi-class road damage dataset folders | **KEPT** (Historical dataset provenance) |
| `scratch/split_dataset.py` | Provenance Script | Train/val/test split generator for YOLO annotations | **KEPT** (Historical dataset provenance) |

---

## 2. Dataset & Subsystem Preservation

1. **`potholes_info/`**: Kept intact as-is. Contains road-damage class mappings, dataset proofs, label ground-truths, and images.
2. **`anpr/`**: Kept intact as-is. Contains ANPR number-plate crops, ground-truth annotations, YOLO model runs, preprocessing experiments, and evaluation reports.
3. **`data/events.db`**: Preserved strictly intact. Contains 7,964 real telemetry records. Zero events altered or deleted.
