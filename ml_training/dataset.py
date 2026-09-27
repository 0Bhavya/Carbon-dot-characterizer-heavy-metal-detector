"""Load and prepare datasets for the heavy-metal training scripts."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from core.heavy_metal.config import SUPPORTED_METALS


REQUIRED_COLUMNS = {
    "sample_id",
    "metal_label",
    "concentration",
    "baseline_intensity",
    "response_intensity",
    "baseline_peak_wavelength_nm",
    "response_peak_wavelength_nm",
    "response_peak_width_nm",
    "spectral_skewness",
    "spectral_kurtosis",
}

NUMERIC_COLUMNS = {
    "concentration",
    "baseline_intensity",
    "response_intensity",
    "baseline_peak_wavelength_nm",
    "response_peak_wavelength_nm",
    "response_peak_width_nm",
    "spectral_skewness",
    "spectral_kurtosis",
}


@dataclass(frozen=True)
class TrainingTargets:
    """Targets shared by the detection, identification, and regression scripts."""

    detection: np.ndarray
    identification_mask: np.ndarray
    identification: np.ndarray
    concentration: np.ndarray


def load_training_dataset(path: str | Path) -> pd.DataFrame:
    """Load a CSV training dataset and reject incompatible or invalid rows."""
    dataset_path = Path(path)
    if dataset_path.suffix.lower() != ".csv":
        raise ValueError("Training datasets must currently be CSV files.")

    dataframe = pd.read_csv(dataset_path, keep_default_na=False)
    missing_columns = sorted(REQUIRED_COLUMNS - set(dataframe.columns))
    if missing_columns:
        raise ValueError(f"Training dataset is missing columns: {', '.join(missing_columns)}")
    if dataframe.empty:
        raise ValueError("Training dataset must contain at least one row.")
    if dataframe["sample_id"].duplicated().any():
        raise ValueError("Training dataset contains duplicate sample_id values.")

    metal_labels = dataframe["metal_label"].astype("string")
    allowed_labels = set(SUPPORTED_METALS) | {"None"}
    unexpected_labels = sorted(set(metal_labels.dropna()) - allowed_labels)
    if unexpected_labels:
        raise ValueError(
            f"Unsupported metal_label values: {', '.join(unexpected_labels)}"
        )
    if metal_labels.isna().any():
        raise ValueError("Training dataset contains missing metal_label values.")

    for column in NUMERIC_COLUMNS:
        values = pd.to_numeric(dataframe[column], errors="coerce")
        if values.isna().any() or not np.isfinite(values.to_numpy()).all():
            raise ValueError(f"Training dataset contains invalid numeric values in {column}.")
        dataframe[column] = values

    if (dataframe["concentration"] < 0).any():
        raise ValueError("Training dataset concentration values cannot be negative.")

    dataframe["metal_label"] = metal_labels
    return dataframe


def derive_training_targets(dataframe: pd.DataFrame) -> TrainingTargets:
    """Derive the three model targets from validated metal labels and concentration."""
    metal_labels = dataframe["metal_label"].astype(str).to_numpy()
    identification_mask = metal_labels != "None"

    return TrainingTargets(
        detection=identification_mask.astype(np.int8),
        identification_mask=identification_mask,
        identification=metal_labels[identification_mask],
        concentration=dataframe["concentration"].to_numpy(dtype=float),
    )