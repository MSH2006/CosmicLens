"""SKYTRACE AI Anomaly Reasoning Engine Orchestrator.

Strictly aligned with Section 5.3, 5.4, 5.5, 5.6 of the specification.
"""

from typing import Any, Dict, List, Optional
import numpy as np

# Ensure detectors are imported and registered
import app.detectors.motion_detector  # noqa: F401
import app.detectors.photometry_detector  # noqa: F401
import app.detectors.spectral_detector  # noqa: F401
import app.detectors.temporal_detector  # noqa: F401
import app.detectors.context_detector  # noqa: F401

from app.detectors.base import DetectorRegistry
from app.detectors.artifact_vetter import FalseAlarmInvestigator
from app.classifiers.astrophysical_classifier import AstrophysicalClassifier
from app.detectors.spectral_detector import SpectralAnomalyDetector
from app.services.catalog_service import CatalogCrossCheckService
from app.models.schemas import (
    ALGORITHM_VERSION,
    DISCLAIMER_TEXT,
    AnalysisResult,
    DetectorResult,
    EvidenceConfidence,
    SEDPoint,
)


class AnomalyEngine:
    """Orchestrates multi-dimensional anomaly detection, vetting, and classification."""

    def __init__(self) -> None:
        self.registry = DetectorRegistry.get_instance()
        self.investigator = FalseAlarmInvestigator(diffraction_limit_fwhm=1.8)
        self.classifier = AstrophysicalClassifier()
        self.spectral_helper = SpectralAnomalyDetector()
        self.catalog_service = CatalogCrossCheckService(search_radius_arcsec=5.0)

    def analyze(
        self,
        object_data: Dict[str, Any],
        region: Dict[str, Any],
        config_override: Optional[Dict[str, Any]] = None,
    ) -> AnalysisResult:
        """Execute full multi-dimensional discovery pipeline on an astronomical target."""
        obj_id = object_data.get("id", "UNKNOWN")
        epochs = object_data.get("epochs", [])

        # 1. Run all active detectors
        active_detectors = self.registry.get_active_detectors()
        detector_results: Dict[str, DetectorResult] = {}
        for det in active_detectors:
            try:
                res = det.calculate(epochs, region, config_override)
                detector_results[det.detector_id] = res
            except Exception as e:
                detector_results[det.detector_id] = DetectorResult(
                    detector_id=det.detector_id,
                    dimension=det.dimension,
                    score=0.0,
                    is_significant=False,
                    metrics={"error": str(e)},
                    description=f"Detector error: {str(e)}",
                )

        # 2. Run False Alarm and Data Quality Investigation
        false_alarm_inv, data_quality = self.investigator.investigate(epochs)

        # 3. Known-Object Catalog Cross-Check
        ras = [ep.get("data", {}).get("ra", 0.0) for ep in epochs]
        decs = [ep.get("data", {}).get("dec", 0.0) for ep in epochs]
        ra_mean = float(np.mean(ras)) if ras else region.get("ra_center", 0.0)
        dec_mean = float(np.mean(decs)) if decs else region.get("dec_center", 0.0)
        catalog_result = self.catalog_service.cross_check(obj_id, ra_mean, dec_mean)

        # 4. Compute Scientific Interestingness Score (transparent heuristic)
        weights = self.registry.get_normalized_weights()
        if config_override and "weights" in config_override:
            raw_w = config_override["weights"]
            tot = sum(raw_w.values())
            weights = {k: v / max(1e-4, tot) for k, v in raw_w.items()}

        composite_interestingness = 0.0
        dimensional_scores: Dict[str, float] = {}

        for det_id, res in detector_results.items():
            w = weights.get(det_id, 0.0)
            composite_interestingness += w * res.score
            dimensional_scores[res.dimension] = round(res.score, 2)

        composite_interestingness = float(np.clip(composite_interestingness, 0.0, 100.0))

        # 5. Compute Separate Evidence Confidence Assessment
        has_failed_check = any(c.status == "FAIL" for c in false_alarm_inv.checks)
        has_caution_check = any(c.status == "CAUTION" for c in false_alarm_inv.checks)
        n_epochs = len(epochs)

        confidence_reasons = []
        if n_epochs >= 4:
            confidence_reasons.append(f"Four usable observation epochs across multi-month baseline.")
        elif n_epochs >= 2:
            confidence_reasons.append(f"{n_epochs} usable observation epochs available.")
        else:
            confidence_reasons.append("Single-epoch detection; temporal baseline is unverified.")

        if has_failed_check:
            confidence_reasons.append("Critical false-alarm check failed (sub-diffraction PSF or detector glitch).")
            conf_tier = "LOW"
            conf_numeric = 22.0
        elif has_caution_check:
            confidence_reasons.append("Observational quality caveats present (marginal SNR or single-epoch outlier dominance).")
            conf_tier = "MODERATE"
            conf_numeric = 62.0
        elif n_epochs >= 3:
            confidence_reasons.append("All automated false-alarm and data-quality checks passed successfully.")
            conf_tier = "HIGH"
            conf_numeric = 92.0
        else:
            conf_tier = "MODERATE"
            conf_numeric = 55.0

        evidence_confidence = EvidenceConfidence(
            tier=conf_tier,
            numeric_value=conf_numeric,
            reasons=confidence_reasons,
        )

        # 6. Scientific Priority (Triage category, not proof of real discovery)
        if composite_interestingness >= 70.0 and conf_tier in ["HIGH", "MODERATE"]:
            scientific_priority = "HIGH"
        elif composite_interestingness >= 40.0:
            scientific_priority = "MODERATE"
        else:
            scientific_priority = "LOW"

        # 7. Astrophysical Classification
        # Create legacy-compatible vetting audit dict for classifier
        legacy_vetting_proxy = type(
            "VettingProxy",
            (),
            {
                "overall_artifact_probability": 85.0 if has_failed_check else 15.0 if has_caution_check else 3.5,
                "psf_consistency": "sub_diffraction_artifact" if has_failed_check else "consistent_stellar_profile",
            },
        )()
        classification_breakdown = self.classifier.classify(detector_results, legacy_vetting_proxy)
        primary_class = classification_breakdown[0]

        # 8. Generate 102-channel SED profile
        sed_profile = self.spectral_helper.generate_sed_spectrum(epochs)

        # 9. Evidence-linked Explanations ("Why Is This Interesting?")
        why_interesting, narrative = self._synthesize_explanations(
            obj_id,
            composite_interestingness,
            evidence_confidence,
            detector_results,
            false_alarm_inv,
            primary_class,
        )

        # 10. Follow-up Suggestions & Limitations
        follow_up = self._generate_follow_up_suggestions(primary_class.category, composite_interestingness)
        limitations = [
            "SIMULATED DEMO DATA — NOT A REAL ASTRONOMICAL DISCOVERY.",
            "SPHEREx observations are discrete survey passes, not continuous monitoring.",
            "Known-object catalog cross-checks are subject to Gaia/2MASS detection and coverage limits.",
            "Anomaly scores are triage heuristics, not physical probabilities.",
        ]

        return AnalysisResult(
            object_id=obj_id,
            data_provenance="SYNTHETIC_DEMO_DATA",
            disclaimer=DISCLAIMER_TEXT,
            algorithm_version=ALGORITHM_VERSION,
            interestingness_score=round(composite_interestingness, 2),
            evidence_confidence=evidence_confidence,
            scientific_priority=scientific_priority,
            primary_classification=primary_class,
            classification_breakdown=classification_breakdown,
            dimensional_scores=dimensional_scores,
            detector_results=detector_results,
            quality_checks=false_alarm_inv.checks,
            false_alarm_investigation=false_alarm_inv,
            known_object_cross_check=catalog_result,
            why_interesting=why_interesting,
            astrophysical_narrative=narrative,
            sed_profile=sed_profile,
            follow_up_suggestions=follow_up,
            limitations=limitations,
        )

    def _synthesize_explanations(
        self,
        object_id: str,
        interestingness: float,
        confidence: EvidenceConfidence,
        detector_results: Dict[str, DetectorResult],
        false_alarm_inv: Any,
        primary_class: Any,
    ) -> (List[str], str):
        cues: List[str] = []

        motion = detector_results.get("astrometric_motion")
        if motion and motion.is_significant:
            tot = motion.metrics.get("total_motion_arcsec", 0.0)
            spd = motion.metrics.get("apparent_speed_arcsec_yr", 0.0)
            lin = motion.metrics.get("trajectory_linearity", 0.0)
            cues.append(
                f"Position changed by {tot:.2f} arcseconds ({spd:.1f} arcsec/yr); exceeds combined astrometric uncertainty with {lin*100:.0f}% orbital linearity."
            )

        photo = detector_results.get("photometric_variability")
        if photo and photo.is_significant:
            frac = photo.metrics.get("fractional_variation", 0.0) * 100.0
            rchi2 = photo.metrics.get("reduced_chi_squared", 1.0)
            cues.append(
                f"Flux varied by {frac:.1f}% across epochs (reduced chi2 = {rchi2:.1f}); exceeds 3-sigma measurement noise."
            )

        spec = detector_results.get("spectral_anomaly")
        if spec and spec.is_significant:
            if spec.metrics.get("has_ice_absorption"):
                cues.append("Strong molecular absorption detected at 3.05 um (H2O ice) and 4.27 um (CO2 ice).")
            else:
                cues.append(f"Infrared color departure: color index = {spec.metrics.get('infrared_color_index', 0.0):.2f} mag.")

        temp = detector_results.get("temporal_dynamics")
        if temp and temp.is_significant:
            cues.append("Temporal evolution indicates non-stationary transient light curve outburst.")

        # False alarm warnings
        for chk in false_alarm_inv.checks:
            if chk.status == "FAIL":
                cues.append(f"Quality Check Warning [{chk.name}]: {chk.details}")
            elif chk.status == "CAUTION":
                cues.append(f"Quality Check Caution [{chk.name}]: {chk.details}")

        if not cues:
            cues.append("Source behavior is consistent with quiescent background stellar population within noise.")

        narrative = (
            f"Candidate {object_id} is evaluated with Scientific Interestingness of {interestingness:.1f}/100 "
            f"and Evidence Confidence tier '{confidence.tier}' ({confidence.numeric_value:.0f}%). "
            f"The primary classification heuristic is {primary_class.label} (confidence: {primary_class.probability * 100:.0f}%). "
            f"{primary_class.rationale}"
        )

        return cues, narrative

    def _generate_follow_up_suggestions(self, category: str, score: float) -> List[str]:
        if category == "NEAR_EARTH_OBJECT":
            return [
                "Submit astrometric positions to IAU Minor Planet Center (MPC) for orbital determination.",
                "Cross-reference with NASA JPL Horizons ephemeris database.",
                "Obtain rapid optical photometric monitoring to constrain rotation period.",
            ]
        elif category == "VARIABLE_STAR":
            return [
                "Monitor across upcoming SPHEREx survey passes to construct full phase light curve.",
                "Perform Lomb-Scargle periodogram analysis for pulsation cycle determination.",
            ]
        elif category == "INFRARED_TRANSIENT":
            return [
                "Trigger urgent near-infrared spectroscopic characterization (e.g. JWST NIRSpec / Keck).",
                "Examine archival deep imaging for progenitor candidate.",
            ]
        elif category == "ICE_RICH_CORE":
            return [
                "Targeted JWST NIRSpec / MIRI spectroscopy (1-28 um) for ice column density profiling.",
                "ALMA sub-millimeter continuum mapping for core mass and kinematics.",
            ]
        elif category == "INSTRUMENTAL_ARTIFACT":
            return [
                "Flag for pipeline focal plane audit: inspect raw detector telemetry for cosmic ray hit.",
                "Deprioritize for follow-up telescope allocation.",
            ]
        else:
            return [
                "Maintain in standard astronomical monitoring catalog.",
                "Re-evaluate upon release of next all-sky survey data pass.",
            ]
