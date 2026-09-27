import streamlit as st
import pandas as pd


import streamlit as st
import pandas as pd

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
    except (pd.errors.ParserError, ValueError, OSError) as error:
        st.error(f"The dataset could not be previewed: {error}")


st.header("Dataset Validation")
st.caption("Validation results will be supplied by the dataset validation module.")

with st.container(border=True):
    validation_row1_col1, validation_row1_col2 = st.columns(2)

    with validation_row1_col1:
        st.metric("Dataset validity", "Pending validation")

    with validation_row1_col2:
        st.metric("Detected columns", "Pending validation")

    validation_row2_col1, validation_row2_col2 = st.columns(2)

    with validation_row2_col1:
        st.metric("Missing values", "Pending validation")

    with validation_row2_col2:
        st.metric("Fluorescence data readiness", "Pending validation")


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

    # Integration point: call fluorescence preprocessing function from another module
    if st.button("Run Heavy Metal Detection", type="primary"):
        # Integration point: call heavy metal detection model
        st.info(
            f"Detection is ready for the {detection_mode.lower()} mode"
            + (" with advanced analysis." if advanced_analysis else ".")
        )
        st.info("Results will appear after the detection module is integrated.")


st.header("Heavy Metal Detection Results")

result_col1, result_col2 = st.columns(2)

with result_col1:
    st.metric("Detection status", "Not run")
    st.metric("Prediction confidence", "Pending")
    st.metric("Concentration uncertainty", "Pending")

with result_col2:
    st.metric("Identified heavy metal", "Pending")
    st.metric("Estimated concentration", "Pending")

st.info("Results will appear after the detection module is integrated.")


st.header("Visualization")

with st.container(border=True):
    st.info("Detection visualizations will appear after the visualization module is integrated.")

# Integration point: display Plotly detection figure returned by visualization module
# Example:
# st.plotly_chart(detection_figure, use_container_width=True)


st.header("Explainable AI Results")
xai_columns = st.columns(3)
xai_placeholders = [
    ("Feature importance", "Pending XAI results"),
    ("SHAP explanation", "Pending XAI results"),
    ("Important contributing features", "Pending XAI results"),
]
for column, (label, value) in zip(xai_columns, xai_placeholders):
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
        st.info("Detection result export will be available after reporting integration.")
with export_columns[2]:
    if st.button("Generate Detection Report", use_container_width=True):
        st.info("Report generation will be available after reporting integration.")
