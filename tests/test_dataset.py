import pandas as pd
import pytest

from ml_training.dataset import derive_training_targets, load_training_dataset


DATASET_PATH = "ml_training/datasets/sample_heavy_metal.csv"


def test_demo_dataset_loads_and_derives_targets():
    dataframe = load_training_dataset(DATASET_PATH)

    targets = derive_training_targets(dataframe)

    assert len(dataframe) == 18
    assert targets.detection.tolist().count(0) == 3
    assert targets.detection.tolist().count(1) == 15
    assert set(targets.identification) == {"Pb", "Hg", "Cd", "Cr", "Cu"}
    assert targets.concentration.min() == 0.0


def test_loader_rejects_duplicate_sample_ids(tmp_path):
    dataframe = pd.read_csv(DATASET_PATH)
    dataframe.loc[1, "sample_id"] = dataframe.loc[0, "sample_id"]
    dataset_path = tmp_path / "duplicate.csv"
    dataframe.to_csv(dataset_path, index=False)

    with pytest.raises(ValueError, match="duplicate sample_id"):
        load_training_dataset(dataset_path)


def test_loader_rejects_unsupported_metals(tmp_path):
    dataframe = pd.read_csv(DATASET_PATH)
    dataframe.loc[0, "metal_label"] = "Fe"
    dataset_path = tmp_path / "unsupported.csv"
    dataframe.to_csv(dataset_path, index=False)

    with pytest.raises(ValueError, match="Unsupported metal_label"):
        load_training_dataset(dataset_path)