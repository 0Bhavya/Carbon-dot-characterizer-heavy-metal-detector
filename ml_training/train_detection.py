"""Train and persist the binary heavy-metal detection model."""

import argparse
from pathlib import Path

from core.heavy_metal.detection_model import train_detection_model
from ml_training.training_utils import add_common_arguments, print_metrics, train_from_dataset


def train_detection(
    dataset_path: Path,
    version: str = "v1.0.0",
    model_type: str = "random_forest",
    artifact_directory: Path | None = None,
) -> dict[str, float | int]:
    """Train detection using every row and persist its versioned artifact."""
    return train_from_dataset(
        dataset_path,
        model_type,
        version,
        artifact_directory,
        train_detection_model,
        lambda data: (data[0], data[1].detection),
        "detection",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_arguments(parser)
    arguments = parser.parse_args()
    print_metrics(train_detection(**vars(arguments)))


if __name__ == "__main__":
    main()