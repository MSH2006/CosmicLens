"""Anomaly reasoning backwards compatibility wrapper for CosmicLens / SKYTRACE AI."""

from typing import Any, Dict
from app.services.engine import AnomalyEngine

_engine = AnomalyEngine()


class AnomalyReasoner:
    """Backwards compatibility wrapper delegating to modular AnomalyEngine."""

    def __init__(self) -> None:
        self.engine = _engine

    def analyze(self, object_data: Dict[str, Any], region: Dict[str, Any]) -> Dict[str, Any]:
        """Run analysis and return dictionary representation."""
        result = self.engine.analyze(object_data, region)
        return result.dict()
