import streamlit as st
import pandas as pd

from styles import load_css


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Carbon Dot Characterization",
    page_icon="🧪",
    layout="wide",
)


# --------------------------------------------------
# LOAD GLOBAL CSS
# --------------------------------------------------

load_css()

st.markdown(
    """
    <style>
    .characterization-upload-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.07);
        padding: 22px 20px;
        margin: 0 0 18px 0;
    }

    .characterization-preview-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.07);
        padding: 22px 20px;
        margin: 0 0 18px 0;
    }

    .characterization-file-status {
        margin-top: 14px;
    }

    .characterization-preview-card {
        padding: 20px;
    }

    .characterization-preview-table {
        margin-top: 16px;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        overflow: hidden;
        background: #FFFFFF;
    }

    .characterization-metric-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 16px;
        margin-top: 18px;
    }

    .characterization-metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 16px;
    }

    .characterization-preview-divider {
        border-top: 1px solid #E2E8F0;
        margin: 18px 0 0 0;
    }

    .validation-section {
        margin-top: 10px;
    }

    .validation-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 18px;
        margin-top: 6px;
    }

    .validation-grid [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.07);
        padding: 18px 18px 16px;
        min-height: 170px;
        height: 100%;
        box-sizing: border-box;
    }

    .validation-grid [data-testid="stMetric"] {
        margin: 0;
    }

    .validation-grid [data-testid="stAlert"] {
        margin-top: 12px;
    }

    @media (max-width: 768px) {
        .validation-grid {
            grid-template-columns: 1fr;
            gap: 14px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# PAGE HERO
# --------------------------------------------------


st.markdown(
    """
<div class="page-hero">
<div class="page-hero-tag">🧪 CHARACTERIZATION MODULE</div>
<div class="page-hero-title">Carbon Dot Characterization</div>
<div class="page-hero-subtitle">Upload and analyze fluorescence or spectroscopy data to understand the physical and optical properties of carbon dots.</div>
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# DATA UPLOAD
# --------------------------------------------------

st.markdown("### Upload Data")

uploaded_file = st.file_uploader(
    "Upload spectroscopy or fluorescence data",
    type=["csv", "xlsx", "xls"],
)

if uploaded_file is not None:
    st.markdown(
        '<div class="characterization-file-status">',
        unsafe_allow_html=True,
    )
    st.success(f"File loaded: {uploaded_file.name}")
    st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

preview_data = None

if uploaded_file is not None:

    try:

        file_extension = uploaded_file.name.rsplit(".", 1)[-1].lower()

        if file_extension == "csv":
            preview_data = pd.read_csv(uploaded_file)

        else:
            preview_data = pd.read_excel(uploaded_file)

    except (
        pd.errors.ParserError,
        ValueError,
        ImportError,
    ) as error:

        st.error(f"Unable to preview this file: {error}")


    if preview_data is not None:

        st.markdown(
            '<div class="characterization-preview-card">',
            unsafe_allow_html=True,
        )

        st.markdown("### Dataset Preview")

        st.markdown(
            '<div class="characterization-preview-table">',
            unsafe_allow_html=True,
        )
        st.dataframe(
            preview_data.head(),
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        rows, columns = preview_data.shape

        st.markdown(
            '<div class="characterization-preview-divider"></div>',
            unsafe_allow_html=True,
        )

        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.markdown(
                '<div class="characterization-metric-card">',
                unsafe_allow_html=True,
            )
            st.metric(
                "Total Rows",
                rows,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with metric_col2:
            st.markdown(
                '<div class="characterization-metric-card">',
                unsafe_allow_html=True,
            )
            st.metric(
                "Total Columns",
                columns,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# DATA VALIDATION
# --------------------------------------------------

st.markdown("## Data Validation")

st.markdown(
    '<div class="validation-section"><div class="validation-grid">',
    unsafe_allow_html=True,
)

validation_col1, validation_col2 = st.columns(2)

with validation_col1:
    with st.container():
        st.metric(
            "Dataset Validity",
            "Pending validation",
        )

    with st.container():
        st.metric(
            "Detected Technique",
            "Pending detection",
        )

with validation_col2:
    with st.container():
        st.metric(
            "Missing Values",
            "Pending validation",
        )

    with st.container():
        st.markdown("**Column Information**")
        st.info(
            "Column metadata will appear here after validation."
        )

st.markdown("</div></div>", unsafe_allow_html=True)


# --------------------------------------------------
# PROCESSING CONTROLS
# --------------------------------------------------

st.markdown("## Processing Controls")


analysis_type = st.selectbox(
    "Analysis Type",
    options=[
        "Select an analysis type",
        "Spectroscopy Characterization",
        "Fluorescence Characterization",
    ],
)


optional_processing = st.checkbox(
    "Enable optional processing"
)


run_characterization = st.button(
    "Run Characterization",
    type="primary",
)


# --------------------------------------------------
# CHARACTERIZATION LOGIC
# --------------------------------------------------

if run_characterization:

    if preview_data is None:

        st.warning(
            "Upload a dataset before running characterization."
        )

    elif analysis_type == "Select an analysis type":

        st.warning(
            "Select an analysis type before running characterization."
        )

    else:

        st.info(
            "The UI is ready for characterization. "
            "The characterization function will be connected "
            "later from the external core module."
        )


# --------------------------------------------------
# CHARACTERIZATION RESULTS
# --------------------------------------------------

st.markdown("## Characterization Results")

with st.container(border=True):
    st.info(
        "Characterization results will appear here after "
        "the core module is connected."
    )


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

st.markdown("## Visualization")

with st.container(border=True):
    st.info(
        "Plotly visualizations will appear here when returned "
        "by the visualization module."
    )


# Integration point:
# st.plotly_chart(
#     external_plotly_figure,
#     use_container_width=True,
# )


# --------------------------------------------------
# SAVE AND EXPORT
# --------------------------------------------------

st.markdown("## Save and Export")

save_col1, save_col2, save_col3 = st.columns(3)

with save_col1:
    if st.button("Save Experiment", use_container_width=True):
        st.info(
            "Save experiment integration is pending."
        )

with save_col2:
    if st.button("Export Results", use_container_width=True):
        st.info(
            "Export results integration is pending."
        )

with save_col3:
    if st.button("Generate Report", use_container_width=True):
        st.info(
            "Report generation integration is pending."
        )