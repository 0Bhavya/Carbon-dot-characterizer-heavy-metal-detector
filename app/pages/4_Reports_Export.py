"""Streamlit page for report generation and analysis exports."""

from io import BytesIO

import pandas as pd
import streamlit as st

try:
	from core.reporting.characterization_report import (
		generate_characterization_pdf,
		export_processed_data,
	)
	from core.reporting.heavy_metal_report import (
		generate_heavy_metal_pdf,
		export_predictions_json,
	)
except ImportError:
	generate_characterization_pdf = None
	export_processed_data = None
	generate_heavy_metal_pdf = None
	export_predictions_json = None


st.title("Reports and Export")
st.write("Download reports and analysis results from the completed platform workflows.")


def _empty_dataframe() -> pd.DataFrame:
	"""Return placeholder processed data until characterization is integrated."""
	return pd.DataFrame()


def _as_download_bytes(value: BytesIO | bytes) -> bytes:
	"""Read an in-memory export without changing the stream position for callers."""
	if isinstance(value, BytesIO):
		return value.getvalue()
	return value


def _result_available(value: object) -> bool:
	"""Check whether external analysis has supplied a non-empty result."""
	if value is None:
		return False
	if isinstance(value, (dict, list, tuple, pd.DataFrame)):
		return len(value) > 0
	return True


st.header("Characterization Report")
characterization_results = st.session_state.get("characterization_results", {})
# Integration point: receive characterization results from the characterization module.
processed_data_value = st.session_state.get("processed_data")
processed_data = (
	processed_data_value
	if isinstance(processed_data_value, pd.DataFrame)
	else _empty_dataframe()
)
# Integration point: receive processed data from the characterization module.

if not _result_available(characterization_results):
	st.info("Characterization results are not available yet. A placeholder report can still be generated.")
if processed_data.empty:
	st.info("Processed characterization data is not available yet.")

if st.button("Generate Characterization PDF", key="generate_characterization_pdf"):
	if generate_characterization_pdf is None:
		st.error("Characterization reporting is unavailable.")
	else:
		# Integration point: pass graph images from the visualization module when available.
		graph_images = st.session_state.get("characterization_graph_images")
		st.session_state["characterization_pdf"] = generate_characterization_pdf(
			characterization_results,
			graph_images=graph_images,
		)
		st.success("Characterization PDF generated.")

characterization_pdf = st.session_state.get("characterization_pdf")
if characterization_pdf is not None:
	st.download_button(
		"Download Characterization PDF",
		data=_as_download_bytes(characterization_pdf),
		file_name="characterization_report.pdf",
		mime="application/pdf",
		key="download_characterization_pdf",
	)

csv_col, xlsx_col = st.columns(2)
with csv_col:
	if st.button("Prepare Processed Data CSV", key="prepare_processed_csv"):
		if export_processed_data is None:
			st.error("Processed data export is unavailable.")
		else:
			st.session_state["processed_data_csv"] = export_processed_data(processed_data, "csv")
	processed_csv = st.session_state.get("processed_data_csv")
	if processed_csv is not None:
		st.download_button(
			"Export Processed Data as CSV",
			data=_as_download_bytes(processed_csv),
			file_name="processed_data.csv",
			mime="text/csv",
			key="download_processed_csv",
		)

with xlsx_col:
	if st.button("Prepare Processed Data XLSX", key="prepare_processed_xlsx"):
		if export_processed_data is None:
			st.error("Processed data export is unavailable.")
		else:
			st.session_state["processed_data_xlsx"] = export_processed_data(processed_data, "xlsx")
	processed_xlsx = st.session_state.get("processed_data_xlsx")
	if processed_xlsx is not None:
		st.download_button(
			"Export Processed Data as XLSX",
			data=_as_download_bytes(processed_xlsx),
			file_name="processed_data.xlsx",
			mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
			key="download_processed_xlsx",
		)


st.header("Heavy Metal Detection Report")
heavy_metal_results = st.session_state.get("heavy_metal_results", {})
# Integration point: receive completed heavy metal prediction results.
explainability_data = st.session_state.get("explainability_data", {})
# Integration point: receive completed explainability and SHAP data.

if not _result_available(heavy_metal_results):
	st.info("Heavy metal detection results are not available yet. A placeholder report can still be generated.")
if not _result_available(explainability_data):
	st.info("Explainability and SHAP data are not available yet.")

if st.button("Generate Heavy Metal Detection PDF", key="generate_heavy_metal_pdf"):
	if generate_heavy_metal_pdf is None:
		st.error("Heavy metal reporting is unavailable.")
	else:
		# Integration point: receive XAI images from the external visualization module.
		graph_images = st.session_state.get("heavy_metal_graph_images")
		xai_images = st.session_state.get("xai_images")
		st.session_state["heavy_metal_pdf"] = generate_heavy_metal_pdf(
			heavy_metal_results,
			graph_images=graph_images,
			xai_images=xai_images,
		)
		st.success("Heavy metal detection PDF generated.")

heavy_metal_pdf = st.session_state.get("heavy_metal_pdf")
if heavy_metal_pdf is not None:
	st.download_button(
		"Download Heavy Metal Detection PDF",
		data=_as_download_bytes(heavy_metal_pdf),
		file_name="heavy_metal_detection_report.pdf",
		mime="application/pdf",
		key="download_heavy_metal_pdf",
	)

prediction_col, xai_col = st.columns(2)
with prediction_col:
	if st.button("Prepare Prediction Results JSON", key="prepare_prediction_json"):
		if export_predictions_json is None:
			st.error("Prediction export is unavailable.")
		else:
			st.session_state["prediction_json"] = export_predictions_json(
				heavy_metal_results,
				{},
			)
	prediction_json = st.session_state.get("prediction_json")
	if prediction_json is not None:
		st.download_button(
			"Export Prediction Results as JSON",
			data=_as_download_bytes(prediction_json),
			file_name="prediction_results.json",
			mime="application/json",
			key="download_prediction_json",
		)

with xai_col:
	if st.button("Prepare SHAP/XAI JSON", key="prepare_xai_json"):
		if export_predictions_json is None:
			st.error("Explainability export is unavailable.")
		else:
			st.session_state["xai_json"] = export_predictions_json(
				{},
				explainability_data,
			)
	xai_json = st.session_state.get("xai_json")
	if xai_json is not None:
		st.download_button(
			"Export SHAP/XAI Data as JSON",
			data=_as_download_bytes(xai_json),
			file_name="shap_xai_data.json",
			mime="application/json",
			key="download_xai_json",
		)


st.header("Graph Export")
st.write("Graphs generated by external visualization modules will be available here for download.")
# Integration point: receive graph images from visualization modules.
graph_exports = st.session_state.get("graph_exports", [])
if not graph_exports:
	st.info("No graph images are available yet.")
else:
	for index, graph in enumerate(graph_exports, start=1):
		graph_data = _as_download_bytes(graph) if isinstance(graph, (BytesIO, bytes)) else graph
		st.download_button(
			f"Download Graph {index}",
			data=graph_data,
			file_name=f"graph_{index}.png",
			mime="image/png",
			key=f"download_graph_{index}",
		)
