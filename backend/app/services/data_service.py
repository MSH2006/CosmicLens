"""Astronomical survey data provider, ingestion pipeline, and synthetic anomaly injector.

Compliant with Section 7 of SKYTRACE AI specification.
All synthetic datasets are explicitly labeled SYNTHETIC_DEMO_DATA.
"""

from typing import Any, Dict, List, Optional
import numpy as np

from app.models.schemas import DISCLAIMER_TEXT, AnomalyInjectionRequest


class AstronomicalDataService:
    """Manages multi-epoch survey fields, dataset ingestion, and dynamic anomaly injection."""

    def __init__(self) -> None:
        self._regions: Dict[str, Dict[str, Any]] = self._generate_default_surveys()

    def get_all_regions(self) -> List[Dict[str, Any]]:
        """List summary of all available survey fields with provenance markers."""
        return [
            {
                "id": r["id"],
                "name": r["name"],
                "data_provenance": r.get("data_provenance", "SYNTHETIC_DEMO_DATA"),
                "disclaimer": DISCLAIMER_TEXT,
                "description": r["description"],
                "ra_center": r["ra_center"],
                "dec_center": r["dec_center"],
                "fov_arcmin": r["fov_arcmin"],
                "epoch_count": len(r["epochs"]),
                "source_count": len(set(s["id"] for ep in r["epochs"] for s in ep["sources"])),
            }
            for r in self._regions.values()
        ]

    def get_region(self, region_id: str) -> Optional[Dict[str, Any]]:
        """Get full multi-epoch astronomical dataset for a specific survey region."""
        return self._regions.get(region_id)

    def inject_synthetic_anomaly(self, req: AnomalyInjectionRequest) -> Dict[str, Any]:
        """Inject a custom synthetic anomaly into a region for real-time testing."""
        region = self._regions.get(req.region_id)
        if not region:
            raise ValueError(f"Region {req.region_id} not found.")

        obj_id = req.object_id
        epochs = region["epochs"]

        base_ra = region["ra_center"] + 0.012
        base_dec = region["dec_center"] - 0.012

        for i, ep in enumerate(epochs):
            ra_shift = (req.ra_offset_arcsec_per_epoch * i) / (3600.0 * max(0.1, np.cos(np.radians(base_dec))))
            dec_shift = (req.dec_offset_arcsec_per_epoch * i) / 3600.0

            multiplier = req.flux_multipliers[i] if i < len(req.flux_multipliers) else 1.0
            flux = req.base_flux * multiplier
            psf = 0.65 if (req.inject_artifact and i == 1) else 2.0
            flag = "marginal" if (req.inject_artifact and i == 1) else "good"

            ep["sources"] = [s for s in ep["sources"] if s["id"] != obj_id]
            ep["sources"].append(
                {
                    "id": obj_id,
                    "ra": base_ra + ra_shift,
                    "dec": base_dec + dec_shift,
                    "position_uncertainty_arcsec": 0.25,
                    "flux": round(flux, 2),
                    "flux_err": round(flux * 0.04, 2),
                    "flag": flag,
                    "psf_fwhm": psf,
                    "type": req.anomaly_type,
                }
            )

        return region

    def ingest_custom_dataset(self, dataset: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and ingest a user-uploaded astronomical survey dataset."""
        region_id = dataset.get("id", f"user_survey_{len(self._regions) + 1}")
        if not dataset.get("epochs") or len(dataset["epochs"]) < 1:
            raise ValueError("Dataset must contain at least one observation epoch.")

        normalized_region = {
            "id": region_id,
            "name": dataset.get("name", "Custom Survey Field"),
            "data_provenance": dataset.get("data_provenance", "SYNTHETIC_DEMO_DATA"),
            "disclaimer": DISCLAIMER_TEXT,
            "ra_center": float(dataset.get("ra_center", 180.0)),
            "dec_center": float(dataset.get("dec_center", 0.0)),
            "fov_arcmin": float(dataset.get("fov_arcmin", 30.0)),
            "description": dataset.get("description", "User-ingested astronomical survey data."),
            "epochs": dataset["epochs"],
        }
        self._regions[region_id] = normalized_region
        return normalized_region

    def _generate_default_surveys(self) -> Dict[str, Dict[str, Any]]:
        """Construct realistic multi-epoch synthetic survey fields."""
        return {
            "region_001": self._create_serpens_field(),
            "region_002": self._create_lyra_field(),
            "region_003": self._create_ecliptic_field(),
        }

    def _create_serpens_field(self) -> Dict[str, Any]:
        """Synthetic Demo Region (Serpens): features DEMO-001 (motion), DEMO-003 (spectral ice), and transient."""
        base_ra = 282.74
        base_dec = -5.52

        epochs_meta = [
            {"epoch_id": "epoch_001", "date": "2026-03-01", "jd": 2460370.5, "wavelength": 1.1},
            {"epoch_id": "epoch_002", "date": "2026-05-15", "jd": 2460445.5, "wavelength": 2.5},
            {"epoch_id": "epoch_003", "date": "2026-08-01", "jd": 2460523.5, "wavelength": 4.2},
            {"epoch_id": "epoch_004", "date": "2026-10-07", "jd": 2460590.5, "wavelength": 3.4},
        ]

        # Trajectory for moving candidate DEMO-001 (also aliased as RW-001)
        demo001_shifts = [
            (0.0, 0.0, 42.0),
            (0.012, 0.011, 54.0),
            (0.025, 0.021, 62.0),
            (0.039, 0.033, 70.0),
        ]

        epochs = []
        for i, meta in enumerate(epochs_meta):
            sources = []

            # 1. Primary candidate: DEMO-001 (Motion Candidate / Solar System Moving Object)
            d_ra, d_dec, flx = demo001_shifts[i]
            sources.append(
                {
                    "id": "DEMO-001",
                    "ra": base_ra + d_ra,
                    "dec": base_dec + d_dec,
                    "position_uncertainty_arcsec": 0.22,
                    "flux": flx,
                    "flux_err": 2.1,
                    "flag": "good",
                    "psf_fwhm": 2.05,
                    "type": "asteroid_candidate",
                }
            )
            # Legacy alias for backward compatibility
            sources.append(
                {
                    "id": "RW-001",
                    "ra": base_ra + d_ra,
                    "dec": base_dec + d_dec,
                    "position_uncertainty_arcsec": 0.22,
                    "flux": flx,
                    "flux_err": 2.1,
                    "flag": "good",
                    "psf_fwhm": 2.05,
                    "type": "asteroid_candidate",
                }
            )

            # 2. Candidate: DEMO-003 / YSO-ICE-07 (Spectral/Ice Anomaly)
            ice_flx = [48.0, 68.0, 85.0, 75.0][i]
            sources.append(
                {
                    "id": "DEMO-003",
                    "ra": base_ra - 0.018,
                    "dec": base_dec + 0.022,
                    "position_uncertainty_arcsec": 0.20,
                    "flux": ice_flx,
                    "flux_err": 2.8,
                    "flag": "good",
                    "psf_fwhm": 2.12,
                    "type": "protostellar_ice_core",
                }
            )

            # 3. Candidate: SN-IR-03 (Infrared Transient Flare)
            sn_flx = [15.0, 115.0, 72.0, 38.0][i]
            sources.append(
                {
                    "id": "SN-IR-03",
                    "ra": base_ra + 0.025,
                    "dec": base_dec - 0.019,
                    "position_uncertainty_arcsec": 0.25,
                    "flux": sn_flx,
                    "flux_err": 3.2,
                    "flag": "good",
                    "psf_fwhm": 1.98,
                    "type": "infrared_transient",
                }
            )

            # 4. Background Reference Stars
            for j in range(1, 12):
                sources.append(
                    {
                        "id": f"SERP-BG-{j:02d}",
                        "ra": base_ra + 0.028 * ((j % 4) - 1.5),
                        "dec": base_dec + 0.026 * ((j // 4) - 1.2),
                        "position_uncertainty_arcsec": 0.18,
                        "flux": 18.0 + (j * 3.7),
                        "flux_err": 1.1,
                        "flag": "good",
                        "psf_fwhm": 1.95,
                        "type": "star",
                    }
                )

            epochs.append(
                {
                    "epoch_id": meta["epoch_id"],
                    "timestamp": meta["date"],
                    "jd": meta["jd"],
                    "wavelength": meta["wavelength"],
                    "sources": sources,
                    "background_median": 14.5,
                    "background_rms": 1.1,
                }
            )

        return {
            "id": "region_001",
            "name": "Synthetic Demo Region (Serpens Field)",
            "data_provenance": "SYNTHETIC_DEMO_DATA",
            "disclaimer": DISCLAIMER_TEXT,
            "ra_center": base_ra,
            "dec_center": base_dec,
            "fov_arcmin": 30.0,
            "description": "Synthetic multi-epoch SPHEREx-like field featuring motion candidate DEMO-001 and spectral ice core DEMO-003.",
            "epochs": epochs,
        }

    def _create_lyra_field(self) -> Dict[str, Any]:
        """Lyra Zone: features DEMO-002 (photometric variability) and DEMO-ART-99 (cosmic ray false alarm)."""
        base_ra = 283.40
        base_dec = 38.78

        epochs_meta = [
            {"epoch_id": "epoch_001", "date": "2026-03-01", "jd": 2460370.5, "wavelength": 1.2},
            {"epoch_id": "epoch_002", "date": "2026-05-15", "jd": 2460445.5, "wavelength": 2.4},
            {"epoch_id": "epoch_003", "date": "2026-08-01", "jd": 2460523.5, "wavelength": 4.1},
            {"epoch_id": "epoch_004", "date": "2026-10-07", "jd": 2460590.5, "wavelength": 3.5},
        ]

        var_fluxes = [32.0, 78.0, 24.0, 65.0]

        epochs = []
        for i, meta in enumerate(epochs_meta):
            sources = []

            # 1. Primary candidate: DEMO-002 / RW-002 (Photometric Variability)
            sources.append(
                {
                    "id": "DEMO-002",
                    "ra": base_ra,
                    "dec": base_dec,
                    "position_uncertainty_arcsec": 0.15,
                    "flux": var_fluxes[i],
                    "flux_err": 2.4,
                    "flag": "good",
                    "psf_fwhm": 2.0,
                    "type": "pulsating_variable",
                }
            )
            sources.append(
                {
                    "id": "RW-002",
                    "ra": base_ra,
                    "dec": base_dec,
                    "position_uncertainty_arcsec": 0.15,
                    "flux": var_fluxes[i],
                    "flux_err": 2.4,
                    "flag": "good",
                    "psf_fwhm": 2.0,
                    "type": "pulsating_variable",
                }
            )

            # 2. False Alarm candidate: DEMO-ART-99 / ART-CR-99 (Sub-diffraction Cosmic Ray)
            sources.append(
                {
                    "id": "DEMO-ART-99",
                    "ra": base_ra + 0.015,
                    "dec": base_dec + 0.012,
                    "position_uncertainty_arcsec": 0.35,
                    "flux": 95.0 if i == 1 else 10.0,
                    "flux_err": 1.8,
                    "flag": "marginal" if i == 1 else "good",
                    "psf_fwhm": 0.65 if i == 1 else 2.0,
                    "type": "cosmic_ray_artifact" if i == 1 else "quiescent_star",
                }
            )
            sources.append(
                {
                    "id": "ART-CR-99",
                    "ra": base_ra + 0.015,
                    "dec": base_dec + 0.012,
                    "position_uncertainty_arcsec": 0.35,
                    "flux": 95.0 if i == 1 else 10.0,
                    "flux_err": 1.8,
                    "flag": "marginal" if i == 1 else "good",
                    "psf_fwhm": 0.65 if i == 1 else 2.0,
                    "type": "cosmic_ray_artifact" if i == 1 else "quiescent_star",
                }
            )

            # 3. Background Reference Stars
            for j in range(1, 10):
                sources.append(
                    {
                        "id": f"LYRA-REF-{j:02d}",
                        "ra": base_ra + 0.022 * ((j % 3) - 1.0),
                        "dec": base_dec + 0.024 * ((j // 3) - 1.0),
                        "position_uncertainty_arcsec": 0.18,
                        "flux": 22.0 + j * 2.0,
                        "flux_err": 1.2,
                        "flag": "good",
                        "psf_fwhm": 1.96,
                        "type": "star",
                    }
                )

            epochs.append(
                {
                    "epoch_id": meta["epoch_id"],
                    "timestamp": meta["date"],
                    "jd": meta["jd"],
                    "wavelength": meta["wavelength"],
                    "sources": sources,
                    "background_median": 12.8,
                    "background_rms": 0.95,
                }
            )

        return {
            "id": "region_002",
            "name": "Lyra High-Variability & False Alarm Test Field",
            "data_provenance": "SYNTHETIC_DEMO_DATA",
            "disclaimer": DISCLAIMER_TEXT,
            "ra_center": base_ra,
            "dec_center": base_dec,
            "fov_arcmin": 25.0,
            "description": "Benchmark field featuring large-amplitude variable candidate DEMO-002 and cosmic ray false alarm DEMO-ART-99.",
            "epochs": epochs,
        }

    def _create_ecliptic_field(self) -> Dict[str, Any]:
        """Ecliptic Field: multiple moving solar system objects."""
        base_ra = 150.25
        base_dec = 12.40

        epochs_meta = [
            {"epoch_id": "epoch_001", "date": "2026-02-10", "jd": 2460351.5, "wavelength": 1.5},
            {"epoch_id": "epoch_002", "date": "2026-04-20", "jd": 2460420.5, "wavelength": 2.8},
            {"epoch_id": "epoch_003", "date": "2026-07-15", "jd": 2460506.5, "wavelength": 4.5},
            {"epoch_id": "epoch_004", "date": "2026-09-30", "jd": 2460583.5, "wavelength": 3.8},
        ]

        epochs = []
        for i, meta in enumerate(epochs_meta):
            sources = []
            sources.append(
                {
                    "id": "NEO-2026-X1",
                    "ra": base_ra + (i * 0.032),
                    "dec": base_dec - (i * 0.024),
                    "position_uncertainty_arcsec": 0.25,
                    "flux": 55.0 + (i * 6.0),
                    "flux_err": 2.2,
                    "flag": "good",
                    "psf_fwhm": 2.02,
                    "type": "near_earth_asteroid",
                }
            )
            for j in range(1, 10):
                sources.append(
                    {
                        "id": f"ECL-BG-{j:02d}",
                        "ra": base_ra - 0.025 + (j * 0.006),
                        "dec": base_dec + 0.020 - (j * 0.005),
                        "position_uncertainty_arcsec": 0.18,
                        "flux": 20.0 + j * 3.1,
                        "flux_err": 1.3,
                        "flag": "good",
                        "psf_fwhm": 1.98,
                        "type": "star",
                    }
                )

            epochs.append(
                {
                    "epoch_id": meta["epoch_id"],
                    "timestamp": meta["date"],
                    "jd": meta["jd"],
                    "wavelength": meta["wavelength"],
                    "sources": sources,
                    "background_median": 16.2,
                    "background_rms": 1.3,
                }
            )

        return {
            "id": "region_003",
            "name": "Ecliptic NEO Corridor",
            "data_provenance": "SYNTHETIC_DEMO_DATA",
            "disclaimer": DISCLAIMER_TEXT,
            "ra_center": base_ra,
            "dec_center": base_dec,
            "fov_arcmin": 35.0,
            "description": "High-latitude ecliptic corridor simulating fast-moving Near-Earth Asteroid orbits.",
            "epochs": epochs,
        }
