from pathlib import Path

import pandas as pd

from core.heavy_metal.pipeline import run_heavy_metal_pipeline
from ml_training.train_concentration import train_concentration
from ml_training.train_detection import train_detection
from ml_training.train_identification import train_identification


DATASET_PATH = Path("ml_training/datasets/sample_heavy_metal.csv")


def test_pipeline_runs_all_prediction_stages(tmp_path: Path):
    train_detection(DATASET_PATH, version="test", artifact_directory=tmp_path)
    train_identification(DATASET_PATH, version="test", artifact_directory=tmp_path)
    train_concentration(DATASET_PATH, version="test", artifact_directory=tmp_path)
    dataframe = pd.read_csv(DATASET_PATH).iloc[[5]]

    result = run_heavy_metal_pipeline(dataframe, artifact_directory=str(tmp_path))

    assert result["detection_status"] == "detected"
    assert result["identification"].metal in {"Pb", "Hg", "Cd", "Cr", "Cu"}
    assert "detection" in result["xai"]
    assert "identification" in result["xai"]
    if result["identification"].is_confident:
        assert "concentration" in result
        assert "concentration" in result["xai"]


def test_pipeline_returns_without_later_models_for_no_metal(tmp_path: Path):
    train_detection(DATASET_PATH, version="test", artifact_directory=tmp_path)
    train_identification(DATASET_PATH, version="test", artifact_directory=tmp_path)
    train_concentration(DATASET_PATH, version="test", artifact_directory=tmp_path)
    dataframe = pd.read_csv(DATASET_PATH).iloc[[0]]

    result = run_heavy_metal_pipeline(dataframe, artifact_directory=str(tmp_path))

    assert result["detection_status"] == "not_detected"
    assert "identification" not in result
    assert "concentration" not in result