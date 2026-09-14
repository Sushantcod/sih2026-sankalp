import os
import hashlib
import json

def get_sha256(filepath):
    if not os.path.exists(filepath):
        return "FILE_NOT_FOUND"
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def run_integrity_verification():
    files_to_check = {
        "Phase 1 Pothole Model": "models/pothole.pt",
        "ANPR Detector Best Weights": "anpr/runs/anpr_detection_v1/weights/best.pt",
        "ANPR Detector Last Weights": "anpr/runs/anpr_detection_v1/weights/last.pt",
        "ANPR Video Input": "data/sample_videos/anpr.mp4",
        "OCR Output Video": "anpr/outputs/anpr_ocr_v1/anpr_ocr_video_annotated.mp4",
        "OCR Audit Script": "scratch/ocr_data_audit.py",
        "OCR Benchmark Script": "scratch/benchmark_ocr.py",
        "OCR Integration Script": "scratch/integrated_ocr_test.py"
    }

    checksums = {}
    print("=== ANPR OCR PIPELINE INTEGRITY & CHECKSUM VERIFICATION ===")
    for label, path in files_to_check.items():
        sha = get_sha256(path)
        checksums[label] = {"path": path, "sha256": sha, "exists": os.path.exists(path)}
        print(f"  {label} ({path}):\n    SHA-256: {sha}")

    # Verify Phase 1 model untouched check
    pothole_sha = checksums["Phase 1 Pothole Model"]["sha256"]
    pothole_untouched = (pothole_sha == "947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b")
    print(f"\nPhase 1 Model Untouched Verification: {'PASS' if pothole_untouched else 'FAIL'} (SHA: {pothole_sha})")

    detector_sha = checksums["ANPR Detector Best Weights"]["sha256"]
    detector_untouched = (detector_sha == "d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a")
    print(f"ANPR Detector Best Weights Untouched Verification: {'PASS' if detector_untouched else 'FAIL'} (SHA: {detector_sha})")

    video_exists = checksums["OCR Output Video"]["exists"]
    print(f"Annotated Video Output Exists: {'PASS' if video_exists else 'FAIL'}")

    with open("scratch/ocr_checksums.json", "w") as fp:
        json.dump(checksums, fp, indent=2)

if __name__ == "__main__":
    run_integrity_verification()
