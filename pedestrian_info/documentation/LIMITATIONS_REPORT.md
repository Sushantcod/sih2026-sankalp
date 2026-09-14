# ⚠️ Phase 8 Limitations & Zero Fabrication Policy

> **Policy Directive**: SIH 2026 Strict Zero-Fabrication Directive  
> **Subsystem**: Phase 8 Pedestrian & Crosswalk Safety Analytics

---

## 1. Zero-Fabrication Directive Alignment

The SIH 2026 platform enforces a strict policy against synthetic telemetry, artificial risk metrics, and fake GIS locations. All system capabilities reported must be grounded in verified dataset ground truth.

---

## 2. Capability Status Summary

| Feature / Capability | Implementation Status | Technical Rationale |
| :--- | :---: | :--- |
| **Pedestrian Object Detection** | ✅ **SUPPORTED** | Trained on 7,737 images in `smart-crossing-version-1` (**81.78% mAP50**). |
| **Crosswalk Detection** | ✅ **SUPPORTED** | Dedicated `crossing` class trained on 7,737 images (**94.40% mAP50**). |
| **Vehicle Detection** | ✅ **SUPPORTED** | Simultaneous `vehicle` class trained on 7,737 images (**80.30% mAP50**). |
| **School-Zone Context** | ⚠️ **UNAVAILABLE** | No school boundary GIS datasets or metadata available in project. |
| **Pedestrian Risk Assessment** | ⚠️ **UNAVAILABLE** | No ground truth collision risk labels present in dataset. |
| **Collision / Near-Miss Prediction** | ⚠️ **UNAVAILABLE** | Requires continuous 3D spatial velocity vector sensors. |
| **GPS Sensor Telemetry** | ⚠️ **UNAVAILABLE** | Dashcam footage recorded without attached NMEA GPS sensor (`GPS: null`). |

---

## 3. Mandatory Operator Guidance

If a capability is marked `UNAVAILABLE`, the API and Dashboard UI explicitly display:

`School-Zone Context Unavailable — location metadata missing`  
`Pedestrian Risk Assessment — Insufficient ground truth risk labels`  
`GPS Telemetry Unavailable`
