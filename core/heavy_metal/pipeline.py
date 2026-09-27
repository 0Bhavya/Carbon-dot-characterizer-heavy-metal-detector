"""End-to-end heavy-metal inference orchestration."""

from typing import Any

import numpy as np
import pandas as pd

from core.heavy_metal.config import FEATURE_ORDER, IDENTIFICATION_CONFIDENCE_THRESHOLD
from core.heavy_metal.detection_model import predict_detection
from core.heavy_metal.feature_extraction import extract_features, features_to_vector
from core.heavy_metal.identification_model import predict_identification
from core.heavy_metal.model_registry import LoadedModel, load_model
from core.heavy_metal.concentration_model import predict_concentration
from core.xai.shap_explainer import explain_prediction, get_explainer


def _apply_saved_scaler(features: np.ndarray, scaler: Any) -> np.ndarray:
    if scaler is None:
        return features
    return np.asarray(scaler.transform(features), dtype=float)


def _explain(loaded_model: LoadedModel, features: np.ndarray) -> dict[str, Any]:
    explanation = explain_prediction(
        get_explainer(loaded_model),
        features,
        loaded_model.feature_order,
    )
    return {
        "shap_values": explanation.shap_values,
        "feature_names": explanation.feature_names,
        "base_value": explanation.base_value,
    }


def run_heavy_metal_pipeline(
    dataframe: pd.DataFrame,
    artifact_directory: str | None = None,
    identification_threshold: float = IDENTIFICATION_CONFIDENCE_THRESHOLD,
) -> dict[str, Any]:
    """Run detection, conditional identification, concentration, and XAI for one row."""
    raw_features = features_to_vector(extract_features(dataframe), FEATURE_ORDER)
    detection_model = load_model("detection", artifact_directory=artifact_directory)
    detection_features = _apply_saved_scaler(raw_features, detection_model.scaler)
    is_detected, detection_confidence = predict_detection(
        detection_model.model,
        detection_features,
    )
    result: dict[str, Any] = {
        "detection_status": "detected" if is_detected else "not_detected",
        "detection_confidence": detection_confidence,
        "model_versions": {"detection": detection_model.version},
        "xai": {"detection": _explain(detection_model, detection_features)},
    }
    if not is_detected:
        return result

    identification_model = load_model(
        "identification",
        artifact_directory=artifact_directory,
    )
    identification_features = _apply_saved_scaler(raw_features, identification_model.scaler)
    identification = predict_identification(
        identification_model.model,
        identification_features,
        threshold=identification_threshold,
    )
    result["identification"] = identification
    result["model_versions"]["identification"] = identification_model.version
    result["xai"]["identification"] = _explain(
        identification_model,
        identification_features,
    )
    if not identification.is_confident:
        return result

    concentration_model = load_model(
        "concentration",
        artifact_directory=artifact_directory,
    )
    concentration_features = _apply_saved_scaler(raw_features, concentration_model.scaler)
    result["concentration"] = predict_concentration(
        concentration_model.model,
        concentration_features,
    )
    result["model_versions"]["concentration"] = concentration_model.version
    result["xai"]["concentration"] = _explain(
        concentration_model,
        concentration_features,
    )
    return result