"""Anomaly detection and scoring engine.

Provides multi-dimensional anomaly reasoning for infrared objects.
"""

from typing import Any, Dict, List

import numpy as np


class AnomalyReasoner:
    """Multi-dimensional anomaly detector with explainability."""

    def __init__(self) -> None:
        """Initialize with default weights."""
        self.weights = {
            "motion": 0.30,
            "photometry": 0.25,
            "spectral": 0.20,
            "temporal": 0.15,
            "context": 0.10,
        }

    def analyze(self, object_data: Dict[str, Any], region: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive anomaly analysis for an object.

        Args:
            object_data: {"id": "RW-001", "epochs": [{"timestamp": ..., "data": {...}}, ...]}
            region: Region containing all sources for context comparison.

        Returns:
            Dict with anomaly scores, confidence, and explanations.
        """
        epochs = object_data["epochs"]

        if len(epochs) < 2:
            return {
                "anomaly_score": 0.0,
                "evidence_confidence": 0.0,
                "why_interesting": ["Insufficient epochs for analysis."],
            }

        motion = self._analyze_motion(epochs)
        photometry = self._analyze_photometry(epochs)
        spectral = self._analyze_spectral(epochs)
        temporal = self._analyze_temporal(epochs)
        context = self._analyze_context(object_data, region)
        quality = self._check_data_quality(epochs)
        artifacts = self._investigate_artifacts(epochs)

        # Composite anomaly score
        composite = (
            self.weights["motion"] * motion["score"]
            + self.weights["photometry"] * photometry["score"]
            + self.weights["spectral"] * spectral["score"]
            + self.weights["temporal"] * temporal["score"]
            + self.weights["context"] * context["score"]
        )

        # Evidence confidence
        artifact_penalty = (
            np.mean([a["probability"] for a in artifacts])
            if artifacts
            else 0.0
        )
        evidence_confidence = max(
            0.0, min(100.0, quality["quality_score"] * (1.0 - artifact_penalty))
        )

        explanation = self._generate_explanation(
            motion, photometry, spectral, quality, context
        )

        return {
            "anomaly_score": float(round(min(100.0, composite), 2)),
            "evidence_confidence": float(round(evidence_confidence, 2)),
            "why_interesting": explanation,
            "artifacts": artifacts,
            "data_quality": quality,
            "motion_anomaly": motion,
            "photometry_anomaly": photometry,
            "spectral_anomaly": spectral,
            "temporal_anomaly": temporal,
            "context_anomaly": context,
        }

    def _analyze_motion(self, epochs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect positional changes."""
        positions = [
            (epoch["data"]["ra"], epoch["data"]["dec"]) for epoch in epochs
        ]
        deltas = []
        for i in range(1, len(positions)):
            dra = abs((positions[i][0] - positions[i - 1][0]) * 3600.0)
            ddec = abs((positions[i][1] - positions[i - 1][1]) * 3600.0)
            deltas.append(np.hypot(dra, ddec))

        total_motion = float(np.sum(deltas)) if deltas else 0.0
        score = min(100.0, total_motion * 12.0)
        return {
            "score": float(round(score, 2)),
            "is_significant": bool(total_motion > 1.5),
            "total_motion_arcsec": float(round(total_motion, 3)),
            "description": f"Total positional change: {total_motion:.2f} arcsec",
        }

    def _analyze_photometry(self, epochs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect brightness changes."""
        fluxes = np.array([epoch["data"]["flux"] for epoch in epochs], dtype=float)
        if len(fluxes) < 2:
            return {
                "score": 0.0,
                "is_variable": False,
                "fractional_variation": 0.0,
                "description": "Insufficient flux data",
            }

        mean_flux = float(np.mean(fluxes))
        variation = float(np.std(fluxes) / mean_flux) if mean_flux else 0.0
        score = min(100.0, variation * 600.0)
        return {
            "score": float(round(score, 2)),
            "is_variable": bool(variation > 0.08),
            "fractional_variation": float(round(variation, 3)),
            "description": f"Brightness variation: {variation * 100:.1f}%",
        }

    def _analyze_spectral(self, epochs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect spectral changes."""
        # Simplified: check wavelength diversity
        wavelengths = [epoch.get("wavelength", 0) for epoch in epochs]
        unique_wl = len(set(wavelengths))

        score = min(100.0, unique_wl * 15.0)
        return {
            "score": float(round(score, 2)),
            "is_variable": bool(unique_wl > 1),
            "description": f"Observed across {unique_wl} distinct wavelengths",
        }

    def _analyze_temporal(self, epochs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect temporal patterns."""
        n_epochs = len(epochs)
        score = min(100.0, n_epochs * 18.0)
        return {
            "score": float(round(score, 2)),
            "is_significant": bool(n_epochs > 2),
            "epoch_count": int(n_epochs),
            "description": f"Observed across {n_epochs} epochs",
        }

    def _analyze_context(self, object_data: Dict[str, Any], region: Dict[str, Any]) -> Dict[str, Any]:
        """Compare to background sources."""
        target = np.mean([epoch["data"]["flux"] for epoch in object_data["epochs"]])
        all_fluxes = []
        for epoch in region["epochs"]:
            for source in epoch["sources"]:
                if source["id"] != object_data["id"]:
                    all_fluxes.append(source["flux"])

        if not all_fluxes:
            return {"score": 0.0, "is_outlier": False, "description": "No comparison sources"}

        background_mean = float(np.mean(all_fluxes))
        background_std = float(np.std(all_fluxes))
        z = abs(target - background_mean) / (background_std + 1e-9)
        score = min(100.0, z * 20.0)
        return {
            "score": float(round(score, 2)),
            "is_outlier": bool(z > 1.5),
            "z_score": float(round(z, 3)),
            "description": "Behavior differs from nearby reference sources",
        }

    def _check_data_quality(self, epochs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate measurement quality."""
        quality_values = []
        flags = []
        for epoch in epochs:
            flag = epoch["data"].get("flag", "unknown")
            flags.append(flag)
            quality_values.append(
                1.0 if flag == "good" else 0.7 if flag == "marginal" else 0.4
            )

        quality_score = float(np.mean(quality_values))
        return {
            "quality_score": float(round(quality_score * 100.0, 2)),
            "measurement_quality": (
                "good" if quality_score > 0.8 else "marginal" if quality_score > 0.5 else "poor"
            ),
            "flags": flags,
        }

    def _investigate_artifacts(self, epochs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for common false-alarm causes."""
        artifacts = []
        for i, epoch in enumerate(epochs):
            flux = epoch["data"].get("flux", 0.0)
            flux_err = epoch["data"].get("flux_err", 0.0)

            if flux_err / max(flux, 1.0) > 0.18:
                artifacts.append(
                    {
                        "type": "measurement_noise",
                        "epoch": int(i),
                        "probability": 0.22,
                        "description": "Flux uncertainty is somewhat high.",
                    }
                )

            if epoch["data"].get("flag") == "marginal":
                artifacts.append(
                    {
                        "type": "data_quality",
                        "epoch": int(i),
                        "probability": 0.18,
                        "description": "One epoch has marginal quality.",
                    }
                )

        return artifacts

    def _generate_explanation(self, motion: Dict, photometry: Dict, spectral: Dict, quality: Dict, context: Dict) -> List[str]:
        """Generate human-readable explanations."""
        reasons: List[str] = []

        if motion["is_significant"]:
            reasons.append(
                f"✓ Motion anomaly: The object changed by {motion['total_motion_arcsec']} arcsec "
                f"between epochs, which exceeds typical astrometric noise."
            )

        if photometry["is_variable"]:
            reasons.append(
                f"✓ Photometric anomaly: The brightness changed by {photometry['fractional_variation'] * 100:.1f}% "
                f"over the observation sequence."
            )

        if spectral["is_variable"]:
            reasons.append(
                "✓ Spectral anomaly: The object shows different colors across infrared bands, "
                "indicating a non-stationary spectral pattern."
            )

        if quality["measurement_quality"] in {"good", "marginal"}:
            reasons.append(
                f"✓ Data quality: The measurements are {quality['measurement_quality']} quality, "
                f"supporting confidence in the detection."
            )

        if context["is_outlier"]:
            reasons.append(
                f"✓ Context anomaly: The source departs from nearby background sources "
                f"(z-score: {context['z_score']})."
            )

        if not reasons:
            reasons.append("⚠ No strong anomaly detected. Object appears consistent with background.")

        return reasons
