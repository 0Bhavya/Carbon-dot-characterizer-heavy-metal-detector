import numpy as np
import pytest

from core.heavy_metal.identification_model import (
    predict_identification,
    train_identification_model,
)


def _training_data():
    features = np.array(
        [
            [0.08, 2.0, 0.92, 35.0, 0.18, 3.2],
            [0.22, 6.0, 0.78, 39.0, 0.25, 3.6],
            [0.39, 11.0, 0.61, 45.0, 0.34, 4.1],
            [0.10, -2.0, 0.90, 34.0, -0.16, 3.1],
            [0.27, -5.0, 0.73, 38.0, -0.24, 3.5],
            [0.45, -11.0, 0.55, 43.0, -0.31, 4.0],
        ]
    )
    labels = np.array(["Pb", "Pb", "Pb", "Hg", "Hg", "Hg"])
    return features, labels


def test_train_and_predict_identification():
    features, labels = _training_data()

    model, metrics = train_identification_model(features, labels, ["Pb", "Hg"])
    result = predict_identification(model, features[0:1], threshold=0.6)

    assert result.metal in {"Pb", "Hg"}
    assert set(result.probabilities) == {"Pb", "Hg"}
    assert 0.0 <= result.confidence <= 1.0
    assert result.is_confident is True
    assert metrics["cv_folds"] == 3
    assert len(metrics["confusion_matrix"]) == 2


def test_prediction_can_be_marked_inconclusive():
    features, labels = _training_data()
    model, _ = train_identification_model(features, labels, ["Pb", "Hg"])

    result = predict_identification(model, features[0:1], threshold=1.0)

    assert result.is_confident is False


def test_training_rejects_unknown_labels():
    features, _ = _training_data()

    with pytest.raises(ValueError, match="belong to metal_classes"):
        train_identification_model(features, np.array(["Pb", "Hg", "Zn", "Pb", "Hg", "Zn"]), ["Pb", "Hg"])