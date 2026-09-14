import os
import zipfile
import xml.etree.ElementTree as ET

def extract_all_ocr_samples():
    zip_path = os.path.expanduser("~/Downloads/number_plate.zip")
    output_dir = "anpr/anpr/ocr"
    img_out_dir = os.path.join(output_dir, "images")
    lbl_out_dir = os.path.join(output_dir, "labels")

    os.makedirs(img_out_dir, exist_ok=True)
    os.makedirs(lbl_out_dir, exist_ok=True)

    print(f"Extracting full OCR ground-truth dataset from {zip_path}...", flush=True)

    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Build case-insensitive filename map
        name_map = {os.path.basename(n).lower(): n for n in zf.namelist() if n.startswith('images/') and not n.endswith('/')}

        with zf.open('number_plate.xlsx') as excel_f:
            xlsx_zip = zipfile.ZipFile(excel_f)
            shared_strings = [elem.text if elem.text else '' for elem in ET.fromstring(xlsx_zip.read('xl/sharedStrings.xml')).findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')]
            sheet_xml = xlsx_zip.read('xl/worksheets/sheet1.xml')

        sheet_tree = ET.fromstring(sheet_xml)
        ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        rows = sheet_tree.findall('.//ns:row', ns)

        pairs = []
        for r in rows[1:]: # Skip header
            cols = r.findall('ns:c', ns)
            if len(cols) >= 2:
                vals = []
                for c in cols[:2]:
                    v = c.find('ns:v', ns)
                    if v is not None and v.text is not None:
                        t_attr = c.attrib.get('t')
                        if t_attr == 's':
                            idx = int(v.text)
                            vals.append(shared_strings[idx] if idx < len(shared_strings) else '')
                        else:
                            vals.append(v.text)
                    else:
                        vals.append('')
                if len(vals) == 2 and vals[0] and vals[1]:
                    pairs.append((vals[0].strip(), vals[1].strip()))

        print(f"Parsed {len(pairs)} rows from Excel sheet.", flush=True)

        extracted = 0
        for idx, (img_fname, raw_gt) in enumerate(pairs):
            clean_gt = "".join(c for c in raw_gt if c.isalnum()).upper()
            if not clean_gt:
                continue

            lookup_key = os.path.basename(img_fname).lower()
            if lookup_key not in name_map:
                continue

            zip_img_path = name_map[lookup_key]

            try:
                img_bytes = zf.read(zip_img_path)
                out_base = f"anpr_ocr_{idx:05d}_{os.path.splitext(lookup_key)[0]}"
                out_img = os.path.join(img_out_dir, f"{out_base}{os.path.splitext(lookup_key)[1]}")
                out_lbl = os.path.join(lbl_out_dir, f"{out_base}.txt")

                with open(out_img, 'wb') as fp:
                    fp.write(img_bytes)

                with open(out_lbl, 'w', encoding='utf-8') as fp:
                    fp.write(clean_gt)

                extracted += 1
            except Exception as e:
                pass

        print(f"Extraction Complete! Extracted {extracted} ground-truth OCR image/label pairs into {output_dir}/")

if __name__ == "__main__":
    extract_all_ocr_samples()
