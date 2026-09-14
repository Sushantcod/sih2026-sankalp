# ANPR Annotation Format Standardization & Conversion Log

---

## 1. Target Format Specification
- **Format**: YOLO Standardized Detection Format (`class_id center_x center_y width height`)
- **Class Mapping**: `0: number_plate`
- **Coordinate System**: Normalized bounding box coordinates $0.0 \le x, y, w, h \le 1.0$ floating point (6 decimal precision).

---

## 2. Conversion Audit Matrix

| Source Dataset | Input Format | Conversion Logic Applied | Converted Images | Converted Boxes | Excluded Annotations |
|:---|:---:|:---|:---:|:---:|:---:|
| `License Plate Recognition` | YOLO `.txt` | Retained normalized coords, mapped class `0` -> `0` | 10,058 | 10,637 | 0 |
| `archive-2` | Pascal VOC `.xml` | Converted $[xmin, ymin, xmax, ymax]$ -> $[cx, cy, w, h]$ normalized | 1,636 | 1,697 | 0 |
| `archive-3` | YOLO `.txt` | Retained normalized coords, mapped class `0` -> `0` | 160 | 261 | 0 |
| `archive` | Pascal VOC `.xml` | Converted $[xmin, ymin, xmax, ymax]$ -> $[cx, cy, w, h]$ normalized | 47 | 52 | 0 |
| `Indian Number Plates` | YOLO `.txt` | Retained normalized coords, mapped class `0` -> `0` | 46 | 56 | 0 |
| **TOTAL** | **Mixed** | **Unified YOLO Detection Format** | **11,954** | **12,703** | **0** |