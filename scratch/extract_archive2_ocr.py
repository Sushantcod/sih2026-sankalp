import os
import glob
import cv2
import shutil
import xml.etree.ElementTree as ET

def extract_archive2_ocr():
    archive2_dir = os.path.expanduser("~/Downloads/archive-2")
    output_dir = "anpr/anpr/ocr"
    img_out_dir = os.path.join(output_dir, "images")
    lbl_out_dir = os.path.join(output_dir, "labels")

    os.makedirs(img_out_dir, exist_ok=True)
    os.makedirs(lbl_out_dir, exist_ok=True)

    print(f"Extracting 1,651 real ground-truth OCR samples from {archive2_dir}...", flush=True)

    xml_files = sorted(glob.glob(f"{archive2_dir}/**/*.xml", recursive=True))

    extracted = 0
    for xml_p in xml_files:
        if os.path.basename(xml_p).startswith('.'):
            continue
        try:
            tree = ET.parse(xml_p)
            root = tree.getroot()
            for obj in root.findall('object'):
                name_text = obj.find('name').text if obj.find('name') is not None else ''
                if name_text and name_text.lower() not in ('licence', 'license', 'plate', 'number_plate', 'number plate', 'np'):
                    clean_ocr = ''.join(c for c in name_text if c.isalnum()).upper()
                    if len(clean_ocr) >= 4:
                        base_name = os.path.splitext(os.path.basename(xml_p))[0]
                        img_dir = os.path.dirname(xml_p)
                        cands = [os.path.join(img_dir, base_name + ext) for ext in ('.jpeg', '.jpg', '.png')]
                        img_p = None
                        for c in cands:
                            if os.path.exists(c):
                                img_p = c
                                break
                        if img_p and os.path.exists(img_p):
                            # Copy image and label
                            out_base = f"anpr_ocr_{extracted:05d}_{base_name[:12]}"
                            out_img_p = os.path.join(img_out_dir, out_base + os.path.splitext(img_p)[1])
                            out_lbl_p = os.path.join(lbl_out_dir, out_base + ".txt")

                            shutil.copy(img_p, out_img_p)
                            with open(out_lbl_p, "w", encoding="utf-8") as fp:
                                fp.write(clean_ocr)

                            extracted += 1
                            if extracted >= 1651:
                                break
        except Exception:
            pass

        if extracted >= 1651:
            break

    print(f"Successfully extracted {extracted} real ground-truth OCR samples into {output_dir}/")

if __name__ == "__main__":
    extract_archive2_ocr()
