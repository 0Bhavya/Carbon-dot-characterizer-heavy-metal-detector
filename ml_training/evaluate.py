"""Evaluate the ML training pipeline on a held-out dataset split."""

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

from core.heavy_metal.concentration_model import train_concentration_model
from core.heavy_metal.detection_model import train_detection_model
from core.heavy_metal.feature_extraction import dataframe_to_matrix
from core.heavy_metal.identification_model import train_identification_model
from core.heavy_metal.config import SUPPORTED_METALS
from ml_training.dataset import derive_training_targets, load_training_dataset
from ml_training.training_utils import DEFAULT_DATASET


def _split_indices(
    indices: np.ndarray,
    labels: np.ndarray | None = None,
    test_size: float = 0.33,
) -> tuple[np.ndarray, np.ndarray]:
    """Create a reproducible split, stratifying when class labels are available."""
    return train_test_split(
        indices,
        test_size=test_size,
        random_state=42,
        stratify=labels,
    )


def evaluate_dataset(
    dataset_path: str | Path = DEFAULT_DATASET,
    model_type: str = "random_forest",
    test_size: float = 0.33,
) -> dict[str, Any]:
    """Train on one split and report metrics only on its unseen holdout rows."""
    if not 0.0 < test_size < 1.0:
        raise ValueError("test_size must be between 0 and 1.")

    dataframe = load_training_dataset(dataset_path)
    features = dataframe_to_matrix(dataframe)
    targets = derive_training_targets(dataframe)
    all_indices = np.arange(len(dataframe))

    detection_train, detection_test = _split_indices(
        all_indices,
        targets.detection,
        test_size,
    )
    detection_model, _ = train_detection_model(
        features[detection_train],
        targets.detection[detection_train],
        model_type=model_type,
    )
    detection_predictions = detection_model.predict(features[detection_test])
    detection_metrics = {
        "accuracy": float(accuracy_score(targets.detection[detection_test], detection_predictions)),
        "precision": float(
            precision_score(targets.detection[detection_test], detection_predictions, zero_division=0)
        ),
        "recall": float(
            recall_score(targets.detection[detection_test], detection_predictions, zero_division=0)
        ),
        "test_samples": int(len(detection_test)),
    }

    metal_indices = np.flatnonzero(targets.identification_mask)
    identification_train, identification_test = _split_indices(
        metal_indices,
        targets.identification,
        test_size,
    )
    identification_model, _ = train_identification_model(
        features[identification_train],
        dataframe["metal_label"].to_numpy()[identification_train],
        SUPPORTED_METALS,
        model_type=model_type,
    )
    identification_predictions = identification_model.predict(features[identification_test])
    identification_metrics = {
        "accuracy": float(
            accuracy_score(
                dataframe["metal_label"].to_numpy()[identification_test],
                identification_predictions,
            )
        ),
        "test_samples": int(len(identification_test)),
    }

    concentration_train, concentration_test = _split_indices(metal_indices, test_size=test_size)
    concentration_model, _ = train_concentration_model(
        features[concentration_train],
        targets.concentration[concentration_train],
        model_type=model_type,
    )
    concentration_predictions = concentration_model.predict(features[concentration_test])
    concentration_actual = targets.concentration[concentration_test]
    concentration_metrics = {
        "rmse": float(np.sqrt(mean_squared_error(concentration_actual, concentration_predictions))),
        "mae": float(mean_absolute_error(concentration_actual, concentration_predictions)),
        "r2": float(r2_score(concentration_actual, concentration_predictions)),
        "test_samples": int(len(concentration_test)),
    }

    return {
        "dataset": str(dataset_path),
        "model_type": model_type,
        "test_size": test_size,
        "detection": detection_metrics,
        "identification": identification_metrics,
        "concentration": concentration_metrics,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", dest="dataset_path", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--model-type", default="random_forest")
    parser.add_argument("--test-size", type=float, default=0.33)
    arguments = parser.parse_args()
    print(json.dumps(evaluate_dataset(**vars(arguments)), indent=2))


if __name__ == "__main__":
    main()