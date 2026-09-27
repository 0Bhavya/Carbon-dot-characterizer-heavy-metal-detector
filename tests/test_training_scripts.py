from pathlib import Path

from ml_training.train_concentration import train_concentration
from ml_training.train_detection import train_detection
from ml_training.train_identification import train_identification
from core.heavy_metal.model_registry import list_versions, load_model


DATASET_PATH = Path("ml_training/datasets/sample_heavy_metal.csv")


def test_training_scripts_persist_all_model_types(tmp_path: Path):
    detection_metrics = train_detection(DATASET_PATH, version="test", artifact_directory=tmp_path)
    identification_metrics = train_identification(
        DATASET_PATH,
        version="test",
        artifact_directory=tmp_path,
    )
    concentration_metrics = train_concentration(
        DATASET_PATH,
        version="test",
        artifact_directory=tmp_path,
    )

    assert detection_metrics["cv_folds"] == 3
    assert identification_metrics["cv_folds"] == 3
    assert concentration_metrics["cv_folds"] == 5
    assert list_versions("detection", tmp_path) == ["test"]
    assert list_versions("identification", tmp_path) == ["test"]
    assert list_versions("concentration", tmp_path) == ["test"]
    assert load_model("detection", "test", tmp_path).feature_order