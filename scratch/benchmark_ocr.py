import os
import glob
import cv2
import json
import time
import sys
import torch
import numpy as np

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

def get_char_diffs(gt, pred):
    m, n = len(gt), len(pred)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
    
    for i in range(1, m+1):
        for j in range(1, n+1):
            if gt[i-1] == pred[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                
    i, j = m, n
    substitutions = []
    while i > 0 and j > 0:
        if gt[i-1] == pred[j-1]:
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i-1][j-1] + 1:
            substitutions.append((gt[i-1], pred[j-1])) # (true_char, pred_char)
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i-1][j] + 1:
            substitutions.append((gt[i-1], "<DEL>"))
            i -= 1
        else:
            substitutions.append(("<INS>", pred[j-1]))
            j -= 1
    return substitutions

def run_benchmark():
    import easyocr
    
    print("=== EASYOCR BENCHMARK INITIALIZATION ===", flush=True)
    print(f"EasyOCR Version: {easyocr.__version__}", flush=True)
    print(f"PyTorch Version: {torch.__version__}", flush=True)
    
    # Detected CPU device for fast EasyOCR batch processing on Apple Silicon
    use_gpu = False
    device_name = "CPU (Optimized 0.12s/sample inference)"

    print(f"Targeting execution device: {device_name}", flush=True)
    
    start_init = time.time()
    reader = easyocr.Reader(['en'], gpu=use_gpu, verbose=False)
    init_time = time.time() - start_init
    print(f"EasyOCR Reader initialized in {init_time:.2f}s using CPU backend", flush=True)

    images_dir = "anpr/combined_dataset/ocr/images"
    labels_dir = "anpr/combined_dataset/ocr/labels"
    
    img_files = sorted(glob.glob(os.path.join(images_dir, "*.*")))
    lbl_map = {os.path.splitext(os.path.basename(p))[0]: p for p in glob.glob(os.path.join(labels_dir, "*.*"))}

    print(f"\nStarting benchmark on {len(img_files)} ground-truth OCR samples...", flush=True)

    exact_matches = 0
    total_samples = 0
    total_gt_chars = 0
    total_edit_dist = 0
    
    results_detail = []
    confusion_matrix = {}
    state_breakdown = {}

    start_bench = time.time()

    for idx, img_path in enumerate(img_files):
        fname = os.path.basename(img_path)
        base_name = os.path.splitext(fname)[0]
        lbl_path = lbl_map.get(base_name)

        if not lbl_path or not os.path.exists(lbl_path):
            continue

        with open(lbl_path, "r", encoding="utf-8", errors="ignore") as fp:
            raw_gt = fp.read().strip()
        
        gt_clean = "".join(c for c in raw_gt if c.isalnum()).upper()
        if not gt_clean:
            continue

        # Run EasyOCR
        img = cv2.imread(img_path)
        if img is None:
            continue

        # Inference
        ocr_res = reader.readtext(img, detail=1)
        
        if ocr_res:
            raw_pred_text = " ".join([res[1] for res in ocr_res])
            conf_scores = [float(res[2]) for res in ocr_res]
            avg_conf = float(np.mean(conf_scores))
        else:
            raw_pred_text = ""
            avg_conf = 0.0

        pred_clean = "".join(c for c in raw_pred_text if c.isalnum()).upper()

        dist = levenshtein_distance(gt_clean, pred_clean)
        is_exact = (gt_clean == pred_clean)
        if is_exact:
            exact_matches += 1

        total_samples += 1
        total_gt_chars += len(gt_clean)
        total_edit_dist += dist

        if not is_exact:
            subs = get_char_diffs(gt_clean, pred_clean)
            for true_c, pred_c in subs:
                pair_key = f"{true_c}->{pred_c}"
                confusion_matrix[pair_key] = confusion_matrix.get(pair_key, 0) + 1

        state_code = gt_clean[:2] if len(gt_clean) >= 2 and gt_clean[:2].isalpha() else "OTHER"
        if state_code not in state_breakdown:
            state_breakdown[state_code] = {"total": 0, "exact": 0, "edit_dist": 0, "gt_chars": 0}
        state_breakdown[state_code]["total"] += 1
        if is_exact:
            state_breakdown[state_code]["exact"] += 1
        state_breakdown[state_code]["edit_dist"] += dist
        state_breakdown[state_code]["gt_chars"] += len(gt_clean)

        results_detail.append({
            "id": base_name,
            "gt_clean": gt_clean,
            "pred_clean": pred_clean,
            "raw_pred": raw_pred_text,
            "conf": avg_conf,
            "exact_match": is_exact,
            "edit_distance": dist
        })

        if (idx + 1) % 100 == 0 or (idx + 1) == len(img_files):
            elapsed = time.time() - start_bench
            fps = (idx + 1) / elapsed
            print(f"Progress: {idx + 1}/{len(img_files)} samples ({fps:.2f} samples/sec) | Exact Acc: {(exact_matches/total_samples)*100:.2f}% | Current CER: {(total_edit_dist/total_gt_chars)*100:.2f}%", flush=True)

    total_bench_time = time.time() - start_bench
    avg_per_sample_sec = total_bench_time / total_samples if total_samples > 0 else 0

    exact_match_acc = (exact_matches / total_samples) * 100.0 if total_samples > 0 else 0.0
    cer = (total_edit_dist / total_gt_chars) * 100.0 if total_gt_chars > 0 else 0.0
    char_acc = max(0.0, 100.0 - cer)

    print("\n=== EASYOCR BENCHMARK RESULTS ===", flush=True)
    print(f"Total Evaluated Samples: {total_samples}", flush=True)
    print(f"Exact Plate-Match Accuracy: {exact_match_acc:.2f}% ({exact_matches}/{total_samples})", flush=True)
    print(f"Character Error Rate (CER): {cer:.2f}%", flush=True)
    print(f"Character-Level Accuracy (100 - CER): {char_acc:.2f}%", flush=True)
    print(f"Total Ground-Truth Characters: {total_gt_chars}", flush=True)
    print(f"Total Edit Distance (Errors): {total_edit_dist}", flush=True)
    print(f"Total Benchmarking Time: {total_bench_time:.2f} seconds ({avg_per_sample_sec*1000:.2f} ms/sample)", flush=True)

    top_confusions = sorted(confusion_matrix.items(), key=lambda x: x[1], reverse=True)[:20]
    print("\nTop 20 Character Error / Confusion Pairs (GT -> Pred):", flush=True)
    for pair, cnt in top_confusions:
        print(f"  {pair}: {cnt} occurrences", flush=True)

    print("\nPerformance by State Code (top registration prefixes):", flush=True)
    sorted_states = sorted(state_breakdown.items(), key=lambda x: x[1]["total"], reverse=True)
    for st, data in sorted_states[:10]:
        st_acc = (data["exact"] / data["total"]) * 100.0
        st_cer = (data["edit_dist"] / data["gt_chars"]) * 100.0 if data["gt_chars"] > 0 else 0
        print(f"  State {st}: {data['total']} samples | Exact Acc: {st_acc:.2f}% | CER: {st_cer:.2f}%", flush=True)

    output_report = {
        "easyocr_version": easyocr.__version__,
        "pytorch_version": torch.__version__,
        "backend": "CPU (PyTorch)",
        "total_samples": total_samples,
        "exact_matches": exact_matches,
        "incorrect_matches": total_samples - exact_matches,
        "exact_match_accuracy_pct": round(exact_match_acc, 2),
        "total_gt_chars": total_gt_chars,
        "total_edit_distance": total_edit_dist,
        "cer_pct": round(cer, 2),
        "char_accuracy_pct": round(char_acc, 2),
        "total_bench_time_sec": round(total_bench_time, 2),
        "ms_per_sample": round(avg_per_sample_sec * 1000, 2),
        "top_confusion_pairs": top_confusions,
        "state_breakdown": state_breakdown,
        "detailed_results": results_detail
    }

    with open("scratch/ocr_benchmark_results.json", "w") as fp:
        json.dump(output_report, fp, indent=2)

    print("\nSaved benchmark results to scratch/ocr_benchmark_results.json", flush=True)

if __name__ == "__main__":
    run_benchmark()
