import streamlit as st
import pandas as pd


st.title("Carbon Dot Characterization")
st.write(
	"Upload carbon dot spectroscopy or fluorescence data to preview the dataset "
	"and view characterization results."
)


uploaded_file = st.file_uploader(
	"Upload spectroscopy or fluorescence data",
	type=["csv", "xlsx", "xls"],
)

preview_data = None
if uploaded_file is not None:
	st.write(f"**File:** {uploaded_file.name}")

	try:
		file_extension = uploaded_file.name.rsplit(".", 1)[-1].lower()
		if file_extension == "csv":
			preview_data = pd.read_csv(uploaded_file)
		else:
			preview_data = pd.read_excel(uploaded_file)
	except (pd.errors.ParserError, ValueError, ImportError) as error:
		st.error(f"Unable to preview this file: {error}")

	if preview_data is not None:
		st.subheader("Dataset Preview")
		st.dataframe(preview_data.head())
		rows, columns = preview_data.shape
		st.write(f"**Dataset dimensions:** {rows} rows x {columns} columns")

st.subheader("Data Validation")

# Integration point: display values returned by the data validation module.
validation_col1, validation_col2 = st.columns(2)
with validation_col1:
	st.metric("Dataset validity", "Pending validation")
	st.metric("Detected technique", "Pending detection")
with validation_col2:
	st.metric("Missing values", "Pending validation")
	st.write("**Column information**")
	st.info("Column metadata will appear here after validation.")

st.subheader("Processing Controls")
analysis_type = st.selectbox(
	"Analysis type",
	options=["Select an analysis type", "Spectroscopy characterization", "Fluorescence characterization"],
)
optional_processing = st.checkbox("Enable optional processing")
run_characterization = st.button("Run Characterization", type="primary")

if run_characterization:
	if preview_data is None:
		st.warning("Upload a dataset before running characterization.")
	elif analysis_type == "Select an analysis type":
		st.warning("Select an analysis type before running characterization.")
	else:
		# Integration point: call characterization function from core module.
		st.info(
			"The UI is ready for characterization. The characterization function "
			"will be connected later from the external core module."
		)

st.subheader("Characterization Results")

# Integration point: populate these values from the external core module.
st.info("Characterization results will appear here after the core module is connected.")

st.subheader("Visualization")
st.info("Plotly visualizations will appear here when returned by the visualization module.")

# Integration point: display Plotly figure from visualization module.
# st.plotly_chart(external_plotly_figure, use_container_width=True)

st.subheader("Save and Export")
save_col1, save_col2, save_col3 = st.columns(3)
with save_col1:
	if st.button("Save Experiment"):
		# Integration point: save experiment using database CRUD function.
		st.info("Save experiment integration is pending.")
with save_col2:
	if st.button("Export Results"):
		# Integration point: export results using the reporting module.
		st.info("Export results integration is pending.")
with save_col3:
	if st.button("Generate Report"):
		# Integration point: generate report using the reporting module.
		st.info("Report generation integration is pending.")
