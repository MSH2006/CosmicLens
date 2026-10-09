"""Data generator backwards compatibility wrapper for CosmicLens."""

from typing import Any, Dict
from app.services.data_service import AstronomicalDataService

_service = AstronomicalDataService()


def generate_demo_regions() -> Dict[str, Any]:
    """Return all default multi-epoch survey regions."""
    return _service._regions


def generate_serpens_region() -> Dict[str, Any]:
    """Return Serpens Star-Forming survey region."""
    return _service._create_serpens_field()


def generate_lyra_region() -> Dict[str, Any]:
    """Return Lyra survey region."""
    return _service._create_lyra_field()
