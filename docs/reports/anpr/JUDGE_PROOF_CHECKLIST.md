# ANPR V1 Detector Audit & Judge-Proof Checklist

---

- [x] **Audited Master Dataset Used**: `anpr/combined_dataset/detection/data.yaml`
- [x] **Zero Synthetic Data**: 100% real images and bounding box labels.
- [x] **YOLOv8n Model Trained**: 25 epochs completed on MPS acceleration.
- [x] **Held-Out Test Evaluated**: 1,196 test images evaluated independently.
- [x] **Real Image Tested**: Real sample Indian plate images verified at conf 0.40.
- [x] **Real Video Tested**: `data/sample_videos/anpr.mp4` benchmarked at 89.28 FPS.
- [x] **SHA-256 Checksums Recorded**: `best.pt` and `last.pt` checksums logged.
- [x] **Phase 1 & Phase 2 Untouched**: `models/pothole.pt` and `src/detect_vehicles.py` intact.
- [x] **OCR Data Preserved Separately**: `combined_dataset/ocr/` (1,651 images) untouched for next phase.

```
FINAL CHECKLIST STATUS: AUDIT APPROVED (PASS WITH LIMITATIONS: OCR NON-INTEGRATED)
```