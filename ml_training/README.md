# ML Training Data Contract

The repository currently contains only `sample_heavy_metal.csv`, which is explicitly synthetic demo data for pipeline testing. It must not be treated as real experimental evidence or used to report scientific model performance.

## One training sample

One row represents one fluorescence/sensing measurement for one sample under one metal/concentration condition. The demo rows contain summarized baseline and response values rather than raw spectra.

## Columns

Required target columns:

- `sample_id`: unique sample identifier.
- `metal_label`: metal identity, or `None` for a no-metal sample.
- `concentration`: concentration in the dataset's declared unit, ppm for the demo data.

Input columns used to derive features:

- `baseline_intensity`
- `response_intensity`
- `baseline_peak_wavelength_nm`
- `response_peak_wavelength_nm`
- `response_peak_width_nm`
- `spectral_skewness`
- `spectral_kurtosis`

`dataset_type` identifies the demo rows as `SYNTHETIC_DEMO`; it is metadata and is not a model feature.

## Targets

Detection labels are derived as follows:

- `0` when `metal_label == "None"`.
- `1` when `metal_label` is one of the configured supported metals.

Identification labels are the non-`None` values in `metal_label`. No-metal rows are excluded from the identification training subset.

Concentration targets are the numeric values in `concentration`. No-metal rows have concentration `0.0`; concentration training policy for those rows must be decided when the real dataset is available. For metal-specific calibration, use only rows for the identified metal.

## Feature interface

Archit's shared `extract_features(df, col_map)` function is the single source of truth for training and inference. Its output is a flat feature dictionary containing the PRD features:

1. `delta_f_over_f0`
2. `emission_shift_nm`
3. `intensity_ratio`
4. `peak_width`
5. `spectral_skewness`
6. `spectral_kurtosis`

`features_to_vector(features, feature_order)` converts that dictionary into the ordered NumPy model input. The required order is the list above and is centralized in `core.heavy_metal.config.FEATURE_ORDER`. Do not depend on CSV column order as a substitute for this feature order.

Archit's `preprocessing.py` and `feature_extraction.py` are not present in the current checkout. Therefore, the demo CSV is contract-shaped, but compatibility cannot yet be executed or confirmed against the actual implementation.

## Scaling lifecycle

At training time, fit the scaler on the training split only and persist it with the model metadata. `apply_scaler(X, scaler_path, fit=True)` is the specified training-time operation.

At inference time, load the persisted scaler and transform incoming vectors without fitting. Use `apply_scaler(X, scaler_path, fit=False)`. This prevents information leakage and train/inference distribution skew.

## Synthetic-data boundary

`SYNTHETIC_DEMO` values are deterministic placeholders designed to exercise file loading, feature extraction, target derivation, and pipeline wiring. They do not represent real carbon-dot fluorescence measurements, validated concentrations, instrument noise, or scientifically meaningful class boundaries.
