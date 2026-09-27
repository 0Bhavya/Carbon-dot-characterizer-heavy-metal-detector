from pathlib import Path

import pytest
from sklearn.dummy import DummyClassifier

from core.heavy_metal.config import FEATURE_ORDER
from core.heavy_metal.model_registry import load_model, list_versions, save_model


def test_save_list_and_load_model(tmp_path: Path):
    model = DummyClassifier(strategy="prior")
    artifact_path = save_model(
        "detection",
        model,
        version="v1.0.0",
        scaler="saved-scaler",
        metrics={"accuracy": 0.9},
        artifact_directory=tmp_path,
    )

    loaded = load_model("detection", artifact_directory=tmp_path)

    assert artifact_path == tmp_path / "detection" / "v1.0.0.pkl"
    assert list_versions("detection", tmp_path) == ["v1.0.0"]
    assert loaded.version == "v1.0.0"
    assert loaded.scaler == "saved-scaler"
    assert loaded.feature_order == FEATURE_ORDER
    assert loaded.metrics == {"accuracy": 0.9}


def test_latest_loads_highest_version(tmp_path: Path):
    model = DummyClassifier(strategy="prior")
    save_model("detection", model, "v1.0.0", artifact_directory=tmp_path)
    save_model("detection", model, "v1.1.0", artifact_directory=tmp_path)

    loaded = load_model("detection", artifact_directory=tmp_path)

    assert loaded.version == "v1.1.0"


def test_registry_rejects_unknown_model_type(tmp_path: Path):
    with pytest.raises(ValueError, match="Unsupported model_type"):
        list_versions("unknown", tmp_path)