"""Discovery passport backwards compatibility wrapper for CosmicLens / SKYTRACE AI."""

from typing import Any, Dict
from app.services.passport_service import PassportService
from app.services.engine import AnomalyEngine

_engine = AnomalyEngine()


class DiscoveryPassport:
    """Backwards compatibility wrapper delegating to PassportService."""

    def __init__(self, object_id: str, object_data: Dict[str, Any], analysis: Any, region: Dict[str, Any]):
        self.object_id = object_id
        self.object_data = object_data
        self.analysis = analysis
        self.region = region

    def to_dict(self) -> Dict[str, Any]:
        """Convert passport to dictionary format."""
        epochs_data = self.object_data.get("epochs", [])
        if isinstance(self.analysis, dict):
            # Run engine analysis to produce typed AnalysisResult
            analysis_obj = _engine.analyze(self.object_data, self.region)
        else:
            analysis_obj = self.analysis

        passport_obj = PassportService.generate_passport(self.object_id, epochs_data, analysis_obj, self.region)
        return passport_obj.dict()
