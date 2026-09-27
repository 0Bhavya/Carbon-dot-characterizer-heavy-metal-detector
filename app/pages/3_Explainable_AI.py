import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.reporting.heavy_metal_report import export_predictions_json, generate_heavy_metal_pdf
from styles import load_css


st.set_page_config(page_title="Explainable AI", page_icon="🧠", layout="wide")
load_css()

st.markdown(
    """
<div class="page-hero">
<div class="page-hero-tag">🧠 EXPLAINABLE AI MODULE</div>
<div class="page-hero-title">Explainable Artificial Intelligence</div>
<div class="page-hero-subtitle">Inspect the explanation attached to the latest heavy-metal prediction.</div>
</div>
""",
    unsafe_allow_html=True,
)


def _plain(value):
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value


results = st.session_state.get("heavy_metal_results")
if not results:
    st.info("Run Heavy Metal Detection first. Its prediction and SHAP explanation will appear here.")
    st.stop()

identification = results.get("identification")
concentration = results.get("concentration")
xai = results.get("xai", {})
detection_xai = xai.get("detection", {})

st.header("Prediction Summary")
summary_columns = st.columns(2)
summary_values = [
    ("Predicted heavy metal", identification.metal if identification else "No metal detected"),
    ("Prediction confidence", f"{identification.confidence:.1%}" if identification else f"{results['detection_confidence']:.1%}"),
    ("Estimated concentration", f"{concentration.value:.3g}" if concentration else "N/A"),
    ("Model versions", ", ".join(f"{key}: {value}" for key, value in results["model_versions"].items())),
]
for index, (label, value) in enumerate(summary_values):
    with summary_columns[index % 2]:
        st.metric(label, value)

st.header("Local SHAP Explanation")
if detection_xai:
    feature_names = detection_xai.get("feature_names", [])
    shap_values = detection_xai.get("shap_values", [])
    contribution_table = pd.DataFrame(
        {
            "Feature Name": feature_names,
            "SHAP Contribution": [float(value) for value in shap_values],
        }
    )
    contribution_table["Impact Direction"] = contribution_table["SHAP Contribution"].map(
        lambda value: "increases model output" if value >= 0 else "decreases model output"
    )
    contribution_table = contribution_table.sort_values(
        "SHAP Contribution", key=lambda values: values.abs(), ascending=False
    )
    st.bar_chart(contribution_table.set_index("Feature Name")["SHAP Contribution"])
    st.dataframe(contribution_table, use_container_width=True, hide_index=True)
else:
    st.info("No SHAP explanation was returned for this prediction.")

st.header("Model Performance Context")
st.json({"model_versions": results.get("model_versions", {})})

st.header("Export Explainability Results")
json_export = export_predictions_json(results, xai).getvalue()
st.download_button(
    "Export SHAP/XAI JSON",
    data=json_export,
    file_name="shap_xai_results.json",
    mime="application/json",
)
pdf_export = generate_heavy_metal_pdf(results, xai_images=None).getvalue()
st.download_button(
    "Generate XAI Report PDF",
    data=pdf_export,
    file_name="xai_report.pdf",
    mime="application/pdf",
)
