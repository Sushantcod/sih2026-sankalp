import os
import glob
import cv2
import json
import time
import torch
import numpy as np
from ultralytics import YOLO
import easyocr

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def run_v2_pipeline():
    print("=== OCR V2 FULL BENCHMARK & VIDEO PIPELINE ===", flush=True)

    # 1. Paths
    model_path = "anpr/runs/anpr_detection_v1/weights/best.pt"
    video_path = "data/sample_videos/anpr.mp4"
    output_dir = "anpr/outputs/anpr_ocr_v2"
    real_img_out_dir = os.path.join(output_dir, "real_images")
    video_out_path = os.path.join(output_dir, "anpr_ocr_v2_video_annotated.mp4")

    os.makedirs(real_img_out_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading YOLOv8n detector: {model_path}", flush=True)
    model = YOLO(model_path)

    print("Initializing EasyOCR Reader (CPU mode)...", flush=True)
    ocr_reader = easyocr.Reader(['en'], gpu=False, verbose=False)

    # ---------------------------------------------------------
    # PART A: Real Image Pipeline Testing
    # ---------------------------------------------------------
    print("\n--- PART A: Testing Integrated V2 Pipeline on Real Test Images ---", flush=True)
    real_img_dir = "anpr/anpr/test/images"
    sample_images = sorted(glob.glob(os.path.join(real_img_dir, "*.*")))[:10]

    for img_p in sample_images:
        fname = os.path.basename(img_p)
        img = cv2.imread(img_p)
        if img is None:
            continue

        annotated_img = img.copy()
        results = model.predict(img, conf=0.25, verbose=False)[0]

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            det_conf = float(box.conf[0])

            h, w, _ = img.shape
            pad_x = int((x2 - x1) * 0.05)
            pad_y = int((y2 - y1) * 0.05)
            crop_x1 = max(0, x1 - pad_x)
            crop_y1 = max(0, y1 - pad_y)
            crop_x2 = min(w, x2 + pad_x)
            crop_y2 = min(h, y2 + pad_y)

            plate_crop = img[crop_y1:crop_y2, crop_x1:crop_x2]
            ocr_res = ocr_reader.readtext(plate_crop, detail=1)

            if ocr_res:
                raw_text = " ".join([r[1] for r in ocr_res])
                ocr_conf = float(np.mean([float(r[2]) for r in ocr_res]))
            else:
                raw_text = ""
                ocr_conf = 0.0

            clean_text = "".join(c for c in raw_text if c.isalnum()).upper()

            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label_str = f"{clean_text} ({det_conf:.2f}|{ocr_conf:.2f})" if clean_text else f"PLATE ({det_conf:.2f})"
            cv2.putText(annotated_img, label_str, (x1, max(20, y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        out_path = os.path.join(real_img_out_dir, fname)
        cv2.imwrite(out_path, annotated_img)
        print(f"  Saved sample output to {out_path}", flush=True)

    # ---------------------------------------------------------
    # PART B: Real Video Pipeline Testing (anpr.mp4)
    # ---------------------------------------------------------
    print("\n--- PART B: Testing Integrated V2 Pipeline on Real Video (anpr.mp4) ---", flush=True)
    cap = cv2.VideoCapture(video_path)
    vid_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vid_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vid_fps = cap.get(cv2.CAP_PROP_FPS)
    vid_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    vid_duration = vid_count / vid_fps if vid_fps > 0 else 0

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_video = cv2.VideoWriter(video_out_path, fourcc, vid_fps, (vid_w, vid_h))

    total_detections = 0
    total_ocr_attempts = 0
    successful_ocr_reads = 0
    failed_ocr_reads = 0
    recognized_strings = {}
    ocr_latencies = []

    start_v = time.time()
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        results = model.predict(frame, conf=0.25, verbose=False)[0]

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            det_conf = float(box.conf[0])
            total_detections += 1

            h, w, _ = frame.shape
            pad_x = int((x2 - x1) * 0.05)
            pad_y = int((y2 - y1) * 0.05)
            crop_x1 = max(0, x1 - pad_x)
            crop_y1 = max(0, y1 - pad_y)
            crop_x2 = min(w, x2 + pad_x)
            crop_y2 = min(h, y2 + pad_y)

            plate_crop = frame[crop_y1:crop_y2, crop_x1:crop_x2]
            total_ocr_attempts += 1
            t0 = time.time()
            ocr_res = ocr_reader.readtext(plate_crop, detail=1)
            t_ocr = time.time() - t0
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
                overlay_label = f"{clean_text} ({det_conf:.2f}|{ocr_conf:.2f})"
                color = (0, 255, 0)
            else:
                failed_ocr_reads += 1
                overlay_label = f"PLATE ({det_conf:.2f})"
                color = (0, 165, 255)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, overlay_label, (x1, max(25, y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)

        out_video.write(frame)

        if frame_idx % 300 == 0 or frame_idx == vid_count:
            elapsed = time.time() - start_v
            fps = frame_idx / elapsed
            print(f"  Frame {frame_idx}/{vid_count} ({fps:.2f} FPS) | Detections: {total_detections} | OCR Reads: {successful_ocr_reads}", flush=True)

    cap.release()
    out_video.release()

    total_proc_time = time.time() - start_v
    effective_fps = vid_count / total_proc_time if total_proc_time > 0 else 0
    avg_ocr_latency = (sum(ocr_latencies) / len(ocr_latencies) * 1000) if ocr_latencies else 0

    print(f"\n--- REAL VIDEO V2 BENCHMARK SUMMARY ---", flush=True)
    print(f"Video Resolution: {vid_w}x{vid_h}", flush=True)
    print(f"Total Frames: {vid_count} | Duration: {vid_duration:.2f}s", flush=True)
    print(f"Total Detections: {total_detections}", flush=True)
    print(f"Total OCR Attempts: {total_ocr_attempts}", flush=True)
    print(f"Successful OCR Reads: {successful_ocr_reads}", flush=True)
    print(f"Failed / Uncertain Reads: {failed_ocr_reads}", flush=True)
    print(f"Distinct Recognized Strings: {len(recognized_strings)}", flush=True)
    print(f"Total Processing Time: {total_proc_time:.2f}s", flush=True)
    print(f"Effective Processing FPS: {effective_fps:.2f} FPS", flush=True)
    print(f"Average Per-Crop OCR Latency: {avg_ocr_latency:.2f} ms", flush=True)

    video_v2_metrics = {
        "video_path": video_path,
        "resolution": f"{vid_w}x{vid_h}",
        "total_frames": vid_count,
        "duration_sec": vid_duration,
        "total_detections": total_detections,
        "total_ocr_attempts": total_ocr_attempts,
        "successful_ocr_reads": successful_ocr_reads,
        "failed_ocr_reads": failed_ocr_reads,
        "distinct_recognized_strings": len(recognized_strings),
        "total_proc_time_sec": round(total_proc_time, 2),
        "effective_fps": round(effective_fps, 2),
        "avg_ocr_latency_ms": round(avg_ocr_latency, 2),
        "output_video_path": video_out_path
    }

    with open("scratch/ocr_v2_video_metrics.json", "w") as fp:
        json.dump(video_v2_metrics, fp, indent=2)

    print("Saved video V2 metrics to scratch/ocr_v2_video_metrics.json", flush=True)

if __name__ == "__main__":
    run_v2_pipeline()
