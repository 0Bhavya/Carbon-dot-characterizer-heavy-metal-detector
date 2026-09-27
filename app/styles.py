import streamlit as st


def render_html(html_str: str):
    """
    Renders HTML safely into Streamlit without indentation
    issues where Markdown treats 4 leading spaces as a code block.
    """
    clean_lines = [line.strip() for line in html_str.strip().splitlines() if line.strip()]
    st.markdown("".join(clean_lines), unsafe_allow_html=True)


def load_css():
    st.markdown(
        """
        <style>
        :root {
            --bg-page: #F8FAFC;
            --bg-card: #FFFFFF;
            --border-color: #E2E8F0;
            --border-light: #F1F5F9;
            --text-dark: #0F172A;
            --text-body: #334155;
            --text-muted: #64748B;
            --primary: #2563EB;
            --primary-hover: #1D4ED8;
            --primary-light: #EFF6FF;
            --primary-border: #BFDBFE;
            --success: #16A34A;
            --success-bg: #DCFCE7;
            --success-border: #BBF7D0;
            --warning: #EA580C;
            --warning-bg: #FEF3C7;
            --warning-border: #FDE68A;
            --danger: #DC2626;
            --danger-bg: #FEE2E2;
            --danger-border: #FECACA;
        }

        /* Fast system fonts - zero network delay */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: var(--bg-page) !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
            color: var(--text-body) !important;
        }

        .block-container {
            padding-top: 1.25rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 1380px !important;
        }

        /* Top Shell Header Bar */
        .app-shell-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 0.65rem 1rem;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
            margin-bottom: 1.25rem;
        }

        .app-shell-brand {
            display: flex;
            align-items: center;
            gap: 0.65rem;
        }

        .app-shell-logo {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.9rem;
            height: 1.9rem;
            border-radius: 8px;
            background: #EFF6FF;
            color: #2563EB;
            font-size: 1.05rem;
            border: 1px solid #DBEAFE;
        }

        .app-shell-name {
            color: #0F172A;
            font-size: 0.98rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .app-shell-actions {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .app-shell-toggle {
            display: inline-flex;
            align-items: center;
            justify-content: space-between;
            width: 2.7rem;
            height: 1.45rem;
            border-radius: 999px;
            background: #E2E8F0;
            border: 1px solid #CBD5E1;
            padding: 0 0.25rem;
            position: relative;
        }

        .app-shell-toggle::before {
            content: "";
            width: 1rem;
            height: 1rem;
            border-radius: 50%;
            background: #FFFFFF;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
        }

        .app-shell-toggle::after {
            content: "☀";
            font-size: 0.68rem;
            color: #64748B;
            margin-right: 0.15rem;
        }

        # .app-shell-avatar {
        #     display: inline-flex;
        #     align-items: center;
        #     justify-content: center;
        #     width: 1.85rem;
        #     height: 1.85rem;
        #     border-radius: 50%;
        #     background: #E2E8F0;
        #     color: #0F172A;
        #     font-size: 0.78rem;
        #     font-weight: 700;
        # }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid var(--border-color) !important;
            box-shadow: none !important;
            width: 250px !important;
        }

        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }

        section[data-testid="stSidebar"] a {
            border-radius: 8px !important;
            padding: 0.55rem 0.85rem !important;
            margin: 0.2rem 0 !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            color: #334155 !important;
            transition: all 0.15s ease !important;
            border: 1px solid transparent !important;
        }

        section[data-testid="stSidebar"] a:hover {
            background-color: #F1F5F9 !important;
            color: #0F172A !important;
        }

        section[data-testid="stSidebar"] a[aria-current="page"] {
            background-color: #EFF6FF !important;
            color: #2563EB !important;
            font-weight: 600 !important;
            border-color: #DBEAFE !important;
        }

        /* Page Headers */
        .page-tag {
            color: #64748B;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }

        .page-title {
            color: #0F172A;
            font-size: 1.75rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            margin: 0;
            line-height: 1.25;
        }

        .page-subtitle {
            color: #475569;
            font-size: 0.92rem;
            line-height: 1.5;
            margin-top: 0.25rem;
            margin-bottom: 1.1rem;
        }

        /* Stepper Navigation */
        .stepper-wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
            max-width: 680px;
            margin: 0.5rem auto 1.5rem auto;
            position: relative;
        }

        .stepper-step {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            background: transparent;
            z-index: 2;
            padding: 0.2rem 0.5rem;
        }

        .stepper-circle {
            width: 1.8rem;
            height: 1.8rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.78rem;
            font-weight: 700;
            background: #FFFFFF;
            color: #64748B;
            border: 2px solid #CBD5E1;
            transition: all 0.2s ease;
        }

        .stepper-circle.active {
            background: #2563EB;
            color: #FFFFFF;
            border-color: #2563EB;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
        }

        .stepper-circle.completed {
            background: #2563EB;
            color: #FFFFFF;
            border-color: #2563EB;
        }

        .stepper-label {
            font-size: 0.82rem;
            font-weight: 500;
            color: #64748B;
        }

        .stepper-label.active {
            color: #0F172A;
            font-weight: 700;
        }

        .stepper-label.completed {
            color: #2563EB;
            font-weight: 600;
        }

        .stepper-divider {
            flex: 1;
            height: 2px;
            background: #E2E8F0;
            margin: 0 0.4rem;
            z-index: 1;
        }

        .stepper-divider.completed {
            background: #2563EB;
        }

        /* Native Container Border Styling */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            background: #FFFFFF !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
            padding: 1.15rem 1.25rem !important;
            margin-bottom: 0.75rem !important;
        }

        /* Card title inside containers */
        .card-header-title {
            color: #0F172A;
            font-size: 0.98rem;
            font-weight: 700;
            margin: 0 0 0.85rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Exact Mockup Dropzone Styling (Image 2) */
        [data-testid="stFileUploader"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }

        [data-testid="stFileUploader"] > label {
            display: none !important;
        }

        [data-testid="stFileUploaderDropzone"] {
            background-color: #F8FBFF !important;
            border: 1.5px dashed #93C5FD !important;
            border-radius: 12px !important;
            padding: 2.2rem 1.5rem !important;
            text-align: center !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: #2563EB !important;
            background-color: #EFF6FF !important;
        }

        [data-testid="stFileUploaderDropzone"] svg {
            width: 2.5rem !important;
            height: 2.5rem !important;
            color: #2563EB !important;
            stroke: #2563EB !important;
            margin-bottom: 0.5rem !important;
        }

        [data-testid="stFileUploaderDropzone"] button {
            background: #FFFFFF !important;
            border: 1px solid #2563EB !important;
            color: #2563EB !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 0.45rem 1.3rem !important;
            box-shadow: 0 1px 2px rgba(37, 99, 235, 0.05) !important;
            margin-top: 0.5rem !important;
        }

        [data-testid="stFileUploaderDropzone"] button:hover {
            background: #EFF6FF !important;
            border-color: #1D4ED8 !important;
            color: #1D4ED8 !important;
        }

        /* Sample Dataset Download Outline Button */
        .sample-download-btn div[data-testid="stDownloadButton"] > button,
        .sample-download-btn div.stButton > button {
            background: #FFFFFF !important;
            border: 1px solid #2563EB !important;
            color: #2563EB !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 0.45rem 1.1rem !important;
            box-shadow: none !important;
        }

        .sample-download-btn div[data-testid="stDownloadButton"] > button:hover,
        .sample-download-btn div.stButton > button:hover {
            background: #EFF6FF !important;
            border-color: #1D4ED8 !important;
            color: #1D4ED8 !important;
        }

        /* Validation metric card */
        .val-metric-card {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 0.9rem 1rem;
        }

        .val-metric-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.35rem;
        }

        .val-metric-value {
            font-size: 1.05rem;
            font-weight: 700;
            color: #0F172A;
        }

        /* Status Banner */
        .analysis-completed-banner {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            background: #F0FDF4;
            border: 1px solid #BBF7D0;
            border-radius: 10px;
            padding: 0.75rem 1rem;
            color: #166534;
            font-size: 0.88rem;
            margin-top: 1.2rem;
            margin-bottom: 0.8rem;
        }

        .analysis-completed-banner strong {
            font-weight: 700;
            color: #14532D;
        }

        .analysis-check-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.35rem;
            height: 1.35rem;
            border-radius: 50%;
            background: #22C55E;
            color: #FFFFFF;
            font-size: 0.75rem;
            font-weight: 800;
        }

        /* Status Badges */
        .status-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.22rem 0.65rem;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 600;
            line-height: 1.2;
        }

        .status-badge.safe {
            background: #DCFCE7;
            color: #166534;
            border: 1px solid #BBF7D0;
        }

        .status-badge.warning {
            background: #FEF3C7;
            color: #92400E;
            border: 1px solid #FDE68A;
        }

        .status-badge.completed {
            background: #DCFCE7;
            color: #166534;
            border: 1px solid #BBF7D0;
        }

        .status-badge.processing {
            background: #FEF3C7;
            color: #92400E;
            border: 1px solid #FDE68A;
        }

        /* Modern Table */
        .modern-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            color: #0F172A;
        }

        .modern-table th {
            text-align: left;
            padding: 0.65rem 0.75rem;
            font-size: 0.75rem;
            font-weight: 600;
            color: #475569;
            border-bottom: 1px solid var(--border-color);
            background: #F8FAFC;
        }

        .modern-table td {
            padding: 0.7rem 0.75rem;
            border-bottom: 1px solid var(--border-color);
            vertical-align: middle;
        }

        .modern-table tr:last-child td {
            border-bottom: none;
        }

        /* Button overrides */
        div.stButton > button,
        div[data-testid="stDownloadButton"] > button {
            border-radius: 8px !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            padding: 0.45rem 1rem !important;
            transition: all 0.15s ease !important;
        }

        div.stButton > button[kind="primary"],
        div.stButton > button[data-testid="stBaseButton-primary"] {
            background-color: #2563EB !important;
            border-color: #2563EB !important;
            color: #FFFFFF !important;
            box-shadow: none !important;
        }

        div.stButton > button[kind="primary"]:hover,
        div.stButton > button[data-testid="stBaseButton-primary"]:hover {
            background-color: #1D4ED8 !important;
            border-color: #1D4ED8 !important;
        }

        div.stButton > button[kind="secondary"],
        div.stButton > button[data-testid="stBaseButton-secondary"] {
            background-color: #FFFFFF !important;
            border: 1px solid var(--border-color) !important;
            color: #334155 !important;
            box-shadow: none !important;
        }

        div.stButton > button[kind="secondary"]:hover,
        div.stButton > button[data-testid="stBaseButton-secondary"]:hover {
            background-color: #F8FAFC !important;
            border-color: #CBD5E1 !important;
            color: #0F172A !important;
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1.5rem !important;
            border-bottom: 1px solid #E2E8F0 !important;
            background: transparent !important;
            padding-bottom: 0.2rem !important;
        }

        .stTabs [data-baseweb="tab"] {
            height: auto !important;
            padding: 0.5rem 0.2rem !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            color: #64748B !important;
            background: transparent !important;
            border: none !important;
        }

        .stTabs [aria-selected="true"] {
            color: #2563EB !important;
            font-weight: 600 !important;
            border-bottom: 2px solid #2563EB !important;
        }

        /* Probability Bars */
        .prob-bar-wrapper {
            margin-bottom: 0.85rem;
        }

        .prob-bar-header {
            display: flex;
            justify-content: space-between;
            font-size: 0.82rem;
            font-weight: 600;
            color: #0F172A;
            margin-bottom: 0.35rem;
        }

        .prob-bar-track {
            width: 100%;
            height: 0.75rem;
            background: #F1F5F9;
            border-radius: 999px;
            overflow: hidden;
        }

        .prob-bar-fill {
            height: 100%;
            border-radius: 999px;
        }

        .prob-bar-fill.green {
            background: #22C55E;
        }

        .prob-bar-fill.orange {
            background: #F59E0B;
        }

        .prob-bar-fill.red {
            background: #EF4444;
        }

        /* Document Paper Preview */
        .report-preview-sheet {
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 8px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
            padding: 2rem 1.5rem;
            min-height: 380px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .report-preview-sheet .doc-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0F172A;
            margin-top: 0.5rem;
            margin-bottom: 0.2rem;
        }

        .report-preview-sheet .doc-subtitle {
            font-size: 0.9rem;
            color: #64748B;
            font-weight: 500;
            margin-bottom: 1.5rem;
        }

        .report-preview-sheet .doc-meta {
            width: 100%;
            border-top: 1px solid #E2E8F0;
            border-bottom: 1px solid #E2E8F0;
            padding: 0.85rem 0;
            margin-bottom: 1.5rem;
            text-align: left;
            font-size: 0.82rem;
            color: #334155;
            line-height: 1.7;
        }

        .report-preview-sheet .doc-preview-body {
            width: 100%;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            padding: 0.75rem;
            font-size: 0.78rem;
            color: #64748B;
            text-align: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_app_shell_header():
    """Renders the top branding bar in light theme."""

    render_html(
        """
        <div class="app-shell-header">
            <div class="app-shell-brand">
                <div class="app-shell-logo">💧</div>
                <div class="app-shell-name">Carbon Dot Characterizer</div>
            </div>
        </div>
        """
    )

def render_stepper(current_step: int, module_prefix: str = "char"):
    """
    Renders the 4-step wizard:
    1 Upload Data -> 2 Validate -> 3 Analyze -> 4 Results
    """
    steps = [
        (1, "Upload Data"),
        (2, "Validate"),
        (3, "Analyze"),
        (4, "Results"),
    ]

    html_parts = ['<div class="stepper-wrapper">']
    for idx, (num, name) in enumerate(steps):
        is_active = num == current_step
        is_completed = num < current_step

        circle_class = "stepper-circle"
        label_class = "stepper-label"

        if is_active:
            circle_class += " active"
            label_class += " active"
        elif is_completed:
            circle_class += " completed"
            label_class += " completed"

        html_parts.append(
            f'<div class="stepper-step"><div class="{circle_class}">{num}</div><span class="{label_class}">{name}</span></div>'
        )

        if idx < len(steps) - 1:
            divider_class = "stepper-divider"
            if num < current_step:
                divider_class += " completed"
            html_parts.append(f'<div class="{divider_class}"></div>')

    html_parts.append("</div>")
    render_html("".join(html_parts))