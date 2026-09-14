import os
import glob
import cv2
import json
import time
import torch
import numpy as np
from ultralytics import YOLO
import easyocr

def run_integrated_pipeline():
    print("=== ANPR DETECTOR + EASYOCR INTEGRATED PIPELINE ===", flush=True)

    # 1. Paths and Setup
    model_path = "anpr/runs/anpr_detection_v1/weights/best.pt"
    video_path = "data/sample_videos/anpr.mp4"
    real_img_dir = "anpr/combined_dataset/detection/test/images"
    output_dir = "anpr/outputs/anpr_ocr_v1"
    real_img_out_dir = os.path.join(output_dir, "real_images")
    video_out_path = os.path.join(output_dir, "anpr_ocr_video_annotated.mp4")

    os.makedirs(real_img_out_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # 2. Load Models
    print(f"Loading YOLOv8n ANPR detector weights from: {model_path}", flush=True)
    model = YOLO(model_path)
    
    print("Initializing EasyOCR Reader (CPU mode for optimized pipeline)...", flush=True)
    ocr_reader = easyocr.Reader(['en'], gpu=False, verbose=False)

    # ---------------------------------------------------------
    # PART A: Real Image Pipeline Benchmark
    # ---------------------------------------------------------
    print("\n--- PART A: Testing Integrated Pipeline on Real Images ---", flush=True)
    sample_images = sorted(glob.glob(os.path.join(real_img_dir, "*.*")))[:10] # Top 10 sample test images
    
    image_results = []

    for img_path in sample_images:
        fname = os.path.basename(img_path)
        img = cv2.imread(img_path)
        if img is None:
            continue
        
        annotated_img = img.copy()
        
        # Detector inference
        results = model.predict(img, conf=0.25, verbose=False)[0]
        
        det_info = []
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            det_conf = float(box.conf[0])
            
            # Crop plate region with small margin
            h, w, _ = img.shape
            pad_x = int((x2 - x1) * 0.05)
            pad_y = int((y2 - y1) * 0.05)
            crop_x1 = max(0, x1 - pad_x)
            crop_y1 = max(0, y1 - pad_y)
            crop_x2 = min(w, x2 + pad_x)
            crop_y2 = min(h, y2 + pad_y)
            
            plate_crop = img[crop_y1:crop_y2, crop_x1:crop_x2]
            
            # OCR Inference
            ocr_res = ocr_reader.readtext(plate_crop, detail=1)
            if ocr_res:
                raw_ocr_text = " ".join([r[1] for r in ocr_res])
                ocr_conf = float(np.mean([float(r[2]) for r in ocr_res]))
            else:
                raw_ocr_text = ""
                ocr_conf = 0.0
                
            clean_ocr = "".join(c for c in raw_ocr_text if c.isalnum()).upper()
            
            # Draw overlay on image
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label_str = f"{clean_ocr} ({det_conf:.2f}|{ocr_conf:.2f})" if clean_ocr else f"Plate ({det_conf:.2f})"
            
            cv2.putText(annotated_img, label_str, (x1, max(20, y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            det_info.append({
                "bbox": [x1, y1, x2, y2],
                "detector_conf": det_conf,
                "raw_ocr_text": raw_ocr_text,
                "clean_ocr": clean_ocr,
                "ocr_conf": ocr_conf
            })

        out_img_path = os.path.join(real_img_out_dir, fname)
        cv2.imwrite(out_img_path, annotated_img)
        image_results.append({
            "image_name": fname,
            "detections": det_info
        })
        print(f"  Processed {fname}: {len(det_info)} detections -> Saved to {out_img_path}", flush=True)

    # ---------------------------------------------------------
    # PART B: Real Video Pipeline Benchmark
    # ---------------------------------------------------------
    print("\n--- PART B: Testing Integrated Pipeline on Real Video (anpr.mp4) ---", flush=True)
    cap = cv2.VideoCapture(video_path)
    vid_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vid_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vid_fps = cap.get(cv2.CAP_PROP_FPS)
    vid_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    vid_duration = vid_count / vid_fps if vid_fps > 0 else 0

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_video = cv2.VideoWriter(video_out_path, fourcc, vid_fps, (vid_width, vid_height))

    total_detections = 0
    total_ocr_attempts = 0
    successful_ocr_reads = 0
    failed_ocr_reads = 0
    recognized_strings = {}
    ocr_latencies = []

    video_start_time = time.time()
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        
        # Detector inference on frame
        results = model.predict(frame, conf=0.25, verbose=False)[0]
        
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            det_conf = float(box.conf[0])
            total_detections += 1
            
            # Crop plate region
            h, w, _ = frame.shape
            pad_x = int((x2 - x1) * 0.05)
            pad_y = int((y2 - y1) * 0.05)
            crop_x1 = max(0, x1 - pad_x)
            crop_y1 = max(0, y1 - pad_y)
            crop_x2 = min(w, x2 + pad_x)
            crop_y2 = min(h, y2 + pad_y)

            plate_crop = frame[crop_y1:crop_y2, crop_x1:crop_x2]
            
            total_ocr_attempts += 1
            t_ocr_0 = time.time()
            ocr_res = ocr_reader.readtext(plate_crop, detail=1)
            t_ocr = time.time() - t_ocr_0
            ocr_latencies.append(t_ocr)

            if ocr_res:
                raw_text = " ".join([r[1] for r in ocr_res])
                ocr_conf = float(np.mean([float(r[2]) for r in ocr_res]))
            else:
                raw_text = ""
                ocr_conf = 0.0

            clean_text = "".join(c for c in raw_text if c.isalnum()).upper()

            if len(clean_text) >= 4 and ocr_conf > 0.20:
                successful_ocr_reads += 1
                recognized_strings[clean_text] = recognized_strings.get(clean_text, 0) + 1
                overlay_text = f"{clean_text} ({det_conf:.2f}|{ocr_conf:.2f})"
                box_color = (0, 255, 0) # Green for successful read
            else:
                failed_ocr_reads += 1
                overlay_text = f"PLATE ({det_conf:.2f})"
                box_color = (0, 165, 255) # Orange for unreadable/uncertain OCR

            # Annotate video frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            cv2.putText(frame, overlay_text, (x1, max(25, y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, box_color, 2)

        out_video.write(frame)

        if frame_idx % 200 == 0 or frame_idx == vid_count:
            elapsed = time.time() - video_start_time
            proc_fps = frame_idx / elapsed
            print(f"  Frame {frame_idx}/{vid_count} ({proc_fps:.2f} FPS) | Detections: {total_detections} | OCR Reads: {successful_ocr_reads} | Failed: {failed_ocr_reads}", flush=True)

    cap.release()
    out_video.release()

    total_video_proc_time = time.time() - video_start_time
    effective_pipeline_fps = vid_count / total_video_proc_time if total_video_proc_time > 0 else 0
    avg_ocr_latency_ms = (sum(ocr_latencies) / len(ocr_latencies) * 1000) if ocr_latencies else 0

    print(f"\n--- REAL VIDEO BENCHMARK SUMMARY ---", flush=True)
    print(f"Video Resolution: {vid_width}x{vid_height}", flush=True)
    print(f"Source FPS: {vid_fps:.2f} | Total Frames: {vid_count} | Duration: {vid_duration:.2f}s", flush=True)
    print(f"Total Plate Bounding Box Detections: {total_detections}", flush=True)
    print(f"Total OCR Attempts: {total_ocr_attempts}", flush=True)
    print(f"Successful OCR Reads (len >= 4, conf > 0.20): {successful_ocr_reads}", flush=True)
    print(f"Failed / Uncertain OCR Cases: {failed_ocr_reads}", flush=True)
    print(f"Distinct Recognized Plate Strings: {len(recognized_strings)}", flush=True)
    print(f"Total Pipeline Processing Time: {total_video_proc_time:.2f}s", flush=True)
    print(f"Effective Processing FPS: {effective_pipeline_fps:.2f} FPS", flush=True)
    print(f"Average Per-Crop OCR Latency: {avg_ocr_latency_ms:.2f} ms", flush=True)

    print("\nTop Recognized Plate Strings in Video:", flush=True)
    sorted_strings = sorted(recognized_strings.items(), key=lambda x: x[1], reverse=True)[:15]
    for p_str, count in sorted_strings:
        print(f"  - '{p_str}': {count} frames", flush=True)

    video_metrics = {
        "video_path": video_path,
        "resolution": f"{vid_width}x{vid_height}",
        "source_fps": vid_fps,
        "total_frames": vid_count,
        "duration_sec": vid_duration,
        "detector_confidence_threshold": 0.25,
        "total_plate_detections": total_detections,
        "total_ocr_attempts": total_ocr_attempts,
        "successful_ocr_reads": successful_ocr_reads,
        "failed_ocr_reads": failed_ocr_reads,
        "distinct_recognized_strings_count": len(recognized_strings),
        "total_processing_time_sec": round(total_video_proc_time, 2),
        "effective_pipeline_fps": round(effective_pipeline_fps, 2),
        "avg_ocr_latency_ms": round(avg_ocr_latency_ms, 2),
        "recognized_strings_distribution": sorted_strings,
        "output_video_path": video_out_path
    }

    with open("scratch/ocr_video_metrics.json", "w") as fp:
        json.dump(video_metrics, fp, indent=2)

    print(f"\nSaved video metrics to scratch/ocr_video_metrics.json", flush=True)
    print(f"Annotated video saved to: {video_out_path}", flush=True)

if __name__ == "__main__":
    run_integrated_pipeline()
