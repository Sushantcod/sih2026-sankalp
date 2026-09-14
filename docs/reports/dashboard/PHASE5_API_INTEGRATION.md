# Phase 5 API Integration & Consumption Report

**Backend Target**: Phase 4 FastAPI REST Service (`http://127.0.0.1:8000`)  
**Frontend Consumer**: Phase 5 Dashboard (`src/dashboard/app.js`)  

---

## 1. API Endpoint Consumption Matrix

| API Endpoint | HTTP Method | Dashboard Usage | Frequency / Trigger | Response Data Extracted |
| :--- | :--- | :--- | :--- | :--- |
| `/health` | `GET` | System Status Indicator | On load & manual Refresh click | `status`, `database` |
| `/stats` | `GET` | Summary Cards & Filter Options | On load & manual Refresh click | `total_events`, `count_by_type`, `count_by_source` |
| `/events` | `GET` | Data Table & GIS Map Markers | On load, filter apply, page change | Event records list (`event_id`, `latitude`, `longitude`, etc.) |
| `/events/{id}`| `GET` | Verbatim JSON Payload Modal | On clicking "Details" button | Full raw event object with verbatim `payload` |

---

## 2. Dynamic Metric Calculation Logic

All summary card values are derived 100% dynamically from API response payloads without any hardcoded constants:

1. **Total Ingested Events**:
   - Source: `stats.total_events` (Empirical value: `7,964`)
2. **Road Damage Events**:
   - Source: Sum of `stats.count_by_type` for `pothole` (527), `alligator_crack` (1,747), `longitudinal_crack` (273), `transverse_crack` (135), `manhole` (24), and `waterlogging` (2). (Empirical value: `2,708`)
3. **ANPR License Plate Events**:
   - Source: `stats.count_by_type.plate_detected` (Empirical value: `5,256`)
4. **GPS-Geolocated Events**:
   - Source: Count of events returned by `/events` where `latitude !== null && longitude !== null`. (Empirical value: `0`)
5. **Unmapped Events**:
   - Source: `total_events - mapped_events`. (Empirical value: `7,964`)

---

## 3. Filter Query Parameter Mapping

The dashboard filter form translates UI control states directly into HTTP query parameters for `GET /events`:

```js
let url = `${API_BASE_URL}/events?limit=${state.pageSize}&offset=${offset}`;

if (state.filters.eventType) url += `&event_type=${encodeURIComponent(state.filters.eventType)}`;
if (state.filters.source)    url += `&source=${encodeURIComponent(state.filters.source)}`;
if (state.filters.startTime) url += `&start_time=${encodeURIComponent(state.filters.startTime)}`;
if (state.filters.endTime)   url += `&end_time=${encodeURIComponent(state.filters.endTime)}`;
```
