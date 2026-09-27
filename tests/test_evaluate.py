from pathlib import Path

import pytest

from ml_training.evaluate import evaluate_dataset


DATASET_PATH = Path("ml_training/datasets/sample_heavy_metal.csv")


def test_evaluate_dataset_reports_holdout_metrics():
    report = evaluate_dataset(DATASET_PATH)

    assert set(report) >= {
        "dataset",
        "model_type",
        "test_size",
        "detection",
        "identification",
        "concentration",
    }
    assert report["detection"]["test_samples"] > 0
    assert report["identification"]["test_samples"] > 0
    assert report["concentration"]["test_samples"] > 0
    assert 0.0 <= report["detection"]["accuracy"] <= 1.0
    assert 0.0 <= report["identification"]["accuracy"] <= 1.0


def test_evaluate_rejects_invalid_test_size():
    with pytest.raises(ValueError, match="test_size"):
        evaluate_dataset(DATASET_PATH, test_size=1.0)