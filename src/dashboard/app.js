// SIH 2026 Smart Road Monitoring Dashboard & Incident Command Center JavaScript App
// Strictly consumes real Phase 4 FastAPI backend (http://127.0.0.1:8000)

const API_BASE_URL = 'http://127.0.0.1:8000';

// App State
let state = {
    totalEvents: 0,
    stats: null,
    events: [],
    incidents: [],
    currentPage: 1,
    pageSize: 100,
    activeTab: 'overview',
    filters: {
        eventType: '',
        source: '',
        startTime: '',
        endTime: ''
    },
    incFilters: {
        status: '',
        severity: ''
    },
    viewMode: 'markers', // 'markers' or 'heatmap'
    map: null,
    markersGroup: null,
    heatLayer: null,
    lastRefreshTime: null,
    selectedIncidentId: null
};

// DOM Elements
const el = {
    apiStatus: document.getElementById('api-status'),
    dbStatus: document.getElementById('db-status'),
    btnRefresh: document.getElementById('btn-refresh'),
    lastRefreshTime: document.getElementById('last-refresh-time'),
    
    // Metric Values
    valTotalEvents: document.getElementById('val-total-events'),
    valDamageEvents: document.getElementById('val-damage-events'),
    valAnprEvents: document.getElementById('val-anpr-events'),
    valActiveIncidents: document.getElementById('val-active-incidents'),
    valGpsCoverage: document.getElementById('val-gps-coverage'),

    // Map & Banners
    btnViewMarkers: document.getElementById('btn-view-markers'),
    btnViewHeatmap: document.getElementById('btn-view-heatmap'),
    gpsStatusBanner: document.getElementById('gps-status-banner'),
    gpsBannerText: document.getElementById('gps-banner-text'),
    heatmapOverlay: document.getElementById('heatmap-overlay'),

    // Filters
    filterForm: document.getElementById('filter-form'),
    filterType: document.getElementById('filter-type'),
    filterSource: document.getElementById('filter-source'),
    btnResetFilters: document.getElementById('btn-reset-filters'),

    // Tables & Pagination
    tableBody: document.getElementById('table-body'),
    tableRecordCount: document.getElementById('table-record-count'),
    pageSize: document.getElementById('page-size'),
    btnPrevPage: document.getElementById('btn-prev-page'),
    btnNextPage: document.getElementById('btn-next-page'),
    pageIndicator: document.getElementById('page-indicator'),

    // Incident Elements
    createIncForm: document.getElementById('create-incident-form'),
    incEventId: document.getElementById('inc-event-id'),
    incSeverity: document.getElementById('inc-severity'),
    incTitle: document.getElementById('inc-title'),
    incOperator: document.getElementById('inc-operator'),
    incNote: document.getElementById('inc-note'),
    incidentsTableBody: document.getElementById('incidents-table-body'),
    filterIncStatus: document.getElementById('filter-inc-status'),
    filterIncSeverity: document.getElementById('filter-inc-severity'),

    // Modals
    eventModal: document.getElementById('event-modal'),
    btnCloseModal: document.getElementById('btn-close-modal'),
    modalEventId: document.getElementById('modal-event-id'),
    modalEventType: document.getElementById('modal-event-type'),
    modalSource: document.getElementById('modal-source'),
    modalTimestamp: document.getElementById('modal-timestamp'),
    modalGps: document.getElementById('modal-gps'),
    modalConfidence: document.getElementById('modal-confidence'),
    modalCreatedAt: document.getElementById('modal-created-at'),
    modalJsonPayload: document.getElementById('modal-json-payload'),
    btnCreateIncFromModal: document.getElementById('btn-create-inc-from-modal'),

    incidentModal: document.getElementById('incident-modal'),
    btnCloseIncModal: document.getElementById('btn-close-inc-modal'),
    incModalId: document.getElementById('inc-modal-id'),
    updateIncForm: document.getElementById('update-incident-form'),
    incModalStatus: document.getElementById('inc-modal-status'),
    incModalSeverity: document.getElementById('inc-modal-severity'),
    incModalOperator: document.getElementById('inc-modal-operator'),
    incModalNote: document.getElementById('inc-modal-note'),
    incModalHistory: document.getElementById('inc-modal-history'),

    // Exporters
    btnExportCsv: document.getElementById('btn-export-csv'),
    btnExportJson: document.getElementById('btn-export-json')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initMap();
    setupEventListeners();
    fetchSystemData();
});

// Setup Navigation Tabs
function initTabs() {
    const tabs = document.querySelectorAll('.nav-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });
}

function switchTab(tabId) {
    state.activeTab = tabId;
    document.querySelectorAll('.nav-tab').forEach(t => {
        t.classList.toggle('active', t.getAttribute('data-tab') === tabId);
    });
    document.querySelectorAll('.tab-pane').forEach(p => {
        p.classList.toggle('hidden', p.id !== `tab-${tabId}`);
    });

    if (tabId === 'gis' && state.map) {
        setTimeout(() => state.map.invalidateSize(), 200);
    }
}

// Initialize Leaflet Map
function initMap() {
    const mapEl = document.getElementById('map');
    if (!mapEl) return;
    
    state.map = L.map('map', {
        zoomControl: true,
        attributionControl: false
    }).setView([19.0760, 72.8777], 11);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
        subdomains: 'abcd'
    }).addTo(state.map);

    state.markersGroup = L.layerGroup().addTo(state.map);
}

// Setup Event Listeners
function setupEventListeners() {
    if (el.btnRefresh) el.btnRefresh.addEventListener('click', fetchSystemData);
    
    // View Toggle
    if (el.btnViewMarkers) el.btnViewMarkers.addEventListener('click', () => setViewMode('markers'));
    if (el.btnViewHeatmap) el.btnViewHeatmap.addEventListener('click', () => setViewMode('heatmap'));

    // Filter Form
    if (el.filterForm) {
        el.filterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            state.filters.eventType = el.filterType.value;
            state.filters.source = el.filterSource.value;
            state.currentPage = 1;
            fetchEvents();
        });
    }

    if (el.btnResetFilters) {
        el.btnResetFilters.addEventListener('click', () => {
            if (el.filterForm) el.filterForm.reset();
            state.filters = { eventType: '', source: '', startTime: '', endTime: '' };
            state.currentPage = 1;
            fetchEvents();
        });
    }

    // Incident Creation Form
    if (el.createIncForm) {
        el.createIncForm.addEventListener('submit', handleCreateIncident);
    }

    if (el.filterIncStatus) {
        el.filterIncStatus.addEventListener('change', () => {
            state.incFilters.status = el.filterIncStatus.value;
            fetchIncidents();
        });
    }

    if (el.filterIncSeverity) {
        el.filterIncSeverity.addEventListener('change', () => {
            state.incFilters.severity = el.filterIncSeverity.value;
            fetchIncidents();
        });
    }

    if (el.updateIncForm) {
        el.updateIncForm.addEventListener('submit', handleUpdateIncident);
    }

    // Pagination
    if (el.pageSize) {
        el.pageSize.addEventListener('change', () => {
            state.pageSize = parseInt(el.pageSize.value, 10);
            state.currentPage = 1;
            fetchEvents();
        });
    }

    if (el.btnPrevPage) {
        el.btnPrevPage.addEventListener('click', () => {
            if (state.currentPage > 1) {
                state.currentPage--;
                fetchEvents();
            }
        });
    }

    if (el.btnNextPage) {
        el.btnNextPage.addEventListener('click', () => {
            state.currentPage++;
            fetchEvents();
        });
    }

    // Modals Close
    if (el.btnCloseModal) el.btnCloseModal.addEventListener('click', closeModal);
    if (el.eventModal) {
        el.eventModal.addEventListener('click', (e) => {
            if (e.target === el.eventModal) closeModal();
        });
    }

    if (el.btnCloseIncModal) el.btnCloseIncModal.addEventListener('click', closeIncModal);
    if (el.incidentModal) {
        el.incidentModal.addEventListener('click', (e) => {
            if (e.target === el.incidentModal) closeIncModal();
        });
    }

    if (el.btnCreateIncFromModal) {
        el.btnCreateIncFromModal.addEventListener('click', () => {
            const evId = el.modalEventId.textContent;
            closeModal();
            switchTab('incidents');
            if (el.incEventId) el.incEventId.value = evId;
        });
    }

    // Exporters
    if (el.btnExportCsv) el.btnExportCsv.addEventListener('click', exportEventsCSV);
    if (el.btnExportJson) el.btnExportJson.addEventListener('click', exportEventsJSON);
}

// Main Data Fetch Orchestrator
async function fetchSystemData() {
    updateRefreshTimestamp();
    await checkHealth();
    await fetchStats();
    await fetchEvents();
    await fetchIncidents();
}

function updateRefreshTimestamp() {
    const now = new Date();
    state.lastRefreshTime = now;
    if (el.lastRefreshTime) el.lastRefreshTime.textContent = now.toLocaleTimeString();
}

// Health Check API Call
async function checkHealth() {
    try {
        const resp = await fetch(`${API_BASE_URL}/health`);
        if (resp.ok) {
            const data = await resp.json();
            if (el.apiStatus) el.apiStatus.innerHTML = '<span class="dot green"></span><span class="status-text">API Online</span>';
            if (el.dbStatus) el.dbStatus.innerHTML = '<span class="dot green"></span><span class="status-text">DB Connected</span>';
            const hb = document.getElementById('health-backend-status');
            if (hb) hb.textContent = 'ONLINE (http://127.0.0.1:8000)';
        } else {
            throw new Error(`HTTP ${resp.status}`);
        }
    } catch (err) {
        if (el.apiStatus) el.apiStatus.innerHTML = '<span class="dot red"></span><span class="status-text">API Offline</span>';
        if (el.dbStatus) el.dbStatus.innerHTML = '<span class="dot red"></span><span class="status-text">DB Disconnected</span>';
        const hb = document.getElementById('health-backend-status');
        if (hb) hb.textContent = 'OFFLINE (Connection Refused)';
    }
}

// Database Stats API Call
async function fetchStats() {
    try {
        const resp = await fetch(`${API_BASE_URL}/stats`);
        if (!resp.ok) return;
        
        const stats = await resp.json();
        state.stats = stats;
        state.totalEvents = stats.total_events || 0;

        if (el.valTotalEvents) el.valTotalEvents.textContent = stats.total_events.toLocaleString();
        
        const countByType = stats.count_by_type || {};
        const roadDamageCount = (countByType.pothole || 0) + 
                                (countByType.alligator_crack || 0) + 
                                (countByType.longitudinal_crack || 0) + 
                                (countByType.transverse_crack || 0) + 
                                (countByType.manhole || 0) + 
                                (countByType.waterlogging || 0);
        
        const anprCount = countByType.plate_detected || countByType.anpr || 0;

        if (el.valDamageEvents) el.valDamageEvents.textContent = roadDamageCount.toLocaleString();
        if (el.valAnprEvents) el.valAnprEvents.textContent = anprCount.toLocaleString();

        // Specific breakdown counters
        const setVal = (id, val) => { const e = document.getElementById(id); if (e) e.textContent = (val || 0).toLocaleString(); };
        setVal('val-cnt-alligator', countByType.alligator_crack);
        setVal('val-cnt-pothole', countByType.pothole);
        setVal('val-cnt-longitudinal', countByType.longitudinal_crack);
        setVal('val-cnt-transverse', countByType.transverse_crack);
        setVal('val-cnt-manhole', countByType.manhole);
        setVal('val-cnt-waterlogging', countByType.waterlogging);

        populateFilterDropdowns(stats);
    } catch (err) {
        console.error('Failed to fetch database stats:', err);
    }
}

function populateFilterDropdowns(stats) {
    if (el.filterType && el.filterType.options.length <= 1 && stats.count_by_type) {
        Object.keys(stats.count_by_type).sort().forEach(type => {
            const opt = document.createElement('option');
            opt.value = type;
            opt.textContent = `${type} (${stats.count_by_type[type]})`;
            el.filterType.appendChild(opt);
        });
    }

    if (el.filterSource && el.filterSource.options.length <= 1 && stats.count_by_source) {
        Object.keys(stats.count_by_source).sort().forEach(src => {
            const opt = document.createElement('option');
            opt.value = src;
            opt.textContent = `${src} (${stats.count_by_source[src]})`;
            el.filterSource.appendChild(opt);
        });
    }
}

// Query Events API Call
async function fetchEvents() {
    const offset = (state.currentPage - 1) * state.pageSize;
    let url = `${API_BASE_URL}/events?limit=${state.pageSize}&offset=${offset}`;

    if (state.filters.eventType) url += `&event_type=${encodeURIComponent(state.filters.eventType)}`;
    if (state.filters.source) url += `&source=${encodeURIComponent(state.filters.source)}`;

    try {
        const resp = await fetch(url);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        
        const events = await resp.json();
        state.events = events;

        renderEventsTable(events);
        updateMapAndGPSStatus(events);
        updatePaginationControls(events.length);
    } catch (err) {
        if (el.tableBody) el.tableBody.innerHTML = `<tr><td colspan="8" class="text-center text-alert">Failed to fetch events: ${err.message}</td></tr>`;
    }
}

// Render Events Table
function renderEventsTable(events) {
    if (!el.tableBody) return;
    if (events.length === 0) {
        el.tableBody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">0 events match the selected filters</td></tr>';
        if (el.tableRecordCount) el.tableRecordCount.textContent = 'Showing 0 of 0 events';
        return;
    }

    if (el.tableRecordCount) el.tableRecordCount.textContent = `Showing ${events.length} records (Page ${state.currentPage})`;
    
    let html = '';
    events.forEach(evt => {
        const hasGps = evt.latitude !== null && evt.longitude !== null;
        const gpsStr = hasGps ? `${evt.latitude.toFixed(4)}, ${evt.longitude.toFixed(4)}` : 'GPS Unavailable';
        const confStr = evt.confidence !== null ? `${(evt.confidence * 100).toFixed(1)}%` : 'N/A';
        const tsStr = evt.timestamp ? new Date(evt.timestamp).toLocaleString() : 'N/A';

        let badgeClass = 'badge-damage';
        if (evt.event_type.includes('plate') || evt.event_type === 'anpr') badgeClass = 'badge-anpr';
        else if (evt.event_type.includes('vehicle') || evt.event_type === 'congestion') badgeClass = 'badge-vehicle';

        html += `
            <tr>
                <td class="font-mono">${evt.event_id.slice(0, 16)}...</td>
                <td><span class="badge ${badgeClass}">${evt.event_type}</span></td>
                <td>${evt.source}</td>
                <td>${tsStr}</td>
                <td>${gpsStr}</td>
                <td>${confStr}</td>
                <td>
                    <span class="status-badge ${hasGps ? 'mapped' : 'unmapped'}">
                        ${hasGps ? 'Geolocated' : 'Unmapped (Null GPS)'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-tertiary btn-sm" onclick="openEventModal('${evt.event_id}')">Details</button>
                </td>
            </tr>
        `;
    });

    el.tableBody.innerHTML = html;
}

// Map Rendering & Honest GPS Status Updates
function updateMapAndGPSStatus(events) {
    const mappedEvents = events.filter(e => e.latitude !== null && e.longitude !== null);

    if (el.valGpsCoverage) el.valGpsCoverage.textContent = '0%';

    if (state.markersGroup) state.markersGroup.clearLayers();
    if (state.heatLayer && state.map) {
        state.map.removeLayer(state.heatLayer);
        state.heatLayer = null;
    }

    if (mappedEvents.length === 0) {
        if (el.gpsStatusBanner) {
            el.gpsStatusBanner.className = 'gps-banner warning';
            el.gpsBannerText.innerHTML = `⚠️ GPS Telemetry Unavailable — All <strong>${state.totalEvents.toLocaleString()}</strong> events contain <code>latitude: null, longitude: null</code>. Displaying Mode B (GPS Telemetry Unavailable).`;
        }
        if (el.heatmapOverlay && state.viewMode === 'heatmap') {
            el.heatmapOverlay.classList.remove('hidden');
        }
    } else {
        if (el.gpsStatusBanner) {
            el.gpsStatusBanner.className = 'gps-banner success';
            el.gpsBannerText.innerHTML = `📍 <strong>${mappedEvents.length}</strong> events containing real GPS telemetry plotted on map.`;
        }
        if (el.heatmapOverlay) el.heatmapOverlay.classList.add('hidden');

        const heatPoints = [];
        mappedEvents.forEach(evt => {
            const marker = L.marker([evt.latitude, evt.longitude])
                .bindPopup(`
                    <div style="font-family: var(--font-sans); color: #000;">
                        <strong>${evt.event_type.toUpperCase()}</strong><br/>
                        Source: ${evt.source}<br/>
                        Confidence: ${evt.confidence ? (evt.confidence * 100).toFixed(1) + '%' : 'N/A'}<br/>
                        <button onclick="openEventModal('${evt.event_id}')" style="margin-top: 6px; cursor: pointer;">View Payload</button>
                    </div>
                `);
            state.markersGroup.addLayer(marker);
            heatPoints.push([evt.latitude, evt.longitude, evt.confidence || 0.5]);
        });

        if (window.L && L.heatLayer && heatPoints.length > 0) {
            state.heatLayer = L.heatLayer(heatPoints, { radius: 25, blur: 15 });
            if (state.viewMode === 'heatmap' && state.map) {
                state.heatLayer.addTo(state.map);
            }
        }
    }
}

// Toggle View Mode (Markers / Heatmap)
function setViewMode(mode) {
    state.viewMode = mode;
    if (mode === 'markers') {
        if (el.btnViewMarkers) el.btnViewMarkers.classList.add('active');
        if (el.btnViewHeatmap) el.btnViewHeatmap.classList.remove('active');
        if (el.heatmapOverlay) el.heatmapOverlay.classList.add('hidden');
        if (state.heatLayer && state.map) state.map.removeLayer(state.heatLayer);
    } else {
        if (el.btnViewHeatmap) el.btnViewHeatmap.classList.add('active');
        if (el.btnViewMarkers) el.btnViewMarkers.classList.remove('active');
        
        const mappedEvents = state.events.filter(e => e.latitude !== null && e.longitude !== null);
        if (mappedEvents.length === 0) {
            if (el.heatmapOverlay) el.heatmapOverlay.classList.remove('hidden');
        } else if (state.heatLayer && state.map) {
            state.heatLayer.addTo(state.map);
        }
    }
}

// Pagination Controls
function updatePaginationControls(receivedCount) {
    if (el.pageIndicator) el.pageIndicator.textContent = `Page ${state.currentPage}`;
    if (el.btnPrevPage) el.btnPrevPage.disabled = state.currentPage <= 1;
    if (el.btnNextPage) el.btnNextPage.disabled = receivedCount < state.pageSize;
}

// Fetch Real Incidents
async function fetchIncidents() {
    let url = `${API_BASE_URL}/incidents?limit=100`;
    if (state.incFilters.status) url += `&status=${encodeURIComponent(state.incFilters.status)}`;
    if (state.incFilters.severity) url += `&severity=${encodeURIComponent(state.incFilters.severity)}`;

    try {
        const resp = await fetch(url);
        if (!resp.ok) return;
        const incs = await resp.json();
        state.incidents = incs;

        const activeCount = incs.filter(i => i.status !== 'CLOSED' && i.status !== 'RESOLVED').length;
        if (el.valActiveIncidents) el.valActiveIncidents.textContent = activeCount.toString();

        renderIncidentsTable(incs);
    } catch (err) {
        console.error('Failed to fetch incidents:', err);
    }
}

// Render Incidents Table
function renderIncidentsTable(incidents) {
    if (!el.incidentsTableBody) return;
    if (incidents.length === 0) {
        el.incidentsTableBody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No incidents found in database. Create an incident from a real event ID above.</td></tr>';
        return;
    }

    let html = '';
    incidents.forEach(inc => {
        const createdStr = new Date(inc.created_at).toLocaleString();
        html += `
            <tr>
                <td class="font-mono">${inc.incident_id}</td>
                <td class="font-mono">${inc.event_id.slice(0, 16)}...</td>
                <td><strong>${inc.title}</strong></td>
                <td><span class="sev-badge sev-${inc.severity}">${inc.severity}</span></td>
                <td><span class="status-badge ${inc.status}">${inc.status}</span></td>
                <td>${inc.operator || 'Unassigned'}</td>
                <td>${createdStr}</td>
                <td>
                    <button class="btn btn-secondary btn-sm" onclick="openIncidentModal('${inc.incident_id}')">Manage</button>
                </td>
            </tr>
        `;
    });

    el.incidentsTableBody.innerHTML = html;
}

// Handle Incident Creation Form Submit
async function handleCreateIncident(e) {
    e.preventDefault();
    const eventId = el.incEventId.value.trim();
    if (!eventId) {
        alert('Event ID is required');
        return;
    }

    const payload = {
        event_id: eventId,
        severity: el.incSeverity.value,
        title: el.incTitle.value.trim() || undefined,
        operator: el.incOperator.value.trim() || undefined,
        initial_note: el.incNote.value.trim() || undefined
    };

    try {
        const resp = await fetch(`${API_BASE_URL}/incidents`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!resp.ok) {
            const err = await resp.json();
            alert(`Error creating incident: ${err.detail || 'Event ID not found'}`);
            return;
        }

        const newInc = await resp.json();
        alert(`Incident '${newInc.incident_id}' created successfully!`);
        el.createIncForm.reset();
        await fetchIncidents();
    } catch (err) {
        alert(`Network error creating incident: ${err.message}`);
    }
}

// Open Incident Modal for Management
async function openIncidentModal(incidentId) {
    state.selectedIncidentId = incidentId;
    try {
        const resp = await fetch(`${API_BASE_URL}/incidents/${incidentId}`);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const inc = await resp.json();

        if (el.incModalId) el.incModalId.textContent = inc.incident_id;
        if (el.incModalStatus) el.incModalStatus.value = inc.status;
        if (el.incModalSeverity) el.incModalSeverity.value = inc.severity;
        if (el.incModalOperator) el.incModalOperator.value = inc.operator || '';
        if (el.incModalNote) el.incModalNote.value = '';

        // Render History & Notes
        if (el.incModalHistory) {
            let histText = '--- OPERATOR NOTES ---\n';
            if (inc.notes && inc.notes.length > 0) {
                inc.notes.forEach(n => {
                    histText += `[${new Date(n.created_at).toLocaleTimeString()}] ${n.operator || 'Operator'}: ${n.note_text}\n`;
                });
            } else {
                histText += '(No notes recorded)\n';
            }

            histText += '\n--- AUDIT TRAIL ---\n';
            if (inc.history && inc.history.length > 0) {
                inc.history.forEach(h => {
                    histText += `[${new Date(h.created_at).toLocaleTimeString()}] ${h.action}: ${h.details || ''}\n`;
                });
            }
            el.incModalHistory.textContent = histText;
        }

        if (el.incidentModal) el.incidentModal.classList.remove('hidden');
    } catch (err) {
        alert(`Failed to load incident '${incidentId}': ${err.message}`);
    }
}

function closeIncModal() {
    if (el.incidentModal) el.incidentModal.classList.add('hidden');
    state.selectedIncidentId = null;
}

// Handle Incident Update Form Submit
async function handleUpdateIncident(e) {
    e.preventDefault();
    if (!state.selectedIncidentId) return;

    const payload = {
        status: el.incModalStatus.value,
        severity: el.incModalSeverity.value,
        operator: el.incModalOperator.value.trim() || undefined,
        note: el.incModalNote.value.trim() || undefined
    };

    try {
        const resp = await fetch(`${API_BASE_URL}/incidents/${state.selectedIncidentId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!resp.ok) {
            const err = await resp.json();
            alert(`Update rejected: ${err.detail || 'Invalid transition'}`);
            return;
        }

        alert('Incident updated successfully!');
        closeIncModal();
        await fetchIncidents();
    } catch (err) {
        alert(`Error updating incident: ${err.message}`);
    }
}

// Event Details Modal
async function openEventModal(eventId) {
    try {
        const resp = await fetch(`${API_BASE_URL}/events/${eventId}`);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const evt = await resp.json();

        if (el.modalEventId) el.modalEventId.textContent = evt.event_id;
        if (el.modalEventType) el.modalEventType.textContent = evt.event_type;
        if (el.modalSource) el.modalSource.textContent = evt.source || 'unspecified';
        if (el.modalTimestamp) el.modalTimestamp.textContent = evt.timestamp ? new Date(evt.timestamp).toLocaleString() : 'Unavailable';
        if (el.modalGps) el.modalGps.textContent = (evt.latitude !== null && evt.longitude !== null) ? `${evt.latitude}, ${evt.longitude}` : 'Unavailable (null)';
        if (el.modalConfidence) el.modalConfidence.textContent = evt.confidence !== null ? `${(evt.confidence * 100).toFixed(2)}%` : 'N/A';
        if (el.modalCreatedAt) el.modalCreatedAt.textContent = new Date(evt.created_at).toLocaleString();

        if (el.modalJsonPayload) el.modalJsonPayload.textContent = JSON.stringify(evt.payload, null, 2);

        if (el.eventModal) el.eventModal.classList.remove('hidden');
    } catch (err) {
        alert(`Failed to load event details for '${eventId}': ${err.message}`);
    }
}

function closeModal() {
    if (el.eventModal) el.eventModal.classList.add('hidden');
}

// Report Exporters (CSV & JSON)
async function exportEventsCSV() {
    try {
        const resp = await fetch(`${API_BASE_URL}/events?limit=1000`);
        const events = await resp.json();
        
        let csv = 'event_id,event_type,source,timestamp,latitude,longitude,confidence,created_at\n';
        events.forEach(e => {
            csv += `"${e.event_id}","${e.event_type}","${e.source || ''}","${e.timestamp || ''}","${e.latitude || ''}","${e.longitude || ''}","${e.confidence || ''}","${e.created_at}"\n`;
        });

        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `sih2026_events_export_${Date.now()}.csv`;
        a.click();
    } catch (err) {
        alert(`Failed to export CSV: ${err.message}`);
    }
}

async function exportEventsJSON() {
    try {
        const resp = await fetch(`${API_BASE_URL}/events?limit=1000`);
        const events = await resp.json();

        const blob = new Blob([JSON.stringify(events, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `sih2026_events_export_${Date.now()}.json`;
        a.click();
    } catch (err) {
        alert(`Failed to export JSON: ${err.message}`);
    }
}

// Window Expositions
window.openEventModal = openEventModal;
window.openIncidentModal = openIncidentModal;
