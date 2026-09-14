# ANPR V1 Detector Model Specifications & SHA-256 Checksums

---

## 1. Model Architecture
- **Model Type**: YOLOv8n Object Detector
- **Input Image Size**: $640 	imes 640$ pixels
- **Classes**: `1` (`0: number_plate`)
- **Parameter Count**: ~3.0 Million Parameters

---

## 2. Model Weight Checksum Matrix

| Model Asset | File Path | SHA-256 Checksum | File Size | Status |
|:---|:---|:---|:---:|:---:|
| **Best Trained Checkpoint** | `anpr/runs/anpr_detection_v1/weights/best.pt` | `d9584abdd286828d6ca0e504ace2c765dd7e66851647d8ba4ad03416f53ecf6a` | 5.95 MB | Active Master |
| **Last Checkpoint** | `anpr/runs/anpr_detection_v1/weights/last.pt` | `f03fc8d33234143fc82391e117db08bfd1fa7abd6f91648a8dc6e25c07272dd2` | 5.95 MB | Epoch 25 Final |

> [!NOTE]
> `models/pothole.pt` remains 100% untouched at SHA-256 `947ee609f36878b4224ade120c359658539dcbec609980f689b397db487b877b`.