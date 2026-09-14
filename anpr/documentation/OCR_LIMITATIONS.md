# ANPR OCR Limitations & Architectural Recommendations

**Document Timestamp**: 2026-09-13T23:38:00Z  
**Target Component**: ANPR OCR Subsystem  

---

## 1. Systemic Limitations of Off-The-Shelf EasyOCR

Empirical benchmarking across 1,651 real ground-truth Indian number plate images and 1,800 real video stream frames identified critical limitations in relying solely on off-the-shelf EasyOCR without domain-specific adaptation:

1. **Low Exact Plate-Match Accuracy (7.51%)**:
   - Out-of-the-box EasyOCR achieves only 7.51% exact match accuracy on Indian license plates.
   - High Character Error Rate (CER = 79.86%) causes ~92.5% of raw reads to contain at least one misread character.

2. **Systemic Character Ambiguities**:
   - Digit `0` vs Letter `O` (467 occurrences).
   - Digit `1` vs Letter `I` (128 occurrences).
   - Digit `2` vs Letter `Z` (108 occurrences).
   - Glyph `A` vs Digit `4` (70 occurrences).

3. **Sensitivity to Multi-Line Plate Layouts**:
   - Standard EasyOCR struggles with stacked Indian registration layouts (e.g. State prefix on top line, registration number on bottom line), frequently reading characters out of sequence or ignoring the lower line.

4. **Background Noise & Frame Artifacts**:
   - Border rivets, state emblems, and `IND` holographic badges trigger false character insertions (`<INS>`), adding 200+ extra garbage characters per 1,000 crops.

---

## 2. Technical Recommendations

### Is Existing EasyOCR Sufficient?
**NO.** Unmodified EasyOCR is insufficient for production automatic number plate recognition due to the low 7.51% exact accuracy.

### Is Preprocessing Needed?
**YES.** Image preprocessing techniques would provide immediate improvements:
- **Perspective Warping / Alignment**: Rectifying skewed or tilted plate crops to a flat horizontal aspect ratio.
- **Adaptive Contrast Enhancement**: Applying CLAHE (Contrast Limited Adaptive Histogram Equalization) and Otsu binarization to highlight high-contrast black characters on white/yellow backings.
- **Rule-Based Post-Processing Rules**: Enforcing Indian registration regex syntax (`^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$`) to automatically resolve `0` vs `O` and `1` vs `I` based on character position in the string.

### Is a Dedicated Fine-Tuned OCR Model Justified?
**YES.** A dedicated custom-trained CRNN + CTC (Convolutional Recurrent Neural Network with Connectionist Temporal Classification) or PARSeq model fine-tuned specifically on Indian license plate fonts is highly justified for future phases.

> [!NOTE]
> As per strict project instructions, **no OCR model training was executed** during this phase. Training a custom OCR model remains pending explicit user approval.
