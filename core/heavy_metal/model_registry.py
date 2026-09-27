"""Versioned persistence and loading for heavy-metal model artifacts."""

from dataclasses import dataclass
from pathlib import Path
import pickle
from typing import Any, Mapping

from core.heavy_metal.config import FEATURE_ORDER, MODEL_ARTIFACT_DIRECTORY


MODEL_TYPES = {"detection", "identification", "concentration"}


@dataclass(frozen=True)
class LoadedModel:
    """Model and metadata required by inference code."""

    model: Any
    scaler: Any
    feature_order: list[str]
    version: str
    metrics: dict[str, Any]


def _validate_model_type(model_type: str) -> None:
    if model_type not in MODEL_TYPES:
        allowed = ", ".join(sorted(MODEL_TYPES))
        raise ValueError(f"Unsupported model_type. Use one of: {allowed}.")


def _artifact_directory(artifact_directory: str | Path | None) -> Path:
    directory = Path(artifact_directory) if artifact_directory else MODEL_ARTIFACT_DIRECTORY
    return directory


def _artifact_path(model_type: str, version: str, artifact_directory: str | Path | None) -> Path:
    _validate_model_type(model_type)
    if not version or Path(version).name != version:
        raise ValueError("Model version must be a non-empty filename-safe value.")
    return _artifact_directory(artifact_directory) / model_type / f"{version}.pkl"


def save_model(
    model_type: str,
    model: Any,
    version: str,
    scaler: Any = None,
    feature_order: list[str] | None = None,
    metrics: Mapping[str, Any] | None = None,
    artifact_directory: str | Path | None = None,
) -> Path:
    """Persist a model and its inference metadata as one versioned artifact."""
    artifact_path = _artifact_path(model_type, version, artifact_directory)
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "model": model,
        "scaler": scaler,
        "feature_order": list(feature_order or FEATURE_ORDER),
        "version": version,
        "metrics": dict(metrics or {}),
    }
    with artifact_path.open("wb") as artifact_file:
        pickle.dump(payload, artifact_file, protocol=pickle.HIGHEST_PROTOCOL)
    return artifact_path


def list_versions(
    model_type: str,
    artifact_directory: str | Path | None = None,
) -> list[str]:
    """List available versions for a model type in ascending order."""
    _validate_model_type(model_type)
    directory = _artifact_directory(artifact_directory) / model_type
    if not directory.exists():
        return []
    return sorted(path.stem for path in directory.glob("*.pkl"))


def load_model(
    model_type: str,
    version: str = "latest",
    artifact_directory: str | Path | None = None,
) -> LoadedModel:
    """Load a versioned model artifact, resolving ``latest`` by version name."""
    selected_version = version
    if version == "latest":
        versions = list_versions(model_type, artifact_directory)
        if not versions:
            raise FileNotFoundError(f"No saved {model_type} model versions were found.")
        selected_version = versions[-1]

    artifact_path = _artifact_path(model_type, selected_version, artifact_directory)
    if not artifact_path.exists():
        raise FileNotFoundError(f"Model artifact does not exist: {artifact_path}")
    with artifact_path.open("rb") as artifact_file:
        payload = pickle.load(artifact_file)

    required_keys = {"model", "scaler", "feature_order", "version", "metrics"}
    if not required_keys.issubset(payload):
        raise ValueError(f"Model artifact is missing metadata: {sorted(required_keys - set(payload))}")
    return LoadedModel(
        model=payload["model"],
        scaler=payload["scaler"],
        feature_order=list(payload["feature_order"]),
        version=str(payload["version"]),
        metrics=dict(payload["metrics"]),
    )