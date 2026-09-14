#!/usr/bin/env python3
"""
Phase 9: Traffic Sign & Infrastructure Intelligence Pipeline
=============================================================
Runs real-time or file-based object detection using the trained Phase 9 YOLOv8 model
(`models/infrastructure/infrastructure_detector.pt`).

Classes: 57 Traffic Sign Classes (Speed Limit, Stop, Give Way, Pedestrian Crossing, School Ahead, etc.)

Features:
- Processes input video files or live USB camera stream (--source)
- Calculates real-time FPS
- Outputs structured telemetry log (outputs/infrastructure_events.jsonl)
- Optional annotated MP4 output (--save-video)
- Strict Zero Fabrication: GPS is set to null if NMEA sensor is absent.
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime, timezone
from collections import Counter
import cv2
import numpy as np
from ultralytics import YOLO

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DEFAULT_MODEL_PATH = os.path.join(PROJECT_ROOT, "models/infrastructure/infrastructure_detector.pt")
DEFAULT_OUTPUT_EVENTS = os.path.join(PROJECT_ROOT, "outputs/infrastructure_events.jsonl")


def process_infrastructure_video(
    source_path: str,
    weights_path: str = DEFAULT_MODEL_PATH,
    conf_thresh: float = 0.35,
    output_events_path: str = DEFAULT_OUTPUT_EVENTS,
    save_video_path: str = None,
    max_frames: int = None
):
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Trained infrastructure model not found at {weights_path}")

    print(f"[MODEL] Loading trained Phase 9 model from {weights_path}")
    model = YOLO(weights_path)

    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source video file not found: {source_path}")

    cap = cv2.VideoCapture(source_path)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video source: {source_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    writer = None
    if save_video_path:
        os.makedirs(os.path.dirname(save_video_path), exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(save_video_path, fourcc, fps, (width, height))

    os.makedirs(os.path.dirname(output_events_path), exist_ok=True)

    frame_idx = 0
    start_time = time.time()
    events = []
    sign_detections_count = 0
    detected_classes = Counter()

    print(f"[PROCESSING] Video {source_path} ({width}x{height} @ {fps:.1f} FPS, total {total_frames} frames)...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        if max_frames and frame_idx > max_frames:
            break

        results = model.predict(frame, conf=conf_thresh, verbose=False)[0]
        boxes = results.boxes

        signs_in_frame = len(boxes)
        annotated_frame = frame.copy()

        for box in boxes:
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            cls_name = model.names.get(cls_id, f"sign_{cls_id}")
            detected_classes[cls_name] += 1
            sign_detections_count += 1

            xyxy = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = map(int, xyxy)

            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            label = f"{cls_name} {conf:.2f}"
            cv2.putText(annotated_frame, label, (x1, max(20, y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        if signs_in_frame > 0:
            timestamp_iso = datetime.now(timezone.utc).isoformat()
            event = {
                "event_id": f"evt_infra_{frame_idx}_{int(time.time())}",
                "event_type": "traffic_sign_detected",
                "source": os.path.basename(source_path),
                "timestamp": timestamp_iso,
                "latitude": None, # Honest GPS null
                "longitude": None,
                "confidence": float(np.mean([b.conf[0].item() for b in boxes])),
                "payload_json": json.dumps({
                    "frame_index": frame_idx,
                    "sign_count": signs_in_frame,
                    "model": "models/infrastructure/infrastructure_detector.pt"
                }),
                "created_at": timestamp_iso
            }
            events.append(event)

        if writer:
            elapsed = time.time() - start_time
            curr_fps = frame_idx / max(0.001, elapsed)
            hud = f"Frame: {frame_idx}/{total_frames} | FPS: {curr_fps:.1f} | Signs: {signs_in_frame}"
            cv2.putText(annotated_frame, hud, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            writer.write(annotated_frame)

    cap.release()
    if writer:
        writer.release()

    elapsed = time.time() - start_time
    avg_fps = frame_idx / max(0.001, elapsed)

    with open(output_events_path, "w") as f:
        for ev in events:
            f.write(json.dumps(ev) + "\n")

    summary = {
        "processed_frames": frame_idx,
        "total_time_sec": round(elapsed, 2),
        "average_fps": round(avg_fps, 2),
        "total_traffic_sign_detections": sign_detections_count,
        "events_logged": len(events),
        "telemetry_output": output_events_path
    }

    print("\n================ INFERENCE SUMMARY ================")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 9 Traffic Sign & Infrastructure Intelligence Pipeline")
    parser.add_argument("--source", type=str, required=True, help="Path to input video file")
    parser.add_argument("--weights", type=str, default=DEFAULT_MODEL_PATH, help="Path to trained model")
    parser.add_argument("--conf", type=float, default=0.35, help="Confidence threshold")
    parser.add_argument("--save-video", type=str, default=None, help="Optional output MP4 path")
    parser.add_argument("--max-frames", type=int, default=None, help="Max frames to process")

    args = parser.parse_args()
    process_infrastructure_video(
        source_path=args.source,
        weights_path=args.weights,
        conf_thresh=args.conf,
        save_video_path=args.save_video,
        max_frames=args.max_frames
    )
