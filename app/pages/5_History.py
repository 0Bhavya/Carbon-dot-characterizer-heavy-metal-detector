import pandas as pd
import streamlit as st

from styles import load_css, render_app_shell_header, render_html

st.set_page_config(
    page_title="History - Carbon Dot Characterizer",
    page_icon="💧",
    layout="wide",
)

load_css()
render_app_shell_header()

# Header
render_html(
    """
    <div style="margin-bottom: 1.25rem;">
        <div class="page-title">Analysis History</div>
        <div class="page-subtitle">View and review previously saved characterization and heavy metal detection experiments.</div>
    </div>
    """
)

# Search & Filter Controls
filter_col1, filter_col2 = st.columns([1.5, 3])

with filter_col1:
    module_filter = st.selectbox(
        "Filter by Module",
        ["All Modules", "Heavy Metal Detection", "Characterization", "Explainable AI"],
        index=0,
    )

with filter_col2:
    search_query = st.text_input("Search by Sample Name", placeholder="e.g. River_Water_07...")

# Fetch real session experiment history ONLY
raw_history = st.session_state.get("experiment_history", [])

history_records = []
for idx, h in enumerate(raw_history, start=1):
    status = h.get("Status", "Completed")
    badge = "completed" if status.lower() == "completed" else "processing"
    history_records.append(
        {
            "ID": f"EXP-{20260900 + idx}",
            "Sample Name": h.get("Sample Name", "Sample"),
            "Module": h.get("Module", "General"),
            "Date": h.get("Date", "Today"),
            "Status": status,
            "Badge": badge,
            "Result": h.get("Result", "Analysis completed and logged to session."),
        }
    )

# Apply filters
filtered = history_records
if module_filter != "All Modules":
    filtered = [r for r in filtered if r["Module"] == module_filter or (module_filter == "Heavy Metal Detection" and "Heavy" in r["Module"])]
if search_query.strip():
    filtered = [r for r in filtered if search_query.lower() in r["Sample Name"].lower()]

with st.container(border=True):
    if filtered:
        render_html(f'<div class="card-header-title">Completed & In-Progress Experiments ({len(filtered)})</div>')

        table_rows = "".join(
            [
                f"<tr><td style='font-weight: 600; color: #2563EB;'>{r['ID']}</td>"
                f"<td style='font-weight: 600; color: #0F172A;'>{r['Sample Name']}</td>"
                f"<td>{r['Module']}</td>"
                f"<td><span class='status-badge {r['Badge']}'>{r['Status']}</span></td>"
                f"<td style='color: #64748B;'>{r['Date']}</td>"
                f"<td style='color: #475569; font-size: 0.8rem;'>{r['Result']}</td></tr>"
                for r in filtered
            ]
        )

        render_html(
            f"""
            <table class="modern-table">
                <thead>
                    <tr>
                        <th>Experiment ID</th>
                        <th>Sample Name</th>
                        <th>Module</th>
                        <th>Status</th>
                        <th>Date</th>
                        <th>Key Findings / Summary</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
            """
        )
    else:
        render_html(
            """
            <div style="background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 10px; padding: 2.2rem 1.5rem; text-align: center;">
                <div style="font-weight: 600; color: #0F172A; font-size: 0.95rem; margin-bottom: 0.35rem;">No saved experiments yet</div>
                <div style="font-size: 0.82rem; color: #64748B; margin-bottom: 1rem;">
                    Once you upload and run an analysis in Characterization or Heavy Metal Detection, your results will be logged here.
                </div>
            </div>
            """
        )
        if st.button("⚡ Load Benchmark Experiments (Reference Preview)", key="btn_load_demo_to_history"):
            st.session_state["experiment_history"] = [
                {
                    "Sample Name": "River_Water_07",
                    "Module": "Heavy Metal Detection",
                    "Status": "Completed",
                    "Date": "12 Sep 2026",
                    "Result": "Cadmium: 0.028 mg/L (Warning), Lead/Mercury/Chromium/Arsenic: Safe",
                },
                {
                    "Sample Name": "Water_Sample_12",
                    "Module": "Characterization",
                    "Status": "Processing",
                    "Date": "11 Sep 2026",
                    "Result": "Optical absorbance scan in progress (Peak: 320 nm)",
                },
                {
                    "Sample Name": "CD_Sample_A3",
                    "Module": "Explainable AI",
                    "Status": "Completed",
                    "Date": "10 Sep 2026",
                    "Result": "Low Risk (82% Safe) | Key features: pH, Absorbance 320nm",
                },
            ]
            st.rerun()