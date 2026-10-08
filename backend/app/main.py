"""Main API entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data_generator import generate_demo_regions
from app.anomaly_engine import AnomalyReasoner
from app.discovery_passport import DiscoveryPassport

app = FastAPI(title="CosmicLens API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load demo data
demo_regions = generate_demo_regions()
reasoner = AnomalyReasoner()


@app.get("/api/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "cosmiclens-backend"}


@app.get("/api/regions")
def list_regions():
    """List available demo regions."""
    return {
        "regions": [
            {
                "id": region["id"],
                "name": region["name"],
                "description": region["description"],
            }
            for region in demo_regions.values()
        ]
    }


@app.get("/api/region/{region_id}")
def get_region(region_id: str):
    """Get full region data."""
    region = demo_regions.get(region_id)
    if not region:
        return {"error": "Region not found"}, 404
    return region


@app.get("/api/analyze/object")
def analyze_object(region_id: str, object_id: str):
    """Analyze a specific object for anomalies."""
    region = demo_regions.get(region_id)
    if not region:
        return {"error": "Region not found"}, 404

    # Collect epochs for this object
    object_epochs = []
    for epoch in region["epochs"]:
        source = next((s for s in epoch["sources"] if s["id"] == object_id), None)
        if source:
            object_epochs.append({"timestamp": epoch["timestamp"], "data": source})

    if not object_epochs:
        return {"error": "Object not found"}, 404

    # Run analysis
    analysis = reasoner.analyze({"id": object_id, "epochs": object_epochs}, region)

    # Generate passport
    passport = DiscoveryPassport(object_id, {"id": object_id, "epochs": object_epochs}, analysis, region).to_dict()

    return {"object_id": object_id, "analysis": analysis, "passport": passport}


@app.get("/api/discoveries")
def get_top_discoveries(region_id: str = "region_001", limit: int = 10):
    """Get top anomalous discoveries in a region."""
    region = demo_regions.get(region_id)
    if not region:
        return {"error": "Region not found"}, 404

    # Collect all unique objects
    all_objects = set()
    for epoch in region["epochs"]:
        for source in epoch["sources"]:
            all_objects.add(source["id"])

    # Analyze each
    discoveries = []
    for obj_id in all_objects:
        object_epochs = []
        for epoch in region["epochs"]:
            source = next((s for s in epoch["sources"] if s["id"] == obj_id), None)
            if source:
                object_epochs.append({"timestamp": epoch["timestamp"], "data": source})

        if len(object_epochs) > 1:  # Only multi-epoch objects
            analysis = reasoner.analyze({"id": obj_id, "epochs": object_epochs}, region)
            discoveries.append(
                {
                    "object_id": obj_id,
                    "interestingness": analysis["anomaly_score"],
                    "confidence": analysis["evidence_confidence"],
                    "why_interesting_summary": analysis["why_interesting"][0] if analysis["why_interesting"] else "No anomalies detected.",
                }
            )

    # Sort by interestingness
    discoveries.sort(key=lambda x: x["interestingness"], reverse=True)

    return {"region_id": region_id, "total": len(discoveries), "discoveries": discoveries[:limit]}
