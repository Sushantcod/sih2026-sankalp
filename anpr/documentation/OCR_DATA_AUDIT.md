# ANPR OCR Data Audit Report

**Audit Timestamp**: 2026-09-13T23:37:40Z  
**Dataset Directory**: `anpr/combined_dataset/ocr/`  
**Auditor**: Antigravity Automated Verification System  

---

## 1. Executive Summary

A comprehensive data integrity audit was conducted across all image and annotation files in the `anpr/combined_dataset/ocr/` directory. All 1,651 raw image files were matched against corresponding label files and evaluated for readability, syntax, character composition, and usability as ground-truth for OCR benchmarking.

- **Total Unique Sample Keys**: `1,651`
- **Usable Ground-Truth OCR Samples**: `1,651` (`100.00%`)
- **Excluded Samples**: `0` (`0.00%`)
- **Total Ground-Truth Characters**: `15,952`
- **Average License Plate Length**: `9.66` characters (Range: `4` to `13` characters)

---

## 2. File Inventory & Integrity

| Category | File Path / Pattern | Count | Status |
| :--- | :--- | :--- | :--- |
| **Image Files** | `anpr/combined_dataset/ocr/images/*` | `1,651` | Valid (All readable by OpenCV) |
| **Label Files** | `anpr/combined_dataset/ocr/labels/*` | `1,651` | Valid (UTF-8 parseable) |
| **Missing Images** | N/A | `0` | Clean |
| **Missing Labels** | N/A | `0` | Clean |
| **Corrupted Files** | N/A | `0` | Clean |

---

## 3. Label Format & Parsing Logic

- **Format Structure**: Single-line plain text strings containing uppercase Indian registration numbers (e.g., `HR26BU0380`, `KL01CC50`, `DL7CN5617`, `MH12DE1433`).
- **Cleaning Transformation**: Stripped whitespace, non-alphanumeric separators, and normalized to uppercase.
- **Usability Verdict**: All 1,651 labels contain unambiguous ground-truth plate identifiers suitable for exact string matching and Edit-Distance Character Error Rate (CER) calculations.

---

## 4. Character Distribution & Frequency

Total analyzed characters: **15,952** across 36 alphanumeric classes (`0-9`, `A-Z`).

### Top 20 Most Frequent Characters
1. `0` — 1,818 (`11.40%`)
2. `1` — 1,222 (`7.66%`)
3. `2` — 1,192 (`7.47%`)
4. `H` — 967 (`6.06%`)
5. `4` — 912 (`5.72%`)
6. `M` — 912 (`5.72%`)
7. `3` — 833 (`5.22%`)
8. `6` — 825 (`5.17%`)
9. `5` — 787 (`4.93%`)
10. `7` — 736 (`4.61%`)
11. `9` — 728 (`4.56%`)
12. `8` — 720 (`4.51%`)
13. `A` — 495 (`3.10%`)
14. `B` — 389 (`2.44%`)
15. `C` — 368 (`2.31%`)
16. `D` — 320 (`2.01%`)
17. `T` — 285 (`1.79%`)
18. `P` — 229 (`1.44%`)
19. `S` — 211 (`1.32%`)
20. `J` — 191 (`1.20%`)

---

## 5. Sample Ground-Truth Entries

```text
anpr_ocr_00000_3ea28df2.txt -> "HR26BU0380"
anpr_ocr_00001_cff75bf9.txt -> "KL01CC50"
anpr_ocr_00002_7b96476c.txt -> "KL01CA2555"
anpr_ocr_00003_347cec96.txt -> "HR26BC5514"
anpr_ocr_00004_ea457074.txt -> "HR26CU6799"
anpr_ocr_00005_36acee60.txt -> "DL7CN5617"
```
