import streamlit as st


st.set_page_config(
	page_title="Carbon Dot Characterizer",
	page_icon="🧪",
	layout="wide",
)


st.title("Carbon Dot Characterizer & Heavy Metal Detection Platform")
st.write(
	"An explainable AI platform for analyzing carbon dot fluorescence and "
	"spectroscopy data, characterizing carbon dots, and supporting heavy metal "
	"detection experiments."
)


st.divider()

st.header("About the Platform")
st.write(
	"The platform brings the complete carbon dot analysis workflow into one "
	"workspace. Explore characterization results, investigate heavy metal "
	"detection experiments, understand model outputs, and keep experiment "
	"reports and history organized."
)

about_columns = st.columns(4)
about_items = [
	(
		"Carbon Dot Characterization",
		"Review fluorescence and spectroscopy data to understand carbon dot properties.",
	),
	(
		"Heavy Metal Detection",
		"Analyze detection experiments and review results for heavy metal targets.",
	),
	(
		"Explainable AI",
		"Interpret model results with clear, human-readable explanations.",
	),
	(
		"Reports and Experiment History",
		"Export findings and revisit earlier analyses from a central history view.",
	),
]

for column, (title, description) in zip(about_columns, about_items):
	with column:
		st.subheader(title)
		st.write(description)


st.header("Workflow")
workflow_steps = [
	"Upload and Analyze Data",
	"Characterize Carbon Dots",
	"Detect Heavy Metals",
	"Generate Explainable AI Results",
	"Export Reports",
	"Review Analysis History",
]

workflow_columns = st.columns(3)
for index, step in enumerate(workflow_steps, start=1):
	with workflow_columns[(index - 1) % 3]:
		st.markdown(f"**{index}. {step}**")


st.header("Platform Modules")
modules = [
	(
		"Carbon Dot Characterization",
		"Explore carbon dot fluorescence and spectroscopy characterization results.",
		"pages/1_Characterization.py",
	),
	(
		"Heavy Metal Detection",
		"Review heavy metal detection workflows, targets, and experiment results.",
		"pages/2_Heavy_Metal_Detection.py",
	),
	(
		"Explainable AI",
		"Understand the reasoning behind detection results through explainable outputs.",
		"pages/3_Explainable_AI.py",
	),
	(
		"Reports and Export",
		"Prepare and export characterization and detection reports.",
		"pages/4_Reports_Export.py",
	),
	(
		"Analysis History",
		"Review previous experiments and keep track of completed analyses.",
		"pages/5_History.py",
	),
	(
		"Platform Overview",
		"Return to this dashboard for the complete workflow and module guide.",
		None,
	),
]

module_columns = st.columns(3)
for index, (title, description, page_path) in enumerate(modules):
	with module_columns[index % 3]:
		st.subheader(title)
		st.write(description)
		if page_path:
			st.page_link(page_path, label=f"Open {title}", icon="→")


st.header("How to Use")
st.write(
	"Begin with the characterization page to upload and analyze your data. "
	"Continue to heavy metal detection to review experiment findings, then "
	"open Explainable AI for interpretable results. Use Reports and Export to "
	"create deliverables, and Analysis History to revisit previous work. "
	"Return to the Platform Overview at any time for a quick guide to the "
	"available modules."
)
