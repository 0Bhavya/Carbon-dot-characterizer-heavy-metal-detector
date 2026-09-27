"""Heavy-metal concentration regression training and inference."""

from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.svm import SVR


@dataclass(frozen=True)
class ConcentrationResult:
    """One concentration prediction and its estimated uncertainty."""

    value: float
    uncertainty: float


def _validate_training_data(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    features = np.asarray(X, dtype=float)
    targets = np.asarray(y, dtype=float)
    if features.ndim != 2 or features.shape[0] < 2:
        raise ValueError("X must be a two-dimensional matrix with at least two rows.")
    if targets.ndim != 1 or targets.shape[0] != features.shape[0]:
        raise ValueError("y must be one-dimensional and match the rows in X.")
    if not np.isfinite(features).all() or not np.isfinite(targets).all():
        raise ValueError("X and y must contain only finite values.")
    return features, targets


def _build_model(model_type: str) -> Any:
    if model_type == "random_forest":
        return RandomForestRegressor(
            n_estimators=200,
            random_state=42,
        )
    if model_type == "svr":
        return SVR()
    if model_type == "xgboost":
        try:
            from xgboost import XGBRegressor
        except ImportError as error:
            raise ValueError("xgboost is required for model_type='xgboost'.") from error
        return XGBRegressor(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            objective="reg:squarederror",
            random_state=42,
        )
    raise ValueError("Unsupported model_type. Use 'random_forest', 'xgboost', or 'svr'.")


def train_concentration_model(
    X: np.ndarray,
    y: np.ndarray,
    model_type: str = "random_forest",
) -> tuple[Any, dict[str, float | int]]:
    """Train a concentration regressor and report cross-validated metrics."""
    features, targets = _validate_training_data(X, y)
    cv_folds = min(5, features.shape[0])
    model = _build_model(model_type)
    splitter = KFold(n_splits=cv_folds, shuffle=True, random_state=42)
    predictions = cross_val_predict(model, features, targets, cv=splitter)

    rmse = float(np.sqrt(mean_squared_error(targets, predictions)))
    metrics: dict[str, float | int] = {
        "rmse": rmse,
        "mae": float(mean_absolute_error(targets, predictions)),
        "r2": float(r2_score(targets, predictions)),
        "cv_folds": cv_folds,
    }
    model.fit(features, targets)
    model.cv_rmse_ = rmse
    return model, metrics


def predict_concentration(model: Any, X: np.ndarray) -> ConcentrationResult:
    """Predict concentration and use cross-validated RMSE as uncertainty."""
    features = np.asarray(X, dtype=float)
    if features.ndim != 2 or features.shape[0] != 1:
        raise ValueError("Concentration prediction expects exactly one feature row.")
    if not np.isfinite(features).all():
        raise ValueError("X contains non-finite feature values.")
    if not hasattr(model, "cv_rmse_"):
        raise ValueError("Model is missing cv_rmse_; train it with train_concentration_model first.")

    value = float(model.predict(features)[0])
    return ConcentrationResult(value=value, uncertainty=float(model.cv_rmse_))