"""Temporal dynamics and light curve evolution detector."""

from typing import Any, Dict, List, Optional
import numpy as np

from app.detectors.base import BaseAnomalyDetector, register_detector
from app.models.schemas import DetectorResult


@register_detector
class TemporalDynamicsDetector(BaseAnomalyDetector):
    """Detects temporal evolution patterns such as fast-rising transients, flares, and non-stationary light curves.
    
    Astrophysical Relevance:
    Explosive transients (supernovae, novae, gamma-ray burst afterglows) exhibit steep
    temporal derivatives ($dF/dt$), while pulsating stars show cyclic inflection points,
    and moving asteroids exhibit steady flux modulation driven by rotational light curves.
    """

    @property
    def detector_id(self) -> str:
        return "temporal_dynamics"

    @property
    def name(self) -> str:
        return "Temporal Dynamics & Transient Evolution Detector"

    @property
    def dimension(self) -> str:
        return "temporal"

    @property
    def default_weight(self) -> float:
        return 0.15

    @property
    def description(self) -> str:
        return "Evaluates temporal derivatives, flux rise/decay asymmetry, cadence coverage, and transient profile signatures."

    def calculate(
        self,
        epochs: List[Dict[str, Any]],
        context: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> DetectorResult:
        n_epochs = len(epochs)
        if n_epochs < 2:
            return DetectorResult(
                detector_id=self.detector_id,
                dimension=self.dimension,
                score=0.0,
                is_significant=False,
                metrics={"epoch_count": n_epochs},
                description="Insufficient temporal epochs to evaluate dynamics.",
            )

        jds = np.array([ep.get("jd", 0.0) for ep in epochs], dtype=float)
        fluxes = np.array([ep.get("data", {}).get("flux", 0.0) for ep in epochs], dtype=float)

        time_deltas = np.diff(jds)
        flux_deltas = np.diff(fluxes)

        # Protect against duplicate timestamps
        safe_time_deltas = np.where(time_deltas <= 0, 1.0, time_deltas)
        rates_of_change = flux_deltas / safe_time_deltas  # uJy / day

        max_rate = float(np.max(np.abs(rates_of_change))) if len(rates_of_change) > 0 else 0.0
        
        # Test for transient flare: rapid initial rise followed by decay
        is_transient_profile = False
        if len(flux_deltas) >= 2:
            if flux_deltas[0] > 0 and np.all(flux_deltas[1:] < 0):
                is_transient_profile = True

        # Monotonicity test
        is_monotonic_brightening = bool(np.all(flux_deltas > 0))
        is_monotonic_fading = bool(np.all(flux_deltas < 0))

        # Overall temporal variability score
        total_baseline = float(jds[-1] - jds[0]) if len(jds) > 1 else 1.0
        cadence_regularity = float(1.0 - (np.std(time_deltas) / max(1.0, np.mean(time_deltas)))) if len(time_deltas) > 1 else 1.0

        score = 0.0
        if is_transient_profile:
            score += 70.0
        elif is_monotonic_brightening or is_monotonic_fading:
            score += 45.0
        
        # Rate-based score component
        mean_flux = float(np.mean(fluxes))
        rel_rate = max_rate / max(1.0, mean_flux)
        score += min(30.0, rel_rate * 50.0)

        # Baseline bonus
        score += min(15.0, n_epochs * 3.5)
        score = float(np.clip(score, 0.0, 100.0))

        is_significant = bool(is_transient_profile or rel_rate > 0.05 or score > 50.0)

        metrics = {
            "epoch_count": n_epochs,
            "temporal_baseline_days": round(total_baseline, 1),
            "max_rate_of_change_uJy_day": round(max_rate, 4),
            "is_transient_flare_profile": is_transient_profile,
            "is_monotonic_brightening": is_monotonic_brightening,
            "is_monotonic_fading": is_monotonic_fading,
            "cadence_regularity": round(max(0.0, cadence_regularity), 3),
        }

        if is_transient_profile:
            desc = "Transient light curve profile detected: steep initial rise followed by gradual post-peak decay."
        elif is_monotonic_brightening:
            desc = f"Monotonically brightening source: sustained positive flux derivative across {n_epochs} epochs."
        elif is_significant:
            desc = f"Dynamic light curve activity: maximum rate of flux change = {max_rate:.2f} uJy/day."
        else:
            desc = f"Quiescent temporal behavior over {total_baseline:.0f} day baseline."

        return DetectorResult(
            detector_id=self.detector_id,
            dimension=self.dimension,
            score=round(score, 2),
            is_significant=is_significant,
            metrics=metrics,
            description=desc,
        )
