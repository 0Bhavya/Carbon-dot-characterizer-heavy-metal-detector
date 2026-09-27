"""Train and persist the heavy-metal concentration regression model."""

import argparse
from pathlib import Path

from core.heavy_metal.concentration_model import train_concentration_model
from core.heavy_metal.feature_extraction import dataframe_to_matrix
from core.heavy_metal.model_registry import save_model
from ml_training.dataset import derive_training_targets, load_training_dataset
from ml_training.training_utils import add_common_arguments, print_metrics


def train_concentration(
    dataset_path: Path,
    version: str = "v1.0.0",
    model_type: str = "random_forest",
    artifact_directory: Path | None = None,
) -> dict[str, float | int]:
    """Train concentration on metal-containing rows and persist its artifact."""
    dataframe = load_training_dataset(dataset_path)
    targets = derive_training_targets(dataframe)
    features = dataframe_to_matrix(dataframe)[targets.identification_mask]
    concentrations = targets.concentration[targets.identification_mask]
    model, metrics = train_concentration_model(
        features,
        concentrations,
        model_type=model_type,
    )
    save_model(
        "concentration",
        model,
        version=version,
        metrics=metrics,
        artifact_directory=artifact_directory,
    )
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_arguments(parser)
    arguments = parser.parse_args()
    print_metrics(train_concentration(**vars(arguments)))


if __name__ == "__main__":
    main()