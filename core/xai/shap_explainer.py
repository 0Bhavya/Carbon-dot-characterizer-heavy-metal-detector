"""SHAP explanations for tree-based heavy-metal models."""

from dataclasses import dataclass
from typing import Any, Mapping

import numpy as np
import shap

from core.heavy_metal.model_registry import LoadedModel


@dataclass(frozen=True)
class LocalExplanation:
    """Feature contributions for one model prediction."""

    shap_values: np.ndarray
    feature_names: list[str]
    base_value: float


_EXPLAINER_CACHE: dict[str, shap.TreeExplainer] = {}


def get_explainer(loaded_model: LoadedModel) -> shap.TreeExplainer:
    """Build or reuse a cached TreeExplainer for a loaded model version."""
    cache_key = f"{loaded_model.version}:{id(loaded_model.model)}"
    if cache_key not in _EXPLAINER_CACHE:
        try:
            _EXPLAINER_CACHE[cache_key] = shap.TreeExplainer(loaded_model.model)
        except Exception as error:
            raise ValueError("The loaded model is not supported by SHAP TreeExplainer.") from error
    return _EXPLAINER_CACHE[cache_key]


def _select_output(values: Any, expected_value: Any) -> tuple[np.ndarray, float]:
    """Normalize SHAP's binary, multiclass, and regression output formats."""
    if isinstance(values, list):
        values = values[-1]
    values_array = np.asarray(values, dtype=float)
    if values_array.ndim == 3:
        values_array = values_array[:, :, -1]
    if values_array.ndim != 2 or values_array.shape[0] != 1:
        raise ValueError("SHAP explanation must contain exactly one sample.")

    expected_array = np.asarray(expected_value, dtype=float)
    if expected_array.ndim > 0:
        expected_array = expected_array.reshape(-1)
        base_value = float(expected_array[-1])
    else:
        base_value = float(expected_array)
    return values_array[0], base_value


def explain_prediction(
    explainer: shap.TreeExplainer,
    X_sample: np.ndarray,
    feature_names: list[str],
) -> LocalExplanation:
    """Explain one prediction and return ordered local SHAP contributions."""
    features = np.asarray(X_sample, dtype=float)
    if features.ndim != 2 or features.shape[0] != 1:
        raise ValueError("X_sample must contain exactly one feature row.")
    if not np.isfinite(features).all():
        raise ValueError("X_sample contains non-finite feature values.")
    if len(feature_names) != features.shape[1]:
        raise ValueError("feature_names must match the number of columns in X_sample.")

    explanation = explainer(features)
    shap_values, base_value = _select_output(explanation.values, explanation.base_values[0])
    if shap_values.shape[0] != len(feature_names):
        raise ValueError("SHAP output does not match feature_names.")
    return LocalExplanation(
        shap_values=shap_values,
        feature_names=list(feature_names),
        base_value=base_value,
    )


def model_performance_summary(model_type: str, metrics: Mapping[str, Any]) -> dict[str, Any]:
    """Return stored training metrics alongside the model type for XAI views."""
    return {"model_type": model_type, "metrics": dict(metrics)}