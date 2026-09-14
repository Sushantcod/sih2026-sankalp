# ANPR OCR V2 Preprocessing Experiments Report

**Experiment Timestamp**: 2026-09-14T00:07:30Z  
**Subset Size**: 200 Representative Ground-Truth Indian License Plate Samples  
**OCR Engine**: EasyOCR v1.7.2 (PyTorch v2.14.0, CPU Mode)  

---

## 1. Experimental Objective & Preprocessing Variants

To evaluate whether low-level image preprocessing can improve off-the-shelf EasyOCR recognition accuracy on Indian license plates, four distinct preprocessing variations were evaluated across a deterministic 200-sample representative subset.

| Variant ID | Preprocessing Method Name | Technical Pipeline Description |
| :--- | :--- | :--- |
| **Variant 1** | **Original Crop (Baseline V1)** | Raw cropped plate image without transformation. |
| **Variant 2** | **Grayscale + 2x Resize** | OpenCV BGR-to-Grayscale conversion + 2x Cubic Interpolation Upsampling. |
| **Variant 3** | **CLAHE + 2x Resize** | Contrast Limited Adaptive Histogram Equalization (`clipLimit=2.0`, `tileGridSize=(8,8)`) + 2x Resize. |
| **Variant 4** | **Adaptive Threshold + 2x Resize** | Gaussian Adaptive Binarization (`blockSize=11`, `C=2`) + 2x Resize. |

---

## 2. Metric Priority & Decision Protocol

Per project instructions, candidate methods were selected using the following strict priority order:
1. **Exact Plate-Match Accuracy** — `PRIMARY`
2. **Character Error Rate (CER)** — `SECONDARY`
3. **Character-Level Accuracy** — `SECONDARY`
4. **Processing Latency** — `TIE-BREAKER`

---

## 3. Empirical Subset Benchmark Results (200 Samples)

| Preprocessing Variant Name | Exact Plate-Match Acc (PRIMARY) | Character Error Rate (CER) | Character Accuracy | Processing Latency | Total Processing Time |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Variant 1: Original Crop (Baseline V1)** | **13.00%** (26/200) | **44.36%** | **55.64%** | **102.0 ms/sample** | **20.40s** |
| **Variant 2: Grayscale + 2x Resize** | **8.50%** (17/200) | **42.51%** | **57.49%** | **387.3 ms/sample** | **77.46s** |
| **Variant 3: CLAHE + 2x Resize** | **11.50%** (23/200) | **44.84%** | **55.16%** | **383.5 ms/sample** | **76.70s** |
| **Variant 4: Adaptive Threshold + 2x Resize** | **0.00%** (0/200) | **59.45%** | **40.55%** | **374.3 ms/sample** | **74.86s** |

---

## 4. Key Preprocessing Findings

1. **Binarization Destroys Deep OCR (Variant 4 - 0.00% Acc)**:
   - Applying adaptive thresholding converts soft anti-aliased font edges into harsh binary noise. EasyOCR's underlying CRAFT text detector and ResNet recognition backbone fail completely on binarized crops.
2. **Contrast Enhancement Degrades Match Rate (Variant 3 - 11.50% Acc)**:
   - CLAHE accentuates background plate rivets, border frames, and `IND` holographic logos as false character strokes, lowering exact match accuracy by -1.50%.
3. **Upsampling Increases Latency Overhead (3.8x Slower)**:
   - 2x image resizing quadruples pixel count, increasing inference latency from 102.0ms up to 387.3ms per crop without improving exact plate matches.
4. **Winning Method**:
   - **Variant 1: Original Crop (Baseline V1)** achieved the highest exact plate-match accuracy (**13.00%**) and lowest latency (**102.0 ms/sample**).
