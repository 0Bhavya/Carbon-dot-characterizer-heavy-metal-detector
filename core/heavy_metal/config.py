"""Shared configuration for the heavy-metal ML pipeline."""

from pathlib import Path

SUPPORTED_METALS = ["Pb", "Hg", "Cd", "Cr", "Cu"]

DETECTION_MODEL_TYPE = "random_forest"
IDENTIFICATION_MODEL_TYPE = "random_forest"
CONCENTRATION_MODEL_TYPE = "random_forest"

IDENTIFICATION_CONFIDENCE_THRESHOLD = 0.6

FEATURE_NAMES = [
    "delta_f_over_f0",
    "emission_shift_nm",
    "intensity_ratio",
    "peak_width",
    "spectral_skewness",
    "spectral_kurtosis",
]
FEATURE_ORDER = FEATURE_NAMES.copy()

MODEL_ARTIFACT_DIRECTORY = Path("models")
