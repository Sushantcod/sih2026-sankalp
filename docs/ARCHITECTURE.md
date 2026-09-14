# SIH 2026 — System Architecture & Technical Flowcharts

This document defines the authoritative system architecture, technical flowcharts, database schemas, and data pipelines for the **SIH 2026 Smart Road Monitoring & Traffic Management Platform**.

---

## 1. Top-Level System Architecture Diagram

```mermaid
graph TD
    subgraph Edge Inference Subsystem
        V1[Dashcam Stream: Road Damage] --> |YOLOv8 6-Class| D1[Road Damage Detector]
        V2[CCTV Stream: Traffic Counting] --> |YOLOv8 COCO + ByteTrack| D2[Vehicle Count & Congestion]
        V3[ANPR Stream: License Plates] --> |YOLOv8 Plate Localizer + EasyOCR| D3[ANPR & OCR Subsystem]
    end

    subgraph Data Ingestion & Central Backend
        D1 --> |JSON Telemetry| API[FastAPI Ingestion Endpoint]
        D2 --> |JSON Telemetry| API
        D3 --> |JSON Telemetry| API
        API --> |Hash Deduplication| DB[(SQLite Database: data/events.db)]
    end

    subgraph Operational Command Center & GIS Frontend
        API --> |REST Query Endpoints| DASH[Glassmorphism GIS Dashboard]
        DASH --> MAP[Leaflet Cartographic GIS & Heatmap]
        DASH --> INC[Incident Management Subsystem]
        DASH --> RPT[CSV / JSON Report Exporters]
    end
```

---

## 2. End-to-End Data Flow

```mermaid
sequenceDiagram
    autonumber
    participant Video as Video Input Stream
    participant Detector as Edge AI Detector
    participant API as FastAPI Backend (/events)
    participant DB as SQLite Event Store
    participant UI as Command Center UI
    participant Incident as Incident Subsystem

    Video->>Detector: Input Frame (1080p/720p @ 25 FPS)
    Detector->>Detector: Execute Model Inference (YOLOv8/ByteTrack)
    Detector->>API: POST /events (JSON Payload)
    API->>DB: Check Deduplication (Primary Key & Content Hash)
    DB-->>API: Insert Record (Created At, Null GPS)
    API-->>Detector: 200 OK (status: ingested)
    UI->>API: GET /events & GET /stats (Polling / Manual Refresh)
    API-->>UI: Stored Event Telemetry & DB Statistics
    UI->>API: POST /incidents (Dispatch Incident from Real Event)
    API->>DB: Insert Incident & Record Audit History
    API-->>UI: 201 Created (Incident Registered)
```

---

## 3. AI Inference Pipeline

```mermaid
graph LR
    subgraph Input Frame Processing
        F[Raw Frame] --> B[Bounding Box Localization]
    end

    subgraph Damage Subsystem
        B -->|Potholes & Cracks| P1[YOLOv8 6-Class Model]
        P1 --> C1[Confidence Filter >= 0.25]
    end

    subgraph Traffic Subsystem
        B -->|Vehicles| P2[YOLOv8 Base + ByteTrack]
        P2 --> C2[10s Rolling Window ID Count]
    end

    subgraph ANPR Subsystem
        B -->|License Plate Crops| P3[YOLOv8 Plate Localizer]
        P3 --> O[EasyOCR Text Recognizer]
        O --> C3[Recognized Text Candidate]
    end

    C1 --> E[Telemetry Event Payload]
    C2 --> E
    C3 --> E
```

---

## 4. Backend Architecture

```mermaid
graph TD
    Client[Dashboard UI / Edge Script] --> Router[FastAPI APIRouter]
    Router --> Middleware[Pydantic Input Validation]
    Middleware --> Models[Data Models & Deduplication Engine]
    Models --> DB_Conn[SQLite Connection Pool]
    DB_Conn --> SQLite[(data/events.db)]
```

---

## 5. Database ER Diagram

```mermaid
erDiagram
    EVENTS ||--o{ INCIDENTS : "links to"
    INCIDENTS ||--o{ INCIDENT_EVENTS : "contains"
    INCIDENTS ||--o{ INCIDENT_NOTES : "has"
    INCIDENTS ||--o{ INCIDENT_HISTORY : "audits"

    EVENTS {
        string event_id PK
        string event_type
        string source
        string timestamp
        float latitude
        float longitude
        float confidence
        string payload_json
        string created_at
    }

    INCIDENTS {
        string incident_id PK
        string event_id FK
        string status
        string severity
        string title
        string description
        string operator
        string created_at
        string updated_at
        string resolved_at
    }

    INCIDENT_NOTES {
        string note_id PK
        string incident_id FK
        string operator
        string note_text
        string created_at
    }

    INCIDENT_HISTORY {
        string history_id PK
        string incident_id FK
        string action
        string old_status
        string new_status
        string operator
        string details
        string created_at
    }
```

---

## 6. Incident Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> OPEN: Created from Real Event ID
    OPEN --> ACKNOWLEDGED: Operator Acknowledges
    OPEN --> RESOLVED: Direct Resolution
    OPEN --> CLOSED: Closed
    ACKNOWLEDGED --> IN_PROGRESS: Unit Dispatched
    ACKNOWLEDGED --> RESOLVED: Issue Resolved
    ACKNOWLEDGED --> CLOSED: Incident Closed
    IN_PROGRESS --> RESOLVED: Repair Completed
    IN_PROGRESS --> CLOSED: Inspection Closed
    RESOLVED --> CLOSED: Final Verification
    RESOLVED --> OPEN: Reopened
    CLOSED --> OPEN: Reopened
```

---

## 7. Dashboard Component Architecture

```mermaid
graph TD
    UI[Index.html Layout] --> Nav[Command Tabs Navigation]
    Nav --> Tab1[Overview View]
    Nav --> Tab2[Road Damage View]
    Nav --> Tab3[Traffic View]
    Nav --> Tab4[ANPR View]
    Nav --> Tab5[Incident Management Form & Directory]
    Nav --> Tab6[Leaflet GIS Cartography]
    Nav --> Tab7[Analytics Metrics]
    Nav --> Tab8[System Health Diagnostics]
    Nav --> Tab9[CSV/JSON Report Exporters]
```

---

## 8. Deployment Architecture

```mermaid
graph TD
    subgraph Edge Nodes
        N1[Bus-101 Camera Node]
        N2[CCTV Intersection Node]
    end

    subgraph Central Host Server
        API_Srv[Uvicorn / FastAPI Service]
        DB_Srv[SQLite WAL Database]
        HTTP_Srv[HTTP Server / NGINX Static Host]
    end

    N1 -->|HTTP POST| API_Srv
    N2 -->|HTTP POST| API_Srv
    API_Srv --> DB_Srv
    HTTP_Srv --> UI_Client[Operator Workstation Browser]
    UI_Client -->|REST Requests| API_Srv
```

---

## 9. SIH Problem-to-Solution Workflow

```mermaid
graph LR
    Prob[SIH Problem: Manual Road Inspection & Congestion] --> Edge[Edge AI Stream Analytics]
    Edge --> Event[Normalized Telemetry Ingestion]
    Event --> Inc[Operator Incident Dispatch]
    Inc --> Dash[Municipal Command Center Visualizer]
    Dash --> Sol[Optimized City Maintenance & Response]
```
