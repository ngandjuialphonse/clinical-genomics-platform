
import streamlit as st
import pandas as pd
import requests

API_URL = "http://api:8000/api/v1"

st.set_page_config(page_title="Sample Tracking", layout="wide")

st.title("Sample Tracking Dashboard")

# --- Data Fetching ---
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def get_samples_data(patient_id=None, status=None):
    params = {}
    if patient_id:
        params["patient_id"] = patient_id
    if status and status != "All":
        params["status"] = status

    try:
        response = requests.get(f"{API_URL}/samples/", params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from API: {e}")
        return pd.DataFrame()

# --- Sidebar Filters ---
st.sidebar.header("Filters")
patient_id_filter = st.sidebar.text_input("Filter by Patient ID")
status_filter = st.sidebar.selectbox(
    "Filter by Status",
    ["All", "received", "analysis", "qc_review", "complete", "failed"],
)

# --- Main Page ---
df = get_samples_data(patient_id=patient_id_filter, status=status_filter)

if not df.empty:
    st.metric("Total Samples", len(df))
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No samples found with the selected filters.")

# --- Detailed View ---
st.header("Detailed Sample View")
sample_id_to_view = st.number_input("Enter Sample ID to view details", min_value=1, step=1)

if st.button("Get Sample Details"):
    try:
        response = requests.get(f"{API_URL}/samples/{sample_id_to_view}")
        response.raise_for_status()
        sample_details = response.json()

        st.subheader(f"Details for Sample ID: {sample_details["id"]}")
        col1, col2, col3 = st.columns(3)
        col1.metric("External ID", sample_details["external_id"])
        col2.metric("Patient ID", sample_details["patient_id"])
        col3.metric("Status", sample_details["status"])

        st.write("**QC Metrics:**")
        if sample_details["qc_metrics"]:
            st.dataframe(pd.DataFrame(sample_details["qc_metrics"]), use_container_width=True)
        else:
            st.info("No QC metrics available for this sample.")

        st.write("**Pipeline Runs:**")
        if sample_details["pipeline_runs"]:
            st.dataframe(pd.DataFrame(sample_details["pipeline_runs"]), use_container_width=True)
        else:
            st.info("No pipeline runs available for this sample.")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching details for sample {sample_id_to_view}: {e}")
