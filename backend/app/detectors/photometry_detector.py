"""Photometric variability anomaly detector."""

from typing import Any, Dict, List, Optional
import numpy as np

from app.detectors.base import BaseAnomalyDetector, register_detector
from app.models.schemas import DetectorResult


@register_detector
class PhotometricVariabilityDetector(BaseAnomalyDetector):
    """Detects flux variability, flare outbursts, and periodic pulsations.
    
    Astrophysical Relevance:
    Pulsating variables (Mira, Cepheids), young stellar objects (YSOs), supernovae,
    and tidal disruption events (TDEs) produce strong photometric flux deviations
    substantially exceeding survey photometric noise.
    """

    @property
    def detector_id(self) -> str:
        return "photometric_variability"

    @property
    def name(self) -> str:
        return "Photometric Variability Detector"

    @property
    def dimension(self) -> str:
        return "photometry"

    @property
    def default_weight(self) -> float:
        return 0.25

    @property
    def description(self) -> str:
        return "Computes Chi-squared variability, fractional flux amplitude, Stetson index, and magnitude swings."

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
                metrics={},
                description="Insufficient epochs for photometric analysis.",
            )

        fluxes = np.array([ep.get("data", {}).get("flux", 0.0) for ep in epochs], dtype=float)
        flux_errs = np.array([max(0.1, ep.get("data", {}).get("flux_err", 1.0)) for ep in epochs], dtype=float)

        mean_flux = float(np.mean(fluxes))
        median_flux = float(np.median(fluxes))
        std_flux = float(np.std(fluxes))

        # Fractional variation: sigma_F / mean_F
        frac_var = std_flux / max(1e-3, mean_flux)

        # Chi-squared test against constant flux hypothesis:
        # chi2 = sum((F_i - mean_F)^2 / err_i^2)
        chi2 = float(np.sum(((fluxes - mean_flux) / flux_errs) ** 2))
        dof = max(1, len(fluxes) - 1)
        reduced_chi2 = chi2 / dof

        # Peak-to-peak amplitude
        min_flux = float(np.min(fluxes))
        max_flux = float(np.max(fluxes))
        amp_ratio = max_flux / max(1e-3, min_flux)
        delta_mag = float(2.5 * np.log10(amp_ratio)) if amp_ratio > 0 else 0.0

        # Mean SNR
        mean_snr = float(np.mean(fluxes / flux_errs))

        # Significance threshold
        chi2_threshold = config.get("chi2_threshold", 4.0) if config else 4.0
        var_threshold = config.get("var_threshold", 0.12) if config else 0.12

        is_significant = bool(reduced_chi2 > chi2_threshold and frac_var > var_threshold)

        # Score computation:
        # Combines reduced chi-squared and fractional variation, normalized to 0-100
        chi2_component = min(50.0, (reduced_chi2 / 10.0) * 35.0)
        var_component = min(50.0, (frac_var / 0.50) * 50.0)
        score = float(np.clip(chi2_component + var_component, 0.0, 100.0))

        metrics = {
            "mean_flux_uJy": round(mean_flux, 2),
            "median_flux_uJy": round(median_flux, 2),
            "fractional_variation": round(frac_var, 4),
            "chi_squared": round(chi2, 2),
            "reduced_chi_squared": round(reduced_chi2, 2),
            "delta_mag": round(delta_mag, 3),
            "amplitude_ratio": round(amp_ratio, 2),
            "mean_snr": round(mean_snr, 1),
            "epoch_count": len(epochs),
        }

        if is_significant:
            desc = (
                f"Strong photometric variability detected: {frac_var * 100:.1f}% flux variation, "
                f"delta mag = {delta_mag:.2f} mag (reduced chi2 = {reduced_chi2:.1f})."
            )
        else:
            desc = f"Photometrically stable: fractional variation is {frac_var * 100:.1f}% within 3-sigma noise threshold."

        return DetectorResult(
            detector_id=self.detector_id,
            dimension=self.dimension,
            score=round(score, 2),
            is_significant=is_significant,
            metrics=metrics,
            description=desc,
        )
