import os
import glob
import cv2
import json

def run_ocr_audit():
    ocr_dir = "anpr/combined_dataset/ocr"
    images_dir = os.path.join(ocr_dir, "images")
    labels_dir = os.path.join(ocr_dir, "labels")

    print(f"=== ANPR OCR DATA AUDIT ===")
    print(f"Scanning OCR directory: {ocr_dir}")

    img_files = sorted(glob.glob(os.path.join(images_dir, "*.*")))
    lbl_files = sorted(glob.glob(os.path.join(labels_dir, "*.*")))

    print(f"Total raw image files found: {len(img_files)}")
    print(f"Total raw label files found: {len(lbl_files)}")

    # Inspect label formats and sample labels
    label_samples = []
    for f in lbl_files[:10]:
        try:
            with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read().strip()
                label_samples.append((os.path.basename(f), content))
        except Exception as e:
            label_samples.append((os.path.basename(f), f"ERROR: {e}"))

    print("\nSample label content (first 10 files):")
    for fname, content in label_samples:
        print(f"  {fname}: '{content}'")

    # Full audit metrics
    usable_samples = []
    excluded_samples = []

    # Map image base names to image paths
    img_map = {os.path.splitext(os.path.basename(p))[0]: p for p in img_files}
    lbl_map = {os.path.splitext(os.path.basename(p))[0]: p for p in lbl_files}

    all_keys = sorted(set(list(img_map.keys()) + list(lbl_map.keys())))

    char_counts = {}
    label_lengths = []
    formats = set()

    for k in all_keys:
        img_path = img_map.get(k)
        lbl_path = lbl_map.get(k)

        if not img_path:
            excluded_samples.append({
                "id": k,
                "reason": "Missing image file",
                "img_path": None,
                "lbl_path": lbl_path
            })
            continue

        if not lbl_path:
            excluded_samples.append({
                "id": k,
                "reason": "Missing label file",
                "img_path": img_path,
                "lbl_path": None
            })
            continue

        # Verify image readability
        img = cv2.imread(img_path)
        if img is None:
            excluded_samples.append({
                "id": k,
                "reason": "Unreadable/Corrupt image file",
                "img_path": img_path,
                "lbl_path": lbl_path
            })
            continue

        h, w, c = img.shape

        # Read and parse label
        try:
            with open(lbl_path, 'r', encoding='utf-8', errors='ignore') as fp:
                raw_text = fp.read().strip()

            # Parse format: Check if text, json, or YOLO-style
            # Many Indian license plate OCR datasets use plain text or filename/label string
            # Check lines
            lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
            
            if not lines:
                excluded_samples.append({
                    "id": k,
                    "reason": "Empty label file",
                    "img_path": img_path,
                    "lbl_path": lbl_path
                })
                continue
            
            # If line has YOLO format (class x y w h text or similar) or single text string
            # Let's inspect parsing logic
            parsed_label = lines[0]
            
            # Basic validation of parsed_label
            # Check if it contains alphanumeric plate text
            clean_gt = "".join(c for c in parsed_label if c.isalnum()).upper()
            
            if len(clean_gt) < 2:
                excluded_samples.append({
                    "id": k,
                    "reason": f"Malformed label string: '{parsed_label}' (clean: '{clean_gt}')",
                    "img_path": img_path,
                    "lbl_path": lbl_path
                })
                continue

            # Record usable
            usable_samples.append({
                "id": k,
                "img_path": img_path,
                "lbl_path": lbl_path,
                "raw_label": parsed_label,
                "clean_gt": clean_gt,
                "img_size": (w, h)
            })

            label_lengths.append(len(clean_gt))
            for char in clean_gt:
                char_counts[char] = char_counts.get(char, 0) + 1

        except Exception as e:
            excluded_samples.append({
                "id": k,
                "reason": f"Label read error: {e}",
                "img_path": img_path,
                "lbl_path": lbl_path
            })

    print(f"\n--- AUDIT SUMMARY ---")
    print(f"Total Unique Keys Evaluated: {len(all_keys)}")
    print(f"Usable Ground-Truth OCR Samples: {len(usable_samples)}")
    print(f"Excluded Samples: {len(excluded_samples)}")

    if excluded_samples:
        print("\nExclusion Breakdown by Reason:")
        reasons = {}
        for ex in excluded_samples:
            r = ex["reason"].split(":")[0]
            reasons[r] = reasons.get(r, 0) + 1
        for r, cnt in reasons.items():
            print(f"  - {r}: {cnt}")

    print(f"\nCharacter Statistics (Total Usable Chars: {sum(char_counts.values())}):")
    sorted_chars = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)
    print("Top 15 most frequent characters:", sorted_chars[:15])

    # Save audit output to json for reporting
    audit_data = {
        "total_unique_keys": len(all_keys),
        "total_images": len(img_files),
        "total_labels": len(lbl_files),
        "usable_count": len(usable_samples),
        "excluded_count": len(excluded_samples),
        "exclusions": excluded_samples,
        "char_counts": char_counts,
        "label_length_min": min(label_lengths) if label_lengths else 0,
        "label_length_max": max(label_lengths) if label_lengths else 0,
        "label_length_avg": sum(label_lengths)/len(label_lengths) if label_lengths else 0
    }

    with open("scratch/ocr_audit_summary.json", "w") as fp:
        json.dump(audit_data, fp, indent=2)

    print("\nSaved audit summary to scratch/ocr_audit_summary.json")

if __name__ == "__main__":
    run_ocr_audit()
