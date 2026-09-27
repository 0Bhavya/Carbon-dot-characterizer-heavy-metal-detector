"""Shared helpers for offline heavy-metal model training scripts."""

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from core.heavy_metal.feature_extraction import dataframe_to_matrix
from core.heavy_metal.model_registry import save_model
from ml_training.dataset import derive_training_targets, load_training_dataset


DEFAULT_DATASET = Path(__file__).resolve().parent / "datasets" / "sample_heavy_metal.csv"


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--dataset", dest="dataset_path", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--version", default="v1.0.0")
    parser.add_argument("--model-type", default="random_forest")
    parser.add_argument("--artifact-directory", type=Path, default=None)


def train_from_dataset(
    dataset_path: Path,
    model_type: str,
    version: str,
    artifact_directory: Path | None,
    trainer: Callable[..., tuple[Any, dict[str, Any]]],
    target_selector: Callable[[Any], tuple[Any, Any]],
    registry_model_type: str,
) -> dict[str, Any]:
    dataframe = load_training_dataset(dataset_path)
    features = dataframe_to_matrix(dataframe)
    targets = derive_training_targets(dataframe)
    selected_features, selected_targets = target_selector((features, targets))
    model, metrics = trainer(selected_features, selected_targets, model_type=model_type)
    save_model(
        registry_model_type,
        model,
        version=version,
        feature_order=None,
        metrics=metrics,
        artifact_directory=artifact_directory,
    )
    return metrics


def print_metrics(metrics: dict[str, Any]) -> None:
    print(json.dumps(metrics, indent=2, default=str))