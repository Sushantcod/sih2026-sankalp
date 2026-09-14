import os
import sys
import shutil
import hashlib
from ultralytics import YOLO

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATASET_DIR = os.path.join(PROJECT_ROOT, "Infrastructure/indian traffic sign dataset")
YAML_PATH = os.path.join(DATASET_DIR, "data_abs.yaml")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "models/infrastructure")
FINAL_MODEL_PATH = os.path.join(OUTPUT_DIR, "infrastructure_detector.pt")

def create_abs_yaml():
    yaml_content = f"""path: "{DATASET_DIR}"
train: train/images
val: valid/images
test: test/images

nc: 57
names: ['-Road narrows on right', '50 mph speed limit', 'Advance Direction', 'Attention Please-', 'Beware of children', 'Built Up Area', 'Bullock and Hand Cart Prohibited', 'Bus Stop', 'CYCLE ROUTE AHEAD WARNING', 'Cycle Prohibited', 'Dangerous Left Curve Ahead', 'Dangerous Rright Curve Ahead', 'End of all speed and passing limits', 'Expressway Rout Marking', 'FS 31 Entry Ramp for Expressway', 'Filling Station', 'Give Way', 'Go Straight or Turn Right', 'Go straight or turn left', 'Height Limit', 'Keep-Left', 'Keep-Right', 'Left Hand Curv', 'Left Zig Zag Traffic', 'Narrow Bridge', 'No Entry', 'No_Over_Taking', 'Object Hazard Right', 'Overtaking by trucks is prohibited', 'Pedestrain Crossing', 'Pedestrian Crossing', 'Right Hand Curv', 'Round-About', 'STOP Sign', 'School Ahead', 'Side Road Right', 'Single Chevron', 'Slippery Road Ahead', 'Speed Limit 20 KMPh', 'Speed Limit 30 KMPh', 'Stack type Advance Direction sign', 'State Highway Route Marker', 'Stop_Sign', 'Straight Ahead Only', 'Toilet', 'Tractor Prohibited', 'Traffic sign Not visibles', 'Traffic_signal', 'Truck traffic is prohibited', 'Turn left ahead', 'Turn right ahead', 'Two Wheeler Prohibited', 'Uneven Road', 'other', 'speed limit', 'speed limit 20', 'speed limit 80']
"""
    with open(YAML_PATH, "w") as f:
        f.write(yaml_content)
    print(f"Created absolute dataset configuration at {YAML_PATH}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    create_abs_yaml()

    config = {
        "dataset_used": "Infrastructure/indian traffic sign dataset",
        "train_image_count": 7255,
        "valid_image_count": 1904,
        "test_image_count": 1033,
        "class_count": 57,
        "epochs": 25,
        "imgsz": 416,
        "batch": 16,
        "device": "mps",
        "workers": 2,
        "cache": False,
        "optimizer": "auto (AdamW)",
        "base_model": "models/yolov8n.pt",
        "dataset_yaml": YAML_PATH
    }

    print("\n================ PHASE 9 FINAL 25-EPOCH TRAINING CONFIGURATION ================")
    for k, v in config.items():
        print(f"  {k}: {v}")
    print("=================================================================================\n")

    print("Loading base YOLOv8 model for transfer learning...")
    base_model_path = os.path.join(PROJECT_ROOT, "models/yolov8n.pt")
    model = YOLO(base_model_path)

    print(f"Starting 25-epoch training run on {YAML_PATH} using Apple Silicon MPS...")
    results = model.train(
        data=YAML_PATH,
        epochs=config["epochs"],
        imgsz=config["imgsz"],
        batch=config["batch"],
        device=config["device"],
        project=os.path.join(PROJECT_ROOT, "runs/infrastructure"),
        name="train_run_25e",
        exist_ok=True,
        workers=config["workers"],
        cache=config["cache"]
    )

    # Save trained weights to models/infrastructure/infrastructure_detector.pt if better
    best_weights = os.path.join(PROJECT_ROOT, "runs/infrastructure/train_run_25e/weights/best.pt")
    if os.path.exists(best_weights):
        # Record pre-existing model SHA256 if present
        if os.path.exists(FINAL_MODEL_PATH):
            prev_sha = hashlib.sha256(open(FINAL_MODEL_PATH, "rb").read()).hexdigest()
            print(f"\nPrevious 6-Epoch Model SHA256: {prev_sha}")

        shutil.copy(best_weights, FINAL_MODEL_PATH)
        print(f"Successfully saved 25-epoch final model to {FINAL_MODEL_PATH}")
    else:
        print("Error: best.pt weights not found!")
        sys.exit(1)

    # Evaluate on untouched test split
    print("\nEvaluating 25-epoch trained model on held-out 1,033-image test split...")
    test_model = YOLO(FINAL_MODEL_PATH)
    metrics = test_model.val(data=YAML_PATH, split="test")

    print("\n================ FINAL 25-EPOCH EVALUATION METRICS ================")
    print(f"Precision: {metrics.results_dict.get('metrics/precision(B)', 0):.4f}")
    print(f"Recall: {metrics.results_dict.get('metrics/recall(B)', 0):.4f}")
    print(f"mAP50: {metrics.results_dict.get('metrics/mAP50(B)', 0):.4f}")
    print(f"mAP50-95: {metrics.results_dict.get('metrics/mAP50-95(B)', 0):.4f}")

    # Compute SHA256 of final model
    sha256_hash = hashlib.sha256()
    with open(FINAL_MODEL_PATH, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    checksum = sha256_hash.hexdigest()
    print(f"\nFinal Infrastructure Model SHA256 Checksum: {checksum}")

if __name__ == "__main__":
    main()

