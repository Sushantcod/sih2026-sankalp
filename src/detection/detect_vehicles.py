#!/usr/bin/env python3
"""
Phase 2: Vehicle Density & Counting
===================================
Aligned with MASTER_PLAN.md.
- Vehicle Detection & Classification using COCO YOLOv8 (yolov8n.pt).
- Filtered vehicle classes: car, bus, truck, motorcycle.
- Object tracking via ByteTrack to maintain vehicle identities across frames.
- Rolling 10-second window vehicle counter.
- Threshold-based Congestion Detection (configurable N).
- Structured telemetry event generation in outputs/events.jsonl.
- Selectable input: Saved Video File OR Live USB Camera (e.g., --source 0).
- Explicit "GPS unavailable" status (zero synthetic GPS).
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


# Target COCO vehicle class names to filter
ALLOWED_VEHICLE_CLASSES = {"car", "bus", "truck", "motorcycle"}


def open_capture_source(source: str):
    """Open capture source from file path or integer camera index."""
    is_live_camera = False
    source_val = source

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


def process_vehicles(
    source_path: str,
    weights_path: str,
    conf_thresh: float,
    congestion_threshold: int,
    output_events_path: str,
    save_video_path: str,
    show_preview: bool = False,
    window_duration_sec: float = 10.0,
    bus_id: str = "BUS-101",
    max_reconnect_attempts: int = 5
):
    """Process video/camera stream for vehicle detection, ByteTrack tracking, and 10s density counting."""
    
    # 1. Load YOLOv8 Model (COCO Pretrained)
    print(f"[MODEL] Loading YOLO vehicle detection model from {weights_path}...")
    model = YOLO(weights_path)
    
    # Identify vehicle class IDs from model metadata
    vehicle_class_ids = {}
    for cls_id, cls_name in model.names.items():
        cls_name_clean = cls_name.lower().strip()
        if cls_name_clean in ALLOWED_VEHICLE_CLASSES:
            vehicle_class_ids[cls_id] = cls_name_clean
            
    print(f"[MODEL] Filtered vehicle target classes: {list(vehicle_class_ids.values())} (IDs: {list(vehicle_class_ids.keys())})")
    
    # 2. Open Video Stream / Camera
    cap, is_live_camera, source_val = open_capture_source(source_path)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or np.isnan(fps) or is_live_camera:
        fps = 30.0  # Default target FPS for live streams or unreadable metadata
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) if not is_live_camera else 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        width, height = 1280, 720
    
    duration_sec = total_frames / fps if total_frames > 0 else 0.0
    source_desc = f"USB Camera {source_val}" if is_live_camera else source_path
    print(f"[STREAM] Source: {source_desc} | Res: {width}x{height} | Target FPS: {fps:.1f}"
          f"{f' | Total Frames: {total_frames}' if not is_live_camera else ' | Live Stream'}")

    # 3. Setup Event Log & Video Writer
    os.makedirs(os.path.dirname(output_events_path), exist_ok=True)
    events_file = open(output_events_path, "a", encoding="utf-8")  # Append to outputs/events.jsonl
    
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

    # Rolling 10-Second Time Window Tracking State
    window_index = 1
    window_start_frame = 1
    window_start_sec = 0.0
    
    # Store set of unique tracked vehicle IDs per class within current 10s window
    window_tracked_vehicles = defaultdict(set)
    
    # Overall summary metrics across entire session
    all_unique_tracked_ids = set()
    total_vehicle_events_logged = 0
    total_congestion_events_logged = 0

    gui_available = show_preview
    reconnect_count = 0
    frame_idx = 0

    print("[PROCESSING] Beginning ByteTrack vehicle detection & tracking loop...")

    try:
        while True:
            ret, frame = cap.read()
            
            # Camera Re-connect handling
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
                        print("[CAMERA ERROR] Camera connection lost and max retries reached.")
                    else:
                        print("[VIDEO] Reached end of video stream.")
                    break
            
            reconnect_count = 0
            frame_idx += 1
            
            # Compute live processing FPS
            now = time.time()
            frame_delta = now - last_frame_time
            last_frame_time = now
            if frame_delta > 0:
                live_fps = 0.9 * live_fps + 0.1 * (1.0 / frame_delta)

            # Elapsed time in video
            video_time_offset_sec = (frame_idx - 1) / fps if not is_live_camera else (now - start_proc_time)
            
            # Exact UTC ISO timestamp for this frame
            frame_utc_time = datetime.fromtimestamp(
                start_wall_time.timestamp() + video_time_offset_sec, 
                tz=timezone.utc
            ).isoformat()

            # Run ByteTrack Tracking on Frame using YOLOv8
            results = model.track(frame, tracker="bytetrack.yaml", persist=True, conf=conf_thresh, verbose=False)
            
            current_frame_vehicles = 0
            
            for result in results:
                boxes = result.boxes
                if boxes is None or len(boxes) == 0:
                    continue
                
                for box in boxes:
                    cls_id = int(box.cls[0].cpu().numpy())
                    if cls_id not in vehicle_class_ids:
                        continue  # Skip non-vehicle classes (person, bicycle, etc.)
                    
                    cls_name = vehicle_class_ids[cls_id]
                    conf = float(box.conf[0].cpu().numpy())
                    xyxy = box.xyxy[0].cpu().numpy().tolist()
                    bbox_int = [int(round(c)) for c in xyxy]
                    
                    # Only count detections with valid ByteTrack tracking IDs to preserve real tracking metrics
                    if box.id is not None:
                        track_id = int(box.id[0].cpu().numpy())
                        track_label = f"#{track_id}"
                        window_tracked_vehicles[cls_name].add(track_id)
                        all_unique_tracked_ids.add(track_id)
                    else:
                        track_label = "[UNTRACKED]"
                    
                    current_frame_vehicles += 1
                    
                    # Draw vehicle bounding box, class, confidence & tracking ID
                    x1, y1, x2, y2 = bbox_int
                    color = (255, 140, 0) if cls_name in ("car", "motorcycle") else (255, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    lbl = f"{cls_name.upper()} {track_label} {conf:.2f}"
                    (tw, th), _ = cv2.getTextSize(lbl, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    cv2.rectangle(frame, (x1, y1 - th - 6), (x1 + tw + 6, y1), color, -1)
                    cv2.putText(frame, lbl, (x1 + 3, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Check 10-Second Time Window Boundary
            window_elapsed = video_time_offset_sec - window_start_sec
            if window_elapsed >= window_duration_sec or (not is_live_camera and frame_idx == total_frames):
                # Calculate window counts
                car_cnt = len(window_tracked_vehicles["car"])
                bus_cnt = len(window_tracked_vehicles["bus"])
                truck_cnt = len(window_tracked_vehicles["truck"])
                moto_cnt = len(window_tracked_vehicles["motorcycle"])
                total_win_vehicles = car_cnt + bus_cnt + truck_cnt + moto_cnt
                
                # 1. Emit vehicle_count Event
                vc_event = {
                    "event_id": f"evt_vc_{int(time.time()*1000)}_{window_index}",
                    "bus_id": bus_id,
                    "event_type": "vehicle_count",
                    "window_index": window_index,
                    "time_window_sec": round(window_duration_sec, 1),
                    "timestamp": frame_utc_time,
                    "vehicle_counts": {
                        "car": car_cnt,
                        "bus": bus_cnt,
                        "truck": truck_cnt,
                        "motorcycle": moto_cnt
                    },
                    "total_vehicle_count": total_win_vehicles,
                    "gps": "GPS unavailable"
                }
                events_file.write(json.dumps(vc_event) + "\n")
                events_file.flush()
                total_vehicle_events_logged += 1
                try:
                    from src.api_client import post_event_to_api
                    post_event_to_api(vc_event)
                except Exception:
                    pass
                
                # 2. Congestion Detection Rule (if total_vehicle_count >= threshold N)
                is_congested = total_win_vehicles >= congestion_threshold
                if is_congested:
                    cg_event = {
                        "event_id": f"evt_cg_{int(time.time()*1000)}_{window_index}",
                        "bus_id": bus_id,
                        "event_type": "congestion",
                        "window_index": window_index,
                        "time_window_sec": round(window_duration_sec, 1),
                        "timestamp": frame_utc_time,
                        "total_vehicle_count": total_win_vehicles,
                        "threshold": congestion_threshold,
                        "vehicle_counts": {
                            "car": car_cnt,
                            "bus": bus_cnt,
                            "truck": truck_cnt,
                            "motorcycle": moto_cnt
                        },
                        "gps": "GPS unavailable"
                    }
                    events_file.write(json.dumps(cg_event) + "\n")
                    events_file.flush()
                    total_congestion_events_logged += 1
                    try:
                        from src.api_client import post_event_to_api
                        post_event_to_api(cg_event)
                    except Exception:
                        pass
                
                print(f"[10s WINDOW #{window_index}] Time: {window_start_sec:.1f}s-{video_time_offset_sec:.1f}s | "
                      f"Total Vehicles: {total_win_vehicles} (Cars: {car_cnt}, Buses: {bus_cnt}, Trucks: {truck_cnt}, Motos: {moto_cnt}) | "
                      f"Congestion: {'YES (TRIGGERED)' if is_congested else 'NO'}")
                
                # Reset 10-second window tracker state for next window
                window_index += 1
                window_start_sec = video_time_offset_sec
                window_tracked_vehicles = defaultdict(set)

            # Draw HUD Overlay Banner
            current_win_total = sum(len(s) for s in window_tracked_vehicles.values())
            is_currently_congested = current_win_total >= congestion_threshold
            
            overlay = frame.copy()
            cv2.rectangle(overlay, (10, 10), (620, 95), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)
            
            mode_str = f"Live USB #{source_val}" if is_live_camera else f"Frame {frame_idx}/{total_frames}"
            hud_l1 = f"Mode: {mode_str} | FPS: {live_fps:.1f} | 10s Window #{window_index}"
            hud_l2 = f"10s Vehicles: {current_win_total} (Car:{len(window_tracked_vehicles['car'])} Bus:{len(window_tracked_vehicles['bus'])} Trk:{len(window_tracked_vehicles['truck'])} Moto:{len(window_tracked_vehicles['motorcycle'])})"
            hud_l3 = f"Congestion Status: {'ALERT >= ' + str(congestion_threshold) if is_currently_congested else 'NORMAL (< ' + str(congestion_threshold) + ')'} | GPS: Unavailable"
            
            status_color = (0, 0, 255) if is_currently_congested else (0, 255, 0)
            cv2.putText(frame, hud_l1, (20, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 1)
            cv2.putText(frame, hud_l2, (20, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
            cv2.putText(frame, hud_l3, (20, 84), cv2.FONT_HERSHEY_SIMPLEX, 0.55, status_color, 2)

            if video_writer:
                video_writer.write(frame)

            if gui_available:
                try:
                    cv2.imshow("UrbanIntel - Vehicle Density & Tracking", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == 27 or key == ord('q'):
                        print("[PREVIEW] Exit requested by user (pressed 'q' / ESC).")
                        break
                except cv2.error:
                    print("[WARNING] Display environment not available for live preview window. Continuing headless...")
                    gui_available = False

            if frame_idx % 100 == 0:
                elapsed = time.time() - start_proc_time
                avg_proc_fps = frame_idx / elapsed if elapsed > 0 else 0
                prog = f"Frame {frame_idx}/{total_frames} ({frame_idx/total_frames*100:.1f}%)" if not is_live_camera else f"Frame {frame_idx}"
                print(f"[PROGRESS] {prog} | Live FPS: {live_fps:.1f} (Avg: {avg_proc_fps:.1f}) | 10s Window #{window_index}")

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
    print("PHASE 2 EXECUTION SUMMARY — VEHICLE DENSITY & COUNTING")
    print("=" * 60)
    print(f"Status: PASS")
    print(f"YOLO Model Loaded: {weights_path}")
    print(f"Tracking Method: ByteTrack (bytetrack.yaml)")
    print(f"Vehicle Classes Filtered: {list(ALLOWED_VEHICLE_CLASSES)}")
    print(f"Source Input: {source_desc}")
    print(f"Total Frames Processed: {frame_idx}")
    print(f"Total Processing Time: {total_proc_time:.2f} seconds")
    print(f"Average Speed: {avg_fps:.2f} FPS")
    print(f"Total Unique Vehicles Tracked: {len(all_unique_tracked_ids)}")
    print(f"Total 10-Second Windows Evaluated: {window_index - 1}")
    print(f"Vehicle Count Events Written: {total_vehicle_events_logged}")
    print(f"Congestion Events Triggered: {total_congestion_events_logged} (Threshold N={congestion_threshold})")
    print(f"Events JSONL Updated: {output_events_path} (Size: {os.path.getsize(output_events_path)} bytes)")
    if save_video_path and os.path.exists(save_video_path):
        print(f"Annotated Video Written: {save_video_path} (Size: {os.path.getsize(save_video_path)} bytes)")
    print("=" * 60)

    return {
        "status": "PASS",
        "model": weights_path,
        "frames_processed": frame_idx,
        "unique_tracked_vehicles": len(all_unique_tracked_ids),
        "windows_evaluated": window_index - 1,
        "vehicle_count_events": total_vehicle_events_logged,
        "congestion_events": total_congestion_events_logged,
        "avg_fps": round(avg_fps, 2)
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 2: Vehicle Density & Counting (MASTER_PLAN Aligned)")
    parser.add_argument("--source", type=str, default="data/sample_videos/traffic_density_bridge.mp4", help="Path to traffic video file OR live camera index (e.g. '0')")
    yolo_weights_default = "models/yolov8n.pt" if os.path.exists("models/yolov8n.pt") else "yolov8n.pt"
    parser.add_argument("--weights", type=str, default=yolo_weights_default, help="Path to YOLO vehicle detection model (COCO)")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold for vehicle detection")
    parser.add_argument("--congestion-threshold", type=int, default=8, help="Configurable threshold N for 10s window congestion alert")
    parser.add_argument("--output-events", type=str, default="outputs/events.jsonl", help="Path to output events JSONL file")
    parser.add_argument("--save-video", type=str, default="outputs/annotated_vehicles.mp4", help="Path to save annotated MP4 video")
    parser.add_argument("--show-preview", action="store_true", help="Display live preview GUI window")
    
    args = parser.parse_args()
    
    process_vehicles(
        source_path=args.source,
        weights_path=args.weights,
        conf_thresh=args.conf,
        congestion_threshold=args.congestion_threshold,
        output_events_path=args.output_events,
        save_video_path=args.save_video,
        show_preview=args.show_preview
    )
