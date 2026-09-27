import sys
from pathlib import Path

import streamlit as st
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.heavy_metal.pipeline import run_heavy_metal_pipeline
from core.heavy_metal.feature_extraction import DEFAULT_COLUMN_MAP
from core.reporting.heavy_metal_report import export_predictions_json, generate_heavy_metal_pdf
from styles import load_css


st.set_page_config(
    page_title="Heavy Metal Detection",
    page_icon="⚗️",
    layout="wide",
)

load_css()

st.markdown(
    """
    <style>
    div[data-testid="stFileUploader"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 0.65rem 0.9rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    div[data-testid="stFileUploader"] > label {
        color: #0F172A;
        font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        padding: 0.8rem 0.9rem;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        overflow: hidden;
        background: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================
# PAGE HERO
# =========================================

st.markdown(
    """
<div class="page-hero">
<div class="page-hero-tag">⚗️ HEAVY METAL DETECTION MODULE</div>
<div class="page-hero-title">Heavy Metal Detection</div>
<div class="page-hero-subtitle">
Upload carbon dot fluorescence experiment data and analyze the presence,
concentration, and characteristics of heavy metal contaminants using
AI-powered detection methods.
</div>
</div>
""",
    unsafe_allow_html=True,
)


st.subheader("Upload Data")
preview_data = None
selected_row = None
selected_sample = None
with st.container(border=True):
    uploaded_file = st.file_uploader(
        "Upload fluorescence experiment data",
        type=["csv", "xlsx", "xls"],
    )

if uploaded_file is not None:
    st.info(f"File loaded: {uploaded_file.name}")

    try:
        if uploaded_file.name.lower().endswith(".csv"):
            preview_data = pd.read_csv(uploaded_file)
        else:
            preview_data = pd.read_excel(uploaded_file)

        st.subheader("Dataset preview")
        with st.container(border=True):
            st.dataframe(preview_data.head(), use_container_width=True)

        rows, columns = preview_data.shape

        preview_metric_col1, preview_metric_col2 = st.columns(2)
        with preview_metric_col1:
            st.metric("Total Rows", rows)
        with preview_metric_col2:
            st.metric("Total Columns", columns)

        if "sample_id" in preview_data.columns:
            selected_sample = st.selectbox(
                "Measurement to analyze",
                preview_data["sample_id"].astype(str).tolist(),
            )
            selected_row = preview_data[
                preview_data["sample_id"].astype(str) == selected_sample
            ].iloc[[0]]
        else:
            selected_row = preview_data.iloc[[0]]
            st.caption("No sample_id column found; the first measurement will be analyzed.")
    except (pd.errors.ParserError, ValueError, OSError) as error:
        st.error(f"The dataset could not be previewed: {error}")


st.header("Dataset Validation")
st.caption("Validation results will be supplied by the dataset validation module.")

with st.container(border=True):
    validation_row1_col1, validation_row1_col2 = st.columns(2)

    with validation_row1_col1:
        st.metric("Dataset validity", "Ready" if preview_data is not None else "Awaiting upload")

    with validation_row1_col2:
        st.metric(
            "Detected columns",
            len(preview_data.columns) if preview_data is not None else "Pending",
        )

    validation_row2_col1, validation_row2_col2 = st.columns(2)

    with validation_row2_col1:
        st.metric(
            "Missing values",
            int(preview_data.isna().sum().sum()) if preview_data is not None else "Pending",
        )

    with validation_row2_col2:
        required_feature_columns = set(DEFAULT_COLUMN_MAP.values())
        missing_feature_columns = (
            required_feature_columns - set(preview_data.columns)
            if preview_data is not None
            else required_feature_columns
        )
        ready = selected_row is not None and not missing_feature_columns
        st.metric("Fluorescence data readiness", "Ready" if ready else "Needs review")

    if preview_data is not None and missing_feature_columns:
        st.warning(
            "Missing required fluorescence columns: "
            + ", ".join(sorted(missing_feature_columns))
        )


st.markdown(
    """
    <style>
    div[data-testid="stSelectbox"] {
        margin-bottom: 0.5rem;
    }

    div[data-testid="stCheckbox"] {
        margin-top: 0.25rem;
        margin-bottom: 0.75rem;
    }

    div[data-testid="stButton"] button {
        margin-top: 0.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.header("Detection Controls")
with st.container(border=True):
    detection_mode = st.selectbox(
        "Detection analysis mode",
        ["Standard detection", "Comparative analysis", "Batch analysis"],
    )
    advanced_analysis = st.checkbox("Enable optional advanced analysis")

    if st.button("Run Heavy Metal Detection", type="primary"):
        if selected_row is None:
            st.error("Upload a valid fluorescence dataset before running detection.")
        else:
            try:
                st.session_state["heavy_metal_results"] = run_heavy_metal_pipeline(
                    selected_row,
                )
                st.session_state["heavy_metal_sample_id"] = selected_sample if "sample_id" in preview_data.columns else "first-row"
                st.success(
                    f"Detection completed in {detection_mode.lower()} mode"
                    + (" with advanced analysis." if advanced_analysis else ".")
                )
            except FileNotFoundError:
                st.error(
                    "No trained model artifacts are available. Run the three "
                    "ml_training scripts and deploy the generated models/ directory."
                )
            except (ValueError, TypeError) as error:
                st.error(f"Detection could not be completed: {error}")


st.header("Heavy Metal Detection Results")

result_col1, result_col2 = st.columns(2)
results = st.session_state.get("heavy_metal_results")
identification = results.get("identification") if results else None
concentration = results.get("concentration") if results else None

with result_col1:
    st.metric("Detection status", results.get("detection_status", "Not run") if results else "Not run")
    st.metric(
        "Prediction confidence",
        f"{results['detection_confidence']:.1%}" if results else "Pending",
    )
    st.metric(
        "Concentration uncertainty",
        f"{concentration.uncertainty:.3g}" if concentration else "N/A",
    )

with result_col2:
    st.metric("Identified heavy metal", identification.metal if identification else "N/A")
    st.metric(
        "Estimated concentration",
        f"{concentration.value:.3g}" if concentration else "N/A",
    )

if identification and not identification.is_confident:
    st.warning("Identification confidence is below the configured threshold; result is inconclusive.")
elif not results:
    st.info("Run detection to view model results.")


st.header("Visualization")

with st.container(border=True):
    if results:
        st.json({"model_versions": results["model_versions"]})
    else:
        st.info("Run detection to view model information.")

# Integration point: display Plotly detection figure returned by visualization module
# Example:
# st.plotly_chart(detection_figure, use_container_width=True)


st.header("Explainable AI Results")
xai_columns = st.columns(3)
if results:
    detection_xai = results["xai"]["detection"]
    top_features = sorted(
        zip(detection_xai["feature_names"], detection_xai["shap_values"]),
        key=lambda item: abs(float(item[1])),
        reverse=True,
    )[:3]
    xai_values = [
        ("Feature importance", top_features[0][0]),
        ("SHAP base value", f"{detection_xai['base_value']:.4g}"),
        ("Important contributing features", ", ".join(name for name, _ in top_features)),
    ]
else:
    xai_values = [
        ("Feature importance", "Run detection first"),
        ("SHAP explanation", "Run detection first"),
        ("Important contributing features", "Run detection first"),
    ]
for column, (label, value) in zip(xai_columns, xai_values):
    with column:
        with st.container(border=True):
            st.subheader(label)
            st.info(value)
# Integration point: display SHAP results returned by XAI module


st.header("Save and Export")
export_columns = st.columns(3)
with export_columns[0]:
    if st.button("Save Experiment", use_container_width=True):
        # Integration point: save experiment using database CRUD function
        st.info("Experiment saving will be available after database integration.")
with export_columns[1]:
    if st.button("Export Detection Results", use_container_width=True):
        if results:
            st.download_button(
                "Download Detection JSON",
                data=export_predictions_json(results, results.get("xai", {})).getvalue(),
                file_name="heavy_metal_prediction.json",
                mime="application/json",
                key="download_detection_json",
            )
        else:
            st.warning("Run detection before exporting results.")
with export_columns[2]:
    if st.button("Generate Detection Report", use_container_width=True):
        if results:
            st.download_button(
                "Download Detection Report",
                data=generate_heavy_metal_pdf(results).getvalue(),
                file_name="heavy_metal_detection_report.pdf",
                mime="application/pdf",
                key="download_detection_report",
            )
        else:
            st.warning("Run detection before generating a report.")
