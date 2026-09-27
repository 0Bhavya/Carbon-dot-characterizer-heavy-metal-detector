import numpy as np

from core.heavy_metal.detection_model import train_detection_model
from core.heavy_metal.feature_extraction import FEATURE_ORDER
from core.heavy_metal.model_registry import LoadedModel
from core.xai.shap_explainer import (
    explain_prediction,
    get_explainer,
    model_performance_summary,
)


def _training_data():
    features = np.array(
        [
            [0.01, 0.0, 0.99, 32.0, 0.10, 2.9],
            [0.02, -0.1, 1.01, 33.0, 0.08, 2.8],
            [0.00, 0.1, 1.00, 31.5, 0.12, 3.0],
            [0.08, 2.0, 0.92, 35.0, 0.18, 3.2],
            [0.22, 6.0, 0.78, 39.0, 0.25, 3.6],
            [0.39, 11.0, 0.61, 45.0, 0.34, 4.1],
        ]
    )
    return features, np.array([0, 0, 0, 1, 1, 1])


def test_explain_prediction_returns_ordered_local_values():
    features, labels = _training_data()
    model, _ = train_detection_model(features, labels)
    loaded_model = LoadedModel(model, None, FEATURE_ORDER, "test", {})
    explainer = get_explainer(loaded_model)

    result = explain_prediction(explainer, features[-1:], FEATURE_ORDER)

    assert result.shap_values.shape == (len(FEATURE_ORDER),)
    assert result.feature_names == FEATURE_ORDER
    assert np.isfinite(result.shap_values).all()
    assert np.isfinite(result.base_value)
    assert get_explainer(loaded_model) is explainer


def test_model_performance_summary_preserves_metrics():
    summary = model_performance_summary("detection", {"accuracy": 0.9})

    assert summary == {"model_type": "detection", "metrics": {"accuracy": 0.9}}