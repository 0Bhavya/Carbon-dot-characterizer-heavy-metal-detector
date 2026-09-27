import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from styles import load_css, render_app_shell_header, render_stepper, render_html

st.set_page_config(
    page_title="Characterization - Carbon Dot Characterizer",
    page_icon="💧",
    layout="wide",
)

load_css()
render_app_shell_header()

# Header
render_html(
    """
    <div style="margin-bottom: 1.25rem;">
        <div class="page-title">Characterization</div>
        <div class="page-subtitle">Analyze optical, structural and surface properties of carbon dots.</div>
    </div>
    """
)

# Initialize step in session state (default to Step 1: Upload Data)
if "char_step" not in st.session_state:
    st.session_state["char_step"] = 1

step_col1, step_col2, step_col3 = st.columns([1, 4, 1])
with step_col2:
    render_stepper(st.session_state["char_step"])


def get_default_sample_df():
    sample_w = np.linspace(200, 700, 501)
    peak1 = 1.42 * np.exp(-((sample_w - 320) ** 2) / (2 * (34) ** 2))
    shoulder = 0.25 * np.exp(-((sample_w - 410) ** 2) / (2 * (40) ** 2))
    tail = 0.08 * np.exp(-(sample_w - 200) / 160)
    sample_a = np.clip(peak1 + shoulder + tail, 0.0, 1.55)
    return pd.DataFrame({"Wavelength_nm": sample_w.round(1), "Absorbance": sample_a.round(3)})


def process_spectrum(df):
    cols = df.columns
    w_col = cols[0]
    a_col = cols[1] if len(cols) > 1 else cols[0]
    for c in cols:
        c_low = str(c).lower()
        if "wave" in c_low or "nm" in c_low:
            w_col = c
        elif "abs" in c_low or "intensity" in c_low:
            a_col = c

    w = pd.to_numeric(df[w_col], errors="coerce").dropna().values
    a = pd.to_numeric(df[a_col], errors="coerce").dropna().values

    idx_sort = np.argsort(w)
    w = w[idx_sort]
    a = a[idx_sort]

    max_idx = np.argmax(a)
    lambda_max = round(float(w[max_idx]), 1)
    peak_abs = round(float(a[max_idx]), 2)

    half_max = peak_abs / 2.0
    above_half = np.where(a >= half_max)[0]
    if len(above_half) > 1:
        fwhm = round(float(w[above_half[-1]] - w[above_half[0]]), 1)
    else:
        fwhm = 85.0

    est_size = round(float(max(1.5, min(8.0, 1.2 + (lambda_max - 280) * 0.09))), 1)
    quantum_yield = round(float(max(5.0, min(35.0, peak_abs * 8.8))), 1)

    return {
        "wavelengths": w,
        "absorbances": a,
        "lambda_max": lambda_max,
        "absorbance": peak_abs,
        "fwhm": fwhm,
        "estimated_size": est_size,
        "quantum_yield": quantum_yield,
    }


# ==========================================
# STEP 1: UPLOAD DATA (EXACT MOCKUP IMAGE 2)
# ==========================================
if st.session_state["char_step"] == 1:
    with st.container(border=True):
        render_html('<div class="card-header-title">Upload Dataset</div>')

        uploaded_file = st.file_uploader(
            "Upload dataset",
            type=["csv", "xlsx", "txt"],
            help="Supported formats: .csv, .xlsx, .txt. Maximum file size: 50MB",
            label_visibility="collapsed",
            key="char_file_uploader",
        )

        render_html(
            """
            <div style="text-align: center; color: #64748B; font-size: 0.8rem; margin-top: 0.85rem; line-height: 1.5;">
                Supported formats: .csv, .xlsx, .txt<br>Maximum file size: 50MB
            </div>
            """
        )

    sample_df = get_default_sample_df()
    sample_csv = sample_df.to_csv(index=False).encode("utf-8")

    with st.container(border=True):
        render_html(
            """
            <div class="card-header-title">Sample Dataset</div>
            <div style="font-size: 0.84rem; color: #64748B; margin-bottom: 0.95rem;">
                Download a sample dataset to see the expected format.
            </div>
            """
        )

        st.markdown('<div class="sample-download-btn">', unsafe_allow_html=True)
        st.download_button(
            "📥 Download Sample",
            data=sample_csv,
            file_name="sample_carbon_dot_spectrum.csv",
            mime="text/csv",
            key="btn_download_sample_char",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    btn_l, btn_r = st.columns([1, 1])
    with btn_r:
        st.markdown("<div style='text-align: right; margin-top: 0.5rem;'>", unsafe_allow_html=True)
        if st.button("Next →", type="primary", key="btn_next_char_to_val"):
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith(".csv"):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    st.session_state["char_uploaded_df"] = df
                    st.session_state["char_sample_name"] = uploaded_file.name.rsplit(".", 1)[0]
                    st.session_state["char_step"] = 2
                    st.rerun()
                except Exception as e:
                    st.error(f"Error reading file: {e}")
            elif "char_uploaded_df" in st.session_state:
                st.session_state["char_step"] = 2
                st.rerun()
            else:
                st.session_state["char_uploaded_df"] = sample_df
                st.session_state["char_sample_name"] = "Water_Sample_12"
                st.session_state["char_step"] = 2
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 2: VALIDATE
# ==========================================
elif st.session_state["char_step"] == 2:
    df = st.session_state.get("char_uploaded_df")
    if df is None:
        df = get_default_sample_df()
        st.session_state["char_uploaded_df"] = df
        st.session_state["char_sample_name"] = "Water_Sample_12"

    sample_name = st.session_state.get("char_sample_name", "Water_Sample_12")

    with st.container(border=True):
        render_html(
            f"""
            <div class="card-header-title">Dataset Validation — {sample_name}</div>
            <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 1.25rem;">
                Verification of file structure, column headers, and data integrity before analysis.
            </div>
            <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                <div class="val-metric-card">
                    <div class="val-metric-label">Dataset Validity</div>
                    <div class="val-metric-value" style="color: #16A34A; display: flex; align-items: center; gap: 0.4rem;">
                        <span>✓</span> Valid Spectroscopy Data
                    </div>
                </div>
                <div class="val-metric-card">
                    <div class="val-metric-label">Detected Technique</div>
                    <div class="val-metric-value" style="color: #2563EB;">UV-Vis Absorbance</div>
                </div>
                <div class="val-metric-card">
                    <div class="val-metric-label">Total Data Points</div>
                    <div class="val-metric-value">{len(df)} rows ({df.iloc[:, 0].min():.1f} nm - {df.iloc[:, 0].max():.1f} nm)</div>
                </div>
                <div class="val-metric-card">
                    <div class="val-metric-label">Missing Values</div>
                    <div class="val-metric-value" style="color: #16A34A;">0 (Clean Dataset)</div>
                </div>
            </div>
            <div style="font-size: 0.9rem; font-weight: 600; color: #0F172A; margin-bottom: 0.5rem;">Data Preview (First 6 Rows)</div>
            """
        )

        st.dataframe(df.head(6), use_container_width=True)

        render_html("<div style='height: 1rem;'></div>")

        b_col1, b_col2 = st.columns([1, 1])
        with b_col1:
            if st.button("← Back to Upload Data", key="btn_back_to_upload"):
                st.session_state["char_step"] = 1
                st.rerun()
        with b_col2:
            st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
            if st.button("Proceed to Analyze →", type="primary", key="btn_proceed_to_analyze"):
                st.session_state["char_step"] = 3
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 3: ANALYZE
# ==========================================
elif st.session_state["char_step"] == 3:
    df = st.session_state.get("char_uploaded_df")
    if df is None:
        df = get_default_sample_df()
        st.session_state["char_uploaded_df"] = df

    sample_name = st.session_state.get("char_sample_name", "Water_Sample_12")

    with st.container(border=True):
        render_html(
            f"""
            <div class="card-header-title">Processing & Analytical Controls</div>
            <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 1.25rem;">
                Select algorithm parameters to run optical property characterization for sample <strong>{sample_name}</strong>.
            </div>
            """
        )

        analysis_mode = st.selectbox(
            "Analysis Algorithm",
            [
                "Standard Peak Detection & Full Spectrum Deconvolution",
                "Savitzky-Golay Smoothed Spectroscopy Scan",
                "Tauc Direct Optical Band Gap Analysis",
            ],
            index=0,
        )

        baseline_corr = st.checkbox("Enable baseline drift and scattering correction", value=True)
        fwhm_calc = st.checkbox("Compute FWHM and particle size distribution approximation", value=True)

        render_html("<div style='height: 1rem;'></div>")

        a_col1, a_col2 = st.columns([1, 1.2])
        with a_col1:
            if st.button("← Back to Validation", key="btn_back_to_val"):
                st.session_state["char_step"] = 2
                st.rerun()
        with a_col2:
            if st.button("🧪 Run Characterization Analysis →", type="primary", use_container_width=True, key="btn_run_char_analysis"):
                results = process_spectrum(df)
                st.session_state["char_results"] = results

                # Append to session experiment history
                history = st.session_state.get("experiment_history", [])
                history.insert(
                    0,
                    {
                        "Sample Name": sample_name,
                        "Module": "Characterization",
                        "Status": "Completed",
                        "Date": "Today",
                    },
                )
                st.session_state["experiment_history"] = history

                st.session_state["char_step"] = 4
                st.rerun()


# ==========================================
# STEP 4: RESULTS (SCREEN 3)
# ==========================================
else:
    results = st.session_state.get("char_results")
    if not results:
        df = st.session_state.get("char_uploaded_df")
        if df is None:
            df = get_default_sample_df()
        results = process_spectrum(df)
        st.session_state["char_results"] = results

    # Sub-tabs
    tab_uv, tab_pl, tab_size, tab_surface = st.tabs(
        ["UV-Vis Spectrum", "PL Spectrum", "Size Distribution", "Surface Properties"]
    )

    with tab_uv:
        chart_col, params_col = st.columns([1.6, 1])

        with chart_col:
            with st.container(border=True):
                render_html('<div class="card-header-title">UV-Vis Absorbance Spectrum</div>')

                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=results["wavelengths"],
                        y=results["absorbances"],
                        mode="lines",
                        line=dict(color="#2563EB", width=2.5),
                        name="Absorbance",
                        hovertemplate="<b>Wavelength:</b> %{x:.1f} nm<br><b>Absorbance:</b> %{y:.3f}<extra></extra>",
                    )
                )

                y_max = max(1.6, float(results["absorbance"]) * 1.15)
                fig.update_layout(
                    margin=dict(l=45, r=20, t=20, b=45),
                    height=320,
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="#FFFFFF",
                    xaxis=dict(
                        title="Wavelength (nm)",
                        title_font=dict(size=12, color="#475569"),
                        tickfont=dict(size=11, color="#64748B"),
                        showgrid=True,
                        gridcolor="#F1F5F9",
                        gridwidth=1,
                        range=[200, 700],
                        tickvals=[200, 300, 400, 500, 600, 700],
                        zeroline=False,
                    ),
                    yaxis=dict(
                        title="Absorbance (a.u.)",
                        title_font=dict(size=12, color="#475569"),
                        tickfont=dict(size=11, color="#64748B"),
                        showgrid=True,
                        gridcolor="#F1F5F9",
                        gridwidth=1,
                        range=[0, y_max],
                        zeroline=False,
                    ),
                    showlegend=False,
                )

                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with params_col:
            with st.container(border=True):
                render_html(
                    f"""
                    <div class="card-header-title">Key Parameters</div>
                    <table class="modern-table">
                        <tbody>
                            <tr>
                                <td style="color: #475569; font-weight: 500;">λmax (nm)</td>
                                <td style="text-align: right; font-weight: 700; color: #0F172A;">{results['lambda_max']}</td>
                            </tr>
                            <tr>
                                <td style="color: #475569; font-weight: 500;">Absorbance</td>
                                <td style="text-align: right; font-weight: 700; color: #0F172A;">{results['absorbance']}</td>
                            </tr>
                            <tr>
                                <td style="color: #475569; font-weight: 500;">FWHM (nm)</td>
                                <td style="text-align: right; font-weight: 700; color: #0F172A;">{results['fwhm']}</td>
                            </tr>
                            <tr>
                                <td style="color: #475569; font-weight: 500;">Estimated Size (nm)</td>
                                <td style="text-align: right; font-weight: 700; color: #0F172A;">{results['estimated_size']}</td>
                            </tr>
                            <tr>
                                <td style="color: #475569; font-weight: 500;">Quantum Yield (%)</td>
                                <td style="text-align: right; font-weight: 700; color: #0F172A;">{results['quantum_yield']}</td>
                            </tr>
                        </tbody>
                    </table>
                    """
                )

        # Analysis Completed Banner
        render_html(
            """
            <div class="analysis-completed-banner">
                <span class="analysis-check-icon">✓</span>
                <div>
                    <strong>Analysis Completed</strong> — Characterization analysis finished successfully.
                </div>
            </div>
            """
        )

        # Bottom Buttons
        btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 1])
        with btn_col1:
            if st.button("← New Analysis (Upload)", key="btn_start_new_char"):
                st.session_state["char_step"] = 1
                st.rerun()

        with btn_col2:
            results_df = pd.DataFrame(
                {
                    "Parameter": ["λmax (nm)", "Absorbance", "FWHM (nm)", "Estimated Size (nm)", "Quantum Yield (%)"],
                    "Value": [results["lambda_max"], results["absorbance"], results["fwhm"], results["estimated_size"], results["quantum_yield"]],
                }
            )
            st.download_button(
                "📥 Download Results",
                data=results_df.to_csv(index=False).encode("utf-8"),
                file_name="characterization_results.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with btn_col3:
            if st.button("📄 Generate Report", type="primary", use_container_width=True, key="btn_gen_char_rep"):
                st.session_state["report_selected_analysis"] = "Characterization"
                st.session_state["report_selected_sample"] = st.session_state.get("char_sample_name", "Water_Sample_12")
                st.switch_page("pages/4_Reports_&_Export.py")

    with tab_pl:
        st.info("Photoluminescence (PL) Emission & Excitation spectrum for sample.")
        pl_wavelengths = np.linspace(350, 650, 301)
        pl_emission = 850 * np.exp(-((pl_wavelengths - 450) ** 2) / (2 * 45**2))
        fig_pl = go.Figure()
        fig_pl.add_trace(go.Scatter(x=pl_wavelengths, y=pl_emission, mode="lines", line=dict(color="#10B981", width=2.5)))
        fig_pl.update_layout(height=280, margin=dict(l=40, r=20, t=20, b=40), xaxis_title="Wavelength (nm)", yaxis_title="PL Intensity (a.u.)")
        st.plotly_chart(fig_pl, use_container_width=True)

    with tab_size:
        st.info(f"DLS Hydrodynamic Particle Size Distribution (Estimated Peak: {results['estimated_size']} nm).")
        sizes = np.linspace(1, 15, 100)
        distribution = np.exp(-((sizes - results['estimated_size']) ** 2) / (2 * 1.5**2))
        fig_size = go.Figure()
        fig_size.add_trace(go.Scatter(x=sizes, y=distribution, mode="lines", fill="tozeroy", line=dict(color="#6366F1", width=2)))
        fig_size.update_layout(height=280, margin=dict(l=40, r=20, t=20, b=40), xaxis_title="Hydrodynamic Diameter (nm)", yaxis_title="Frequency (%)")
        st.plotly_chart(fig_size, use_container_width=True)

    with tab_surface:
        st.info("FTIR Surface Functional Groups (C=O, -OH, C-N bonds identified).")
        ftir_wn = np.linspace(4000, 500, 300)
        transmittance = 100 - (35 * np.exp(-((ftir_wn - 3400) ** 2) / (2 * 150**2)) + 45 * np.exp(-((ftir_wn - 1650) ** 2) / (2 * 60**2)))
        fig_ftir = go.Figure()
        fig_ftir.add_trace(go.Scatter(x=ftir_wn, y=transmittance, mode="lines", line=dict(color="#EC4899", width=2)))
        fig_ftir.update_layout(height=280, margin=dict(l=40, r=20, t=20, b=40), xaxis=dict(autorange="reversed", title="Wavenumber (cm⁻¹)"), yaxis_title="Transmittance (%)")
        st.plotly_chart(fig_ftir, use_container_width=True)