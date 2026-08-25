import streamlit as st

GLOBAL_CSS = """
<style>
/* Global Font & Sans-Serif Typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #1E242B;
}

/* Page Header & Container Styling */
.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1300px;
}

/* Custom Card Container */
.rail-card {
    background-color: #FFFFFF;
    border: 1px solid #E1E4E8;
    border-radius: 8px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.rail-card-title {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #5A6672;
    margin-bottom: 0.5rem;
}

.rail-card-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #1E242B;
    line-height: 1.2;
}

.rail-card-sublabel {
    font-size: 0.75rem;
    color: #6B7280;
    margin-top: 0.25rem;
}

/* Semantic Badges */
.rail-badge {
    display: inline-block;
    padding: 0.2rem 0.5rem;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 4px;
    border: 1px solid transparent;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

/* Operational Header Strip */
.operational-header {
    background-color: #1E242B;
    color: #FFFFFF;
    padding: 1.25rem 1.5rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    border-left: 4px solid #C8102E;
}

.operational-header h1 {
    font-size: 1.4rem;
    font-weight: 700;
    margin: 0;
    color: #FFFFFF;
    letter-spacing: 0.02em;
}

.operational-header p {
    font-size: 0.85rem;
    color: #9CA3AF;
    margin: 0.25rem 0 0 0;
}

/* Streamlit Native Widget Cleanups */
.stButton > button {
    border-radius: 6px;
    font-weight: 600;
    border: 1px solid #D1D5DB;
}

.stDataFrame {
    border-radius: 6px;
    border: 1px solid #E1E4E8;
}
</style>
"""


def inject_custom_css():
    """Inject centralized RailHelpAI CSS tokens once into the Streamlit page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
