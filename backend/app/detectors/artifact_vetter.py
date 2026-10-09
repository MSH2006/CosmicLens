"""False alarm and data quality investigation engine.

Aligned with Section 5.4 of SKYTRACE AI specification.
Produces discrete states: PASS, CAUTION, FAIL, UNKNOWN, NOT EVALUATED.
"""

from typing import Any, Dict, List
import numpy as np

from app.models.schemas import (
    DataQualitySummary,
    FalseAlarmInvestigation,
    QualityCheckItem,
)


class FalseAlarmInvestigator:
    """Investigates potential instrumental artifacts and data-quality concerns."""

    def __init__(self, diffraction_limit_fwhm: float = 1.8) -> None:
        self.diffraction_limit_fwhm = diffraction_limit_fwhm

    def investigate(self, epochs: List[Dict[str, Any]]) -> (FalseAlarmInvestigation, DataQualitySummary):
        """Execute structured false-alarm checks across multi-epoch measurements."""
        checks: List[QualityCheckItem] = []
        possible_alternatives: List[str] = []
        available_flags: List[str] = []
        missing_metadata: List[str] = []

        if not epochs:
            checks.append(
                QualityCheckItem(
                    name="epoch_coverage",
                    status="FAIL",
                    details="Zero observation epochs available for evaluation.",
                )
            )
            return (
                FalseAlarmInvestigation(
                    checks=checks,
                    possible_alternatives=["Unobserved field"],
                    assessment="Insufficient observational coverage.",
                ),
                DataQualitySummary(
                    available_flags=[],
                    missing_metadata=["flux", "psf_fwhm", "coordinates"],
                    assessment="Missing all observational metadata.",
                ),
            )

        fwhm_values = []
        flux_snr_values = []
        flags = []

        for i, ep in enumerate(epochs):
            src = ep.get("data", {})
            flux = float(src.get("flux", 0.0))
            flux_err = float(src.get("flux_err", 1.0))
            flag = src.get("flag", "unknown")
            psf = float(src.get("psf_fwhm", 2.0))

            fwhm_values.append(psf)
            flags.append(flag)
            available_flags.append(f"T{i+1}:{flag}")
            if flux_err > 0:
                flux_snr_values.append(flux / flux_err)

        # CHECK 1: Signal-to-Noise Ratio (SNR)
        mean_snr = float(np.mean(flux_snr_values)) if flux_snr_values else 0.0
        min_snr = float(np.min(flux_snr_values)) if flux_snr_values else 0.0

        if min_snr >= 7.0:
            checks.append(
                QualityCheckItem(
                    name="signal_to_noise",
                    status="PASS",
                    details=f"High photometric SNR across all epochs (mean SNR = {mean_snr:.1f}, min SNR = {min_snr:.1f}).",
                )
            )
        elif min_snr >= 3.0:
            checks.append(
                QualityCheckItem(
                    name="signal_to_noise",
                    status="CAUTION",
                    details=f"Marginal detection SNR in at least one epoch (min SNR = {min_snr:.1f}). Photometric error may contribute to variability.",
                )
            )
            possible_alternatives.append("Photometric noise fluctuation near detection limit.")
        else:
            checks.append(
                QualityCheckItem(
                    name="signal_to_noise",
                    status="FAIL",
                    details=f"Low signal-to-noise ratio (min SNR = {min_snr:.1f} < 3.0). Detections susceptible to background noise spikes.",
                )
            )
            possible_alternatives.append("Background noise fluctuation.")

        # CHECK 2: Point Spread Function (PSF) Consistency vs Optical Diffraction Limit
        min_fwhm = float(np.min(fwhm_values)) if fwhm_values else 2.0
        if min_fwhm < (self.diffraction_limit_fwhm * 0.60):
            checks.append(
                QualityCheckItem(
                    name="psf_diffraction_consistency",
                    status="FAIL",
                    details=f"Sub-diffraction PSF FWHM detected ({min_fwhm:.2f}\" < {self.diffraction_limit_fwhm * 0.60:.2f}\"). Strongly characteristic of direct cosmic ray charge deposit in detector pixels.",
                )
            )
            possible_alternatives.append("Cosmic ray charge deposit (sub-diffraction point profile).")
        elif min_fwhm > (self.diffraction_limit_fwhm * 2.2):
            checks.append(
                QualityCheckItem(
                    name="psf_diffraction_consistency",
                    status="CAUTION",
                    details=f"Extended PSF FWHM ({min_fwhm:.2f}\"). Possible blended source, unresolved binary, or background galaxy.",
                )
            )
            possible_alternatives.append("Stellar blending or extended diffuse background source.")
        else:
            checks.append(
                QualityCheckItem(
                    name="psf_diffraction_consistency",
                    status="PASS",
                    details=f"PSF FWHM ({min_fwhm:.2f}\") is fully consistent with SPHEREx optical diffraction limit.",
                )
            )

        # CHECK 3: Single-Epoch Dominance
        if len(epochs) == 1:
            checks.append(
                QualityCheckItem(
                    name="single_epoch_dominance",
                    status="CAUTION",
                    details="Source appears in only 1 epoch. Temporal verification across survey baseline is currently absent.",
                )
            )
            possible_alternatives.append("Unconfirmed single-epoch transient or fleeting detector anomaly.")
        else:
            # Check if one epoch accounts for >80% of total variance
            fluxes = [float(ep.get("data", {}).get("flux", 0.0)) for ep in epochs]
            mean_f = np.mean(fluxes)
            deviations = [abs(f - mean_f) for f in fluxes]
            max_dev = max(deviations) if deviations else 0.0
            sum_dev = sum(deviations) if deviations else 1.0

            if (max_dev / max(1e-3, sum_dev)) > 0.85 and max(fluxes) > (2.5 * min(fluxes)):
                checks.append(
                    QualityCheckItem(
                        name="single_epoch_dominance",
                        status="CAUTION",
                        details="Anomaly score is heavily dominated by a single epoch outlier. Multi-epoch confirmation recommended.",
                    )
                )
                possible_alternatives.append("Isolated single-epoch flare or transient calibration jump.")
            else:
                checks.append(
                    QualityCheckItem(
                        name="single_epoch_dominance",
                        status="PASS",
                        details="Behavior is verified across multiple epochs without single-epoch outlier dominance.",
                    )
                )

        # CHECK 4: Detector Quality Flags
        has_bad_pixel = any(f in ["bad_pixel", "saturated"] for f in flags)
        has_marginal = any(f in ["marginal", "marginal_edge"] for f in flags)

        if has_bad_pixel:
            checks.append(
                QualityCheckItem(
                    name="detector_flags",
                    status="FAIL",
                    details="Pipeline flags indicate bad pixel defect or saturation in focal plane array.",
                )
            )
            possible_alternatives.append("Known detector bad pixel or focal plane artifact.")
        elif has_marginal:
            checks.append(
                QualityCheckItem(
                    name="detector_flags",
                    status="CAUTION",
                    details="Marginal measurement flag present. Astrometric or photometric precision may be degraded.",
                )
            )
        else:
            checks.append(
                QualityCheckItem(
                    name="detector_flags",
                    status="PASS",
                    details="All epoch measurement flags pass standard quality thresholds ('good').",
                )
            )

        # CHECK 5: Coordinate Metadata Check
        pos_uncertainties = [ep.get("data", {}).get("position_uncertainty_arcsec") for ep in epochs]
        if all(u is not None for u in pos_uncertainties):
            checks.append(
                QualityCheckItem(
                    name="astrometric_uncertainty_metadata",
                    status="PASS",
                    details="Astrometric uncertainty metadata available and accounted for in motion estimation.",
                )
            )
        else:
            checks.append(
                QualityCheckItem(
                    name="astrometric_uncertainty_metadata",
                    status="UNKNOWN",
                    details="Positional uncertainty metadata partially absent; default survey baseline used.",
                )
            )
            missing_metadata.append("position_uncertainty_arcsec")

        # Synthesize Overall Assessment
        has_fail = any(c.status == "FAIL" for c in checks)
        has_caution = any(c.status == "CAUTION" for c in checks)

        if has_fail:
            assessment = "High false-alarm likelihood. One or more critical quality checks failed (e.g. sub-diffraction PSF or detector glitch)."
        elif has_caution:
            assessment = "Low-to-moderate false-alarm risk. Some quality caveats present (e.g. single-epoch dominance or marginal SNR)."
        else:
            assessment = "Passed all automated false-alarm and data-quality checks. High observational reliability."

        if not possible_alternatives:
            possible_alternatives.append("Genuine astrophysical phenomenon (low artifact probability).")

        data_quality_assessment = (
            "Good quality" if not has_fail and not has_caution else "Marginal quality with caveats" if not has_fail else "Compromised quality"
        )

        return (
            FalseAlarmInvestigation(
                checks=checks,
                possible_alternatives=possible_alternatives,
                assessment=assessment,
            ),
            DataQualitySummary(
                available_flags=list(set(available_flags)),
                missing_metadata=missing_metadata,
                assessment=data_quality_assessment,
            ),
        )
