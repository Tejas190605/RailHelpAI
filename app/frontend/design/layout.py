import streamlit as st
from app.frontend.design.styles import inject_custom_css


def setup_app_layout(page_title: str):
    """Setup page configuration and inject design system CSS."""
    st.set_page_config(
        page_title=f"{page_title} — RailHelpAI",
        page_icon="🚆",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    inject_custom_css()
