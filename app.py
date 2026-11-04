
import streamlit as st
import pandas as pd
import requests
import os

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="DataSentinel AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #F4F7FF, #F9F5FF);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #172554, #312E81);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg, #2563EB, #9333EA, #0891B2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #64748B;
    font-size: 17px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    box-shadow: 0px 4px 15px rgba(50, 60, 120, 0.08);
}

.section-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    margin-bottom: 15px;
}

.stButton > button {
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    min-height: 48px;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1D4ED8, #6D28D9);
    color: white;
    border: none;
}

.stDownloadButton > button {
    background: linear-gradient(90deg, #059669, #0D9488);
    color: white;
    border: none;
    border-radius: 10px;
    min-height: 45px;
}

div[data-testid="stFileUploader"] {
    background: white;
    padding: 15px;
    border-radius: 15px;
    border: 1px dashed #818CF8;
}

h1, h2, h3 {
    color: #172554;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. N8N CONFIGURATION
# ==========================================

try:
    N8N_WEBHOOK_URL = st.secrets.get(
        "N8N_WEBHOOK_URL", ""
    )
except Exception:
    N8N_WEBHOOK_URL = os.getenv(
        "N8N_WEBHOOK_URL", ""
    )

# ==========================================
# 4. SIDEBAR
# ==========================================

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

    st.markdown("### 🤖 AI Agents")

    st.markdown("""
    🔹 Data Quality Auditor

    🔹 ML Risk Analyst

    🔹 ML Strategy Advisor

    🔹 Final Report Generator
    """)

    st.markdown("---")

    st.caption("Multi-Agent AI System")

    st.caption("Developed with Streamlit + n8n")

# ==========================================
# 5. MAIN HEADER
# ==========================================

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

st.write("")

# ==========================================
# 6. ABOUT PAGE
# ==========================================

if page == "About Project":

    st.header("🚀 About DataSentinel AI")

    st.markdown("""
    <div class="section-card">
    <h3>Intelligent Dataset Analysis</h3>
    DataSentinel AI is a multi-agent AI application
    that evaluates CSV datasets and generates
    machine learning readiness recommendations.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Our AI Agents")

    agents = [
        ("🔍 Data Quality Auditor",
         "Identifies missing values, duplicates and data types."),
        ("⚠️ ML Risk Analyst",
         "Evaluates target variables, data risks and possible leakage."),
        ("🧠 ML Strategy Advisor",
         "Suggests preprocessing and suitable ML models."),
        ("📊 Final Report Generator",
         "Creates a comprehensive dataset analysis report.")
    ]

    for name, description in agents:
        with st.expander(name):
            st.write(description)

    st.subheader("Technology Stack")

    st.write(
        "Python | Streamlit | n8n | Google Gemini | "
        "Pandas | Multi-Agent AI"
    )

# ==========================================
# 7. DATASET ANALYZER PAGE
# ==========================================

else:

    st.header("📂 Dataset Upload")

    st.write(
        "Upload any CSV dataset to explore its structure "
        "and generate an AI-powered analysis."
    )

    uploaded_file = st.file_uploader(
        "Choose your CSV dataset",
        type=["csv"],
        help="Upload a CSV file containing your dataset."
    )

    target_column = st.text_input(
        "🎯 Target Column (Optional)",
        placeholder="Example: churn"
    )

    df = None

    # ======================================
    # 8. DATASET PREVIEW
    # ======================================

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file)

            if df.empty:
                st.error("The uploaded CSV is empty.")
                df = None

            elif len(df.columns) == 0:
                st.error("No columns found in the CSV.")
                df = None

            else:
                st.success("✅ Dataset uploaded successfully!")

        except Exception as e:
            st.error(f"CSV reading error: {e}")

    if df is not None:

        st.markdown("---")

        st.header("📊 Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Rows", f"{df.shape[0]:,}")

        col2.metric("Total Columns", f"{df.shape[1]:,}")

        col3.metric(
            "Missing Values",
            f"{int(df.isnull().sum().sum()):,}"
        )

        col4.metric(
            "Duplicate Rows",
            f"{int(df.duplicated().sum()):,}"
        )

        # ==================================
        # 9. INTERACTIVE TABS
        # ==================================

        tab1, tab2, tab3 = st.tabs([
            "📋 Data Preview",
            "📈 Missing Values",
            "🔎 Column Information"
        ])

        with tab1:

            st.subheader("Dataset Preview")

            st.dataframe(
                df.head(20),
                use_container_width=True,
                height=350
            )

        with tab2:

            st.subheader("Missing Values Analysis")

            missing = df.isnull().sum()

            missing = missing[missing > 0]

            if len(missing) > 0:

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

        # ==================================
        # 10. TARGET COLUMN VALIDATION
        # ==================================

        if target_column.strip():

            if target_column not in df.columns:
                st.warning(
                    f"Target column '{target_column}' "
                    "was not found in the dataset."
                )

            else:
                st.info(
                    f"🎯 Selected target column: {target_column}"
                )

        # ==================================
        # 11. AI ANALYSIS
        # ==================================

        st.markdown("---")

        st.header("🤖 AI-Powered Dataset Analysis")

        st.write(
            "Our four specialist agents will analyze "
            "your dataset and prepare a report."
        )

        if st.button(
            "🚀 Analyze Dataset",
            use_container_width=True
        ):

            if df is None:

                st.warning("Please upload a valid CSV first.")

            elif not N8N_WEBHOOK_URL:

                st.error(
                    "n8n Webhook URL is not configured yet. "
                    "We will connect it during deployment."
                )

            else:

                with st.spinner(
                    "🤖 DataSentinel AI agents are working..."
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

                            st.session_state["report"] = report

                            st.success(
                                "🎉 Dataset analysis completed!"
                            )

                        else:

                            st.error(
                                "No report received from n8n."
                            )

                            st.json(result)

                    except requests.exceptions.Timeout:

                        st.error(
                            "Analysis timed out. Please try again."
                        )

                    except requests.exceptions.RequestException as e:

                        st.error(
                            f"Connection error: {e}"
                        )

                    except Exception as e:

                        st.error(
                            f"Unexpected error: {e}"
                        )

        # ==================================
        # 12. DISPLAY REPORT
        # ==================================

        if st.session_state.get("report"):

            st.markdown("---")

            st.header("📑 DataSentinel AI Report")

            st.markdown(
                st.session_state["report"]
            )

            st.download_button(
                "⬇️ Download Analysis Report",
                data=st.session_state["report"],
                file_name="DataSentinel_AI_Report.md",
                mime="text/markdown",
                use_container_width=True
            )

# ==========================================
# 13. FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#64748B;">
        🛡️ <b>DataSentinel AI</b><br>
        Intelligent Dataset Quality & ML Readiness Auditor<br>
        Powered by Multi-Agent AI
    </div>
    """,
    unsafe_allow_html=True
)
