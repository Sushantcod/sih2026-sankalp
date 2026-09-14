import os
import sys
import shutil
import hashlib
from ultralytics import YOLO

# Project root path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATASET_DIR = os.path.join(PROJECT_ROOT, "pedestrian_info/pedestrian")
YAML_PATH = os.path.join(DATASET_DIR, "data_abs.yaml")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "models/pedestrian")
FINAL_MODEL_PATH = os.path.join(OUTPUT_DIR, "pedestrian_detector.pt")

def create_abs_yaml():
    yaml_content = f"""path: "{DATASET_DIR}"
train: train/images
val: valid/images
test: test/images

nc: 3
names: ['crossing', 'pedestrian', 'vehicle']
"""
    with open(YAML_PATH, "w") as f:
        f.write(yaml_content)
    print(f"Created absolute dataset configuration at {YAML_PATH}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    create_abs_yaml()

    # Exact pre-training configuration logging
    config = {
        "epochs": 8,
        "imgsz": 416,
        "batch": 64,
        "device": "mps",
        "workers": 2,
        "optimizer": "auto (AdamW)",
        "base_model": "models/yolov8n.pt",
        "dataset_yaml": YAML_PATH,
        "train_images": 5415,
        "valid_images": 1547,
        "test_images": 775,
        "classes": ["crossing", "pedestrian", "vehicle"]
    }

    print("\n================ FINAL TRAINING CONFIGURATION ================")
    for k, v in config.items():
        print(f"  {k}: {v}")
    print("==============================================================\n")

    print("Loading base YOLOv8 model for transfer learning...")
    base_model_path = os.path.join(PROJECT_ROOT, "models/yolov8n.pt")
    model = YOLO(base_model_path)

    print(f"Starting 8-epoch final training run on {YAML_PATH} using Apple Silicon MPS...")
    results = model.train(
        data=YAML_PATH,
        epochs=config["epochs"],
        imgsz=config["imgsz"],
        batch=config["batch"],
        device=config["device"],
        project=os.path.join(PROJECT_ROOT, "runs/pedestrian"),
        name="final_train_run",
        exist_ok=True,
        workers=config["workers"]
    )

    # Save trained weights to models/pedestrian/pedestrian_detector.pt
    best_weights = os.path.join(PROJECT_ROOT, "runs/pedestrian/final_train_run/weights/best.pt")
    if os.path.exists(best_weights):
        shutil.copy(best_weights, FINAL_MODEL_PATH)
        print(f"\nSuccessfully saved final model to {FINAL_MODEL_PATH}")
    else:
        print("Error: best.pt weights not found!")
        sys.exit(1)

    # Evaluate on untouched test split
    print("\nEvaluating trained final model on test split...")
    test_model = YOLO(FINAL_MODEL_PATH)
    metrics = test_model.val(data=YAML_PATH, split="test")

    print("\n================ FINAL EVALUATION METRICS ================")
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
    print(f"\nFinal Model SHA256 Checksum: {checksum}")

if __name__ == "__main__":
    main()
