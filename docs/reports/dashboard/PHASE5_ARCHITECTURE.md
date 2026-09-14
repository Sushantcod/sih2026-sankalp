# Phase 5 System Architecture Report — GIS Dashboard & Real-Data Heatmap

**System**: SIH 2026 Smart Road Damage & Traffic Management Subsystem  
**Component**: Phase 5 GIS Dashboard & Visualization Subsystem  
**Date**: 2026-09-14  

---

## 1. End-to-End System Integration Flow

```
 +-----------------------------------------------------------------------------------+
 |                             EDGE INFRASTRUCTURE / VIDEO LOGS                      |
 |                                                                                   |
 | Phase 1 & 2 Video (`BUS-101`)                     Phase 3 ANPR Video (`anpr.mp4`) |
 +----------------------------------+------------------------------------------------+
                                    |
                                    v REAL DETECTOR & ANPR LOGS
 +-----------------------------------------------------------------------------------+
 |                           PHASE 4 FASTAPI INGESTION ENGINE                        |
 |                                                                                   |
 | Base URL: `http://127.0.0.1:8000`                                                 |
 | Database: `data/events.db` (7,964 Real Telemetry Records)                         |
 +----------------------------------+------------------------------------------------+
                                    | REST API GET Responses (`/health`, `/stats`, `/events`)
                                    v
 +-----------------------------------------------------------------------------------+
 |                   PHASE 5 GIS DASHBOARD FRONTEND (`src/dashboard/`)               |
 |                                                                                   |
 |   +--------------------------+  +--------------------------+  +-----------------+  |
 |   | Glassmorphism UI Layout  |  | Leaflet GIS & Heatmap    |  | Telemetry Data  |  |
 |   | (`index.html`, `styles`) |  | (`app.js` + Leaflet.heat)|  | Table & Filters |  |
 |   +--------------------------+  +--------------------------+  +-----------------+  |
 +----------------------------------+------------------------------------------------+
                                    | HTTP Server Serving Dashboard
                                    v
 +-----------------------------------------------------------------------------------+
 |                           USER BROWSER / SIH PRESENTATION                         |
 |                           `http://127.0.0.1:3000/index.html`                      |
 +-----------------------------------------------------------------------------------+
```

---

## 2. Frontend Subsystem Components

1. **Dashboard UI Frame (`src/dashboard/index.html`)**:
   - Header with SIH 2026 branding, live API status badge, DB connection indicator, manual refresh button, and last refresh timestamp.
   - Summary Metric Cards: Total Events (7,964), Road Damage Events (2,708), ANPR Plate Events (5,256), Mapped Events (0), Unmapped Events (7,964).
   - GIS Map Container (`#map`) with OpenStreetMap dark cartographic layer.
   - GPS Telemetry Warning Banner and Heatmap Overlay.
   - Query Filter Bar (`Event Type`, `Source`, `Start Time`, `End Time`).
   - Telemetry Events Table with paginated pagination controls.
   - Verbatim JSON Event Details Modal Window.

2. **Styling & Glassmorphism Tokens (`src/dashboard/styles.css`)**:
   - Built with modern HSL color tokens (`--bg-primary: #0a0d14`, `--accent-indigo: #6366f1`, etc.).
   - Responsive flexbox and grid layouts.
   - Inter typography for dashboard metrics and JetBrains Mono for event IDs and raw JSON viewer.

3. **Application Logic Controller (`src/dashboard/app.js`)**:
   - Asynchronously queries Phase 4 REST API endpoints (`/health`, `/stats`, `/events`, `/events/{id}`).
   - Dynamically populates dropdown filters from live `/stats` response.
   - Handles map rendering, marker group updates, and honest GPS warning banners.
   - Controls event table pagination and modal view rendering.
