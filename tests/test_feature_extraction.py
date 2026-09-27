import numpy as np
import pandas as pd
import pytest

from core.heavy_metal.config import FEATURE_ORDER
from core.heavy_metal.feature_extraction import dataframe_to_matrix, extract_features


def test_extract_features_uses_documented_feature_order():
    dataframe = pd.DataFrame(
        [{
            "baseline_intensity": 100.0,
            "response_intensity": 80.0,
            "baseline_peak_wavelength_nm": 450.0,
            "response_peak_wavelength_nm": 456.0,
            "response_peak_width_nm": 39.0,
            "spectral_skewness": 0.25,
            "spectral_kurtosis": 3.6,
        }]
    )

    features = extract_features(dataframe)
    matrix = dataframe_to_matrix(dataframe)

    assert features["delta_f_over_f0"] == pytest.approx(-0.2)
    assert features["emission_shift_nm"] == pytest.approx(6.0)
    assert matrix.shape == (1, len(FEATURE_ORDER))
    assert np.array_equal(matrix[0], [
        -0.2, 6.0, 0.8, 39.0, 0.25, 3.6,
    ])


def test_extract_features_rejects_zero_baseline():
    dataframe = pd.DataFrame([{
        "baseline_intensity": 0.0,
        "response_intensity": 80.0,
        "baseline_peak_wavelength_nm": 450.0,
        "response_peak_wavelength_nm": 456.0,
        "response_peak_width_nm": 39.0,
        "spectral_skewness": 0.25,
        "spectral_kurtosis": 3.6,
    }])

    with pytest.raises(ValueError, match="non-zero"):
        extract_features(dataframe)