"""Multiclass heavy-metal identification model training and inference."""

from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from core.heavy_metal.detection_model import _build_model


@dataclass(frozen=True)
class IdentificationResult:
    """One metal prediction and its probability distribution."""

    metal: str
    confidence: float
    probabilities: dict[str, float]
    is_confident: bool


def _validate_training_data(
    X: np.ndarray,
    y: np.ndarray,
    metal_classes: list[str],
) -> tuple[np.ndarray, np.ndarray]:
    features = np.asarray(X, dtype=float)
    labels = np.asarray(y).astype(str)
    if features.ndim != 2 or features.shape[0] == 0:
        raise ValueError("X must be a non-empty two-dimensional feature matrix.")
    if labels.ndim != 1 or labels.shape[0] != features.shape[0]:
        raise ValueError("y must be one-dimensional and match the rows in X.")
    if not np.isfinite(features).all():
        raise ValueError("X contains non-finite feature values.")
    if not metal_classes or not set(labels).issubset(metal_classes):
        raise ValueError("Identification labels must belong to metal_classes.")
    if len(set(labels)) < 2:
        raise ValueError("Identification training requires at least two metal classes.")
    return features, labels


def train_identification_model(
    X: np.ndarray,
    y: np.ndarray,
    metal_classes: list[str],
    model_type: str = "random_forest",
) -> tuple[Any, dict[str, Any]]:
    """Train a multiclass detector and report stratified cross-validated metrics."""
    features, labels = _validate_training_data(X, y, metal_classes)
    class_counts = np.unique(labels, return_counts=True)[1]
    cv_folds = int(min(5, class_counts.min()))
    if cv_folds < 2:
        raise ValueError("Identification training requires at least two samples per class.")

    model = _build_model(model_type)
    splitter = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    predictions = cross_val_predict(model, features, labels, cv=splitter, method="predict")
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        labels=metal_classes,
        zero_division=0,
    )
    metrics: dict[str, Any] = {
        "accuracy": float(accuracy_score(labels, predictions)),
        "per_class": {
            metal: {
                "precision": float(precision[index]),
                "recall": float(recall[index]),
                "f1": float(f1[index]),
            }
            for index, metal in enumerate(metal_classes)
        },
        "confusion_matrix": confusion_matrix(
            labels,
            predictions,
            labels=metal_classes,
        ).tolist(),
        "metal_classes": list(metal_classes),
        "cv_folds": cv_folds,
    }
    model.fit(features, labels)
    return model, metrics


def predict_identification(
    model: Any,
    X: np.ndarray,
    threshold: float = 0.6,
) -> IdentificationResult:
    """Predict the most likely metal and flag probabilities below the threshold."""
    features = np.asarray(X, dtype=float)
    if features.ndim != 2 or features.shape[0] != 1:
        raise ValueError("Identification prediction expects exactly one feature row.")
    if not np.isfinite(features).all():
        raise ValueError("X contains non-finite feature values.")
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("Identification confidence threshold must be between 0 and 1.")

    probabilities_array = model.predict_proba(features)[0]
    classes = [str(label) for label in model.classes_]
    probabilities = {
        metal: float(probability)
        for metal, probability in zip(classes, probabilities_array)
    }
    best_index = int(np.argmax(probabilities_array))
    confidence = float(probabilities_array[best_index])
    return IdentificationResult(
        metal=classes[best_index],
        confidence=confidence,
        probabilities=probabilities,
        is_confident=confidence >= threshold,
    )