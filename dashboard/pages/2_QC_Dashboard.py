
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://api:8000/api/v1"

st.set_page_config(page_title="QC Dashboard", layout="wide")

st.title("Quality Control (QC) Dashboard")

# --- Data Fetching ---
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_all_qc_data():
    try:
        # This assumes your API has an endpoint to get all QC metrics
        # We will need to add this to the FastAPI backend.
        response = requests.get(f"{API_URL}/qc_metrics/all/") # Placeholder
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException:
        # Fallback to fetching samples and extracting QC
        try:
            response = requests.get(f"{API_URL}/samples/?limit=1000")
            response.raise_for_status()
            samples = response.json()
            qc_list = []
            for sample in samples:
                if sample.get("qc_metrics"):
                    for qc in sample["qc_metrics"]:
                        qc["patient_id"] = sample["patient_id"]
                        qc_list.append(qc)
            return pd.DataFrame(qc_list)
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data from API: {e}")
            return pd.DataFrame()

# --- Main Page ---
df_qc = get_all_qc_data()

if not df_qc.empty:
    st.header("Overall QC Metrics Distribution")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Mapping Rate (%)")
        fig = px.histogram(df_qc, x="mapping_rate", nbins=20, title="Distribution of Mapping Rates")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Mean Coverage (X)")
        fig = px.histogram(df_qc, x="mean_coverage", nbins=20, title="Distribution of Mean Coverage")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Duplicate Rate (%)")
        fig = px.histogram(df_qc, x="duplicate_rate", nbins=20, title="Distribution of Duplicate Rates")
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Q30 Percentage (%)")
        fig = px.histogram(df_qc, x="q30_percentage", nbins=20, title="Distribution of Q30 Percentage")
        st.plotly_chart(fig, use_container_width=True)

    st.header("QC Metrics Scatter Plots")
    
    scatter_x = st.selectbox("Select X-axis", options=df_qc.columns, index=list(df_qc.columns).index("mapping_rate"))
    scatter_y = st.selectbox("Select Y-axis", options=df_qc.columns, index=list(df_qc.columns).index("mean_coverage"))
    
    fig_scatter = px.scatter(df_qc, x=scatter_x, y=scatter_y, hover_data=["sample_id", "patient_id"], title=f"{scatter_y} vs. {scatter_x}")
    st.plotly_chart(fig_scatter, use_container_width=True)

else:
    st.warning("No QC data available to display.")
