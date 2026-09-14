# ANPR Exact & Near-Duplicate Analysis Report

---

## 1. Cryptographic SHA-256 Exact Duplicate Summary
- **Total Images Scanned**: 13776
- **Unique SHA-256 Images**: 13638
- **Exact Duplicate File Instances Removed**: **138**

---

## 2. Duplicate Breakdown Across Sources

- **License Plate Recognition**: 67 intra-dataset exact duplicates removed.
- **archive-2**: 47 intra-dataset exact duplicates removed.
- **number_plate**: 9 intra-dataset exact duplicates removed.
- **Cross-Dataset Duplicates**: 15 exact MD5/SHA-256 duplicates detected between `archive-2` and `number_plate`.

---

## 3. Perceptual Hashing (dHash) Near-Duplicate Findings
- **dHash Function**: 8x8 Difference Hash (64-bit binary vector)
- **Hamming Distance Threshold**: $d \le 2$
- **Identified Near-Duplicates**: **735** images (predominantly consecutive video sequence frames in `archive-3` vid-1, vid-2, vid-3 and `archive-2/video_images`).
- **Data Leakage Mitigation**: All sequence frames from the same video source were grouped into identical sequence blocks and assigned strictly to the SAME train/valid/test split during combination.