# CosmicLens Backend — Phase 1

Phase 1 backend includes:
- Demo data generator (2 synthetic regions)
- Anomaly detection engine (motion, photometry, spectral, temporal, context)
- Discovery Passport generator
- FastAPI endpoints for region data and analysis

## Testing locally

### 1. Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Test data generation
```bash
python -c "from app.data_generator import generate_demo_regions; regions = generate_demo_regions(); print(list(regions.keys())); print(f'Serpens epochs: {len(regions[\"region_001\"][\"epochs\"])}')"
```

### 3. Test anomaly engine
```bash
python -c "
from app.data_generator import generate_demo_regions
from app.anomaly_engine import AnomalyReasoner

regions = generate_demo_regions()
reasoner = AnomalyReasoner()
region = regions['region_001']

# Collect RW-001 epochs
object_epochs = []
for epoch in region['epochs']:
    source = next((s for s in epoch['sources'] if s['id'] == 'RW-001'), None)
    if source:
        object_epochs.append({'timestamp': epoch['timestamp'], 'data': source})

analysis = reasoner.analyze({'id': 'RW-001', 'epochs': object_epochs}, region)
print(f\"Anomaly score: {analysis['anomaly_score']}/100\")
print(f\"Confidence: {analysis['evidence_confidence']}%\")
print('Why interesting:')
for reason in analysis['why_interesting']:
    print(f'  {reason}')
"
```

### 4. Run the API server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then test endpoints:

```bash
# Health check
curl http://localhost:8000/api/health

# List regions
curl http://localhost:8000/api/regions

# Get region data
curl http://localhost:8000/api/region/region_001

# Analyze an object
curl "http://localhost:8000/api/analyze/object?region_id=region_001&object_id=RW-001"

# Get top discoveries
curl "http://localhost:8000/api/discoveries?region_id=region_001&limit=5"
```
