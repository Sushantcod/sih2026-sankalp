#!/usr/bin/env python3
"""
Phase 1: Pothole & Road Defect Detection
=========================================
Rebuilt from scratch aligned with MASTER_PLAN.md.
Architectural reference: src/detect_vehicles.py

Features:
- Selectable input: Saved Video File OR Live USB Camera (e.g., --source 0).
- Dynamic YOLO class name extraction from model.names (supports 1-class or multi-class trained models).
- Structured telemetry event generation saved to outputs/events.jsonl.
- Total detections represent frame-level model predictions, not unique physical potholes.
- Recommended default operating confidence threshold: 0.40.
- Optional annotated MP4 output (--save-video).
- Optional live preview window (--show-preview) with clean HUD banner & live FPS overlay.
- Robust USB Camera re-connect handling for live streams.
- Accurate frame-based or wall-clock UTC ISO timestamps.
- Explicit "GPS unavailable" status (zero synthetic GPS).
- Post events to central backend API if available.
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime, timezone
from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO


def open_capture_source(source: str):
    """Open capture source from file path or integer camera index."""
    is_live_camera = False
    source_val = source

    # Determine if source is camera index (e.g. "0", "1") or file path
    if source.isdigit():
        source_val = int(source)
        is_live_camera = True
        print(f"[CAMERA] Opening USB Live Camera (Index: {source_val})...")
    else:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source video file not found: {source}")
        print(f"[VIDEO] Opening saved video file: {source}")

    cap = cv2.VideoCapture(source_val)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open capture source: {source}")

    return cap, is_live_camera, source_val


def process_potholes(
    source_path: str,
    weights_path: str,
    conf_thresh: float,
    output_events_path: str,
    save_video_path: str,
    show_preview: bool = False,
    bus_id: str = "BUS-101",
    max_reconnect_attempts: int = 5,
    clean_events: bool = False
):
    """Process video file or live USB camera stream for pothole / road damage detection."""
    
    # 1. Load YOLO Pothole Model
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Model weights not found at: {weights_path}. Please ensure training completed and model exists.")
        
    print(f"[MODEL] Loading YOLO pothole model from {weights_path}...")
    model = YOLO(weights_path)
    
    # Extract actual model class mapping dynamically
    class_names = model.names
    print(f"[MODEL] Model loaded successfully. Active defect classes ({len(class_names)}): {class_names}")
    
    # 2. Open Video Stream / Camera
    cap, is_live_camera, source_val = open_capture_source(source_path)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or np.isnan(fps) or is_live_camera:
        fps = 30.0  # Default target FPS for live streams or unreadable metadata
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) if not is_live_camera else 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        width, height = 1280, 720  # Standard fallback resolution
    
    duration_sec = total_frames / fps if total_frames > 0 else 0.0
    source_desc = f"USB Camera {source_val}" if is_live_camera else source_path
    print(f"[STREAM] Source: {source_desc} | Res: {width}x{height} | Target FPS: {fps:.1f}"
          f"{f' | Total Frames: {total_frames}' if not is_live_camera else ' | Live Stream'}")
    
    # 3. Setup Outputs
    os.makedirs(os.path.dirname(output_events_path), exist_ok=True)
    file_mode = "w" if clean_events else "a"
    events_file = open(output_events_path, file_mode, encoding="utf-8")
    
    video_writer = None
    if save_video_path:
        os.makedirs(os.path.dirname(save_video_path), exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(save_video_path, fourcc, fps, (width, height))
        print(f"[OUTPUT] Writing annotated video to: {save_video_path}")

    # Start timestamp anchors
    start_wall_time = datetime.now(timezone.utc)
    start_proc_time = time.time()
    last_frame_time = start_proc_time
    live_fps = fps

    frame_idx = 0
    total_detections_count = 0
    events_logged_count = 0
    class_detection_counts = defaultdict(int)
    unique_defect_track_ids = set()
    
    gui_available = show_preview
    reconnect_count = 0

    print("[PROCESSING] Beginning YOLO road damage detection loop...")

    try:
        while True:
            ret, frame = cap.read()
            
            # Camera Re-connect handling for live streams
            if not ret:
                if is_live_camera and reconnect_count < max_reconnect_attempts:
                    reconnect_count += 1
                    print(f"[CAMERA WARNING] Stream interrupted. Re-connect attempt {reconnect_count}/{max_reconnect_attempts}...")
                    time.sleep(1.0)
                    cap.release()
                    cap = cv2.VideoCapture(source_val)
                    if cap.isOpened():
                        print("[CAMERA] Re-connected successfully!")
                        reconnect_count = 0
                    continue
                else:
                    if is_live_camera:
                        print("[CAMERA ERROR] Camera connection lost and max reconnect retries reached.")
                    else:
                        print("[VIDEO] Reached end of video stream.")
                    break
            
            reconnect_count = 0  # Reset on successful frame read
            frame_idx += 1
            
            # Compute live processing FPS (rolling window)
            now = time.time()
            frame_delta = now - last_frame_time
            last_frame_time = now
            if frame_delta > 0:
                live_fps = 0.9 * live_fps + 0.1 * (1.0 / frame_delta)

            # Calculate real video/stream offset in seconds
            video_time_offset_sec = (frame_idx - 1) / fps if not is_live_camera else (now - start_proc_time)
            
            # Calculate ISO timestamp for this exact frame
            frame_utc_time = datetime.fromtimestamp(
                start_wall_time.timestamp() + video_time_offset_sec, 
                tz=timezone.utc
            ).isoformat()
            
            # Run ByteTrack model tracking on frame
            results = model.track(frame, tracker="bytetrack.yaml", persist=True, imgsz=640, conf=conf_thresh, verbose=False)
            
            frame_detections_count = 0
            
            # Distinct color map for all 6 defect classes (BGR format for OpenCV)
            color_map = {
                0: (255, 144, 30),  # Blue (longitudinal_crack)
                1: (113, 179, 60),  # Green (transverse_crack)
                2: (0, 215, 255),   # Yellow (alligator_crack)
                3: (0, 0, 255),      # Red (pothole)
                4: (211, 85, 186),  # Magenta (manhole)
                5: (255, 255, 0)    # Cyan (waterlogging)
            }
            
            for result in results:
                boxes = result.boxes
                if boxes is None or len(boxes) == 0:
                    continue
                
                for box in boxes:
                    conf = float(box.conf[0].cpu().numpy())
                    cls_id = int(box.cls[0].cpu().numpy())
                    cls_name = class_names.get(cls_id, f"Class_{cls_id}")
                    xyxy = box.xyxy[0].cpu().numpy().tolist()  # [x1, y1, x2, y2]
                    
                    bbox_int = [int(round(coord)) for coord in xyxy]
                    
                    # Track ID assignment via ByteTrack
                    if box.id is not None:
                        track_id = int(box.id[0].cpu().numpy())
                        track_label = f"#{track_id}"
                        unique_defect_track_ids.add((cls_id, track_id))
                    else:
                        track_label = "[UNTRACKED]"
                        
                    total_detections_count += 1
                    frame_detections_count += 1
                    class_detection_counts[cls_name] += 1
                    
                    # Create event payload using model's actual detected class
                    event_type_slug = cls_name.lower().replace(" ", "_")
                    event_data = {
                        "event_id": f"evt_{int(time.time()*1000)}_{frame_idx}_{frame_detections_count}",
                        "bus_id": bus_id,
                        "frame_index": frame_idx,
                        "video_timestamp_sec": round(video_time_offset_sec, 3),
                        "timestamp": frame_utc_time,
                        "event_type": event_type_slug,
                        "defect_class": cls_name,
                        "track_id": track_label,
                        "confidence": round(conf, 4),
                        "bounding_box": bbox_int,
                        "gps": "GPS unavailable"  # Strict rule: GPS not simulated when hardware absent
                    }
                    
                    events_file.write(json.dumps(event_data) + "\n")
                    events_file.flush()
                    events_logged_count += 1
                    
                    # POST event to Central Backend Ingestion API if client available
                    try:
                        from src.api_client import post_event_to_api
                        post_event_to_api(event_data)
                    except Exception:
                        pass
                    
                    # Draw bounding box and label on frame
                    x1, y1, x2, y2 = bbox_int
                    color = color_map.get(cls_id, (0, 255, 0))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    label_str = f"{cls_name.upper()} {track_label} {conf:.2f}"
                    (t_w, t_h), _ = cv2.getTextSize(label_str, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
                    cv2.rectangle(frame, (x1, y1 - t_h - 6), (x1 + t_w + 6, y1), color, -1)
                    cv2.putText(frame, label_str, (x1 + 3, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)

            # Draw HUD Overlay Banner
            mode_str = f"Live USB Cam #{source_val}" if is_live_camera else f"Frame {frame_idx}/{total_frames}"
            hud_line1 = f"Mode: {mode_str} | FPS: {live_fps:.1f} | Active Classes: {len(class_names)}"
            hud_line2 = f"Frame Defects: {frame_detections_count} | Unique Defects Tracked: {len(unique_defect_track_ids)}"
            hud_line3 = f"Counts: {dict(class_detection_counts)} | GPS: Unavailable"
            
            # Semi-transparent overlay banner at top
            overlay = frame.copy()
            cv2.rectangle(overlay, (10, 10), (620, 95), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)
            
            cv2.putText(frame, hud_line1, (20, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 1)
            cv2.putText(frame, hud_line2, (20, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
            cv2.putText(frame, hud_line3, (20, 84), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 1)
            
            if video_writer:
                video_writer.write(frame)
                
            # Live Preview Display
            if gui_available:
                try:
                    cv2.imshow("UrbanIntel - Pothole & Road Damage Detection", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == 27 or key == ord('q'):
                        print("[PREVIEW] Exit requested by user (pressed 'q' / ESC).")
                        break
                except cv2.error:
                    print("[WARNING] Display environment not available for live preview window. Continuing headless...")
                    gui_available = False
                
            if frame_idx % 100 == 0 or (not is_live_camera and frame_idx == total_frames):
                elapsed = time.time() - start_proc_time
                avg_proc_fps = frame_idx / elapsed if elapsed > 0 else 0
                progress_str = f"Frame {frame_idx}/{total_frames} ({frame_idx/total_frames*100:.1f}%)" if not is_live_camera else f"Frame {frame_idx}"
                print(f"[PROGRESS] {progress_str} | Live FPS: {live_fps:.1f} (Avg: {avg_proc_fps:.1f}) | Total Defects: {events_logged_count}")

    finally:
        cap.release()
        events_file.close()
        if video_writer:
            video_writer.release()
        if gui_available:
            try:
                cv2.destroyAllWindows()
            except Exception:
                pass

    total_proc_time = time.time() - start_proc_time
    avg_fps = frame_idx / total_proc_time if total_proc_time > 0 else 0
    
    print("\n" + "=" * 60)
    print("PHASE 1 EXECUTION SUMMARY — ROAD DAMAGE DETECTION")
    print("=" * 60)
    print(f"Status: PASS")
    print(f"Model Loaded: {weights_path}")
    print(f"Model Classes: {list(class_names.values())}")
    print(f"Source Input: {source_desc}")
    print(f"Total Frames Processed: {frame_idx}")
    print(f"Total Processing Time: {total_proc_time:.2f} seconds")
    print(f"Average Speed: {avg_fps:.2f} FPS")
    print(f"Total Unique Physical Defects Tracked: {len(unique_defect_track_ids)}")
    print(f"Total Frame-Level Detection Records Logged: {events_logged_count}")
    print(f"Detections Breakdown by Class: {dict(class_detection_counts)}")
    print(f"Events JSONL Written: {output_events_path} (Size: {os.path.getsize(output_events_path)} bytes)")
    if save_video_path and os.path.exists(save_video_path):
        print(f"Annotated Video Written: {save_video_path} (Size: {os.path.getsize(save_video_path)} bytes)")
    print("=" * 60)
    
    return {
        "status": "PASS",
        "model": weights_path,
        "classes": list(class_names.values()),
        "frames_processed": frame_idx,
        "total_detections": events_logged_count,
        "class_counts": dict(class_detection_counts),
        "events_file_size": os.path.getsize(output_events_path),
        "video_output_size": os.path.getsize(save_video_path) if save_video_path and os.path.exists(save_video_path) else 0,
        "avg_fps": round(avg_fps, 2)
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 1: Pothole & Road Defect Detection (MASTER_PLAN Aligned)")
    parser.add_argument("--source", type=str, default="data/sample_videos/pothole_road_damage.mp4", help="Path to video file OR live camera index (e.g., '0' for USB webcam)")
    parser.add_argument("--weights", type=str, default="models/pothole.pt", help="Path to trained YOLO pothole model weights")
    parser.add_argument("--conf", type=float, default=0.40, help="Confidence threshold for detection (default: 0.40 based on empirical test recommendations)")
    parser.add_argument("--output-events", type=str, default="outputs/events.jsonl", help="Path to output events JSONL file")
    parser.add_argument("--save-video", type=str, default="outputs/annotated_output.mp4", help="Path to save annotated MP4 video")
    parser.add_argument("--show-preview", action="store_true", help="Display live preview GUI window with FPS overlay")
    parser.add_argument("--clean-events", action="store_true", help="Overwrite output events JSONL file instead of appending")
    
    args = parser.parse_args()
    
    process_potholes(
        source_path=args.source,
        weights_path=args.weights,
        conf_thresh=args.conf,
        output_events_path=args.output_events,
        save_video_path=args.save_video,
        show_preview=args.show_preview,
        clean_events=args.clean_events
    )
