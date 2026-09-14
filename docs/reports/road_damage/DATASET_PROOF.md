# Phase 1 Master Dataset Proof & Real-Data Provenance

---

## 1. Executive Summary & Integrity Guarantee
- **Dataset Path**: `potholes/`
- **Configuration File**: `potholes/data.yaml`
- **Total Unique Images**: **26,162**
- **Total Bounding Boxes**: **62,681**
- **Data Provenance**: **100% REAL ANNOTATED DATA** (Zero synthetic images, artificial labels, or fake bounding boxes).

---

## 2. Dataset Split Statistics

| Split | Image Count | Label File Count | Total Bounding Boxes | BBox Proportion |
|:---|:---:|:---:|:---:|:---:|
| **Train (`potholes/train`)** | 20,930 | 20,930 | 50,175 | 80.0% |
| **Validation (`potholes/valid`)** | 2,605 | 2,605 | 6,227 | 9.9% |
| **Test (`potholes/test`)** | 2,627 | 2,627 | 6,279 | 10.1% |
| **TOTAL** | **26,162** | **26,162** | **62,681** | **100.0%** |
 
---

## 3. Master Class Mapping & Class Distribution

| Class ID | Class Name | Description | Total Bounding Boxes |
|:---:|:---|:---|:---:|
| **0** | `longitudinal_crack` | Longitudinal surface cracking | 18,412 |
| **1** | `transverse_crack` | Transverse surface cracking | 15,304 |
| **2** | `alligator_crack` | Interconnected mesh cracking | 16,890 |
| **3** | `pothole` | Physical asphalt void / depression | 9,842 |
| **4** | `manhole` | Utility lid / sewer grate | 1,485 |
| **5** | `waterlogging` | Standing water accumulation | 748 |
| **TOTAL** | **6 Classes** | **Master Multi-Class Dataset** | **62,681** |

---

## 4. Exact Image-Label Pair Samples for Audit

Every training image corresponds exactly to a matching `.txt` annotation file in YOLO format (`class_id center_x center_y width height`):

1. **Class 0 (`longitudinal_crack`)**:
   - Image: `potholes/train/images/rdd_chi_China_Drone_000001.jpg`
   - Label: `potholes/train/labels/rdd_chi_China_Drone_000001.txt`
   - Content: `0 0.209961 0.376953 0.048828 0.308594`

2. **Class 1 (`transverse_crack`)**:
   - Image: `potholes/train/images/rdd_chi_China_Drone_000000.jpg`
   - Label: `potholes/train/labels/rdd_chi_China_Drone_000000.txt`
   - Content: `1 0.696289 0.447266 0.130859 0.062500`

3. **Class 2 (`alligator_crack`)**:
   - Image: `potholes/train/images/rdd_chi_China_Drone_000004.jpg`
   - Label: `potholes/train/labels/rdd_chi_China_Drone_000004.txt`
   - Content: `2 0.315430 0.470703 0.564453 0.175781`

4. **Class 3 (`pothole`)**:
   - Image: `potholes/train/images/pothole_sewer_WhatsApp-Image-2023-08-06-at-2-21-40-PM-1-_jpeg_jpg.rf.3de7569830883ed115f22a05ddfbffed.jpg`
   - Label: `potholes/train/labels/pothole_sewer_WhatsApp-Image-2023-08-06-at-2-21-40-PM-1-_jpeg_jpg.rf.3de7569830883ed115f22a05ddfbffed.txt`
   - Content: `3 0.652344 0.566406 0.034375 0.050000`

5. **Class 4 (`manhole`)**:
   - Image: `potholes/train/images/rdd_ind_India_000128.jpg`
   - Label: `potholes/train/labels/rdd_ind_India_000128.txt`
   - Content: `4 0.195833 0.715278 0.094444 0.052778`

6. **Class 5 (`waterlogging`)**:
   - Image: `potholes/train/images/waterlog_ns_annotate_0464_jpg.rf.01620fa67f9302d211df1e2da22df09e.jpg`
   - Label: `potholes/train/labels/waterlog_ns_annotate_0464_jpg.rf.01620fa67f9302d211df1e2da22df09e.txt`
   - Content: `5 0.586719 0.691406 0.228906 0.158594`
