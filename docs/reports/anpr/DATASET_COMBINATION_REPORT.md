# ANPR Master Dataset Combination & Train/Valid/Test Split Report

---

## 1. Combined Structure Path
- **Detection Dataset Path**: `/Users/sushant/Documents/SIH2026 /anpr/combined_dataset/detection`
- **OCR Dataset Path**: `/Users/sushant/Documents/SIH2026 /anpr/combined_dataset/ocr`
- **YAML Configuration**: `combined_dataset/detection/data.yaml`

---

## 2. Split Breakdown & Data Leakage Prevention

To prevent video sequence data leakage, sequence frames (e.g. `archive-3` vid-1, vid-2, vid-3; `archive-2` video_images) were grouped by video source sequence and assigned atomically to a single split.

| Dataset Split | Unique Images | Percentage | Total Bounding Boxes | BBox Proportion | Leakage Check |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Train Split (`detection/train`)** | **9563** | **80.00%** | 10071 | 79.9% | **PASSED (0 Cross-Split Overlap)** |
| **Validation Split (`detection/valid`)** | **1195** | **10.00%** | 1260 | 10.1% | **PASSED (0 Cross-Split Overlap)** |
| **Test Split (`detection/test`)** | **1196** | **10.01%** | 1257 | 10.0% | **PASSED (0 Cross-Split Overlap)** |
| **TOTAL COMBINED** | **11954** | **100.0%** | **12588** | **100.0%** | **VERIFIED CLEAN** |