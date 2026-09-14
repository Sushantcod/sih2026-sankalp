#!/usr/bin/env python3
"""
Step 8 — Real Video Validation Script for Phase 8
===================================================
Runs inference on real video clips from IPID (Indian Pedestrian Intention Dataset)
using the trained model `models/pedestrian/pedestrian_detector.pt`.

Outputs real detection statistics, bounding box counts, confidence, and FPS.
Strict Zero Fabrication: GPS is output as null ("GPS: Unavailable").
"""

import os
import sys
import json
import time
from ultralytics import YOLO

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
MODEL_PATH = os.path.join(PROJECT_ROOT, "models/pedestrian/pedestrian_detector.pt")
VIDEO_DIR = os.path.join(PROJECT_ROOT, "data/sample_videos")

def run_validation():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file {MODEL_PATH} does not exist yet.")
        sys.exit(1)

    print(f"Loading trained Phase 8 model: {MODEL_PATH}")
    model = YOLO(MODEL_PATH)

    sample_video = os.path.join(VIDEO_DIR, "pedestrian_ipid.mp4")
    if not os.path.exists(sample_video):
        sample_video = os.path.join(VIDEO_DIR, "crossign.mp4")
    
    print(f"Processing sample real video clip: {sample_video}")

    import cv2
    cap = cv2.VideoCapture(sample_video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_count = 0
    total_pedestrians = 0
    total_vehicles = 0
    total_crossings = 0
    confidences = []

    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        if frame_count > 100: # Evaluate 100 frames for validation report
            break

        results = model.predict(frame, conf=0.30, verbose=False)[0]
        boxes = results.boxes

        for box in boxes:
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            cls_name = model.names.get(cls_id, f"class_{cls_id}")
            confidences.append(conf)

            if cls_name == "pedestrian":
                total_pedestrians += 1
            elif cls_name == "vehicle":
                total_vehicles += 1
            elif cls_name == "crossing":
                total_crossings += 1

    cap.release()
    elapsed = time.time() - start_time
    avg_fps = frame_count / max(0.001, elapsed)
    mean_conf = float(sum(confidences) / len(confidences)) if confidences else 0.0

    print("\n================ REAL VIDEO VALIDATION RESULTS ================")
    print(f"  Video Source: {os.path.basename(sample_video)}")
    print(f"  Resolution: {width}x{height} @ {fps:.1f} FPS")
    print(f"  Processed Frames: {frame_count}")
    print(f"  Inference Speed: {avg_fps:.2f} FPS")
    print(f"  Pedestrians Detected: {total_pedestrians}")
    print(f"  Vehicles Detected: {total_vehicles}")
    print(f"  Crossings Detected: {total_crossings}")
    print(f"  Mean Bounding Box Confidence: {mean_conf:.4f}")
    print(f"  GPS Telemetry: UNAVAILABLE (GPS: null)")
    print(f"  School-Zone Metadata: UNAVAILABLE")
    print("==============================================================")

if __name__ == "__main__":
    run_validation()
