# ANPR OCR V2 Real Video Stream Benchmark Report

**Benchmark Timestamp**: 2026-09-14T00:11:00Z  
**Video File**: `data/sample_videos/anpr.mp4`  
**Annotated Output Video**: [`anpr/outputs/anpr_ocr_v2/anpr_ocr_v2_video_annotated.mp4`](file:///Users/sushant/Documents/SIH2026/anpr/outputs/anpr_ocr_v2/anpr_ocr_v2_video_annotated.mp4)  

---

## 1. Video Specifications & Benchmark Execution

| Parameter | Value | Note |
| :--- | :--- | :--- |
| **Video Resolution** | **1440 x 960** | High Definition Traffic Stream |
| **Source Video FPS** | **30.00 FPS** | Standard Real-Time Video |
| **Total Frame Count** | **1,800 frames** | Complete 1-minute video |
| **Video Duration** | **60.00 seconds** | 100% evaluated |
| **Detector Threshold** | **0.25** | YOLOv8n `best.pt` |
| **Pipeline Processing Time** | **104.09 seconds** | Complete end-to-end execution |
| **Effective Processing FPS** | **17.29 FPS** | Real-time interactive processing |

---

## 2. Integrated Pipeline Detections & OCR Performance

```
Total Plate Bounding Box Detections : 5,256
Total OCR Inference Attempts        : 5,256
Successful High-Conf OCR Reads      : 1,008  (19.18%)
Failed / Uncertain OCR Cases        : 4,248  (80.82%)
Distinct Recognized Plate Strings   : 613
Average Per-Crop OCR Latency        : 11.97 ms
```

---

## 3. Top Recognized Plate Strings in Video Stream

| Rank | Recognized Plate String | Frame Frequency |
| :--- | :--- | :--- |
| **1** | `GXIS0GJ` | **50 frames** |
| **2** | `KHOSZZK` | **29 frames** |
| **3** | `GXISOGJ` | **22 frames** |
| **4** | `APOSJEO` | **20 frames** |
| **5** | `EXGINBG` | **14 frames** |
| **6** | `KHOGKSU` | **9 frames** |
| **7** | `LNSZZQ` | **9 frames** |
| **8** | `LNSZZC` | **9 frames** |
| **9** | `APOSJEQ` | **8 frames** |
| **10** | `EYGINBG` | **8 frames** |
