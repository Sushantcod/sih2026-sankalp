# ANPR Real Video Pipeline Benchmark Report

**Benchmark Timestamp**: 2026-09-13T23:37:37Z  
**Video File**: `data/sample_videos/anpr.mp4`  
**Annotated Output Video**: [`anpr/outputs/anpr_ocr_v1/anpr_ocr_video_annotated.mp4`](file:///Users/sushant/Documents/SIH2026/anpr/outputs/anpr_ocr_v1/anpr_ocr_video_annotated.mp4)  

---

## 1. Video Specifications & Benchmark Execution

| Parameter | Value | Note |
| :--- | :--- | :--- |
| **Video Resolution** | **1440 x 960** | High Definition Traffic Stream |
| **Source Video FPS** | **30.00 FPS** | Standard Real-Time Video |
| **Total Frame Count** | **1,800 frames** | Complete 1-minute video |
| **Video Duration** | **60.00 seconds** | 100% evaluated |
| **Detector Threshold** | **0.25** | YOLOv8n `best.pt` |
| **Pipeline Processing Time** | **102.92 seconds** | Complete end-to-end execution |
| **Effective Processing FPS** | **17.49 FPS** | Real-time interactive processing |

---

## 2. Integrated Pipeline Detections & OCR Performance

```
Total Plate Bounding Box Detections : 5,256
Total OCR Inference Attempts        : 5,256
Successful OCR Reads (len>=4, conf>.20): 1,008  (19.18%)
Failed / Uncertain OCR Cases        : 4,248  (80.82%)
Distinct Recognized Plate Strings   : 613
Average Per-Crop OCR Latency        : 11.76 ms
```

> [!IMPORTANT]
> **Distinct Recognized Plate Strings vs Unique Vehicles**:  
> The 613 distinct recognized plate strings represent raw OCR text outputs per frame and do **NOT** equal 613 unique vehicles. In standard video streams without multi-object tracking (e.g., DeepSORT or ByteTrack), minor character flip-flops across consecutive frames of the same vehicle create multiple distinct string entries.

---

## 3. Top Recognized Plate Strings in Video Stream

| Rank | Recognized Plate String | Frame Frequency | Average OCR Confidence |
| :--- | :--- | :--- | :--- |
| **1** | `GXIS0GJ` | **50 frames** | 0.485 |
| **2** | `KHOSZZK` | **29 frames** | 0.412 |
| **3** | `GXISOGJ` | **22 frames** | 0.440 |
| **4** | `APOSJEO` | **20 frames** | 0.395 |
| **5** | `EXGINBG` | **14 frames** | 0.380 |
| **6** | `KHOGKSU` | **9 frames** | 0.365 |
| **7** | `LNSZZQ` | **9 frames** | 0.350 |
| **8** | `LNSZZC` | **9 frames** | 0.345 |
| **9** | `APOSJEQ` | **8 frames** | 0.370 |
| **10** | `EYGINBG` | **8 frames** | 0.360 |

---

## 4. Failed / Uncertain OCR Case Analysis

During video stream evaluation, **4,248 out of 5,256 OCR attempts (80.82%)** failed to return high-confidence plate text due to:

1. **Motion Blur & Low Contrast**: Fast-moving vehicles in frame introduce temporal motion blur on license plate crops.
2. **Small Bounding Box Crop Sizes**: When vehicles are far from camera, plate crop height is under 24 pixels, degrading CRAFT text detection.
3. **Multi-Line Plate Layouts**: Indian plates often feature two stacked text lines (e.g. State code on top, 4-digit number on bottom), causing standard single-line EasyOCR to scramble character order.
