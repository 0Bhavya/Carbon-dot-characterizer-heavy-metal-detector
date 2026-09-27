import streamlit as st
from styles import load_css, render_app_shell_header, render_html

st.set_page_config(
    page_title="Dashboard - Carbon Dot Characterizer",
    page_icon="💧",
    layout="wide",
)

load_css()
render_app_shell_header()

# Header
render_html(
    """
    <div style="margin-bottom: 1.25rem;">
        <div class="page-tag">SCIENTIFIC ANALYSIS PLATFORM</div>
        <div class="page-title">Dashboard</div>
        <div class="page-subtitle">Start a new analysis or continue previous work.</div>
    </div>
    """
)

if st.button("+ New Analysis", key="btn_new_analysis", type="primary"):
    st.switch_page("pages/1_Characterization.py")

render_html("<div style='height: 1.2rem;'></div>")

# Analysis Modules
render_html(
    """
    <div style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin-bottom: 0.85rem;">
        Analysis Modules
    </div>
    """
)

modules = [
    {
        "icon": "🔬",
        "icon_bg": "#EFF6FF",
        "icon_border": "#BFDBFE",
        "title": "Characterization",
        "desc": "Analyze optical and structural properties.",
        "page": "pages/1_Characterization.py",
        "key": "mod_char",
    },
    {
        "icon": "💧",
        "icon_bg": "#F0FDF4",
        "icon_border": "#BBF7D0",
        "title": "Heavy Metal Detection",
        "desc": "Detect and quantify heavy metals in water.",
        "page": "pages/2_Heavy_Metal_Detection.py",
        "key": "mod_heavy",
    },
    {
        "icon": "📊",
        "icon_bg": "#FAF5FF",
        "icon_border": "#E9D5FF",
        "title": "Explainable AI",
        "desc": "Understand model predictions.",
        "page": "pages/3_Explainable_AI.py",
        "key": "mod_xai",
    },
    {
        "icon": "📄",
        "icon_bg": "#FFFBEB",
        "icon_border": "#FDE68A",
        "title": "Reports & Export",
        "desc": "Generate and export analysis reports.",
        "page": "pages/4_Reports_&_Export.py",
        "key": "mod_rep",
    },
]

cols = st.columns(4)
for idx, mod in enumerate(modules):
    with cols[idx]:
        with st.container(border=True):
            render_html(
                f"""
                <div style="display: flex; flex-direction: column; min-height: 120px;">
                    <div style="display: inline-flex; align-items: center; justify-content: center; width: 2.2rem; height: 2.2rem; border-radius: 8px; background: {mod['icon_bg']}; border: 1px solid {mod['icon_border']}; font-size: 1.1rem; margin-bottom: 0.75rem;">
                        {mod['icon']}
                    </div>
                    <div style="font-size: 0.95rem; font-weight: 700; color: #0F172A; margin-bottom: 0.25rem;">
                        {mod['title']}
                    </div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.45;">
                        {mod['desc']}
                    </div>
                </div>
                """
            )
            st.markdown('<div class="mod-link-btn">', unsafe_allow_html=True)
            if st.button("Open →", key=mod["key"]):
                st.switch_page(mod["page"])
            st.markdown("</div>", unsafe_allow_html=True)

render_html("<div style='height: 1.2rem;'></div>")

# Lower Section: Recent Analyses & System Status
left_col, right_col = st.columns([1.65, 1])

with left_col:
    with st.container(border=True):
        render_html('<div class="card-header-title">Recent Analyses</div>')
        analyses = st.session_state.get("experiment_history", [])

        if analyses:
            rows_html = []
            for idx, item in enumerate(analyses[:5], start=1):
                sample = item.get("Sample Name", "Sample")
                module = item.get("Module", "General")
                status = item.get("Status", "Completed")
                date = item.get("Date", "Today")
                badge_class = "completed" if status.lower() == "completed" else "processing"

                rows_html.append(
                    f"<tr><td>{idx}</td><td style='font-weight: 500;'>{sample}</td><td>{module}</td>"
                    f"<td><span class='status-badge {badge_class}'>{status}</span></td>"
                    f"<td style='color: #64748B;'>{date}</td></tr>"
                )

            render_html(
                f"""
                <table class="modern-table">
                    <thead>
                        <tr>
                            <th style="width: 35px;">#</th>
                            <th>Sample Name</th>
                            <th>Module</th>
                            <th>Status</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rows_html)}
                    </tbody>
                </table>
                """
            )
        else:
            render_html(
                """
                <div style="background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 10px; padding: 1.8rem 1.2rem; text-align: center;">
                    <div style="font-weight: 600; color: #0F172A; font-size: 0.92rem; margin-bottom: 0.25rem;">No analyses yet</div>
                    <div style="font-size: 0.82rem; color: #64748B; margin-bottom: 0.75rem;">Upload spectroscopy data or water sample to see your results here.</div>
                </div>
                """
            )
            # Give optional demo button only if user explicitly wants to preview reference layout
            if st.button("⚡ Preview Demo Analyses (Reference UI)", key="btn_load_demo_history"):
                st.session_state["experiment_history"] = [
                    {"Sample Name": "River_Water_07", "Module": "Heavy Metal", "Status": "Completed", "Date": "12 Sep 2026"},
                    {"Sample Name": "Water_Sample_12", "Module": "Characterization", "Status": "Processing", "Date": "11 Sep 2026"},
                    {"Sample Name": "CD_Sample_A3", "Module": "Explainable AI", "Status": "Completed", "Date": "10 Sep 2026"},
                ]
                st.rerun()

with right_col:
    with st.container(border=True):
        render_html(
            """
            <div class="card-header-title">System Status</div>
            <div style="display: flex; flex-direction: column; gap: 0.9rem; padding: 0.25rem 0;">
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.88rem;">
                    <div style="display: flex; align-items: center; gap: 0.6rem;">
                        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #22C55E;"></span>
                        <span style="font-weight: 500; color: #0F172A;">Dataset</span>
                    </div>
                    <span style="color: #16A34A; font-weight: 600; font-size: 0.82rem;">Ready</span>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.88rem;">
                    <div style="display: flex; align-items: center; gap: 0.6rem;">
                        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #22C55E;"></span>
                        <span style="font-weight: 500; color: #0F172A;">ML Models</span>
                    </div>
                    <span style="color: #16A34A; font-weight: 600; font-size: 0.82rem;">Ready</span>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.88rem;">
                    <div style="display: flex; align-items: center; gap: 0.6rem;">
                        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #22C55E;"></span>
                        <span style="font-weight: 500; color: #0F172A;">XAI Engine</span>
                    </div>
                    <span style="color: #16A34A; font-weight: 600; font-size: 0.82rem;">Ready</span>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.88rem;">
                    <div style="display: flex; align-items: center; gap: 0.6rem;">
                        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #22C55E;"></span>
                        <span style="font-weight: 500; color: #0F172A;">Reporting</span>
                    </div>
                    <span style="color: #16A34A; font-weight: 600; font-size: 0.82rem;">Ready</span>
                </div>
            </div>
            """
        )
