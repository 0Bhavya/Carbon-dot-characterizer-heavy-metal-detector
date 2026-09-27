import numpy as np
import pytest

from core.heavy_metal.detection_model import predict_detection, train_detection_model


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
    labels = np.array([0, 0, 0, 1, 1, 1])
    return features, labels


def test_train_detection_model_returns_metrics_and_predicts():
    features, labels = _training_data()

    model, metrics = train_detection_model(features, labels)
    detected, confidence = predict_detection(model, features[-1:])

    assert detected is True
    assert 0.0 <= confidence <= 1.0
    assert set(metrics) >= {"accuracy", "precision", "recall", "f1", "roc_auc", "cv_folds"}
    assert metrics["cv_folds"] == 3


def test_training_rejects_single_class_labels():
    features, _ = _training_data()

    with pytest.raises(ValueError, match="both negative and positive"):
        train_detection_model(features, np.ones(features.shape[0], dtype=int))


def test_prediction_requires_one_row():
    features, labels = _training_data()
    model, _ = train_detection_model(features, labels)

    with pytest.raises(ValueError, match="exactly one feature row"):
        predict_detection(model, features)