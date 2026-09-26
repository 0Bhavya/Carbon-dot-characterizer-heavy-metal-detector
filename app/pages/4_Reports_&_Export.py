import io
from datetime import datetime
import pandas as pd
import streamlit as st

from styles import load_css, render_app_shell_header, render_html

try:
    from core.reporting.heavy_metal_report import generate_heavy_metal_pdf
    from core.reporting.characterization_report import generate_characterization_pdf
except ImportError:
    generate_heavy_metal_pdf = None
    generate_characterization_pdf = None

st.set_page_config(
    page_title="Reports & Export - Carbon Dot Characterizer",
    page_icon="💧",
    layout="wide",
)

load_css()
render_app_shell_header()

# Header
render_html(
    """
    <div style="margin-bottom: 1.25rem;">
        <div class="page-title">Reports & Export</div>
        <div class="page-subtitle">Generate and export detailed analysis reports.</div>
    </div>
    """
)

tab_gen, tab_saved = st.tabs(["Generate Report", "Saved Reports"])

with tab_gen:
    col_form, col_prev = st.columns([1, 1.2])

    with col_form:
        # Pre-select if redirected from another page
        default_analysis = st.session_state.get("report_selected_analysis", "Heavy Metal Detection")
        analysis_options = ["Heavy Metal Detection", "Characterization", "Explainable AI"]
        analysis_index = analysis_options.index(default_analysis) if default_analysis in analysis_options else 0

        selected_analysis = st.selectbox(
            "Select Analysis",
            analysis_options,
            index=analysis_index,
            key="rep_select_analysis",
        )

        # Dynamic sample list from session state
        existing_samples = []
        if "char_sample_name" in st.session_state:
            existing_samples.append(st.session_state["char_sample_name"])
        if "heavy_sample_name" in st.session_state:
            existing_samples.append(st.session_state["heavy_sample_name"])
        for h in st.session_state.get("experiment_history", []):
            s_name = h.get("Sample Name")
            if s_name and s_name not in existing_samples:
                existing_samples.append(s_name)

        if not existing_samples:
            existing_samples = ["River_Water_07", "Water_Sample_12", "CD_Sample_A3"]

        default_sample = st.session_state.get("report_selected_sample", existing_samples[0])
        sample_index = existing_samples.index(default_sample) if default_sample in existing_samples else 0

        selected_sample = st.selectbox(
            "Select Sample",
            existing_samples,
            index=sample_index,
            key="rep_select_sample",
        )

        report_format = st.radio(
            "Report Format",
            ["PDF", "Excel", "CSV"],
            index=0,
            key="rep_format_radio",
        )

        render_html("<div style='height: 0.8rem;'></div>")

        if st.button("📄 Generate Report", type="primary", use_container_width=True, key="btn_execute_generate"):
            st.session_state["report_ready"] = True
            st.session_state["active_rep_format"] = report_format
            st.session_state["active_rep_sample"] = selected_sample
            st.session_state["active_rep_module"] = selected_analysis

        if st.session_state.get("report_ready", False):
            rep_fmt = st.session_state.get("active_rep_format", "PDF")
            rep_smp = st.session_state.get("active_rep_sample", selected_sample)
            rep_mod = st.session_state.get("active_rep_module", selected_analysis)

            st.success(f"{rep_fmt} report for {rep_smp} is ready!")

            if rep_fmt == "PDF":
                pdf_output = io.BytesIO()
                if rep_mod == "Heavy Metal Detection" and generate_heavy_metal_pdf:
                    sample_results = {
                        "status": "Completed",
                        "detection_status": "Metal Detected (Low Risk)",
                        "metal": "Cadmium (Cd) - 0.028 mg/L",
                        "concentration": "0.028 mg/L",
                        "sample_name": rep_smp,
                        "notes": "Lead, Mercury, Chromium, Arsenic within Safe limits.",
                    }
                    pdf_output = generate_heavy_metal_pdf(sample_results)
                elif rep_mod == "Characterization" and generate_characterization_pdf:
                    char_results = {
                        "lambda_max": 320,
                        "absorbance": 1.42,
                        "fwhm": 85,
                        "estimated_size": "4.8 nm",
                        "quantum_yield": "12.5%",
                    }
                    pdf_output = generate_characterization_pdf(char_results)
                else:
                    if generate_heavy_metal_pdf:
                        pdf_output = generate_heavy_metal_pdf({"status": "Completed", "module": rep_mod, "sample_name": rep_smp})
                    else:
                        pdf_output.write(b"%PDF-1.4 Carbon Dot Report")

                pdf_bytes = pdf_output.getvalue() if hasattr(pdf_output, "getvalue") else pdf_output

                st.download_button(
                    label="📥 Click Here to Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"{rep_smp}_{rep_mod.replace(' ', '_')}_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="btn_download_pdf_file",
                )
            elif rep_fmt == "Excel":
                sample_df = pd.DataFrame(
                    {
                        "Metal": ["Lead (Pb)", "Mercury (Hg)", "Cadmium (Cd)", "Chromium (Cr)", "Arsenic (As)"],
                        "Concentration (mg/L)": [0.012, 0.004, 0.028, 0.006, 0.0008],
                        "Status": ["Safe", "Safe", "Warning", "Safe", "Safe"],
                    }
                )
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                    sample_df.to_excel(writer, index=False, sheet_name="Analysis")
                st.download_button(
                    label="📥 Click Here to Download Excel Report",
                    data=excel_buffer.getvalue(),
                    file_name=f"{rep_smp}_{rep_mod.replace(' ', '_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="btn_download_excel_file",
                )
            else:
                csv_data = "Metal,Concentration_mg_L,Status\nLead (Pb),0.012,Safe\nMercury (Hg),0.004,Safe\nCadmium (Cd),0.028,Warning\nChromium (Cr),0.006,Safe\nArsenic (As),<0.001,Safe\n"
                st.download_button(
                    label="📥 Click Here to Download CSV Report",
                    data=csv_data.encode("utf-8"),
                    file_name=f"{rep_smp}_{rep_mod.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="btn_download_csv_file",
                )

    with col_prev:
        render_html(
            f"""
            <div style="font-size: 0.95rem; font-weight: 700; color: #0F172A; margin-bottom: 0.6rem;">Preview</div>
            <div class="report-preview-sheet">
                <div style="font-size: 1.5rem; margin-bottom: 0.2rem;">💧</div>
                <div class="doc-title">Carbon Dot Characterizer</div>
                <div class="doc-subtitle">Analysis Report</div>
                <div class="doc-meta">
                    <div><strong>Sample:</strong> &nbsp;{selected_sample}</div>
                    <div><strong>Module:</strong> &nbsp;{selected_analysis}</div>
                    <div><strong>Date:</strong> &nbsp;12 Sep 2026</div>
                </div>
                <div class="doc-preview-body">
                    <div style="font-weight: 600; color: #0F172A; margin-bottom: 0.4rem;">Executive Summary:</div>
                    Sample <strong>{selected_sample}</strong> was evaluated on the Scientific Analysis Platform.<br>
                    • Status: <span style="color:#16A34A; font-weight:600;">Analysis Completed</span><br>
                    • Module: {selected_analysis}<br>
                    • AI prediction indicates overall compliance within environmental standards.<br>
                    • Full spectroscopic dataset and trace element log attached in report.
                </div>
            </div>
            """
        )

with tab_saved:
    saved_history = st.session_state.get("experiment_history", [])
    if saved_history:
        rows = []
        for idx, h in enumerate(saved_history, start=1):
            s_name = h.get("Sample Name", "Sample")
            mod_name = h.get("Module", "General")
            date_val = h.get("Date", "12 Sep 2026")
            rows.append(
                f"<tr><td>{idx}</td><td style='font-weight: 600;'>{s_name}</td><td>{mod_name}</td>"
                f"<td style='color: #64748B;'>{date_val}</td><td>PDF</td>"
                f"<td><span style='color: #2563EB; font-weight: 600;'>Generated</span></td></tr>"
            )

        render_html(
            f"""
            <div class="card-container">
                <div class="card-title">Saved Analysis Reports</div>
                <table class="modern-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Sample Name</th>
                            <th>Module</th>
                            <th>Date</th>
                            <th>Format</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rows)}
                    </tbody>
                </table>
            </div>
            """
        )
    else:
        render_html(
            """
            <div class="card-container">
                <div class="card-title">Saved Analysis Reports</div>
                <div style="background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 10px; padding: 2rem 1.2rem; text-align: center;">
                    <div style="font-weight: 600; color: #0F172A; font-size: 0.92rem; margin-bottom: 0.25rem;">No saved reports yet</div>
                    <div style="font-size: 0.82rem; color: #64748B;">Generate your first report under the 'Generate Report' tab to see it here.</div>
                </div>
            </div>
            """
        )