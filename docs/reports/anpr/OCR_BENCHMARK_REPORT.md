# EasyOCR Engine Benchmark Report

**Evaluation Timestamp**: 2026-09-13T23:35:20Z  
**OCR Engine**: EasyOCR v1.7.2 (PyTorch v2.14.0, CPU execution target)  
**Ground-Truth Dataset**: `anpr/combined_dataset/ocr/` (1,651 usable samples)  

---

## 1. Metric Overview

The existing off-the-shelf `EasyOCR` model was benchmarked against all **1,651 real ground-truth Indian number plate images** without introducing fine-tuning or custom OCR training.

```
Total Ground-Truth Samples : 1,651
Exact Plate-Match Accuracy : 7.51% (124 / 1,651 correctly matched)
Character Error Rate (CER)  : 79.86% (12,740 total character errors)
Character-Level Accuracy   : 20.14% (100.0% - CER)
Total GT Characters        : 15,952
Total Edit Distance        : 12,740
Total Benchmarking Time    : 1,368.04 seconds (828.61 ms / sample)
```

---

## 2. Evaluation Formulas & Definitions

1. **Exact Plate-Match Accuracy**:
   $$\text{Accuracy}_{\text{exact}} = \frac{N_{\text{exact}}}{N_{\text{total}}} \times 100\%$$
   where $N_{\text{exact}}$ is the count of samples where the predicted alphanumeric string identically matches the ground-truth string (`gt_clean == pred_clean`).

2. **Character Error Rate (CER)**:
   $$\text{CER} = \frac{\sum_{i=1}^{N} \text{Levenshtein}(GT_i, Pred_i)}{\sum_{i=1}^{N} \text{len}(GT_i)} \times 100\%$$
   where Levenshtein edit distance includes character insertions, deletions, and substitutions.

3. **Character-Level Accuracy**:
   $$\text{Accuracy}_{\text{char}} = \max(0, 100.0\% - \text{CER})$$

---

## 3. Character Confusion & Common Errors

Analysis of error alignment dynamic programming revealed systemic failure modes in standard EasyOCR when applied to Indian license plate fonts and layouts:

| Ranking | Error Pair (GT $\rightarrow$ Pred) | Occurrence Count | Error Category |
| :--- | :--- | :--- | :--- |
| **1** | `0` $\rightarrow$ `O` | **467** | Digit/Letter Ambiguity |
| **2** | `<INS>` $\rightarrow$ `A` | **254** | Background Noise Insertion |
| **3** | `<INS>` $\rightarrow$ `O` | **240** | Background Noise Insertion |
| **4** | `<INS>` $\rightarrow$ `E` | **227** | Background Noise Insertion |
| **5** | `<INS>` $\rightarrow$ `I` | **219** | Separator / Border Insertion |
| **6** | `1` $\rightarrow$ `I` | **128** | Digit/Letter Ambiguity |
| **7** | `2` $\rightarrow$ `Z` | **108** | Visual Glyph Similarity |
| **8** | `M` $\rightarrow$ `H` | **91** | Font Stroke Confusion |
| **9** | `0` $\rightarrow$ `<DEL>` | **72** | Character Deletion |
| **10** | `A` $\rightarrow$ `4` | **70** | Glyph Confusion |

---

## 4. Performance by Registration State Code

| State Code | Sample Count | Exact Match Acc (%) | Character Error Rate (%) |
| :--- | :--- | :--- | :--- |
| **State MH** (Maharashtra) | 769 | **5.59%** | 94.21% |
| **State TN** (Tamil Nadu) | 79 | **7.59%** | 106.01% |
| **State KL** (Kerala) | 70 | **14.29%** | 75.19% |
| **State DL** (Delhi) | 66 | **10.61%** | 76.96% |
| **State HR** (Haryana) | 61 | **19.67%** | 75.84% |
| **State GJ** (Gujarat) | 44 | **4.55%** | 71.59% |
| **State KA** (Karnataka) | 41 | **9.76%** | 102.05% |
| **State AP** (Andhra Pradesh) | 39 | **20.51%** | 41.67% |
| **State PB** (Punjab) | 36 | **2.78%** | 49.29% |
| **State UP** (Uttar Pradesh) | 35 | **14.29%** | 54.23% |

---

## 5. Key Empirical Observations

1. **Low Exact Match Accuracy (7.51%)**: Standard EasyOCR without preprocessing or fine-tuning fails on ~92.5% of Indian number plates due to non-standard fonts, stacked two-line plate text, and zero/O confusion.
2. **High Insertion Rate**: EasyOCR text detector frequently picks up surrounding plate frame borders, bolts, and logo text (IND), introducing false character insertions (`<INS>`).
