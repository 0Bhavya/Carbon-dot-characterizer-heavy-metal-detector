import streamlit as st
import pandas as pd
from styles import load_css


st.set_page_config(
    page_title="Explainable AI",
    page_icon="🧠",
    layout="wide",
)

load_css()

st.markdown(
    """
<div class="page-hero">
<div class="page-hero-tag">🧠 EXPLAINABLE AI MODULE</div>
<div class="page-hero-title">Explainable Artificial Intelligence</div>
<div class="page-hero-subtitle">
Explore interpretable AI explanations to understand how predictions
are made, which features influence results, and why the model reaches
a particular heavy metal detection decision.
</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        padding: 0.8rem 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.header("Prediction Summary")
summary_columns = st.columns(2)
summary_placeholders = [
    ("Predicted heavy metal", "Pending"),
    ("Prediction confidence", "Pending"),
    ("Estimated concentration", "Pending"),
    ("Model name", "Pending"),
]

for index, (label, value) in enumerate(summary_placeholders):
    column = summary_columns[index % 2]
    with column:
        st.metric(label, value)


st.header("Local SHAP Explanation")
with st.container(border=True):
    st.info("The local SHAP explanation for the selected prediction will appear here.")


st.header("Global Feature Importance")
importance_columns = st.columns(2)
with importance_columns[0]:
    with st.container(border=True):
        st.info("The global feature importance visualization will appear here.")
with importance_columns[1]:
    with st.container(border=True):
        st.write("**Most important features**")
        st.info("The most important features will appear here.")


st.header("Feature Contribution Table")
contribution_table = pd.DataFrame(
    columns=[
        "Feature Name",
        "Feature Value",
        "Contribution",
        "Impact Direction",
    ]
)
with st.container(border=True):
    st.dataframe(contribution_table, use_container_width=True)


st.header("Model Performance Metrics")
performance_columns = st.columns(4)
performance_placeholders = [
    ("Accuracy", "Pending"),
    ("Precision", "Pending"),
    ("Recall", "Pending"),
    ("F1 Score", "Pending"),
]
for column, (label, value) in zip(performance_columns, performance_placeholders):
    with column:
        st.metric(label, value)


st.header("Export Explainability Results")
export_columns = st.columns(3)
with export_columns[0]:
    if st.button("Export Explanation"):
        st.info("Explanation export will be available after reporting integration.")
with export_columns[1]:
    if st.button("Export SHAP Data"):
        st.info("SHAP data export will be available after reporting integration.")
with export_columns[2]:
    if st.button("Generate XAI Report"):
        st.info("XAI report generation will be available after reporting integration.")
