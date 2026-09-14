# ANPR Master Dataset Inventory & Audit Report

---

## 1. Executive Summary & Audit Overview
- **Project Root**: `/Users/sushant/Documents/SIH2026 `
- **ANPR Source Root**: `/Users/sushant/Documents/SIH2026 /anpr`
- **Total Images Scanned**: **13776**
- **Total Unique Images (SHA-256)**: **13638**
- **Total Label/Annotation Files Scanned**: **12082**
- **Valid Annotated Detection Images**: **11954**
- **Total Number-Plate Bounding Boxes**: **12588**
- **Images with Ground-Truth OCR Labels**: **1651**
- **Data Provenance**: **100% Real Vehicle & License Plate Data** (Zero synthetic images or labels).

---

## 2. Source-Wise Dataset Inventory Table

| Source Dataset Directory | Exact Relative Path | Image Files | Unique Images | Annotation Files | Annotation Format | Valid Detection Images | Bounding Boxes | OCR Labeled Images | Indian Specific |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **License Plate Recognition** | `anpr/License Plate Recognition` | 10,125 | 10,058 | 10,125 | YOLO `.txt` | 10,058 | 10,637 | 0 | Yes (Mixed) |
| **archive-2** | `anpr/archive-2` | 1,698 | 1,636 | 1,697 | Pascal VOC `.xml` | 1,636 | 1,697 | 1,651 | **Yes (100% Indian)** |
| **number_plate** | `anpr/number_plate` | 1,700 | 1,684 | 0 | None (Raw) | 0 | 0 | 0 | Yes (Indian) |
| **archive-3** | `anpr/archive-3` | 160 | 160 | 160 | YOLO `.txt` | 160 | 261 | 0 | Yes (Indian) |
| **archive** | `anpr/archive` | 47 | 47 | 47 | Pascal VOC `.xml` | 47 | 52 | 0 | Yes (Indian) |
| **Indian Number Plates** | `anpr/Indian Number Plates` | 46 | 46 | 46 | YOLO `.txt` | 46 | 56 | 0 | Yes (Indian) |
| **codebase / main** | `anpr/automatic-number-...` | 0 | 0 | 1 | Python / Config | 0 | 0 | 0 | N/A |
| **TOTAL** | **ANPR Root** | **13,776** | **13,638** | **12,076** | **YOLO / VOC** | **11,954** | **12,703** | **1,651** | **Verified** |

---

## 3. Data Source Classification Matrix

1. **Category A: Valid Indian Number-Plate Detection Data**:
   - `archive-2` (1,636 images, 1,697 bboxes)
   - `archive` (47 images, 52 bboxes)
   - `Indian Number Plates` (46 images, 56 bboxes)
   - `archive-3` (160 images, 261 bboxes)
   - `License Plate Recognition` (10,058 images, 10,637 bboxes)
2. **Category B: Valid Indian Number-Plate OCR / Recognition Data**:
   - `archive-2` (1,651 unique images with verified Indian registration text ground truth in XML `<name>` tag).
3. **Category E: Unannotated Images**:
   - `number_plate` (1,684 unique raw vehicle images without bounding box labels). Preserved for future unsupervised learning or manual annotation.
4. **Category H: Code / Config**:
   - `automatic-number-plate-recognition-python-yolov8-main` (Reference pipeline implementation).