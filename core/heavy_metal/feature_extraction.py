"""Feature extraction shared by heavy-metal training and inference."""

import numpy as np
import pandas as pd

from core.heavy_metal.config import FEATURE_ORDER


DEFAULT_COLUMN_MAP = {
    "baseline_intensity": "baseline_intensity",
    "response_intensity": "response_intensity",
    "baseline_peak_wavelength_nm": "baseline_peak_wavelength_nm",
    "response_peak_wavelength_nm": "response_peak_wavelength_nm",
    "response_peak_width_nm": "response_peak_width_nm",
    "spectral_skewness": "spectral_skewness",
    "spectral_kurtosis": "spectral_kurtosis",
}


def extract_features(
    dataframe: pd.DataFrame,
    col_map: dict[str, str] | None = None,
) -> dict[str, float]:
    """Extract one feature dictionary from a single measurement row."""
    columns = {**DEFAULT_COLUMN_MAP, **(col_map or {})}
    missing_columns = [column for column in columns.values() if column not in dataframe]
    if missing_columns:
        raise ValueError(f"Missing feature columns: {', '.join(missing_columns)}")
    if len(dataframe) != 1:
        raise ValueError("extract_features expects exactly one measurement row.")

    row = dataframe.iloc[0]
    baseline_intensity = float(row[columns["baseline_intensity"]])
    response_intensity = float(row[columns["response_intensity"]])
    if baseline_intensity == 0:
        raise ValueError("baseline_intensity must be non-zero.")

    return {
        "delta_f_over_f0": (response_intensity - baseline_intensity) / baseline_intensity,
        "emission_shift_nm": float(row[columns["response_peak_wavelength_nm"]])
        - float(row[columns["baseline_peak_wavelength_nm"]]),
        "intensity_ratio": response_intensity / baseline_intensity,
        "peak_width": float(row[columns["response_peak_width_nm"]]),
        "spectral_skewness": float(row[columns["spectral_skewness"]]),
        "spectral_kurtosis": float(row[columns["spectral_kurtosis"]]),
    }


def features_to_vector(
    features: dict[str, float],
    feature_order: list[str] | None = None,
) -> np.ndarray:
    """Convert named features into the model's persisted column order."""
    order = feature_order or FEATURE_ORDER
    missing_features = [name for name in order if name not in features]
    if missing_features:
        raise ValueError(f"Missing features: {', '.join(missing_features)}")
    return np.asarray([[float(features[name]) for name in order]], dtype=float)


def dataframe_to_matrix(
    dataframe: pd.DataFrame,
    col_map: dict[str, str] | None = None,
    feature_order: list[str] | None = None,
) -> np.ndarray:
    """Extract an ordered feature matrix from all measurement rows."""
    rows = [
        features_to_vector(extract_features(dataframe.iloc[[index]], col_map), feature_order)[0]
        for index in range(len(dataframe))
    ]
    return np.asarray(rows, dtype=float)