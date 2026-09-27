"""Train and persist the multiclass heavy-metal identification model."""

import argparse
from pathlib import Path

from core.heavy_metal.config import SUPPORTED_METALS
from core.heavy_metal.identification_model import train_identification_model
from ml_training.training_utils import add_common_arguments, print_metrics
from ml_training.dataset import derive_training_targets, load_training_dataset
from core.heavy_metal.feature_extraction import dataframe_to_matrix
from core.heavy_metal.model_registry import save_model


def train_identification(
    dataset_path: Path,
    version: str = "v1.0.0",
    model_type: str = "random_forest",
    artifact_directory: Path | None = None,
) -> dict[str, object]:
    """Train identification on metal-containing rows and persist its artifact."""
    dataframe = load_training_dataset(dataset_path)
    targets = derive_training_targets(dataframe)
    features = dataframe_to_matrix(dataframe)[targets.identification_mask]
    model, metrics = train_identification_model(
        features,
        targets.identification,
        SUPPORTED_METALS,
        model_type=model_type,
    )
    save_model(
        "identification",
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
    print_metrics(train_identification(**vars(arguments)))


if __name__ == "__main__":
    main()