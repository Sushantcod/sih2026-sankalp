import os
import shutil
import glob

def combine_anpr():
    print("=== COMBINING ANPR_INFO AND ANPR INTO A SINGLE 'anpr/' FOLDER ===", flush=True)

    anpr_dir = "anpr"
    anpr_info_dir = "anpr_info"

    os.makedirs(anpr_dir, exist_ok=True)
    
    # 1. Dataset subfolder inside anpr (anpr/anpr matching potholes_info/potholes)
    target_dataset_dir = os.path.join(anpr_dir, "anpr")
    source_dataset_dir = os.path.join(anpr_info_dir, "anpr")

    if os.path.exists(source_dataset_dir):
        if os.path.exists(target_dataset_dir):
            shutil.rmtree(target_dataset_dir)
        shutil.move(source_dataset_dir, target_dataset_dir)
        print(f"Moved dataset to {target_dataset_dir}", flush=True)

    # 2. Documentation folder inside anpr/documentation
    doc_target_dir = os.path.join(anpr_dir, "documentation")
    os.makedirs(doc_target_dir, exist_ok=True)

    # Move markdown files from anpr_info into anpr/documentation and anpr/
    for doc_p in glob.glob(os.path.join(anpr_info_dir, "*.md")):
        fname = os.path.basename(doc_p)
        shutil.copy(doc_p, doc_target_dir)

    # 3. Runs and Outputs
    source_runs = os.path.join(anpr_info_dir, "runs")
    target_runs = os.path.join(anpr_dir, "runs")
    if os.path.exists(source_runs):
        if os.path.exists(target_runs):
            shutil.rmtree(target_runs)
        shutil.move(source_runs, target_runs)

    source_outputs = os.path.join(anpr_info_dir, "outputs")
    target_outputs = os.path.join(anpr_dir, "outputs")
    if os.path.exists(source_outputs):
        if os.path.exists(target_outputs):
            shutil.rmtree(target_outputs)
        shutil.move(source_outputs, target_outputs)

    # 4. Remove anpr_info folder completely
    if os.path.exists(anpr_info_dir):
        shutil.rmtree(anpr_info_dir)
        print(f"Removed temporary {anpr_info_dir} folder.", flush=True)

    print("\n--- FINAL SINGLE 'anpr/' FOLDER INVENTORY ---")
    for root, dirs, files in os.walk(anpr_dir):
        rel = os.path.relpath(root, anpr_dir)
        if rel == ".":
            print(f"📁 {anpr_dir}/")
        else:
            depth = rel.count(os.sep)
            if depth <= 2:
                indent = "  " * (depth + 1)
                print(f"{indent}📁 {os.path.basename(root)}/ ({len(files)} files)")

if __name__ == "__main__":
    combine_anpr()
