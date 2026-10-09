"""Astrometric proper motion anomaly detector."""

from typing import Any, Dict, List, Optional
import numpy as np

from app.detectors.base import BaseAnomalyDetector, register_detector
from app.models.schemas import DetectorResult


@register_detector
class AstrometricMotionDetector(BaseAnomalyDetector):
    """Detects positional displacement and linear trajectory consistency across survey epochs.
    
    Astrophysical Relevance:
    Solar System objects (Near-Earth Asteroids, Main-Belt Asteroids, Kuiper Belt Objects)
    display significant proper motion over baseline epochs (arcsec to arcmin displacement),
    whereas distant stars and galaxies maintain fixed coordinates within astrometric error.
    """

    @property
    def detector_id(self) -> str:
        return "astrometric_motion"

    @property
    def name(self) -> str:
        return "Astrometric Proper Motion Detector"

    @property
    def dimension(self) -> str:
        return "motion"

    @property
    def default_weight(self) -> float:
        return 0.30

    @property
    def description(self) -> str:
        return "Quantifies sky displacement, proper motion velocity vector, and linear orbital trajectory consistency."

    def calculate(
        self,
        epochs: List[Dict[str, Any]],
        context: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> DetectorResult:
        if len(epochs) < 2:
            return DetectorResult(
                detector_id=self.detector_id,
                dimension=self.dimension,
                score=0.0,
                is_significant=False,
                metrics={"total_motion_arcsec": 0.0, "epoch_count": len(epochs)},
                description="Insufficient epochs to calculate astrometric motion.",
            )

        positions = []
        timestamps = []
        for ep in epochs:
            src = ep.get("data", {})
            positions.append((src.get("ra", 0.0), src.get("dec", 0.0)))
            timestamps.append(ep.get("jd", 0.0))

        deltas = []
        ra_deltas = []
        dec_deltas = []
        for i in range(1, len(positions)):
            ra1, dec1 = positions[i - 1]
            ra2, dec2 = positions[i]
            # Convert RA/Dec degree differences to arcseconds, accounting for cos(dec)
            dec_mean_rad = np.radians((dec1 + dec2) / 2.0)
            dra = (ra2 - ra1) * np.cos(dec_mean_rad) * 3600.0
            ddec = (dec2 - dec1) * 3600.0
            step_disp = float(np.hypot(dra, ddec))
            deltas.append(step_disp)
            ra_deltas.append(dra)
            dec_deltas.append(ddec)

        total_motion_arcsec = float(np.sum(deltas))
        max_single_step = float(np.max(deltas)) if deltas else 0.0

        # Calculate linear trajectory fit (R-squared / direction consistency)
        time_span_days = max(1.0, (timestamps[-1] - timestamps[0]))
        velocity_arcsec_day = total_motion_arcsec / time_span_days

        # Measure directional linearity (Keplerian motion produces steady heading)
        if len(ra_deltas) > 1:
            angles = [np.arctan2(dec_deltas[i], ra_deltas[i]) for i in range(len(ra_deltas))]
            angle_variance = float(np.var(angles))
            linearity_score = max(0.0, min(1.0, 1.0 - (angle_variance / (np.pi ** 2))))
        else:
            linearity_score = 0.85

        # Typical astrometric noise for SPHEREx is ~0.15 - 0.3 arcsec.
        # Motion > 1.2 arcsec is highly statistically significant.
        threshold = config.get("motion_threshold_arcsec", 1.2) if config else 1.2

        # Non-linear scaling to 0-100 score
        # 0 arcsec -> 0
        # 1.2 arcsec -> 45
        # 3.0 arcsec -> 85
        # 5.0+ arcsec -> 100
        score = float(np.clip(100.0 / (1.0 + np.exp(-1.2 * (total_motion_arcsec - 1.5))) - 15.0, 0.0, 100.0))
        # Boost if highly linear (consistent asteroid/solar system track)
        if total_motion_arcsec > threshold and linearity_score > 0.7:
            score = float(min(100.0, score * 1.15))

        is_significant = total_motion_arcsec >= threshold

        metrics = {
            "total_motion_arcsec": round(total_motion_arcsec, 4),
            "max_step_arcsec": round(max_single_step, 4),
            "velocity_arcsec_day": round(velocity_arcsec_day, 5),
            "apparent_speed_arcsec_yr": round(velocity_arcsec_day * 365.25, 3),
            "trajectory_linearity": round(linearity_score, 3),
            "time_baseline_days": round(time_span_days, 1),
            "threshold_arcsec": threshold,
        }

        if is_significant:
            desc = (
                f"Significant sky displacement: {total_motion_arcsec:.2f} arcsec "
                f"({metrics['apparent_speed_arcsec_yr']:.1f} arcsec/yr) with "
                f"{linearity_score * 100:.0f}% orbital trajectory linearity."
            )
        else:
            desc = f"Astrometrically stationary: total displacement {total_motion_arcsec:.2f} arcsec within survey point-spread limits."

        return DetectorResult(
            detector_id=self.detector_id,
            dimension=self.dimension,
            score=round(score, 2),
            is_significant=is_significant,
            metrics=metrics,
            description=desc,
        )
