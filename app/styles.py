import streamlit as st


def load_css():
    st.markdown(
        """
        <style>

        /* MAIN APPLICATION */
        .stApp {
            background: linear-gradient(
                135deg,
                #F8FAFC 0%,
                #EEF6F8 50%,
                #F8FAFC 100%
            );
        }


        /* MAIN CONTENT */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }


        /* HEADINGS */
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


        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #0F172A,
                #172554
            );
        }

        section[data-testid="stSidebar"] * {
            color: #E2E8F0;
        }


        /* SIDEBAR NAVIGATION */
        section[data-testid="stSidebar"] a {
            border-radius: 8px;
            padding: 8px 12px;
            margin: 3px 6px;
            transition: 0.2s;
        }

        section[data-testid="stSidebar"] a:hover {
            background-color: rgba(20, 184, 166, 0.25);
        }


        /* BUTTONS */
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
            transition: 0.2s;
        }

        .stButton > button:hover {
            background: linear-gradient(
                135deg,
                #115E59,
                #0D9488
            );
            transform: translateY(-1px);
            box-shadow: 0px 4px 12px rgba(20, 184, 166, 0.25);
        }


        /* METRIC CARDS */
        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid #E2E8F0;
            padding: 18px;
            border-radius: 12px;
            box-shadow: 0px 3px 10px rgba(15, 23, 42, 0.06);
        }


        /* INFO BOXES */
        .stAlert {
            border-radius: 10px;
            border: none;
        }


        /* FILE UPLOADER */
        [data-testid="stFileUploader"] {
            background: white;
            border-radius: 12px;
            padding: 12px;
            border: 1px solid #CBD5E1;
        }


        /* SELECT BOX */
        .stSelectbox > div > div {
            border-radius: 8px;
        }


        /* DATAFRAME */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #E2E8F0;
        }


        /* HORIZONTAL DIVIDER */
        hr {
            border-color: #CBD5E1;
            margin-top: 2rem;
            margin-bottom: 2rem;
        }


        /* CHECKBOX */
        .stCheckbox {
            padding-top: 5px;
        }


        /* EXPANDERS */
        .streamlit-expanderHeader {
            border-radius: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )