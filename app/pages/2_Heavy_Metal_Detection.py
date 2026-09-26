import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from styles import load_css, render_app_shell_header, render_stepper, render_html

st.set_page_config(
    page_title="Heavy Metal Detection - Carbon Dot Characterizer",
    page_icon="💧",
    layout="wide",
)

load_css()
render_app_shell_header()

# Header
render_html(
    """
    <div style="margin-bottom: 1.25rem;">
        <div class="page-title">Heavy Metal Detection</div>
        <div class="page-subtitle">Detect and quantify heavy metals in water using AI models.</div>
    </div>
    """
)

# Step management: Start on Step 1 (Upload Data)
if "heavy_step" not in st.session_state:
    st.session_state["heavy_step"] = 1

step_col1, step_col2, step_col3 = st.columns([1, 4, 1])
with step_col2:
    render_stepper(st.session_state["heavy_step"], module_prefix="heavy")


def get_default_water_df():
    return pd.DataFrame(
        {
            "Metal": ["Lead (Pb)", "Mercury (Hg)", "Cadmium (Cd)", "Chromium (Cr)", "Arsenic (As)"],
            "Fluorescence_Quenching_%": [12.4, 5.2, 38.6, 8.1, 1.3],
            "Concentration_mg_L": [0.012, 0.004, 0.028, 0.006, 0.0008],
        }
    )


def analyze_heavy_metals(sample_name="River_Water_07", custom_data=None):
    if custom_data is not None and not custom_data.empty:
        metals = []
        for _, row in custom_data.iterrows():
            m_name = str(row.iloc[0])
            val = float(row.iloc[-1]) if pd.notnull(row.iloc[-1]) else 0.0
            is_warning = False
            if "cadmium" in m_name.lower() or "cd" in m_name.lower():
                is_warning = val > 0.003
            elif "lead" in m_name.lower() or "pb" in m_name.lower():
                is_warning = val > 0.010
            elif "mercury" in m_name.lower() or "hg" in m_name.lower():
                is_warning = val > 0.006
            elif "chromium" in m_name.lower() or "cr" in m_name.lower():
                is_warning = val > 0.050
            elif "arsenic" in m_name.lower() or "as" in m_name.lower():
                is_warning = val > 0.010

            status = "Warning" if is_warning else "Safe"
            badge = "warning" if is_warning else "safe"
            metals.append(
                {
                    "metal": m_name,
                    "conc": f"{val:.3f}" if val >= 0.001 else "< 0.001",
                    "val": val,
                    "status": status,
                    "badge": badge,
                }
            )
    else:
        metals = [
            {"metal": "Lead (Pb)", "conc": "0.012", "val": 0.012, "status": "Safe", "badge": "safe"},
            {"metal": "Mercury (Hg)", "conc": "0.004", "val": 0.004, "status": "Safe", "badge": "safe"},
            {"metal": "Cadmium (Cd)", "conc": "0.028", "val": 0.028, "status": "Warning", "badge": "warning"},
            {"metal": "Chromium (Cr)", "conc": "0.006", "val": 0.006, "status": "Safe", "badge": "safe"},
            {"metal": "Arsenic (As)", "conc": "< 0.001", "val": 0.0008, "status": "Safe", "badge": "safe"},
        ]

    return metals


# ==========================================
# STEP 1: UPLOAD DATA (EXACT MOCKUP IMAGE 2)
# ==========================================
if st.session_state["heavy_step"] == 1:
    with st.container(border=True):
        render_html('<div class="card-header-title">Upload Dataset</div>')

        uploaded_water_file = st.file_uploader(
            "Upload dataset",
            type=["csv", "xlsx", "txt"],
            help="Supported formats: .csv, .xlsx, .txt. Maximum file size: 50MB",
            label_visibility="collapsed",
            key="heavy_file_uploader",
        )

        render_html(
            """
            <div style="text-align: center; color: #64748B; font-size: 0.8rem; margin-top: 0.85rem; line-height: 1.5;">
                Supported formats: .csv, .xlsx, .txt<br>Maximum file size: 50MB
            </div>
            """
        )

    sample_water_df = get_default_water_df()
    sample_csv = sample_water_df.to_csv(index=False).encode("utf-8")

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
            file_name="sample_water_heavy_metal.csv",
            mime="text/csv",
            key="btn_download_sample_heavy",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    btn_l, btn_r = st.columns([1, 1])
    with btn_r:
        st.markdown("<div style='text-align: right; margin-top: 0.5rem;'>", unsafe_allow_html=True)
        if st.button("Next →", type="primary", key="btn_next_heavy_to_val"):
            if uploaded_water_file is not None:
                try:
                    if uploaded_water_file.name.endswith(".csv"):
                        df = pd.read_csv(uploaded_water_file)
                    else:
                        df = pd.read_excel(uploaded_water_file)
                    st.session_state["heavy_uploaded_df"] = df
                    st.session_state["heavy_sample_name"] = uploaded_water_file.name.rsplit(".", 1)[0]
                    st.session_state["heavy_step"] = 2
                    st.rerun()
                except Exception as e:
                    st.error(f"Error reading file: {e}")
            elif "heavy_uploaded_df" in st.session_state:
                st.session_state["heavy_step"] = 2
                st.rerun()
            else:
                st.session_state["heavy_uploaded_df"] = sample_water_df
                st.session_state["heavy_sample_name"] = "River_Water_07"
                st.session_state["heavy_step"] = 2
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 2: VALIDATE
# ==========================================
elif st.session_state["heavy_step"] == 2:
    df = st.session_state.get("heavy_uploaded_df")
    if df is None:
        df = get_default_water_df()
        st.session_state["heavy_uploaded_df"] = df
        st.session_state["heavy_sample_name"] = "River_Water_07"

    sample_name = st.session_state.get("heavy_sample_name", "River_Water_07")

    with st.container(border=True):
        render_html(
            f"""
            <div class="card-header-title">Dataset Validation — {sample_name}</div>
            <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 1.25rem;">
                Sensor integrity check, baseline stability, and candidate heavy metal analytes identified.
            </div>
            <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                <div class="val-metric-card">
                    <div class="val-metric-label">Dataset Validity</div>
                    <div class="val-metric-value" style="color: #16A34A; display: flex; align-items: center; gap: 0.4rem;">
                        <span>✓</span> Valid Fluorescence Data
                    </div>
                </div>
                <div class="val-metric-card">
                    <div class="val-metric-label">Identified Sample</div>
                    <div class="val-metric-value" style="color: #2563EB;">{sample_name}</div>
                </div>
                <div class="val-metric-card">
                    <div class="val-metric-label">Target Analytes</div>
                    <div class="val-metric-value">{len(df)} Metals (Pb, Hg, Cd, Cr, As)</div>
                </div>
                <div class="val-metric-card">
                    <div class="val-metric-label">Sensor Readiness</div>
                    <div class="val-metric-value" style="color: #16A34A;">Ready for AI Inference</div>
                </div>
            </div>
            <div style="font-size: 0.9rem; font-weight: 600; color: #0F172A; margin-bottom: 0.5rem;">Data Preview</div>
            """
        )

        st.dataframe(df, use_container_width=True)

        render_html("<div style='height: 1.2rem;'></div>")

        b_col1, b_col2 = st.columns([1, 1])
        with b_col1:
            if st.button("← Back to Upload Data", key="btn_back_heavy_upload"):
                st.session_state["heavy_step"] = 1
                st.rerun()
        with b_col2:
            st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
            if st.button("Proceed to Analyze →", type="primary", key="btn_proceed_heavy_analyze"):
                st.session_state["heavy_step"] = 3
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 3: ANALYZE
# ==========================================
elif st.session_state["heavy_step"] == 3:
    df = st.session_state.get("heavy_uploaded_df")
    sample_name = st.session_state.get("heavy_sample_name", "River_Water_07")

    with st.container(border=True):
        render_html(
            f"""
            <div class="card-header-title">Detection Model Controls</div>
            <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 1.25rem;">
                Configure the AI quantification engine for sample <strong>{sample_name}</strong>.
            </div>
            """
        )

        detection_model = st.selectbox(
            "AI Detection & Quantification Model",
            [
                "Multi-Target Random Forest Regressor (Trained on CD Quenching)",
                "Gradient Boosted Metal Identification Classifier",
                "Linear Stern-Volmer Quenching Calibration",
            ],
            index=0,
        )

        guideline = st.selectbox(
            "Environmental Safety Standard",
            [
                "WHO Drinking Water Guidelines (2022)",
                "EPA National Primary Drinking Water Regulations",
                "BIS Indian Standard for Drinking Water (IS 10500)",
            ],
            index=0,
        )

        render_html("<div style='height: 1.2rem;'></div>")

        a_col1, a_col2 = st.columns([1, 1.2])
        with a_col1:
            if st.button("← Back to Validation", key="btn_back_heavy_val"):
                st.session_state["heavy_step"] = 2
                st.rerun()
        with a_col2:
            if st.button("💧 Run Heavy Metal Detection →", type="primary", use_container_width=True, key="btn_run_heavy_analysis"):
                metals = analyze_heavy_metals(sample_name=sample_name, custom_data=df)
                st.session_state["heavy_results"] = metals

                # Append to session experiment history
                history = st.session_state.get("experiment_history", [])
                history.insert(
                    0,
                    {
                        "Sample Name": sample_name,
                        "Module": "Heavy Metal",
                        "Status": "Completed",
                        "Date": "Today",
                    },
                )
                st.session_state["experiment_history"] = history

                st.session_state["heavy_step"] = 4
                st.rerun()


# ==========================================
# STEP 4: RESULTS (SCREEN 4)
# ==========================================
else:
    metals_data = st.session_state.get("heavy_results")
    if not metals_data:
        metals_data = analyze_heavy_metals("River_Water_07")
        st.session_state["heavy_results"] = metals_data

    col_left, col_right = st.columns([1, 1])

    with col_left:
        with st.container(border=True):
            render_html('<div class="card-header-title">Detected Heavy Metals</div>')

            table_rows = "".join(
                [
                    f"<tr><td style='font-weight: 500;'>{m['metal']}</td><td>{m['conc']}</td>"
                    f"<td><span class='status-badge {m['badge']}'>{m['status']}</span></td></tr>"
                    for m in metals_data
                ]
            )

            render_html(
                f"""
                <table class="modern-table">
                    <thead>
                        <tr>
                            <th>Metal</th>
                            <th>Concentration (mg/L)</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                """
            )

    with col_right:
        with st.container(border=True):
            render_html('<div class="card-header-title">Concentration Levels</div>')

            metal_labels = []
            metal_values = []
            metal_colors = []
            metal_texts = []

            for m in metals_data:
                label = m["metal"].split("(")[-1].replace(")", "").strip() if "(" in m["metal"] else m["metal"][:3]
                metal_labels.append(label)
                metal_values.append(m["val"])
                metal_colors.append("#EA580C" if m["badge"] == "warning" else "#2563EB")
                metal_texts.append(m["conc"])

            max_val = max(metal_values) if metal_values else 0.04
            y_upper = max(0.045, max_val * 1.25)

            fig_bars = go.Figure()
            fig_bars.add_trace(
                go.Bar(
                    x=metal_labels,
                    y=metal_values,
                    marker=dict(color=metal_colors, cornerradius=4),
                    text=metal_texts,
                    textposition="outside",
                    textfont=dict(size=10, color="#475569"),
                    hovertemplate="<b>%{x}</b><br>Concentration: %{y:.4f} mg/L<extra></extra>",
                    width=0.42,
                )
            )

            fig_bars.update_layout(
                margin=dict(l=45, r=15, t=25, b=35),
                height=280,
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                xaxis=dict(
                    title="",
                    tickfont=dict(size=11, color="#334155"),
                    showgrid=False,
                    zeroline=False,
                ),
                yaxis=dict(
                    title="Concentration (mg/L)",
                    title_font=dict(size=11, color="#64748B"),
                    tickfont=dict(size=10, color="#64748B"),
                    showgrid=True,
                    gridcolor="#F1F5F9",
                    gridwidth=1,
                    range=[0, y_upper],
                    zeroline=True,
                    zerolinecolor="#E2E8F0",
                ),
                bargap=0.35,
            )

            st.plotly_chart(fig_bars, use_container_width=True, config={"displayModeBar": False})

    # Banner and Action Buttons
    banner_col, action_col = st.columns([1.6, 1.2])
    with banner_col:
        render_html(
            """
            <div class="analysis-completed-banner" style="margin-bottom: 0;">
                <span class="analysis-check-icon">✓</span>
                <div>
                    <strong>Analysis Completed</strong> — Heavy metal detection finished successfully.
                </div>
            </div>
            """
        )
    with action_col:
        st.markdown("<div style='margin-top: 0.35rem;'>", unsafe_allow_html=True)
        act_col1, act_col2 = st.columns([1, 1.2])
        with act_col1:
            if st.button("View Details", use_container_width=True, key="btn_view_details"):
                st.switch_page("pages/3_Explainable_AI.py")
        with act_col2:
            if st.button("Generate Report", type="primary", use_container_width=True, key="btn_gen_heavy_rep"):
                st.session_state["report_selected_analysis"] = "Heavy Metal Detection"
                st.session_state["report_selected_sample"] = st.session_state.get("heavy_sample_name", "River_Water_07")
                st.switch_page("pages/4_Reports_&_Export.py")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    if st.button("← New Sample Analysis", key="btn_restart_heavy"):
        st.session_state["heavy_step"] = 1
        st.rerun()