import os
import glob
import cv2
import json
import time
import torch
import numpy as np
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

def preprocess_variant(img, variant_id):
    if variant_id == 1:
        # Variant 1: Original Crop (Baseline V1)
        return img

    h, w = img.shape[:2]
    # 2x Resize for enhanced character detail
    resized = cv2.resize(img, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)

    if variant_id == 2:
        # Variant 2: Grayscale + 2x Resize
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    elif variant_id == 3:
        # Variant 3: CLAHE + 2x Resize
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)

    elif variant_id == 4:
        # Variant 4: Adaptive Threshold (Binarization) + 2x Resize
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        return cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    return img

def run_subset_experiment():
    print("=== OCR V2 PREPROCESSING SUBSET EXPERIMENT (200 SAMPLES) ===", flush=True)
    print("Initializing EasyOCR Reader (CPU Backend)...", flush=True)
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)

    images_dir = "anpr/anpr/ocr/images"
    labels_dir = "anpr/anpr/ocr/labels"

    img_files = sorted(glob.glob(os.path.join(images_dir, "*.*")))[:200]
    lbl_files = [os.path.join(labels_dir, os.path.splitext(os.path.basename(p))[0] + ".txt") for p in img_files]

    usable_pairs = []
    for img_p, lbl_p in zip(img_files, lbl_files):
        if os.path.exists(lbl_p):
            with open(lbl_p, "r", encoding="utf-8", errors="ignore") as fp:
                gt = fp.read().strip()
            clean_gt = "".join(c for c in gt if c.isalnum()).upper()
            if clean_gt:
                usable_pairs.append((img_p, clean_gt))

    print(f"Loaded {len(usable_pairs)} deterministic subset samples.", flush=True)

    variants = [
        (1, "Variant 1: Original Crop (Baseline V1)"),
        (2, "Variant 2: Grayscale + 2x Resize"),
        (3, "Variant 3: CLAHE + 2x Resize"),
        (4, "Variant 4: Adaptive Threshold + 2x Resize")
    ]

    experiment_results = []

    for v_id, v_name in variants:
        print(f"\nEvaluating {v_name}...", flush=True)
        exact_matches = 0
        total_gt_chars = 0
        total_edit_dist = 0
        start_t = time.time()

        for img_p, gt_clean in usable_pairs:
            img = cv2.imread(img_p)
            if img is None:
                continue

            prep_img = preprocess_variant(img, v_id)
            ocr_res = reader.readtext(prep_img, detail=1)

            if ocr_res:
                raw_pred = " ".join([r[1] for r in ocr_res])
            else:
                raw_pred = ""

            pred_clean = "".join(c for c in raw_pred if c.isalnum()).upper()

            dist = levenshtein_distance(gt_clean, pred_clean)
            is_exact = (gt_clean == pred_clean)
            if is_exact:
                exact_matches += 1

            total_gt_chars += len(gt_clean)
            total_edit_dist += dist

        elapsed = time.time() - start_t
        exact_acc = (exact_matches / len(usable_pairs)) * 100.0
        cer = (total_edit_dist / total_gt_chars) * 100.0 if total_gt_chars > 0 else 0.0
        char_acc = max(0.0, 100.0 - cer)
        ms_per_sample = (elapsed / len(usable_pairs)) * 1000.0

        res_dict = {
            "variant_id": v_id,
            "variant_name": v_name,
            "exact_matches": exact_matches,
            "total_samples": len(usable_pairs),
            "exact_match_acc_pct": round(exact_acc, 2),
            "total_gt_chars": total_gt_chars,
            "total_edit_dist": total_edit_dist,
            "cer_pct": round(cer, 2),
            "char_acc_pct": round(char_acc, 2),
            "latency_ms_per_sample": round(ms_per_sample, 2),
            "total_time_sec": round(elapsed, 2)
        }
        experiment_results.append(res_dict)

        print(f"  Exact Match Acc: {exact_acc:.2f}% ({exact_matches}/{len(usable_pairs)}) | CER: {cer:.2f}% | Latency: {ms_per_sample:.1f}ms/sample")

    # Select winner based on priority rules:
    # 1. Exact Match Acc (Primary)
    # 2. CER (Secondary, lower is better)
    # 3. Char Acc (Secondary, higher is better)
    # 4. Latency (Tie breaker, lower is better)
    sorted_results = sorted(experiment_results, key=lambda x: (x["exact_match_acc_pct"], -x["cer_pct"], -x["latency_ms_per_sample"]), reverse=True)
    winning_variant = sorted_results[0]

    print("\n=== SUBSET COMPARISON TABLE ===")
    print(f"{'Variant ID & Name':<45} | {'Exact Acc':<10} | {'CER (%)':<8} | {'Char Acc':<10} | {'Latency':<10}")
    print("-" * 95)
    for r in experiment_results:
        print(f"{r['variant_name']:<45} | {r['exact_match_acc_pct']:<9.2f}% | {r['cer_pct']:<8.2f} | {r['char_acc_pct']:<9.2f}% | {r['latency_ms_per_sample']:<8.1f} ms")

    print(f"\nWINNING PREPROCESSING METHOD: {winning_variant['variant_name']} (Exact Match Acc: {winning_variant['exact_match_acc_pct']}%, CER: {winning_variant['cer_pct']}%)")

    output_data = {
        "subset_size": len(usable_pairs),
        "experiment_results": experiment_results,
        "winning_variant": winning_variant
    }

    with open("scratch/ocr_v2_subset_results.json", "w") as fp:
        json.dump(output_data, fp, indent=2)

if __name__ == "__main__":
    run_subset_experiment()
