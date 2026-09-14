#!/usr/bin/env python3
"""
Phase 3: Automatic Number Plate Recognition (ANPR) & EasyOCR Subsystem
========================================================================
Architectural reference: src/detect_potholes.py & src/detect_vehicles.py

Features:
- YOLOv8n Number Plate Detector (weights: anpr/runs/anpr_detection_v1/weights/best.pt).
- EasyOCR Reader integration for optical character recognition on bounding box crops.
- Selectable input: Saved Video File OR Live USB Camera (e.g., --source 0).
- Recommended default operating confidence threshold: 0.25.
- Optional annotated MP4 output (--save-video).
- Optional live preview window (--show-preview) with HUD overlay.
- Structured telemetry event generation saved to JSON/JSONL logs.
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime, timezone
import cv2
import numpy as np
from ultralytics import YOLO
import easyocr


def open_capture_source(source: str):
    """Open capture source from file path or integer camera index."""
    is_live_camera = False
    source_val = source

    if source.isdigit():
        source_val = int(source)
        is_live_camera = True
        print(f"[CAMERA] Opening Live Camera (Index: {source_val})...")
    else:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source video file not found: {source}")
        print(f"[VIDEO] Opening video file: {source}")

    cap = cv2.VideoCapture(source_val)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open capture source: {source}")

    return cap, is_live_camera, source_val


def process_anpr(
    source_path: str,
    weights_path: str,
    conf_thresh: float = 0.25,
    save_video_path: str = None,
    output_events_path: str = None,
    show_preview: bool = False
):
    print("=== ANPR (AUTOMATIC NUMBER PLATE RECOGNITION) INFERENCE ENGINE ===", flush=True)

    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"ANPR detector model weights not found at: {weights_path}")

    # Load YOLO detector
    print(f"[MODEL] Loading YOLOv8n ANPR Detector from {weights_path}...", flush=True)
    model = YOLO(weights_path)

    # Initialize EasyOCR
    print("[OCR] Initializing EasyOCR Reader (CPU mode)...", flush=True)
    ocr_reader = easyocr.Reader(['en'], gpu=False, verbose=False)

    cap, is_live, source_val = open_capture_source(source_path)

    vid_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vid_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vid_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) if not is_live else 0

    out_video = None
    if save_video_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_video_path)), exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_video = cv2.VideoWriter(save_video_path, fourcc, vid_fps, (vid_w, vid_h))
        print(f"[OUTPUT] Saving annotated video to: {save_video_path}")

    total_detections = 0
    total_ocr_reads = 0
    recognized_plates = {}
    events_log = []

    start_time = time.time()
    frame_idx = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                if is_live:
                    time.sleep(0.01)
                    continue
                else:
                    break

            frame_idx += 1
            t_frame_start = time.time()

            # YOLO Bounding Box Detection
            results = model.predict(frame, conf=conf_thresh, verbose=False)[0]

            frame_events = []

            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                det_conf = float(box.conf[0])
                total_detections += 1

                # Crop plate region with 5% padding
                h, w, _ = frame.shape
                pad_x = int((x2 - x1) * 0.05)
                pad_y = int((y2 - y1) * 0.05)
                crop_x1 = max(0, x1 - pad_x)
                crop_y1 = max(0, y1 - pad_y)
                crop_x2 = min(w, x2 + pad_x)
                crop_y2 = min(h, y2 + pad_y)

                plate_crop = frame[crop_y1:crop_y2, crop_x1:crop_x2]

                # EasyOCR inference
                ocr_res = ocr_reader.readtext(plate_crop, detail=1)

                if ocr_res:
                    raw_text = " ".join([r[1] for r in ocr_res])
                    ocr_conf = float(np.mean([float(r[2]) for r in ocr_res]))
                else:
                    raw_text = ""
                    ocr_conf = 0.0

                clean_plate = "".join(c for c in raw_text if c.isalnum()).upper()

                if len(clean_plate) >= 4 and ocr_conf > 0.20:
                    total_ocr_reads += 1
                    recognized_plates[clean_plate] = recognized_plates.get(clean_plate, 0) + 1
                    overlay_label = f"{clean_plate} ({det_conf:.2f}|{ocr_conf:.2f})"
                    box_color = (0, 255, 0)
                else:
                    overlay_label = f"PLATE ({det_conf:.2f})"
                    box_color = (0, 165, 255)

                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                cv2.putText(frame, overlay_label, (x1, max(25, y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.65, box_color, 2)

                frame_events.append({
                    "frame_idx": frame_idx,
                    "bbox": [x1, y1, x2, y2],
                    "detector_confidence": det_conf,
                    "recognized_text": clean_plate,
                    "ocr_confidence": ocr_conf
                })

            if out_video:
                out_video.write(frame)

            if show_preview:
                cv2.imshow("ANPR Pipeline (Press Q to quit)", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("[USER] Quitting preview loop.")
                    break

            if frame_events:
                events_log.extend(frame_events)

            if frame_idx % 100 == 0:
                elapsed = time.time() - start_time
                fps = frame_idx / elapsed
                print(f"[PROGRESS] Frame {frame_idx} | Detections: {total_detections} | OCR Reads: {total_ocr_reads} | FPS: {fps:.2f}", flush=True)

    finally:
        cap.release()
        if out_video:
            out_video.release()
        if show_preview:
            cv2.destroyAllWindows()

    total_time = time.time() - start_time
    effective_fps = frame_idx / total_time if total_time > 0 else 0

    print("\n=== ANPR PROCESSING SUMMARY ===")
    print(f"Total Frames Processed: {frame_idx}")
    print(f"Total Bounding Box Detections: {total_detections}")
    print(f"Successful OCR Reads: {total_ocr_reads}")
    print(f"Distinct Plate Strings: {len(recognized_plates)}")
    print(f"Total Processing Time: {total_time:.2f}s ({effective_fps:.2f} FPS)")

    if output_events_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_events_path)), exist_ok=True)
        with open(output_events_path, 'w') as f:
            json.dump({
                "source": source_path,
                "weights": weights_path,
                "total_frames": frame_idx,
                "total_detections": total_detections,
                "total_ocr_reads": total_ocr_reads,
                "distinct_plates_count": len(recognized_plates),
                "top_recognized_plates": sorted(recognized_plates.items(), key=lambda x: x[1], reverse=True)[:20],
                "events": events_log
            }, f, indent=2)
        print(f"[EVENTS] Saved telemetries to: {output_events_path}")

    return {
        "frames": frame_idx,
        "detections": total_detections,
        "ocr_reads": total_ocr_reads,
        "distinct_plates": len(recognized_plates),
        "fps": effective_fps
    }


def main():
    parser = argparse.ArgumentParser(description="Phase 3: ANPR Detector + EasyOCR Inference Engine")
    parser.add_argument("--source", type=str, default="data/sample_videos/anpr.mp4", help="Video path or camera index (e.g. 0)")
    anpr_weights_default = "models/anpr/best.pt" if os.path.exists("models/anpr/best.pt") else "anpr/runs/anpr_detection_v1/weights/best.pt"
    parser.add_argument("--weights", type=str, default=anpr_weights_default, help="Path to YOLOv8n ANPR weights")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--save-video", type=str, default=None, help="Path to save output annotated video")
    parser.add_argument("--output-events", type=str, default=None, help="Path to save JSON telemetry events log")
    parser.add_argument("--show-preview", action="store_true", help="Display live OpenCV window preview")

    args = parser.parse_args()

    process_anpr(
        source_path=args.source,
        weights_path=args.weights,
        conf_thresh=args.conf,
        save_video_path=args.save_video,
        output_events_path=args.output_events,
        show_preview=args.show_preview
    )


if __name__ == "__main__":
    main()
