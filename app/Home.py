import streamlit as st
from styles import load_css


st.set_page_config(
    page_title="Carbon Dot Characterizer",
    page_icon="🧪",
    layout="wide",
)

st.markdown(
    """
    <style>

    /* Main page spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Hero section */
    .hero-container {
        padding: 55px 60px;
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            #0F172A 0%,
            #1E3A5F 50%,
            #0F766E 100%
        );
        color: white;
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.25);
    }

    .hero-title {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 15px;
        color: white;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 20px;
        line-height: 1.6;
        color: #DCE6F2;
        max-width: 850px;
    }

    .hero-tag {
        display: inline-block;
        background-color: rgba(255,255,255,0.15);
        padding: 7px 16px;
        border-radius: 20px;
        font-size: 14px;
        margin-bottom: 18px;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Feature cards */
    .feature-card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        min-height: 150px;
        transition: 0.3s;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.10);
    }

    .feature-icon {
        font-size: 30px;
        margin-bottom: 10px;
    }

    .feature-title {
        font-size: 18px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 8px;
    }

    .feature-text {
        color: #64748B;
        font-size: 14px;
        line-height: 1.5;
    }

    /* Workflow dashboard */
    .workflow-section {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 20px;
        margin: 8px 0 12px;
    }

    .workflow-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.07);
        min-height: 150px;
        padding: 24px;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .workflow-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.12);
    }

    .workflow-number {
        align-items: center;
        background: #0F766E;
        border-radius: 50%;
        color: white;
        display: flex;
        font-size: 14px;
        font-weight: 700;
        height: 38px;
        justify-content: center;
        margin-bottom: 18px;
        width: 38px;
    }

    .workflow-title {
        color: #0F172A;
        font-size: 17px;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 8px;
    }

    .workflow-text {
        color: #64748B;
        font-size: 14px;
        line-height: 1.5;
        margin: 0;
    }

    @media (max-width: 900px) {
        .workflow-section {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 600px) {
        .workflow-section {
            grid-template-columns: 1fr;
        }
    }

    /* Platform module cards */
    .module-section {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 20px;
        margin: 8px 0 12px;
    }

    .module-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.07);
        min-height: 190px;
        padding: 24px;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .module-card:hover {
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.12);
        transform: translateY(-5px);
    }

    .module-icon {
        font-size: 30px;
        line-height: 1;
        margin-bottom: 18px;
    }

    .module-title {
        color: #0F172A;
        font-size: 18px;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 8px;
    }

    .module-text {
        color: #64748B;
        font-size: 14px;
        line-height: 1.5;
        margin: 0;
    }

    .module-link {
        margin-top: -12px;
    }

    .module-link a {
        color: #0F766E !important;
        font-size: 14px;
        font-weight: 700;
        text-decoration: none;
    }

    .module-link a:hover {
        color: #1E3A5F !important;
        text-decoration: underline;
    }

    @media (max-width: 900px) {
        .module-section {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 600px) {
        .module-section {
            grid-template-columns: 1fr;
        }
    }

    /* Getting started guide */
    .getting-started-section {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 20px;
        margin: 18px 0 12px;
    }

    .getting-started-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.07);
        min-height: 180px;
        padding: 24px;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .getting-started-card:hover {
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.12);
        transform: translateY(-5px);
    }

    .getting-started-top {
        align-items: center;
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
    }

    .getting-started-number {
        align-items: center;
        background: #0F766E;
        border-radius: 50%;
        color: #FFFFFF;
        display: flex;
        flex: 0 0 auto;
        font-size: 13px;
        font-weight: 700;
        height: 36px;
        justify-content: center;
        width: 36px;
    }

    .getting-started-icon {
        font-size: 25px;
        line-height: 1;
    }

    .getting-started-title {
        color: #0F172A;
        font-size: 17px;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 9px;
    }

    .getting-started-text {
        color: #64748B;
        font-size: 14px;
        line-height: 1.5;
        margin: 0;
    }

    @media (max-width: 1000px) {
        .getting-started-section {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 600px) {
        .getting-started-section {
            grid-template-columns: 1fr;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)
load_css()

hero_html = """
<div class="hero-container">
<div class="hero-tag">
🧪 AI-Powered Scientific Analysis Platform
</div>
<div class="hero-title">
Carbon Dot Intelligence Platform
</div>
<div class="hero-subtitle">
An intelligent platform for carbon dot characterization,
fluorescence and spectroscopy analysis, heavy metal detection,
and explainable artificial intelligence.
</div>
</div>
"""

st.markdown(
    hero_html,
    unsafe_allow_html=True,
)

feature_columns = st.columns(4)

feature_items = [
    (
        "🔬",
        "Carbon Dot Analysis",
        "Characterize carbon dots through fluorescence and spectroscopy analysis.",
    ),
    (
        "🧪",
        "Heavy Metal Detection",
        "Analyze experiments and identify heavy metal targets with confidence.",
    ),
    (
        "🧠",
        "Explainable AI",
        "Understand model results through clear, human-readable explanations.",
    ),
    (
        "📊",
        "Reports & Export",
        "Turn findings into organized reports and shareable analysis outputs.",
    ),
]

for column, (icon, title, description) in zip(feature_columns, feature_items):
    with column:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-text">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# About Section
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


# Workflow Section
st.header("Workflow")

workflow_steps = [
    (
        "Upload and Analyze Data",
        "Prepare experiment files for analysis.",
    ),
    (
        "Characterize Carbon Dots",
        "Review fluorescence and spectroscopy properties.",
    ),
    (
        "Detect Heavy Metals",
        "Analyze targets and detection experiment results.",
    ),
    (
        "Generate Explainable AI Results",
        "Interpret model findings with transparent explanations.",
    ),
    (
        "Export Reports",
        "Create organized reports for sharing and review.",
    ),
    (
        "Review Analysis History",
        "Revisit completed experiments and previous findings.",
    ),
]

workflow_cards = "".join(
    f"""
<div class="workflow-card">
<div class="workflow-number">{index:02d}</div>
<div class="workflow-title">{title}</div>
<p class="workflow-text">{description}</p>
</div>
"""
    for index, (title, description) in enumerate(workflow_steps, start=1)
)

st.markdown(
    f"""
<div class="workflow-section">
{workflow_cards}
</div>
""",
    unsafe_allow_html=True,
)


# Platform Modules
st.header("Platform Modules")

modules = [
    (
        "🔬",
        "Carbon Dot Characterization",
        "Explore carbon dot fluorescence and spectroscopy characterization results.",
        "pages/1_Characterization.py",
    ),
    (
        "🧪",
        "Heavy Metal Detection",
        "Review heavy metal detection workflows, targets, and experiment results.",
        "pages/2_Heavy_Metal_Detection.py",
    ),
    (
        "🧠",
        "Explainable AI",
        "Understand the reasoning behind detection results through explainable outputs.",
        "pages/3_Explainable_AI.py",
    ),
    (
        "📊",
        "Reports and Export",
        "Prepare and export characterization and detection reports.",
        "pages/4_Reports_Export.py",
    ),
    (
        "🕘",
        "Analysis History",
        "Review previous experiments and keep track of completed analyses.",
        "pages/5_History.py",
    ),
]

module_columns = st.columns(3)

for index, (icon, title, description, page_path) in enumerate(modules):
    with module_columns[index % 3]:
        st.markdown(
            f"""
<div class="module-card">
<div class="module-icon">{icon}</div>
<div class="module-title">{title}</div>
<p class="module-text">{description}</p>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="module-link">', unsafe_allow_html=True)
        st.page_link(page_path, label="Open Module →")
        st.markdown("</div>", unsafe_allow_html=True)


# How to Use Section
st.header("How to Get Started")
st.write("Follow these simple steps to begin your carbon dot analysis workflow.")

getting_started_steps = [
    (
        "01",
        "📤",
        "Upload Your Data",
        "Start from Carbon Dot Characterization and upload fluorescence or spectroscopy data.",
    ),
    (
        "02",
        "🔬",
        "Analyze and Detect",
        "Characterize the carbon dots and continue to Heavy Metal Detection.",
    ),
    (
        "03",
        "🧠",
        "Understand the Results",
        "Use Explainable AI to understand the model predictions and results.",
    ),
    (
        "04",
        "📊",
        "Export and Review",
        "Generate reports and revisit previous experiments using Analysis History.",
    ),
]

getting_started_cards = "".join(
    f"""
<div class="getting-started-card">
<div class="getting-started-top">
<div class="getting-started-number">{number}</div>
<div class="getting-started-icon">{icon}</div>
</div>
<div class="getting-started-title">{title}</div>
<p class="getting-started-text">{description}</p>
</div>
"""
    for number, icon, title, description in getting_started_steps
)

st.markdown(
    f"""
<div class="getting-started-section">
{getting_started_cards}
</div>
""",
    unsafe_allow_html=True,
)