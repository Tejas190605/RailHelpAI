import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import time
from design.layout import setup_app_layout
from design.components import render_page_header, get_priority_badge_html, get_status_badge_html
from utils_api import create_complaint

setup_app_layout("Submit Complaint")

render_page_header(
    title="Submit Passenger Complaint",
    subtitle="Capture passenger grievance with guided AI intelligence analysis and automated routing."
)

form_col, info_col = st.columns([3, 2])

with form_col:
    with st.form("guided_submission_form"):
        st.markdown("### 📝 Incident Information")
        complaint_text = st.text_area("Grievance Description *", placeholder="Describe the issue (e.g., AC is not cooling in coach B4 seat 21 since Pune)...", height=120)
        
        c1, c2 = st.columns(2)
        with c1:
            train_number = st.text_input("Train Number", placeholder="e.g. 12951")
            coach = st.text_input("Coach", placeholder="e.g. B4")
        with c2:
            station = st.text_input("Station", placeholder="e.g. Pune")
            seat = st.text_input("Seat / Berth", placeholder="e.g. 21")

        st.markdown("### 📷 Evidence Upload (Optional)")
        uploaded_file = st.file_uploader("Attach Photo / Ticket Image", type=["jpg", "jpeg", "png"], help="Max file size 5.0 MB")

        submitted = st.form_submit_button("🚀 Submit & Analyze Grievance", type="primary")

        if submitted:
            if not complaint_text or len(complaint_text.strip()) < 5:
                st.error("Please enter a valid complaint description (at least 5 characters).")
            else:
                progress_placeholder = st.empty()
                with progress_placeholder.container():
                    st.info("⚙️ **ANALYZING INCIDENT...**")
                    time.sleep(0.2)

                payload = {
                    "complaint_text": complaint_text.strip(),
                    "train_number": train_number.strip() if train_number else None,
                    "station": station.strip() if station else None,
                    "coach": coach.strip() if coach else None,
                    "seat": seat.strip() if seat else None
                }

                res = create_complaint(payload)
                progress_placeholder.empty()

                if res.get("success"):
                    data = res.get("data", {})
                    st.success(f"✅ Complaint successfully submitted and logged! Reference ID: `{data.get('complaint_id')}`")
                    
                    st.markdown("---")
                    st.markdown("### 🤖 Initial AI Assessment")
                    k1, k2, k3 = st.columns(3)
                    k1.markdown(f"**Category:** `{data.get('complaint_type')}`")
                    k2.markdown(f"**Priority:** {get_priority_badge_html(data.get('priority'))}", unsafe_allow_html=True)
                    k3.markdown(f"**Department:** `{data.get('department')}`")
                else:
                    st.error(f"Error submitting complaint: {res.get('error')}")

with info_col:
    st.markdown("### ℹ️ Operational Guidance")
    st.info(
        "• **P1 Critical:** Life-threatening, fire, medical emergencies, security threats.\n"
        "• **P2 High:** Utility failures (Air Conditioning, major water leakage).\n"
        "• **P3/P4 Medium-Low:** General cleanliness, catering, minor fixtures."
    )
