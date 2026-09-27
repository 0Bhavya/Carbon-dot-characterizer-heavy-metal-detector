"""Binary heavy-metal detection model training and inference."""

from typing import Any

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict


def _validate_training_data(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    features = np.asarray(X, dtype=float)
    labels = np.asarray(y, dtype=int)
    if features.ndim != 2 or features.shape[0] == 0:
        raise ValueError("X must be a non-empty two-dimensional feature matrix.")
    if labels.ndim != 1 or labels.shape[0] != features.shape[0]:
        raise ValueError("y must be one-dimensional and match the rows in X.")
    if not np.isfinite(features).all():
        raise ValueError("X contains non-finite feature values.")
    if not np.isin(labels, [0, 1]).all():
        raise ValueError("Detection labels must contain only 0 and 1.")
    if np.unique(labels).size != 2:
        raise ValueError("Detection training requires both negative and positive samples.")
    return features, labels


def _build_model(model_type: str) -> Any:
    if model_type == "random_forest":
        return RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=42,
        )
    if model_type == "xgboost":
        try:
            from xgboost import XGBClassifier
        except ImportError as error:
            raise ValueError("xgboost is required for model_type='xgboost'.") from error
        return XGBClassifier(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            eval_metric="logloss",
            random_state=42,
        )
    raise ValueError("Unsupported model_type. Use 'random_forest' or 'xgboost'.")


def train_detection_model(
    X: np.ndarray,
    y: np.ndarray,
    model_type: str = "random_forest",
) -> tuple[Any, dict[str, float | int]]:
    """Train a binary detector and report stratified cross-validated metrics."""
    features, labels = _validate_training_data(X, y)
    class_counts = np.bincount(labels, minlength=2)
    cv_folds = int(min(5, class_counts.min()))
    if cv_folds < 2:
        raise ValueError("Detection training requires at least two samples per class.")

    model = _build_model(model_type)
    splitter = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    predictions = cross_val_predict(model, features, labels, cv=splitter, method="predict")
    probabilities = cross_val_predict(
        model,
        features,
        labels,
        cv=splitter,
        method="predict_proba",
    )[:, 1]

    metrics: dict[str, float | int] = {
        "accuracy": float(accuracy_score(labels, predictions)),
        "precision": float(precision_score(labels, predictions, zero_division=0)),
        "recall": float(recall_score(labels, predictions, zero_division=0)),
        "f1": float(f1_score(labels, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(labels, probabilities)),
        "cv_folds": cv_folds,
    }
    model.fit(features, labels)
    return model, metrics


def predict_detection(model: Any, X: np.ndarray) -> tuple[bool, float]:
    """Predict metal presence and return the positive-class probability."""
    features = np.asarray(X, dtype=float)
    if features.ndim != 2 or features.shape[0] != 1:
        raise ValueError("Detection prediction expects exactly one feature row.")
    if not np.isfinite(features).all():
        raise ValueError("X contains non-finite feature values.")

    probability = float(model.predict_proba(features)[0, 1])
    return bool(probability >= 0.5), probability