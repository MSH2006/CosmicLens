"""Base classes and registry for extensible anomaly detectors in CosmicLens."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
import threading

from app.models.schemas import DetectorResult


class BaseAnomalyDetector(ABC):
    """Abstract Base Class for all anomaly detectors.
    
    To integrate a new detector or increase detection accuracy:
    1. Subclass BaseAnomalyDetector.
    2. Define detector_id, name, dimension, version, default_weight, and description.
    3. Implement calculate().
    4. Decorate the class with @register_detector.
    
    The detector will instantly be registered in the pipeline with zero core modifications!
    """

    @property
    @abstractmethod
    def detector_id(self) -> str:
        """Unique machine-readable identifier (e.g., 'astrometric_motion')."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable display name (e.g., 'Astrometric Proper Motion Detector')."""
        pass

    @property
    @abstractmethod
    def dimension(self) -> str:
        """Physical or statistical dimension: 'motion', 'photometry', 'spectral', 'temporal', 'context'."""
        pass

    @property
    def version(self) -> str:
        """Detector algorithm version."""
        return "1.0.0"

    @property
    def default_weight(self) -> float:
        """Default contribution weight in composite anomaly score (0.0 - 1.0)."""
        return 0.20

    @property
    def description(self) -> str:
        """Scientific description of the detector's physical principles and detection logic."""
        return "Anomaly detector"

    @abstractmethod
    def calculate(
        self,
        epochs: List[Dict[str, Any]],
        context: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> DetectorResult:
        """Compute anomaly score and physical metrics from multi-epoch observations.
        
        Args:
            epochs: List of epoch observations containing 'timestamp', 'jd', 'wavelength', 'data' (SourceObservation dict).
            context: Context data such as region background sources, coordinates, fov.
            config: Optional configuration overrides (e.g. custom threshold multipliers).
            
        Returns:
            DetectorResult containing normalized score (0-100), significance flag, metrics dict, and explanation.
        """
        pass


class DetectorRegistry:
    """Thread-safe global registry of anomaly detectors."""

    _instance: Optional["DetectorRegistry"] = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self._detectors: Dict[str, BaseAnomalyDetector] = {}
        self._weights: Dict[str, float] = {}
        self._active_status: Dict[str, bool] = {}

    @classmethod
    def get_instance(cls) -> "DetectorRegistry":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def register(self, detector_cls: Type[BaseAnomalyDetector]) -> Type[BaseAnomalyDetector]:
        """Register a detector class."""
        detector = detector_cls()
        det_id = detector.detector_id
        self._detectors[det_id] = detector
        if det_id not in self._weights:
            self._weights[det_id] = detector.default_weight
        self._active_status[det_id] = True
        return detector_cls

    def get_detector(self, detector_id: str) -> Optional[BaseAnomalyDetector]:
        """Retrieve a registered detector instance by ID."""
        return self._detectors.get(detector_id)

    def list_detectors(self) -> List[Dict[str, Any]]:
        """List all registered detectors with their metadata, weights, and active status."""
        return [
            {
                "detector_id": d.detector_id,
                "name": d.name,
                "dimension": d.dimension,
                "version": d.version,
                "weight": self._weights.get(d.detector_id, d.default_weight),
                "is_active": self._active_status.get(d.detector_id, True),
                "description": d.description,
            }
            for d in self._detectors.values()
        ]

    def get_active_detectors(self) -> List[BaseAnomalyDetector]:
        """Get list of currently active detector instances."""
        return [
            d for det_id, d in self._detectors.items()
            if self._active_status.get(det_id, True)
        ]

    def get_normalized_weights(self) -> Dict[str, float]:
        """Get normalized weights such that sum of active detector weights equals 1.0."""
        active_ids = [
            det_id for det_id, active in self._active_status.items()
            if active and det_id in self._detectors
        ]
        if not active_ids:
            return {}
        
        raw_weights = {det_id: self._weights.get(det_id, 1.0) for det_id in active_ids}
        total = sum(raw_weights.values())
        if total <= 0:
            equal_w = 1.0 / len(active_ids)
            return {det_id: equal_w for det_id in active_ids}
        return {det_id: w / total for det_id, w in raw_weights.items()}

    def set_weights(self, weights: Dict[str, float]) -> None:
        """Update weights for specified detectors."""
        with self._lock:
            for det_id, w in weights.items():
                if det_id in self._detectors and w >= 0.0:
                    self._weights[det_id] = float(w)

    def set_active(self, detector_id: str, is_active: bool) -> bool:
        """Toggle active status of a detector."""
        if detector_id in self._detectors:
            with self._lock:
                self._active_status[detector_id] = is_active
            return True
        return False


def register_detector(cls: Type[BaseAnomalyDetector]) -> Type[BaseAnomalyDetector]:
    """Class decorator to auto-register an anomaly detector with the global registry."""
    DetectorRegistry.get_instance().register(cls)
    return cls
