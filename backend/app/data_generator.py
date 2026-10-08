"""Demo data generator for CosmicLens.

Generates synthetic SPHEREx-like infrared observations.
"""

from datetime import datetime
from typing import Any, Dict, List

import numpy as np


def generate_demo_regions() -> Dict[str, Any]:
    """Generate synthetic demo regions with temporal anomalies."""
    return {
        "region_001": generate_serpens_region(),
        "region_002": generate_lyra_region(),
    }


def generate_serpens_region() -> Dict[str, Any]:
    """
    Serpens Deep Survey region.
    Contains RW-001: a moving object with motion and photometric anomalies.
    """
    np.random.seed(42)
    base_ra = 282.74
    base_dec = -5.52

    epochs_data = [
        {"date": "2026-03-01", "wavelength": 1.1, "flux_delta": 0.0, "ra_shift": 0.0, "dec_shift": 0.0},
        {"date": "2026-05-15", "wavelength": 2.5, "flux_delta": 12.0, "ra_shift": 0.012, "dec_shift": 0.011},
        {"date": "2026-08-01", "wavelength": 4.2, "flux_delta": 20.0, "ra_shift": 0.025, "dec_shift": 0.021},
        {"date": "2026-10-07", "wavelength": 3.4, "flux_delta": 28.0, "ra_shift": 0.039, "dec_shift": 0.033},
    ]

    epochs = []
    for i, e in enumerate(epochs_data):
        sources = []

        # Primary candidate object (RW-001)
        sources.append(
            {
                "id": "RW-001",
                "ra": base_ra + e["ra_shift"],
                "dec": base_dec + e["dec_shift"],
                "flux": 42.0 + e["flux_delta"],
                "flux_err": 2.1,
                "flag": "good",
                "psf_fwhm": 2.1,
                "type": "unknown",
            }
        )

        # Background sources
        for j in range(8):
            sources.append(
                {
                    "id": f"BG-{j:03d}",
                    "ra": base_ra + 0.03 * (j + 1),
                    "dec": base_dec - 0.025 * (j + 1),
                    "flux": 18.0 + j * 2.5,
                    "flux_err": 1.4,
                    "flag": "good",
                    "psf_fwhm": 1.8,
                    "type": "star",
                }
            )

        epochs.append(
            {
                "timestamp": e["date"],
                "jd": 2460000 + i * 70,
                "wavelength": e["wavelength"],
                "sources": sources,
            }
        )

    return {
        "id": "region_001",
        "name": "Serpens Deep Survey",
        "ra_center": base_ra,
        "dec_center": base_dec,
        "fov_arcmin": 30,
        "epochs": epochs,
        "description": "Deep infrared survey region with a moving candidate object.",
    }


def generate_lyra_region() -> Dict[str, Any]:
    """
    Lyra Anomaly Zone.
    Contains RW-002: a variable star with photometric anomalies.
    """
    np.random.seed(123)
    base_ra = 18.5
    base_dec = 42.2

    epochs_data = [
        {"date": "2026-03-01", "wavelength": 1.2, "flux_factor": 1.0},
        {"date": "2026-05-15", "wavelength": 2.4, "flux_factor": 1.4},
        {"date": "2026-08-01", "wavelength": 4.1, "flux_factor": 0.7},
        {"date": "2026-10-07", "wavelength": 3.5, "flux_factor": 1.2},
    ]

    epochs = []
    for i, e in enumerate(epochs_data):
        sources = []

        # Variable candidate (RW-002)
        sources.append(
            {
                "id": "RW-002",
                "ra": base_ra + np.random.normal(0, 0.0005),
                "dec": base_dec + np.random.normal(0, 0.0005),
                "flux": 35.0 * e["flux_factor"],
                "flux_err": 2.5,
                "flag": "good",
                "psf_fwhm": 2.0,
                "type": "variable",
            }
        )

        # Background sources
        for j in range(8):
            sources.append(
                {
                    "id": f"LY-{j:03d}",
                    "ra": base_ra + 0.02 * (j + 1),
                    "dec": base_dec - 0.02 * (j + 1),
                    "flux": 20.0 + j * 1.5,
                    "flux_err": 1.2,
                    "flag": "good",
                    "psf_fwhm": 1.9,
                    "type": "star",
                }
            )

        epochs.append(
            {
                "timestamp": e["date"],
                "jd": 2460100 + i * 70,
                "wavelength": e["wavelength"],
                "sources": sources,
            }
        )

    return {
        "id": "region_002",
        "name": "Lyra Anomaly Zone",
        "ra_center": base_ra,
        "dec_center": base_dec,
        "fov_arcmin": 30,
        "epochs": epochs,
        "description": "Region with strong photometric variability.",
    }
