
import streamlit as st
import pandas as pd
import requests
import os

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="DataSentinel AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. CUSTOM CSS - PROFESSIONAL LIGHT THEME
# =====================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F3F6FC;
}

/* Main text */
.stApp,
.stApp p,
.stApp label,
.stApp li,
.stApp span {
    color: #172554;
}

/* Main headings */
h1, h2, h3, h4 {
    color: #172554 !important;
    font-weight: 750 !important;
}

/* Main title */
.main-title {
    color: #243B85 !important;
    font-size: 42px;
    font-weight: 850;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    color: #475569 !important;
    font-size: 17px;
    margin-bottom: 20px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #172554 !important;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D5DFF0;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 3px 10px rgba(30, 50, 100, 0.07);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #475569 !important;
}

[data-testid="stMetricValue"] {
    color: #2457C5 !important;
}

/* Buttons */
.stButton > button {
    background-color: #4F46E5 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    min-height: 46px;
}

.stButton > button p {
    color: #FFFFFF !important;
}

.stButton > button:hover {
    background-color: #3730A3 !important;
    color: #FFFFFF !important;
}

/* Download button */
.stDownloadButton > button {
    background-color: #047857 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    min-height: 45px;
}

.stDownloadButton > button p {
    color: #FFFFFF !important;
}

/* Text inputs */
.stTextInput label {
    color: #172554 !important;
    font-weight: 650 !important;
}

.stTextInput input {
    background-color: #FFFFFF !important;
    color: #172554 !important;
    border: 1px solid #A5B4FC !important;
    border-radius: 9px !important;
}

.stTextInput input::placeholder {
    color: #64748B !important;
    opacity: 1;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #FFFFFF !important;
    border: 2px dashed #818CF8 !important;
    border-radius: 14px !important;
    padding: 18px;
}

[data-testid="stFileUploader"] * {
    color: #172554 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    color: #334155 !important;
    font-weight: 650 !important;
}

.stTabs [aria-selected="true"] {
    color: #4338CA !important;
}

/* Expanders */
[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D9E3F5 !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color: #172554 !important;
    font-weight: 650 !important;
}

/* Alerts */
[data-testid="stAlert"] p {
    color: #172554 !important;
}

/* Report text */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #263449 !important;
    line-height: 1.7;
}

[data-testid="stMarkdownContainer"] strong {
    color: #172554 !important;
}

/* Dataframe container */
[data-testid="stDataFrame"] {
    background-color: #FFFFFF !important;
    border-radius: 12px;
}

/* Section cards */
.section-card {
    background-color: #FFFFFF;
    padding: 22px;
    border: 1px solid #D9E3F5;
    border-radius: 14px;
    margin-bottom: 15px;
}

/* Footer */
.footer {
    text-align: center;
    color: #475569 !important;
    font-size: 14px;
}

/* Dividers */
hr {
    border-color: #CBD5E1 !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. N8N WEBHOOK CONFIGURATION
# =====================================================

try:
    N8N_WEBHOOK_URL = st.secrets.get(
        "N8N_WEBHOOK_URL", ""
    )
except Exception:
    N8N_WEBHOOK_URL = os.getenv(
        "N8N_WEBHOOK_URL", ""
    )


# =====================================================
# 4. SESSION STATE
# =====================================================

if "report" not in st.session_state:
    st.session_state.report = ""

if "report_file_name" not in st.session_state:
    st.session_state.report_file_name = ""


# =====================================================
# 5. SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🛡️ DataSentinel AI")

    st.markdown("---")

    st.subheader("Navigation")

    page = st.radio(
        "Choose Page",
        [
            "Dataset Analyzer",
            "About Project"
        ]
    )

    st.markdown("---")

    st.subheader("🤖 AI Specialist Agents")

    st.markdown("""
    🔍 Data Quality Auditor

    ⚠️ ML Risk Analyst

    🧠 ML Strategy Advisor

    📊 Final Report Generator
    """)

    st.markdown("---")

    st.caption("Powered by Multi-Agent AI")
    st.caption("Streamlit + n8n + Gemini")


# =====================================================
# 6. MAIN HEADER
# =====================================================

st.markdown(
    '<div class="main-title">🛡️ DataSentinel AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Intelligent Dataset Quality & ML Readiness Auditor'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =====================================================
# 7. ABOUT PROJECT PAGE
# =====================================================

if page == "About Project":

    st.header("🚀 About DataSentinel AI")

    st.markdown("""
    <div class="section-card">
        <h3>Intelligent Dataset Analysis</h3>
        <p>
        DataSentinel AI is a multi-agent artificial intelligence
        application that analyzes CSV datasets, identifies data
        quality problems, evaluates machine learning risks and
        provides preprocessing recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Our Specialist Agents")

    with st.expander("🔍 Agent 1 - Data Quality Auditor"):
        st.write("""
        Identifies missing values, duplicate records,
        incorrect data types and data quality problems.
        """)

    with st.expander("⚠️ Agent 2 - ML Risk Analyst"):
        st.write("""
        Evaluates target variables, possible data leakage,
        class imbalance when counts are available and
        potential fairness concerns.
        """)

    with st.expander("🧠 Agent 3 - ML Strategy Advisor"):
        st.write("""
        Recommends data cleaning, imputation, encoding,
        scaling, suitable machine learning algorithms
        and evaluation metrics.
        """)

    with st.expander("📊 Agent 4 - Final Report Generator"):
        st.write("""
        Combines the findings from all specialist agents
        into a structured dataset analysis report.
        """)

    st.subheader("Technology Stack")

    st.write("""
    Python | Pandas | Streamlit | n8n |
    Google Gemini | Multi-Agent AI
    """)


# =====================================================
# 8. DATASET ANALYZER PAGE
# =====================================================

else:

    st.header("📂 Upload Your Dataset")

    st.write(
        "Upload your CSV file to explore your dataset "
        "and perform AI-powered analysis."
    )

    uploaded_file = st.file_uploader(
        "Choose your CSV dataset",
        type=["csv"],
        help="Upload a CSV file for dataset analysis."
    )

    target_column = st.text_input(
        "🎯 Target Column Name (Optional)",
        placeholder="Example: churn"
    )

    df = None

    # =================================================
    # 9. READ CSV
    # =================================================

    if uploaded_file is not None:

        try:

            df = pd.read_csv(uploaded_file)

            if df.empty:
                st.error("The uploaded CSV contains no records.")
                df = None

            elif len(df.columns) == 0:
                st.error("No columns were found in the CSV.")
                df = None

            else:
                st.success("✅ Dataset uploaded successfully!")

        except Exception as e:

            st.error(f"Unable to read CSV: {e}")
            df = None

    # =================================================
    # 10. DATASET OVERVIEW
    # =================================================

    if df is not None:

        st.divider()

        st.header("📊 Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Rows",
            f"{df.shape[0]:,}"
        )

        col2.metric(
            "Total Columns",
            f"{df.shape[1]:,}"
        )

        col3.metric(
            "Missing Values",
            f"{int(df.isnull().sum().sum()):,}"
        )

        col4.metric(
            "Duplicate Rows",
            f"{int(df.duplicated().sum()):,}"
        )

        # =============================================
        # 11. INTERACTIVE TABS
        # =============================================

        st.subheader("🔎 Explore Your Dataset")

        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Data Preview",
            "📈 Missing Values",
            "🔍 Column Details",
            "📊 Data Statistics"
        ])

        with tab1:

            st.subheader("Dataset Records")

            st.dataframe(
                df.head(20),
                use_container_width=True,
                height=350
            )

        with tab2:

            st.subheader("Missing Values Analysis")

            missing = df.isnull().sum()
            missing = missing[missing > 0]

            if not missing.empty:

                st.bar_chart(
                    missing,
                    color="#8B5CF6"
                )

                st.dataframe(
                    missing.rename("Missing Count"),
                    use_container_width=True
                )

            else:

                st.success("🎉 No missing values found!")

        with tab3:

            st.subheader("Column Information")

            info_df = pd.DataFrame({
                "Column": df.columns,
                "Data Type": [
                    str(dtype) for dtype in df.dtypes
                ],
                "Non-Null Count": df.notnull().sum().values,
                "Unique Values": df.nunique().values
            })

            st.dataframe(
                info_df,
                use_container_width=True
            )

        with tab4:

            st.subheader("Numerical Data Statistics")

            numeric_df = df.select_dtypes(
                include="number"
            )

            if not numeric_df.empty:

                st.dataframe(
                    numeric_df.describe().round(2),
                    use_container_width=True
                )

            else:

                st.info(
                    "No numerical columns are available "
                    "for statistical analysis."
                )

        # =============================================
        # 12. TARGET COLUMN
        # =============================================

        if target_column.strip():

            if target_column not in df.columns:

                st.warning(
                    f"Target column '{target_column}' "
                    "does not exist in this dataset."
                )

            else:

                st.success(
                    f"🎯 Target column selected: {target_column}"
                )

        # =============================================
        # 13. AI ANALYSIS
        # =============================================

        st.divider()

        st.header("🤖 AI-Powered Dataset Analysis")

        st.write(
            "Four specialist AI agents will analyze "
            "your dataset and prepare a detailed report."
        )

        if st.button(
            "🚀 Analyze Dataset",
            use_container_width=True
        ):

            if df is None:

                st.warning("Please upload a valid CSV file.")

            elif not N8N_WEBHOOK_URL:

                st.error(
                    "n8n Webhook URL is not configured. "
                    "We need to connect your n8n workflow first."
                )

            elif target_column.strip() and target_column not in df.columns:

                st.error(
                    "Please enter a valid target column name "
                    "or leave it empty."
                )

            else:

                with st.spinner(
                    "🤖 AI agents are analyzing your dataset..."
                ):

                    try:

                        uploaded_file.seek(0)

                        files = {
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "text/csv"
                            )
                        }

                        data = {
                            "target_column": target_column
                        }

                        response = requests.post(
                            N8N_WEBHOOK_URL,
                            files=files,
                            data=data,
                            timeout=300
                        )

                        response.raise_for_status()

                        result = response.json()

                        report = result.get("report", "")

                        if report:

                            st.session_state.report = report

                            st.session_state.report_file_name = (
                                uploaded_file.name
                            )

                            st.success(
                                "🎉 Dataset analysis completed!"
                            )

                        else:

                            st.error(
                                "No report was received from n8n."
                            )

                            st.json(result)

                    except requests.exceptions.Timeout:

                        st.error(
                            "Analysis timed out. Please try again."
                        )

                    except requests.exceptions.RequestException as e:

                        st.error(
                            f"Unable to connect to n8n: {e}"
                        )

                    except Exception as e:

                        st.error(
                            f"Unexpected error: {e}"
                        )

        # =============================================
        # 14. DISPLAY AI REPORT
        # =============================================

        if st.session_state.report:

            st.divider()

            st.header("📑 DataSentinel AI Analysis Report")

            st.markdown(
                st.session_state.report
            )

            st.download_button(
                label="⬇️ Download Analysis Report",
                data=st.session_state.report,
                file_name="DataSentinel_AI_Report.md",
                mime="text/markdown",
                use_container_width=True
            )


# =====================================================
# 15. FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    color:#475569;
    padding:15px;
    font-size:14px;
">
    🛡️ <b>DataSentinel AI</b><br>
    Intelligent Dataset Quality & ML Readiness Auditor<br>
    Powered by Multi-Agent Artificial Intelligence
</div>
""", unsafe_allow_html=True)
