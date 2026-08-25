import sys
import os

# Standardize sys.path so 'design', 'app', and root packages resolve deterministically
FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(FRONTEND_DIR)
PROJECT_DIR = os.path.dirname(APP_DIR)

for path in [FRONTEND_DIR, APP_DIR, PROJECT_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

import streamlit as st

st.set_page_config(
    page_title="RailHelpAI — AI Railway Operations Platform",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

from design.styles import inject_custom_css

# Configure multipage app shell with st.navigation & st.Page
command_center = st.Page("pages/01_Overview.py", title="Command Center", icon="📊", default=True)
submit_complaint = st.Page("pages/02_Submit_Complaint.py", title="Submit Complaint", icon="📝")
complaint_queue = st.Page("pages/04_Complaint_Queue.py", title="Complaint Queue", icon="📋")
human_review = st.Page("pages/06_Human_Review_Queue.py", title="Human Review Queue", icon="🔍")
sla_monitor = st.Page("pages/05_SLA_Monitor.py", title="SLA Monitor", icon="⏱️")

ai_analysis = st.Page("pages/03_AI_Analysis.py", title="AI Analysis", icon="🤖")
incident_clusters = st.Page("pages/10_Incident_Clusters.py", title="Incident Clusters", icon="🧩")
train_intel = st.Page("pages/08_Train_Intelligence.py", title="Train Intelligence", icon="🚆")
station_intel = st.Page("pages/09_Station_Intelligence.py", title="Station Intelligence", icon="🚉")
executive_intel = st.Page("pages/11_Executive_Intelligence.py", title="Executive Intelligence", icon="📈")

complaint_detail = st.Page("pages/07_Complaint_Detail.py", title="Complaint Detail", icon="🔎")

pg = st.navigation(
    {
        "OVERVIEW": [command_center],
        "COMPLAINT OPERATIONS": [submit_complaint, complaint_queue, human_review, sla_monitor],
        "INTELLIGENCE": [ai_analysis, incident_clusters, train_intel, station_intel, executive_intel],
        "SYSTEM": [complaint_detail]
    }
)

# Sidebar Header Branding
st.sidebar.markdown(
    """
    <div style="padding: 0.5rem 0; border-bottom: 1px solid #E1E4E8; margin-bottom: 1rem;">
        <div style="font-size: 1.1rem; font-weight: 700; color: #C8102E; letter-spacing: 0.05em;">RAILHELPAI</div>
        <div style="font-size: 0.7rem; color: #5A6672; font-weight: 500;">AI Railway Operations Platform</div>
    </div>
    """,
    unsafe_allow_html=True
)

inject_custom_css()
pg.run()
