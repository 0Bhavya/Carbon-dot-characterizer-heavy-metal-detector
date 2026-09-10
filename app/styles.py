import streamlit as st


def load_css():
    st.markdown(
        """
        <style>

        /* =========================================
           MAIN APPLICATION
        ========================================= */

        .stApp {
            background: linear-gradient(
                135deg,
                #F8FAFC 0%,
                #EEF6F8 50%,
                #F8FAFC 100%
            );
        }


        /* =========================================
           MAIN CONTENT
        ========================================= */

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }


        /* =========================================
           HEADINGS
        ========================================= */

        h1 {
            color: #0F172A;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        h2 {
            color: #1E293B;
            font-weight: 650;
            margin-top: 1.5rem;
        }

        h3 {
            color: #334155;
        }


        /* =========================================
           SIDEBAR
        ========================================= */

        section[data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #0B1220 0%,
                #0F172A 45%,
                #172554 100%
            );
            border-right: 1px solid rgba(148, 163, 184, 0.18);
        }


        section[data-testid="stSidebar"] > div {
            padding-top: 1.2rem;
        }


        section[data-testid="stSidebar"] * {
            color: #E2E8F0;
        }


        section[data-testid="stSidebar"] a {
            border-radius: 10px;
            padding: 10px 14px;
            margin: 4px 8px;
            min-height: 42px;
            transition: all 0.25s ease;
            font-weight: 500;
            border-left: 3px solid transparent;
        }


        section[data-testid="stSidebar"] a:hover {
            background: rgba(20, 184, 166, 0.16);
            border-left: 3px solid #14B8A6;
            transform: translateX(3px);
        }


        section[data-testid="stSidebar"] a[aria-current="page"] {
            background: linear-gradient(
                90deg,
                rgba(20, 184, 166, 0.28),
                rgba(20, 184, 166, 0.08)
            );
            border-left: 3px solid #2DD4BF;
            font-weight: 700;
            color: white !important;
        }


        /* =========================================
           BUTTONS
        ========================================= */

        .stButton > button {
            background: linear-gradient(
                135deg,
                #0F766E,
                #14B8A6
            );
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.55rem 1.2rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }


        .stButton > button:hover {
            background: linear-gradient(
                135deg,
                #115E59,
                #0D9488
            );
            transform: translateY(-1px);
            box-shadow:
                0px 4px 12px
                rgba(20, 184, 166, 0.25);
        }


        /* =========================================
           METRIC CARDS
        ========================================= */

        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 18px;
            border-radius: 12px;
            box-shadow:
                0px 3px 10px
                rgba(15, 23, 42, 0.06);
        }


        /* =========================================
           INFO BOXES
        ========================================= */

        .stAlert {
            border-radius: 10px;
            border: none;
        }


        /* =========================================
           FILE UPLOADER
        ========================================= */

        [data-testid="stFileUploader"] {
            background: white;
            border-radius: 12px;
            padding: 12px;
            border: 1px solid #CBD5E1;
        }


        /* =========================================
           DATAFRAME
        ========================================= */

        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #E2E8F0;
        }


        /* =========================================
           DIVIDERS
        ========================================= */

        hr {
            border-color: #CBD5E1;
            margin-top: 2rem;
            margin-bottom: 2rem;
        }


        /* =========================================
           EXPANDERS
        ========================================= */

        .streamlit-expanderHeader {
            border-radius: 10px;
        }


        /* =========================================
           MODULE PAGE HERO
           Used by Characterization and future pages
        ========================================= */

        .page-hero {
            width: 100%;
            box-sizing: border-box;

            background: linear-gradient(
                135deg,
                #0F172A 0%,
                #1E3A5F 55%,
                #0F766E 100%
            );

            padding: 42px 48px;

            border-radius: 20px;

            margin-top: 0;
            margin-bottom: 32px;

            box-shadow:
                0 10px 30px
                rgba(15, 23, 42, 0.20);

            color: #FFFFFF;
        }


        /* HERO TAG */

        .page-hero .page-hero-tag {
            display: inline-block;

            padding: 7px 16px;

            background:
                rgba(255, 255, 255, 0.12);

            border:
                1px solid
                rgba(255, 255, 255, 0.22);

            border-radius: 20px;

            font-size: 12px;
            font-weight: 600;

            letter-spacing: 0.7px;

            margin-bottom: 20px;

            color: #CCFBF1 !important;
        }


        /* HERO TITLE */

        .page-hero .page-hero-title {
            display: block;

            font-size: 42px;
            font-weight: 750;

            line-height: 1.2;

            letter-spacing: -1px;

            margin-bottom: 14px;

            color: #FFFFFF !important;
        }


        /* HERO SUBTITLE */

        .page-hero .page-hero-subtitle {
            display: block;

            font-size: 17px;

            font-weight: 400;

            line-height: 1.7;

            max-width: 850px;

            color: #DCE6F2 !important;
        }


        /* =========================================
           RESPONSIVE
        ========================================= */

        @media (max-width: 768px) {

            .page-hero {
                padding: 28px 25px;
                border-radius: 14px;
            }

            .page-hero .page-hero-title {
                font-size: 30px;
            }

            .page-hero .page-hero-subtitle {
                font-size: 15px;
            }

        }

        </style>
        """,
        unsafe_allow_html=True,
    )