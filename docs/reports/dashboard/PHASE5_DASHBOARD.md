# Phase 5 Dashboard Specification & User Interface Report

**Dashboard URL**: `http://127.0.0.1:3000/index.html`  
**Theme**: Glassmorphism Dark Mode  
**Typography**: Inter (UI) + JetBrains Mono (Payloads & IDs)  

---

## 1. User Interface Layout & Sections

```
+-----------------------------------------------------------------------------------+
| SIH 2026 Smart Road Monitoring | API Online | DB Connected | Refresh [12:15 PM]   |
+-----------------------------------------------------------------------------------+
| [ Total: 7,964 ] [ Road Damage: 2,708 ] [ ANPR: 5,256 ] [ Mapped: 0 ] [ Unmapped: 7,964 ] |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  GIS MAP CONTAINER (Leaflet Dark Theme)                                          |
|  ⚠️ GPS Telemetry Unavailable — 7,964 events in database contain null GPS...      |
|                                                                                   |
+-----------------------------------------------------------------------------------+
| FILTERS: [Event Type v] [Source v] [Start Time] [End Time] [ Apply ] [ Reset ]    |
+-----------------------------------------------------------------------------------+
| INGESTED TELEMETRY EVENTS TABLE                                                   |
| Event ID         | Type            | Source  | Timestamp          | Location      |
| evt_178927402... | alligator_crack | BUS-101 | 2026-09-13 04:33...| GPS Unavailable|
| evt_7f1a30c88... | plate_detected  | anpr.mp4| N/A                | GPS Unavailable|
+-----------------------------------------------------------------------------------+
| PAGE CONTROL: [< Prev]  Page 1  [Next >]                    Show: [ 100 v ]       |
+-----------------------------------------------------------------------------------+
```

---

## 2. Event Data Table Features

- **Columns**: `Event ID`, `Event Type` (with color-coded category badges), `Source`, `Timestamp`, `GPS Location`, `Confidence`, `Mapping Status`, `Action`.
- **Category Badges**:
  - `badge-damage`: Rose border & fill for road defects (`pothole`, `crack`, `manhole`, `waterlogging`).
  - `badge-anpr`: Sky blue border & fill for license plate recognition (`plate_detected`).
  - `badge-vehicle`: Purple border & fill for traffic analytics (`vehicle_count`, `congestion`).
- **Status Column**:
  - `Unmapped (Null GPS)`: Displayed in muted slate pill when coordinates are null.
  - `Geolocated`: Displayed in bright emerald pill when numeric GPS exists.
- **Action Button**: `Details` button triggers the verbatim JSON payload viewer modal.

---

## 3. Raw Payload Modal Dialog

When clicking `Details`, the dashboard queries `GET /events/{event_id}` and opens a modal dialog displaying:
- Metadata grid: Event ID, Category, Source, Timestamp, GPS Coordinates, Confidence, and Ingestion Timestamp.
- Code block container (`<pre><code id="modal-json-payload">`): Formatted verbatim JSON serialization of 100% of the raw event properties stored in SQLite.
