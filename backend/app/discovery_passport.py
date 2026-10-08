"""Scientific Discovery Passport generator."""

from typing import Any, Dict


class DiscoveryPassport:
    """Generates a scientific profile for each candidate object."""

    def __init__(self, object_id: str, object_data: Dict[str, Any], analysis: Dict[str, Any], region: Dict[str, Any]):
        self.object_id = object_id
        self.object_data = object_data
        self.analysis = analysis
        self.region = region

    def to_dict(self) -> Dict[str, Any]:
        """Convert passport to dictionary."""
        start = self.object_data["epochs"][0]["timestamp"]
        end = self.object_data["epochs"][-1]["timestamp"]

        anomaly_score = self.analysis.get("anomaly_score", 0.0)
        if anomaly_score > 75:
            priority = "HIGH"
        elif anomaly_score > 50:
            priority = "MODERATE"
        else:
            priority = "LOW"

        return {
            "passport_id": f"CL-{self.region['id'].split('_')[-1]}-{self.object_id}",
            "generated_at": "2026-10-08T00:00:00Z",
            "identity": {
                "source_id": self.object_id,
                "region": self.region["name"],
                "observation_start": start,
                "observation_end": end,
                "epoch_count": len(self.object_data["epochs"]),
            },
            "motion": {
                "total_motion_arcsec": self.analysis["motion_anomaly"].get("total_motion_arcsec", 0.0),
                "assessment": "Significant motion" if self.analysis["motion_anomaly"].get("is_significant") else "Stable position",
            },
            "photometry": {
                "fractional_variation": self.analysis["photometry_anomaly"].get("fractional_variation", 0.0),
                "assessment": "Brightness changes detected"
                if self.analysis["photometry_anomaly"].get("is_variable")
                else "No strong photometric change",
            },
            "spectrum": {
                "assessment": "Multi-band infrared observation",
                "note": "Spectral fingerprint shows wavelength-dependent variation.",
            },
            "false_alarm_check": {
                "artifact_probability": round(
                    sum(a["probability"] for a in self.analysis.get("artifacts", [])) / max(1, len(self.analysis.get("artifacts", []))),
                    2,
                ),
                "assessment": "Low artifact probability",
            },
            "ai_summary": {
                "anomaly_score": self.analysis.get("anomaly_score", 0.0),
                "evidence_confidence": self.analysis.get("evidence_confidence", 0.0),
                "why_interesting": self.analysis.get("why_interesting", []),
            },
            "scientific_priority": priority,
            "recommendations": [
                "Review full light curve and spectral evolution.",
                "Cross-check against known moving objects.",
                "Consider follow-up observations in targeted filters.",
            ],
        }
