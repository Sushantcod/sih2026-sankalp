# Phase 1 Model Limitations & Failure Modes Report

---

## 1. Overview
This report documents known performance boundaries, class imbalance effects, and failure modes observed during Phase 1 multi-class road damage model evaluation.

---

## 2. Key Model Limitations

1. **Waterlogging Detection Limitation**:
   - **Metrics**: Precision = 15.95%, Recall = 0.98%, mAP50 = 12.43%.
   - **Root Cause**: Severe dataset class imbalance (~1.2% representation in the overall real dataset).
   - **Status**: **NOT PRODUCTION-READY.** Standing water detection requires additional target training data and multi-spectral sensors.

2. **Pothole Recall Boundary**:
   - **Metrics**: Precision = 57.19%, Recall = 40.17%, mAP50 = 46.10%.
   - **Root Cause**: Low-contrast shallow potholes and dark shadows resemble ordinary asphalt edges at IoU 0.50 thresholds.

3. **False Positive Triggers**:
   - **Shadows & Tar Patch Edges**: Deep roadside tree shadows and fresh black tar patch repair seams occasionally trigger low-confidence pothole detections (conf 0.41-0.44).

4. **Class Capacity Tradeoff**:
   - Transitioning from single-class pothole detection to 6-class surface defect classification distributes network capacity across crack geometries, utility lids, and surface depressions.
