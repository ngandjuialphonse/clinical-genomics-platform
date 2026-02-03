'''
Main Streamlit Application - Entry Point

This is the main page for the Streamlit dashboard.
It serves as the landing page and provides an overview of the platform.

KEY STREAMLIT CONCEPTS:
---------------------
- st.set_page_config: Sets the page title, icon, and layout.
- st.title, st.header, st.markdown: Used for displaying text.
- Multi-page apps: Streamlit automatically creates a sidebar for navigation
  when you have a `pages/` directory.
'''

import streamlit as st

st.set_page_config(
    page_title="Clinical Genomics QC Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🧬 Clinical Genomics QC & Monitoring Platform")

st.markdown('''
Welcome to the central dashboard for monitoring clinical genomics operations.

This platform provides real-time insights into sample tracking, pipeline status, and quality control (QC) metrics from the bioinformatics analysis pipelines.

### How to Use This Dashboard

- **Sample Tracking**: Navigate to the `Sample Tracking` page to view the status of all samples in the system, from receipt to analysis completion.
- **QC Dashboard**: Go to the `QC Dashboard` to visualize key quality metrics across all samples and sequencing runs. This is crucial for identifying trends, detecting batch effects, and ensuring data quality.

This dashboard is powered by a **FastAPI** backend and a **PostgreSQL** database, demonstrating a full-stack approach to building bioinformatics platforms.
''')

st.info("Select a page from the sidebar to get started.", icon="👈")
