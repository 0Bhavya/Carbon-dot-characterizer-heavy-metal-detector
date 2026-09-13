from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd
from scipy.ndimage import median_filter
from scipy.signal import savgol_filter


@dataclass
class CleaningConfig:
    """Configuration for the characterization cleaning pipeline."""

    missing_method: str = "interpolate"
    artifact_z_thresh: float = 3.0
    artifact_action: str = "flag"
    smoothing_window: int = 11
    smoothing_polyorder: int = 3
    smooth: bool = True


@dataclass
class CleanedResult:
    """Raw data, cleaned data, artifact flags, and processing metadata."""

    raw: pd.DataFrame
    cleaned: pd.DataFrame
    artifact_mask: np.ndarray
    params_used: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def _mapped_columns(
    df: pd.DataFrame,
    col_map: dict,
) -> tuple[object | None, object | None]:
    """Return mapped x/y columns, or (None, None) for an invalid map."""

    if not isinstance(col_map, dict):
        return None, None

    x_column = col_map.get("x")
    y_column = col_map.get("y")

    if x_column is None or y_column is None:
        return None, None

    try:
        if x_column not in df.columns or y_column not in df.columns:
            return None, None
    except Exception:
        return None, None

    if x_column == y_column:
        return None, None

    return x_column, y_column


def _numeric_series(values: pd.Series) -> pd.Series:
    """Convert values to floats without changing the source Series."""

    return pd.to_numeric(values, errors="coerce").astype(float)


def handle_missing_values(
    df: pd.DataFrame,
    col_map: dict,
    method: str = "interpolate",
) -> pd.DataFrame:
    """Handle missing x/y values on a deep copy of df.

    interpolate:
        Fills internal numeric gaps and leaves edge gaps missing.

    drop:
        Removes rows missing either required value.

    ffill:
        Carries the last known numeric value forward.

    Non-numeric values are not converted into valid measurements.
    """

    cleaned = (
        df.copy(deep=True)
        if isinstance(df, pd.DataFrame)
        else pd.DataFrame()
    )

    if not isinstance(df, pd.DataFrame):
        return cleaned

    if method not in {"interpolate", "drop", "ffill"}:
        raise ValueError(
            "method must be 'interpolate', 'drop', or 'ffill'"
        )

    x_column, y_column = _mapped_columns(cleaned, col_map)

    if x_column is None or y_column is None:
        return cleaned

    if method == "drop":
        return cleaned.dropna(
            subset=[x_column, y_column]
        ).copy()

    for column in (x_column, y_column):
        values = cleaned[column]

        if not values.isna().any():
            continue

        numeric = _numeric_series(values)

        if (
            values.notna().any()
            and numeric.notna().sum() == values.notna().sum()
        ):
            if method == "interpolate":
                cleaned[column] = numeric.interpolate(
                    method="linear",
                    limit_area="inside",
                )
            else:
                cleaned[column] = numeric.ffill()

    return cleaned


def detect_artifacts(
    y: np.ndarray,
    z_thresh: float = 3.0,
) -> np.ndarray:
    """Return a mask for isolated spikes using local median deviation.

    The local median makes the detector less likely to flag a broad,
    genuine spectral peak.

    Very small datasets are not statistically reliable for artifact
    detection, so artifact detection is skipped when fewer than
    five finite values are available.
    """

    if z_thresh <= 0:
        raise ValueError("z_thresh must be greater than zero")

    values = pd.to_numeric(
        pd.Series(np.asarray(y).reshape(-1)),
        errors="coerce",
    )

    values = values.to_numpy(dtype=float)

    mask = np.zeros(values.size, dtype=bool)

    finite = np.isfinite(values)

    # Do not perform statistical artifact detection on very small datasets.
    if finite.sum() < 5:
        return mask

    window = min(5, values.size)

    if window % 2 == 0:
        window -= 1

    if window < 3:
        return mask

    filled = values.copy()

    median_value = float(np.nanmedian(filled[finite]))
    filled[~finite] = median_value

    local_median = median_filter(
        filled,
        size=window,
        mode="nearest",
    )

    deviation = np.abs(filled - local_median)

    valid_deviation = deviation[finite]

    center = float(np.median(valid_deviation))

    mad = float(
        np.median(
            np.abs(valid_deviation - center)
        )
    )

    scale = 1.4826 * mad

    if scale == 0:
        candidate = deviation > center
    else:
        candidate = (
            deviation
            > center + z_thresh * scale
        )

    mask[finite] = candidate[finite]

    return mask


def smooth_spectrum(
    y: np.ndarray,
    window: int = 11,
    polyorder: int = 3,
) -> np.ndarray:
    """Smooth a numeric signal using Savitzky-Golay filtering."""

    if window <= 0 or polyorder < 0:
        raise ValueError(
            "window must be positive and "
            "polyorder cannot be negative"
        )

    if window % 2 == 0:
        window -= 1

    if window <= polyorder:
        raise ValueError(
            "window must be greater than polyorder"
        )

    values = pd.to_numeric(
        pd.Series(np.asarray(y).reshape(-1)),
        errors="coerce",
    )

    result = values.to_numpy(dtype=float)

    if (
        result.size <= polyorder
        or not np.isfinite(result).all()
    ):
        return result.copy()

    valid_window = min(
        window,
        result.size
        if result.size % 2
        else result.size - 1,
    )

    if valid_window <= polyorder or valid_window < 3:
        return result.copy()

    return savgol_filter(
        result,
        window_length=valid_window,
        polyorder=polyorder,
    )


def clean_pipeline(
    df: pd.DataFrame,
    col_map: dict,
    config: CleaningConfig | None = None,
) -> CleanedResult:
    """Run missing-value handling, artifact flagging, and smoothing."""

    config = config or CleaningConfig()

    raw = (
        df.copy(deep=True)
        if isinstance(df, pd.DataFrame)
        else pd.DataFrame()
    )

    cleaned = raw.copy(deep=True)

    warnings: list[str] = []

    artifact_mask = np.zeros(
        len(cleaned),
        dtype=bool,
    )

    params_used = {
        "missing_method": config.missing_method,
        "artifact_z_thresh": config.artifact_z_thresh,
        "artifact_action": config.artifact_action,
        "smoothing_window": config.smoothing_window,
        "smoothing_polyorder": config.smoothing_polyorder,
        "smooth": config.smooth,
    }

    x_column, y_column = _mapped_columns(
        cleaned,
        col_map,
    )

    if x_column is None or y_column is None:
        warnings.append(
            "Cleaning skipped because the x/y "
            "column mapping is invalid."
        )

        return CleanedResult(
            raw,
            cleaned,
            artifact_mask,
            params_used,
            warnings,
        )

    try:
        cleaned = handle_missing_values(
            cleaned,
            col_map,
            method=config.missing_method,
        )

    except ValueError as error:
        warnings.append(str(error))

        return CleanedResult(
            raw,
            cleaned,
            artifact_mask,
            params_used,
            warnings,
        )

    try:
        artifact_mask = detect_artifacts(
            _numeric_series(
                cleaned[y_column]
            ).to_numpy(),
            z_thresh=config.artifact_z_thresh,
        )

    except ValueError as error:
        warnings.append(
            f"Artifact detection skipped: {error}"
        )

        return CleanedResult(
            raw,
            cleaned,
            artifact_mask,
            params_used,
            warnings,
        )

    if artifact_mask.any():
        warnings.append(
            f"Flagged {int(artifact_mask.sum())} "
            "possible artifact(s)."
        )

    if (
        config.artifact_action == "interpolate"
        and artifact_mask.any()
    ):
        cleaned.loc[
            cleaned.index[artifact_mask],
            y_column,
        ] = np.nan

        cleaned = handle_missing_values(
            cleaned,
            col_map,
            method="interpolate",
        )

    elif (
        config.artifact_action == "drop"
        and artifact_mask.any()
    ):
        cleaned = cleaned.loc[
            ~artifact_mask
        ].copy()

    elif config.artifact_action != "flag":
        warnings.append(
            "Unknown artifact action; artifacts "
            "were only flagged."
        )

    if config.smooth and y_column in cleaned.columns:
        try:
            cleaned[y_column] = smooth_spectrum(
                _numeric_series(
                    cleaned[y_column]
                ).to_numpy(),
                window=config.smoothing_window,
                polyorder=config.smoothing_polyorder,
            )

        except ValueError as error:
            warnings.append(
                f"Smoothing skipped: {error}"
            )

    return CleanedResult(
        raw,
        cleaned,
        artifact_mask,
        params_used,
        warnings,
    )