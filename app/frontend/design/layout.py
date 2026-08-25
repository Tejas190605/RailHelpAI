from design.styles import inject_custom_css


def setup_app_layout(page_title: str = None):
    """Inject design system CSS into the Streamlit workstation page."""
    inject_custom_css()
