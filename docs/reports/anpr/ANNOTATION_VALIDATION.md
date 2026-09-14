# ANPR Annotation Validation & Quality Report

---

## 1. Validation Criteria
- **YOLO Text Annotations**: Evaluated $0.0 \le cx, cy, w, h \le 1.0$, $w > 0$, $h > 0$, matching image file exists.
- **Pascal VOC XML Annotations**: Verified valid XML schema parsing, image dimensions $w, h > 0$, $xmin < xmax$, $ymin < ymax$ within image boundaries.
- **OCR Text Ground Truth**: Verified presence of non-generic text strings (e.g. `KA05HS4495`, `MH20BN3525`) in XML `<name>` tags.

---

## 2. Validation Results Table

| Annotation Source | Annotation Format | Total Annotation Files | Valid Annotation Files | Valid Bounding Boxes | Invalid / Corrupt BBoxes | Validation Rate |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| `License Plate Recognition` | YOLO `.txt` | 10,125 | 10,125 | 10,637 | 0 | 100.0% |
| `archive-2` | Pascal VOC `.xml` | 1,697 | 1,697 | 1,697 | 0 | 100.0% |
| `archive-3` | YOLO `.txt` | 160 | 160 | 261 | 0 | 100.0% |
| `archive` | Pascal VOC `.xml` | 47 | 47 | 52 | 0 | 100.0% |
| `Indian Number Plates` | YOLO `.txt` | 46 | 46 | 56 | 0 | 100.0% |
| **TOTAL** | **YOLO / VOC** | **12,075** | **12,075** | **12,703** | **0** | **100.0%** |