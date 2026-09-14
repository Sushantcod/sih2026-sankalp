# ANPR OCR V2 Benchmark Report

**Benchmark Timestamp**: 2026-09-14T00:12:00Z  
**OCR Engine**: EasyOCR v1.7.2 (PyTorch v2.14.0, CPU Mode)  
**Evaluated Method**: Selected V2 Preprocessing Pipeline (Variant 1 Original Crop)  
**Ground-Truth Dataset**: `anpr/anpr/ocr/` (1,651 real ground-truth samples)  

---

## 1. Full Benchmark Summary (1,651 Real Samples)

Following the 200-sample subset preprocessing experiment, the winning pipeline (Variant 1: Original Crop) was evaluated across all **1,651 real ground-truth Indian license plate samples**.

```
Total Ground-Truth Samples Evaluated : 1,651
Exact Plate-Match Accuracy           : 7.51% (124 / 1,651)
Character Error Rate (CER)            : 79.86% (12,740 edit distance errors)
Character-Level Accuracy             : 20.14% (100.0% - CER)
Total Ground-Truth Characters        : 15,952
Total Edit Distance                  : 12,740
Total Benchmarking Execution Time    : 1,368.04 seconds (828.61 ms / sample)
```

---

## 2. Character Error & Confusion Analysis

The top 10 character substitution and insertion error pairs (Ground Truth $\rightarrow$ Prediction) across the 1,651 ground-truth samples:

| Rank | Error Pair (GT $\rightarrow$ Pred) | Occurrence Count | Root Cause Analysis |
| :--- | :--- | :--- | :--- |
| **1** | `0` $\rightarrow$ `O` | **467** | Glyph similarity between digit `0` and letter `O`. |
| **2** | `<INS>` $\rightarrow$ `A` | **254** | Background frame noise interpreted as letter `A`. |
| **3** | `<INS>` $\rightarrow$ `O` | **240** | Plate border rivets interpreted as letter `O`. |
| **4** | `<INS>` $\rightarrow$ `E` | **227** | Border artifact insertion. |
| **5** | `<INS>` $\rightarrow$ `I` | **219** | Vertical plate separator border line insertion. |
| **6** | `1` $\rightarrow$ `I` | **128** | Glyph similarity between digit `1` and letter `I`. |
| **7** | `2` $\rightarrow$ `Z` | **108** | Glyph similarity between digit `2` and letter `Z`. |
| **8** | `M` $\rightarrow$ `H` | **91** | Font stroke structure confusion on Indian fonts. |
| **9** | `0` $\rightarrow$ `<DEL>` | **72** | Low-contrast zero character deletion. |
| **10** | `A` $\rightarrow$ `4` | **70** | Diagonal stroke confusion between letter `A` and `4`. |

---

## 3. Performance Breakdown by Registration Prefix

| State Code | Sample Count | Exact Match Acc (%) | Character Error Rate (%) |
| :--- | :--- | :--- | :--- |
| **MH** (Maharashtra) | 769 | **5.59%** | 94.21% |
| **TN** (Tamil Nadu) | 79 | **7.59%** | 106.01% |
| **KL** (Kerala) | 70 | **14.29%** | 75.19% |
| **DL** (Delhi) | 66 | **10.61%** | 76.96% |
| **HR** (Haryana) | 61 | **19.67%** | 75.84% |
| **GJ** (Gujarat) | 44 | **4.55%** | 71.59% |
| **KA** (Karnataka) | 41 | **9.76%** | 102.05% |
| **AP** (Andhra Pradesh) | 39 | **20.51%** | 41.67% |
| **PB** (Punjab) | 36 | **2.78%** | 49.29% |
| **UP** (Uttar Pradesh) | 35 | **14.29%** | 54.23% |
