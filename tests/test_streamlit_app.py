from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

FRONTEND_APP_PATH = Path(__file__).parent.parent / "app" / "frontend" / "app.py"
PAGES_DIR = Path(__file__).parent.parent / "app" / "frontend" / "pages"


def test_streamlit_entrypoint_app():
    """Verify entrypoint app.py loads cleanly and renders navigation shell."""
    at = AppTest.from_file(FRONTEND_APP_PATH, default_timeout=10).run()
    assert not at.exception
    assert len(at.markdown) > 0


def test_page_01_command_center():
    """Verify 01 Command Center page loads cleanly."""
    at = AppTest.from_file(PAGES_DIR / "01_Overview.py", default_timeout=10).run()
    assert not at.exception
    assert len(at.markdown) > 0


def test_page_02_submit_complaint_form_submission():
    """Verify 02 Submit Complaint form submission interaction."""
    at = AppTest.from_file(PAGES_DIR / "02_Submit_Complaint.py", default_timeout=10).run()
    assert not at.exception
    assert len(at.text_area) > 0
    assert len(at.text_input) >= 2
    
    # Fill in grievance form
    at.text_area[0].input("AC is not cooling in coach B4 seat 21 on train 12951 since Pune.").run()
    assert not at.exception


def test_page_03_ai_analysis_interaction():
    """Verify 03 AI Analysis page renders text area and triggers assessment."""
    at = AppTest.from_file(PAGES_DIR / "03_AI_Analysis.py", default_timeout=10).run()
    assert not at.exception
    assert len(at.text_area) > 0
    
    # Input text and click assessment button
    at.text_area[0].input("Water leakage in coach A2 seat 10 near Surat.").run()
    assert not at.exception


def test_page_04_complaint_queue():
    """Verify 04 Complaint Queue page loads cleanly."""
    at = AppTest.from_file(PAGES_DIR / "04_Complaint_Queue.py", default_timeout=10).run()
    assert not at.exception


def test_page_05_sla_monitor():
    """Verify 05 SLA Monitor page loads cleanly."""
    at = AppTest.from_file(PAGES_DIR / "05_SLA_Monitor.py", default_timeout=10).run()
    assert not at.exception


def test_page_06_human_review_queue():
    """Verify 06 Human Review Queue page loads cleanly."""
    at = AppTest.from_file(PAGES_DIR / "06_Human_Review_Queue.py", default_timeout=10).run()
    assert not at.exception


def test_page_07_complaint_detail():
    """Verify 07 Complaint Detail page loads cleanly."""
    at = AppTest.from_file(PAGES_DIR / "07_Complaint_Detail.py", default_timeout=10).run()
    assert not at.exception


def test_page_08_train_intelligence():
    """Verify 08 Train Intelligence page loads cleanly."""
    at = AppTest.from_file(PAGES_DIR / "08_Train_Intelligence.py", default_timeout=10).run()
    assert not at.exception


def test_page_09_station_intelligence():
    """Verify 09 Station Intelligence page loads cleanly."""
    at = AppTest.from_file(PAGES_DIR / "09_Station_Intelligence.py", default_timeout=10).run()
    assert not at.exception


def test_page_10_incident_clusters():
    """Verify 10 Incident Clusters page loads cleanly."""
    at = AppTest.from_file(PAGES_DIR / "10_Incident_Clusters.py", default_timeout=10).run()
    assert not at.exception


def test_page_11_executive_intelligence():
    """Verify 11 Executive Intelligence page loads cleanly."""
    at = AppTest.from_file(PAGES_DIR / "11_Executive_Intelligence.py", default_timeout=10).run()
    assert not at.exception
