from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, List, Dict, Any
from src.backend.database import get_db_connection
from src.backend.schemas import (
    EventIngestPayload,
    EventBatchIngestRequest,
    EventResponse,
    IngestionResult,
    BatchIngestionResult,
    DatabaseStatsResponse,
    SUPPORTED_EVENT_TYPES,
    IncidentCreate,
    IncidentUpdate,
    IncidentNoteCreate,
    IncidentNoteResponse,
    IncidentHistoryResponse,
    IncidentResponse,
    IncidentStatsSummary
)
from src.backend.models import (
    insert_single_event,
    query_events,
    get_event_by_id,
    get_database_stats,
    create_incident,
    query_incidents,
    get_incident_by_id,
    update_incident,
    add_incident_note,
    get_incident_stats
)

router = APIRouter()

@router.get("/", summary="Backend Status Info")
def root_info():
    return {
        "service": "SIH 2026 Phase 4 Central Backend Ingestion API",
        "status": "online",
        "framework": "FastAPI",
        "database": "SQLite (data/events.db)",
        "supported_event_types": sorted(list(SUPPORTED_EVENT_TYPES))
    }

@router.get("/health", summary="Health Check")
def health_check():
    try:
        conn = get_db_connection()
        conn.execute("SELECT 1")
        conn.close()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

@router.post("/events", response_model=IngestionResult, summary="Ingest Single Event")
def ingest_event(payload: EventIngestPayload):
    raw_dict = payload.model_dump()
    # Merge payload dict if extra keys were passed in payload
    if "payload" in raw_dict and isinstance(raw_dict["payload"], dict):
        base_payload = raw_dict.pop("payload")
        for k, v in base_payload.items():
            if k not in raw_dict:
                raw_dict[k] = v

    conn = get_db_connection()
    try:
        is_duplicate, event_id, message = insert_single_event(conn, raw_dict)
        return IngestionResult(
            status="duplicate" if is_duplicate else "ingested",
            event_id=event_id,
            is_duplicate=is_duplicate,
            message=message
        )
    finally:
        conn.close()

@router.post("/events/batch", response_model=BatchIngestionResult, summary="Ingest Batch Events")
def ingest_batch_events(request: EventBatchIngestRequest):
    conn = get_db_connection()
    ingested_count = 0
    duplicate_count = 0
    failed_count = 0
    details = []

    try:
        for item in request.events:
            if not isinstance(item, dict):
                failed_count += 1
                details.append(IngestionResult(status="failed", event_id="unknown", is_duplicate=False, message="Item is not a valid dictionary"))
                continue
            
            # Validate event_type
            e_type = str(item.get("event_type", "")).lower().strip()
            if e_type not in SUPPORTED_EVENT_TYPES:
                failed_count += 1
                details.append(IngestionResult(status="failed", event_id=item.get("event_id", "unknown"), is_duplicate=False, message=f"Unsupported event_type '{e_type}'"))
                continue

            is_duplicate, event_id, message = insert_single_event(conn, item)
            if is_duplicate:
                duplicate_count += 1
                details.append(IngestionResult(status="duplicate", event_id=event_id, is_duplicate=True, message=message))
            else:
                ingested_count += 1
                details.append(IngestionResult(status="ingested", event_id=event_id, is_duplicate=False, message=message))
    finally:
        conn.close()

    return BatchIngestionResult(
        total_received=len(request.events),
        ingested_count=ingested_count,
        duplicate_count=duplicate_count,
        failed_count=failed_count,
        details=details
    )

@router.get("/events", response_model=List[EventResponse], summary="Retrieve Events")
def get_events(
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    source: Optional[str] = Query(None, description="Filter by event source / bus_id"),
    start_time: Optional[str] = Query(None, description="Filter by start ISO timestamp"),
    end_time: Optional[str] = Query(None, description="Filter by end ISO timestamp"),
    limit: int = Query(100, ge=1, le=1000, description="Page size limit"),
    offset: int = Query(0, ge=0, description="Page offset")
):
    return query_events(
        event_type=event_type,
        source=source,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
        offset=offset
    )

@router.get("/events/{event_id}", response_model=EventResponse, summary="Get Event By ID")
def get_single_event(event_id: str = Path(..., description="Unique Event ID")):
    event = get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail=f"Event '{event_id}' not found")
    return event

@router.get("/stats", response_model=DatabaseStatsResponse, summary="Get Database Statistics")
def get_stats():
    return get_database_stats()

# Incident Endpoints

@router.post("/incidents", response_model=IncidentResponse, status_code=201, summary="Create Incident From Real Event")
def post_create_incident(payload: IncidentCreate):
    result, message = create_incident(
        event_id=payload.event_id,
        title=payload.title,
        description=payload.description,
        severity=payload.severity,
        operator=payload.operator,
        initial_note=payload.initial_note
    )
    if not result:
        if "does not exist" in message:
            raise HTTPException(status_code=404, detail=message)
        raise HTTPException(status_code=400, detail=message)
    return result

@router.get("/incidents", response_model=List[IncidentResponse], summary="Query Incidents")
def get_all_incidents(
    status: Optional[str] = Query(None, description="Filter by status (OPEN, ACKNOWLEDGED, IN_PROGRESS, RESOLVED, CLOSED)"),
    severity: Optional[str] = Query(None, description="Filter by severity (LOW, MEDIUM, HIGH, CRITICAL)"),
    event_type: Optional[str] = Query(None, description="Filter by linked event type"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    return query_incidents(status=status, severity=severity, event_type=event_type, limit=limit, offset=offset)

@router.get("/incidents/stats/summary", response_model=IncidentStatsSummary, summary="Get Incident Statistics Summary")
def get_incidents_stats_summary():
    return get_incident_stats()

@router.get("/incidents/{incident_id}", response_model=IncidentResponse, summary="Get Incident By ID")
def get_single_incident(incident_id: str = Path(..., description="Incident ID")):
    inc = get_incident_by_id(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found")
    return inc

@router.patch("/incidents/{incident_id}", response_model=IncidentResponse, summary="Update Incident Status / Severity / Operator")
def patch_update_incident(payload: IncidentUpdate, incident_id: str = Path(..., description="Incident ID")):
    result, message = update_incident(
        incident_id=incident_id,
        status=payload.status,
        severity=payload.severity,
        operator=payload.operator,
        note=payload.note
    )
    if not result:
        if "not found" in message:
            raise HTTPException(status_code=404, detail=message)
        raise HTTPException(status_code=400, detail=message)
    return result

@router.post("/incidents/{incident_id}/notes", response_model=IncidentNoteResponse, status_code=201, summary="Add Operator Note To Incident")
def post_incident_note(payload: IncidentNoteCreate, incident_id: str = Path(..., description="Incident ID")):
    note_obj, message = add_incident_note(
        incident_id=incident_id,
        note_text=payload.note_text,
        operator=payload.operator
    )
    if not note_obj:
        raise HTTPException(status_code=404, detail=message)
    return note_obj

@router.get("/incidents/{incident_id}/history", response_model=List[IncidentHistoryResponse], summary="Get Incident Audit History")
def get_single_incident_history(incident_id: str = Path(..., description="Incident ID")):
    inc = get_incident_by_id(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found")
    return inc["history"]

