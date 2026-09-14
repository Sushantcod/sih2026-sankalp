import json
import hashlib
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator

SUPPORTED_EVENT_TYPES = {
    # Phase 1 Road Damage
    "pothole",
    "longitudinal_crack",
    "transverse_crack",
    "alligator_crack",
    "manhole",
    "waterlogging",
    # Phase 2 Vehicle Density
    "vehicle_count",
    "congestion",
    # Phase 3 ANPR
    "plate_detected",
    "anpr",
    # Phase 8 Pedestrian Safety
    "pedestrian_detected",
    "crossing_detected",
    # Phase 9 Infrastructure
    "traffic_sign_detected"
}

class EventIngestPayload(BaseModel):
    """Payload model for ingestion request."""
    event_id: Optional[str] = None
    event_type: str
    source: Optional[str] = None
    timestamp: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    confidence: Optional[float] = None
    payload: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("event_type")
    def validate_event_type(cls, v: str) -> str:
        clean_v = str(v).lower().strip()
        if clean_v not in SUPPORTED_EVENT_TYPES:
            raise ValueError(f"Unsupported event_type '{v}'. Supported types: {sorted(list(SUPPORTED_EVENT_TYPES))}")
        return clean_v

class EventBatchIngestRequest(BaseModel):
    events: List[Dict[str, Any]]

class EventResponse(BaseModel):
    event_id: str
    event_type: str
    source: Optional[str] = None
    timestamp: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    confidence: Optional[float] = None
    payload: Dict[str, Any]
    created_at: str

class EventQueryFilter(BaseModel):
    event_type: Optional[str] = None
    source: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)

class IngestionResult(BaseModel):
    status: str
    event_id: str
    is_duplicate: bool = False
    message: str

class BatchIngestionResult(BaseModel):
    total_received: int
    ingested_count: int
    duplicate_count: int
    failed_count: int
    details: List[IngestionResult] = Field(default_factory=list)

class DatabaseStatsResponse(BaseModel):
    total_events: int
    count_by_type: Dict[str, int]
    count_by_source: Dict[str, int]
    earliest_timestamp: Optional[str] = None
    latest_timestamp: Optional[str] = None

# Incident Schemas

VALID_STATUSES = {"OPEN", "ACKNOWLEDGED", "IN_PROGRESS", "RESOLVED", "CLOSED"}
VALID_SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

class IncidentCreate(BaseModel):
    event_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = "MEDIUM"
    operator: Optional[str] = None
    initial_note: Optional[str] = None

class IncidentUpdate(BaseModel):
    status: Optional[str] = None
    severity: Optional[str] = None
    operator: Optional[str] = None
    note: Optional[str] = None

class IncidentNoteCreate(BaseModel):
    note_text: str
    operator: Optional[str] = None

class IncidentNoteResponse(BaseModel):
    note_id: str
    incident_id: str
    operator: Optional[str] = None
    note_text: str
    created_at: str

class IncidentHistoryResponse(BaseModel):
    history_id: str
    incident_id: str
    action: str
    old_status: Optional[str] = None
    new_status: Optional[str] = None
    operator: Optional[str] = None
    details: Optional[str] = None
    created_at: str

class IncidentResponse(BaseModel):
    incident_id: str
    event_id: str
    status: str
    severity: str
    title: str
    description: Optional[str] = None
    operator: Optional[str] = None
    created_at: str
    updated_at: str
    resolved_at: Optional[str] = None
    event: Optional[EventResponse] = None
    notes: List[IncidentNoteResponse] = Field(default_factory=list)
    history: List[IncidentHistoryResponse] = Field(default_factory=list)

class IncidentStatsSummary(BaseModel):
    total_incidents: int
    count_by_status: Dict[str, int]
    count_by_severity: Dict[str, int]
    count_by_event_type: Dict[str, int]

