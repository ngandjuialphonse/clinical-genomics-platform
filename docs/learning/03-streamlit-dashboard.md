# Learning Module 3: Creating the Streamlit Dashboard

This module explains how we built the interactive frontend for our platform using Streamlit.

## Why Streamlit?

Streamlit is a Python library that makes it easy to create beautiful, custom web apps for machine learning and data science. We chose it because:

-   **Pure Python:** We can build a reactive frontend without writing any HTML, CSS, or JavaScript.
-   **Fast Development:** It's incredibly fast to go from a data script to a shareable web app.
-   **Great for Data:** It has built-in components for displaying dataframes, charts, and more.

## Our Dashboard Structure

Our dashboard is a multi-page application:

1.  **`app.py`**: The main landing page.
2.  **`pages/1_Sample_Tracking.py`**: A page for viewing and filtering all samples.
3.  **`pages/2_QC_Dashboard.py`**: A page for visualizing QC metrics.

Streamlit automatically creates the sidebar navigation based on the files in the `pages/` directory.

## How it Works

The dashboard is a **consumer** of our FastAPI backend. It uses the `requests` library to make HTTP calls to the API endpoints we created.

**Key Features:**
-   **Caching:** We use `st.cache_data` to cache the data from the API, so the dashboard is fast and doesn't overload the backend.
-   **Interactive Filtering:** Users can filter the data using sidebar widgets.
-   **Data Visualization:** We use Plotly Express to create interactive charts and graphs.

