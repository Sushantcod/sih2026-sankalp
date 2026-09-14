# ANPR Dataset Known Limitations & Provenance Boundaries

---

## 1. Domain & Environment Limitations
1. **Lighting & Night Operations**: The majority of images represent daytime and bright illumination conditions. Low-light and headlight-glare nighttime footage represents ~8% of the dataset.
2. **Camera Angles & Distance**: High-angle dashboard/bus camera views are well-represented, but acute side angles (>60 degrees) reduce bounding box IoU precision.
3. **Plate Condition**: Damaged, dirty, or non-standard regional font plates (e.g. Marathi/Hindi script non-HSRP plates) require dedicated OCR lexicon tuning.

---

## 2. Provenance Boundaries
- Zero synthetic data was added.
- Unannotated images (`number_plate/images`, 1,684 images) were excluded from supervised detection training to prevent false negative gradient penalties.