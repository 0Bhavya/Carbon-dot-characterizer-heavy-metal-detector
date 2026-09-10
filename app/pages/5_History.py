import streamlit as st
import pandas as pd

from styles import load_css

st.set_page_config(
    page_title="Analysis History",
    page_icon="📚",
    layout="wide",
)

load_css()

st.markdown(
    """
<div class="page-hero">
<div class="page-hero-tag">📚 ANALYSIS HISTORY MODULE</div>
<div class="page-hero-title">Analysis History</div>
<div class="page-hero-subtitle">
View, filter, and review previously saved characterization and
heavy metal detection experiments from a centralized workspace.
</div>
</div>
""",
    unsafe_allow_html=True,
)

st.title("Analysis History")
st.write(
	"View and review previously saved characterization and heavy metal detection experiments."
)

st.header("Experiment History")

# Integration point: fetch experiment history using database CRUD function
experiment_history = st.session_state.get("experiment_history", [])
history_df = pd.DataFrame(experiment_history)

expected_columns = [
	"Experiment ID",
	"Module",
	"Experiment Name",
	"Date",
	"Status",
]
for column in expected_columns:
	if column not in history_df.columns:
		history_df[column] = ""

history_df = history_df[expected_columns]

st.subheader("Filter Experiments")
module_filter = st.selectbox(
	"Filter by module",
	["All Modules", "Characterization", "Heavy Metal Detection"],
)

if module_filter != "All Modules":
	displayed_history_df = history_df[history_df["Module"] == module_filter]
else:
	displayed_history_df = history_df

if displayed_history_df.empty:
	st.info("No saved experiments are available yet.")
else:
	st.dataframe(displayed_history_df, use_container_width=True, hide_index=True)

st.header("Experiment Details")

if displayed_history_df.empty:
	st.info("Select an experiment after saved history is available.")
else:
	experiment_options = displayed_history_df["Experiment ID"].astype(str).tolist()
	selected_experiment_id = st.selectbox("Select an experiment", experiment_options)
	selected_experiment = displayed_history_df[
		displayed_history_df["Experiment ID"].astype(str) == selected_experiment_id
	].iloc[0]

	# Integration point: fetch selected experiment details using database CRUD function
	st.subheader("Experiment Information")
	st.json(selected_experiment.to_dict())

	st.subheader("Input Dataset Information")
	st.info("Saved input dataset information will appear here.")

	# Integration point: load saved results
	st.subheader("Analysis Results")
	st.info("Saved analysis results will appear here.")

	# Integration point: load generated reports
	st.subheader("Generated Reports")
	st.info("Generated reports will appear here.")

	if st.button("Open Experiment Details"):
		st.info("Experiment details are ready to be loaded.")
