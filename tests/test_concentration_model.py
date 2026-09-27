import numpy as np
import pytest

from core.heavy_metal.concentration_model import (
    predict_concentration,
    train_concentration_model,
)


def _training_data():
    features = np.array(
        [
            [0.08, 2.0, 0.92, 35.0, 0.18, 3.2],
            [0.14, 4.0, 0.86, 37.0, 0.21, 3.4],
            [0.22, 6.0, 0.78, 39.0, 0.25, 3.6],
            [0.30, 8.0, 0.70, 42.0, 0.29, 3.9],
            [0.39, 11.0, 0.61, 45.0, 0.34, 4.1],
            [0.45, 13.0, 0.55, 48.0, 0.38, 4.3],
        ]
    )
    concentrations = np.array([1.0, 2.0, 5.0, 7.0, 10.0, 12.0])
    return features, concentrations


def test_train_and_predict_concentration():
    features, concentrations = _training_data()

    model, metrics = train_concentration_model(features, concentrations)
    result = predict_concentration(model, features[2:3])

    assert np.isfinite(result.value)
    assert result.uncertainty >= 0.0
    assert set(metrics) >= {"rmse", "mae", "r2", "cv_folds"}
    assert metrics["cv_folds"] == 5


def test_training_rejects_non_finite_targets():
    features, concentrations = _training_data()
    concentrations[0] = np.nan

    with pytest.raises(ValueError, match="finite"):
        train_concentration_model(features, concentrations)


def test_prediction_requires_trained_uncertainty():
    features, concentrations = _training_data()
    model, _ = train_concentration_model(features, concentrations)
    del model.cv_rmse_

    with pytest.raises(ValueError, match="cv_rmse_"):
        predict_concentration(model, features[0:1])