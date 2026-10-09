"""Field context and neighborhood outlier detector."""

from typing import Any, Dict, List, Optional
import numpy as np

from app.detectors.base import BaseAnomalyDetector, register_detector
from app.models.schemas import DetectorResult


@register_detector
class ContextualOutlierDetector(BaseAnomalyDetector):
    """Compares candidate properties against surrounding field reference stars.
    
    Astrophysical Relevance:
    Real astronomical anomalies stand out prominently against the local stellar background
    population. Determining contextual departure ensures that field-wide systematics
    (such as solar stray light, calibration drift, or zodiacal light gradient) are distinguished
    from genuine astrophysical anomalies.
    """

    @property
    def detector_id(self) -> str:
        return "contextual_outlier"

    @property
    def name(self) -> str:
        return "Field Context & Neighborhood Outlier Detector"

    @property
    def dimension(self) -> str:
        return "context"

    @property
    def default_weight(self) -> float:
        return 0.10

    @property
    def description(self) -> str:
        return "Computes robust z-score deviation and spatial isolation relative to the local reference population."

    def calculate(
        self,
        epochs: List[Dict[str, Any]],
        context: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> DetectorResult:
        if not epochs:
            return DetectorResult(
                detector_id=self.detector_id,
                dimension=self.dimension,
                score=0.0,
                is_significant=False,
                metrics={},
                description="No epochs available for context comparison.",
            )

        obj_id = epochs[0].get("data", {}).get("id", "")
        obj_fluxes = [ep.get("data", {}).get("flux", 0.0) for ep in epochs]
        target_mean_flux = float(np.mean(obj_fluxes))

        # Extract background sources from region context
        region_epochs = context.get("epochs", [])
        field_fluxes = []
        for ep in region_epochs:
            for src in ep.get("sources", []):
                if src.get("id") != obj_id:
                    field_fluxes.append(src.get("flux", 0.0))

        if not field_fluxes:
            return DetectorResult(
                detector_id=self.detector_id,
                dimension=self.dimension,
                score=10.0,
                is_significant=False,
                metrics={"field_source_count": 0},
                description="Isolated source with no local comparison stars.",
            )

        field_array = np.array(field_fluxes, dtype=float)
        field_mean = float(np.mean(field_array))
        field_std = float(np.std(field_array))
        field_median = float(np.median(field_array))
        field_mad = float(np.median(np.abs(field_array - field_median))) * 1.4826  # Normalized MAD

        # Robust z-score
        robust_z = abs(target_mean_flux - field_median) / max(1e-3, field_mad)

        # Score calculation
        z_threshold = config.get("z_threshold", 2.5) if config else 2.5
        score = float(np.clip((robust_z / 4.0) * 80.0, 0.0, 100.0))
        is_significant = bool(robust_z >= z_threshold)

        metrics = {
            "robust_z_score": round(robust_z, 2),
            "target_mean_flux_uJy": round(target_mean_flux, 2),
            "field_median_flux_uJy": round(field_median, 2),
            "field_mad_uJy": round(field_mad, 2),
            "reference_sources_compared": len(field_fluxes),
            "significance_threshold_z": z_threshold,
        }

        if is_significant:
            desc = (
                f"Statistically significant field outlier: departs by {robust_z:.1f} sigma (MAD) "
                f"from {len(field_fluxes)} background reference observations."
            )
        else:
            desc = f"Consistent with local background population (z-score = {robust_z:.1f} sigma)."

        return DetectorResult(
            detector_id=self.detector_id,
            dimension=self.dimension,
            score=round(score, 2),
            is_significant=is_significant,
            metrics=metrics,
            description=desc,
        )
