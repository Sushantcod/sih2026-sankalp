# Phase 5 System Limitations & Operational Upgrade Pathway

**System**: Phase 5 GIS Dashboard & Real-Data Heatmap Subsystem  
**Date**: 2026-09-14  

---

## 1. Identified System Limitations & Root Cause Analysis

1. **GPS Hardware Telemetry Gap**:
   - *Observation*: All 7,964 stored event records contain `latitude: null, longitude: null`.
   - *Root Cause*: Input video streams (`data/sample_videos/`) were recorded without active NMEA GPS sensors attached to the edge camera hardware rig.
   - *System Response*: The dashboard honestly reports `"GPS Telemetry Unavailable — 7,964 events in database contain null GPS"` and disables heatmap rendering instead of fabricating fake points.
   - *Upgrade Pathway*: In live deployment, connecting a USB or serial NMEA GPS receiver (e.g. u-blox NEO-6M) to the edge inference pipeline will output numeric float coordinates. The Phase 4 API and Phase 5 Dashboard will immediately plot map markers and render heatmaps without any code changes.

2. **Browser Memory & Large Page Limits**:
   - *Observation*: Data table page size is currently capped at 250 records per page.
   - *Root Cause*: Rendering tens of thousands of DOM rows simultaneously degrades browser scrolling performance.
   - *Upgrade Pathway*: Implement virtual scrolling (`Clusterize.js` or React Window) in Phase 6 for large datasets.

3. **HTTP Polling vs WebSocket Streaming**:
   - *Observation*: Real-time updates rely on manual refresh clicks or periodic HTTP polling.
   - *Upgrade Pathway*: Implement WebSocket streaming endpoints (`ws://127.0.0.1:8000/ws/events`) in Phase 6 for sub-second event push notifications.

---

## 2. Classification Summary

As explicitly defined in Section 21 of the SIH 2026 Master Plan instructions:
> *"If GPS data is unavailable but the dashboard itself is correctly implemented and honestly reports the limitation, use: B — PHASE 5 SUCCESSFUL WITH LIMITATIONS."*

Phase 5 is officially classified under **STATUS B — PHASE 5 SUCCESSFUL WITH LIMITATIONS**.
