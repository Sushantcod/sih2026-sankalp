# ANPR V1 Detector Known Limitations & Failure Modes

---

## 1. Operational & Environmental Limitations
1. **OCR Non-Integration**: This model is strictly a license plate *detector* (bounding boxes). Character recognition (OCR) will be handled separately in the next phase using `combined_dataset/ocr/` (1,651 ground-truth images).
2. **Acute Side Angles**: License plates viewed at extreme side angles (>60 degrees) show reduced bounding box IoU accuracy.
3. **Dirty / Blurred Plates**: Heavily rusted, mud-splattered, or motion-blurred plates on fast-moving vehicles require higher confidence thresholds (0.45+).

---

## 2. Provenance Boundaries
- Zero synthetic data was used in training or evaluation.
- Held-out test split (1,196 images) was kept 100% isolated.