# Phase 5 GIS Subsystem & Mapping Integration Report

**Mapping Framework**: Leaflet 1.9.4  
**Tile Layer Provider**: OpenStreetMap CartoDB Dark Matter (`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`)  
**Strict Zero Fabrication Constraint**: Enforced  

---

## 1. GIS Engine Architecture & Configuration

The Leaflet map engine is initialized inside `#map` with an interactive Dark Matter cartographic theme.

```javascript
state.map = L.map('map', {
    zoomControl: true,
    attributionControl: false
}).setView([19.0760, 72.8777], 11);
```

---

## 2. Marker Plotting Rules & GPS Filtering

Before any marker is passed to Leaflet, the event is strictly validated for genuine numeric coordinates:

```javascript
const mappedEvents = events.filter(e => e.latitude !== null && e.longitude !== null);
```

### Un-Geolocated Event Handling Rules:
1. Events with `latitude === null` or `longitude === null` are **STRICTLY EXCLUDED** from map marker creation.
2. Un-geolocated events are **NEVER** placed at a default city center or random coordinate.
3. The dashboard UI renders an explicit, high-visibility status banner across the map container:
   > ⚠️ **GPS Telemetry Unavailable** — **7,964** events in database contain `latitude: null, longitude: null` and cannot be plotted on map.

---

## 3. Dynamic Map Popup Specifications

When genuine geographic events are present in future live NMEA hardware runs, Leaflet markers display popups containing:
- **Event Category**: e.g. `POTHOLE`, `PLATE_DETECTED`
- **Source Identifier**: e.g. `BUS-101`
- **Confidence Score**: e.g. `94.2%`
- **Payload Inspection Button**: Triggers verbatim JSON payload modal rendering.
