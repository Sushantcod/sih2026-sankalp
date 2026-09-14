import os
import zipfile
import shutil
import glob

def setup_anpr_folder():
    print("=== SETTING UP ANPR_INFO/ANPR DATASET FOLDER (MATCHING POTHOLES_INFO) ===", flush=True)

    anpr_info_dir = "anpr_info"
    anpr_dataset_dir = os.path.join(anpr_info_dir, "anpr")
    
    os.makedirs(anpr_dataset_dir, exist_ok=True)

    # Zip path
    zip_path = os.path.expanduser("~/Downloads/License Plate Recognition.v13i.yolov8.zip")
    
    if os.path.exists(zip_path):
        print(f"Extracting detection dataset from {zip_path} into {anpr_dataset_dir}...", flush=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(anpr_dataset_dir)
        print("Detection dataset extracted successfully.", flush=True)
    else:
        print(f"WARNING: Zip file not found at {zip_path}", flush=True)

    # OCR dataset setup inside anpr_info/anpr/ocr
    ocr_target_dir = os.path.join(anpr_dataset_dir, "ocr")
    os.makedirs(ocr_target_dir, exist_ok=True)
    
    ocr_source_imgs = os.path.join(anpr_info_dir, "anpr_proof_samples", "ocr")
    if os.path.exists(ocr_source_imgs):
        shutil.copytree(ocr_source_imgs, os.path.join(ocr_target_dir, "samples"), dirs_exist_ok=True)
        print(f"OCR proof dataset prepared in {ocr_target_dir}", flush=True)

    print("\nVerifying directory contents of anpr_info/anpr/...")
    for item in sorted(os.listdir(anpr_dataset_dir)):
        item_p = os.path.join(anpr_dataset_dir, item)
        if os.path.isdir(item_p):
            sub_count = len(os.listdir(item_p))
            print(f"  📁 {item}/ ({sub_count} items)")
        else:
            size_kb = os.path.getsize(item_p) / 1024
            print(f"  📄 {item} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    setup_anpr_folder()
