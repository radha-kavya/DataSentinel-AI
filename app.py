import streamlit as st
import requests
import pandas as pd
import os

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="DataSentinel AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------------------------------
# CUSTOM DESIGN
# ---------------------------------

st.title("🛡️ DataSentinel AI")
st.subheader("Intelligent Dataset Quality & ML Readiness Auditor")

st.write(
    "Upload your dataset to identify data quality issues, "
    "machine learning risks, and preprocessing recommendations."
)

st.divider()

# ---------------------------------
# N8N WEBHOOK CONFIGURATION
# ---------------------------------

N8N_WEBHOOK_URL = st.secrets.get(
    "N8N_WEBHOOK_URL",
    ""
)

# ---------------------------------
# DATASET UPLOAD
# ---------------------------------

st.header("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

target_column = st.text_input(
    "Target Column Name (Optional)",
    placeholder="Example: churn"
)

# ---------------------------------
# DATASET PREVIEW
# ---------------------------------

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)

        st.success("Dataset uploaded successfully!")

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", int(df.isnull().sum().sum()))

        st.subheader("Dataset Preview")

        st.dataframe(df.head(10), use_container_width=True)

        st.subheader("Column Names")

        st.write(list(df.columns))

    except Exception as e:
        st.error(f"Unable to read CSV: {e}")

# ---------------------------------
# ANALYSIS
# ---------------------------------

st.divider()

if st.button("🔍 Analyze Dataset", use_container_width=True):

    if uploaded_file is None:

        st.warning("Please upload a CSV file first.")

    elif not N8N_WEBHOOK_URL:

        st.error("n8n Webhook URL is not configured yet.")

    else:

        with st.spinner("DataSentinel AI is analyzing your dataset..."):

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

                    st.success("Dataset analysis completed!")

                    st.header("📊 DataSentinel AI Report")

                    st.markdown(report)

                    st.download_button(
                        label="⬇️ Download Analysis Report",
                        data=report,
                        file_name="DataSentinel_AI_Report.md",
                        mime="text/markdown"
                    )

                else:

                    st.error(
                        "Analysis completed, but no report was returned. "
                        "Please check the n8n response."
                    )

                    st.json(result)

            except requests.exceptions.Timeout:

                st.error("Analysis timed out. Please try again.")

            except requests.exceptions.RequestException as e:

                st.error(f"Connection to n8n failed: {e}")

            except Exception as e:

                st.error(f"Unexpected error: {e}")

# ---------------------------------
# FOOTER
# ---------------------------------

st.divider()

st.caption(
    "DataSentinel AI | Multi-Agent Dataset Quality & ML Readiness Auditor"
)