# SKYTRACE AI — API Reference

## Base URL
`http://localhost:8000` (Local Development)

All endpoints output `data_provenance: "SYNTHETIC_DEMO_DATA"` and `disclaimer`.

---

## Endpoints

### 1. System Health
- **`GET /api/health`**
  - Returns service status, active data mode, and algorithm version.

### 2. Survey Regions
- **`GET /api/regions`**
  - Returns list of available multi-epoch survey fields with coordinate boundaries and source counts.
- **`GET /api/region/{region_id}`**
  - Returns full multi-epoch dataset for a specified region.
- **`GET /api/region/{region_id}/epochs`**
  - Returns list of discrete observation epochs for a region.
- **`GET /api/region/{region_id}/sources`**
  - Returns paginated list of unique sources in a region with mean fluxes and epoch counts.

### 3. Source Detail & Anomaly Analysis
- **`GET /api/source/{source_id}`**
  - Returns complete observation history of a source across epochs.
- **`GET /api/analyze/object?region_id=...&object_id=...`** (or `POST /api/analyze/object`)
  - Executes 5D anomaly reasoning, false-alarm checks, catalog cross-match, and outputs full Discovery Passport.
- **`GET /api/discoveries?region_id=...&category_filter=...&limit=50`**
  - Returns ranked triage catalog sorted by Scientific Interestingness.

### 4. Scientific Discovery Passports & Reports
- **`GET /api/passport/{passport_id}`**
  - Returns canonical Section 5.7 Scientific Discovery Passport JSON.
- **`GET /api/report/{passport_id}`** (or `POST /api/report/{passport_id}`)
  - Generates and returns self-contained printable HTML Scientific Discovery Report.

### 5. Extensibility & Simulation
- **`GET /api/detectors`**
  - Lists all registered anomaly detectors and current weights.
- **`POST /api/detectors/weights`**
  - Dynamically updates detector weights at runtime.
- **`POST /api/data/inject`**
  - Injects synthetic moving asteroids or transients into the field for real-time testing.
- **`POST /api/data/ingest`**
  - Ingests custom survey datasets in JSON format.
